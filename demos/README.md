# Aurora-PEF — Output Entitlement & Governance Demos

Modern LLMs do not mainly fail because they lack knowledge.  
They fail because they do not know **when they are entitled to speak**.

This repository documents a set of minimal, behavior-level demonstrations showing how output can be **refused, constrained, clarified, or terminated** at runtime — independent of model training or prompting.

---

## ▶ Run the live guided demo (recommended)

**Live demo (no install):**  
https://milarien.github.io/aurora-pef/

The guided demo shows a full **STOP → clarify → bind → resolve** loop enforced by an external gate:
- refusal as a first-class outcome
- clarification without free chat
- resolution only after explicit binding
- termination at the entitlement boundary

The runnable implementation is intentionally deployed externally.

---

## What’s in this repository

| Folder | Purpose |
|------|--------|
| `01_reasoning_kernel_ambiguity/` | Minimal ambiguity witnesses and failure cases |
| `02_interactive_clarification_cli/` | Earlier local clarification experiments (superseded) |
| `03_aurora_trace_player_demo/` | Trace-based inspection of gated decisions |
| `04_operator-lattice/` | Structural primitives and operator relationships |
| `05_PEF_minimal_demo/` | Minimal Persistent Existence Frame example |

Each folder contains its own README explaining scope and intent.

---

## Why the live demo runs externally

This repository demonstrates the **contract and evidence**.  
The live demo demonstrates **behavior under constraint**.

Separating them prevents:
- trivial code extraction
- partial reproduction without governance
- confusion between explanation and enforcement

---

## Status

The local gated demo has been retired.  
The Cloudflare-hosted guided demo is the canonical execution path.
