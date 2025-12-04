# Aurora + PEF — Meaning-First Reasoning Substrate

Aurora + PEF is a **non-token, structure-first reasoning architecture** designed to run
*alongside or beneath* transformer LLMs.

Instead of treating language as a sequence of tokens to predict, Aurora operates over:

- **Conceptual kernels** in a **Persistent Existence Frame (PEF)** substrate,
- **Roles / Domains / Spans** as explicit structural handles,
- A small set of **primitive operators** (e.g. BRANCH, HOLD, PRUNE, BIND, TRACE),
- Parallel interpretations with **constraint-based pruning** instead of probabilistic collapse.

This repo provides:

- The **Aurora + PEF whitepaper (v1.0)** with empirical evidence of transformer failure modes,
- A reference **Python implementation sketch** of the core primitives and interpreter,
- A small **demo** showing how Aurora preserves and resolves ambiguity where LLMs collapse it,
- An example **sandwich pipeline**: Aurora Interpretation → LLM Expression → Aurora Verification.

---

## Repository Structure

- `whitepaper/` — Final PDF whitepaper (v1.0) with appendices.
- `diagrams/` — Architecture diagrams used in the paper.
- `src/aurora/` — Core primitives, PEF substrate, interpreter, verifier, traces.
- `src/demo/` — CLI demo and example sentences.
- `src/integrations/` — Example adapter for plugging Aurora around an LLM.
- `tests/` — Basic tests for primitives and ambiguity handling.
- `examples/` — JSON test cases and helper scripts.
- `evidence/` — Screenshots and notes corresponding to appendices.

---

## Quickstart

```bash
git clone https://github.com/<your-username>/aurora-pef.git
cd aurora-pef
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt  # if you add one
python -m src.demo.cli_demo
