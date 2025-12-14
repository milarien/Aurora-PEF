# ⚠️ HISTORICAL DEMO
# This file is retained for provenance only.
# It does NOT represent current Aurora behavior.
# Run demo/aurora_cli_demo.py instead.

raise RuntimeError(
    "This demo is historical. Run demo/aurora_cli_demo.py instead."
)

#!/usr/bin/env python3
"""
Aurora CLI Demo (Minimal Invariants) — Patched (Generalized)

Design invariants enforced:

- Ambiguity is handled as a STOP + clarification question about the utterance.
- No fact invention: only explicit assertions update state.
- No constraint application unless prerequisites are satisfied.
- No world-fact questions if they do not guarantee collapse.
- Constrained answers only; elaboration is ignored.
- Deterministic collapse when admissible.
- Aurora is allowed to say: "I cannot proceed without clarification."

Patch goals:

- Generalize explicit assertions from "has a sister" -> "has a/an <noun>"
- Generalize ambiguous spans from "her sister" -> "(her|his|their) <noun>"
- Context admissibility becomes object-aware: candidate must have explicit "<candidate> has <noun>"
- Resolved interpretation rewrite becomes object-aware

UX behavior for demo:
- When clarification is required, prints a loud STOP banner and switches prompt to `clarify>`.
- After a successful clarification, prints a resolved interpretation (rewritten utterance)
  and exits back to the directory prompt.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

SHOW_JSON = False  # flip to True if you want full traces

# ----------------------------
# Guards: do not let referential operators become entities
# ----------------------------

PRONOUNS = {
    "i", "me", "my", "mine",
    "we", "us", "our", "ours",
    "you", "your", "yours",
    "he", "him", "his",
    "she", "her", "hers",
    "they", "them", "their", "theirs",
    "it", "its",
}

# Words that should never be treated as entity introductions (optional but sane)
STOPWORDS = {
    "a", "an", "the", "this", "that", "these", "those",
    "and", "or", "but", "if", "then", "because",
}

# ----------------------------
# Data structures
# ----------------------------

@dataclass
class Fact:
    subject: str
    relation: str
    obj: str


@dataclass
class Ambiguity:
    ambig_id: str
    ambig_type: str  # "reference"
    span: str        # e.g. "her sister" / "his dog" / "their cat"
    slot: str        # e.g. "her" / "his" / "their"
    obj: str         # e.g. "sister" / "dog" / "cat"
    candidates: List[str]
    question: str
    allowed_answers: Dict[str, str]  # normalized_answer -> chosen_candidate


@dataclass
class State:
    entities: Dict[str, Dict] = field(default_factory=dict)
    facts: List[Fact] = field(default_factory=list)

    # Explicit bindings created by clarification, e.g. {"her": "Lucy"}
    bindings: Dict[str, str] = field(default_factory=dict)

    # The utterance that triggered STOP (so we can resume it after clarification)
    suspended_utterance: Optional[str] = None

    # Store the ambiguity that triggered STOP so rewrite is exact after clarification
    suspended_ambiguity: Optional[Ambiguity] = None

    pending_ambiguity: Optional[Ambiguity] = None
    turn_index: int = 0


# ----------------------------
# Parsing: explicit-only context update
# ----------------------------

ENTITY_PATTERN = re.compile(r"\b([A-Z][a-z]+)\b")

# Generalized explicit assertion:
#   "<Name> has a/an <noun>."
# Notes:
# - keeps the demo intentionally narrow: only recognizes this form as a state-updating assertion.
# - noun is captured as a simple alphabetic token (no multiword nouns).
HAS_X_PATTERN = re.compile(
    r"^\s*([A-Z][a-z]+)\s+has\s+a[n]?\s+([a-z]+)\s*\.?\s*$",
    re.IGNORECASE
)

# Generalized ambiguous span:
#   "(her|his|their) <noun>"
PRONOUN_X_PATTERN = re.compile(
    r"\b(her|his|their)\s+([a-z]+)\b",
    re.IGNORECASE
)


def ensure_entity(state: State, name: str) -> None:
    if name not in state.entities:
        state.entities[name] = {"name": name}


def add_fact(state: State, subject: str, relation: str, obj: str) -> None:
    state.facts.append(Fact(subject=subject, relation=relation, obj=obj))


def parse_and_update_state(state: State, utterance: str) -> Dict:
    """
    Updates state only via explicit assertions.
    """
    parse_record = {
        "recognized_assertions": [],
        "recognized_entities": [],
        "recognized_ambiguous_spans": [],
    }

    # Surface entities (capitalized names). Guard against pronouns/stopwords.
    for m in ENTITY_PATTERN.finditer(utterance):
        name = m.group(1)
        low = name.lower()
        if low in PRONOUNS or low in STOPWORDS:
            continue
        ensure_entity(state, name)
        if name not in parse_record["recognized_entities"]:
            parse_record["recognized_entities"].append(name)

    # Explicit assertion: "<Name> has a/an <noun>."
    m = HAS_X_PATTERN.match(utterance)
    if m:
        name = m.group(1)
        obj = m.group(2).lower()
        ensure_entity(state, name)
        add_fact(state, subject=name, relation="has", obj=obj)
        parse_record["recognized_assertions"].append(f"{name} has {obj}")

    # Detect ambiguous span: "(her|his|their) <noun>"
    m2 = PRONOUN_X_PATTERN.search(utterance)
    if m2:
        pron = m2.group(1).lower()
        obj = m2.group(2).lower()
        parse_record["recognized_ambiguous_spans"].append(f"{pron} {obj}")

    return parse_record


# ----------------------------
# Ambiguity detection + admissibility gate
# ----------------------------

def context_supports(state: State, candidate: str, obj: str) -> bool:
    # Prerequisite is explicit: "<candidate> has <obj>"
    return any(
        f.subject == candidate and f.relation == "has" and f.obj == obj
        for f in state.facts
    )


def build_ambiguity(state: State, utterance: str) -> Optional[Ambiguity]:
    m = PRONOUN_X_PATTERN.search(utterance)
    if not m:
        return None

    slot = m.group(1).lower()  # her/his/their
    obj = m.group(2).lower()   # sister/dog/etc.
    span = f"{slot} {obj}"

    candidates = sorted(state.entities.keys())

    # If fewer than 2 candidate entities exist, we can't offer a useful constrained set.
    # Keep the invariant: ask about the utterance, not the world.
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
        else:
            question = f'Who does "{slot}" refer to in "{span}"? (answer with a name already introduced)'
            return Ambiguity(
                ambig_id=f"ambig-{state.turn_index}",
                ambig_type="reference",
                span=span,
                slot=slot,
                obj=obj,
                candidates=[],
                question=question,
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
# Clarification handling
# ----------------------------

def normalize_answer(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s’']", " ", text)
    tokens = text.split()
    return " ".join(tokens[:4])


def apply_clarification(state: State, answer: str) -> Dict:
    amb = state.pending_ambiguity
    assert amb is not None

    if not amb.candidates:
        return {"clarification_accepted": False, "reason": "no_candidates_in_state"}

    norm = normalize_answer(answer)
    chosen = amb.allowed_answers.get(norm)

    if chosen is None:
        # Looser: if a candidate name appears anywhere
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

    # Persist binding; clear pending ambiguity
    state.bindings[amb.slot] = chosen
    state.pending_ambiguity = None

    return {
        "clarification_accepted": True,
        "resolved_reference": {
            "slot": amb.slot,
            "span": amb.span,
            "obj": amb.obj,
            "chosen": chosen
        },
    }


def rewrite_resolved_utterance(utterance: str, chosen: str, ambiguity: Ambiguity) -> str:
    # Deterministic rewrite: clarify the utterance; do not add world facts.
    # Replace the specific ambiguous span (slot + obj) with "<Chosen>’s <obj>"
    pron = ambiguity.slot
    obj = ambiguity.obj
    pattern = rf"\b{re.escape(pron)}\s+{re.escape(obj)}\b"
    return re.sub(pattern, f"{chosen}’s {obj}", utterance, flags=re.IGNORECASE)


# ----------------------------
# Engine step
# ----------------------------

def step(state: State, user_input: str) -> Dict:
    state.turn_index += 1

    # Clarification mode: accept constrained answer ONLY
    if state.pending_ambiguity is not None:
        result = apply_clarification(state, user_input)

        out = {
            "turn": state.turn_index,
            "mode": "AWAITING_CLARIFICATION",
            "input": user_input,
            "result": result,
            "state_snapshot": snapshot_state(state),
        }

        # If accepted, resume the suspended utterance (interpretation only)
        if result.get("clarification_accepted") and state.suspended_utterance is not None:
            suspended = state.suspended_utterance
            amb = state.suspended_ambiguity  # must exist if suspended_utterance exists in STOP mode

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

    # Deterministic collapse by context (one supported candidate)
    chosen = supported[0]
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
                "span": ambiguity.span,
                "obj": ambiguity.obj,
                "chosen": chosen
            },
        },
        "state_snapshot": snapshot_state(state),
    }


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


# ----------------------------
# CLI
# ----------------------------

HELP = """\
Aurora CLI Demo (Minimal)
Type sentences. Example:
  Emma has a sister.
  Lucy has a sister.
  Her sister is nice.

