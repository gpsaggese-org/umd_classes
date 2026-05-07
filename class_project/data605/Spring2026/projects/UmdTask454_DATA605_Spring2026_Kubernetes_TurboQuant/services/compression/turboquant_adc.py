import importlib.util
import math
import site
from pathlib import Path

import numpy as np
import torch


def _load_core():
    for d in site.getsitepackages() + [site.getusersitepackages()]:
        p = Path(d) / "turboquant" / "core.py"
        if p.exists():
            spec = importlib.util.spec_from_file_location("turboquant.core", str(p))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise ImportError("turboquant.core not found. pip install turboquant")


_core = _load_core()
TurboQuantIP = _core.TurboQuantIP


class TurboQuantIndex:
    def __init__(self, dim=512, bits=4, device="cpu", seed=42):
        self.dim = dim
        self.bits = bits
        self.device = device
        self.tq = TurboQuantIP(dim=dim, bits=bits, device=device, seed=seed)
        self.mse_indices = None
        self.norms = None
        self.qjl_signs = None
        self.residual_norms = None
        self.n_vectors = 0

    def add(self, x):
        x = x.to(self.device).float()
        mse_idx, norms, signs, res_norms = self.tq.quantize(x)
        if self.mse_indices is None:
            self.mse_indices = mse_idx
            self.norms = norms
            self.qjl_signs = signs
            self.residual_norms = res_norms
        else:
            self.mse_indices = torch.cat([self.mse_indices, mse_idx], dim=0)
            self.norms = torch.cat([self.norms, norms], dim=0)
            self.qjl_signs = torch.cat([self.qjl_signs, signs], dim=0)
            self.residual_norms = torch.cat([self.residual_norms, res_norms], dim=0)
        self.n_vectors = self.mse_indices.shape[0]

    def search(self, query, k=10, rerank=False, rerank_mult=2, fp32_vectors=None):
        fetch_k = k * rerank_mult if rerank else k
        query = query.to(self.device).float()
        if query.dim() == 1:
            query = query.unsqueeze(0)

        nq = query.shape[0]
        nc = self.tq.num_centroids
        codebook = self.tq.codebook
        q_rot = query @ self.tq.rotation_t

        N = self.n_vectors
        all_scores = torch.zeros(nq, N, device=self.device)

        for qi in range(nq):
            q = q_rot[qi]
            offsets = (torch.arange(N, device=self.device) * nc).unsqueeze(1)
            flat_bins = (self.mse_indices.long() + offsets).reshape(-1)
            flat_weights = q.unsqueeze(0).expand(N, -1).reshape(-1)
            bin_sums = torch.zeros(N * nc, device=self.device)
            bin_sums.scatter_add_(0, flat_bins, flat_weights)
            bin_sums = bin_sums.reshape(N, nc)
            base_dp = (bin_sums * codebook.unsqueeze(0)).sum(dim=1)

            signs_pm = 2.0 * self.qjl_signs.float() - 1.0
            q_proj = self.tq.S @ query[qi]
            error_dp = (signs_pm * q_proj.unsqueeze(0)).sum(dim=1)
            alpha = math.sqrt(math.pi / 2) / self.dim
            error_dp = self.residual_norms.squeeze(1) * alpha * error_dp

            all_scores[qi] = self.norms.squeeze(1) * (base_dp + error_dp)

        topk_scores, topk_ids = torch.topk(all_scores, k=min(fetch_k, N), dim=1)

        if rerank and fp32_vectors is not None:
            fp32_t = torch.from_numpy(fp32_vectors).float()
            out_scores = torch.zeros(nq, k, device=self.device)
            out_ids = torch.zeros(nq, k, dtype=torch.long, device=self.device)
            for qi in range(nq):
                cand = topk_ids[qi]
                exact = query[qi] @ fp32_t[cand].T
                top = torch.topk(exact, k=min(k, len(exact)))
                out_scores[qi] = top.values
                out_ids[qi] = cand[top.indices]
            return out_scores, out_ids

        return topk_scores[:, :k], topk_ids[:, :k]

    def memory_bytes(self):
        mse_bits = self.bits - 1
        index_bytes = self.n_vectors * self.dim * mse_bits / 8
        sign_bytes = self.n_vectors * self.dim / 8
        norm_bytes = self.n_vectors * 4
        res_norm_bytes = self.n_vectors * 4
        total = index_bytes + sign_bytes + norm_bytes + res_norm_bytes
        fp32_bytes = self.n_vectors * self.dim * 4
        return {
            "compressed_bytes": total,
            "compressed_mb": total / (1024 ** 2),
            "fp32_mb": fp32_bytes / (1024 ** 2),
            "compression_ratio": fp32_bytes / total,
        }
