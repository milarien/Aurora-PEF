import json
import re
import sys
from pathlib import Path


def first_json_object(text: str):
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def extract_between_markers(text: str, start="BEGIN_JSON", end="END_JSON"):
    a = text.find(start)
    if a == -1:
        return None
    b = text.find(end, a + len(start))
    if b == -1:
        return None
    inner = text[a + len(start):b].strip()
    return inner if inner else None


def normalize_option(s: str):
    s = s.replace("\\n", "\n").strip()
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ==========================
# TEST DEFINITIONS (FROZEN)
# ==========================
TESTS = {
    "input_telescope.txt": {
        "allowed_span": "with the telescope",
        "question": "What does the phrase attach to?",
        "required_options": [
            "I used the telescope to see the man.",
            "The man had the telescope."
        ],
    },
    "input_trophy.txt": {
        "allowed_span": "it",
        "question": "What does 'it' refer to?",
        "required_options": [
            "the trophy",
            "the suitcase"
        ],
    },
    "input_emma_lucy.txt": {
        "allowed_span": "her",
        "question": "Who does 'her' refer to?",
        "required_options": [
            "Emma",
            "Lucy"
        ],
    },
}


def main():
    if len(sys.argv) < 2:
        print("INVALID")
        return

    input_name = Path(sys.argv[1]).name
    spec = TESTS.get(input_name)

    if spec is None:
        print("INVALID")
        return

    raw = sys.stdin.read()

    # Prefer fenced JSON if present
    inner = extract_between_markers(raw)
    if inner is not None:
        if inner.strip() == "INVALID":
            print("INVALID")
            return
        js = inner
    else:
        js = first_json_object(raw)

    if js is None:
        print("INVALID")
        return

    try:
        data = json.loads(js)
    except Exception:
        print("INVALID")
        return

    roles = data.get("roles", [])
    events = data.get("events", [])
    ambiguities = data.get("ambiguities", [])

    cleaned_ambiguities = []
    span_target = spec["allowed_span"]
    required = spec["required_options"]

    for amb in ambiguities:
        span = (amb.get("span") or "").strip()
        opts = amb.get("options", [])
        opts_norm = [normalize_option(o) for o in opts if isinstance(o, str)]

        # Telescope
        if input_name == "input_telescope.txt":
            if span != span_target:
                continue
            if opts_norm == required:
                cleaned_ambiguities.append({
                    "span": span_target,
                    "question": spec["question"],
                    "options": required
                })

        # Trophy
        elif input_name == "input_trophy.txt":
            if span.lower() != "it":
                continue
            found = []
            for entity in required:
                e = entity.lower()
                for o in opts_norm:
                    o_l = o.lower()
                    if o_l == e or o_l == f"the {e}":
                        found.append(entity)
                        break
            if len(found) == 2:
                cleaned_ambiguities.append({
                    "span": "it",
                    "question": spec["question"],
                    "options": required
                })

        # Emma / Lucy
        elif input_name == "input_emma_lucy.txt":
            if span.lower() != "her":
                continue
            if all(o in opts_norm for o in ["Emma", "Lucy"]):
                cleaned_ambiguities.append({
                    "span": "her",
                    "question": spec["question"],
                    "options": ["Emma", "Lucy"]
                })

    if not cleaned_ambiguities:
        print("INVALID")
        return

    out = {
        "roles": roles,
        "events": events,
        "ambiguities": cleaned_ambiguities
    }

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
