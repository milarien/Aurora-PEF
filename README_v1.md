<p align="center">
  <img src="docs/images/aurora_pef_logo.png" alt="Aurora + PEF Logo" width="600">
</p>

# Aurora + PEF Reasoning Framework  
### A non-temporal substrate for explicit compositional reasoning

Aurora + PEF is a structure-first reasoning architecture that preserves ambiguity, maintains persistent conceptual identity, and applies explicit compositional operators over a continuous, non-temporal meaning substrate.

Transformers approximate language.  
Aurora + PEF constructs meaning.

---

## 🚀 Start Here

If you're new to Aurora + PEF, begin here:

- **Live Admissibility Gate Demo (web):**  
  https://milarien.github.io/Aurora-PEF/

- **Architecture overview:**  
  `docs/Aurora-Architecture-Overview.md`

- **Executive summary:**  
  `docs/Executive-Summary.md`

- **Research abstract:**  
  `docs/Research-Abstract.md`

- **Primitive operators:**  
  `docs/primitives.md`

- **Persistent Existence Frame (PEF):**  
  `docs/pef.md`

- **Runnable demos:**  
  `demos/`


These provide the conceptual foundation of the architecture and explain why transformers consistently fail at structured reasoning.

---
## ▶️ Demos

Runnable, minimal demonstrations live under `demos/`.  
Each demo isolates a specific failure mode or control surface.

### 01 — Reasoning Kernel: Ambiguity
**`demos/01_reasoning_kernel_ambiguity/`**

Demonstrates:
- parallel admissible interpretations
- refusal to collapse without forcing constraints
- explicit ambiguity as a first-class state

Key files:
- `aurora_ambiguity_demo.py`
- `cli_demo.py`

---

### 02 — Interactive Clarification CLI
**`demos/02_interactive_clarification_cli/`**

Demonstrates:
- hard STOP on unresolved ambiguity
- clarification questions that target the utterance, not the world
- refusal as correct reasoning

Key file:
- `aurora_cli_demo.py`

---

### 03 — Constraint Governance / Extraction
**`demos/03_constraint_governance_extraction/`**

Demonstrates:
- constraint-scoped interpretation
- refusal of unsupported premise injection
- explicit extraction traces

Key files:
- `clean_extract.py`
- `extractor_prompt.txt`
- example inputs (`input_*.txt`)

---

### Operator Lattice Prototype
**`demos/operator-lattice/`**

Experimental prototype exploring:
- operator-level state transitions
- lattice-based resolution
- explicit frame traversal

This is exploratory and not presented as a finished system.

## 📘 Overview

Transformers predict fluently — but they do **not** maintain:

- persistent conceptual structure  
- stable identity across spans  
- parallel interpretations  
- operator-level compositionality  
- constraint-driven coherence  

As a result, predictive models exhibit cross-platform failure modes:

- **premature interpretive collapse**  
- invented "rules" to rationalize outputs  
- contradictory heuristics across similar prompts  
- world-state and premise drift  
- inability to sustain multiple valid interpretations  

These are **architectural**, not trainable.

Aurora + PEF addresses these gaps by separating **meaning construction** from **surface language generation**:

- **Aurora** provides explicit conceptual structure  
  *(Roles → Domains → Spans; operators: WE, THEN, WHILE, UNTIL, BECAUSE)*  
- **PEF** supplies a continuous present-state substrate  
  *(no temporal modeling, no positional encodings)*  
- **Transformers (optional)** handle expression only  
- **Aurora Verification Layer** enforces coherence and collapse rules  

Ambiguity is not noise.  
Ambiguity is the diagnostic surface revealing the absence of structured reasoning.

---

## 📄 Core Documents

### **Aurora Architecture Overview**  
High-level conceptual description of the architecture.  
👉 `docs/Aurora-Architecture-Overview.md`

### **Research Abstract**  
Problem framing + contribution.  
👉 `docs/Research-Abstract.md`

### **Whitepaper v1.1 (76 pages)**  
Full architectural specification, including:

- empirical ambiguity failures  
- diagnosis of transformer limitations  
- operator system + topology  
- PEF mechanics  
- hybrid Aurora–LLM integration  
- Appendices A–D (formal structures)

👉 Download: **Whitepaper v1.1 (PDF)**

---

## 🧩 Conceptual Components

### **Aurora Primitive Operators**  
Defined operators for structured reasoning with explicit lifecycle rules.  
👉 `docs/primitives.md`

---

### **Persistent Existence Frame (PEF)**  
A non-temporal meaning substrate where conceptual states persist.  
👉 `docs/pef.md`

---

## 🧪 Prototype Reasoning Unit (Demonstrator)

A minimal Aurora-style engine demonstrating:

- maintenance of parallel interpretations  
- constraint-governed collapse  
- principled context integration  
- transparent JSON traces  

**Files:**

- `src/demo/aurora_ambiguity_demo.py`  
- `src/demo/README.md`

**Run:**  
```bash
python src/demo/aurora_ambiguity_demo.py
```

**Output:**  
`results.json` (archived under `src/demo/archive/`)

This is a substrate demonstration, not a full Aurora engine.

---

## 🏗️ Architecture

```
User Input
    ↓
Aurora Interpretation Layer
  (Roles → Domains → Spans; explicit primitives)
    ↓
Transformer Expression Layer (optional)
  (surface language generation only)
    ↓
Aurora Verification Layer
  (constraints, collapse, coherence)
    ↓
Final Structured Meaning
```

Aurora is the reasoning physics.  
Transformers are the expression surface.  
PEF is the existential field where meaning persists.

---

## ⭐ Why This Matters

What Aurora + PEF provides:

- explicit reasoning traces
- persistent conceptual identity
- non-temporal state stability
- operator-level compositionality
- deterministic collapse rules
- principled ambiguity retention

Aurora can operate standalone, or as a hybrid compositional layer wrapped around an LLM.

---

## 🔐 IP Notice

Protected under Australian provisional patents:

- **2025905835** — Compositional Primitives Architecture
- **2025905860** — Persistent Existence Frame (PEF)
- **2025905885** — Aurora Conceptual Blocks
- **2025906132** — Aurora–PEF Advanced Reasoning Engine

Coverage includes the substrate (PEF), conceptual state structures (Roles, Domains, Spans), the operator system, and the full Aurora reasoning cycle.

---

## 📫 Contact

**Margaret Stokes**  
📧 margaret.stokes.ai@gmail.com  
(Research correspondence only)
