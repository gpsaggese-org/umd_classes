"""
RL-for-auto-EDA -- prototype, agent version (issue #506).

A real inference-time loop where the AGENT is Claude Code, driven by GP's
`PromptSequencer` (helpers_root/dev_scripts_helpers/ai/cc_lib.py). Instead of
Python pre-computing the answer and the model formatting it, Claude Code is
handed the raw dataset and *writes and runs its own analysis* -- regressions,
independence tests, LiNGAM direction checks -- then emits the discovered DAG.
We score that against the held-out ground truth with the SHD pipeline.

This matches how GP works: `cc_lib` loops Claude Code over a task using its
built-in tools (Bash/Read/Write), rather than registering custom Python tools.

Flow:
  1. Generate a random ground-truth DAG G* and LiNGAM data (Milestone 1).
  2. Write ONLY the data (no ground truth) to <workdir>/data.csv.
  3. PromptSequencer runs Claude Code with Bash/Read/Write allowed, told to do
     EDA and write the inferred DAG to <workdir>/graph.json.
  4. Read graph.json, build B_hat, score vs G* with SHD (Milestone 2).

Run:
  # Real agent (needs claude_agent_sdk + Claude Code auth + helpers on PYTHONPATH):
  python cc_eda_agent.py --seed 0
  # Round-trip test without the SDK (simulates what Claude Code would write):
  python cc_eda_agent.py --seed 0 --simulate

Identifiability note (PR #520): data uses non-Gaussian (LiNGAM) noise so edge
DIRECTION is recoverable; under Gaussian noise only the CPDAG is identifiable.
"""

from __future__ import annotations

import argparse
import asyncio
import itertools
import json
import os
import tempfile

import numpy as np
from sklearn.linear_model import LinearRegression


# ===========================================================================
# Milestone 1 -- synthetic environment (self-contained; no gCastle)
# ===========================================================================
def random_dag(n_nodes: int, n_edges: int, seed: int, w_range=(0.5, 2.0)) -> np.ndarray:
    rng = np.random.default_rng(seed)
    order = rng.permutation(n_nodes)
    possible = [(order[i], order[j]) for i in range(n_nodes) for j in range(i + 1, n_nodes)]
    n_edges = min(n_edges, len(possible))
    W = np.zeros((n_nodes, n_nodes))
    for idx in rng.choice(len(possible), size=n_edges, replace=False):
        i, j = possible[idx]
        W[i, j] = rng.choice([-1.0, 1.0]) * rng.uniform(*w_range)
    return W


def simulate_lingam(W: np.ndarray, n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 1)
    d = W.shape[0]
    parents = {j: set(np.where(W[:, j] != 0)[0]) for j in range(d)}
    order, seen = [], set()
    while len(order) < d:
        for j in range(d):
            if j not in seen and parents[j] <= seen:
                order.append(j); seen.add(j)
    X = np.zeros((n, d))
    for j in order:
        X[:, j] = X @ W[:, j] + (rng.exponential(1.0, size=n) - 1.0)
    return X


class Environment:
    def __init__(self, n_nodes=6, n_edges=6, n_samples=3000, test_frac=0.33, seed=0):
        self.n_nodes, self.seed = n_nodes, seed
        self.W = random_dag(n_nodes, n_edges, seed)
        self.B_true = (self.W != 0).astype(int)
        X = simulate_lingam(self.W, n_samples, seed)
        cut = int(n_samples * (1 - test_frac))
        self.X_train, self.X_test = X[:cut], X[cut:]


# ===========================================================================
# Milestone 2 -- verifiable reward
# ===========================================================================
def shd(B_hat: np.ndarray, B_true: np.ndarray) -> int:
    n = B_true.shape[0]
    return int(sum(
        (B_true[i, j], B_true[j, i]) != (B_hat[i, j], B_hat[j, i])
        for i, j in itertools.combinations(range(n), 2)
    ))


