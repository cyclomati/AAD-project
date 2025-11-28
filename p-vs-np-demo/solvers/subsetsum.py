"""
Subset Sum algorithms: brute force and meet-in-the-middle.
"""
from typing import List, Tuple
from bisect import bisect_left

def brute_force(nums: List[int], target: int) -> Tuple[bool, list]:
    """
    Enumerate all subsets and test their sum.

    Args:
        nums: List of integers.
        target: Target sum to realize.
    Returns:
        Tuple (found_solution, subset_values) where subset_values sum to target.
    """
    n = len(nums)
    for mask in range(1 << n):
        s = 0; subset = []
        for i in range(n):
            if mask & (1 << i):
                s += nums[i]; subset.append(nums[i])
        if s == target:
            return True, subset
    return False, []

def meet_in_the_middle(nums: List[int], target: int) -> Tuple[bool, list]:
    """
    Horowitz–Sahni meet-in-the-middle search splitting the array into halves.

    Args:
        nums: List of integers.
        target: Desired subset sum.
    Returns:
        Tuple (found_solution, subset_values) with subset summing to target.
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
    for sA, subA in sumsA:
        need = target - sA
        i = bisect_left(Bs, need)
        if i < len(Bs) and Bs[i] == need:
            return True, subA + sumsB[i][1]
    return False, []
