# Aurora + PEF Reasoning Framework  
### *A non-temporal substrate for explicit compositional reasoning*

**Status:** Research Architecture — Conceptual Specification + Empirical Evidence  
**Purpose:** Provide the structured reasoning substrate that current transformer models lack.

---

## Overview

Aurora + PEF is a meaning-first reasoning architecture developed to address a class of **structural limitations** consistently observed across transformer systems (Grok, GPT-4, Gemini, Claude).

These limitations include:

- irreversible interpretive collapse  
- invented grammatical or causal rules  
- premise mutation and world-state drift  
- loss of persistent conceptual identity  
- contradictory reasoning heuristics  
- inability to maintain multiple valid interpretations  

These behaviours do **not** arise from training gaps.  
They are consequences of the architectural constraints of **sequence-based attention models**.

Aurora + PEF takes a different approach:

- **Aurora** provides explicit compositional reasoning using structured conceptual units (Roles → Domains → Spans) and formal operators (WE, THEN, WHILE, UNTIL, BECAUSE).  
- **PEF** (Persistent Existence Frame) provides a **non-temporal substrate** where conceptual states persist without positional or sequential encoding.  
- **Transformers** operate only as **expression layers** for linguistic realization.  
- **Aurora Verification** performs constraint-level auditing for coherence and collapse conditions.

Ambiguity is **not** the “problem” being solved.  
It is the **diagnostic case** that reveals the underlying architectural deficiency in transformer reasoning.

---

## Repository Contents

### 1. Core Papers

- **Executive Summary**  
- **Research Abstract**  
- **Full Architecture Paper (v1.1, 76 pages)**  
  Includes:  
  - empirical ambiguity tests  
  - structural diagnosis of transformer failure modes  
  - Aurora’s operator system  
  - PEF specification  
  - integration pathways  
  - conceptual diagrams  
  - appendices A–D

### 2. Empirical Evidence

Reproducible tests demonstrating structural cross-model failure:

- premature collapse when context supports multiple interpretations  
- contradictory heuristics across identical inputs  
- invented explanation rules  
- inability to sustain parallel interpretations  
- instability of conceptual identity  

These tests expose a deeper absence of:

- persistent roles  
- stable conceptual spans  
- operator-level compositionality  
- non-temporal state coherence  
- constraint-bound reasoning behaviour  

### 3. Prototype Reasoning Unit

This repository includes a **minimal Aurora interpretation prototype** that demonstrates:

- parallel interpretation maintenance  
- context-governed resolution  
- explicit collapse conditions  
- transparent reasoning traces  

**Note:** This is *not* a production implementation of Aurora or PEF.  
It is a conceptual demonstration of **substrate behaviour in isolation**.

---

## Conceptual Architecture (High-Level)

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

Aurora supplies the **reasoning physics**.  
Transformers supply the **linguistic surface**.  
PEF supplies the **field in which meaning persists**.

---

## Why This Matters

Transformers do not maintain conceptual structure.  
They do not possess explicit operators.  
They do not preserve ambiguity.  
They do not reason.

They approximate.

Aurora + PEF introduces:

- explicit, interpretable reasoning operations  
- persistent conceptual identity  
- non-temporal substrate stability  
- constraint-governed interpretation  
- deterministic, inspectable reasoning traces  

A substrate capable of reasoning independently or serving as a **hybrid control layer** around transformer systems.

---

## IP Notice

Aurora + PEF is protected by the following Australian provisional patents:

- **2025905835** — Compositional Primitives Architecture  
- **2025905860** — Persistent Existence Frame (PEF)  
- **2025905885** — Integrated Aurora + PEF Reasoning System  

---

## Contact

For research dialogue or collaboration inquiries:  
**Margaret Stokes**  
(See email information in the included papers)