def score(B_hat: np.ndarray, env: Environment) -> dict:
    tp = int(((B_hat == 1) & (env.B_true == 1)).sum())
    fp = int(((B_hat == 1) & (env.B_true == 0)).sum())
    fn = int(((B_hat == 0) & (env.B_true == 1)).sum())
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    fdr = fp / (tp + fp) if (tp + fp) else 0.0
    f1 = (2 * tp) / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0
    r2s = []
    for j in range(env.n_nodes):
        pa = list(np.where(B_hat[:, j] == 1)[0])
        if pa:
            m = LinearRegression().fit(env.X_train[:, pa], env.X_train[:, j])
            r2s.append(max(0.0, m.score(env.X_test[:, pa], env.X_test[:, j])))
    return {"shd": shd(B_hat, env.B_true), "tpr": round(tpr, 3),
            "fdr": round(fdr, 3), "f1": round(f1, 3),
            "oos_r2_mean": round(float(np.mean(r2s)) if r2s else 0.0, 3)}


# ===========================================================================
# Dataset I/O between us and the Claude Code agent
# ===========================================================================
def write_dataset(env: Environment, workdir: str) -> str:
    """Write ONLY the data (no ground truth) plus a tiny spec file."""
    os.makedirs(workdir, exist_ok=True)
    data_path = os.path.join(workdir, "data.csv")
    header = ",".join(f"x{k}" for k in range(env.n_nodes))
    np.savetxt(data_path, env.X_train, delimiter=",", header=header, comments="")
    with open(os.path.join(workdir, "spec.json"), "w") as f:
        json.dump({"n_nodes": env.n_nodes,
                   "columns": [f"x{k}" for k in range(env.n_nodes)]}, f, indent=2)
    return data_path


def read_graph(workdir: str, n_nodes: int) -> np.ndarray:
    """Read graph.json (a list of [parent, child] pairs) into a binary DAG."""
    with open(os.path.join(workdir, "graph.json")) as f:
        edges = json.load(f)
    B = np.zeros((n_nodes, n_nodes), dtype=int)
    for p, c in edges:
        if 0 <= p < n_nodes and 0 <= c < n_nodes and p != c:
            B[p, c] = 1
    return B


# ===========================================================================
# The inference-time loop -- Claude Code as the agent, via GP's PromptSequencer
# ===========================================================================
def build_eda_prompt(workdir: str, n_nodes: int) -> str:
    return (
        f"You are a data scientist doing exploratory data analysis to recover the "
        f"causal DAG that generated a dataset.\n\n"
        f"The data is at {workdir}/data.csv: {n_nodes} numeric columns x0..x{n_nodes-1}, "
        f"one row per sample. It was generated by a linear structural equation model "
        f"with NON-Gaussian (exponential) noise, so edge directions are identifiable "
        f"(a LiNGAM-style setting).\n\n"
        f"Write and run Python (pandas / numpy / scikit-learn / scipy) to:\n"
        f"  1. Inspect the data and compute a correlation matrix.\n"
        f"  2. Recover the skeleton: for each pair, test marginal and conditional "
        f"independence (partial correlation controlling for other variables) to decide "
        f"whether an edge exists.\n"
        f"  3. Orient each edge using the non-Gaussianity: regress each direction and "
        f"check higher-order dependence between the presumed cause and the residual "
        f"(a LiNGAM direction test), not just linear correlation.\n"
        f"  4. Emit the inferred DAG.\n\n"
        f"Write ONLY the result to {workdir}/graph.json as a JSON list of directed "
        f"edges, each [parent_index, child_index] with integer 0-based indices. "
        f"For example: [[2, 0], [3, 2]]. Do not write anything else to that file."
    )


