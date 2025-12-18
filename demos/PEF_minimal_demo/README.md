# PEF Reconstruction Demo

This repository contains a **minimal demonstration of constraint-first reasoning**.

The core idea is simple:

> **Some questions must not be answered until their preconditions are satisfied.**

The demo shows how enforcing explicit constraints on *referent resolution* and *information sufficiency* produces behavior that current large language models do not reliably exhibit.

---

## What This Demonstrates

The script enforces two non-negotiable constraints:

1. **Definite description constraint**  
   A phrase like *“the dog”* may only be resolved if it uniquely refers to exactly one entity.  
   If not, the system stops and asks for clarification.

2. **Information sufficiency constraint**  
   A *“where”* question may only be answered if an explicit location fact exists.  
   If not, the system refuses to guess.

Ambiguity and missing information are treated as **valid terminal states**, not errors.

---

## What This Is Not

- Not a language model  
- Not a reasoning engine  
- Not a chatbot  
- Not an attempt to be helpful by guessing  

This is a **proof-of-concept epistemic kernel**, not a product.

---

## Failure Modes (Why This Exists)

Transformer-based LLMs fail this task in systematic ways:  
they prematurely resolve ambiguity, invent events or invariants, and collapse “unknown” into narrative completion.

These failures are documented in detail here:

➡ **[Failure Taxonomy: Why LLMs Fail the Missing-Key Test](docs/failure_taxonomy.md)**

The taxonomy contrasts different failure classes (e.g. Grok vs Gemini) and explains why they are architectural rather than accidental.

---

## Running the Demo

```bash
python pef_dog_demo.py
```
