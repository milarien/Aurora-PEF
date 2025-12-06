<p align="left">
  <img src="https://img.shields.io/badge/architecture-Aurora+PEF-blueviolet" alt="Aurora+PEF Architecture">
  <img src="https://img.shields.io/badge/license-Custom%20Non--Commercial-important" alt="Custom License">
  <img src="https://img.shields.io/badge/language-Python%203.10+-yellow" alt="Python Version">
  <img src="https://img.shields.io/badge/status-Research%20Prototype-lightgrey" alt="Status">
</p>

# Aurora + PEF Reasoning Framework
### *A structural alternative to transformer-based reasoning*

**Status:** Research Architecture (Conceptual Specification + Empirical Evidence)  
**Primary Goal:** Provide an explicit, interpretable reasoning substrate that resolves architectural limitations in transformer models.

---

## Overview

Aurora + PEF is a **meaning-first reasoning architecture** developed in response to reproducible, cross-model failures observed in modern transformer systems, including:

- **premature ambiguity collapse**  
- **invented grammatical or causal rules**  
- **input mutation and premise drift**  
- **irreversible interpretive collapse**  
- **cross-model hallucination propagation**  
- **loss of persistent conceptual identity**

These behaviours were observed across Grok, GPT-4, Gemini, and Claude in controlled tests.  
They arise **not from training gaps**, but from the representational limits of attention-based sequence modelling.

Aurora separates the components that transformers conflate:

1. **Interpretation** — structured meaning formation (Aurora)  
2. **Expression** — linguistic realization (LLM)  
3. **Verification** — constraint-based audit for fidelity (Aurora)

Transformers remain linguistic engines.  
**Aurora governs meaning.**  
**PEF stabilises the world in which meaning exists.**

---

## Key Documents

📄 **Executive Summary**  
`docs/Executive-Summary.md`

📄 **Research Abstract**  
`docs/Research-Abstract.md`

---

## Repository Contents

### **1. Aurora + PEF Architecture (Whitepaper v1.1)**  
Comprehensive 76-page document including:

- empirical tests across four transformer families  
- structural diagnosis of failure modes  
- full Aurora primitive system (WE, THEN, WHILE, UNTIL, BECAUSE, etc.)  
- Persistent Existence Frame (PEF): a non-temporal substrate  
- computational feasibility analysis  
- hybrid integration pathway (Interpret → LLM → Verify)

### **2. Appendices A–D**  
Raw, reproducible evidence:

- Grok ambiguity suite (6 tests)  
- GPT-4 & Gemini replication  
- Claude hallucination cascade failure  
- canonical primitive operator set  

### **3. Diagrams**  
Conceptual architecture figures and interpretive flow maps.

> **Note:** This repository provides documentation and evidence.  
> It does *not* include a full production implementation.

---

## Whitepaper Access

All formal materials are located in:


Contents include:

- conceptual foundations  
- empirical demonstrations  
- Aurora interpretive model  
- PEF reconstructive/state framework  
- integration with transformers  
- implications for safety, reasoning, and multi-agent stability  

---

## Purpose of This Release

This repository is intended to:

- support **research evaluation and critique**, especially in interpretability and alignment  
- provide a **reproducible empirical dataset** demonstrating transformer limitations  
- document a **coherent alternative conceptual substrate**  
- invite **collaboration, review, and technical discussion**

---

## Status

Aurora + PEF is an active research architecture.  
This repository contains:

- the conceptual specification  
- empirical evidence  
- supporting documents for technical review  

Future development will proceed through structured collaboration.

---

## Contact

For research dialogue or collaboration enquiries:  
**Margaret Stokes**  
via GitHub or the email listed in the whitepaper

---
