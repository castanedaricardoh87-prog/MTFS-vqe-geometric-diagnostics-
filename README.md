# MTFS Geometric Diagnostics for Variational Quantum Eigensolvers

> **A system can look converged in energy while still moving wildly in parameter space.**

This repository implements and validates geometric convergence diagnostics originally developed inside the Multi-Timescale Frozen Search (MTFS) framework, transferred for the first time to molecular VQE.

## The Core Insight

Standard VQE optimizers stop (or declare success) when the energy stops changing:
# MTFS Geometric Diagnostics for Variational Quantum Eigensolvers

|Eₜ − Eₜ₋₁| < ε

But that is not the same as the parameters having settled:
