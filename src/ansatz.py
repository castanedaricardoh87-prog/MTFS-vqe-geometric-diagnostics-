"""Hardware-efficient 4-qubit ansatz (pure PyTorch)."""
import torch

def hardware_efficient_ansatz(params: torch.Tensor) -> torch.Tensor:
    """
    params shape: (n_layers, n_qubits=4, 3)
    Returns normalized state vector of length 16.
    Starts from Hartree-Fock |0011⟩ (index 3).
    """
    state = torch.zeros(16, dtype=torch.float32)
    state[3] = 1.0

    n_layers = params.shape[0]
    for layer in range(n_layers):
        # Single-qubit rotations
        for q in range(4):
            alpha = params[layer, q, 0]
            c, s = torch.cos(alpha), torch.sin(alpha)
            for idx in range(16):
                if ((idx >> q) & 1) == 0:
                    pair = idx | (1 << q)
                    v0, v1 = state[idx].clone(), state[pair].clone()
                    state[idx]  = c * v0 - s * v1
                    state[pair] = s * v0 + c * v1

        # Nearest-neighbour CNOTs
        for q in range(3):
            for idx in range(16):
                if ((idx >> q) & 1) == 1 and ((idx >> (q + 1)) & 1) == 0:
                    flipped = idx ^ (1 << (q + 1))
                    state[idx], state[flipped] = state[flipped].clone(), state[idx].clone()

    norm = torch.linalg.vector_norm(state) + 1e-12
    return state / norm
