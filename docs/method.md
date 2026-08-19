# Method

## Dual Convergence Criterion

We declare true settling only when **both** conditions hold
:
|Eₜ − Eₜ₋₁| < ε_E     ∧     ‖Δθₜ‖ < ε_θ

and, more diagnostically, when the orthogonal fraction of the update is also small.

## Geometric Quantities

For every optimization step we record:

- `u = ‖Δθ‖`                     — update magnitude
- `g = ‖∇E‖`                     — gradient norm
- `d_grad = cos(Δθ, −∇E)`        — alignment with descent direction
- `o = ‖Δθ⊥‖`                    — component orthogonal to −∇E
- `leakage = o / u`              — fraction of motion that is sideways

## False Convergence

A trajectory is labelled **False Convergence** when, in the final window of steps:

- Energy changes are negligible, **yet**
- Leakage remains high.

This is exactly the observational signature isolated inside MTFS and now shown to appear spontaneously in ordinary VQE trajectories.
