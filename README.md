This repository addresses a specific architectural failure in LLMs:
the inability to maintain epistemic legitimacy under pressure.

The goal is not better answers, but structurally justified conclusions — including refusal — under audit.

### New readers: Start with [EPISTEMIC_LEGITIMACY.md](EPISTEMIC_LEGITIMACY.md) for the governing frame of this work.

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

Some components are intentionally minimal or constrained in order to separate
**behavioral evidence** from **mechanism disclosure**.

### Start here:

1. **Live Admissibility Gate Demo (web)**  
   Canonical execution path demonstrating STOP → clarify → bind → resolve.  
   👉 https://milarien.github.io/Aurora-PEF/

2. **Failure Taxonomy**  
   Architectural failure classes under incomplete information.  
   👉 [docs/Taxonomy/Failure_Taxonomy.md](docs/Taxonomy/Failure_Taxonomy.md)

3. **Architecture Overview**  
   Structural overview of Aurora + PEF.  
   👉 [docs/01_Aurora-Architecture-Overview.md](docs/01_Aurora-Architecture-Overview.md)

4. **Runnable Minimal Demos (supporting)**  
   Epistemic state and structural witness demonstrations.  
   👉 [demos/](demos/)

---

## Demonstrators and Evidence

This repository includes a set of **minimal, runnable demonstrators** that act as
*evidentiary witnesses* for output entitlement and epistemic governance.

- See [`demos/`](./demos/) for behavior-level demonstrations.
- See [`docs/Epistemic_Legitimacy_Demonstrator.md`](./docs/Epistemic_Legitimacy_Demonstrator.md)
  for a documented, auditable example contrasting licensed vs unlicensed resolution under ambiguity.

---

## What Aurora + PEF Provides

- explicit epistemic states  
- parallel admissible interpretations  
- constraint-governed collapse  
- refusal as a valid terminal outcome  
- non-temporal persistence of meaning (PEF)  

Aurora governs reasoning.  
Transformers (optionally) handle expression.

The architecture rests on two foundations:

- the **Persistent Existence Frame (PEF)**  
- explicit **compositional primitives**

Without these, the failure analyses and demos in this repository cannot be interpreted correctly.

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
📧 margaret.stokes.ai@gmail.com  
(Research correspondence only)
