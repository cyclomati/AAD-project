"""
Simple DPLL SAT solver with unit propagation and pure literal elimination.
Usage:
    from solvers.sat import dpll_solve
    sat, model, nodes = dpll_solve(n_vars, clauses)
"""
from typing import List, Dict, Tuple

def unit_propagate(clauses: List[List[int]], assignment: Dict[int, bool]) -> Tuple[List[List[int]], Dict[int, bool]]:
    """
    Perform unit-clause propagation.

    Args:
        clauses: List of CNF clauses, each clause is a list of ints representing literals.
        assignment: Current partial assignment mapping variable -> boolean value.
    Returns:
        A tuple of (new_clauses, updated_assignment) after propagation halts or finds conflict.
    """
    changed = True
    while changed:
        changed = False
        unit_literals = []
        for c in clauses:
            if len(c) == 0:
                return clauses, assignment
            if len(c) == 1:
                unit_literals.append(c[0])
        if not unit_literals:
            break
        for lit in unit_literals:
            var = abs(lit); val = (lit > 0)
            if var in assignment and assignment[var] != val:
                return [[]], assignment
            assignment[var] = val
            new_clauses = []
            for c in clauses:
                if lit in c:
                    continue
                if -lit in c:
                    nc = [x for x in c if x != -lit]
                    new_clauses.append(nc)
                else:
                    new_clauses.append(c)
            clauses = new_clauses
            changed = True
    return clauses, assignment

def pure_literal_elim(clauses: List[List[int]], assignment: Dict[int, bool]) -> Tuple[List[List[int]], Dict[int, bool]]:
    """
    Eliminate pure literals that appear with only one polarity.

    Args:
        clauses: CNF clauses.
        assignment: Current assignment map.
    Returns:
        Tuple of (reduced_clauses, updated_assignment) where satisfied clauses are removed.
    """
    lits = set(x for c in clauses for x in c)
    pures = {l for l in lits if -l not in lits}
    if not pures:
        return clauses, assignment
    for lit in pures:
        var = abs(lit); assignment[var] = (lit > 0)
    new_clauses = [c for c in clauses if not any(l in pures for l in c)]
    return new_clauses, assignment

def choose_variable(clauses: List[List[int]], assignment: Dict[int, bool]) -> int:
    """
    Pick the next decision variable.

    Args:
        clauses: Remaining CNF clauses.
        assignment: Current assignment map.
    Returns:
        An integer variable index that is unassigned (0 if none found).
    """
    for c in clauses:
        for lit in c:
            v = abs(lit)
            if v not in assignment:
                return v
    return 0

def dpll(clauses: List[List[int]], assignment: Dict[int, bool]) -> Tuple[bool, Dict[int, bool], int]:
    """
    Run the recursive DPLL search.

    Args:
        clauses: CNF clauses to satisfy.
        assignment: Current variable assignment.
    Returns:
        Tuple (is_satisfiable, final_assignment, explored_nodes).
    """
    clauses, assignment = unit_propagate(clauses, assignment)
    if [] in clauses:
        return False, assignment, 1
    clauses, assignment = pure_literal_elim(clauses, assignment)
    if not clauses:
        return True, assignment, 1
    v = choose_variable(clauses, assignment)
    if v == 0:
        return True, assignment, 1
    count = 1
    for val in (True, False):
        new_assign = dict(assignment); new_assign[v] = val
        new_clauses = []
        lit_true = v if val else -v
        for c in clauses:
            if lit_true in c:
                continue
            if -lit_true in c:
                new_c = [x for x in c if x != -lit_true]
                new_clauses.append(new_c)
            else:
                new_clauses.append(c)
        sat, model, c_added = dpll(new_clauses, new_assign)
        count += c_added
        if sat:
            return True, model, count
    return False, assignment, count

def dpll_solve(n_vars: int, clauses: List[List[int]]):
    """
    Solve a SAT instance using DPLL.

    Args:
        n_vars: Number of boolean variables in the instance (unused but kept for API symmetry).
        clauses: CNF clauses.
    Returns:
        Tuple (is_satisfiable, satisfying_assignment, node_count).
    """
    sat, model, nodes = dpll(clauses, {})
    return sat, model, nodes
