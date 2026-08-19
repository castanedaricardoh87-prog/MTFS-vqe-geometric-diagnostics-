"""Generate the 24-trajectory honest proof set."""
import os
import csv
import uuid
import torch
from hamiltonian import get_h2_hamiltonian_matrix, FCI_ENERGY
from ansatz import hardware_efficient_ansatz
from geometry import geometric_diagnostics
from optimizers import AdamAdapter, LBFGSAdapter, SPSAAdapter

def run_trajectory(opt_name: str, seed: int, max_steps: int = 50):
    torch.manual_seed(seed)
    H = get_h2_hamiltonian_matrix()
    params = torch.randn(2, 4, 3) * 0.12
    params.requires_grad_(True)

    def energy(p):
        state = hardware_efficient_ansatz(p)
        return torch.dot(state, torch.matmul(H, state))

    if opt_name == "adam":
        adapter = AdamAdapter(params)
        step_fn = lambda: adapter.step(lambda: energy(params))
    elif opt_name == "lbfgs":
        adapter = LBFGSAdapter(params)
        def closure():
            adapter.opt.zero_grad()
            loss = energy(params)
            loss.backward()
            return loss
        step_fn = lambda: adapter.step(closure)
    else:
        adapter = SPSAAdapter(params, seed=seed)
        step_fn = lambda: adapter.step(energy)

    os.makedirs("trajectories", exist_ok=True)
    run_id = str(uuid.uuid4())[:8]
    path = f"trajectories/{run_id}.csv"
    fields = ["run_id", "optimizer", "seed", "step", "energy", "energy_delta",
              "residual_to_fci", "gradient_norm", "update_norm", "orthogonal_fraction"]

    with open(path, "w", newline="") as f:
        csv.DictWriter(f, fieldnames=fields).writeheader()

    prev_e = float("inf")
    for step in range(1, max_steps + 1):
        delta, grad = step_fn()
        e = float(energy(params).detach())
        de = e - prev_e if prev_e != float("inf") else 0.0
        res = abs(e - FCI_ENERGY)
        geo = geometric_diagnostics(delta, grad)

        row = {
            "run_id": run_id, "optimizer": opt_name, "seed": seed, "step": step,
            "energy": e, "energy_delta": de, "residual_to_fci": res,
            "gradient_norm": geo["gradient_norm"],
            "update_norm": geo["update_norm"],
            "orthogonal_fraction": geo["orthogonal_fraction"]
        }
        with open(path, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=fields).writerow(row)
        prev_e = e

    return run_id, res


if __name__ == "__main__":
    print("Generating 24-trajectory proof set (8 seeds × 3 optimizers)...")
    for opt in ["adam", "lbfgs", "spsa"]:
        for seed in range(8):
            rid, res = run_trajectory(opt, seed)
            print(f"  {opt:6s} seed={seed} → residual={res:.5f}  [{rid}.csv]")
    print("\nDone. Trajectories written to ./trajectories/")
