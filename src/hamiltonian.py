"""Physical 4-qubit H₂ Hamiltonian (Jordan-Wigner, STO-3G approximation)."""
import torch

FCI_ENERGY = -1.137306035753

def get_h2_hamiltonian_matrix() -> torch.Tensor:
    """
    Return a 16×16 real-symmetric matrix approximating 
    the H₂ electronic Hamiltonian at equilibrium geometry.
    """
    H = torch.zeros((16, 16), dtype=torch.float32)

    # Identity / nuclear + core shift
    for i in range(16):
        H[i, i] += -0.0984

    # One-body Z terms
    z_coeffs = {0: 0.1712, 1: 0.1712, 2: -0.2228, 3: -0.2228}
    for state in range(16):
        for q, coeff in z_coeffs.items():
            bit = (state >> q) & 1
            sign = -1.0 if bit else 1.0
            H[state, state] += sign * coeff

    # Two-body ZZ terms
    zz = [
        (0, 1, 0.1686), (0, 2, 0.1205), (1, 3, 0.1205),
        (0, 3, 0.1659), (1, 2, 0.1659), (2, 3, 0.1743)
    ]
    for qA, qB, coeff in zz:
        for state in range(16):
            bitA = (state >> qA) & 1
            bitB = (state >> qB) & 1
            sign = 1.0 if bitA == bitB else -1.0
            H[state, state] += sign * coeff

    # Off-diagonal double-excitation / hopping terms
    hops = [(3, 12, 0.0454), (5, 10, 0.0454), (6, 9, 0.0454)]
    for a, b, coeff in hops:
        H[a, b] += coeff
        H[b, a] += coeff

    return H
