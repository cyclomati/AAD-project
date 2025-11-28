"""
Minimal DIMACS CNF utilities.
"""
from typing import List, Tuple

def write_dimacs(n_vars: int, clauses: List[List[int]]) -> str:
    """
    Serialize clauses into DIMACS CNF format.

    Args:
        n_vars: Total number of boolean variables.
        clauses: List of clauses, each a list of integer literals.
    Returns:
        DIMACS-formatted string with header and clauses.
    """
    lines = [f"p cnf {n_vars} {len(clauses)}"]
    for c in clauses:
        lines.append(" ".join(str(l) for l in c) + " 0")
    return "\n".join(lines) + "\n"

def parse_dimacs(text: str) -> Tuple[int, list]:
    """
    Parse DIMACS CNF text back into clauses.

    Args:
        text: Raw DIMACS string.
    Returns:
        Tuple (n_vars, clauses) extracted from the text.
    """
    n_vars, n_clauses = 0, 0
    clauses = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("c"):
            continue
        if s.startswith("p"):
            parts = s.split()
            n_vars = int(parts[2]); n_clauses = int(parts[3])
        else:
            lits = [int(x) for x in s.split() if x != "0"]
            if lits:
                clauses.append(lits)
    return n_vars, clauses
