"""Frozen geometric diagnostics (MTFS-derived)."""
import torch

EPS = 1e-12

def geometric_diagnostics(delta: torch.Tensor, grad: torch.Tensor) -> dict:
    """
    Compute update norm, gradient norm, directional alignment,
    orthogonal component and leakage fraction.
    """
    u = torch.linalg.vector_norm(delta)
    descent = -grad

    d_grad = torch.dot(delta.flatten(), descent.flatten()) / (
        torch.linalg.vector_norm(delta) * torch.linalg.vector_norm(descent) + EPS
    )

    g2 = torch.dot(grad.flatten(), grad.flatten())
    parallel = (torch.dot(delta.flatten(), descent.flatten()) / (g2 + EPS)) * descent
    orthogonal = delta - parallel.reshape(delta.shape)
    o = torch.linalg.vector_norm(orthogonal)
    leakage = o / (u + EPS)

    return {
        "update_norm": float(u),
        "gradient_norm": float(torch.linalg.vector_norm(grad)),
        "directional_alignment_grad": float(d_grad),
        "orthogonal_norm": float(o),
        "orthogonal_fraction": float(leakage),
    }
