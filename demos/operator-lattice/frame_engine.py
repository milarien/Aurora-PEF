# frame_engine.py

"""
Frame-level planning substrate.

Each Frame = 32 floats.
Pathway band:
- OP_CODE     (which operator is active)
- PATH_POS    (normalized position along the path)
- PATH_STATE  (OPEN / RESOLVED / BLOCKED)
- PATH_BRANCH (parallel branch id)
"""

NUM_CHANNELS = 32

# Data + control slices (reserved for later)
CH_DATA_START    = 0
CH_DATA_END      = 8
CH_CONTROL_START = 8
CH_CONTROL_END   = 16

# Pathway channels (state machine band)
CH_PATH_OP     = 24  # operator id
CH_PATH_POS    = 25  # position [0..1]
CH_PATH_STATE  = 26  # OPEN / RESOLVED / BLOCKED
CH_PATH_BRANCH = 27  # branch id (0 = main)

# Operator set: Aurora-flavoured connectors
OPERATORS = ["WE", "THEN", "BECAUSE", "BUT", "IF"]


# ---- Encoding / decoding helpers ----

def encode_op(name):
    """Map operator name to a normalized float in (0, 1]."""
    if name not in OPERATORS:
        raise ValueError("Unknown operator %r" % name)
    idx = OPERATORS.index(name)
    return float(idx + 1) / float(len(OPERATORS))


def decode_op(val):
    """Inverse of encode_op, with clamping."""
    n = len(OPERATORS)
    idx = int(round(val * n) - 1)
    if idx < 0:
        idx = 0
    if idx >= n:
        idx = n - 1
    return OPERATORS[idx]


def encode_state(name):
    """
    Encode path state as:
      OPEN     -> 0.0
      RESOLVED -> 1.0
      BLOCKED  -> -1.0
    """
    if name == "OPEN":
        return 0.0
    if name == "RESOLVED":
        return 1.0
    if name == "BLOCKED":
        return -1.0
    raise ValueError("Unknown state %r" % name)


def decode_state(val):
    """
    Inverse of encode_state:
      >  0.5  -> RESOLVED
      < -0.5  -> BLOCKED
      else    -> OPEN
    """
    if val > 0.5:
        return "RESOLVED"
    if val < -0.5:
        return "BLOCKED"
    return "OPEN"


def encode_pos(idx, total):
    """Normalize index to [0, 1]."""
    if total <= 1:
        return 0.0
    return float(idx) / float(total - 1)


def decode_pos(val, total):
    if total <= 1:
        return 0
    return int(round(val * (total - 1)))


# ---- Frame / lattice helpers ----

def new_frame():
    """Return a fresh frame (32 floats initialised to 0)."""
    return [0.0 for _ in range(NUM_CHANNELS)]


def set_pathway(frame,
                op=None,
                pos_idx=None,
                total_steps=None,
                state=None,
                branch_id=None):
    """Set pathway-related fields for a single frame (in-place)."""
    if op is not None:
        frame[CH_PATH_OP] = encode_op(op)
    if pos_idx is not None and total_steps is not None:
        frame[CH_PATH_POS] = encode_pos(pos_idx, total_steps)
    if state is not None:
        frame[CH_PATH_STATE] = encode_state(state)
    if branch_id is not None:
        frame[CH_PATH_BRANCH] = float(branch_id) / 100.0


def get_pathway(frame, total_steps):
    """Decode the pathway fields from a frame."""
    return {
        "op": decode_op(frame[CH_PATH_OP]),
        "pos": decode_pos(frame[CH_PATH_POS], total_steps),
        "state": decode_state(frame[CH_PATH_STATE]),
        "branch": int(round(frame[CH_PATH_BRANCH] * 100.0)),
    }


def build_lattice(total_steps=8, branch_id=0):
    """
    Build a 1D lattice (time axis) of frames.

    Initialise:
    - PATH_POS with normalized index
    - PATH_STATE as OPEN
    - PATH_BRANCH as given branch
    """
    lattice = [new_frame() for _ in range(total_steps)]
    for t in range(total_steps):
        set_pathway(
            lattice[t],
            pos_idx=t,
            total_steps=total_steps,
            state="OPEN",
            branch_id=branch_id,
        )
    return lattice
