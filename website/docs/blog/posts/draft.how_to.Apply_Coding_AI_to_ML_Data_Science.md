Coding AI applies to ML and data science in several key ways:

1. Accelerating Experimentation
- AI coding assistants (like Claude) speed up iteration cycles
- Data scientists write exploratory code, model training loops, and feature
  engineering faster
- Less boilerplate → more time on the actual ML problem (algorithm choice,
  hyperparameter tuning, feature validation)

2. Catching Common Mistakes
- ML/DS code has high-stakes gotchas (e.g., data leakage, 
  imbalanced class handling)
- AI can spot these patterns and flag them during development.

3. Generating Experimental Code Paths
- ML workflows branch heavily
  - "what if we try PCA?"
  - "what if we use this loss function?"

- AI can rapidly scaffold alternatives without manual boilerplate, letting you
  focus on which direction to take

4. Documentation & Reproducibility
- Codegen helps write clearer experiment logs, parameter tracking, and model card generation
  - Critical for DS work where you need to explain what you tried and why.

5. Bridging Domains
- ML projects mix math, data eng, and software eng. AI can translate between
  idioms:
  - "write the statsmodel formula for this concept,"
  - "convert this PyTorch code to JAX,"
  - "explain this Spark DAG."

- Trade-off:
  - AI-generated code needs validation (especially numerical correctness)
  - You need to always sanity-check model outputs, not just syntactic correctness.
