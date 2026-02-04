# Demos — Output Entitlement & Governance

Modern LLMs do not mainly fail because they lack knowledge.  
They fail because they do not know **when they are entitled to speak**.

This directory contains a set of **minimal, behavior-level demonstrations** showing how output can be **refused, constrained, clarified, or terminated** at runtime — independent of model training or prompting.

These demos function as **evidentiary witnesses**, not products.

---

## ▶ Run the live guided demo (recommended)

**Live demo (no install):**  
https://Aurora-Governor.github.io/Aurora-PEF/

The guided demo shows a full **STOP → clarify → bind → resolve** loop enforced by an external gate:

- refusal as a first-class outcome  
- clarification without free chat  
- resolution only after explicit binding  
- termination at the entitlement boundary  

The runnable implementation is intentionally deployed externally.

---

## What’s in this directory

All folders listed below are located under `demos/`.

| Folder | Purpose |
|------|--------|
| `01_reasoning_kernel_ambiguity/` | Minimal ambiguity witnesses and failure cases |
| `02_interactive_clarification_cli/` | Earlier local clarification experiments (superseded) |
| `03_aurora_trace_player_demo/` | Trace-based inspection of gated decisions |
| `04_operator-lattice/` | Structural primitives and operator relationships |
| `05_PEF_state_semantics_demo/` | Persistent Existence Frame (epistemic state) demo |
| `epistemic_legitimacy_pronoun_binding/` | Minimal demonstrator of licensed vs unlicensed resolution under ambiguity |

Each folder contains its own README explaining scope and intent.

Some demos isolate a single epistemic failure mode (e.g. ambiguity collapse) to make refusal as a correct outcome directly observable.

---

## Why the live demo runs externally

This repository documents the **contract and evidence**.  
The live demo demonstrates **behavior under constraint**.

Separating them prevents:

- trivial code extraction  
- partial reproduction without governance  
- confusion between explanation and enforcement  

---

## Status

Local demos are maintained as **evidentiary and developmental artifacts**.  
The live guided demo is the **canonical execution path**.