Patched: also supports:
  Joanna has a dog.
  Marcelline has a dog.
  Her dog is evil.
  Jacob has a sister.
  Robert has a sister.
  His sister is nice.
  Ada has a cat.
  Bea has a cat.
  Their cat is loud.

If Aurora asks a clarification question, answer with ONLY one of the candidate names (e.g. "Emma" or "Lucy").
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

        # If in clarification mode and the answer was rejected, say so plainly.
        if trace.get("mode") == "AWAITING_CLARIFICATION":
            res = trace.get("result", {})
            if res.get("clarification_accepted") is False:
                reason = res.get("reason", "rejected")
                print(f"(Not accepted: {reason}. Please answer with one candidate name.)")

        decision = trace.get("decision", {})

        # STOP banner (human-visible, primary)
        if decision.get("status") == "STOP_NEEDS_CLARIFICATION":
            print("\n" + "=" * 72)
            print("STOP: CLARIFICATION REQUIRED")
            print(decision["refusal"])
            print("Q:", decision["question"])
            print("Answer with one of:", ", ".join(decision["ambiguity"]["candidates"]))
            print("=" * 72 + "\n")

        # Resume = terminal success (print and exit)
        if trace.get("resume") is not None:
            resolved = trace["resume"]["resolved_utterance"]
            print("\n" + "-" * 72)
            print("RESOLVED INTERPRETATION")
            print(resolved)
            print("Note: This output is a resolved interpretation of the utterance, not a world assertion.")
            print("END (press Enter to exit)")
            print("-" * 72)
            input()   # <-- pause here
            return

        # Optional audit output
        if SHOW_JSON:
            print(json.dumps(trace, indent=2))


if __name__ == "__main__":
    main()
