# ⚠️ HISTORICAL DEMO
# This file is retained for provenance only.
# It does NOT represent current Aurora behavior.
# Run demo/aurora_cli_demo.py instead.

raise RuntimeError(
    "This demo is historical. Run demo/aurora_cli_demo.py instead."
)
#!/usr/bin/env python3
"""
Aurora CLI Demo (Minimal Invariants) — v4
Generalized + Optional Adjective + Corrected Pronoun Capture (no "cat is" / "brother is" capture)

Key fixes in v4:
- Explicit assertions support: "<Name> has|had a/an <obj>." where <obj> is:
    - noun ("cat")
    - adjective + noun ("black cat")
- Ambiguous spans support: "(her|his|their) <obj>" with the SAME object shape,
  BUT pronoun-object capture will NOT accidentally absorb the next verb:
    - "her brother is tall" -> captures obj="brother" (NOT "brother is")
    - "their cat is cute"   -> captures obj="cat"     (NOT "cat is")
    - "his black cat is..." -> captures obj="black cat"

Design invariants enforced:
- Ambiguity => STOP + clarification question about the utterance
- No fact invention: only explicit assertions update state
- No constraint application unless prerequisites are satisfied
- Constrained answers only; elaboration ignored
- Deterministic collapse when admissible
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

SHOW_JSON = False  # flip to True if you want full traces

PRONOUNS = {
    "i", "me", "my", "mine",
    "we", "us", "our", "ours",
    "you", "your", "yours",
    "he", "him", "his",
    "she", "her", "hers",
    "they", "them", "their", "theirs",
    "it", "its",
}

STOPWORDS = {
    "a", "an", "the", "this", "that", "these", "those",
    "and", "or", "but", "if", "then", "because",
}

# Tokens we treat as "not part of the object" when they appear immediately after the object.
# (Stops "cat is", "brother was", "dog will", etc.)
DISALLOWED_OBJ_TAIL = {
    "is", "was", "are", "were", "be", "been", "being",
    "am",
    "do", "does", "did",
    "has", "have", "had",
    "will", "would", "shall", "should",
    "can", "could", "may", "might", "must",
    "to",
}

# ----------------------------
# Data structures
# ----------------------------

@dataclass
class Fact:
    subject: str
    relation: str
    obj: str  # normalized object: "cat" or "black cat"


@dataclass
class Ambiguity:
    ambig_id: str
    ambig_type: str  # "reference"
    span: str        # e.g. "her sister" / "his black cat"
    slot: str        # her / his / their
    obj: str         # "sister" / "black cat"
    candidates: List[str]
    question: str
    allowed_answers: Dict[str, str]


@dataclass
class State:
    entities: Dict[str, Dict] = field(default_factory=dict)
    facts: List[Fact] = field(default_factory=list)
    bindings: Dict[str, str] = field(default_factory=dict)

    suspended_utterance: Optional[str] = None
    suspended_ambiguity: Optional[Ambiguity] = None

    pending_ambiguity: Optional[Ambiguity] = None
    turn_index: int = 0


# ----------------------------
# Helpers
# ----------------------------

ENTITY_PATTERN = re.compile(r"\b([A-Z][a-z]+)\b")

def normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def normalize_obj(s: str) -> str:
    return normalize_ws(s.lower())

def ensure_entity(state: State, name: str) -> None:
    if name not in state.entities:
        state.entities[name] = {"name": name}

def add_fact(state: State, subject: str, relation: str, obj: str) -> None:
    state.facts.append(Fact(subject=subject, relation=relation, obj=obj))


# ----------------------------
# Patterns
# ----------------------------

# Explicit assertion:
#   "<Name> has a/an <noun>" OR "<Name> had a/an <noun>"
#   optional adjective:
#   "<Name> has a black cat." / "<Name> had a white cat."
HAS_OBJ_PATTERN = re.compile(
    r"^\s*([A-Z][a-z]+)\s+(has|had)\s+a[n]?\s+([a-z]+(?:\s+[a-z]+)?)\s*\.?\s*$",
    re.IGNORECASE
)

# Corrected pronoun-object capture:
#   "(her|his|their) <w1> [<w2>]"
# where <w2> is optional BUT we will IGNORE it if it's a tail verb/aux token.
#
# This is the crucial change vs v3: we capture one required token + one optional token,
# then decide whether token2 is part of the object, instead of allowing a 2-token object
# and later vetoing, which caused misses like "her brother is tall".
PRONOUN_W1_W2_PATTERN = re.compile(
    r"\b(her|his|their)\s+([a-z]+)(?:\s+([a-z]+))?\b",
    re.IGNORECASE
)


# ----------------------------
# Parsing
# ----------------------------

def parse_and_update_state(state: State, utterance: str) -> Dict:
    parse_record = {
        "recognized_assertions": [],
        "recognized_entities": [],
        "recognized_ambiguous_spans": [],
    }

    # entity extraction
    for m in ENTITY_PATTERN.finditer(utterance):
        name = m.group(1)
        low = name.lower()
        if low in PRONOUNS or low in STOPWORDS:
            continue
        ensure_entity(state, name)
        if name not in parse_record["recognized_entities"]:
            parse_record["recognized_entities"].append(name)

    # explicit assertions
    m = HAS_OBJ_PATTERN.match(utterance)
    if m:
        name = m.group(1)
        obj = normalize_obj(m.group(3))
        ensure_entity(state, name)
        add_fact(state, subject=name, relation="has", obj=obj)  # normalize tense to relation="has"
        parse_record["recognized_assertions"].append(f"{name} has {obj}")

    # ambiguity detection (record only, mirrors build_ambiguity logic)
    m2 = PRONOUN_W1_W2_PATTERN.search(utterance)
    if m2:
        slot = m2.group(1).lower()
        w1 = (m2.group(2) or "").lower()
        w2 = (m2.group(3) or "").lower()

        if w2 == "" or w2 in DISALLOWED_OBJ_TAIL:
            obj = w1
        else:
            obj = f"{w1} {w2}"

        obj = normalize_obj(obj)
        if obj:
            parse_record["recognized_ambiguous_spans"].append(f"{slot} {obj}")

    return parse_record


# ----------------------------
# Ambiguity + admissibility
# ----------------------------

def context_supports(state: State, candidate: str, obj: str) -> bool:
    return any(f.subject == candidate and f.relation == "has" and f.obj == obj for f in state.facts)

def build_ambiguity(state: State, utterance: str) -> Optional[Ambiguity]:
    m = PRONOUN_W1_W2_PATTERN.search(utterance)
    if not m:
        return None

    slot = m.group(1).lower()
    w1 = (m.group(2) or "").lower()
    w2 = (m.group(3) or "").lower()

    if not w1:
        return None

    # If the optional second token is a verb/aux tail, ignore it.
    if w2 == "" or w2 in DISALLOWED_OBJ_TAIL:
        obj = w1
    else:
        obj = f"{w1} {w2}"

    obj = normalize_obj(obj)
    span = f"{slot} {obj}"

    candidates = sorted(state.entities.keys())

    if len(candidates) < 2:
        if len(candidates) == 1:
            only = candidates[0]
            question = f'When you say "{span}", do you mean {only}’s {obj}? (answer: {only})'
            allowed = {
                only.lower(): only,
                f"{only.lower()} {obj}": only,
                f"{only.lower()}'s {obj}": only,
                f"{only.lower()}’s {obj}": only,
            }
            return Ambiguity(
                ambig_id=f"ambig-{state.turn_index}",
                ambig_type="reference",
                span=span,
                slot=slot,
                obj=obj,
                candidates=candidates,
                question=question,
                allowed_answers=allowed,
            )
        return Ambiguity(
            ambig_id=f"ambig-{state.turn_index}",
            ambig_type="reference",
            span=span,
            slot=slot,
            obj=obj,
            candidates=[],
            question=f'Who does "{slot}" refer to in "{span}"? (answer with a name already introduced)',
            allowed_answers={},
        )

    opts = " or ".join([f"{c}’s {obj}" for c in candidates])
    question = f'Is "{span}" referring to {opts}?'

    allowed: Dict[str, str] = {}
    for c in candidates:
        keys = {
            c.lower(),
            f"{c.lower()} {obj}",
            f"{c.lower()}'s {obj}",
            f"{c.lower()}’s {obj}",
            f"{c.lower()}'s",
            f"{c.lower()}’s",
        }
        for k in keys:
            allowed[k] = c

    return Ambiguity(
        ambig_id=f"ambig-{state.turn_index}",
        ambig_type="reference",
        span=span,
        slot=slot,
        obj=obj,
        candidates=candidates,
        question=question,
        allowed_answers=allowed,
    )

def admissibility_check(state: State, ambiguity: Ambiguity) -> Tuple[bool, List[str]]:
    supported = [c for c in ambiguity.candidates if context_supports(state, c, ambiguity.obj)]
    return (len(supported) == 1), supported


# ----------------------------
# Clarification
# ----------------------------

def normalize_answer(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s’']", " ", text)
    tokens = text.split()
    return " ".join(tokens[:6])

def apply_clarification(state: State, answer: str) -> Dict:
    amb = state.pending_ambiguity
    assert amb is not None

    if not amb.candidates:
        return {"clarification_accepted": False, "reason": "no_candidates_in_state"}

    norm = normalize_answer(answer)
    chosen = amb.allowed_answers.get(norm)

    if chosen is None:
        for c in amb.candidates:
            if re.search(rf"\b{re.escape(c.lower())}\b", answer.lower()):
                chosen = c
                break

    if chosen is None:
        return {
            "clarification_accepted": False,
            "reason": "answer_not_in_allowed_set",
            "expected_sample": sorted(set(amb.allowed_answers.keys()))[:12],
        }

    state.bindings[amb.slot] = chosen
    state.pending_ambiguity = None

    return {
        "clarification_accepted": True,
        "resolved_reference": {"slot": amb.slot, "span": amb.span, "obj": amb.obj, "chosen": chosen},
    }

def rewrite_resolved_utterance(utterance: str, chosen: str, ambiguity: Ambiguity) -> str:
    pattern = rf"\b{re.escape(ambiguity.slot)}\s+{re.escape(ambiguity.obj)}\b"
    return re.sub(pattern, f"{chosen}’s {ambiguity.obj}", utterance, flags=re.IGNORECASE)


# ----------------------------
# Engine step
# ----------------------------

def snapshot_state(state: State) -> Dict:
    return {
        "entities": sorted(state.entities.keys()),
        "facts": [{"subject": f.subject, "relation": f.relation, "obj": f.obj} for f in state.facts],
        "bindings": dict(state.bindings),
        "pending_ambiguity": None if state.pending_ambiguity is None else {
            "id": state.pending_ambiguity.ambig_id,
            "type": state.pending_ambiguity.ambig_type,
            "span": state.pending_ambiguity.span,
            "slot": state.pending_ambiguity.slot,
            "obj": state.pending_ambiguity.obj,
            "candidates": state.pending_ambiguity.candidates,
            "question": state.pending_ambiguity.question,
        }
    }

def step(state: State, user_input: str) -> Dict:
    state.turn_index += 1

    if state.pending_ambiguity is not None:
        result = apply_clarification(state, user_input)
        out = {
            "turn": state.turn_index,
            "mode": "AWAITING_CLARIFICATION",
            "input": user_input,
            "result": result,
            "state_snapshot": snapshot_state(state),
        }

        if result.get("clarification_accepted") and state.suspended_utterance is not None:
            suspended = state.suspended_utterance
            amb = state.suspended_ambiguity
            state.suspended_utterance = None
            state.suspended_ambiguity = None
            chosen = result["resolved_reference"]["chosen"]
            resolved = rewrite_resolved_utterance(suspended, chosen, amb) if amb else suspended
            out["resume"] = {
                "utterance": suspended,
                "resolved_utterance": resolved,
                "status": "RESUMED_AFTER_CLARIFICATION",
            }
        return out

    parse_record = parse_and_update_state(state, user_input)
    ambiguity = build_ambiguity(state, user_input)

    if ambiguity is None:
        return {
            "turn": state.turn_index,
            "mode": "NORMAL",
            "input": user_input,
            "parse": parse_record,
            "decision": {"status": "no_ambiguity"},
            "state_snapshot": snapshot_state(state),
        }

    admissible, supported = admissibility_check(state, ambiguity)

    if not admissible:
        state.pending_ambiguity = ambiguity
        state.suspended_utterance = user_input
        state.suspended_ambiguity = ambiguity
        return {
            "turn": state.turn_index,
            "mode": "NORMAL",
            "input": user_input,
            "parse": parse_record,
            "decision": {
                "status": "STOP_NEEDS_CLARIFICATION",
                "ambiguity": {
                    "id": ambiguity.ambig_id,
                    "type": ambiguity.ambig_type,
                    "span": ambiguity.span,
                    "slot": ambiguity.slot,
                    "obj": ambiguity.obj,
                    "candidates": ambiguity.candidates,
                    "supported_by_context": supported,
                },
                "refusal": "I cannot proceed without clarification.",
                "question": ambiguity.question,
                "answer_policy": "constrained_only_ignore_elaboration",
            },
            "state_snapshot": snapshot_state(state),
        }

    chosen = supported[0]
    state.bindings[ambiguity.slot] = chosen

    return {
        "turn": state.turn_index,
        "mode": "NORMAL",
        "input": user_input,
        "parse": parse_record,
        "decision": {
            "status": "RESOLVED_BY_CONTEXT",
            "collapse": {"slot": ambiguity.slot, "span": ambiguity.span, "obj": ambiguity.obj, "chosen": chosen},
        },
        "state_snapshot": snapshot_state(state),
    }


# ----------------------------
# CLI
# ----------------------------

HELP = """\
Aurora CLI Demo (Minimal)
Examples:
  Lucy has a brother.
  Jenny has a brother.
  her brother is tall.

  Peter had a black cat.
  Jenny had a white cat.
  Their cat is really cute.

