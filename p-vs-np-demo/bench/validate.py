"""
Empirical validation helpers for reductions.
Run:
  python -m bench.validate
"""
import random
from itertools import combinations, product
from solvers.sat import dpll_solve
from solvers.vertex_cover import exact_branching
from solvers.subsetsum import brute_force
from reductions import sat_to_vc, subsetsum_to_sat
from bench.run import random_3sat
from utils.checks import check_vertex_cover, check_sat

random.seed(1)

def validate_sat_to_vc(trials: int = 5, n_vars: int = 4, n_clauses: int = 6):
    """
    Randomly sample 3-SAT instances and check SAT ↔ VC cover existence.
    """
    mismatches = 0
    attempts = 0
    while attempts < trials:
        clauses = random_3sat(n_vars, n_clauses)
        sat_res, model, _ = dpll_solve(n_vars, clauses)
        g, k = sat_to_vc.reduce_3sat_to_vc(n_vars, clauses)
        # Skip pathological instances that would force enormous branching
        if k > 20:
            continue
        vc_sat, cover, _ = exact_branching(g, k, track_count=True)
        if vc_sat:
            check_vertex_cover(g, cover)
        if sat_res != vc_sat:
            mismatches += 1
        attempts += 1
    return mismatches

def find_parity_mismatch(max_n: int = 4, max_val: int = 6):
    """
    Search small Subset Sum instances for a parity encoding mismatch.

    Returns:
        Example tuple (nums, target, actual_sat, parity_sat) where they differ, or None.
    """
    for n in range(1, max_n + 1):
        for nums in product(range(1, max_val + 1), repeat=n):
            nums = list(nums)
            total = sum(nums)
            for target in range(total + 1):
                actual_sat, _, _ = brute_force(nums, target, track_count=True)
                n_vars, clauses, _ = subsetsum_to_sat.exactly_equal_sum_parity(nums, target)
                parity_sat, model, _ = dpll_solve(n_vars, clauses)
                if actual_sat != parity_sat:
                    # Validate model when SAT to avoid false positives
                    if parity_sat:
                        check_sat(clauses, model)
                    return nums, target, actual_sat, parity_sat
    return None

if __name__ == "__main__":
    mismatches = validate_sat_to_vc()
    print(f"3-SAT -> VC mismatches over samples: {mismatches}")
    example = find_parity_mismatch()
    if example:
        nums, target, actual, parity = example
        print(f"Found parity mismatch for nums={nums}, target={target}: actual={actual}, parity={parity}")
    else:
        print("No parity mismatch found in searched range.")
