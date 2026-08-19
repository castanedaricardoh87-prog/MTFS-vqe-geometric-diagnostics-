"""Optimizer adapters that expose the actual parameter displacement."""
import torch
from torch.optim import Adam, LBFGS

class AdamAdapter:
    def __init__(self, params, lr=0.025):
        self.params = params
        self.opt = Adam([params], lr=lr)

    def step(self, loss_fn):
        self.opt.zero_grad()
        loss = loss_fn()
        loss.backward()
        prev = self.params.detach().clone()
        self.opt.step()
        return self.params.detach() - prev, self.params.grad.detach().clone()


class LBFGSAdapter:
    def __init__(self, params, lr=0.15):
        self.params = params
        self.opt = LBFGS([params], lr=lr, max_iter=1)

    def step(self, closure):
        prev = self.params.detach().clone()
        self.opt.step(closure)
        grad = (self.params.grad.detach().clone()
                if self.params.grad is not None
                else torch.zeros_like(self.params))
        return self.params.detach() - prev, grad


class SPSAAdapter:
    def __init__(self, params, lr=0.04, seed=0):
        self.params = params
        self.lr = lr
        self.t = 0
        self.gen = torch.Generator().manual_seed(seed)

    def step(self, energy_fn):
        self.t += 1
        a_t = self.lr / (self.t + 8) ** 0.602
        c_t = 0.08 / max(self.t, 1) ** 0.101
        pert = torch.randint(0, 2, self.params.shape, generator=self.gen).float() * 2 - 1
        e_plus  = energy_fn(self.params + c_t * pert)
        e_minus = energy_fn(self.params - c_t * pert)
        g_hat = (e_plus - e_minus) / (2.0 * c_t * pert + 1e-12)
        proposed = -a_t * g_hat
        with torch.no_grad():
            self.params.add_(proposed)
        return proposed, g_hat
