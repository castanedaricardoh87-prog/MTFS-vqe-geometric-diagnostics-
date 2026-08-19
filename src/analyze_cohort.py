"""Detect False Convergence using the frozen dual criterion."""
import os
import csv
import glob
from collections import defaultdict

def analyze(target_dir="trajectories"):
    files = glob.glob(os.path.join(target_dir, "*.csv"))
    if not files:
        print("No trajectory files found.")
        return

    anomalies = 0
    regimes = defaultdict(int)
    examples = []

    for path in files:
        with open(path) as f:
            rows = list(csv.DictReader(f))
        if len(rows) < 10:
            continue

        tail = rows[-12:]
        avg_de = sum(abs(float(r["energy_delta"])) for r in tail) / len(tail)
        avg_leak = sum(float(r["orthogonal_fraction"]) for r in tail) / len(tail)
        final_res = float(rows[-1]["residual_to_fci"])
        opt = rows[0]["optimizer"]
        run_id = rows[0]["run_id"]

        energy_flat = avg_de < 1.5e-4
        geometry_moving = avg_leak > 0.28

        if energy_flat and geometry_moving:
            regime = "FALSE_CONVERGENCE"
            anomalies += 1
            examples.append((run_id, opt, final_res, avg_de, avg_leak))
        elif energy_flat:
            regime = "TRUE_SETTLING"
        else:
            regime = "STILL_EVOLVING"
        regimes[regime] += 1

    print("=" * 65)
    print("MTFS-VQE Geometric Diagnostics — Analysis Report")
    print("=" * 65)
    print(f"Total trajectories          : {len(files)}")
    print(f"FALSE CONVERGENCE detected  : {anomalies}")
    print(f"Anomaly rate                : {anomalies / len(files) * 100:.1f}%\n")

    print("Regime distribution:")
    for r, c in sorted(regimes.items(), key=lambda x: -x[1]):
        print(f"  {r:22s} : {c:3d}")

    if examples:
        print("\nExample False Convergence cases:")
        for rid, opt, res, de, leak in examples[:5]:
            print(f"  {rid} | {opt:6s} | residual={res:.4f} | ΔE≈{de:.1e} | leakage={leak:.0%}")

    print("=" * 65)


if __name__ == "__main__":
    analyze()
