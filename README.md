# MTFS Geometric Diagnostics for Variational Quantum Eigensolvers

> **A system can look converged in energy while still moving wildly in parameter space.**

This repository implements and validates geometric convergence diagnostics originally developed inside the Multi-Timescale Frozen Search (MTFS) framework, transferred for the first time to molecular VQE.

## The Core Insight

Standard VQE optimizers stop (or declare success) when the energy stops changing:
# MTFS Geometric Diagnostics for Variational Quantum Eigensolvers

|Eₜ − Eₜ₋₁| < ε

But that is not the same as the parameters having settled:

‖Δθₜ‖ → 0    and    orthogonal leakage → 0

We track both. When energy has plateaued **while** a large fraction of the update remains orthogonal to the gradient, we call it **False Convergence**.

## Key Experimental Result

**24 independent trajectories** on a physical 4-qubit Jordan–Wigner H₂ Hamiltonian (STO-3G):

| Metric                        | Value     |
|-------------------------------|-----------|
| Total trajectories            | 24        |
| Optimizers                    | Adam, L-BFGS, SPSA |
| Steps per trajectory          | 50        |
| **False Convergence rate**    | **7 / 24 ≈ 29%** |

In these 7 cases the energy had essentially stopped changing, yet the optimizer continued to take large sideways steps in parameter space — a failure mode completely invisible to energy-only monitoring.

## Why This Matters

- Energy alone is an incomplete convergence criterion.
- Geometric diagnostics (update norm + orthogonal leakage) reveal hidden residual motion.
- The same signature appears across different optimizers.
- This is a direct transfer of an MTFS-derived principle into quantum variational optimization.

## Quick Start

```bash
git clone https://github.com/castanedaricardoh87-prog/MTFS-vqe-geometric-diagnostics-.git
cd mtfs-vqe-geometric-diagnostics
pip install -r requirements.txt

# Reproduce the 24-trajectory proof set
python src/run_cohort.py

# Analyze and detect False Convergence
python src/analyze_cohort.py
