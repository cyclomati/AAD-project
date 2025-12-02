"""
Subset Sum algorithms: brute force and meet-in-the-middle.
"""
from typing import List, Tuple
from bisect import bisect_left

def brute_force(nums: List[int], target: int, track_count: bool = False, validate: bool = False) -> Tuple[bool, list] | Tuple[bool, list, int]:
    """
    Enumerate all subsets and test their sum.

    Args:
        nums: List of integers.
        target: Target sum to realize.
        track_count: If True, also return the number of subsets examined.
        validate: If True, assert the found subset sums to target.
    Returns:
        Tuple (found_solution, subset_values[, explored]).
    """
    n = len(nums)
    explored = 0
    for mask in range(1 << n):
        s = 0; subset = []
        for i in range(n):
            if mask & (1 << i):
                s += nums[i]; subset.append(nums[i])
        explored += 1
        if s == target:
            if validate:
                from utils.checks import check_subset_sum
                check_subset_sum(subset, target)
            return (True, subset, explored) if track_count else (True, subset)
    return (False, [], explored) if track_count else (False, [])

def meet_in_the_middle(nums: List[int], target: int, track_count: bool = False, validate: bool = False) -> Tuple[bool, list] | Tuple[bool, list, int]:
    """
    Horowitz–Sahni meet-in-the-middle search splitting the array into halves.

    Args:
        nums: List of integers.
        target: Desired subset sum.
        track_count: If True, also return the number of combinations considered.
        validate: If True, assert the found subset sums to target.
    Returns:
        Tuple (found_solution, subset_values[, explored]) with subset summing to target.
    """
    n = len(nums)
    A, B = nums[:n//2], nums[n//2:]
    sumsA = []
    for mask in range(1 << len(A)):
        s = 0; subset = []
        for i in range(len(A)):
            if mask & (1 << i):
                s += A[i]; subset.append(A[i])
        sumsA.append((s, subset))
    sumsB = []
    for mask in range(1 << len(B)):
        s = 0; subset = []
        for i in range(len(B)):
            if mask & (1 << i):
                s += B[i]; subset.append(B[i])
        sumsB.append((s, subset))
    sumsB.sort(key=lambda x: x[0])
    Bs = [x[0] for x in sumsB]
    explored = 0
    for sA, subA in sumsA:
        need = target - sA
        i = bisect_left(Bs, need)
        if i < len(Bs) and Bs[i] == need:
            subset = subA + sumsB[i][1]
            if validate:
                from utils.checks import check_subset_sum
                check_subset_sum(subset, target)
            return (True, subset, explored) if track_count else (True, subset)
        explored += 1
    return (False, [], explored) if track_count else (False, [])
