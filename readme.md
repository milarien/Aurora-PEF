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

Aurora + PEF is a **meaning-first reasoning architecture** developed in response to reproducible, cross-model failures observed in transformer systems, including:

- **premature ambiguity collapse**  
- **invented grammatical or causal rules**  
- **input mutation and premise drift**  
- **irreversible interpretive collapse**  
- **cross-model hallucination propagation**  
- **loss of persistent conceptual identity**

These behaviours were observed across Grok, GPT-4, Gemini, and Claude in controlled tests.  
They arise **not from training gaps**, but from structural limits of attention-based sequence modelling.

Aurora separates the components that transformers conflate:

1. **Interpretation** — structured meaning formation  
2. **Expression** — linguistic realization (LLM)  
3. **Verification** — constraint-based audit for fidelity  

Transformers remain linguistic engines.  
**Aurora governs meaning.**  
**PEF stabilises the world in which meaning exists.**

---

## Key Documents

📄 **Executive Summary**  
[`docs/Executive-Summary.md`](docs/Executive-Summary.md)

📄 **Research Abstract**  
[`docs/Abstract.md`](docs/Abstract.md)

📄 **Full Architecture Paper (v1.1, 76 pages)**  
[`whitepaper/Aurora PEF Final with Appendices.pdf`](whitepaper/Aurora%20PEF%20Final%20with%20Appendices.pdf)

These three documents form the core of the research release.

---

## Repository Contents

### **1. Aurora + PEF Architecture (Whitepaper v1.1)**
A complete description of:

- empirical ambiguity tests across multiple LLMs  
- structural diagnosis of transformer failure modes  
- Aurora’s primitive operator system (WE, THEN, WHILE, UNTIL, BECAUSE, etc.)  
- Persistent Existence Frame (PEF): a non-temporal interpretive substrate  
- computational feasibility and scaling behaviour  
- hybrid integration architecture (Interpret → LLM → Verify)

### **2. Appendices A–D**
Included in the whitepaper PDF:

- Grok ambiguity test suite  
- GPT-4 & Gemini replication  
- Claude cascade hallucination failure  
- canonical primitive operator set  

### **3. Diagrams**
High-level conceptual architecture figures (embedded in the PDF).

> **Note:** This repository provides documentation and empirical evidence.  
> It does *not* include a production implementation of Aurora or PEF.

---

## Purpose of This Release

This repository is intended to:

- support **technical review** by interpretability, safety, and architecture researchers  
- provide a **reproducible empirical dataset** illustrating transformer limitations  
- document a **coherent alternative substrate** for reasoning  
- enable discussion around collaboration and further development pathways  

---

## Status

Aurora + PEF is an active research architecture.  
This repository contains:

- conceptual specifications  
- empirical evidence  
- documentation for expert evaluation  

Future development will proceed through targeted research collaboration, not open-source contribution.

---

## Contact

For research dialogue or collaboration enquiries:  
**Margaret Stokes**  
via GitHub or the email listed in the whitepaper

---

