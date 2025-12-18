#!/usr/bin/env python3
"""
PEF Reconstruction Demo — constraints first (definite description + missing info)

Run:
  python pef_dog_demo.py

Demo idea:
  - Two owners may each have a dog.
  - "the dog" requires a unique referent. If not unique -> STOP + clarify.
  - "where is the dog" requires location info. If absent -> STOP + request info.
"""

from dataclasses import dataclass, asdict
import json
import re
from typing import Dict, List, Optional, Tuple


# -------------------------
#   PEF: echo-traces (not a timeline)
# -------------------------

@dataclass
class PEF:
    owners_with_dogs: Dict[str, int]            # e.g. {"jane": 1, "sally": 1}
    last_event_about_dog: Optional[str] = None  # e.g. "ran_away"
    locations: Dict[str, str] = None            # e.g. {"jane_dog": "park"} (rare in this toy)

    def __post_init__(self):
        if self.locations is None:
            self.locations = {}


def ingest(pef: PEF, sentence: str) -> None:
    s = sentence.strip().lower()

    # Ownership: "jane had a dog"
    m = re.match(r"^(\w+)\s+had\s+a\s+dog\.?$", s)
    if m:
        name = m.group(1)
        pef.owners_with_dogs[name] = pef.owners_with_dogs.get(name, 0) + 1
        return

    # Dog event: "the dog ran away"
    if re.match(r"^the\s+dog\s+ran\s+away\.?$", s):
        pef.last_event_about_dog = "ran_away"
        return

    # Location fact (optional extension): "jane's dog is at the park"
    m2 = re.match(r"^(\w+)'s\s+dog\s+is\s+at\s+the\s+(.+?)\.?$", s)
    if m2:
        name = m2.group(1)
        loc = m2.group(2)
        pef.locations[f"{name}_dog"] = loc
        return


# -------------------------
#   Reconstruction helpers
# -------------------------

def candidate_dogs(pef: PEF) -> List[str]:
    # Each owner yields a dog token in this toy model.
    # NOTE: dict iteration preserves insertion order in modern Python, which is fine for a demo.
    return [f"{name}_dog" for name, n in pef.owners_with_dogs.items() for _ in range(n)]


def resolve_definite_description_the_dog(pef: PEF) -> Tuple[str, Optional[str], List[str]]:
    """
    Constraint: 'the dog' must refer to exactly one candidate in scope.
    If not unique -> STOP.
    """
    cands = candidate_dogs(pef)

    if len(cands) == 0:
        return ("stop_no_dog_in_pef", None, cands)

    if len(cands) == 1:
        return ("resolved_unique", cands[0], cands)

    # More than one dog exists -> cannot uniquely resolve "the dog"
    return ("stop_ambiguous_definite_description", None, cands)


def answer_where_is_x(pef: PEF, dog_id: str) -> Tuple[str, Optional[str]]:
    """
    Constraint: A 'where' answer requires an explicit location fact.
    No inference allowed.
    """
    if dog_id in pef.locations:
        return ("answered", pef.locations[dog_id])
    return ("stop_missing_location_fact", None)


# -------------------------
#   Query handler
# -------------------------

def handle_query(pef: PEF, query: str) -> Dict:
    q = query.strip().lower()

    # We only support "where is the dog?" in this toy.
    if not re.match(r"^where\s+is\s+the\s+dog\??$", q):
        return {
            "status": "stop_unsupported_query",
            "explanation": "This demo only supports the query: 'where is the dog?'",
        }

    # Step 1: resolve "the dog"
    ref_status, dog_id, cands = resolve_definite_description_the_dog(pef)

    if ref_status != "resolved_unique":
        # STOP — need clarification before even attempting a 'where' answer

        if ref_status == "stop_ambiguous_definite_description":
            owners = [c.split("_")[0].capitalize() for c in cands]

            if len(owners) == 2:
                clarification = f"Which dog do you mean — {owners[0]}'s dog or {owners[1]}'s dog?"
            else:
                joined = ", ".join(f"{o}'s dog" for o in owners[:-1])
                clarification = f"Which dog do you mean — {joined}, or {owners[-1]}'s dog?"
        else:
            clarification = "Who has the dog you're referring to?"

        return {
            "status": ref_status,
            "explanation": (
                "Definite description 'the dog' is not uniquely resolvable under constraints."
                if ref_status == "stop_ambiguous_definite_description"
                else "No dog exists in PEF, so 'the dog' cannot refer."
            ),
            "candidates": cands,
            "clarification_question": clarification,
        }

    # Step 2: answer where (requires location fact)
    where_status, loc = answer_where_is_x(pef, dog_id)

    if where_status != "answered":
        return {
            "status": where_status,
            "referent": dog_id,
            "explanation": "No location fact exists in PEF for that referent. Constraints forbid guessing.",
            "clarification_question": "Do you know where the dog was last seen, or is there a location clue?",
        }

    return {
        "status": "answered",
        "referent": dog_id,
        "answer": loc,
    }


# -------------------------
#   CLI
# -------------------------

def main():
    print("\nPEF Reconstruction Demo — constraints first")
    print("Enter context lines (blank line to end), then enter the query line.\n")

    pef = PEF(owners_with_dogs={})

    context_lines: List[str] = []
    while True:
        line = input("context> ").rstrip("\n")
        if line.strip() == "":
            break
        context_lines.append(line)
        ingest(pef, line)

    query = input("query  > ").rstrip("\n")

    result = handle_query(pef, query)

    print("\n--- TRACE (JSON) ---")
    print(
        json.dumps(
            {
                "pef": asdict(pef),
                "context": context_lines,
                "query": query,
                "result": result,
            },
            indent=2,
            ensure_ascii=True,
        )
    )
    print()


if __name__ == "__main__":
    main()
