\# Demos



The current reference demo is:

```

python demos/aurora\_cli\_demo.py

```




All other demo files in this directory are historical and retained for provenance only. They do not represent current behaviour.

## What this demo demonstrates

This demo shows a minimal, explicit approach to ambiguity-aware reasoning.

In natural language, many utterances are ambiguous unless additional context is provided. Humans often resolve this ambiguity implicitly using visual cues, shared history, or unspoken assumptions. A language model does not have access to that private context.

This system treats missing information as missing, not as an invitation to guess.

Specifically, the demo enforces the following invariants:

1. **Ambiguity is detected, not ignored**  
   If multiple coherent interpretations exist, the system halts.

2. **Clarification is required to proceed**  
   The system asks a targeted question about the utterance itself.

3. **New attributes are committed only after binding**  
   State updates occur only once a referent has been explicitly resolved.

4. **Previously committed structure enables later deterministic resolution**  
   Once relevant information has been committed, later ambiguous utterances may collapse without clarification.

## Example


```

> Sally had a dog.

> Jenny had a dog.

> Her dog was louder.



STOP: CLARIFICATION REQUIRED

Q: Is "her dog" referring to Jenny's dog or Sally's dog?



clarify> Sally



POST-COMMIT: Sally.dog has\_attr comp\_er:loud



> Her dog was louder.



RESOLVED BY CONTEXT

Sally's dog was louder.

```


The second utterance resolves without clarification because the relevant attribute was previously committed.

## What this demo is (and is not)

* This is not a language model.
* This is not a chatbot.
* This is not a claim of general intelligence.

It is a minimal demonstrator of epistemic discipline: rules governing when a conclusion is allowed, rather than mechanisms for producing fluent answers.

The demo is intentionally small so that its guarantees are visible and auditable. Scaling is an engineering problem; constraint governance is the point.

## On "hard-coded" behaviour

The system does not encode outcomes.  
It encodes the conditions under which an outcome is justified.

Hard-coded systems choose answers.  
This system constrains epistemic legitimacy.

# Language here is illustrative, not normative.
