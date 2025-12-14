# Aurora CLI Demo — Explicit Ambiguity Handling

This demo illustrates a core Aurora invariant:

> When ambiguity is linguistic or referential, the system must refuse to proceed
> and ask a clarification question about the utterance itself.

The refusal is **correct reasoning**, not failure.

---

## Reasoning Contract

This demo enforces the following rules:

- No facts are invented.
- Constraints are applied only when their prerequisites are satisfied.
- Ambiguity triggers a hard STOP if collapse is not guaranteed.
- Clarification questions target the utterance, not the world.
- Only constrained clarification answers are accepted.
- All outputs after clarification are **resolved interpretations**, not assertions
  about the world.

---

## Running the Demo

```bash
python aurora_cli_demo.py
```
## Example Interaction
> Emma has a sister
> Lucy has a sister
> Her sister is nice.

STOP: CLARIFICATION REQUIRED
I cannot proceed without clarification.
Q: Is "her sister" referring to Emma’s sister or Lucy’s sister?

clarify> Luc
(Not accepted: answer_not_in_allowed_set. Please answer with one candidate name.)

clarify> Lucy

RESOLVED INTERPRETATION
Lucy’s sister is nice.
Note: This output is a resolved interpretation of the utterance, not a world assertion.
END (press Enter to exit)

## Non-Goals

This demo does NOT:

- guess referents
- infer world facts
- continue execution under ambiguity
- optimise, generalise, or learn

Its purpose is to make ambiguity handling explicit, deterministic, and auditable.
