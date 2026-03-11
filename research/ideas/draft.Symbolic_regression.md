# Symbolic regression

1) AI Feynman (Max Tegmark's approach)
  -	Install: pip install aifeynman
  -	Note: Docs say it's supported on Linux & macOS (not Windows-native).
2) PySR (very popular, high-performance)
  -	Python interface to a fast backend; widely used in science for interpretable formulas.
  -	Available on PyPI/conda-forge (recent releases continue).
3) gplearn (scikit-learn-style genetic programming)
  -	Classic symbolic regression with SymbolicRegressor, sklearn-like API.
4) PhySO (physics-oriented symbolic regression)
  -	Explicitly aimed at inferring analytical functions from data; strong for
    physics-style problems.
https://arxiv.org/abs/2505.10762
