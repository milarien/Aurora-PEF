# Failure Taxonomy: Epistemic Collapse Under Incomplete Information

This document classifies the failure modes observed when transformer-based language models are asked to resolve referential ambiguity under incomplete information, using the *Missing Key* scenario as a minimal witness.

The purpose of this taxonomy is not to criticize individual models, but to identify **systematic, architectural failure classes** that persist across implementations, prompting styles, and model families.

---

## The Test (Minimal Witness)

Alice has a key.
Bob has a key.
Alice’s key was last seen on the table.
The key is missing.

Where is the key?

---

## Correct Epistemic Posture

* Two candidate entities (`alice_key`, `bob_key`)
* One trace: `last_seen(alice_key) = table`
* Unknown current location for both
* Referent ambiguous
* Only admissible move: **request referent binding**

---

## Overview of Failure Classes

All observed failures fall into one or more of the following categories:

1. Forced Disambiguation
2. Action Hallucination
3. Invariant Hallucination
4. Trace → State Collapse
5. Salience-Driven Binding
6. Irreversible World-State Corruption
7. Symbolic Cosplay (Pseudo-Formal Reasoning)

Each class is described below, with concrete examples from **Grok** and **Gemini**.

---

## 1. Forced Disambiguation

**Definition**

The model resolves an ambiguous referent without being licensed to do so by the input.

**Symptom**

* Answers “where is the key?” with a specific location or owner
* Does not ask “which key?”

**Why it fails**

Ambiguity is treated as a defect to be eliminated rather than a state to be preserved.

**Observed in**

* Grok
* Gemini
* ChatGPT (various runs)

---

## 2. Action Hallucination (Grok-dominant)

**Definition**

The model invents an unstated event to explain ambiguity.

**Example (Grok)**

> “The logical conclusion is that Bob took it.”

This introduces:

* an agent (`Bob`)
* an action (`take`)
* a causal chain

None of these appear in the input.

**Formal Error**

```text
missing(X) ⇒ took(Y, X)
```

This implication does not exist.

**Why it happens**

Narrative coherence is preferred over epistemic restraint.
The model completes a *story*, not a state.

---

## 3. Invariant Hallucination (Gemini-dominant)

**Definition**

The model invents a persistent rule or invariant and then preserves it against contradictory evidence.

**Example (Gemini)**

> “Alice has a key”
> ⟹ `current_location(alice_key) = alice`

This rule is **never stated** in the input.

When faced with “the key is missing”, Gemini preserves the invented invariant by inventing a transition:

> “She picked it up.”

**Formal Error**

```text
has(Alice, key) ⇒ always_with(Alice, key)
```

**Why it happens**

Transformers optimize for constraint preservation once a pattern is inferred, even if the constraint itself is spurious.

---

## 4. Trace → State Collapse

**Definition**

A past trace (“last seen”) is treated as evidence of current state.

**Examples**

* “last seen on the table” treated as “located on the table”
* disappearance treated as a movement from that location

**Correct Distinction**

```text
past_location(X) ≠ current_location(X)
```

**Observed in**

* Grok
* Gemini

---

## 5. Salience-Driven Binding

**Definition**

The model binds a referent based on discourse salience (recency, emphasis) rather than logical license.

**Example (Gemini)**

> “By the principle of linguistic salience (recency), ‘the key’ refers to Alice’s key.”

Salience is a **heuristic**, not a binding rule.

**Why it fails**

Salience can guide interpretation, but it does not authorize commitment in the absence of disambiguating facts.

---

## 6. Irreversible World-State Corruption

**Definition**

Once the model commits to an invented state, it propagates it forward as fact.

**Example**

```text
current_location(alice_key) = bob
current_location(bob_key) = bob
```

Subsequent turns are forced to maintain internal consistency with an invalid state.

**Why this matters**

Errors are not local; they contaminate all downstream reasoning.

---

## 7. Symbolic Cosplay (Pseudo-Formal Reasoning)

**Definition**

The model uses the language of formal reasoning without performing actual constraint satisfaction.

**Examples**

* “Based on the formal logic…”
* “Constraint Satisfaction model”
* “Apply a Move command”

These constructs are **described**, not **executed**.

**Key Distinction**

* Kernel: enforces constraints
* LLM: narrates constraints

---

## Comparative Summary: Grok vs Gemini

| Aspect                | Grok                       | Gemini                                |
| :-------------------- | :------------------------- | :------------------------------------ |
| Primary hallucination | **Action** (“Bob took it”) | **Invariant** (“Alice always has it”) |
| Error style           | Narrative completion       | Rule preservation                     |
| Binding method        | Story plausibility         | Salience + invented constraints       |
| Confidence escalation | Yes                        | Strongly yes                          |
| Formal language use   | Moderate                   | Heavy (state machines, constraints)   |

Both models fail, but in **complementary ways**:

* Grok invents *events*
* Gemini invents *laws*

---

## Why These Failures Are Architectural

All failure classes arise from the same underlying properties:

* Optimization for next-token plausibility
* Lack of explicit epistemic state representation
* No first-class concept of “admissible vs inadmissible inference”
* No mechanism for persistent ambiguity

These are **not bugs**.
They are **predictable consequences** of the architecture.

---

## Contrast: Kernel-Based Reasoning

A kernel enforcing epistemic admissibility:

* Separates trace from state
* Refuses to bind without license
* Does not invent actions or invariants
* Preserves ambiguity as a valid terminal state
* Allows lawful resolution after explicit binding

This difference is **structural**, not stylistic.

---

## Conclusion

The Missing Key scenario exposes a family of failures that cannot be eliminated by:

* more data
* better prompts
* chain-of-thought
* fine-tuning

Because the failures arise **before** language generation — at the level of state construction and constraint enforcement.

This taxonomy documents those failures so they can be recognized, reproduced, and reasoned about explicitly.
