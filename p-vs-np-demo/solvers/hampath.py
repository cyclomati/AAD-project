"""
Hamiltonian Path algorithms: backtracking search and Held-Karp DP.
Graphs are adjacency dictionaries mapping node -> set of neighbors.
"""
from typing import Dict, Set, List, Tuple, Optional

Graph = Dict[int, Set[int]]

def backtracking_path(g: Graph, track_count: bool = False) -> Tuple[bool, List[int]] | Tuple[bool, List[int], int]:
    """
    Try to find a Hamiltonian path via DFS backtracking.

    Args:
        g: Undirected graph adjacency dict.
    Returns:
        Tuple (exists, path) where path lists vertices in order when found.
    """
    nodes = list(g.keys())
    n = len(nodes)
    if n == 0:
        return True, []

    count = 0

    def dfs(v: int, visited: Set[int], path: List[int]) -> Optional[List[int]]:
        nonlocal count
        count += 1
        """
        Extend a partial Hamiltonian path via DFS.

        Args:
            v: Current vertex.
            visited: Set of vertices already on the path.
            path: Current path prefix.
        Returns:
            Complete path list when all vertices are visited, otherwise None.
        """
        if len(path) == n:
            return path.copy()
        for nbr in g.get(v, []):
            if nbr in visited:
                continue
            visited.add(nbr)
            path.append(nbr)
            res = dfs(nbr, visited, path)
            if res:
                return res
            path.pop()
            visited.remove(nbr)
        return None

    for start in nodes:
        visited = {start}
        res = dfs(start, visited, [start])
        if res:
            return (True, res, count) if track_count else (True, res)
    return (False, [], count) if track_count else (False, [])

def held_karp_path(g: Graph, track_count: bool = False) -> Tuple[bool, List[int]] | Tuple[bool, List[int], int]:
    """
    Held-Karp dynamic programming for Hamiltonian Path on small graphs.

    Args:
        g: Undirected graph adjacency dict.
    Returns:
        Tuple (exists, path) with a Hamiltonian path when one is found.
    """
    nodes = list(g.keys())
    n = len(nodes)
    if n == 0:
        return True, []
    if n == 1:
        return True, [nodes[0]]

    idx = {v: i for i, v in enumerate(nodes)}
    size = 1 << n
    # dp[mask][j] = predecessor index for a path covering mask and ending at j; None = unreachable. 
    dp: List[List[Optional[int]]] = [[None for _ in range(n)] for _ in range(size)]
    transitions = 0

    for i in range(n):
        dp[1 << i][i] = -1  # start at node i

    for mask in range(size):
        for j in range(n):
            if dp[mask][j] is None:
                continue
            vj = nodes[j]
            for nbr in g.get(vj, []):
                k = idx.get(nbr)
                if k is None or (mask & (1 << k)):
                    continue
                new_mask = mask | (1 << k)
                transitions += 1
                if dp[new_mask][k] is None:
                    dp[new_mask][k] = j

    full = (1 << n) - 1
    end = next((j for j in range(n) if dp[full][j] is not None), None)
    if end is None:
        return (False, [], transitions) if track_count else (False, [])

    # Reconstruct path by walking predecessors backward.
    path_idx = []
    cur_mask, cur = full, end
    while cur != -1 and cur is not None:
        path_idx.append(cur)
        prev = dp[cur_mask][cur]
        cur_mask &= ~(1 << cur)
        cur = prev
    path_idx.reverse()
    path = [nodes[i] for i in path_idx]
    return (True, path, transitions) if track_count else (True, path)
