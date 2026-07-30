Train an LLM from scratch to propose a formula for a set of data points

Create a generator to create synthetic (random) datasets from expressions from 

  - Math datasets

  Open-WebMath — https://huggingface.co/datasets/open-web-math/open-web-math
  MathPile — https://huggingface.co/datasets/GAIR/MathPile (gated, requires accepting terms) / commercial-use version: https://huggingface.co/datasets/GAIR/MathPile_Commercial
  InfiMM-WebMath-40B — https://huggingface.co/datasets/Infi-MM/InfiMM-WebMath-40B
  MegaMath — https://huggingface.co/datasets/LLM360/MegaMath
  FineMath — https://huggingface.co/datasets/HuggingFaceTB/finemath
  NuminaMath-CoT — https://huggingface.co/datasets/AI-MO/NuminaMath-CoT
  MetaMathQA — https://huggingface.co/datasets/meta-math/MetaMathQA
  MathInstruct — https://huggingface.co/datasets/TIGER-Lab/MathInstruct

  - Physics dataset
  PHYSICS (Zheng et al., 2025) — GitHub repo: https://github.com/Zhengsh123/PHYSICS (paper: https://arxiv.org/abs/2506.00022). The repo has the download links/instructions for the actual data files.

- Create a dataset

- Learn a model using different level of complexity of the formula
  number of data points

- This problem can't really be solved in one shot but requires some sort
  of hill-climbing / search
