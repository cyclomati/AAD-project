✅ **P vs NP Demonstrator — Final Report**

**Author**: Anmol Sharma  
**Course**: Algorithm Analysis & Design  
**Project**: P vs NP Demonstrator (Solo)

---

## Title Page & Abstract

### Abstract
The P vs NP question asks whether every problem whose solutions are verifiable in
polynomial time can also be solved in polynomial time. Proving or refuting this
statement is out of reach for a course project, so this work instead demonstrates
NP-completeness empirically. I implement three canonical NP-complete problems
from scratch (SAT via DPLL, Subset Sum via brute force and Horowitz–Sahni MITM,
and Vertex Cover via exact branching plus a 2-approximation). I also construct
two classical reductions (3-SAT → Vertex Cover and Subset Sum → SAT) and a bonus
encoding of 4×4 Sudoku into SAT that can be solved by my solver or by MiniSat.
Benchmarking scripts generate random instances, collect runtimes/solution
quality, and produce publication-ready plots that exhibit exponential growth in
the exact algorithms. The experiments show that even tiny increases in input
size can cause the exact solvers to blow up, while MITM and approximation
strategies stabilize performance as theory predicts. The resulting datasets,
reductions, and Sudoku workflow form a self-contained demonstrator of
NP-completeness in practice.

---

## 1. Introduction

### 1.1 Background and Motivation
Class **P** contains problems solvable in polynomial time, whereas **NP**
contains problems whose solutions can be verified in polynomial time. A problem
is NP-complete if (i) it is in NP and (ii) every problem in NP reduces to it in
polynomial time. NP-complete problems appear throughout logistics, security, and
puzzles; their ubiquity means that even modest ability to solve them efficiently
would have enormous economic impact. Because theoretical progress on P vs NP is
unlikely in a semester, the goal is to *show* NP-completeness experimentally by
building solvers, reductions, and reductions-driven applications from scratch.

### 1.2 Objectives
1. Implement exact algorithms for SAT, Subset Sum, and Vertex Cover without
   relying on external SAT/ILP packages.
2. Provide at least one optimized or approximate algorithm per problem (MITM
   for Subset Sum, 2-approximation for Vertex Cover).
3. Construct reductions connecting the problems.
4. Build a benchmarking harness that generates synthetic data, records runtime
   metrics, and produces figures for the report and presentation.
5. Deliver a bonus SAT encoding of Sudoku and compare the in-house solver
   against MiniSat to earn the 5-point bonus.

---

## 2. Algorithm Descriptions

### 2.1 SAT — DPLL with Pruning
* **Algorithm**: Recursive DPLL with unit propagation, pure literal elimination,
  and a depth-first search using the leftmost unassigned variable.
* **Correctness**: Unit propagation and pure literal elimination preserve
  satisfiability (Sipser, 2012). The recursion explores both truth assignments
  for every branch, guaranteeing completeness.
* **Complexity**: Worst-case time remains \(O(2^n)\). Propagation prunes the
  tree substantially in practice, as shown by the node counts logged in
  `data/sat_runtime.csv`. Space usage is linear in the recursion depth.

### 2.2 Subset Sum
1. **Brute Force Enumeration**  
   Enumerates all \(2^n\) masks, accumulates subset sums on the fly, and halts
   once a subset matches the target. Complexity: \(O(2^n)\) time and \(O(1)\)
   auxiliary space.

2. **Meet-in-the-Middle (Horowitz–Sahni)**  
   Splits the array, enumerates \(2^{n/2}\) sums per half, sorts one side, and
   binary-searches complements. Complexity: \(O(2^{n/2} \log 2^{n/2})\) time and
   \(O(2^{n/2})\) space. The implementation stores concrete subsets so the
   solutions can be reconstructed for demo purposes.

### 2.3 Vertex Cover
1. **Exact Branching**  
   Recursively pick an arbitrary edge \((u, v)\) and branch on including each
   endpoint. The recursion depth equals the requested cover size \(k\). Time
   complexity is \(O(2^k)\), which becomes exponential in \(n\) when \(k\) scales
   with the number of vertices.

