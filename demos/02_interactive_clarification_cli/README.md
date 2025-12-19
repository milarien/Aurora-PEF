# Demos

# Interactive Clarification Demo (Web)

This demo is hosted as a live behavior-only witness.

- Web demo: https://milarien.github.io/Aurora-PEF/
- API endpoint (POST-only): https://aurora-clarify.milamba.workers.dev

The public repo intentionally does not ship the interactive CLI source.
The point of this demo is the reasoning contract: STOP → clarify → commit,
without exposing internal state, scoring, or trace mechanics.


The included trace player allows readers to inspect refusal, clarification, and commitment behavior step-by-step, without relying on executable heuristics.

---

## What This Is (and Is Not)

This demo is a **constraint‑governed reasoning** demonstrator.

It is **not**:

* a language model
* a chatbot
* a natural language processing system
* a claim about scalability or performance

Language is used only as a **human‑readable input notation** for candidate propositions. The demo does not model grammar, discourse, pragmatics, or conversational skill.

Evaluate it as a reasoning control system: **rules that govern when a conclusion is permitted**, and when the system must stop.

---

## The Contract This Demo Enforces

The demo enforces the following invariants:

1. **Ambiguity is detected, not ignored**
   If more than one coherent interpretation is available, execution halts.

2. **Clarification is required to proceed**
   The system asks a targeted question about the utterance itself, then continues only after an explicit binding is provided.

3. **State updates require binding**
   Attributes are committed only once the relevant referent is unambiguously resolved.

4. **Committed structure enables later resolution**
   Once bindings exist, later ambiguous utterances may collapse deterministically without further clarification.

These rules are intentionally small and inspectable.

---

## Example

```
> Sally had a dog.
> Jenny had a dog.
> Her dog was louder.

STOP: CLARIFICATION REQUIRED
Q: Is "her dog" referring to Jenny's dog or Sally's dog?

clarify> Sally

POST-COMMIT: Sally.dog has_attr comp_er:loud

> Her dog was louder.

RESOLVED BY CONTEXT
Sally's dog was louder.
```

The second occurrence resolves without clarification because the necessary binding was previously committed.

---

## On “Hard‑Coded”

This system does **not** encode answers.
It encodes the **conditions under which an answer is justified**.

Hard‑coded systems select outcomes.
This system constrains admissible state transitions.

---

## Why This Matters

Most deployed language systems are optimized for **fluent continuation**. That pressure favors *guessing* over *withholding* when information is missing, and it masks uncertainty with confident prose.

This demo isolates a specific failure mode: **unauthorized certainty**.

It demonstrates a minimal alternative:

> Progress is conditional on epistemic legitimacy, not on fluency.

The visible guarantee is the point:

* no invented facts
* no commitments without binding
* no resolution without justification

That control surface is foundational anywhere trust, auditability, or responsibility matter.
