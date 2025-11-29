"""
Benchmark harness to generate runtime data and plots.
Run:
  python -m bench.run
"""
import time, random, csv, os
from typing import List
from solvers.sat import dpll_solve
from solvers.subsetsum import brute_force, meet_in_the_middle
from solvers.vertex_cover import exact_branching, approx_2, add_edge
from solvers import hampath

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def random_3sat(n_vars: int, n_clauses: int) -> List[List[int]]:
    """
    Sample a random 3-CNF instance.

    Args:
        n_vars: Number of boolean variables.
        n_clauses: Number of clauses (each of size 3).
    Returns:
        List of clauses represented as integer literal triples.
    """
    clauses = []
    for _ in range(n_clauses):
        lits = set()
        while len(lits) < 3:
            v = random.randint(1, n_vars)
            s = random.choice([-1, 1])
            lits.add(s * v)
        clauses.append(list(lits))
    return clauses

def bench_sat():
    """
    Benchmark the DPLL SAT solver over increasing n and write CSV.

    Returns:
        Path to the generated CSV file.
    """
    path = os.path.join(DATA_DIR, "sat_runtime.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n_vars", "n_clauses", "time_s", "nodes", "sat"])
        for n in range(10, 23, 2):
            clauses = random_3sat(n, n * 4)
            t0 = time.time()
            sat, model, nodes = dpll_solve(n, clauses)
            dt = time.time() - t0
            w.writerow([n, n * 4, round(dt, 5), nodes, int(sat)])
    return path

def bench_subsetsum():
    """
    Benchmark brute force vs. meet-in-the-middle subset sum solvers.

    Returns:
        Path to the generated CSV file.
    """
    path = os.path.join(DATA_DIR, "subsetsum_runtime.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "algo", "time_s"])
        for n in range(10, 37, 2):
            nums = [random.randint(1, 1000) for _ in range(n)]
            target = sum(nums[: n // 3])
            t0 = time.time(); brute_force(nums, target); dt = time.time() - t0
            w.writerow([n, "brute", round(dt, 5)])
            t0 = time.time(); meet_in_the_middle(nums, target); dt = time.time() - t0
            w.writerow([n, "mitm", round(dt, 5)])
    return path

def bench_vertex_cover():
    """
    Benchmark exact branching vs. 2-approximation for random graphs.

    Returns:
        Path to the generated CSV file.
    """
    path = os.path.join(DATA_DIR, "vertexcover_runtime.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "m", "k", "algo", "time_s", "cover_size"])
        for n in range(6, 15):
            g = {}
            edges = set()
            while len(edges) < n * 2:
                u = random.randint(1, n); v = random.randint(1, n)
                if u == v: 
                    continue
                e = (min(u, v), max(u, v))
                if e in edges:
                    continue
                edges.add(e)
            for (u, v) in edges:
                add_edge(g, u, v)
            k = n // 2
            t0 = time.time(); sat, cover = exact_branching(g, k); dt = time.time() - t0
            w.writerow([n, len(edges), k, "exact", round(dt, 5), len(cover) if sat else -1])
            t0 = time.time(); cover2 = approx_2(g); dt = time.time() - t0
            w.writerow([n, len(edges), k, "approx", round(dt, 5), len(cover2)])
    return path

def _random_graph(n: int, edge_prob: float = 0.35):
    """
    Generate an undirected graph with edges sampled independently.

    Args:
        n: Number of vertices (labeled 1..n).
        edge_prob: Probability of including each possible edge.
    Returns:
        Graph adjacency dict suitable for the Hamiltonian Path solvers.
    """
    g = {}
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if random.random() < edge_prob:
                add_edge(g, u, v)
    return g

def bench_hampath():
    """
    Benchmark Hamiltonian Path backtracking vs. Held-Karp DP.

    Returns:
        Path to the generated CSV file.
    """
    path = os.path.join(DATA_DIR, "hampath_runtime.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "m", "algo", "time_s", "found", "path_len"])
        for n in range(6, 15, 2):
            g = _random_graph(n, edge_prob=0.4)
            m = sum(len(nbrs) for nbrs in g.values()) // 2
            t0 = time.time(); found_bt, path_bt = hampath.backtracking_path(g); dt = time.time() - t0
            w.writerow([n, m, "backtracking", round(dt, 5), int(found_bt), len(path_bt)])
            t0 = time.time(); found_dp, path_dp = hampath.held_karp_path(g); dt = time.time() - t0
            w.writerow([n, m, "held_karp", round(dt, 5), int(found_dp), len(path_dp)])
    return path

if __name__ == "__main__":
    print("Running SAT bench..."); print(bench_sat())
    print("Running Subset Sum bench..."); print(bench_subsetsum())
    print("Running Vertex Cover bench..."); print(bench_vertex_cover())
    print("Running Hamiltonian Path bench..."); print(bench_hampath())
