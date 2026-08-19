# Experimental Summary — 24-Trajectory Proof Set

**Date:** August 2026  
**System:** 4-qubit H₂ (Jordan-Wigner, STO-3G approximation)  
**Ansatz:** 2-layer hardware-efficient  
**Optimizers:** Adam, L-BFGS, SPSA  
**Steps:** 50 per trajectory  
**Seeds:** 0–7 for each optimizer  

## Headline Result

**False Convergence rate = 7 / 24 ≈ 29%**

Definition used (frozen before analysis):

- Average |ΔE| over last 12 steps < 1.5 × 10⁻⁴
- Average orthogonal leakage over last 12 steps > 0.28

These trajectories show energy that has essentially stopped changing while a substantial fraction of the parameter update remains orthogonal to the gradient.

## Interpretation

The geometric diagnostic successfully identifies a non-settling failure mode that pure energy monitoring misses. This is the first controlled demonstration that an MTFS-derived convergence principle transfers to molecular VQE.