If Aurora asks a clarification question, answer with ONLY one candidate name.
Commands:
  /state   show current state
  /reset   reset state
  /quit    exit
"""

def main() -> None:
    state = State()
    print(HELP)

    while True:
        try:
            prompt = "clarify> " if state.pending_ambiguity is not None else "> "
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n/quit")
            return

        if not user_input:
            continue
        if user_input == "/quit":
            return
        if user_input == "/reset":
            state = State()
            print("State reset.")
            continue
        if user_input == "/state":
            print(json.dumps(snapshot_state(state), indent=2))
            continue

        trace = step(state, user_input)

        if trace.get("mode") == "AWAITING_CLARIFICATION":
            res = trace.get("result", {})
            if res.get("clarification_accepted") is False:
                reason = res.get("reason", "rejected")
                print(f"(Not accepted: {reason}. Please answer with one candidate name.)")

        decision = trace.get("decision", {})

        if decision.get("status") == "STOP_NEEDS_CLARIFICATION":
            print("\n" + "=" * 72)
            print("STOP: CLARIFICATION REQUIRED")
            print(decision["refusal"])
            print("Q:", decision["question"])
            print("Answer with one of:", ", ".join(decision["ambiguity"]["candidates"]))
            print("=" * 72 + "\n")

        if trace.get("resume") is not None:
            resolved = trace["resume"]["resolved_utterance"]
            print("\n" + "-" * 72)
            print("RESOLVED INTERPRETATION")
            print(resolved)
            print("Note: This output is a resolved interpretation of the utterance, not a world assertion.")
            print("END (press Enter to exit)")
            print("-" * 72)
            input()
            return

        if SHOW_JSON:
            print(json.dumps(trace, indent=2))

if __name__ == "__main__":
    main()
