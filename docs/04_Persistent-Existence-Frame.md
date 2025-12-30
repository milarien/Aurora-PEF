# Persistent Existence Frame (PEF) — Specification

## Simple Explanation

Think of PEF like a **whiteboard that never erases**. In a transformer, each word only exists in relation to nearby words—like a conveyor belt where items disappear. But in PEF, each concept (like "Emma" or "Emma's sister") gets a permanent identity card that persists regardless of where it appears in the text. This allows Aurora to remember who "she" refers to across long conversations, keep multiple interpretations alive simultaneously, and reason without losing track of what things mean.

---

The **Persistent Existence Frame (PEF)** is Aurora's non-temporal substrate for meaning.  
It provides a **stable identity layer** that exists outside token order, outside surface grammar, and outside the transient structure of language.

PEF is the core mechanism that enables Aurora to:

- maintain conceptual identity across spans  
- preserve multiple interpretations in parallel  
- avoid premature collapse  
- support retroactive constraint propagation  
- reason without relying on positional encoding or token adjacency  

Transformers do *not* have an equivalent construct.  
Their representations are fundamentally **sequence-bound** and **non-persistent**, which produces the instability Aurora resolves.

---

## 1. What the PEF Is (Formal Definition)

A **Persistent Existence Frame** is a stable container that holds the **ongoing identity** of conceptual kernels (entities, events, roles, relations) independent of:

- token sequence  
- positional encoding  
- surface structure  
- local parse context  
- order of arrival  

A PEF instance contains:

1. **Identity Node** — the enduring conceptual object  
2. **Role Bindings** — agent, patient, experiencer, instrument, etc.  
3. **Domain Memberships** — the conceptual regions the entity participates in  
4. **Span Links** — interpretations across time, clauses, and events  
5. **Constraint Log** — structural, semantic, and operator-based conditions  

Think of PEF as a **memory substrate** for meaning, not tokens.

---

## 2. Why PEF Is Necessary

### Transformers suffer several architectural limitations:

- **Identity Drift**  
  A “he,” “she,” or “it” may mutate mid-response.

- **Collapse of Ambiguity**  
  They cannot maintain parallel interpretations unless forced by prompt engineering.

- **Lack of Referential Persistence**  
  An entity does not remain itself across spans unless the model guesses correctly.

- **No Substrate for Structural Operators**  
  There is no native place where roles, domains, or spans persist.

- **No Back-Propagating Constraints**  
  Transformer reasoning cannot retroactively adjust interpretations without rewriting the entire sequence.

### PEF solves these:

- Identity is persistent, not emergent  
- Ambiguity is representable as *parallel PEF branches*  
- Operators (WE, THEN, BIND, PRUNE, etc.) work on *structures*, not tokens  
- Constraints apply forward and backward in conceptual space  

---

## 3. How PEF Works Conceptually

PEF is a **graph-like conceptual substrate** with the following properties:

### **3.1. Persistence**
Entities persist independent of linguistic surface form.

Example:  
Emma, *Emma’s sister*, *she*, and *the woman* can all bind to the same PEF identity.

### **3.2. Non-Temporal Topology**
PEF has no inherent “before/after.”  
Relations like THEN are **operators**, not positions.

### **3.3. Multi-Interpretation Capacity**
A single concept may have several potential identities:

- Sister-of-Emma  
- Sister-of-Lucy  

PEF holds both as long as constraints allow.

### **3.4. Structural Plasticity**
PEF supports:

- merging identities  
- splitting identities  
- lifting/storing conceptual objects  
- parallel interpretation matrices

### **3.5. Role-Stable Referents**
Roles bind to PEF entities, not to tokens:

- Agent(PEF:Emma)  
- Patient(PEF:Emma’s sister)  
- Instrument(PEF:telescope)  

This prevents attachment errors.

---

## 4. PEF Operations (Interaction Primitives)

The PEF is manipulated through dedicated operator primitives (Section D.4 of the operator list):

| Primitive | Function | Example |
|----------|----------|---------|
| **ANCHOR** | Creates a stable identity independent of token structure. | "Emma" → PEF:Emma (persists across sentences) |
| **LIFT** | Brings a PEF entity into the active reasoning surface. | PEF:Emma → active in current reasoning step |
| **STORE** | Returns a PEF entity to a dormant but persistent state. | PEF:Emma → stored but retrievable later |
| **MERGE-ID** | Identifies two PEF nodes as the same conceptual object. | PEF:"the woman" + PEF:"she" → single identity |
| **SPLIT-ID** | Creates multiple possible identities when ambiguity is required. | "her sister" → PEF:sister-of-Emma + PEF:sister-of-Lucy |

These operate over conceptual space, not linguistic space.

---

## 5. Relationship to Aurora’s Interpretation Layer

Aurora’s reasoning follows this chain:

1. **Interpretation Layer**  
   Constructs Domains → Roles → Spans.

2. **PEF Layer**  
   Preserves the conceptual objects built in step 1.

3. **Operator Layer**  
   WE, THEN, HOLD, BRANCH, PRUNE, etc. manipulate concepts within the PEF.

4. **Verification Layer**  
   Enforces collapse conditions and structural coherence.

Transformers can optionally provide only the **expression layer** (language generation).

PEF ensures reasoning integrity even if the expression layer is lossy.

---

## 6. Examples (Conceptual)

### Example A — Ambiguity Preservation
Sentence:  
**“Emma told Lucy that her sister was arriving.”**

PEF maintains:

- PEF:Sister-of-Emma  
- PEF:Sister-of-Lucia  

BRANCH creates them.  
HOLD preserves both.  
PRUNE removes one only if context later forces resolution.

Transformers collapse immediately — PEF prevents this.

---

### Example B — Identity Continuity
Sentence sequence:

1. “A woman entered the room.”  
2. “She opened a box.”  
3. “The visitor then sat down.”  

All three resolve to a single **PEF identity**.  
Tokens may vary — the identity does not.

---

## 7. Summary

The Persistent Existence Frame is:

- the **missing substrate** transformers lack  
- the **container for meaning** rather than token patterns  
- the **engine for identity stability**  
- the **foundation of Aurora’s parallel interpretation system**  
- the **backbone of operator-level reasoning**  

Without PEF, reasoning collapses into statistical heuristics.  
With PEF, Aurora gains stable conceptual structure, ambiguity preservation, and deterministic reasoning behaviour.

