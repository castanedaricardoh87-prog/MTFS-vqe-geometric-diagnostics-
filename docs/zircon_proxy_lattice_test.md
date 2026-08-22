# Solid-State Lattice Test — Zircon Proxy

To test the numerical pipeline beyond the earlier low-dimensional cases, the engine was exercised on a Stage-2 discrete lattice whose anisotropy and dipole parameters were taken from a zircon (ZrSiO₄) proxy.

**Run configuration**
- Lattice: \(N=8\) (expanded), \(K=2\) → 256-dimensional Hilbert space
- Material object: `ZrSiO4_proxy` (Stage-2 parameterized proxy)
- Trajectory length: 32 steps × \(t = 0.25\)

**Observed results**
- Freeze executed successfully (`Froze: True`)
- Extracted coordinate: `[6 13]`
- Confidence: `1.0000` (under the supplied margins)
- Final energy: `10.4065`
- Dipole mean: `0.1022`
- Dipole peak frequency: `0.363636`

The expand → evolve → freeze pipeline completed cleanly and produced consistent spectral output.

> **Scope note**  
> This is a numerical test of the discrete soft-Hamiltonian engine on a parameterized proxy. It does **not** constitute a first-principles, force-field, or crystallographic simulation of real zircon (ZrSiO₄). It is independent of the VQE geometric diagnostics that form the primary focus of this repository.
