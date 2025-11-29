"""
Demo encoding: Subset Sum -> SAT for small instances.
We encode selection bits b_i and constrain sum == T using parity-style constraints.
This is a minimal didactic encoding suitable for tiny demos, not industrial scale.
"""
from typing import List, Tuple
from utils.dimacs import write_dimacs

def _new_var(counter): 
    """
    Increment the shared counter and return a fresh DIMACS variable id.

    Args:
        counter: Single-element list storing the last issued variable id.
    Returns:
        Integer variable identifier.
    """
    counter[0] += 1
    return counter[0]

def exactly_equal_sum_parity(nums: List[int], target: int) -> Tuple[int, list, str]:
    """
    Encode Subset Sum as a parity-based SAT instance.

    Args:
        nums: Sequence of positive integers.
        target: Desired subset sum.
    Returns:
        Tuple (n_vars, clauses, dimacs_text) describing the CNF encoding.
    """
    width = max(target.bit_length(), max((x.bit_length() for x in nums), default=1)) + 1
    counter = [0]
    b = [_new_var(counter) for _ in nums]
    S = [_new_var(counter) for _ in range(width)]  # "sum bits"

    clauses = []

    def xor2(a, b, out):
        """
        Encode a 2-input XOR gate into CNF.

        Args:
            a: Variable id for the first input.
            b: Variable id for the second input.
            out: Variable id that should equal a ⊕ b.
        Returns:
            None; clauses are appended in-place to the surrounding `clauses` list.
        """
        clauses.extend([[-a, -b, -out], [a, b, -out], [a, -b, out], [-a, b, out]])

    for k in range(width):
        contributors = []
        for i, x in enumerate(nums):
            if (x >> k) & 1:
                contributors.append(b[i])
        if not contributors:
            # Force S[k] to target bit
            clauses.append([S[k]] if ((target >> k) & 1) else [-S[k]])
        else:
            cur = contributors[0]
            for j in contributors[1:]:
                t = _new_var(counter)
                xor2(cur, j, t)
                cur = t
            const = _new_var(counter)
            clauses.append([const] if ((target >> k) & 1) else [-const])
            xor2(cur, const, S[k])

    n_vars = max(counter[0], max(b + S))
    dimacs = write_dimacs(n_vars, clauses)
    return n_vars, clauses, dimacs
