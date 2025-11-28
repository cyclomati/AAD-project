"""
4x4 Sudoku -> SAT (CNF). Variables v(r,c,d): cell (r,c) has digit d in {1..4}.
DIMACS variable mapping: v = 16*(d-1) + 4*(r-1) + c
"""
import argparse
import json
from typing import Dict, List, Tuple
from utils.dimacs import write_dimacs
from solvers.sat import dpll_solve

def var(r: int, c: int, d: int) -> int:
    """
    Map a (row, column, digit) triple to a DIMACS variable id.

    Args:
        r: Row index in 1..4.
        c: Column index in 1..4.
        d: Digit index in 1..4.
    Returns:
        Integer variable identifier.
    """
    return 16 * (d - 1) + 4 * (r - 1) + c

def _sudoku_clauses(given: List[List[int]]) -> Tuple[int, List[List[int]]]:
    """
    Build the CNF clauses for a 4x4 Sudoku instance.

    Args:
        given: 4x4 grid with digits or 0 for blanks.
    Returns:
        Tuple (n_vars, clauses) describing the CNF.
    """
    clauses = []
    # cell constraints
    for r in range(1, 5):
        for c in range(1, 5):
            clauses.append([var(r, c, d) for d in range(1, 5)])  # at least one
            for d1 in range(1, 5):
                for d2 in range(d1 + 1, 5):
                    clauses.append([-var(r, c, d1), -var(r, c, d2)])  # at most one

    # row & column uniqueness
    for d in range(1, 5):
        for r in range(1, 5):
            clauses.append([var(r, c, d) for c in range(1, 5)])
            for c1 in range(1, 5):
                for c2 in range(c1 + 1, 5):
                    clauses.append([-var(r, c1, d), -var(r, c2, d)])
        for c in range(1, 5):
            clauses.append([var(r, c, d) for r in range(1, 5)])
            for r1 in range(1, 5):
                for r2 in range(r1 + 1, 5):
                    clauses.append([-var(r1, c, d), -var(r2, c, d)])

    # 2x2 subgrid uniqueness
    for d in range(1, 5):
        for br in [1, 3]:
            for bc in [1, 3]:
                cells = [(r, c) for r in range(br, br + 2) for c in range(bc, bc + 2)]
                clauses.append([var(r, c, d) for (r, c) in cells])
                for i in range(len(cells)):
                    for j in range(i + 1, len(cells)):
                        r1, c1 = cells[i]; r2, c2 = cells[j]
                        clauses.append([-var(r1, c1, d), -var(r2, c2, d)])

    # givens
    for r in range(1, 5):
        for c in range(1, 5):
            d = given[r - 1][c - 1]
            if d != 0:
                clauses.append([var(r, c, d)])

    n_vars = 16 * 4
    return n_vars, clauses

def encode_sudoku(given: List[List[int]]) -> str:
    """
    Return a DIMACS string encoding of the Sudoku instance.

    Args:
        given: 4x4 grid.
    Returns:
        DIMACS CNF string.
    """
    n_vars, clauses = _sudoku_clauses(given)
    return write_dimacs(n_vars, clauses)

def solve_sudoku(given: List[List[int]]) -> Tuple[bool, List[List[int]]]:
    """
    Solve the Sudoku instance using the in-house DPLL SAT solver.

    Args:
        given: 4x4 grid with 0 for blanks.
    Returns:
        Tuple (has_solution, solved_grid). Solved grid is 4x4 integers when solvable, else [].
    """
    n_vars, clauses = _sudoku_clauses(given)
    sat, model, _ = dpll_solve(n_vars, clauses)
    if not sat:
        return False, []
    return True, _assignment_to_grid(model)

def _assignment_to_grid(model: Dict[int, bool]) -> List[List[int]]:
    """
    Convert a satisfying assignment into a 4x4 Sudoku grid.

    Args:
        model: Mapping from variable id to boolean value.
    Returns:
        4x4 list of digits.
    """
    grid = [[0 for _ in range(4)] for _ in range(4)]
    for var_id, val in model.items():
        if not val:
            continue
        var_id -= 1
        d = var_id // 16 + 1
        rem = var_id % 16
        r = rem // 4 + 1
        c = rem % 4 + 1
        grid[r - 1][c - 1] = d
    return grid

def write_sudoku_dimacs(given: List[List[int]], path: str) -> str:
    """
    Write the Sudoku CNF to disk for use with MiniSat or other solvers.

    Args:
        given: 4x4 grid.
        path: Output file path.
    Returns:
        Path that was written.
    """
    text = encode_sudoku(given)
    with open(path, "w") as f:
        f.write(text)
    return path

def _load_puzzle(path: str | None) -> List[List[int]]:
    """
    Load a 4x4 puzzle from JSON or return a default demo puzzle.

    Args:
        path: Optional filesystem path to a JSON file.
    Returns:
        4x4 list of ints.
    """
    default = [
        [1, 0, 0, 0],
        [0, 0, 4, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 2],
    ]
    if path is None:
        return default
    with open(path) as f:
        return json.load(f)

def cli():
    """
    Small CLI wrapper so bonus/sudoku_sat.py can encode or solve puzzles from the shell.
    """
    parser = argparse.ArgumentParser(description="Solve or export 4x4 Sudoku via SAT.")
    parser.add_argument("--puzzle", help="Path to JSON file containing a 4x4 list-of-lists puzzle", default=None)
    parser.add_argument("--dimacs-out", help="Optional output path for DIMACS CNF", default=None)
    args = parser.parse_args()

    puzzle = _load_puzzle(args.puzzle)
    if args.dimacs_out:
        path = write_sudoku_dimacs(puzzle, args.dimacs_out)
        print(f"Wrote DIMACS CNF to {path}")
    sat, grid = solve_sudoku(puzzle)
    print("Solved with DPLL?", sat)
    if sat:
        for row in grid:
            print(row)

if __name__ == "__main__":
    cli()
