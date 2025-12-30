# Appendix D — Aurora Primitive Operators (Canonical List)

Aurora’s reasoning does not emerge from token sequences but from the interaction of conceptual kernels through a small set of **primitive operators**.

These primitives form the minimal *instruction set* for meaning-first computation.  
They operate over:

- **Roles** (agent, patient, instrument, etc.)  
- **Domains** (conceptual regions of meaning)  
- **Spans** (scope of applicability or interpretation)  
- **Persistent Existence Frames (PEFs)** — stable identity containers  

The primitive set is intentionally small.  
Its expressive power comes from **composability**, not quantity.

---

## D.1 — Structural Primitives

These govern the construction of conceptual structure.

| Primitive | Function | Example Operational Meaning | Concrete Example |
|----------|----------|------------------------------|------------------|
| **WE** (With-Event) | Establishes a co-occurring or co-constitutive relation between conceptual kernels. | "X with Y" forms a merged event-space with ambiguous attachment. | "Emma and Lucy" → WE(Emma, Lucy) |
| **THEN** | Temporal or causal successor relation between kernels. | X occurs → THEN Y, constraining possible interpretations. | "She arrived THEN she sat" → THEN(arrive, sit) |
| **BECAUSE** | Establishes causal linkage between Domains. | Links cause and effect relationships in conceptual structure. | "She left BECAUSE it rained" → BECAUSE(leave, rain) |
| **IS** | Identity or classification mapping. | Assigns a kernel to a category without forcing collapse of ambiguity. | "Emma IS a teacher" → IS(Emma, teacher) |
| **HAS** | Possession or containment linkage. | X has Y (attribute, substructure, dependency). | "Emma HAS a key" → HAS(Emma, key) |
| **IN** | Embedding relation between conceptual structures. | Interprets X within the domain of Y (physical or conceptual). | "The book IN the box" → IN(book, box) |

---

## D.2 — Ambiguity & Interpretation Primitives

These fuel Aurora’s **parallel interpretation engine**.

| Primitive | Function | Example | Concrete Example |
|----------|----------|---------|------------------|
| **BRANCH** | Spawns multiple valid interpretations without collapse. | Sister-of-Emma vs Sister-of-Lucia. | "her sister" → BRANCH(sister-of-Emma, sister-of-Lucy) |
| **HOLD** | Maintains ambiguity as an active state, preventing premature resolution. | Keeps both readings alive across spans. | HOLD maintains both "her = Emma" and "her = Lucy" interpretations |
| **PRUNE** | Removes interpretations inconsistent with downstream constraints. | Logical pruning without probabilistic collapse. | PRUNE removes "sister-of-Emma" if context shows it's impossible |
| **BIND** | Anchors an interpretation to a role when constraints require it. | Attaches "with a telescope" to "saw" vs "sister." | BIND("with telescope", "saw") when context forces attachment |
| **TRACE** | Produces explicit reasoning chains for each surviving interpretation. | Transparent logs for alignment/debugging. | TRACE generates audit log showing reasoning path |

---

## D.3 — Constraint & Topology Primitives

These operate over the **conceptual geometry** rather than tokens.

| Primitive | Function |
|----------|----------|
| **SPREAD** | Distributes a concept across multiple domains where semantically admissible. |
| **LIMIT** | Narrows a domain when constraints prohibit spread. |
| **FUSE** | Merges two conceptual kernels into a single event-structure when roles/domains converge. |
| **SEPARATE** | Forces distinction where fusion violates constraints. |
| **ECHO** | Propagates a constraint backward through the interpretation chain (retroactive pruning). |

---

## D.4 — PEF-Interaction Primitives

These govern the **persistence and identity** structure within the PEF.

| Primitive | Function |
|----------|----------|
| **ANCHOR** | Establishes a persistent identity outside token space. |
| **LIFT** | Brings a PEF entity into the active reasoning surface. |
| **STORE** | Returns an entity to a dormant but stable state. |
| **MERGE-ID** | Identifies two PEF entities as the same conceptual object. |
| **SPLIT-ID** | Divides a PEF identity into multiple conceptual roles. |

---

## D.5 — Summary Table (Engineer-Friendly)

| Category | Key Operators |
|----------|----------------|
| **Structural** | WE, THEN, IS, HAS, IN |
| **Ambiguity Engine** | BRANCH, HOLD, PRUNE, BIND, TRACE |
| **Topology** | SPREAD, LIMIT, FUSE, SEPARATE, ECHO |
| **PEF Dynamics** | ANCHOR, LIFT, STORE, MERGE-ID, SPLIT-ID |

---

This canonical list defines the **operator-level semantics** that Aurora uses to construct, preserve, manipulate, and collapse conceptual interpretations independently of token sequences.