2. **Greedy 2-Approximation**  
   Iteratively select any uncovered edge and add both endpoints to the cover.
   Proofs guarantee a solution of size \(\le 2 \cdot OPT\). Runtime is
   \(O(n + m)\) because each edge is removed once.

### 2.4 Hamiltonian Path
1. **DFS Backtracking**  
   Depth-first search that grows a path, marking visited vertices and backtracking
   when stuck. Complexity is \(O(n!)\) in the worst case because it can enumerate
   all permutations of vertices. Space is \(O(n)\) for the recursion stack and
   visited set.

2. **Held–Karp Dynamic Programming**  
   Classic subset DP where `dp[mask][j]` tracks whether there is a path covering
   vertex subset `mask` and ending at vertex `j`. Complexity is
   \(O(n^2 2^n)\) time and \(O(n 2^n)\) space; practical only for small \(n\)
   but much faster than naive permutation search on those sizes.

---

## 3. Implementation Details

* **Code structure**: Each solver sits in its own module inside `solvers/`,
  reductions live in `reductions/`, and the benchmarking harness plus plotting
  scripts reside in `bench/`. Shared DIMACS helpers are centralized in
  `utils/dimacs.py`.
* **Design decisions**:
  - SAT uses Python lists for clauses, which keeps clause copying simple while
    enabling list comprehension tricks for filtering literals.
  - Subset Sum MITM records both the sum and the contributing subset to support
    demo-friendly reconstructions even though it costs memory.
  - Vertex Cover graphs use adjacency dictionaries so both algorithms can share
    helper routines such as `add_edge` and `remove_vertex`.
* **Instrumentation**: DPLL returns the number of recursion nodes explored, and
  the benchmarking harness writes that metric alongside runtime to CSV.
* **Challenges**: Exponential algorithms blow up quickly, so the harness clamps
  SAT to 22 variables, Subset Sum to 36 integers, and Vertex Cover to graphs of
  size ≤ 14 nodes to keep runtimes in the <2 s regime for live demos.

---

## 4. Experimental Setup

* **Hardware**: Apple Silicon MacBook Pro (M1 Pro, 32 GB RAM).
* **Software**: Python 3.11 inside a virtual environment, matplotlib 3.8 for
  plotting. No external SAT solvers are used except for the MiniSat comparison
  in the bonus section.
* **Datasets**:
  - SAT: Random 3-CNF instances with clause-to-variable ratio 4.0, generated by
    `bench.run.random_3sat`.
  - Subset Sum: Random positive integers in \([1, 1000]\); the target is the sum
    of the first \(n/3\) values to guarantee satisfiable instances.
  - Vertex Cover: Random simple graphs with roughly \(2n\) edges.
* **Metrics**: Wall-clock runtime, recursion-node counts (SAT), cover size
  returned by exact vs. approximation algorithms, and whether the instance is
  satisfiable.
* **Benchmark harness**: `python -m bench.run` regenerates CSV data; `python -m
  bench.plots` regenerates PNG plots included in the report and slides.

---

## 5. Results & Analysis

### 5.1 SAT (DPLL)
`data/sat_runtime.csv` shows runtimes growing from 0.00012 s at \(n=12\) variables
to 0.00177 s at \(n=22\). More telling is the recursion-node count: only 7 nodes
are explored for \(n=12\), while 45 nodes are needed for \(n=22\). The trend is
roughly exponential despite small absolute times; doubling the variable count
increases nodes between 5× and 7×. This mirrors the theoretical \(O(2^n)\)
complexity and visually produces the sharp bend in `data/plot_sat_runtime.png`.

### 5.2 Subset Sum
The benchmark intentionally picks easy targets, so brute force often halts once
it encounters the planted solution. Nevertheless, the recorded runtimes still
grow from 0.00001 s at \(n=10\) to ≈0.0096 s at \(n=36\). MITM, in contrast,
processes entire halves regardless of target placement and therefore shows a
clean doubling pattern: 0.00005 s at \(n=10\), 0.00474 s at \(n=22\), and 1.27 s
at \(n=36\). Although the constant factors currently favor brute force for these
synthetic, solution-heavy instances, the slope of the MITM curve (visible in
`plot_subsetsum_runtime.png`) is dramatically flatter. This illustrates the
value of algorithmic improvements even when asymptotics remain exponential.

