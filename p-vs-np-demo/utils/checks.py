"""
Small validation helpers to assert solver outputs are correct.
"""
from typing import Dict, List, Set, Tuple

Graph = Dict[int, Set[int]]

def check_subset_sum(subset: List[int], target: int) -> None:
    """
    Raise AssertionError if the provided subset does not sum to target.
    """
    assert sum(subset) == target, f"Subset sums to {sum(subset)} not target {target}"

def check_vertex_cover(g: Graph, cover: List[int]) -> None:
    """
    Raise AssertionError if any edge is uncovered by the provided cover.
    """
    cover_set = set(cover)
    for u, nbrs in g.items():
        for v in nbrs:
            if u < v and not ({u, v} & cover_set):
                raise AssertionError(f"Edge {(u, v)} not covered by {cover}")

def check_hamiltonian_path(g: Graph, path: List[int]) -> None:
    """
    Raise AssertionError if the path is not a Hamiltonian path of g.
    """
    nodes = set(g.keys())
    assert len(path) == len(nodes), f"Path length {len(path)} != {len(nodes)}"
    assert len(set(path)) == len(path), "Path repeats vertices"
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if v not in g.get(u, set()):
            raise AssertionError(f"No edge between {u} and {v} in path {path}")

def check_sat(clauses: List[List[int]], model: Dict[int, bool]) -> None:
    """
    Raise AssertionError if any clause is unsatisfied under the model.
    """
    for idx, clause in enumerate(clauses):
        ok = False
        for lit in clause:
            val = model.get(abs(lit), False)
            if (lit > 0 and val) or (lit < 0 and not val):
                ok = True
                break
        if not ok:
            raise AssertionError(f"Clause {idx} not satisfied: {clause}")
