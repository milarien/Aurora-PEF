# Aurora + PEF  
### Explicit compositional reasoning on a non-temporal substrate

Aurora + PEF is a structure-first reasoning framework designed to address
systematic failures in transformer-based language models.

Transformers optimize for fluent continuation.
Aurora constructs and governs meaning.

---

## What Problem This Addresses

Across models and vendors, LLMs exhibit the same failures:

- premature interpretive collapse
- invented rules or events to justify answers
- contradictory heuristics across identical structures
- inability to refuse commitment under insufficient information

These failures are **architectural**, not trainable.

Aurora + PEF demonstrates why — and what properties are required to avoid them.

---

## How to Approach This Repository

This repository is **not** a product release.
It is an **architectural and evidentiary artifact**.

Some components are intentionally minimal or constrained to separate
**behavioral evidence** from **mechanism disclosure**.

### Start here:

1. **Live Admissibility Gate Demo (web)**  
   https://milarien.github.io/Aurora-PEF/

2. **Failure Taxonomy**  
   Architectural failure classes under incomplete information.  
   → `docs/failure_taxonomy/`

3. **Architecture Overview**  
   How Aurora + PEF is structured.  
   → `docs/Aurora-Architecture-Overview.md`

4. **Runnable Minimal Demos**  
   Witnesses showing admissibility, refusal, and ambiguity retention.  
   → `demos/`

---

## What Aurora + PEF Provides

- explicit epistemic states
- parallel admissible interpretations
- constraint-governed collapse
- refusal as a valid terminal outcome
- non-temporal persistence of meaning (PEF)

Aurora handles reasoning.
Transformers (optionally) handle expression.

The architecture rests on two foundations: the Persistent Existence Frame (PEF) and explicit compositional primitives. Without these, the failure analyses and demos cannot be interpreted correctly.

---

## Scope Note

Ambiguity is used as a **minimal witness**, not the sole problem domain.
The same failure modes generalize to causal inference, explanation,
intent attribution, and epistemic overreach.

---

## IP Notice

Protected under Australian provisional patents covering:

- compositional primitives
- Persistent Existence Frame (PEF)
- conceptual state structures (Roles, Domains, Spans)
- the Aurora reasoning cycle

---

## Contact

Margaret Stokes  
margaret.stokes.ai@gmail.com  
(Research correspondence only)
