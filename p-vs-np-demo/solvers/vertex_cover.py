"""
Exact and 2-approximation algorithms for Vertex Cover.
Graph stored as adjacency list: Dict[int, Set[int]].
"""
from typing import Dict, Set, Tuple, List

Graph = Dict[int, Set[int]]

def add_edge(g: Graph, u: int, v: int):
    """
    Insert an undirected edge into the adjacency list graph.

    Args:
        g: Graph adjacency dict.
        u: First endpoint.
        v: Second endpoint.
    """
    g.setdefault(u, set()).add(v)
    g.setdefault(v, set()).add(u)

def any_edge(g: Graph):
    """
    Return an arbitrary edge (u, v) with u < v, or None if graph is edgeless.

    Args:
        g: Graph adjacency dict.
    Returns:
        Tuple (u, v) or None.
    """
    for u, nbrs in g.items():
        for v in nbrs:
            if u < v:
                return (u, v)
    return None

def remove_vertex(g: Graph, u: int) -> Graph:
    """
    Remove vertex u and its incident edges.

    Args:
        g: Graph adjacency dict.
        u: Vertex to delete.
    Returns:
        A shallow copy of g with u removed.
    """
    g2 = {x: set(nbrs) for x, nbrs in g.items()}
    for v in list(g2.get(u, [])):
        g2[v].discard(u)
    g2.pop(u, None)
    return g2

def exact_branching(g: Graph, k: int, track_count: bool = False) -> Tuple[bool, List[int]] | Tuple[bool, List[int], int]:
    """
    Exponential branching algorithm deciding if there is a vertex cover of size ≤ k.

    The recursion aborts immediately once k < 0, so any successful result
    satisfies len(cover) ≤ the original k budget.
    """
    count = 0

    def rec(graph: Graph, remaining: int) -> Tuple[bool, List[int], int]:
        nonlocal count
        count += 1
        if remaining < 0:
            return False, [], count
        e = any_edge(graph)
        if e is None:
            return True, [], count
        u, v = e
        sat, cover, _ = rec(remove_vertex(graph, u), remaining - 1)
        if sat:
            return True, cover + [u], count
        sat, cover, _ = rec(remove_vertex(graph, v), remaining - 1)
        if sat:
            return True, cover + [v], count
        return False, [], count

    sat, cover, count = rec(g, k)
    return (sat, cover, count) if track_count else (sat, cover)

def approx_2(g: Graph) -> List[int]:
    """
    Greedy 2-approximation for vertex cover by picking both endpoints of uncovered edges.

    Args:
        g: Graph adjacency dict.
    Returns:
        List of vertices forming a 2-approximate cover.
    """
    g2 = {x: set(n) for x, n in g.items()}
    cover = []
    while True:
        e = any_edge(g2)
        if e is None:
            break
        u, v = e
        cover += [u, v]
        g2 = remove_vertex(remove_vertex(g2, u), v)
    return cover
