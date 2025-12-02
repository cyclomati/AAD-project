"""
CLI driver to showcase the P vs NP demonstrator.
Run examples:
  python main.py --problem sat --vars 8
  python main.py --problem subsetsum --n 14
  python main.py --problem vertexcover --n 8
  python main.py --problem hampath --n 8
  python main.py --problem sudoku
"""
import argparse, random, time
from bench.run import random_3sat, _random_graph
from solvers.sat import dpll_solve
from solvers.subsetsum import brute_force, meet_in_the_middle
from solvers.vertex_cover import exact_branching, approx_2
from solvers import hampath
from bonus.sudoku_sat import solve_sudoku
from utils.checks import check_subset_sum, check_vertex_cover, check_hamiltonian_path, check_sat

def demo_sat(n_vars: int):
    clauses = random_3sat(n_vars, n_vars * 4)
    t0 = time.time()
    sat, model, nodes = dpll_solve(n_vars, clauses)
    dt = time.time() - t0
    print(f"SAT instance with {n_vars} vars, {len(clauses)} clauses")
    print("Clauses:", clauses)
    print(f"Satisfiable? {sat}, nodes explored={nodes}, time={dt:.5f}s")
    if sat:
        check_sat(clauses, model)

def demo_subsetsum(n: int):
    nums = [random.randint(1, 50) for _ in range(n)]
    target = sum(nums[: n // 3])
    print(f"Subset Sum instance (n={n}, target={target}): {nums}")
    t0 = time.time(); found_b, subset_b, explored_b = brute_force(nums, target, track_count=True, validate=True); dt = time.time() - t0
    print(f"Brute force -> found={found_b}, subset={subset_b}, explored={explored_b}, time={dt:.5f}s")
    if found_b:
        check_subset_sum(subset_b, target)
    t0 = time.time(); found_m, subset_m, explored_m = meet_in_the_middle(nums, target, track_count=True, validate=True); dt = time.time() - t0
    print(f"MITM -> found={found_m}, subset={subset_m}, explored={explored_m}, time={dt:.5f}s")
    if found_m:
        check_subset_sum(subset_m, target)

def demo_vertexcover(n: int):
    g = _random_graph(n, edge_prob=0.35)
    k = n // 2
    m = sum(len(nbrs) for nbrs in g.values()) // 2
    print(f"Vertex Cover instance (n={n}, m={m}, k={k})")
    t0 = time.time(); sat, cover, nodes = exact_branching(g, k, track_count=True); dt = time.time() - t0
    print(f"Exact branching -> sat={sat}, cover={cover}, nodes={nodes}, time={dt:.5f}s")
    if sat:
        check_vertex_cover(g, cover)
    t0 = time.time(); cover2 = approx_2(g); dt = time.time() - t0
    check_vertex_cover(g, cover2)
    print(f"2-approx -> cover_size={len(cover2)}, time={dt:.5f}s")

def demo_hampath(n: int):
    g = _random_graph(n, edge_prob=0.4)
    m = sum(len(nbrs) for nbrs in g.values()) // 2
    print(f"Hamiltonian Path instance (n={n}, m={m})")
    t0 = time.time(); found_bt, path_bt, nodes_bt = hampath.backtracking_path(g, track_count=True); dt = time.time() - t0
    print(f"Backtracking -> found={found_bt}, path={path_bt}, nodes={nodes_bt}, time={dt:.5f}s")
    if found_bt:
        check_hamiltonian_path(g, path_bt)
    t0 = time.time(); found_dp, path_dp, nodes_dp = hampath.held_karp_path(g, track_count=True); dt = time.time() - t0
    print(f"Held-Karp -> found={found_dp}, path={path_dp}, transitions={nodes_dp}, time={dt:.5f}s")
    if found_dp:
        check_hamiltonian_path(g, path_dp)

def demo_sudoku():
    sat, grid = solve_sudoku([
        [1, 0, 0, 0],
        [0, 0, 4, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 2],
    ])
    print("Sudoku solved?", sat)
    for row in grid:
        print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P vs NP demonstrator CLI")
    parser.add_argument("--problem", choices=["sat", "subsetsum", "vertexcover", "hampath", "sudoku"], required=True)
    parser.add_argument("--vars", type=int, default=10, help="Number of variables for SAT")
    parser.add_argument("--n", type=int, default=12, help="Size parameter for Subset Sum, Vertex Cover, Hamiltonian Path")
    args = parser.parse_args()

    if args.problem == "sat":
        demo_sat(args.vars)
    elif args.problem == "subsetsum":
        demo_subsetsum(args.n)
    elif args.problem == "vertexcover":
        demo_vertexcover(args.n)
    elif args.problem == "hampath":
        demo_hampath(args.n)
    elif args.problem == "sudoku":
        demo_sudoku()
