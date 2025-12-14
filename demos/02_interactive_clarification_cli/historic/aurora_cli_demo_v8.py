# ⚠️ HISTORICAL DEMO
# This file is retained for provenance only.
# It does NOT represent current Aurora behavior.
# Run demo/aurora_cli_demo.py instead.

raise RuntimeError(
    "This demo is historical. Run demo/aurora_cli_demo.py instead."
)
#!/usr/bin/env python3
"""
Aurora CLI Demo (Minimal Invariants) — v8
Proper (still minimal) attribute model with degree semantics + deterministic scoring

Core upgrade:
- Attribute is now a structured object: (base, degree)
  degree ∈ {"pos", "comp_more", "comp_less", "comp_er"}

What v8 supports (intentionally narrow but principled):
1) Explicit assertions:
   - "<Name> has|had a/an <noun>."
   - "<Name> has|had a/an <adj> <noun>."
     -> stores has(<head>)
     -> stores attr(<head>, base=<adj>, degree=pos)

2) Pronoun reference:
   - "her|his|their <noun>" or "her|his|their <adj> <noun>"
     -> builds an ambiguity object with:
        head noun
        (optional) noun-phrase attribute constraint: base=<adj>, degree=pos

3) Predicate attribute:
   - "... is|was|are|were <adj>"
   - "... is|was|are|were more <adj>"
   - "... is|was|are|were less <adj>"
   - "... is|was|are|were <adj-er>" (heuristic: bigger->big, smaller->small, etc.)
     -> builds a predicate constraint Attribute(base, degree)

4) Admissibility:
   - Candidates must have has(head) to be considered supported.
   - If there is an attribute constraint, candidates are scored:
       score 2: exact match base+degree exists
       score 1: base exists at any degree (base-only match)
       score 0: no base match
     Collapse only if there is a *unique best* candidate with score > 0.
     Otherwise STOP.

5) Commit-after-binding:
   - Predicate attributes are committed only after:
       (a) clarification binds the referent, OR
       (b) deterministic collapse selects a unique candidate
   - (Optionally) noun-phrase adjective can also be committed after binding (kept OFF by default)

This preserves the invariant: no commit without a bound referent.

Notes:
- This is still a demo. It does NOT model comparison targets (“bigger than X”).
  Comparative forms are treated as degrees of the same base attribute.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

SHOW_JSON = False

# Toggle: if True, after binding we also commit noun-phrase adjectives (e.g., "her black cat")
COMMIT_NP_ADJ_AFTER_BINDING = False


# ----------------------------
# Vocabulary guards
# ----------------------------

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

@dataclass(frozen=True)
class Attribute:
    base: str                 # e.g. "magnificent", "big"
    degree: str               # "pos" | "comp_more" | "comp_less" | "comp_er"

    def as_str(self) -> str:
        return f"{self.degree}:{self.base}"


@dataclass
class Fact:
    subject: str
    relation: str             # currently only "has"
    head: str                 # head noun only: "stick", "cat"


@dataclass
class Ambiguity:
    ambig_id: str
    span: str                 # e.g. "his stick"
    slot: str                 # "his" / "her" / "their"
    head: str                 # "stick"
    np_attr: Optional[Attribute]       # adjective from noun phrase (pos only)
    pred_attr: Optional[Attribute]     # attribute from predicate ("was more magnificent")
    candidates: List[str]
    question: str
    allowed_answers: Dict[str, str]


@dataclass
class State:
    entities: Dict[str, Dict] = field(default_factory=dict)
    facts: List[Fact] = field(default_factory=list)

    # attributes[subject][head] = set(Attribute)
    attributes: Dict[str, Dict[str, Set[Attribute]]] = field(default_factory=dict)

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

def norm(s: str) -> str:
    return normalize_ws(s.lower())

def ensure_entity(state: State, name: str) -> None:
    state.entities.setdefault(name, {"name": name})

def add_fact_has(state: State, subject: str, head: str) -> None:
    state.facts.append(Fact(subject=subject, relation="has", head=head))

def add_attr(state: State, subject: str, head: str, attr: Attribute) -> None:
    state.attributes.setdefault(subject, {}).setdefault(head, set()).add(attr)

def subject_has_head(state: State, subject: str, head: str) -> bool:
    return any(f.subject == subject and f.relation == "has" and f.head == head for f in state.facts)

def get_attrs(state: State, subject: str, head: str) -> Set[Attribute]:
    return state.attributes.get(subject, {}).get(head, set())


def split_obj_phrase(obj_phrase: str) -> Tuple[Optional[str], str]:
    """
    obj_phrase is 1 or 2 tokens:
      "stick" -> (None, "stick")
      "big stick" -> ("big", "stick")
    """
    toks = norm(obj_phrase).split()
    if not toks:
        return (None, "")
    if len(toks) == 1:
        return (None, toks[0])
    return (toks[0], toks[1])


# ----------------------------
# Comparative handling
# ----------------------------

# A tiny irregular map; keeps the demo sane without pretending to be a full lemmatizer.
IRREGULAR_ER = {
    "better": "good",
    "worse": "bad",
    "bigger": "big",
    "smaller": "small",
    "larger": "large",
    "further": "far",
    "farther": "far",
}

def parse_predicate_attribute(utterance: str) -> Optional[Attribute]:
    """
    Parses minimal predicate attribute forms:
      was tall               -> pos:tall
      was more magnificent   -> comp_more:magnificent
      was less shiny         -> comp_less:shiny
      was bigger             -> comp_er:big   (heuristic)
    """
    u = norm(utterance)

    # more/less + adjective
    m = re.search(r"\b(?:is|was|are|were)\s+(more|less)\s+([a-z]+)\b", u)
    if m:
        quant = m.group(1)
        adj = m.group(2)
        degree = "comp_more" if quant == "more" else "comp_less"
        return Attribute(base=adj, degree=degree)

    # single adjective after copula
    m = re.search(r"\b(?:is|was|are|were)\s+([a-z]+)\b", u)
    if not m:
        return None

    token = m.group(1)

    # comparative -er heuristic
    if token in IRREGULAR_ER:
        return Attribute(base=IRREGULAR_ER[token], degree="comp_er")

    if token.endswith("er") and len(token) >= 4:
        # crude but explicit: "brighter" -> "bright"
        base = token[:-2]
        return Attribute(base=base, degree="comp_er")

    return Attribute(base=token, degree="pos")


# ----------------------------
# Patterns (explicit assertions + pronoun object)
# ----------------------------

HAS_OBJ_PATTERN = re.compile(
    r"^\s*([A-Z][a-z]+)\s+(has|had)\s+a[n]?\s+([a-z]+(?:\s+[a-z]+)?)\s*\.?\s*$",
    re.IGNORECASE
)

PRONOUN_W1_W2_PATTERN = re.compile(
    r"\b(her|his|their)\s+([a-z]+)(?:\s+([a-z]+))?\b",
    re.IGNORECASE
)


def extract_pronoun_obj(utterance: str) -> Optional[Tuple[str, str]]:
    """
    Returns (slot, obj_phrase) for "his stick" / "her black cat"
    with tail-verb protection ("cat is" won't be captured).
    """
    m = PRONOUN_W1_W2_PATTERN.search(utterance)
    if not m:
        return None
    slot = m.group(1).lower()
    w1 = m.group(2).lower()
    w2 = (m.group(3) or "").lower()
    if not w2 or w2 in DISALLOWED_OBJ_TAIL:
        obj_phrase = w1
    else:
        obj_phrase = f"{w1} {w2}"
    return slot, norm(obj_phrase)


# ----------------------------
# Parsing: explicit-only state updates
# ----------------------------

def parse_and_update_state(state: State, utterance: str) -> Dict:
    rec = {
        "recognized_entities": [],
        "recognized_assertions": [],
    }

    for m in ENTITY_PATTERN.finditer(utterance):
        name = m.group(1)
        low = name.lower()
        if low in PRONOUNS or low in STOPWORDS:
            continue
        ensure_entity(state, name)
        if name not in rec["recognized_entities"]:
            rec["recognized_entities"].append(name)

    m = HAS_OBJ_PATTERN.match(utterance)
    if m:
        name = m.group(1)
        obj_phrase = norm(m.group(3))
        adj, head = split_obj_phrase(obj_phrase)
        ensure_entity(state, name)

        if head:
            add_fact_has(state, name, head)
            rec["recognized_assertions"].append(f"{name} has {head}")

        if adj and head:
            add_attr(state, name, head, Attribute(base=adj, degree="pos"))
            rec["recognized_assertions"].append(f"{name}.{head} has_attr pos:{adj}")

    return rec


# ----------------------------
# Ambiguity build + admissibility scoring
# ----------------------------

def build_ambiguity(state: State, utterance: str) -> Optional[Ambiguity]:
    extracted = extract_pronoun_obj(utterance)
    if not extracted:
        return None

    slot, obj_phrase = extracted
    adj, head = split_obj_phrase(obj_phrase)
    if not head:
        return None

    np_attr = Attribute(base=adj, degree="pos") if adj else None
    pred_attr = parse_predicate_attribute(utterance)

    candidates = sorted(state.entities.keys())
    if len(candidates) < 2:
        # Still form an ambiguity object; caller will decide how to handle.
        pass

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
        span=f"{slot} {head}",
        slot=slot,
        head=head,
        np_attr=np_attr,
        pred_attr=pred_attr,
        candidates=candidates,
        question=question,
        allowed_answers=allowed,
    )


def candidate_score_for_attr(state: State, subject: str, head: str, constraint: Attribute) -> int:
    """
    score 2: exact base+degree present
    score 1: base present at any degree (base-only match)
    score 0: no base match
    """
    attrs = get_attrs(state, subject, head)
    if constraint in attrs:
        return 2
    if any(a.base == constraint.base for a in attrs):
        return 1
    return 0


def choose_by_constraints(state: State, amb: Ambiguity) -> Tuple[Optional[str], Dict[str, int], List[str]]:
    """
    Returns:
      chosen (or None)
      per-candidate score map (only for candidates that have head)
      supported list (candidates that have head)
    """
    supported = [c for c in amb.candidates if subject_has_head(state, c, amb.head)]
    if not supported:
        return None, {}, []

    # Determine which constraint (if any) should be used for collapse:
    # Predicate attribute is stronger than NP adjective.
    constraint = amb.pred_attr or amb.np_attr
    if not constraint:
        return None, {}, supported

    scores = {c: candidate_score_for_attr(state, c, amb.head, constraint) for c in supported}
    best = max(scores.values(), default=0)
    if best <= 0:
        return None, scores, supported

    best_candidates = [c for c, s in scores.items() if s == best]
    if len(best_candidates) == 1:
        return best_candidates[0], scores, supported

    return None, scores, supported


def commit_after_binding(state: State, chosen: str, amb: Ambiguity) -> List[str]:
    """
    Commit predicate attr after binding; optionally commit NP adjective too.
    Returns audit strings.
    """
    audits: List[str] = []

    if amb.pred_attr:
        add_attr(state, chosen, amb.head, amb.pred_attr)
        audits.append(f"{chosen}.{amb.head} has_attr {amb.pred_attr.as_str()} (from predicate)")

    if COMMIT_NP_ADJ_AFTER_BINDING and amb.np_attr:
        add_attr(state, chosen, amb.head, amb.np_attr)
        audits.append(f"{chosen}.{amb.head} has_attr {amb.np_attr.as_str()} (from noun phrase)")

    return audits


# ----------------------------
# Snapshot
# ----------------------------

def snapshot_state(state: State) -> Dict:
    return {
        "entities": sorted(state.entities.keys()),
        "facts": [{"subject": f.subject, "relation": f.relation, "head": f.head} for f in state.facts],
        "attributes": {
            subj: {head: sorted([a.as_str() for a in attrs]) for head, attrs in heads.items()}
            for subj, heads in state.attributes.items()
        },
        "bindings": dict(state.bindings),
        "pending_ambiguity": None if state.pending_ambiguity is None else {
            "id": state.pending_ambiguity.ambig_id,
            "span": state.pending_ambiguity.span,
            "head": state.pending_ambiguity.head,
            "np_attr": None if state.pending_ambiguity.np_attr is None else state.pending_ambiguity.np_attr.as_str(),
            "pred_attr": None if state.pending_ambiguity.pred_attr is None else state.pending_ambiguity.pred_attr.as_str(),
            "candidates": state.pending_ambiguity.candidates,
            "question": state.pending_ambiguity.question,
        }
    }


# ----------------------------
# Engine step
# ----------------------------

def normalize_answer(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s’']", " ", text)
    tokens = text.split()
    return " ".join(tokens[:6])

def apply_clarification(state: State, answer: str) -> Tuple[bool, Optional[str], Optional[str]]:
    amb = state.pending_ambiguity
    assert amb is not None

    norm_ans = normalize_answer(answer)
    chosen = amb.allowed_answers.get(norm_ans)

    if chosen is None:
        for c in amb.candidates:
            if re.search(rf"\b{re.escape(c.lower())}\b", answer.lower()):
                chosen = c
                break

    if chosen is None:
        return False, None, "answer_not_in_allowed_set"

    state.bindings[amb.slot] = chosen
    state.pending_ambiguity = None
    return True, chosen, None


def rewrite_resolved_utterance(utterance: str, chosen: str, amb: Ambiguity) -> str:
    pattern = rf"\b{re.escape(amb.slot)}\s+{re.escape(amb.head)}\b"
    return re.sub(pattern, f"{chosen}’s {amb.head}", utterance, flags=re.IGNORECASE)


def step(state: State, user_input: str) -> Dict:
    state.turn_index += 1

    # Clarification mode
    if state.pending_ambiguity is not None:
        ok, chosen, reason = apply_clarification(state, user_input)
        out = {
            "turn": state.turn_index,
            "mode": "AWAITING_CLARIFICATION",
            "input": user_input,
            "accepted": ok,
            "reason": reason,
            "state_snapshot": snapshot_state(state),
        }
        if ok and state.suspended_utterance and state.suspended_ambiguity:
            suspended = state.suspended_utterance
            amb = state.suspended_ambiguity
            state.suspended_utterance = None
            state.suspended_ambiguity = None

            audits = commit_after_binding(state, chosen, amb)
            resolved = rewrite_resolved_utterance(suspended, chosen, amb)

            out["resume"] = {
                "resolved_utterance": resolved,
                "post_commit": audits,
            }
            out["state_snapshot"] = snapshot_state(state)
        return out

    # Normal mode: update state only via explicit assertions
    parse_rec = parse_and_update_state(state, user_input)

    amb = build_ambiguity(state, user_input)
    if amb is None:
        return {
            "turn": state.turn_index,
            "mode": "NORMAL",
            "input": user_input,
            "parse": parse_rec,
            "decision": {"status": "no_ambiguity"},
            "state_snapshot": snapshot_state(state),
        }

    chosen, scores, supported = choose_by_constraints(state, amb)

    if chosen is None:
        # STOP
        state.pending_ambiguity = amb
        state.suspended_utterance = user_input
        state.suspended_ambiguity = amb

        return {
            "turn": state.turn_index,
            "mode": "NORMAL",
            "input": user_input,
            "parse": parse_rec,
            "decision": {
                "status": "STOP_NEEDS_CLARIFICATION",
                "refusal": "I cannot proceed without clarification.",
                "question": amb.question,
                "candidates": amb.candidates,
                "head_supported": supported,
                "constraint_used": (amb.pred_attr or amb.np_attr).as_str() if (amb.pred_attr or amb.np_attr) else None,
                "scores": scores,
            },
            "state_snapshot": snapshot_state(state),
        }

    # Deterministic collapse
    state.bindings[amb.slot] = chosen
    audits = commit_after_binding(state, chosen, amb)

    return {
        "turn": state.turn_index,
        "mode": "NORMAL",
        "input": user_input,
        "parse": parse_rec,
        "decision": {
            "status": "RESOLVED_BY_CONTEXT",
            "chosen": chosen,
            "constraint_used": (amb.pred_attr or amb.np_attr).as_str() if (amb.pred_attr or amb.np_attr) else None,
            "scores": scores,
            "post_commit": audits,
        },
        "state_snapshot": snapshot_state(state),
        "resolved_utterance": rewrite_resolved_utterance(user_input, chosen, amb),
    }


# ----------------------------
# CLI
# ----------------------------

HELP = """\
Aurora CLI Demo (Minimal) — v8

Key v8 idea: attribute constraints have STRUCTURE: (base, degree)

Try (comparatives as degrees):
  /reset
  John had a big stick.
  Rob had a big stick.
  His stick was bigger.
  (STOP; clarify)
  -> commits comp_er:big to chosen stick

Try (more/less phrase):
  /reset
  John had a stick.
  Rob had a stick.
  His stick was more magnificent.
  (STOP; clarify)
  -> commits comp_more:magnificent to chosen stick

Try (collapse by stored constraint):
  /reset
  John had a magnificent stick.
  Rob had a stick.
  His stick was more magnificent.
  -> collapses to John (exact/base match wins) OR STOP if tie

Commands:
  /state
  /reset
  /quit
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

        # clarification rejection
        if trace.get("mode") == "AWAITING_CLARIFICATION" and trace.get("accepted") is False:
            print(f"(Not accepted: {trace.get('reason','rejected')}. Please answer with one candidate name.)")
            continue

        decision = trace.get("decision", {})

        if decision.get("status") == "STOP_NEEDS_CLARIFICATION":
            print("\n" + "=" * 72)
            print("STOP: CLARIFICATION REQUIRED")
            print(decision["refusal"])
            print("Q:", decision["question"])
            print("Answer with one of:", ", ".join(decision["candidates"]))
            if decision.get("constraint_used"):
                print("Constraint:", decision["constraint_used"])
            if decision.get("scores"):
                print("Scores:", decision["scores"])
            print("=" * 72 + "\n")

        # terminal success after clarification
        if trace.get("resume") is not None:
            resolved = trace["resume"]["resolved_utterance"]
            print("\n" + "-" * 72)
            print("RESOLVED INTERPRETATION")
            print(resolved)
            print("Note: This output is a resolved interpretation of the utterance, not a world assertion.")
            for a in trace["resume"].get("post_commit", []):
                print("POST-COMMIT:", a)
            print("END (press Enter to exit)")
            print("-" * 72)
            input()
            return

        # terminal-ish success on deterministic collapse (optional: keep running; demo exits here)
        if trace.get("resolved_utterance") and decision.get("status") == "RESOLVED_BY_CONTEXT":
            print("\n" + "-" * 72)
            print("RESOLVED BY CONTEXT")
            print(trace["resolved_utterance"])
            for a in decision.get("post_commit", []):
                print("POST-COMMIT:", a)
            print("END (press Enter to exit)")
            print("-" * 72)
            input()
            return

        if SHOW_JSON:
            print(json.dumps(trace, indent=2))


if __name__ == "__main__":
    main()
