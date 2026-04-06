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
simulation to reproduce that pattern, then uses causal ML to prove that luck,
not talent, is the dominant driver. You can run the whole thing in 60 minutes.

<!-- more -->

## What You Will Build

This tutorial implements the simulation and causal analysis from
[Saggese (2025), *A Causal Analysis of Skill and Luck in Agent Outcomes*](https://github.com/gpsaggese/gpsaggese.github.io/blob/master/papers/Causal_Analysis_of_Agent_Skill_And_Luck/Causal_Analysis_of_Agent_Skill_And_Luck.pdf).
By the end you will have a working agent-based simulation with $N = 100$
agents, talent vectors $T_i \in [0,1]^4$, and multiplicative capital evolution
$C_{i,t+1} = C_{i,t}(1 + \Delta)$ running over $T = 200$ periods. You will
produce a DML estimate showing that each lucky event causes roughly $12.7\%$
higher final capital ($\hat{\tau} = 0.12$) after controlling for talent
confounders, along with CATE estimates from Causal Forests that show IQ
moderates the treatment effects ($\rho = 0.41$). Five resource allocation
policies (egalitarian, meritocratic, performance-based, random, CATE-optimal)
are compared side by side, and the notebook optionally closes with Bayesian
posterior distributions as a robustness check.

## What You Will Need

All you really need is Docker (recommended) or Python 3.10+ with `pip`, about
60 minutes of focused time, and no prior causal inference background. The
notebooks explain everything from scratch.

To get started:

```bash
cd research/A_Causal_Analysis_of_Success_in_Modern_Society
./docker_build.sh
./docker_jupyter.sh
```

Then open the notebooks in order. Start with `causal_success.API.ipynb` to
understand the building blocks, and move on to `causal_success.example.ipynb`
for the full analysis.

## The Idea in 30 Seconds

Human abilities, things like intelligence, effort, and creativity, cluster
around the middle. But wealth, citations, and company sizes don't. They follow
extreme power laws where a tiny fraction of people hold most of the total.

The paper defines luck formally as $L_A(E) = U_A(E) \cdot S(E|I_A) \cdot (1 -
C_A(E))$, combining utility, surprise (rarity), and lack of control. This
tutorial shows that **multiplicative compounding** is the mechanism that turns
modest luck differences into massive outcome gaps. The simulation demonstrates
the dynamic, and the causal analysis confirms it. The variance decomposition
comes out to roughly $0.08$ (talent) $+ 0.67$ (luck) $+ 0.25$ (interaction).

## Background Reading

Four sources are worth having open alongside the notebooks. Saggese (2025),
["A Causal Analysis of Skill and Luck in Agent Outcomes"](https://github.com/gpsaggese/gpsaggese.github.io/blob/master/papers/Causal_Analysis_of_Agent_Skill_And_Luck/Causal_Analysis_of_Agent_Skill_And_Luck.pdf),
provides the theoretical framework that this tutorial implements. Pluchino,
Biondo & Rapisarda (2018),
["Talent versus Luck"](https://doi.org/10.1142/S0219525918500145), is the paper
that inspired the original simulation design. Chernozhukov et al. (2018),
["Double/Debiased Machine Learning"](https://doi.org/10.1111/ectj.12097), lays
out the econometric method behind the DML estimates. Finally, the
[EconML documentation](https://econml.azurewebsites.net/) covers the Microsoft
library that powers the DML and Causal Forest fits here.

## What Is In the Tutorial

Everything lives in `research/A_Causal_Analysis_of_Success_in_Modern_Society/`.
The core library is `causal_success_utils.py`, which contains the Agent class,
the simulation engine, Gini and inequality metrics, the policy simulation,
wrappers around DML and Causal Forest fitting, the policy comparison function,
and the Bayesian regression helpers. The walkthrough notebook
`causal_success.API.ipynb` demos each of these pieces in isolation with small,
self-contained examples, while `causal_success.example.ipynb` runs the full
analysis from start to finish. Docker setup (`Dockerfile`, `docker_build.sh`,
`docker_jupyter.sh`) is included for one-command reproducibility.

## What Happens in `causal_success.example.ipynb`

### Part 1: Building the World and Watching Inequality Emerge

We create $N = 100$ agents with talent vectors $T_i$ drawn from truncated
$\mathcal{N}(0.5, 0.15^2)$ distributions and identical starting capital
$C_{i,0} = 1.0$. Over $T = 200$ periods, random events hit agents with exposure
probability $q_i = \sigma(\alpha(t_i^{(1)} - 0.5))$ and change capital
multiplicatively. Even though everyone starts equal, final capital spans orders
of magnitude. The Gini coefficient reaches roughly $0.38$, and the top 10% end
up holding around $28\%$ of total capital.

The punchline is stark. Top performers have a median talent rank of about
$52/100$ (i.e., perfectly average), yet they experienced $8.3$ lucky events
versus the population mean of $4.8$.

### Part 2: Proving It Causally and Testing Policies

Correlation isn't enough on its own, because talent confounds luck. The
paper's causal model (Section 6.8) specifies the treatment as
$T_i =$ lucky events, the outcome as $Y_i = \log(C_{i,T})$, and the
confounders as $X_i = (t_i^{(1)}, t_i^{(2)}, t_i^{(3)})$. DML yields
$\hat{\tau} = 0.12$ ($e^{0.12} \approx 12.7\%$ per event), with tight
confidence intervals. Naive OLS overstates the effect at $0.156$ because
residual confounding isn't removed.

Causal Forests then estimate heterogeneous effects, with mean CATE $= 0.12$
and $\sigma = 0.03$, and IQ moderates the treatment effects at $\rho = 0.41$.
The CATE-optimal allocation policy uses those estimates to target resources
via $R_i \propto \max(0, \hat{\tau}(X_i))$.

The policy comparison (Table 5 in the paper) shows CATE-optimal achieving the
highest total welfare ($921$), while performance-based allocation is dominated
on both efficiency and equity. That's a cautionary finding for institutions
that reward past success without adjusting for luck.

## Key Takeaways

The variance decomposition ($67\%$ luck, $8\%$ talent, $25\%$ interaction)
puts numbers on something that had mostly been intuition. Among reasonably
capable agents, luck is the dominant differentiator of outcomes.

For individuals, increasing exposure ($t_i^{(1)}$) raises the event encounter
rate through the sigmoid mechanism. But outcomes retain a large stochastic
component, which is exactly why the paper's luck formalism suggests some
humility about success.

For policymakers, CATE-optimal targeting maximizes total welfare.
Performance-based allocation, the "back the winners" rule, is dominated on
both dimensions, and egalitarian allocation provides a robust alternative when
estimation is noisy.

For researchers, the tutorial demonstrates how agent-based simulation combined
with causal inference can validate theoretical frameworks against known
ground-truth causal structure (Section 6.10 of the paper).

## What Is Next

This tutorial covers the core simulation from Section 6 of the paper. Natural
extensions include talent evolution equations, explicit network graph
structures, calibration to empirical wealth or citation distributions, and
multi-period policy interventions. All of these are discussed in Section 6.11
of the paper.

Now go run the notebooks and see it for yourself.
