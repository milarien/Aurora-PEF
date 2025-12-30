#!/usr/bin/env python3
"""
demo_epistemic_gate.py

A modest first demonstrator:
- Isolate a single failure mode: ambiguity collapse under pressure (high-entropy stream)
- Show best-guess reasoning vs epistemically legitimate reasoning
- Make refusal visible as a correct outcome

This is a TOY. It is not Aurora. It is a posture proof.

Based on the same pronoun-binding ambiguity pattern used in prior empirical demos:
"Emma told Lucy that her sister was arriving. Whose sister is arriving?"
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import json
import random

# -------------------------
#   CORE DATA STRUCTURES
# -------------------------


@dataclass
class PEFState:
    """Tiny 'PEF-like' context store for one phenomenon: whether each sister is salient in prior context."""
    emma_sister_mentioned: bool = False
    lucy_sister_mentioned: bool = False


@dataclass
class Interpretation:
    binding: str
    structurally_valid: bool
    context_supported: bool


@dataclass
class Decision:
    engine: str
    status: str
    resolved_to: Optional[str]
    explanation: str
    interpretations: List[Dict]
    meta: Dict[str, object]

# -------------------------
#   INPUT STREAM GENERATION
# -------------------------

AMBIGUOUS_SENTENCE = "Emma told Lucy that her sister was arriving."

CTX_EMMA = "Emma's sister moved back from Canada last week."
CTX_LUCY = "Lucy's sister is flying in for the holidays."
CTX_BOTH = "Emma's sister and Lucy's sister both live overseas."

NOISE_POOL = [
    "Anyway—completely different topic—did you see that comet last night?",
    "I can't believe he said that. Honestly, I'm shaking.",
    "By the way, the council meeting got moved again. Typical.",
    "This is a mess. I'm not even sure what to think anymore.",
    "Random thought: koalas are basically eucalyptus-powered teddy bears.",
    "Look, ignore all that—back to what we were saying.",
    "I'm trying to be rational but my brain is doing jazz hands.",
    "Unrelated: someone keeps parking in my spot.",
    "If this keeps going, I'm going to need tea and a legal brief.",
    "No, wait—I'm overreacting. Or am I? (rhetorical; don't answer that.)",
]


def high_entropy_stream(seed: int, n_noise: int = 7) -> List[str]:
    """
    Generates a noisy/high-entropy 'conversation' leading into the ambiguous sentence.

    This version avoids accidental repetition by sampling noise WITHOUT replacement:
    we shuffle NOISE_POOL deterministically (seeded), then take the first n_noise lines.

    NOTE: This function intentionally does *not* include context lines; regimes are injected later
    to keep the demo deterministic and falsifiable.
    """
    rnd = random.Random(seed)
    pool = list(NOISE_POOL)
    rnd.shuffle(pool)
    n = max(0, min(n_noise, len(pool)))
    stream: List[str] = pool[:n]
    stream.append(AMBIGUOUS_SENTENCE)
    return stream


def inject_context(stream: List[str], regime: str) -> Tuple[List[str], List[str]]:
    """
    Deterministically injects context atoms into a high-entropy stream.

    regime ∈ { "none", "emma", "lucy", "both" }

    Returns:
        (new_stream, evidence_atoms)
    """
    if regime not in {"none", "emma", "lucy", "both"}:
        raise ValueError("regime must be one of: none, emma, lucy, both")

    evidence_atoms = {
        "none": [],
        "emma": [CTX_EMMA],
        "lucy": [CTX_LUCY],
        "both": [CTX_BOTH],
    }[regime]

    # Insert evidence early-ish but not first, so it can be 'lost' amid entropy.
    out = list(stream)
    insert_at = 1 if len(out) >= 3 else 0
    for line in reversed(evidence_atoms):
        out.insert(insert_at, line)
    return out, list(evidence_atoms)


# -------------------------
#   CONTEXT UPDATE (TINY "PEF")
# -------------------------


def normalize(s: str) -> str:
    return s.replace("’", "'").strip()


def update_pef(state: PEFState, sentence: str) -> None:
    t = normalize(sentence).lower()
    if "emma's sister" in t:
        state.emma_sister_mentioned = True
    if "lucy's sister" in t:
        state.lucy_sister_mentioned = True

def supported_bindings_from_stream(stream: List[str]) -> List[str]:
    """Return list of bindings supported by prefix evidence (excluding the ambiguous sentence)."""
    pef = PEFState()
    for s in stream[:-1]:
        update_pef(pef, s)

    supported: List[str] = []
    if pef.emma_sister_mentioned:
        supported.append("Emma's sister")
    if pef.lucy_sister_mentioned:
        supported.append("Lucy's sister")
    return supported



# -------------------------
#   ENGINE 1: "VANILLA" (BEST-GUESS COLLAPSE)
# -------------------------


def vanilla_collapse(stream: List[str], seed: int) -> Decision:
    """
    Simulates a best-guess model:
    - picks ONE binding even when multiple are supported or none are supported
    - invents a justification (post-hoc rationalization)
    - content/noise influences which heuristic gets chosen (mode switching)
    """
    rnd = random.Random(seed)
    pef = PEFState()
    for s in stream[:-1]:
        update_pef(pef, s)

    heuristics: List[Tuple[str, str]] = [
        ("SUBJECT_BIAS", "Her most naturally refers to the subject of the reporting clause (Emma)."),
        ("RECENCY", "Her refers to the most recently mentioned relevant female noun (Lucy)."),
        ("PRAGMATIC_LISTENER", "When you tell someone something like this, it's usually about them (Lucy)."),
        ("PRAGMATIC_SPEAKER", "When reporting news, the speaker often refers to their own circle (Emma)."),
    ]

    # "Pressure" feature: emotional/noisy lines nudge heuristic selection
    pressure = sum(
        1 for s in stream
        if any(x in s.lower() for x in ["shaking", "mess", "overreacting", "honestly"])
    )

    # Under higher pressure, pick a heuristic more randomly (less stable)
    if pressure >= 2:
        heuristic_name, rationale = rnd.choice(heuristics)
    else:
        heuristic_name, rationale = heuristics[0]  # stable default

    # Collapse decision (ALWAYS chooses a single binding)
    if heuristic_name in ("RECENCY", "PRAGMATIC_LISTENER"):
        resolved_to = "Lucy's sister"
    else:
        resolved_to = "Emma's sister"

    # Context consideration (neutral, audit-friendly flags)
    context_considered = rnd.random() < 0.4
    context_available = bool(pef.emma_sister_mentioned or pef.lucy_sister_mentioned)

    interps = [
        Interpretation("Emma's sister", True, pef.emma_sister_mentioned),
        Interpretation("Lucy's sister", True, pef.lucy_sister_mentioned),
    ]

    return Decision(
        engine="VANILLA",
        status="collapsed_best_guess",
        resolved_to=resolved_to,
        explanation=f"{rationale} (heuristic={heuristic_name})",
        interpretations=[asdict(i) for i in interps],
        meta={
            "heuristic": heuristic_name,
            "pressure": pressure,
            "context_available": context_available,
            "context_considered": context_considered,
        },
    )


# -------------------------
#   ENGINE 2: "GATE" (EPISTEMIC LEGITIMACY)
# -------------------------


def gate_legitimate(stream: List[str]) -> Decision:
    """
    Epistemically legitimate gate:
    - Recognize ambiguity
    - Check context support
    - Collapse only when uniquely constrained
    - Otherwise refuse / preserve ambiguity as a correct outcome

    INVARIANT:
        resolve ⇔ |SupportedBindings| = 1
        refuse  ⇔ |SupportedBindings| ∈ {0, 2}
    """
    pef = PEFState()
    for s in stream[:-1]:
        update_pef(pef, s)

    interps = [
        Interpretation("Emma's sister", True, pef.emma_sister_mentioned),
        Interpretation("Lucy's sister", True, pef.lucy_sister_mentioned),
    ]

    supported = [i for i in interps if i.context_supported]

    if len(supported) == 0:
        return Decision(
            engine="GATE",
            status="REFUSE_AMBIGUOUS_UNCONSTRAINED",
            resolved_to=None,
            explanation=(
                "Ambiguity detected ('her sister' can bind to Emma or Lucy). "
                "No prior context supports either binding, so a single conclusion is not licensed."
            ),
            interpretations=[asdict(i) for i in interps],
            meta={"supported_bindings": supported_bindings_from_stream(stream)},
        )

    if len(supported) == 1:
        return Decision(
            engine="GATE",
            status="RESOLVED_BY_CONTEXT",
            resolved_to=supported[0].binding,
            explanation=(
                f"Ambiguity detected. Prior context uniquely supports {supported[0].binding}, "
                "so collapse is licensed."
            ),
            interpretations=[asdict(i) for i in interps],
            meta={"supported_bindings": supported_bindings_from_stream(stream)},
        )

    return Decision(
        engine="GATE",
        status="REFUSE_AMBIGUOUS_SUPPORTED",
        resolved_to=None,
        explanation=(
            "Ambiguity detected. Prior context supports BOTH bindings, so collapse is not licensed. "
            "Refusal/clarification is the correct outcome."
        ),
        interpretations=[asdict(i) for i in interps],
            meta={"supported_bindings": supported_bindings_from_stream(stream)},
    )


# -------------------------
#   CLARIFICATION HANDLING
# -------------------------


def extract_entity_names(text: str, candidate_bindings: List[str]) -> List[str]:
    """
    Extract entity names from free-text clarification by matching against candidate bindings.
    
    Uses case-insensitive partial matching to find mentions of entities in the text.
    Returns list of bindings that were mentioned in the text.
    """
    text_lower = normalize(text).lower()
    matched = []
    
    for binding in candidate_bindings:
        # Extract the person's name from binding (e.g., "Emma's sister" -> "Emma")
        person_name = binding.split("'s")[0].lower()
        # Check if the person's name appears in the text
        if person_name in text_lower:
            matched.append(binding)
    
    return matched


def apply_clarification(
    clarification: str,
    candidate_bindings: List[str],
    allowed_answers: Optional[List[str]] = None
) -> Optional[str]:
    """
    Apply clarification to resolve ambiguity.
    
    Accepts free-text clarification by extracting entity names from the text,
    without requiring a fixed allowed answer list. Keeps /bind as an optional shortcut.
    
    Args:
        clarification: User's clarification input (free text or /bind command)
        candidate_bindings: List of possible bindings (e.g., ["Emma's sister", "Lucy's sister"])
        allowed_answers: Optional list of allowed answers (legacy support, ignored if provided)
    
    Returns:
        Resolved binding string if exactly one match found, None otherwise
    
    Examples:
        >>> apply_clarification("Emma", ["Emma's sister", "Lucy's sister"])
        "Emma's sister"
        
        >>> apply_clarification("/bind Emma's sister", ["Emma's sister", "Lucy's sister"])
        "Emma's sister"
        
        >>> apply_clarification("It's Emma's", ["Emma's sister", "Lucy's sister"])
        "Emma's sister"
        
        >>> apply_clarification("both", ["Emma's sister", "Lucy's sister"])
        None  # Multiple matches
    """
    # Normalize input
    clarification = normalize(clarification).strip()
    
    # Handle /bind shortcut: /bind <entity>
    if clarification.startswith("/bind"):
        # Extract entity after /bind
        entity_text = clarification[5:].strip()  # Remove "/bind"
        # Try exact match first
        for binding in candidate_bindings:
            if entity_text.lower() in binding.lower() or binding.lower() in entity_text.lower():
                return binding
        # If no exact match, fall through to entity extraction
    
    # Extract entity names from free text
    matched = extract_entity_names(clarification, candidate_bindings)
    
    # Return binding if exactly one match found
    if len(matched) == 1:
        return matched[0]
    
    # Multiple matches or no matches: return None (requires further clarification)
    return None


# -------------------------
#   RUN DEMO
# -------------------------


def pretty_stream(stream: List[str]) -> str:
    return "\n".join(f"{i+1:02d}. {s}" for i, s in enumerate(stream))


def pretty_decision(d: Decision) -> str:
    box = {
        "engine": d.engine,
        "status": d.status,
        "resolved_to": d.resolved_to,
        "explanation": d.explanation,
        "interpretations": d.interpretations,
        "meta": d.meta,
    }
    return json.dumps(box, indent=2, ensure_ascii=True)


def run_case(seed: int, regime: str) -> Dict:
    base = high_entropy_stream(seed=seed)
    stream, evidence_atoms = inject_context(base, regime=regime)

    supported = supported_bindings_from_stream(stream)
    supported_count = len(supported)

    van = vanilla_collapse(stream, seed=seed)
    gate = gate_legitimate(stream)

    return {
        "seed": seed,
        "regime": regime,
        "stream": stream,
        "evidence_atoms": evidence_atoms,
        "supported_bindings": supported,
        "supported_count": supported_count,
        "vanilla": asdict(van),
        "gate": asdict(gate),
        "delta": {
            "vanilla_collapses": van.resolved_to is not None,
            "gate_refuses": gate.resolved_to is None,
            "gate_resolves": gate.resolved_to is not None,
            "vanilla_licensed": (supported_count == 1 and van.resolved_to == supported[0]),
        },
    }


def test_clarification():
    """Test the apply_clarification function with various inputs."""
    candidate_bindings = ["Emma's sister", "Lucy's sister"]
    
    test_cases = [
        ("Emma", "Emma's sister"),
        ("Lucy", "Lucy's sister"),
        ("It's Emma's sister", "Emma's sister"),
        ("I mean Lucy", "Lucy's sister"),
        ("/bind Emma's sister", "Emma's sister"),
        ("/bind Lucy", "Lucy's sister"),
        ("both", None),  # Multiple matches
        ("neither", None),  # No matches
        ("", None),  # Empty
    ]
    
    print("\n" + "=" * 72)
    print("TESTING: apply_clarification (free-text entity extraction)")
    print("=" * 72 + "\n")
    
    for input_text, expected in test_cases:
        result = apply_clarification(input_text, candidate_bindings)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {input_text!r:30} -> {result!r:20} (expected: {expected!r})")
    
    print()


def main():
    # Deterministic 4-quadrant demonstrator:
    #   both  -> legitimate refusal (supported set size 2)
    #   emma  -> legitimate resolution (supported set size 1)
    #   lucy  -> legitimate resolution (supported set size 1)
    #   none  -> legitimate refusal (supported set size 0)
    cases = [
        run_case(seed=7, regime="both"),
        run_case(seed=11, regime="emma"),
        run_case(seed=13, regime="lucy"),
        run_case(seed=17, regime="none"),
    ]

    print("\n" + "=" * 72)
    print("MODEST DEMONSTRATOR: best-guess collapse vs epistemic legitimacy gate")
    print("=" * 72 + "\n")

    print("INVARIANT: resolve iff exactly one binding is context-supported; otherwise refuse.")
    print("          resolve \u21d4 |SupportedBindings| = 1\n")

    for idx, c in enumerate(cases, start=1):
        print(f"\n--- CASE {idx} ---")
        print(f"seed={c['seed']}, regime={c['regime']}\n")
        print("High-entropy input stream:")
        print(pretty_stream(c["stream"]))

        print("\nVANILLA decision:")
        print(pretty_decision(Decision(**c["vanilla"])))

        print("\nGATE decision:")
        print(pretty_decision(Decision(**c["gate"])))

        v_to = c["vanilla"]["resolved_to"]
        g_to = c["gate"]["resolved_to"]

        if g_to is None and v_to is not None:
            verdict = "Verdict: VANILLA collapses; GATE refuses (licensed)."
        elif g_to is not None and v_to is not None:
            verdict = "Verdict: both answer; GATE only answers because context licenses it."
        else:
            verdict = "Verdict: (unexpected) check logic."
        print("\n" + verdict)
        print("-" * 72)

    with open("demo_results.json", "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=True)

    print("\nWrote demo_results.json\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-clarification":
        test_clarification()
    else:
        main()
