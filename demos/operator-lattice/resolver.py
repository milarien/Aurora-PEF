# resolver.py

"""
Resolver: applies operators over the frame lattice.

Adds an escape rule: if the same operator repeats 3 times, force a pivot.
This prevents sink attractors like IF -> IF -> IF forever.
"""

import random
from frame_engine import (
    CH_PATH_OP, CH_PATH_STATE,
    encode_op, decode_op,
    encode_state, decode_state,
)


def enact(op):
    """
    Toy execution semantics.
    - WE, THEN, BECAUSE always succeed.
    - BUT sometimes blocks.
    - IF sometimes blocks.
    """
    if op == "BUT":
        return "BLOCKED" if random.random() < 0.2 else "RESOLVED"
    if op == "IF":
        return "BLOCKED" if random.random() < 0.3 else "RESOLVED"
    return "RESOLVED"


def choose_next_operator(prev_op, prev_state, transitions, mode, repeat_count, max_repeat=3):
    options = transitions.get(prev_op, [])
    if not options:
        options = ["WE"]

    # If we are blocked, try a local pivot first
    if prev_state == "BLOCKED":
        for candidate in ("BUT", "THEN"):
            if candidate in options and candidate != prev_op:
                return candidate

    # ✅ Escape rule: break self-loop attractors
    if repeat_count >= max_repeat:
        # try to remove self-loop
        options_no_self = [op for op in options if op != prev_op]
        if options_no_self:
            options = options_no_self
        else:
            # graph forces a self-loop (e.g. IF -> IF), so hard pivot
            return "THEN"

    # Ranking preferences by mode
    if mode == "conservative":
        preference_order = ["WE", "THEN", "BECAUSE", "BUT", "IF"]
    elif mode == "exploratory":
        preference_order = ["IF", "BUT", "BECAUSE", "THEN", "WE"]
    else:
        preference_order = options[:]

    # Prefer best ranked option that isn't a trivial self-loop
    for preferred in preference_order:
        if preferred in options and preferred != prev_op:
            return preferred

    return options[0]


def run_lattice(frames, transitions, start_op="WE", mode="conservative"):
    T = len(frames)

    # Seed the first actionable frame (t=1)
    frames[1][CH_PATH_OP] = encode_op(start_op)

    last_op = None
    repeat_count = 0

    for t in range(1, T - 1):
        frame = frames[t]

        op = decode_op(frame[CH_PATH_OP])
        state = decode_state(frame[CH_PATH_STATE])

        # Track repeats
        if op == last_op:
            repeat_count += 1
        else:
            last_op = op
            repeat_count = 1

        # Enact if OPEN
        if state == "OPEN":
            new_state = enact(op)
            frame[CH_PATH_STATE] = encode_state(new_state)
            state = new_state

        # Choose next op with escape rule
        next_op = choose_next_operator(op, state, transitions, mode, repeat_count)
        frames[t + 1][CH_PATH_OP] = encode_op(next_op)

    return frames
