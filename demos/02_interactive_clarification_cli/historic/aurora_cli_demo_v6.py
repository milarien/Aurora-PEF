# ⚠️ HISTORICAL DEMO
# This file is retained for provenance only.
# It does NOT represent current Aurora behavior.
# Run demo/aurora_cli_demo.py instead.

raise RuntimeError(
    "This demo is historical. Run demo/aurora_cli_demo.py instead."
)
#!/usr/bin/env python3
"""
Aurora CLI Demo (Minimal Invariants) — v6
Generalized + Optional Adjective + Corrected Pronoun Capture + Minimal Attributes

What v6 adds (minimal, deterministic, demo-safe):
- Parses and stores head-noun facts:       "Jenny has a brother."      -> has(brother)
- Parses and stores attribute facts:       "Jenny has a tall brother." -> has(brother) + attr(brother,tall)
- Parses a tiny predicate form:            "Her brother is tall."      -> reference(obj=brother) + requires attr(tall)
- Uses attributes as admissibility constraints:
    If exactly one candidate’s <noun> has required <adj>, collapse by context.
    Otherwise STOP and ask clarification (utterance-first, not world-fact questions).

Still intentionally narrow:
- Objects are 1 or 2 tokens: "cat" or "black cat"
- Predicate attribute is a single token: "is tall"
- No full grammar, no guessing, no “most natural”.

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
from typing import Dict, List, Optional, Tuple, Set

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
    obj: str  # head noun only: "brother", "cat", "dog"


@dataclass
class Ambiguity:
    ambig_id: str
    ambig_type: str  # "reference"
    span: str        # e.g. "her brother"
    slot: str        # her / his / their
    obj_phrase: str  # e.g. "brother" or "black cat" (as spoken)
    head: str        # head noun: "brother" or "cat"
    required_attr: Optional[str]  # e.g. "tall" from "is tall" or from "black cat"
    candidates: List[str]
    question: str
    allowed_answers: Dict[str, str]


@dataclass
class State:
    entities: Dict[str, Dict] = field(default_factory=dict)
    facts: List[Fact] = field(default_factory=list)

    # attributes[subject][head_noun] = {"tall","black",...}
    attributes: Dict[str, Dict[str, Set[str]]] = field(default_factory=dict)

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

def normalize_obj_phrase(s: str) -> str:
    return normalize_ws(s.lower())

def ensure_entity(state: State, name: str) -> None:
    if name not in state.entities:
        state.entities[name] = {"name": name}

def add_fact(state: State, subject: str, relation: str, obj: str) -> None:
    state.facts.append(Fact(subject=subject, relation=relation, obj=obj))

def add_attr(state: State, subject: str, head: str, attr: str) -> None:
    subject_map = state.attributes.setdefault(subject, {})
    head_set = subject_map.setdefault(head, set())
    head_set.add(attr)

def split_obj_phrase(obj_phrase: str) -> Tuple[Optional[str], str]:
    """
    obj_phrase is 1 or 2 tokens.
    - "brother" -> (None, "brother")
    - "black cat" -> ("black", "cat")
    """
    toks = normalize_obj_phrase(obj_phrase).split()
    if not toks:
        return (None, "")
    if len(toks) == 1:
        return (None, toks[0])
    # two tokens max by design
    return (toks[0], toks[1])


# ----------------------------
# Patterns (explicit-only + tiny predicate)
# ----------------------------

# Explicit assertion:
#   "<Name> has|had a/an <noun>" OR "<Name> has|had a/an <adj> <noun>"
HAS_OBJ_PATTERN = re.compile(
    r"^\s*([A-Z][a-z]+)\s+(has|had)\s+a[n]?\s+([a-z]+(?:\s+[a-z]+)?)\s*\.?\s*$",
    re.IGNORECASE
)

# Pronoun + object:
#   "(her|his|their) <w1> [<w2>]"
# We decide whether w2 is adjective or a tail verb/aux.
PRONOUN_W1_W2_PATTERN = re.compile(
    r"\b(her|his|their)\s+([a-z]+)(?:\s+([a-z]+))?\b",
    re.IGNORECASE
)

# Predicate attribute:
#   "... is <adj>."  (very small by design)
# We only use it when the utterance ALSO contains a pronoun-object span.
PRED_ATTR_PATTERN = re.compile(
    r"\b(?:is|was|are|were)\s+([a-z]+)\b",
    re.IGNORECASE
)


# ----------------------------
# Parsing: explicit-only state update
# ----------------------------

def parse_and_update_state(state: State, utterance: str) -> Dict:
    parse_record = {
        "recognized_assertions": [],
        "recognized_entities": [],
        "recognized_ambiguous_spans": [],
        "recognized_predicate_attr": None,
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
        obj_phrase = normalize_obj_phrase(m.group(3))
        adj, head = split_obj_phrase(obj_phrase)
        if head:
            ensure_entity(state, name)
            add_fact(state, subject=name, relation="has", obj=head)  # normalize tense to "has"
            parse_record["recognized_assertions"].append(f"{name} has {head}")
            if adj:
                add_attr(state, subject=name, head=head, attr=adj)
                parse_record["recognized_assertions"].append(f"{name}.{head} has_attr {adj}")

    # ambiguity detection (record only)
    m2 = PRONOUN_W1_W2_PATTERN.search(utterance)
    if m2:
        slot = m2.group(1).lower()
        w1 = (m2.group(2) or "").lower()
        w2 = (m2.group(3) or "").lower()

        # Decide whether w2 is part of the object phrase.
        if w2 == "" or w2 in DISALLOWED_OBJ_TAIL:
            obj_phrase = w1
        else:
            obj_phrase = f"{w1} {w2}"

        obj_phrase = normalize_obj_phrase(obj_phrase)
        if obj_phrase:
            parse_record["recognized_ambiguous_spans"].append(f"{slot} {obj_phrase}")

            # If the utterance also includes "is/was/are/were <adj>", capture it.
            # (Used later as a constraint for admissibility.)
            pm = PRED_ATTR_PATTERN.search(utterance)
            if pm:
                parse_record["recognized_predicate_attr"] = pm.group(1).lower()

    return parse_record


# ----------------------------
# Ambiguity building + admissibility
# ----------------------------

def subject_has_head(state: State, subject: str, head: str) -> bool:
    return any(f.subject == subject and f.relation == "has" and f.obj == head for f in state.facts)

def subject_head_has_attr(state: State, subject: str, head: str, attr: str) -> bool:
    return attr in state.attributes.get(subject, {}).get(head, set())

def extract_pronoun_obj_from_utterance(utterance: str) -> Optional[Tuple[str, str]]:
    """
    Returns (slot, obj_phrase) where obj_phrase is 1-2 tokens, with tail-verb protection.
    """
    m = PRONOUN_W1_W2_PATTERN.search(utterance)
    if not m:
        return None
    slot = m.group(1).lower()
    w1 = (m.group(2) or "").lower()
    w2 = (m.group(3) or "").lower()
    if not w1:
        return None
    if w2 == "" or w2 in DISALLOWED_OBJ_TAIL:
        obj_phrase = w1
    else:
        obj_phrase = f"{w1} {w2}"
    return (slot, normalize_obj_phrase(obj_phrase))

def build_ambiguity(state: State, utterance: str) -> Optional[Ambiguity]:
    extracted = extract_pronoun_obj_from_utterance(utterance)
    if not extracted:
        return None

    slot, obj_phrase = extracted
    adj_from_phrase, head = split_obj_phrase(obj_phrase)
    if not head:
        return None

    # Attribute constraint can come from either:
    # - the obj phrase itself (e.g., "her black cat" -> requires "black" on cat)
    # - a predicate attribute (e.g., "her brother is tall" -> requires "tall" on brother)
    required_attr: Optional[str] = adj_from_phrase

    pm = PRED_ATTR_PATTERN.search(utterance)
    if pm:
        # predicate attr wins (more explicit in the clause)
        required_attr = pm.group(1).lower()

    # Candidate set: only entities that have the head object, if any exist.
    all_entities = sorted(state.entities.keys())
    head_candidates = [c for c in all_entities if subject_has_head(state, c, head)]
    candidates = head_candidates if head_candidates else all_entities

    if len(candidates) < 2:
        # Keep utterance-first question. If only one candidate, allow it.
        if len(candidates) == 1:
            only = candidates[0]
            question = f'When you say "{slot} {head}", do you mean {only}’s {head}? (answer: {only})'
            allowed = {
                only.lower(): only,
                f"{only.lower()} {head}": only,
                f"{only.lower()}'s {head}": only,
                f"{only.lower()}’s {head}": only,
            }
            return Ambiguity(
                ambig_id=f"ambig-{state.turn_index}",
                ambig_type="reference",
                span=f"{slot} {head}",
                slot=slot,
                obj_phrase=obj_phrase,
                head=head,
                required_attr=required_attr,
                candidates=candidates,
                question=question,
                allowed_answers=allowed,
            )
        # zero candidates: ask, but without a constrained set
        return Ambiguity(
            ambig_id=f"ambig-{state.turn_index}",
            ambig_type="reference",
            span=f"{slot} {head}",
            slot=slot,
            obj_phrase=obj_phrase,
            head=head,
            required_attr=required_attr,
            candidates=[],
            question=f'Who does "{slot}" refer to in "{slot} {head}"? (answer with a name already introduced)',
            allowed_answers={},
        )

    opts = " or ".join([f"{c}’s {head}" for c in candidates])
    question = f'Is "{slot} {head}" referring to {opts}?'

    allowed: Dict[str, str] = {}
    for c in candidates:
        keys = {
            c.lower(),
            f"{c.lower()} {head}",
            f"{c.lower()}'s {head}",
            f"{c.lower()}’s {head}",
            f"{c.lower()}'s",
            f"{c.lower()}’s",
        }
        for k in keys:
            allowed[k] = c

    return Ambiguity(
        ambig_id=f"ambig-{state.turn_index}",
        ambig_type="reference",
        span=f"{slot} {head}",
        slot=slot,
        obj_phrase=obj_phrase,
        head=head,
        required_attr=required_attr,
        candidates=candidates,
        question=question,
        allowed_answers=allowed,
    )

def admissibility_check(state: State, ambiguity: Ambiguity) -> Tuple[bool, List[str], List[str]]:
    """
    Returns:
    - admissible: exactly one candidate remains after constraints
    - supported_by_head: candidates that have the head object
    - supported_by_constraints: candidates that satisfy all constraints (head + required_attr if any)
    """
    supported_by_head = [c for c in ambiguity.candidates if subject_has_head(state, c, ambiguity.head)]

    if ambiguity.required_attr:
        supported_by_constraints = [
            c for c in supported_by_head
            if subject_head_has_attr(state, c, ambiguity.head, ambiguity.required_attr)
        ]
    else:
        supported_by_constraints = supported_by_head[:]

    return (len(supported_by_constraints) == 1), supported_by_head, supported_by_constraints


# ----------------------------
# Clarification handling
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
        "resolved_reference": {
            "slot": amb.slot,
            "span": amb.span,
            "head": amb.head,
            "required_attr": amb.required_attr,
            "chosen": chosen
        },
    }

def rewrite_resolved_utterance(utterance: str, chosen: str, ambiguity: Ambiguity) -> str:
    # Replace the span "her brother" (slot + head) only — keep the rest intact.
    pattern = rf"\b{re.escape(ambiguity.slot)}\s+{re.escape(ambiguity.head)}\b"
    return re.sub(pattern, f"{chosen}’s {ambiguity.head}", utterance, flags=re.IGNORECASE)


# ----------------------------
# Engine step
# ----------------------------

def snapshot_state(state: State) -> Dict:
    return {
        "entities": sorted(state.entities.keys()),
        "facts": [{"subject": f.subject, "relation": f.relation, "obj": f.obj} for f in state.facts],
        "attributes": {
            subj: {head: sorted(list(attrs)) for head, attrs in heads.items()}
            for subj, heads in state.attributes.items()
        },
        "bindings": dict(state.bindings),
        "pending_ambiguity": None if state.pending_ambiguity is None else {
            "id": state.pending_ambiguity.ambig_id,
            "span": state.pending_ambiguity.span,
            "slot": state.pending_ambiguity.slot,
            "head": state.pending_ambiguity.head,
            "required_attr": state.pending_ambiguity.required_attr,
            "candidates": state.pending_ambiguity.candidates,
            "question": state.pending_ambiguity.question,
        }
    }

def step(state: State, user_input: str) -> Dict:
    state.turn_index += 1

    # Clarification mode
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

    # Normal mode
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

    admissible, supported_by_head, supported_by_constraints = admissibility_check(state, ambiguity)

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
                    "span": ambiguity.span,
                    "head": ambiguity.head,
                    "required_attr": ambiguity.required_attr,
                    "candidates": ambiguity.candidates,
                    "supported_by_head": supported_by_head,
                    "supported_by_constraints": supported_by_constraints,
                },
                "refusal": "I cannot proceed without clarification.",
                "question": ambiguity.question,
                "answer_policy": "constrained_only_ignore_elaboration",
            },
            "state_snapshot": snapshot_state(state),
        }

    # Deterministic collapse by constraints
    chosen = supported_by_constraints[0]
    state.bindings[ambiguity.slot] = chosen

    return {
        "turn": state.turn_index,
        "mode": "NORMAL",
        "input": user_input,
        "parse": parse_record,
        "decision": {
            "status": "RESOLVED_BY_CONTEXT",
            "collapse": {
                "slot": ambiguity.slot,
                "head": ambiguity.head,
                "required_attr": ambiguity.required_attr,
                "chosen": chosen,
            },
        },
        "state_snapshot": snapshot_state(state),
    }


# ----------------------------
# CLI
# ----------------------------

HELP = """\
Aurora CLI Demo (Minimal) — v6

Try:
  /reset
  Jenny has a brother.
  Amelia has a brother.
  Jenny has a tall brother.
  Her brother is tall.

Expected: resolves to Jenny by attribute constraint (no STOP).

Also:
  /reset
  Peter had a black cat.
  Jenny had a white cat.
  Their cat is really cute.

Expected: STOP (both have "cat", no attribute constraint from predicate on "cute" stored for either).
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
