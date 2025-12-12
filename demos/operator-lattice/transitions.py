# transitions.py

import re
from frame_engine import OPERATORS

# Map tokens → operator label
TOKEN_TO_OP = {
    "we":      "WE",
    "then":    "THEN",
    "because": "BECAUSE",
    "but":     "BUT",
    "if":      "IF",
}


def detect_operator(text):
    """Detect which operator is active in a line."""
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    for tok in tokens:
        if tok in TOKEN_TO_OP:
            return TOKEN_TO_OP[tok]
    return None


def _extract_steps(text):
    """
    Extract candidate step lines from:
      - numbered lines: '1. ...', '2) ...'
      - <STEP>...</STEP> tags
      - or, if none of the above, any non-empty line
    """
    lines = text.splitlines()
    steps = []

    numbered = re.compile(r"\s*\d+[\.\)]\s+(.*)")
    step_tag = re.compile(r"<STEP[^>]*>(.*?)</STEP>", re.IGNORECASE | re.DOTALL)

    # 1) numbered lines
    for line in lines:
        m = numbered.match(line)
        if m:
            steps.append(m.group(1).strip())

    # 2) <STEP> tags
    for m in step_tag.finditer(text):
        content = m.group(1).strip()
        if content:
            steps.append(content)

    # 3) fallback: any non-empty line if we found nothing else
    if not steps:
        for line in lines:
            s = line.strip()
            if s:
                steps.append(s)

    return steps


def mine_transitions_from_text(corpus_text):
    """
    Returns: dict mapping OP -> list of allowed next OP values.
    """
    steps = _extract_steps(corpus_text)

    ops = []
    for step in steps:
        op = detect_operator(step)
        if op:
            ops.append(op)

    print("DEBUG: mined operator steps:")
    for i, (step, op) in enumerate(zip(steps, ops), start=1):
        print("  %d. %r -> %s" % (i, step, op))

    transitions = {}
    for op in OPERATORS:
        transitions[op] = []

    for a, b in zip(ops, ops[1:]):
        if b not in transitions[a]:
            transitions[a].append(b)

    # fallback: ops with no outgoing edges can go to anything
    for op in OPERATORS:
        if not transitions[op]:
            transitions[op] = OPERATORS[:]

    return transitions


def mine_transitions_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return mine_transitions_from_text(text)


# Backwards compatibility for main.py if it still calls mine_transitions()
def mine_transitions(corpus_text):
    return mine_transitions_from_text(corpus_text)
