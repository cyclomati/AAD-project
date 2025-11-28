"""
Classic reduction: 3-SAT -> Vertex Cover.
Given CNF with exactly 3 literals per clause, construct a graph and integer k.
Returns (graph adjacency dict, k).
"""
from typing import List, Dict, Set, Tuple
from solvers.vertex_cover import add_edge

def reduce_3sat_to_vc(n_vars: int, clauses: List[List[int]]):
    """
    Build the classic 3-SAT to Vertex Cover reduction graph.

    Args:
        n_vars: Number of boolean variables in the CNF.
        clauses: List of clauses containing integer literals (size ≤ 3).
    Returns:
        Tuple (graph, k) where graph is an adjacency dict and k is the cover size threshold.
    """
    g: Dict[int, Set[int]] = {}
    node_id = 1
    var_node_pos = {}
    var_node_neg = {}

    # Variable pairs (xi, ¬xi) connected by an edge
    for v in range(1, n_vars + 1):
        p, n = node_id, node_id + 1
        var_node_pos[v] = p; var_node_neg[v] = n
        add_edge(g, p, n)
        node_id += 2

    # Clause gadgets: triangles
    clause_nodes = []
    for c in clauses:
        c = (c + [c[-1]] * 3)[:3]  # pad/trim to length 3 for safety
        ids = [node_id, node_id + 1, node_id + 2]
        node_id += 3
        add_edge(g, ids[0], ids[1]); add_edge(g, ids[1], ids[2]); add_edge(g, ids[0], ids[2])
        clause_nodes.append((ids, c))

    # Connect clause literal nodes to the opposite variable node
    for ids, lits in clause_nodes:
        for nid, lit in zip(ids, lits):
            v = abs(lit); is_pos = (lit > 0)
            target = var_node_neg[v] if is_pos else var_node_pos[v]
            add_edge(g, nid, target)

    # k = (#variables) + 2*(#clauses)
    k = n_vars + 2 * len(clauses)
    return g, k
