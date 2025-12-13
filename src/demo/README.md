## Prototype Demo: Context-Aware Ambiguity Engine

This repository includes a minimal, fully runnable Aurora-style ambiguity demo:

- **File:** `demo/aurora_ambiguity_demo.py`
- **Output:** `results.json` (generated on run)

What it does:

- Tracks a tiny conceptual state (`AuroraState`) with two boolean facts:  
  whether Emma has a sister and whether Lucy has a sister.
- Parses context sentences to update that state.
- Evaluates the ambiguous sentence _"Emma told Lucy that her sister was arriving."_  
  under six different context conditions.
- Produces a structured JSON trace describing:
  - status (`ambiguous_unconstrained`, `resolved_by_context`, `ambiguous_supported`)
  - which interpretations are structurally valid
  - which are context-supported
  - whether ambiguity is preserved or collapsed

### How to run

```bash
cd demo
python aurora_ambiguity_demo.py
```
## Interactive Demo: Clarification-Gated Reasoning (CLI)

This repository also includes an interactive Aurora-style CLI demo that
demonstrates **hard refusal under unresolved linguistic ambiguity**.

- File: demos/cli/aurora_cli_demo.py

What it does:

- Maintains an explicit reasoning state over discourse entities and facts
- Detects referential ambiguity at the point it is encountered
- Enforces a hard STOP when ambiguity cannot be resolved from prerequisites
- Asks a closed-form clarification question about the utterance
- Accepts only constrained clarification answers
- Resumes reasoning deterministically after clarification
- Terminates after producing a resolved interpretation (not a world assertion)

This demo exists to show that **refusal is correct reasoning**, not failure.
