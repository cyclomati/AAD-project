# P vs NP Demonstrator — Slide Outline

1. **Title & Motivation (1 slide)**
   - Project title, name, course.
   - One-sentence reminder of P vs NP and why NP-completeness matters.
   - Agenda preview.

2. **Problem Statement & Goals (1 slide)**
   - Bullet goals: implement solvers, construct reductions, build benchmark harness, deliver bonus Sudoku encoding.
   - Diagram showing the three core problems plus arrows for reductions.

3. **SAT Solver Overview (1 slide)**
   - Mini flowchart of DPLL recursion.
   - Key features: unit propagation, pure literal elimination, recursion-node counter.
   - Complexity reminder \(O(2^n)\).

4. **Subset Sum Algorithms (1 slide)**
   - Compare brute force vs. Horowitz–Sahni MITM.
   - Mention reconstruction of subsets and asymptotic improvements.

5. **Vertex Cover Algorithms (1 slide)**
   - Explain exact branching on edges and 2-approximation heuristic.
   - Include diagram of branching tree vs. greedy picks.

6. **Polynomial-Time Reductions (1 slide)**
   - Visual sketch of 3-SAT → Vertex Cover gadget.
   - Outline of Subset Sum → SAT parity encoding.

7. **Experimental Setup (1 slide)**
   - Hardware/software, dataset generation strategy, metrics captured.
   - Screenshot of repo structure or benchmarking pipeline.

8. **Results — SAT (1 slide)**
   - Include `plot_sat_runtime.png`.
   - Discuss runtime curve and recursion-node growth.

9. **Results — Subset Sum (1 slide)**
   - Include `plot_subsetsum_runtime.png`.
   - Explain why MITM slope is flatter even when absolute runtime > brute-force.

10. **Results — Vertex Cover (1 slide)**
    - Include `plot_vertexcover_runtime.png`.
    - Highlight feasibility gap between exact and approximation algorithms.

11. **Bonus: Sudoku → SAT (1 slide)**
    - Show puzzle grid → CNF pipeline.
    - Mention DPLL vs. MiniSat parity check and CLI usage.

12. **Key Takeaways & Lessons (1 slide)**
    - Three bullets: exponential blow-up observed, reductions connect diverse problems, tooling makes NP-completeness tangible.
    - Mention challenges (exponential runtimes, data generation) and mitigations.

13. **Future Work & Q/A (1 slide)**
    - Ideas: add Hamiltonian Path/Clique, more heuristics, richer visualizations.
    - Invite questions.
