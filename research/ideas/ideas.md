# Ideas from papers/Research_plan/paper.tex

# Causal Analysis of Financial Tradability

We want to find the optimal trading horizon
There are competing
shorter time horizons -> smaller returns, more predictability
What is the hit rate to achieve a certain value of 


# A Causal Analysis of HF Performance

# Create a tutorial about Sampling

Refs:
https://ermongroup.github.io/cs228-notes/inference/sampling/

# Planning vs execution

Is it better to try things or plan hard?
Bayesian entrepreneurship

# **Misc ML ideas**

### **Can time be a feature of machine learning**

What if the system is changing slowly can you generalize the learning bounds (VC bounds) with a similar mathematical approach of learning theory?

Why does

### **Quasi-stationarity learning**

How to compute the VC dimension when the system and the is changing

Kolmogorov complexity over time

Different types of non stationary systems

* regime shift
* Covariate
* Concept

How much data to use to train when the world is changing
Eg use exponential tau as hyper parameter

### **MDL extensions**

VC dimension including also the research process

VC dimension for a system specified through a causal / Bayesian network

Measure complexity of back testing in terms of VC dimension

Complexity of a model with priors

Shannon entropy

Kolmogorov complexity

Rademacher complexity

### **Fouriered learning**

Apply Fourier transform on inputs and outputs and then learn the coefficients
Exchange learning and Fourier transform

### **Gradient descent as NN**

Can you create a neural network that implements learning”
Create inputs, learn weights as input set
Then learn this relationship

VC ability to predict winners
Hedge funds

### **Closed formulization**

Interpolate formula from casual skill analysis

* then check whether out of sample holds
*
* 👉 **arXiv:1905.11481 — AI Feynman: a Physics-Inspired Method for Symbolic Regression**

# Lean

