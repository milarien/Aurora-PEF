# main.py

import os
import random

from frame_engine import build_lattice, get_pathway
from transitions import mine_transitions, mine_transitions_from_file
from resolver import run_lattice

CORPUS = """
1. We define the frame.
2. Then we branch possibilities.
3. Because certain facts hold, we reject some branches.
4. But there is a conflicting observation.
5. Then we reconcile the conflict.
6. If reconciliation fails, we restart from a different frame.
"""

CORPUS_FILE = "corpus.txt"


def score_branch(frames):
    """Return counts of OPEN / RESOLVED / BLOCKED."""
    from frame_engine import decode_state

    counts = {"OPEN": 0, "RESOLVED": 0, "BLOCKED": 0}
    for t in range(len(frames)):
        state = decode_state(frames[t][26])  # CH_PATH_STATE = 26
        if state in counts:
            counts[state] += 1
    return counts


def compute_score(counts):
    """
    score = RESOLVED - 2*BLOCKED - OPEN
    """
    resolved = counts.get("RESOLVED", 0)
    blocked = counts.get("BLOCKED", 0)
    open_ = counts.get("OPEN", 0)
    return resolved - 2 * blocked - open_


def get_final_op(frames):
    """Operator of the final frame."""
    info = get_pathway(frames[-1], total_steps=len(frames))
    return info["op"]


def interpret_final_op(op):
    """Human-readable stance."""
    explanations = {
        "WE": "Anchor stance: (re)frame or stabilise before proceeding.",
        "THEN": "Progress stance: continue the line of action or reasoning.",
        "BECAUSE": "Justification stance: prioritise reasons/explanations.",
        "BUT": "Tension stance: flag unresolved conflict/exception.",
        "IF": "Conditional stance: keep possibilities open; defer commitment.",
    }
    return explanations.get(op, "Unknown stance.")


def print_branch(label, frames):
    print("\n=== Branch: %s ===" % label)
    T = len(frames)
    for t, frame in enumerate(frames):
        info = get_pathway(frame, total_steps=T)
        print(
            "t=%d: pos=%d | op=%-8s | state=%-9s | branch=%d"
            % (t, info["pos"], info["op"], info["state"], info["branch"])
        )
    counts = score_branch(frames)
    score = compute_score(counts)
    print("Summary for %s: %s | score = %d" % (label, counts, score))
    return counts, score


def main():
    # ✅ Deterministic runs
    random.seed(0)

    # Load / mine transitions
    if os.path.exists(CORPUS_FILE):
        print("Using external corpus file:", CORPUS_FILE)
        transitions = mine_transitions_from_file(CORPUS_FILE)
    else:
        print("Using inline CORPUS string.")
        transitions = mine_transitions(CORPUS)

    print("\n=== Operator Transitions ===")
    for k, v in transitions.items():
        print("%-8s -> %s" % (k, v))

    total_steps = 8

    # Conservative
    frames_conservative = build_lattice(total_steps=total_steps, branch_id=0)
    frames_conservative = run_lattice(
        frames_conservative, transitions, start_op="WE", mode="conservative"
    )

    # Exploratory
    frames_exploratory = build_lattice(total_steps=total_steps, branch_id=1)
    frames_exploratory = run_lattice(
        frames_exploratory, transitions, start_op="WE", mode="exploratory"
    )

    cons_counts, cons_score = print_branch("Conservative (branch 0)", frames_conservative)
    expl_counts, expl_score = print_branch("Exploratory  (branch 1)", frames_exploratory)

    final_cons_op = get_final_op(frames_conservative)
    final_expl_op = get_final_op(frames_exploratory)

    print("\n=== Branch Comparison ===")
    print("Conservative score:", cons_score, "with counts", cons_counts)
    print("Exploratory  score:", expl_score, "with counts", expl_counts)

    print("\nFinal stances:")
    print("Conservative:", final_cons_op, "-", interpret_final_op(final_cons_op))
    print("Exploratory :", final_expl_op, "-", interpret_final_op(final_expl_op))



    if cons_score > expl_score:
        winner = "Conservative branch (0)"
        winner_op = final_cons_op
    elif expl_score > cons_score:
        winner = "Exploratory branch (1)"
        winner_op = final_expl_op
    else:
        winner = "Tie"
        winner_op = None

    if winner_op is not None:
        print("\nWinner:", winner)
        print("Winning branch final operator:", winner_op)
        print("Interpretation:", interpret_final_op(winner_op))
    else:
        print("\nResult: Tie — branches are equally effective under this corpus.")
        print("Final operators: Conservative=%s, Exploratory=%s" % (final_cons_op, final_expl_op))

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
