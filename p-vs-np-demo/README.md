# P vs NP Demonstrator

Hands-on exploration of NP-completeness through from-scratch implementations of
SAT, Subset Sum, Vertex Cover, and Hamiltonian Path solvers; polynomial-time
reductions; and a bonus Sudoku → SAT encoding.

## Repository Layout

```
bench/            Benchmark + plotting scripts that emit CSV/PNGs in data/
bench/validate.py Empirical reduction checks (3-SAT→VC) + parity mismatch finder
bonus/            Sudoku → SAT encoder + CLI for the bonus component
data/             Generated runtime CSVs and plots
reductions/       3-SAT→VC and Subset Sum→SAT encodings
solvers/          DPLL SAT, Subset Sum, Vertex Cover, and Hamiltonian Path algorithms
minisat_files/    Sample DIMACS and MiniSat output files
presentation/     Slide outline (see report/ for the long-form write-up)
report/           Project report (outline + final draft)
utils/            DIMACS helpers shared across modules
main.py           CLI demo to run solvers/reductions interactively
```

## Environment Setup

Run all commands from the repository root (`p-vs-np-demo`). If you start in the
parent workspace, `cd` into the project first.

```bash
cd p-vs-np-demo          # skip if you are already here
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install matplotlib
```

No third-party SAT libraries are used—only Python stdlib plus matplotlib for
plotting.

## Running the Core Solvers

All solvers live inside the `solvers/` package and can be imported from any
Python session.

```python
from solvers import sat, subsetsum, vertex_cover
from solvers import hampath
from utils import checks

# SAT (clauses are lists of ints; positive=literal, negative=negation)
sat_result, model, nodes = sat.dpll_solve(
    n_vars=4,
    clauses=[[1, 2, -3], [-1, 4, -2], [3, -4, 2]],
)
checks.check_sat([[1, 2, -3], [-1, 4, -2], [3, -4, 2]], model)

# Subset Sum
found, subset = subsetsum.brute_force([3, 7, 9, 10], target=19, validate=True)
found_fast, subset_fast = subsetsum.meet_in_the_middle([3, 7, 9, 10], 19, validate=True)

# Vertex Cover (graph stored as adjacency dict)
graph = {}
vertex_cover.add_edge(graph, 1, 2)
vertex_cover.add_edge(graph, 2, 3)
has_cover, cover_vertices, nodes_vc = vertex_cover.exact_branching(graph, k=2, track_count=True)
greedy_cover = vertex_cover.approx_2(graph)
if has_cover:
    checks.check_vertex_cover(graph, cover_vertices)
checks.check_vertex_cover(graph, greedy_cover)

# Hamiltonian Path (adjacency dict; works on small graphs)
g_hp = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}}
exists_bt, path_bt, nodes_bt = hampath.backtracking_path(g_hp, track_count=True)
exists_dp, path_dp, trans_dp = hampath.held_karp_path(g_hp, track_count=True)
if exists_bt:
    checks.check_hamiltonian_path(g_hp, path_bt)
if exists_dp:
    checks.check_hamiltonian_path(g_hp, path_dp)
```

## Polynomial-Time Reductions

* `reductions/sat_to_vc.py` exposes `reduce_3sat_to_vc(n_vars, clauses)`.
* `reductions/subsetsum_to_sat.py` exposes
  `exactly_equal_sum_parity(nums, target)`, returning `(n_vars, clauses, dimacs)`.

Use them interactively:

```python
from reductions import sat_to_vc, subsetsum_to_sat

g, k = sat_to_vc.reduce_3sat_to_vc(3, [[1, -2, 3], [-1, 2, -3]])
n_vars, clauses, dimacs = subsetsum_to_sat.exactly_equal_sum_parity([3, 5, 7], 10)
```

## Benchmarking & Plots

1. Generate runtime CSVs (ensure your shell is inside `p-vs-np-demo` so the
   `bench` package can be imported):

   ```bash
   python3 -m bench.run
   ```

   This overwrites `data/sat_runtime.csv`, `data/subsetsum_runtime.csv`,
   `data/vertexcover_runtime.csv`, and `data/hampath_runtime.csv`. Each run
   validates solver outputs and logs extra metrics (node/transition counts).

2. Regenerate publication-ready plots:

   ```bash
   python3 -m bench.plots
   ```

   PNGs land in `data/plot_*`, including `plot_hampath_runtime.png`.

## Bonus: Sudoku → SAT (plus MiniSat comparison)

The bonus component lives in `bonus/sudoku_sat.py`, which now doubles as a CLI.

* Solve the default 4×4 puzzle with the in-house DPLL solver:

  ```bash
  python3 -m bonus.sudoku_sat
  ```

* Provide a custom puzzle via JSON (4×4 list of lists) and emit DIMACS for use
  with MiniSat:

  ```bash
  python3 -m bonus.sudoku_sat --puzzle bonus/sample_puzzle.json --dimacs-out minisat_files/sudoku.cnf
  minisat minisat_files/sudoku.cnf minisat_files/sudoku.out   # requires minisat on PATH
  ```

  `minisat_files/sudoku.out` stores the satisfying assignment, which can be fed
  back into `utils.dimacs.parse_dimacs` if needed.

## Validation & Demo CLI

* Reduction sanity checks:

  ```bash
  python3 -m bench.validate
  ```

  Confirms 3-SAT ↔ VC correctness on random small instances and surfaces an
  example where the Subset Sum parity encoding diverges from true satisfiability.

* Interactive demonstrator (random instances + runtime/metric prints):

  ```bash
  python3 main.py --problem sat --vars 12
  python3 main.py --problem subsetsum --n 14
  python3 main.py --problem vertexcover --n 10
  python3 main.py --problem hampath --n 8
  python3 main.py --problem sudoku
  ```

## Reproducing Report Tables & Figures

* Benchmarks + plots → follow the “Benchmarking & Plots” section.
* SAT node counts appear directly in `data/sat_runtime.csv`.
* Subset Sum, Vertex Cover, and Hamiltonian Path runtime + exploration counts
  are read straight from their CSVs.
* The Sudoku DIMACS instance used in the report can be reproduced with the CLI
  commands above (see `minisat_files/` for reference outputs).

## Troubleshooting

* Random instance generation is currently seeded in `bench/run.py` for
  reproducibility. Remove or change `random.seed(0)` if you want varied runs.
* The solvers are exponential by design—expect long runtimes beyond the ranges
  used in `bench.run`.