### 5.3 Vertex Cover
Exact branching succeeds for the smallest graphs (e.g., \(n=6\) with \(k=3\) in
0.00003 s) but already fails to find a cover of size \(k=6\) on the \(n=13\)
instance, taking 0.0005 s before exhausting the search tree. The 2-approximation
finishes every run in at most 0.00003 s and returns covers of size at most
twice \(k\) (e.g., 12 vertices when \(n=14, k=7\)). The contrast highlights why
approximation algorithms are essential in practice: they yield predictable
runtimes while communicating how far the solution might be from optimal.

### 5.4 Reductions in Practice
The 3-SAT → Vertex Cover reduction produces graphs with \(2n + 3m\) vertices; the
generated instances were fed back into the exact/approx VC solvers to validate
their correctness. Similarly, Subset Sum instances reduced to SAT via the parity
encoding were solved with the DPLL implementation, closing the reductions loop.
The Subset Sum encoding is parity-correct but does not model carries, so it is a
didactic toy rather than a fully faithful many-one reduction; this limitation is
called out explicitly in the demo and documentation.

### 5.5 Bonus: Sudoku → SAT + MiniSat
`bonus/sudoku_sat.py` encodes 4×4 Sudoku grids into 256-variable CNFs. Running
`python -m bonus.sudoku_sat --puzzle bonus/sample_puzzle.json --dimacs-out
minisat_files/sudoku.cnf` writes the DIMACS file solved both by my DPLL solver
(finishes in <0.01 s) and by MiniSat (also <0.01 s on Apple Silicon). MiniSat’s
model matches the assignment produced by my solver, demonstrating the soundness
of the encoding and providing a real-world puzzle application. The generated
MiniSat output is stored in `minisat_files/sudoku.out` for reference.

### 5.6 Hamiltonian Path
`data/hampath_runtime.csv` logs runtimes for both algorithms on random graphs
with \(n = 6..14\). Held–Karp is slightly faster on the tiny \(n=6\) case
(0.00005 s vs. 0.00017 s) but slows relative to backtracking at \(n=8\) and
especially \(n=12\) (0.01573 s vs. 0.00001 s) because it enumerates every subset.
At \(n=14\) the DP reclaims a lead (0.0293 s vs. 0.06319 s), illustrating how
backtracking performance is highly instance-dependent while DP grows
monotonically with \(2^n\). The plot `data/plot_hampath_runtime.png` captures
this crossover and the shared exponential wall.

---

## 6. Conclusion

This project recreated a miniature NP-completeness toolkit: exact solvers,
optimized/approximate counterparts, reductions, benchmarking scripts, and a
bonus puzzle encoding. The empirical curves reaffirm the theoretical message:
exact algorithms for NP-complete problems scale exponentially, while clever
techniques (propagation, MITM, approximations) stretch the feasible frontier.
Encoding Sudoku into SAT and solving it with both my solver and MiniSat
connects the theory to a familiar real-world problem. Future work could extend
the harness to additional NP-complete problems (Hamiltonian Path, Clique) or
instrument the solvers with profiling hooks to study heuristics more deeply.

---

## 7. Bonus Disclosure

The following components qualify for bonus evaluation:
1. 4×4 Sudoku → SAT encoding with DIMACS export.
2. Solving Sudoku using the in-house DPLL solver.
3. Cross-checking the same CNF with MiniSat and archiving the output.
4. Visualization-ready DIMACS helper scripts for demonstrations.

---

## References

1. Michael Sipser. *Introduction to the Theory of Computation*. Cengage, 3rd
   edition.
2. Michael Garey and David Johnson. *Computers and Intractability: A Guide to
   the Theory of NP-Completeness*. W. H. Freeman, 1979.
3. Martin Davis, Hilary Putnam, George Logemann, and Donald Loveland. “A
   Machine Program for Theorem-Proving.” *Communications of the ACM*, 1962.
4. Donald Knuth. *The Art of Computer Programming, Vol. 4, Fascicle 6*.
5. Course lecture notes, Algorithm Analysis & Design, IIIT Hyderabad.
