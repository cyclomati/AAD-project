# P vs NP Demonstrator — Slide Deck

## 1. Title & Motivation
- Anmol Sharma — Algorithm Analysis & Design (Final Project)
- P vs NP reminder: verify in polytime vs. solve in polytime; NP-complete problems capture the frontier.
- Agenda: solvers → reductions → experiments → bonus → takeaways.

## 2. Goals & Scope
- Implement from-scratch solvers: SAT (DPLL), Subset Sum (brute + MITM), Vertex Cover (exact + 2-approx), Hamiltonian Path (backtracking + Held–Karp).
- Provide two polynomial-time reductions: 3-SAT→VC, Subset Sum→SAT.
- Benchmark runtime growth; generate plots/CSVs.
- Bonus: Sudoku→SAT encoding + MiniSat comparison.

## 3. SAT Solver (DPLL)
- Recursion with unit propagation + pure-literal elimination; choose first unassigned var.
- Completeness by exploring both assignments; pruning preserves satisfiability.
- Complexity: worst case \(O(2^n)\); node counter instrumented.

## 4. Subset Sum Algorithms
- Brute force: enumerate \(2^n\) masks; early-exit on target.
- Horowitz–Sahni MITM: split set, precompute \(2^{n/2}\) sums, binary-search complements; reconstruct subsets for demos.
- Complexity: \(O(2^{n/2} \log 2^{n/2})\) time, \(O(2^{n/2})\) space.

## 5. Vertex Cover Algorithms
- Exact branching: pick any edge \((u,v)\); branch on including \(u\) or \(v\); \(O(2^k)\) with depth \(k\).
- 2-approximation: pick uncovered edge, add both endpoints; guarantee \(\le 2 \cdot OPT\); \(O(n+m)\).

## 6. Hamiltonian Path Algorithms
- DFS backtracking: grow path, backtrack on dead-ends; worst-case \(O(n!)\) permutations.
- Held–Karp DP: `dp[mask][j]` stores predecessor; \(O(n^2 2^n)\) time, \(O(n 2^n)\) space; predictable on small \(n\).

## 7. Reductions
- 3-SAT→VC: variable pairs + clause triangles; \(k = n + 2m\); validates VC solvers.
- Subset Sum→SAT: parity/XOR bitwise encoding with fresh vars; DIMACS export for SAT solver.

## 8. Experimental Setup
- Hardware: Apple Silicon MBP (M1 Pro, 32 GB).
- Software: Python 3.11 + matplotlib; no external solver except MiniSat for bonus check.
- Data: random 3-CNF (m=4n), random int arrays, random graphs (~2n edges), random graphs for Hampath (p=0.4).
- Metrics: runtime, SAT node counts, cover sizes, path existence/length.

## 9. Results — SAT
- `data/plot_sat_runtime.png`: runtime vs \(n\); node counts grow roughly 5–7× per +2 vars.
- Exponential curve visible despite small absolute times; pruning helps but doesn’t change asymptotics.

## 10. Results — Subset Sum
- `data/plot_subsetsum_runtime.png`: brute rises slowly due to planted solutions; MITM slope flatter for larger \(n\).
- Takeaway: algorithmic improvement shifts the exponential base; memory trade-off is justified.

## 11. Results — Vertex Cover
- `data/plot_vertexcover_runtime.png`: exact branching blows up as \(n\) grows; 2-approx stays near-zero runtime.
- Approximation returns cover within factor 2 of optimum; practical for live demos.

## 12. Results — Hamiltonian Path
- `data/plot_hampath_runtime.png`: DP predictable \(2^n\) growth; backtracking highly instance-dependent (can be faster with lucky paths).
- At \(n=14\), DP 0.0293 s vs. backtracking 0.06319 s on the sampled graph; crossover captured in plot.

## 13. Bonus: Sudoku→SAT + MiniSat
- 4×4 grid encoding (256 vars); CLI: `python -m bonus.sudoku_sat --dimacs-out minisat_files/sudoku.cnf`.
- Solved by in-house DPLL and MiniSat; outputs match (`minisat_files/sudoku.out`).
- Demonstrates a real-world puzzle reduction.

## 14. Key Takeaways
- Exponential blow-up observed across all exact solvers; heuristics/approximations extend feasible range.
- Reductions let one solver class validate another (SAT↔VC↔Subset Sum, Sudoku).
- Tooling (benchmarks + plots) makes NP-completeness tangible for the live demo.

## 15. Future Work & Q/A
- Add more problems (Clique, TSP variants), richer heuristics (VSIDS-like for SAT), visualization of search trees.
- Open for questions.
