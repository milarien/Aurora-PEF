# Aurora Demo Map

This repository contains several small, focused demos.
They are not alternatives to one another; they form a **deliberate progression**, each answering a different question about reasoning under constraint.

---

## ▶️ Start Here: Interactive Clarification

**Path:** `02_interactive_clarification_cli/`
**Run:** `python demos/aurora_cli_demo.py`

**Purpose:** Show the core reasoning contract *in action*.

This demo demonstrates a system that:

* halts when ambiguity is detected
* requires explicit clarification to proceed
* commits new structure only after binding
* allows later deterministic resolution once structure exists

This is the fastest way to understand what Aurora-style reasoning feels like.

---

## Auditable Kernel: Ambiguity Enumeration

**Path:** `01_reasoning_kernel_ambiguity/`
**Run:** `python demos/aurora_ambiguity_demo.py`
**Output:** `results.json`

**Purpose:** Make reasoning outcomes explicit and inspectable.

This demo:

* enumerates all structurally valid interpretations
* evaluates them under different context conditions
* preserves ambiguity where required
* emits a machine-readable JSON trace

Use this demo to verify *what* the system allows, forbids, or preserves.

---

## Boundary Demo: Constraint Governance vs LLMs

**Path:** `03_constraint_governance_llm/`

**Purpose:** Show why fluent language models cannot reliably govern ambiguity.

In this demo:

* an LLM is used only as a **proposal engine**
* it may invent, drop, or distort structure
* a separate constraint layer validates and prunes the output
* the final JSON contains only ambiguities licensed by the source text

This demo illustrates why reasoning control must be external to fluency-driven models.

---

## Conceptual Demonstrator: Operator Lattice

**Path:** `operator-lattice/`

**Purpose:** Establish a core structural claim about reasoning.

This demonstrator is intentionally deterministic and hard-coded.
It exists to show that:

* reasoning can be represented as traversal over explicit operators
  (e.g. WE, THEN, BECAUSE, BUT, IF)
* different reasoning policies can traverse the same operator topology
* different policies can reach different terminal *stances*
* those stances can be compared and evaluated

This is a **conceptual proof of structure**, not a behavioral system.

---

## Historical Demos

**Path:** `historic/`

Files in this directory are retained for provenance only.
They do not represent current Aurora behavior and should not be used for evaluation.

---

### How to Use This Repo

* **Want intuition?** Run the interactive clarification demo.
* **Want proof?** Inspect the kernel JSON output.
* **Want comparison?** Examine the LLM constraint governance demo.
* **Want structure?** Read the operator lattice demonstrator.

Each demo is intentionally small so its guarantees remain visible.

# Aurora Demo Map

This repository contains several small, focused demos.
They are not alternatives to one another; they form a **deliberate progression**, each answering a different question about reasoning under constraint.

---

## ▶️ Start Here: Interactive Clarification

**Path:** `02_interactive_clarification_cli/`
**Run:** `python demos/aurora_cli_demo.py`

**Purpose:** Show the core reasoning contract *in action*.

This demo demonstrates a system that:

* halts when ambiguity is detected
* requires explicit clarification to proceed
* commits new structure only after binding
* allows later deterministic resolution once structure exists

This is the fastest way to understand what Aurora-style reasoning feels like.

---

## Auditable Kernel: Ambiguity Enumeration

**Path:** `01_reasoning_kernel_ambiguity/`
**Run:** `python demos/aurora_ambiguity_demo.py`
**Output:** `results.json`

**Purpose:** Make reasoning outcomes explicit and inspectable.

This demo:

* enumerates all structurally valid interpretations
* evaluates them under different context conditions
* preserves ambiguity where required
* emits a machine-readable JSON trace

Use this demo to verify *what* the system allows, forbids, or preserves.

---

## Boundary Demo: Constraint Governance vs LLMs

**Path:** `03_constraint_governance_llm/`

**Purpose:** Show why fluent language models cannot reliably govern ambiguity.

In this demo:

* an LLM is used only as a **proposal engine**
* it may invent, drop, or distort structure
* a separate constraint layer validates and prunes the output
* the final JSON contains only ambiguities licensed by the source text

This demo illustrates why reasoning control must be external to fluency-driven models.

---

## Conceptual Demonstrator: Operator Lattice

**Path:** `operator-lattice/`

**Purpose:** Establish a core structural claim about reasoning.

This demonstrator is intentionally deterministic and hard-coded.
It exists to show that:

* reasoning can be represented as traversal over explicit operators
  (e.g. WE, THEN, BECAUSE, BUT, IF)
* different reasoning policies can traverse the same operator topology
* different policies can reach different terminal *stances*
* those stances can be compared and evaluated

This is a **conceptual proof of structure**, not a behavioral system.

- **PEF Reconstruction Demo (stable)** — see `DEMOs/PEF_minimal_demo/`  
  (Release: *PEF Reconstruction Demo – Stable*)


---

## Historical Demos

**Path:** `historic/`

Files in this directory are retained for provenance only.
They do not represent current Aurora behavior and should not be used for evaluation.

---

### How to Use This Repo

* **Want intuition?** Run the interactive clarification demo.
* **Want proof?** Inspect the kernel JSON output.
* **Want comparison?** Examine the LLM constraint governance demo.
* **Want structure?** Read the operator lattice demonstrator.

Each demo is intentionally small so its guarantees remain visible.



Aurora + PEF provide an explicit substrate for epistemic legitimacy: identity persistence, constraint-governed commitment, licensed collapse, and refusal as a first-class outcome — whether or not ambiguity is present.

These examples contain no ambiguity. Failures shown here arise from the absence of explicit identity, constraint-governed commitment, and licensed collapse.

