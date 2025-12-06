"""
Minimal Aurora-style ambiguity substrate.

Demonstrates:
- explicit conceptual state (Emma/Lucy sister references)
- parallel interpretations represented as data structures
- context-governed resolution vs ambiguity preservation

Not a transformer, not an NLP heuristic.
A toy structural engine reflecting Aurora’s reasoning pattern.
"""

from dataclasses import dataclass, asdict
import json

# -------------------------
#   DATA STRUCTURES
# -------------------------

@dataclass
class AuroraState:
    emma_has_sister: bool = False
    lucy_has_sister: bool = False

@dataclass
class Interpretation:
    binding: str
    structurally_valid: bool
    context_supported: bool


# -------------------------
#   STATE UPDATER
# -------------------------

def update_state_with_context(state: AuroraState, sentence: str) -> None:
    # Normalize Unicode to ASCII first
    sentence = sentence.replace("’", "'")

    text = sentence.lower()
    if "emma's sister" in text:
        state.emma_has_sister = True
    if "lucy's sister" in text:
        state.lucy_has_sister = True


# -------------------------
#   AMBIGUITY EVALUATION
# -------------------------

def evaluate_ambiguity(state: AuroraState, sentence: str):
    # Normalize Unicode to ASCII
    sentence = sentence.replace("’", "'")

    interps = [
        Interpretation("Emma's sister", True, state.emma_has_sister),
        Interpretation("Lucy's sister", True, state.lucy_has_sister),
    ]

    supported = [i for i in interps if i.context_supported]

    if len(supported) == 0:
        status = "ambiguous_unconstrained"
        explanation = (
            "Both Emma's sister and Lucy's sister are structurally valid, "
            "but neither is supported by prior context. Ambiguity is preserved."
        )
        resolved_to = None

    elif len(supported) == 1:
        status = "resolved_by_context"
        explanation = (
            f"Only {supported[0].binding} is supported by prior context, "
            "so ambiguity collapses to that interpretation."
        )
        resolved_to = supported[0].binding

    else:
        status = "ambiguous_supported"
        explanation = (
            "Both Emma's sister and Lucy's sister are supported by prior context. "
            "The engine deliberately preserves ambiguity instead of forcing a choice."
        )
        resolved_to = None

    return {
        "status": status,
        "resolved_to": resolved_to,
        "explanation": explanation,
        "interpretations": [asdict(i) for i in interps],
    }


# -------------------------
#   MAIN TEST RUNNER
# -------------------------

def run_tests():
    tests = [
        {
            "name": "Test 1: No context (baseline)",
            "sentences": [
                "Emma told Lucy that her sister was arriving."
            ],
        },
        {
            "name": "Test 2: No context (variant phrasing 1)",
            "sentences": [
                "Later that day, Emma told Lucy that her sister was arriving."
            ],
        },
        {
            "name": "Test 3: No context (variant phrasing 2)",
            "sentences": [
                "The next morning, Emma told Lucy that her sister was arriving."
            ],
        },
        {
            "name": "Test 4: Emma's sister in context",
            "sentences": [
                "Emma's sister moved back from Canada last week.",
                "Emma told Lucy that her sister was arriving."
            ],
        },
        {
            "name": "Test 5: Lucy's sister in context",
            "sentences": [
                "Lucy's sister is flying in for the holidays.",
                "Emma told Lucy that her sister was arriving."
            ],
        },
        {
            "name": "Test 6: Both sisters in context",
            "sentences": [
                "Emma's sister and Lucy's sister both live overseas.",
                "Emma told Lucy that her sister was arriving."
            ],
        },
    ]

    results = []

    for test in tests:
        state = AuroraState()

        # Normalize every sentence to ASCII
        norm_sentences = [s.replace("’", "'") for s in test["sentences"]]

        *context_sentences, ambiguous = norm_sentences

        for s in context_sentences:
            update_state_with_context(state, s)

        result = evaluate_ambiguity(state, ambiguous)

        results.append({
            "test_name": test["name"],
            "input_sentences": norm_sentences,
            "result": result,
        })

    return results


# -------------------------
#   ENTRY POINT
# -------------------------

if __name__ == "__main__":
    results = run_tests()

    # Create ASCII-only, clean JSON
    output = json.dumps(results, indent=2, ensure_ascii=True)

    # Extra normalization pass
    output = output.replace("’", "'")

    print(output)

    with open("results.json", "w", encoding="ascii") as f:
        f.write(output)



