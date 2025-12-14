# Ambiguity Extraction & Constraint Governance Demo

## What this demo shows

This demo demonstrates a simple but important limitation of current Large Language Models (LLMs):

LLMs cannot reliably preserve linguistic ambiguity or obey strict structural constraints without external enforcement.

In this demo, an LLM is used **only** as a proposal engine. It suggests candidate structure, but may:

- invent extra explanations
- add spurious ambiguities
- drop required ambiguities
- violate formatting or schema rules

A separate **constraint / cleaning layer** then validates and prunes the output, producing a final, stable JSON representation that contains *only* the ambiguities licensed by the original text.

---

## What is being demonstrated

The demo contains three controlled test cases:

### 1. Trophy pronoun ambiguity

**Sentence:**  
> The trophy didn't fit in the suitcase because it was too small.

**Ambiguity:**  
- `it` → *the trophy* / *the suitcase*

---

### 2. Telescope attachment ambiguity

**Sentence:**  
> I saw the man with the telescope.

**Ambiguity:**  
- prepositional phrase attachment  
  - “I used the telescope to see the man.”  
  - “The man had the telescope.”

---

### 3. Emma / Lucy pronoun ambiguity

**Sentence:**  
> Emma told Lucy that her sister was arriving tomorrow.

**Ambiguity:**  
- `her` → *Emma* / *Lucy*

---

For each test case, the system produces:

- a **raw LLM output** (often messy or over-creative)
- a **cleaned output** that strictly conforms to predefined constraints

---

## Why this matters

LLMs are good at *generating* candidate interpretations, but poor at:

- enforcing exact schemas
- preserving ambiguity without collapsing it
- distinguishing genuine ambiguity from explanation or speculation

This demo shows that:

- constraint enforcement must live **outside** the model
- reliable downstream reasoning requires **explicit structure**
- governance cannot be delegated to probabilistic text generation

---

## What this demo is not

- This is **not** a reasoning engine
- It does **not** perform inference or collapse interpretations
- It does **not** replace LLMs

This demo only demonstrates **controlled extraction and validation of ambiguity**.

---

## Relationship to other demos

This demo is intentionally separate from the `operator_lattice` demo.

- **This demo:** extracts and governs ambiguity objects from text
- **operator_lattice:** operates *on* explicit structures once they exist

They are complementary layers, but independent demonstrations.

---

## Output format

The final output is a validated JSON object of the form:

```json
{
  "roles": [],
  "events": [],
  "ambiguities": []
}
```
If any rule is violated, the system outputs:

INVALID

## Status

- This demo is intentionally minimal, deterministic, and frozen.
- It exists as an empirical demonstration, not a production system.
