# ⚠️ HISTORICAL DEMO
# This file is retained for provenance only.
# It does NOT represent current Aurora behavior.
# Run demo/aurora_cli_demo.py instead.

raise RuntimeError(
    "This demo is historical. Run demo/aurora_cli_demo.py instead."
)
#!/usr/bin/env python3
"""
Aurora CLI Demo (Minimal Invariants) — v7.1
Generalized + Optional Adjective + Corrected Pronoun Capture
+ Minimal Attributes
+ Attribute Commit After Clarification / Deterministic Collapse
+ FIX: multi-word predicate attributes ("more magnificent", "less shiny")

Only change vs v7:
- Predicate attribute extractor now captures:
    - single adjective        ("tall", "fierce")
    - comparative + adjective ("more magnificent", "less shiny")

All invariants preserved.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

SHOW_JSON = False

PRONOUNS = {
    "i","me","my","mine","we","us","our","ours","you","your","yours",
    "he","him","his","she","her","hers","they","them","their","theirs",
    "it","its",
}

STOPWORDS = {
    "a","an","the","this","that","these","those",
    "and","or","but","if","then","because",
}

DISALLOWED_OBJ_TAIL = {
    "is","was","are","were","be","been","being","am",
    "do","does","did","has","have","had",
    "will","would","shall","should",
    "can","could","may","might","must","to",
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
    ambig_type: str
    span: str
    slot: str
    obj_phrase: str
    head: str
    required_attr: Optional[str]
    predicate_attr: Optional[str]
    candidates: List[str]
    question: str
    allowed_answers: Dict[str, str]


@dataclass
class State:
    entities: Dict[str, Dict] = field(default_factory=dict)
    facts: List[Fact] = field(default_factory=list)
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
    state.entities.setdefault(name, {"name": name})

def add_fact(state: State, subject: str, relation: str, obj: str) -> None:
    state.facts.append(Fact(subject, relation, obj))

def add_attr(state: State, subject: str, head: str, attr: str) -> None:
    state.attributes.setdefault(subject, {}).setdefault(head, set()).add(attr)

def split_obj_phrase(obj_phrase: str) -> Tuple[Optional[str], str]:
    toks = normalize_obj_phrase(obj_phrase).split()
    if len(toks) == 1:
        return None, toks[0]
    if len(toks) == 2:
        return toks[0], toks[1]
    return None, ""


# ----------------------------
# Patterns
# ----------------------------

HAS_OBJ_PATTERN = re.compile(
    r"^\s*([A-Z][a-z]+)\s+(has|had)\s+a[n]?\s+([a-z]+(?:\s+[a-z]+)?)\s*\.?\s*$",
    re.IGNORECASE
)

PRONOUN_W1_W2_PATTERN = re.compile(
    r"\b(her|his|their)\s+([a-z]+)(?:\s+([a-z]+))?\b",
    re.IGNORECASE
)

# FIXED: capture "more magnificent" / "less shiny" as a unit
PRED_ATTR_PATTERN = re.compile(
    r"\b(?:is|was|are|were)\s+((?:more|less)\s+[a-z]+|[a-z]+)\b",
    re.IGNORECASE
)


# ----------------------------
# Parsing
# ----------------------------

def parse_and_update_state(state: State, utterance: str) -> Dict:
    record = {
        "recognized_assertions": [],
        "recognized_entities": [],
        "recognized_predicate_attr": None,
    }

    for m in ENTITY_PATTERN.finditer(utterance):
        name = m.group(1)
        if name.lower() not in PRONOUNS | STOPWORDS:
            ensure_entity(state, name)
            record["recognized_entities"].append(name)

    m = HAS_OBJ_PATTERN.match(utterance)
    if m:
        name = m.group(1)
        obj_phrase = normalize_obj_phrase(m.group(3))
        adj, head = split_obj_phrase(obj_phrase)
        ensure_entity(state, name)
        add_fact(state, name, "has", head)
        if adj:
            add_attr(state, name, head, adj)
        record["recognized_assertions"].append(f"{name} has {obj_phrase}")

    pm = PRED_ATTR_PATTERN.search(utterance)
    if pm:
        record["recognized_predicate_attr"] = normalize_ws(pm.group(1).lower())

    return record


# ----------------------------
# Ambiguity + constraints
# ----------------------------

def subject_has_head(state: State, subject: str, head: str) -> bool:
    return any(f.subject == subject and f.obj == head for f in state.facts)

def subject_head_has_attr(state: State, subject: str, head: str, attr: str) -> bool:
    return attr in state.attributes.get(subject, {}).get(head, set())

def extract_pronoun_obj(utterance: str) -> Optional[Tuple[str, str]]:
    m = PRONOUN_W1_W2_PATTERN.search(utterance)
    if not m:
        return None
    slot = m.group(1).lower()
    w1 = m.group(2).lower()
    w2 = (m.group(3) or "").lower()
    obj = w1 if not w2 or w2 in DISALLOWED_OBJ_TAIL else f"{w1} {w2}"
    return slot, normalize_obj_phrase(obj)

def build_ambiguity(state: State, utterance: str) -> Optional[Ambiguity]:
    extracted = extract_pronoun_obj(utterance)
    if not extracted:
        return None

    slot, obj_phrase = extracted
    adj, head = split_obj_phrase(obj_phrase)
    predicate_attr = None
    pm = PRED_ATTR_PATTERN.search(utterance)
    if pm:
        predicate_attr = normalize_ws(pm.group(1).lower())

    required_attr = predicate_attr or adj
    candidates = sorted(state.entities.keys())

    allowed = {c.lower(): c for c in candidates}

    return Ambiguity(
        ambig_id=f"ambig-{state.turn_index}",
        ambig_type="reference",
        span=f"{slot} {head}",
        slot=slot,
        obj_phrase=obj_phrase,
        head=head,
        required_attr=required_attr,
        predicate_attr=predicate_attr,
        candidates=candidates,
        question=f'Is "{slot} {head}" referring to ' + " or ".join(f"{c}’s {head}" for c in candidates) + "?",
        allowed_answers=allowed,
    )


def admissibility_check(state: State, amb: Ambiguity) -> List[str]:
    supported = [c for c in amb.candidates if subject_has_head(state, c, amb.head)]
    if amb.required_attr:
        supported = [
            c for c in supported
            if subject_head_has_attr(state, c, amb.head, amb.required_attr)
        ]
    return supported


# ----------------------------
# Commit logic
# ----------------------------

def commit_predicate_attr(state: State, chosen: str, amb: Ambiguity):
    if amb.predicate_attr:
        add_attr(state, chosen, amb.head, amb.predicate_attr)
        return f"{chosen}.{amb.head} has_attr {amb.predicate_attr}"
    return None


# ----------------------------
# Engine step
# ----------------------------

def step(state: State, user_input: str) -> Dict:
    state.turn_index += 1

    if state.pending_ambiguity:
        amb = state.pending_ambiguity
        chosen = amb.allowed_answers.get(user_input.lower())
        if not chosen:
            return {"mode": "AWAITING_CLARIFICATION", "accepted": False}

        state.pending_ambiguity = None
        commit = commit_predicate_attr(state, chosen, amb)
        resolved = re.sub(
            rf"\b{amb.slot}\s+{amb.head}\b",
            f"{chosen}’s {amb.head}",
            state.suspended_utterance,
            flags=re.IGNORECASE,
        )
        return {
            "mode": "RESOLVED",
            "resolved": resolved,
            "commit": commit,
        }

    parse_and_update_state(state, user_input)
    amb = build_ambiguity(state, user_input)
    if not amb:
        return {"mode": "NORMAL"}

    supported = admissibility_check(state, amb)
    if len(supported) == 1:
        chosen = supported[0]
        commit = commit_predicate_attr(state, chosen, amb)
        return {
            "mode": "RESOLVED",
            "resolved": re.sub(
                rf"\b{amb.slot}\s+{amb.head}\b",
                f"{chosen}’s {amb.head}",
                user_input,
                flags=re.IGNORECASE,
            ),
            "commit": commit,
        }

    state.pending_ambiguity = amb
    state.suspended_utterance = user_input
    return {"mode": "STOP", "ambiguity": amb}


# ----------------------------
# CLI
# ----------------------------

def main():
    state = State()
    print("Aurora CLI Demo (Minimal) — v7.1")

    while True:
        prompt = "clarify> " if state.pending_ambiguity else "> "
        try:
            text = input(prompt).strip()
        except EOFError:
            break
        if not text:
            continue
        if text == "/reset":
            state = State()
            print("State reset.")
            continue
        if text == "/quit":
            break

        out = step(state, text)

        if out["mode"] == "STOP":
            amb = out["ambiguity"]
            print("\nSTOP: CLARIFICATION REQUIRED")
            print("Q:", amb.question)
            print("Answer with one of:", ", ".join(amb.candidates), "\n")

        if out["mode"] == "RESOLVED":
            print("\nRESOLVED INTERPRETATION")
            print(out["resolved"])
            if out.get("commit"):
                print("POST-COMMIT:", out["commit"])
            print("END\n")
            return


if __name__ == "__main__":
    main()