async def run_cc_agent(workdir: str, n_nodes: int, model: str = "") -> None:
    """Drive Claude Code over the EDA task using GP's PromptSequencer."""
    # Imported here so --simulate works even without the SDK installed.
    import dev_scripts_helpers.ai.cc_lib as dshaccli  # GP's wrapper

    seq = dshaccli.PromptSequencer(
        allowed_tools=["Read", "Write", "Bash"],   # Claude Code's built-in tools
        permission_mode="bypassPermissions",        # unattended run
        cwd=workdir,
        model=model,                                  # "" -> SDK default
        context_strategy="session",
        print_output=True,
        max_turns=40,                                 # cap the agent loop
    )
    await seq.execute([build_eda_prompt(workdir, n_nodes)])
    stats = seq.get_chunk_stats()
    if stats:
        s = stats[0]
        print(f"  [agent] turns={s['num_turns']} cost_usd={s['cost_usd']} "
              f"error={s['is_error']}")


def simulate_agent_output(env: Environment, workdir: str) -> None:
    """Stand-in for the SDK path: run the same heuristic the agent should learn
    to run, and write graph.json exactly as Claude Code would. Lets us test the
    write -> read -> score round-trip without a live Claude Code session."""
    X = env.X_train
    n = env.n_nodes
    def corr(i, j): return abs(np.corrcoef(X[:, i], X[:, j])[0, 1])
    def pcorr(i, j, k):
        ri = X[:, i] - LinearRegression().fit(X[:, [k]], X[:, i]).predict(X[:, [k]])
        rj = X[:, j] - LinearRegression().fit(X[:, [k]], X[:, j]).predict(X[:, [k]])
        return abs(np.corrcoef(ri, rj)[0, 1])
    def direction(i, j):
        def dep(c, e):
            r = X[:, e] - LinearRegression().fit(X[:, [c]], X[:, e]).predict(X[:, [c]])
            return abs(np.corrcoef(X[:, c], np.abs(r))[0, 1])
        return 1 if dep(i, j) < dep(j, i) else -1
    edges = []
    for i, j in itertools.combinations(range(n), 2):
        if corr(i, j) >= 0.15 and not any(
            pcorr(i, j, k) < 0.15 for k in range(n) if k not in (i, j)
        ):
            edges.append([i, j] if direction(i, j) >= 0 else [j, i])
    with open(os.path.join(workdir, "graph.json"), "w") as f:
        json.dump(edges, f)


# ===========================================================================
# Main
# ===========================================================================
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-nodes", type=int, default=6)
    ap.add_argument("--model", default="", help="Claude model; '' = SDK default")
    ap.add_argument("--simulate", action="store_true",
                    help="Skip the SDK; simulate Claude Code's output to test the round-trip")
    ap.add_argument("--workdir", default="", help="Where to write data/graph (default: temp dir)")
    args = ap.parse_args()

    env = Environment(n_nodes=args.n_nodes, n_edges=args.n_nodes, seed=args.seed)
    workdir = args.workdir or tempfile.mkdtemp(prefix="cc_eda_")
    write_dataset(env, workdir)
    print(f"Workdir: {workdir}")
    print(f"Ground-truth edges (held out): "
          f"{[list(map(int, e)) for e in zip(*np.where(env.B_true == 1))]}")

    if args.simulate:
        print("Mode: SIMULATE (no Claude Code session; standing in for the agent)")
        simulate_agent_output(env, workdir)
    else:
        print("Mode: REAL (Claude Code via cc_lib.PromptSequencer)")
        try:
            asyncio.run(run_cc_agent(workdir, env.n_nodes, model=args.model))
        except ModuleNotFoundError as e:
            print(f"\n  claude_agent_sdk / helpers not importable ({e}).")
            print("  Run with --simulate to test the pipeline, or set PYTHONPATH")
            print("  to include helpers_root and install claude_agent_sdk.")
            return
        except Exception as e:
            print(f"\n  Agent run failed: {e}")
            return

    graph_path = os.path.join(workdir, "graph.json")
    if not os.path.exists(graph_path):
        print("  No graph.json was produced; nothing to score.")
        return
    B_hat = read_graph(workdir, env.n_nodes)
    print(f"\nDiscovered edges: "
          f"{[list(map(int, e)) for e in zip(*np.where(B_hat == 1))]}")
    print(f"Score vs ground truth: {score(B_hat, env)}")


if __name__ == "__main__":
    main()