**Lean**
[https://arxiv.org/pdf/2202.01344](https://arxiv.org/pdf/2202.01344)
[https://projectnumina.ai/](https://projectnumina.ai/)
[https://huggingface.co/blog/AI-MO/kimina-prover](https://huggingface.co/blog/AI-MO/kimina-prover)
[https://chatgpt.com/share/6906bdd6-e4b8-8013-8a77-a7194618d7bb](https://chatgpt.com/share/6906bdd6-e4b8-8013-8a77-a7194618d7bb)
[https://chatgpt.com/share/6906bf0b-b5c0-8013-bdee-26e9d7e75175](https://chatgpt.com/share/6906bf0b-b5c0-8013-bdee-26e9d7e75175)
[https://arxiv.org/abs/2102.11107](https://arxiv.org/abs/2102.11107)
[https://ista.ac.at/en/research/locatello-group/](https://ista.ac.at/en/research/locatello-group/)

**Coding**
Llm and lean
[https://chatgpt.com/share/68e1c12d-5210-8013-a8d2-d198ff3d4a1d](https://chatgpt.com/share/68e1c12d-5210-8013-a8d2-d198ff3d4a1d)

|  |  | Reinforcement learning environment for Lean proofs | [https://leandojo.org](https://leandojo.org/) |
| :---- | :---- | :---- | :---- |
| MiniF2F |  | Math problem benchmark for Lean/LLMs | [https://github.com/openai/miniF2F](https://github.com/openai/miniF2F) |
| Mathlib4 |  | Comprehensive Lean 4 mathematics library | [https://github.com/leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) |
| ProofNet |  | Dataset for neural theorem proving | [https://github.com/openai/proofnet](https://github.com/openai/proofnet) |
| Lean Copilot (Experimental) |  | VSCode extension for LLM-assisted Lean proofs | (Community prototype on GitHub) |

Python-Lean
[https://chatgpt.com/share/68e1c5e6-d3a8-8013-b038-46e2f4082092](https://chatgpt.com/share/68e1c5e6-d3a8-8013-b038-46e2f4082092)
\#
ROI
Product roadmap
\#
Everybody should have 2-3 agents going at very single time
**Outline method** (main points \+ indented subpoints)
	•	**Mind map** (visual, branching ideas)
	•	**Table/chart** (good for comparisons)
**Highlight structure** – Use headings, bullet points, and numbering to show relationships between ideas.
	7\.	**Use symbols and abbreviations** – E.g., “→” for leads to, “↑” for increase, “w/” for with.
	8\.	**Mark confusing points** – Use a star or “?” so you know to ask later.
The **outline method** is a note-taking style where you organize information in a **hierarchical, bullet-point format** — starting with the main topic, then indenting subtopics and details underneath.
[https://chatgpt.com/share/6897526e-5db4-8013-b189-3c7a73c6e6a5](https://chatgpt.com/share/6897526e-5db4-8013-b189-3c7a73c6e6a5)
livestream here: https://youtube.com/live/2Auc57lxgeU
repo here: https://github.com/pymc-labs/ai\_decision\_workshop
Tutorials for class

* over fitting
* Write notes and then do videos
*

Automatically generate images with OpenAI api
Get notification for weather through api
Generate research for understanding relationship btw people and not

* add papers

\> ./dev\_scripts\_umd\_msml610/thin\_client/tmux.py
Traceback (most recent call last):
  File "/Users/saggese/src/umd\_msml6101/./dev\_scripts\_umd\_msml610/thin\_client/tmux.py", line 12, in \<module\>
    assert os.path.exists(os.path.join(dir\_name, "thin\_client\_utils.py")), (
           \~\~\~\~\~\~\~\~\~\~\~\~\~\~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Can't find thin\_client\_utils.py
ln \-sf ../../helpers\_root/dev\_scripts\_helpers/thin\_client/tmux.py ./dev\_scripts\_umd\_msml610/thin\_client/tmux.py
PyCG (Practical Call Graph Generator
flake8-function-order

| pyan3 | Lightweight call graph generator using static parsing |
| :---- | :---- |
| SnakeViz | Works on runtime profiling (not static), gives function timing & hierarchy |
| pycallgraph2 | Creates runtime call graphs (requires code execution) |
| code2flow | Turns structured Python code into flowcharts, but less accurate for dynamic code |

[**pyreverse**](https://pylint.readthedocs.io/en/latest/user_guide/usage/run.html#cmdoption-pyreverse)

| radon | Static analysis for complexity, can complement class structure graphs |
| :---- | :---- |

Pydeps

| Xenon | Enforces complexity thresholds based on Radon | ✅ Built on Radon | CI-friendly enforcement |
| :---- | :---- | :---- | :---- |
| Lizard | Measures cyclomatic complexity for many languages | ✅ Yes | Lightweight & fast |

| Vulture | Finds dead (unused) code | 🚫 Complementary | Prune unused functions/classes |
| :---- | :---- | :---- | :---- |

[https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity](https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity)
[https://www.youtube.com/watch?v=PA7js-mSU3Q](https://www.youtube.com/watch?v=PA7js-mSU3Q)
[https://www.youtube.com/watch?v=LQY3CzUfJgA](https://www.youtube.com/watch?v=LQY3CzUfJgA)
[https://www.wsj.com/articles/amazons-finance-teams-are-relying-more-on-aiand-not-j\[…\]mple-stuff-21313906?st=iCwaCy\&reflink=desktopwebshare\_permalink](https://www.wsj.com/articles/amazons-finance-teams-are-relying-more-on-aiand-not-j%5B%E2%80%A6%5Dmple-stuff-21313906?st=iCwaCy&reflink=desktopwebshare_permalink)
[https://distyl.ai/](https://distyl.ai/)
[https://www.prnewswire.co.uk/news-releases/pecan-ai-launches-demandforecastai-to-fix-th\[…\]ap-with-genai-powered-supply-chain-insights-302540307.html](https://www.prnewswire.co.uk/news-releases/pecan-ai-launches-demandforecastai-to-fix-th%5B%E2%80%A6%5Dap-with-genai-powered-supply-chain-insights-302540307.html)
[https://www.youtube.com/watch?v=Szlz3JE-L5M](https://www.youtube.com/watch?v=Szlz3JE-L5M)
[https://samwitty.github.io/papers/Witty\_Dissertation.pdf](https://samwitty.github.io/papers/Witty_Dissertation.pdf)
AI Assisted Causal Inference, with Sam Witty
[https://www.youtube.com/watch?v=Szlz3JE-L5M](https://www.youtube.com/watch?v=Szlz3JE-L5M)
How to speak
[https://www.youtube.com/watch?v=Unzc731iCUY\&list=PLOe2Tlpw8fRABuFqrQg9tqcCJ0R0\_Eubi](https://www.youtube.com/watch?v=Unzc731iCUY&list=PLOe2Tlpw8fRABuFqrQg9tqcCJ0R0_Eubi)
[https://parabole.ai/](https://parabole.ai/)
[https://www.forbes.com/sites/stevebanker/2024/04/15/what-georgia-pacific-is-doing-with-causal-ai-is-remarkable/](https://www.forbes.com/sites/stevebanker/2024/04/15/what-georgia-pacific-is-doing-with-causal-ai-is-remarkable/)
[https://www.linkedin.com/posts/davewangmia\_i-mapped-81-ai-companies-disrupting-wall-activity-7358518819625000960-578I/](https://www.linkedin.com/posts/davewangmia_i-mapped-81-ai-companies-disrupting-wall-activity-7358518819625000960-578I/)
[https://www.res-group.com/resources/blog/data-as-the-path-to-lower-operating-costs-and-higher-performance/](https://www.res-group.com/resources/blog/data-as-the-path-to-lower-operating-costs-and-higher-performance/)
https://www.evolver.ai/

**Papers**
[https://papers.ssrn.com/sol3/Delivery.cfm/SSRN\_ID4706629\_code2969338.pdf?abstractid=4706629\&mirid=1\&type=2](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4706629_code2969338.pdf?abstractid=4706629&mirid=1&type=2)
[https://m.youtube.com/watch?v=WWCWsub3YkE\&pp=ygUTRnBnYXMgbm90IGdvb2QgZGVlcA%3D%3D](https://m.youtube.com/watch?v=WWCWsub3YkE&pp=ygUTRnBnYXMgbm90IGdvb2QgZGVlcA%3D%3D)
https://m.youtube.com/playlist?list=PLJePd8QU\_LYKZwJnByZ8FHDg5l1rXtcIq

# GP's law

The world GDP is $100T / year
"GP's law": a substantial share (even 90%\!) is wasted in bad business decisions

Businesses make 100s decisions / day
Pricing changes
Hiring / promotions
Capital projects
Product feature priorities
Vendor / partner selection
...

Humans are terrible decision makers
Don't understand probability
Do not use data
Can't think counterfactually
Use heuristics and gut feelings

In a study of 500 managers, 98% failed to apply even basic decision-making best practices \[Larson, E. (2017)\]
\~50% of decisions rely on intuition over data \[BARC Survey (2016)\]
Businesses use only 40-50% of available information \[BARC Survey (2016)\]

# Symbolic regression

1) AI Feynman (Max Tegmark’s approach)
	•	Install: pip install aifeynman
	•	Note: Docs say it’s supported on Linux & macOS (not Windows-native).
2) PySR (very popular, high-performance)
	•	Python interface to a fast backend; widely used in science for interpretable formulas.
	•	Available on PyPI/conda-forge (recent releases continue).
3) gplearn (scikit-learn-style genetic programming)
	•	Classic symbolic regression with SymbolicRegressor, sklearn-like API.
4) PhySO (physics-oriented symbolic regression)
	•	Explicitly aimed at inferring analytical functions from data; strong for physics-style problems.
https://arxiv.org/abs/2505.10762

# VS Code and containers

VS Code developing inside a container
https://code.visualstudio.com/docs/devcontainers/containers
https://code.claude.com/docs/en/devcontainer

# Improve dockerized executables

dockerized executables (hard)
Improve the logic and make it more transparent

