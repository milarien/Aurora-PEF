# Aurora + PEF Reasoning Framework  
### A non-temporal substrate for explicit compositional reasoning

**Status:** Research Architecture — Conceptual Specification + Empirical Evidence  
**Purpose:** Provide the structured reasoning substrate that current transformer models lack.

---

## 📘 Overview

Aurora + PEF is a meaning-first reasoning architecture developed to address structural limitations consistently observed across transformer models (Grok, GPT-4, Gemini, Claude).

Transformers predict fluently, but they do **not** maintain:

- persistent conceptual structure  
- stable identity across spans  
- parallel interpretations  
- operator-level reasoning  
- constraint-driven coherence  

Across models, the same failures recur:

- irreversible interpretive collapse  
- invented grammatical or causal rules  
- premise mutation and world-state drift  
- contradictory heuristics  
- inability to sustain multiple valid interpretations  

These are not training errors.  
They are **architectural consequences** of sequence-based attention systems.

Aurora + PEF takes a different approach:

- **Aurora** provides explicit conceptual structure (Roles → Domains → Spans) and formal operators (WE, THEN, WHILE, UNTIL, BECAUSE).  
- **PEF** (Persistent Existence Frame) supplies a **non-temporal substrate** where conceptual states persist without positional encoding.  
- **Transformers** become expression-only layers.  
- **Aurora Verification** enforces constraints, collapse conditions, and coherence.  

Ambiguity is not the “problem.”
It is the diagnostic surface exposing the deeper absence of structured reasoning.

<p align="center">
  <sub>
    <a href="docs/Executive-Summary.md">Summary</a> ·
    <a href="Whitepaper/Aurora%20PEF%20Final%20with%20Appendices%20v1.1.pdf">Whitepaper</a> ·
    <a href="src/demo/README.md">Demo</a> ·
    <a href="docs/primitives.md">Primitives</a> ·
    <a href="docs/pef.md">PEF</a> ·
    <a href="docs/FOR_REVIEWERS.md">Review Notes</a>
  </sub>
</p>

# 📄 Core Documents

### **Executive Summary**  
A concise overview of the architecture and motivation.  
👉 [Executive-Summary.md](docs/Executive-Summary.md)

### **Research Abstract**  
High-level motivation, problem framing, and architectural contribution.  
👉 [Research-Abstract.md](docs/Research-Abstract.md)

### **Whitepaper (v1.1)** — *76 pages*  
Full conceptual specification of Aurora + PEF, including:

- empirical ambiguity-resolution tests  
- structural diagnosis of transformer failure modes  
- operator system and topology  
- PEF substrate specification  
- integration pathways for hybrid Aurora–LLM systems  
- appendices A–D (formal structures)

👉 **[Download Whitepaper v1.1 (PDF)](Whitepaper/Aurora%20PEF%20Final%20with%20Appendices%20v1.1.pdf)**

---

# 🧩 Conceptual Components

### **Aurora Primitive Operators**  
Canonical operator list used for structural reasoning.  
👉 [primitives.md](docs/primitives.md)

### **Persistent Existence Frame (PEF) Specification**  
Defines Aurora’s non-temporal identity substrate and continuity model.  
👉 [pef.md](docs/pef.md)

---

# 🧪 Prototype Reasoning Unit

A minimal Aurora-style interpretation engine is provided for demonstration:

- parallel interpretation maintenance  
- context-governed collapse  
- explicit constraint evaluation  
- transparent JSON traces

### **Demo files:**  
- `src/demo/aurora_ambiguity_demo.py`  
- `src/demo/README.md`

### **Run the demo:**

```bash
python src/demo/aurora_ambiguity_demo.py
```
Output is written to results.json (archived under src/demo/archive/).

This is not a production Aurora engine — it is a conceptual substrate demonstration.

#Conceptual Architecture (High-Level)

User Input
    ↓
Aurora Interpretation Layer
(Roles → Domains → Spans, explicit primitives)
    ↓
Transformer Expression Layer
(surface language generation)
    ↓
Aurora Verification Layer
(constraint enforcement, collapse rules)
    ↓
Final Structured Meaning

Aurora supplies the reasoning physics.  
Transformers supply the linguistic surface.  
PEF supplies the field in which meaning persists.

---

## ⭐ Why This Matters

Transformers **approximate** language.  
Aurora + PEF **construct** meaning.

The architecture provides:

- explicit, interpretable reasoning  
- persistent conceptual identity  
- non-temporal state cohesion  
- operator-level compositionality  
- deterministic, inspectable reasoning traces  

Aurora may operate independently or as a **hybrid control layer** around transformer models.

---

## 🔐 IP Notice

Aurora + PEF is protected under Australian provisional patents:

- **2025905835 — Compositional Primitives Architecture**  
- **2025905860 — Persistent Existence Frame (PEF)**  
- **2025905885 — Integrated Aurora + PEF Reasoning System**  

---

## 📫 Contact

For research correspondence:  
**Margaret Stokes**  
*(Email provided in the included papers)*  

