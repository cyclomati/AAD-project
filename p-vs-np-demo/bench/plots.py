"""
Make plots from CSVs in /data. Uses matplotlib only.
Run:
  python -m bench.plots
"""
import csv, os
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..", "data")

def load_csv(path):
    """
    Load a CSV file into a list of dictionaries keyed by column names.

    Args:
        path: Path to the CSV file.
    Returns:
        List of dict rows.
    """
    with open(path) as f:
        return list(csv.DictReader(f))

def plot_sat():
    """
    Plot SAT runtime vs. variable count and save PNG into the data directory.
    """
    rows = load_csv(os.path.join(BASE, "sat_runtime.csv"))
    xs = [int(r["n_vars"]) for r in rows]
    ys = [float(r["time_s"]) for r in rows]
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.xlabel("Variables (n)"); plt.ylabel("Runtime (s)"); plt.title("3-SAT DPLL Runtime vs n")
    plt.savefig(os.path.join(BASE, "plot_sat_runtime.png"), dpi=160)

def plot_subsetsum():
    """
    Plot brute-force vs MITM subset sum runtimes.
    """
    rows = load_csv(os.path.join(BASE, "subsetsum_runtime.csv"))
    xs_b = [int(r["n"]) for r in rows if r["algo"] == "brute"]
    ys_b = [float(r["time_s"]) for r in rows if r["algo"] == "brute"]
    xs_m = [int(r["n"]) for r in rows if r["algo"] == "mitm"]
    ys_m = [float(r["time_s"]) for r in rows if r["algo"] == "mitm"]
    plt.figure()
    plt.plot(xs_b, ys_b, marker="o", label="Brute force")
    plt.plot(xs_m, ys_m, marker="x", label="Meet-in-the-middle")
    plt.xlabel("n"); plt.ylabel("Runtime (s)"); plt.title("Subset Sum: Brute vs MITM")
    plt.legend()
    plt.savefig(os.path.join(BASE, "plot_subsetsum_runtime.png"), dpi=160)

def plot_vertexcover():
    """
    Plot runtime comparison between exact branching and 2-approximation for vertex cover.
    """
    rows = load_csv(os.path.join(BASE, "vertexcover_runtime.csv"))
    xs_e = [int(r["n"]) for r in rows if r["algo"] == "exact"]
    ys_e = [float(r["time_s"]) for r in rows if r["algo"] == "exact"]
    xs_a = [int(r["n"]) for r in rows if r["algo"] == "approx"]
    ys_a = [float(r["time_s"]) for r in rows if r["algo"] == "approx"]
    plt.figure()
    plt.plot(xs_e, ys_e, marker="o", label="Exact")
    plt.plot(xs_a, ys_a, marker="x", label="2-Approx")
    plt.xlabel("n"); plt.ylabel("Runtime (s)"); plt.title("Vertex Cover: Exact vs Approx")
    plt.legend()
    plt.savefig(os.path.join(BASE, "plot_vertexcover_runtime.png"), dpi=160)

def plot_hampath():
    """
    Plot runtime comparison between Hamiltonian Path algorithms.
    """
    rows = load_csv(os.path.join(BASE, "hampath_runtime.csv"))
    xs_bt = [int(r["n"]) for r in rows if r["algo"] == "backtracking"]
    ys_bt = [float(r["time_s"]) for r in rows if r["algo"] == "backtracking"]
    xs_dp = [int(r["n"]) for r in rows if r["algo"] == "held_karp"]
    ys_dp = [float(r["time_s"]) for r in rows if r["algo"] == "held_karp"]
    plt.figure()
    plt.plot(xs_bt, ys_bt, marker="o", label="Backtracking")
    plt.plot(xs_dp, ys_dp, marker="x", label="Held-Karp DP")
    plt.xlabel("n"); plt.ylabel("Runtime (s)"); plt.title("Hamiltonian Path: Backtracking vs DP")
    plt.legend()
    plt.savefig(os.path.join(BASE, "plot_hampath_runtime.png"), dpi=160)

if __name__ == "__main__":
    plot_sat(); plot_subsetsum(); plot_vertexcover(); plot_hampath()
