- Create an end-to-end test for notes_to_pdf.py converting this snippet of
  markdown to typst
- Reuse the existing functions in the test
```
* Bayes' Theorem: Recap
- @Definition@: **Bayes' theorem** posits that for model parameters $\theta$ and
  data $X$
  $$
  \red{\Pr(\theta | X)}
  = \frac{\teal{\Pr(X | \theta)} \cdot \blue{\Pr(\theta)}}{\violet{\Pr(X)}}
  $$
  where:
  - $\red{\Pr(\theta | X)}$
    - **Posterior**: probability for parameters $\theta$ after seeing
      data $X$
  - $\teal{\Pr(X | \theta)}$
    - **Likelihood** (aka "statistical model"): plausibility of data
      $X$ given parameters $\theta$
  - $\blue{\Pr(\theta)}$
    - **Prior**: knowledge about parameter $\theta$ before any data
  - $\violet{\Pr(X)}$
    - **Evidence** ("marginal likelihood"): probability of observing data $X$
    - "Marginal" as it averages over all possible parameter values
  - In other words:
    $$
    \red{Posterior}
    = \frac{\teal{Likelihood} \cdot \blue{Prior}}{\violet{Evidence}}
    $$
```

- Check if this is rendered correctly through the pipeline and if not understand
  why

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`
- When writing testing code you must always follow the instructions in
  `.claude/skills/testing.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear
  - You MUST not perform it
  - Ask for clarifications
  - Create a `plan.md` in the same directory with 5 bullet points explaining what
    the plan is
