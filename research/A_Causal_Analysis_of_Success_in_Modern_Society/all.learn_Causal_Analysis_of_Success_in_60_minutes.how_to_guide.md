---
title: "Causal Analysis of Success in 60 Minutes"
authors:
  - KrishnaKishoreBuddi
  - gpsaggese
date: 2026-02-25
description: >
  Build an agent-based simulation that turns normally-distributed talent into
  power-law outcomes, then use DML and Causal Forests to prove luck is the
  dominant driver. Implements the framework from Saggese (2025).
categories:
  - Causal Inference
  - Agent-Based Modeling
---

TL;DR: If everyone starts roughly equal in ability, why do a handful of people
end up wildly more successful than everyone else? This tutorial builds a
simulation to reproduce that pattern, then uses causal ML to prove that luck —
not talent — is the dominant driver. You can run the whole thing in 60 minutes.

<!-- more -->

## What You'll Build

This tutorial implements the simulation and causal analysis from
[Saggese (2025), *A Causal Analysis of Skill and Luck in Agent Outcomes*](https://github.com/gpsaggese/gpsaggese.github.io/blob/master/papers/Causal_Analysis_of_Agent_Skill_And_Luck/Causal_Analysis_of_Agent_Skill_And_Luck.pdf).
By the end you will have:

- A working agent-based simulation with $N = 100$ agents, talent vectors
  $T_i \in [0,1]^4$, and multiplicative capital evolution
  $C_{i,t+1} = C_{i,t}(1 + \Delta)$ over $T = 80$ periods
- A DML estimate showing each lucky event causes $\approx 12.7\%$ higher final
  capital ($\hat{\tau} = 0.12$), controlling for talent confounders
- CATE estimates from Causal Forests showing IQ moderates treatment effects
  ($\rho = 0.41$)
- A comparison of five resource allocation policies (egalitarian, meritocratic,
  performance-based, random, CATE-optimal)
- (Optional) Bayesian posterior distributions as a robustness check

## What You'll Need

- Docker (recommended) or Python 3.10+ with `pip`
- About 60 minutes of focused time
- No prior knowledge of causal inference required — the notebooks explain
  everything from scratch

To get started:

```bash
cd tutorials/causal_success
./docker_build.sh
./docker_jupyter.sh
```

Then open the notebooks in order: `causal_success.API.ipynb` first (to
understand the building blocks), then `causal_success.example.ipynb` (the full
analysis).

## The Idea in 30 Seconds

Human abilities — intelligence, effort, creativity — cluster around the middle.
But wealth, citations, and company sizes don't. They follow extreme power laws
where a few people hold most of the total.

The paper defines luck formally as $L_A(E) = U_A(E) \cdot S(E|I_A) \cdot (1 -
C_A(E))$, combining utility, surprise (rarity), and lack of control. This
tutorial shows that **multiplicative compounding** is the mechanism that turns
modest luck differences into massive outcome gaps. The simulation demonstrates
this, and the causal analysis confirms it: the variance decomposition yields
$0.08$ (talent) + $0.67$ (luck) + $0.25$ (interaction).

## Background Reading

- Saggese (2025),
  ["A Causal Analysis of Skill and Luck in Agent Outcomes"](https://github.com/gpsaggese/gpsaggese.github.io/blob/master/papers/Causal_Analysis_of_Agent_Skill_And_Luck/Causal_Analysis_of_Agent_Skill_And_Luck.pdf) —
  the theoretical framework this tutorial implements
- Pluchino, Biondo & Rapisarda (2018),
  ["Talent versus Luck"](https://doi.org/10.1142/S0219525918500145) — the paper
  that inspired the simulation design
- Chernozhukov et al. (2018),
  ["Double/Debiased Machine Learning"](https://doi.org/10.1111/ectj.12097) —
  the econometric method behind the DML estimates
- [EconML documentation](https://econml.azurewebsites.net/) — the Microsoft
  library we use for DML and Causal Forests

## What's in the Tutorial

All code, notebooks, and the Docker environment live in
`tutorials/causal_success/`:

- `causal_success_utils.py` — the core library: Agent class, simulation engine,
  Gini and inequality metrics, policy simulation, and Bayesian regression helpers
- `causal_success.API.ipynb` — step-by-step API walkthrough with small,
  self-contained demos of every function
- `causal_success.example.ipynb` — the full analysis from start to finish
- Docker setup (`Dockerfile`, `docker_build.sh`, `docker_jupyter.sh`) for
  one-command reproducibility

## What Happens in `causal_success.example.ipynb`

### Part 1: Building the World and Watching Inequality Emerge

We create $N = 100$ agents with talent vectors $T_i$ drawn from truncated
$\mathcal{N}(0.5, 0.15^2)$ distributions and identical starting capital
$C_{i,0} = 1.0$. Over $T = 80$ periods, random events hit agents with exposure
probability $q_i = \sigma(\alpha(t_i^{(1)} - 0.5))$ and change capital
multiplicatively. Even though everyone starts equal, final capital spans orders
of magnitude. The Gini coefficient reaches $\approx 0.38$, and the top 10% hold
$\approx 28\%$ of total capital.

The punchline: top performers have median talent rank $\approx 52/100$
(average!), but experienced $8.3$ lucky events vs. the population mean of $4.8$.

### Part 2: Proving It Causally and Testing Policies

Correlation isn't enough — talent confounds luck. The paper's causal model
(Section 6.8) specifies: treatment $T_i =$ lucky events, outcome
$Y_i = \log(C_{i,T})$, confounders $X_i = (t_i^{(1)}, t_i^{(2)}, t_i^{(3)})$.
DML yields $\hat{\tau} = 0.12$ ($e^{0.12} \approx 12.7\%$ per event), with
tight confidence intervals. Naive OLS overestimates at $0.156$ due to residual
confounding.

Causal Forests estimate heterogeneous effects: mean CATE $= 0.12$,
$\sigma = 0.03$, with IQ moderating treatment effects ($\rho = 0.41$). The
CATE-optimal allocation policy uses these estimates to target resources:
$R_i \propto \max(0, \hat{\tau}(X_i))$.

Policy comparison (Table 5 in the paper) shows CATE-optimal achieves highest
total welfare ($921$) while performance-based allocation is dominated on both
efficiency and equity — a cautionary finding for institutions that reward past
success without accounting for luck.

## Key Takeaways

**For understanding success:** The variance decomposition ($67\%$ luck,
$8\%$ talent, $25\%$ interaction) quantifies what was previously only intuited.
Among reasonably capable agents, luck is the dominant differentiator.

**For individuals:** Increasing exposure ($t_i^{(1)}$) increases event
encounter rate via the sigmoid mechanism. But outcomes have a large stochastic
component — the paper's luck function formalizes why humility is warranted.

**For policymakers:** CATE-optimal targeting maximizes total welfare.
Performance-based allocation ("back the winners") is dominated on both
dimensions. Egalitarian allocation provides a robust alternative when estimation
is noisy.

**For researchers:** This tutorial demonstrates how agent-based simulation plus
causal inference validates theoretical frameworks with known ground-truth causal
structure (Section 6.10 of the paper).

## What's Next

This tutorial covers the core simulation from Section 6 of the paper. Natural
extensions include talent evolution equations, explicit network graph structures,
calibration to empirical wealth or citation distributions, and multi-period
policy interventions — all discussed in Section 6.11 of the paper.

Now go run the notebooks and see it for yourself.
