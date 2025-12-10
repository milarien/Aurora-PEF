# Aurora + PEF Reasoning Framework
### A non-temporal substrate for explicit compositional reasoning

## 🚀 Start Here

If you’re new to **Aurora + PEF**, begin with:

1. [Aurora Architecture Overview](docs/Aurora-Architecture-Overview.md)
2. [Executive Summary](Whitepaper/Executive-Summary.md)
3. [Primitives](docs/primitives.md)
4. [Ambiguity Demonstrator](src/demo/)

These provide the conceptual foundation of the architecture.

---

# **Aurora + PEF Reasoning Framework**
### *A non-temporal substrate for explicit compositional reasoning*

Aurora + PEF is a structured reasoning architecture that preserves ambiguity, maintains conceptual identity, and applies explicit operators over a **non-temporal meaning substrate**.

---

## 📘 Overview

Transformers predict fluently—but they do **not** maintain:

- persistent conceptual structure  
- stable identity across spans  
- parallel interpretations  
- operator-level compositionality  
- constraint-driven coherence  

Predictive models fail in consistent, cross-platform ways:

- premature interpretive collapse  
- invented rules to “explain” choices  
- contradictory heuristics between identical structures  
- drift in world-state and premises  
- inability to keep multiple valid interpretations alive  

These are **architectural**, not trainable.

Aurora + PEF approaches meaning differently:

- **Aurora** provides explicit conceptual structure  
  (Roles → Domains → Spans, operator set: WE, THEN, WHILE, UNTIL, BECAUSE).  
- **PEF** supplies a **continuous present-state substrate**,  
  eliminating temporal modelling entirely.  
- **Transformers** (optional) are relegated to *expression only*.  
- **Aurora Verification** enforces coherence and collapse rules.

Ambiguity is not noise.  
It is the diagnostic surface revealing the absence of structured reasoning.

---

<p align="center">
  <sub>
    <a href="docs/Executive-Summary.md">Executive Summary</a> ·
    <a href="Whitepaper/Aurora%20PEF%20Final%20with%20Appendices%20v1.1.pdf">Whitepaper</a> ·
    <a href="src/demo/README.md">Demo</a> ·
    <a href="docs/primitives.md">Primitives</a> ·
    <a href="docs/pef.md">PEF Specification</a> ·
    <a href="docs/FOR_REVIEWERS.md">Review Notes</a>
  </sub>
</p>

---

# 📄 Core Documents

### **Executive Summary**  
Concise motivation + architectural outline.  
👉 [docs/Executive-Summary.md](docs/Executive-Summary.md)

### **Research Abstract**  
High-level framing, problem statement, and contribution.  
👉 [docs/Research-Abstract.md](docs/Research-Abstract.md)

### **Whitepaper (v1.1)** — *76 pages*  
Full conceptual specification including:

- empirical ambiguity failures across models  
- structural diagnosis of transformer limitations  
- operator system and topology  
- PEF substrate mechanics  
- hybrid Aurora–LLM integration pathway  
- Appendices A–D (formal structures)

👉 **[Download Whitepaper v1.1 (PDF)](Whitepaper/Aurora%20PEF%20Final%20with%20Appendices%20v1.1.pdf)**

---

# 🧩 Conceptual Components

### **Aurora Primitive Operators**  
Canonical operator set for structured reasoning.  
👉 [docs/primitives.md](docs/primitives.md)

### **Persistent Existence Frame (PEF)**  
A non-temporal substrate where conceptual states persist without positional encoding.  
👉 [docs/pef.md](docs/pef.md)

---

# 🧪 Prototype Reasoning Unit (Demonstrator)

A minimal Aurora-style engine showcasing:

- parallel interpretation maintenance  
- constraint-governed collapse  
- principled context integration  
- transparent JSON traces  

### Files:
- `src/demo/aurora_ambiguity_demo.py`  
- `src/demo/README.md`

### Run:

```bash
python src/demo/aurora_ambiguity_demo.py
```

Output appears in `results.json` (archived under `src/demo/archive/`).

This is *not* a production Aurora engine—only a substrate demonstration.

---

# **Conceptual Architecture (High-Level)**

```
User Input
    ↓
Aurora Interpretation Layer
  (Roles → Domains → Spans, explicit primitives)
    ↓
Transformer Expression Layer (optional)
  (surface language generation only)
    ↓
Aurora Verification Layer
  (constraints, collapse, coherence-checking)
    ↓
Final Structured Meaning
```

Aurora is the **reasoning physics**.  
Transformers are the **expression surface**.  
PEF is the **existential field** in which meaning persists.

---

## ⭐ Why This Matters

Transformers **approximate** language.  
Aurora + PEF **construct** meaning.

What Aurora provides:

- explicit, interpretable reasoning traces  
- persistent conceptual identity  
- non-temporal state stability  
- operator-level compositionality  
- deterministic collapse rules  
- principled ambiguity retention  

Aurora can operate independently or as a **hybrid control layer** wrapped around an LLM.

---

## 🔐 IP Notice

Protected under Australian provisional patents:

- **2025905835 — Compositional Primitives Architecture**  
- **2025905860 — Persistent Existence Frame (PEF)**  
- **2025905885 — Aurora Conceptual Blocks**  
- **2025906132 — Aurora–PEF Advanced Reasoning Engine**  

Coverage includes the substrate (PEF), conceptual state structures (Roles, Domains, Spans), the operator system, and the full Aurora reasoning cycle.

---

## 📫 Contact

**Margaret Stokes**  
📧 margaret.stokes.ai@gmail.com  
(Research correspondence only)
