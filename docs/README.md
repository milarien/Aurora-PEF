# Aurora + PEF — Documentation

This directory contains the **architectural documentation, evidence, and live demonstration assets**
for the Aurora + Persistent Existence Frame (PEF) framework.

The materials here support the claims demonstrated in the live admissibility gate demo and
the runnable minimal demos in `/demos/`.

This is not end-user documentation.  
It is an **evidentiary and architectural record**.

---

## How to Navigate This Documentation

### 1. Live Admissibility Gate Demo (web)

The canonical execution path for demonstrating output entitlement, refusal, clarification,
and termination under constraint.

👉 https://Aurora-Governor.github.io/Aurora-PEF/

Source files:
- [index.html](index.html)
- [demo.js](demo.js)
- [style.css](style.css)

---

### 2. Failure Taxonomy

A systematic classification of architectural failure modes observed across transformer-based LLMs
under incomplete or underspecified information.

👉 [Taxonomy/Failure_Taxonomy.md](Taxonomy/Failure_Taxonomy.md)  
👉 [Taxonomy/README.md](Taxonomy/README.md)

This taxonomy provides the empirical motivation for Aurora + PEF.

---

### 3. Architecture Overview

High-level structural documentation describing how Aurora + PEF is composed and why
constraint-first reasoning is required.

- 👉 [01_Aurora-Architecture-Overview.md](01_Aurora-Architecture-Overview.md)
- 👉 [04_Persistent-Existence-Frame.md](04_Persistent-Existence-Frame.md)
- 👉 [05_Compositional-Primitives.md](05_Compositional-Primitives.md)

These documents explain the separation between:
- epistemic state (PEF),
- compositional reasoning (Aurora),
- and surface-level language generation.

---

### 4. Executive & Research Summaries

Concise, reviewer-oriented summaries of the work.

- 👉 [02_Executive-Summary.md](02_Executive-Summary.md)
- 👉 [03_Research-Abstract.md](03_Research-Abstract.md)
- 👉 [FOR_REVIEWERS.md](FOR_REVIEWERS.md)

---

### 5. Evidence & Transcripts

Raw transcripts and captured outputs used as empirical evidence in the failure taxonomy
and comparative analysis.

👉 [Evidence/Model_Transcripts/](Evidence/Model_Transcripts/)

---

## Relationship to `/demos/`

The documentation in this directory explains and justifies the behavior shown in:

👉 [`/demos/`](../demos/)

In particular:
- the **PEF minimal demo** demonstrates epistemic state persistence without resolution,
- the **reasoning kernel and trace demos** act as structural and evidentiary witnesses.

The live web demo shows **when** a system may speak.  
The PEF demo shows **what exists when it cannot**.

---

## Scope Note

The examples in this documentation frequently use ambiguity as a minimal witness.
The same architectural issues generalize to:

- causal reasoning
- explanation generation
- intent attribution
- policy and rule interpretation
- epistemic overreach

---

## Status

This documentation is current and maintained.  
Superseded or historical materials are explicitly marked elsewhere in the repository.
