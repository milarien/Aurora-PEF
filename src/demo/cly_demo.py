"""
Simple CLI demo for Aurora ambiguity handling.

For now this is a placeholder that shows the intended flow:
- load example sentences
- construct 2+ interpretations
- hold them
- prune them (no-op at first)
- print traces
"""

from src.aurora.primitives import Kernel, Interpretation, branch, hold, prune, bind, trace


def run_telescope_demo():
    # Example: "Emma saw her sister with a telescope."
    base = Interpretation(id="base", kernels=[Kernel(id="emma", data="Emma")], notes=[])

    # Two naive branches: instrument vs attribute
    inst = Interpretation(id="instrument", kernels=base.kernels.copy(), notes=base.notes.copy())
    inst = bind(inst, "Attach 'with a telescope' to ACTION (saw)")

    attr = Interpretation(id="attribute", kernels=base.kernels.copy(), notes=base.notes.copy())
    attr = bind(attr, "Attach 'with a telescope' to ENTITY (sister)")

    candidates = branch(base, inst, attr)
    candidates = hold(candidates)
    candidates = prune(candidates)

    for c in candidates:
        print(trace(c))


if __name__ == "__main__":
    run_telescope_demo()
