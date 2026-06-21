Modify class_scripts/create_book_toc_from_slides.py 

1) Parse 

```
### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
```

instead of

```
**Lessons**
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
```

2) Add an option --in_place that after

```
### Lessons
- `msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt`
```

adds the TOC in the format below

```
### Current TOC

// msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt

- Logic-Based AI Under Uncertainty (10)
  - Problem (3)
  - Solution (7)
- Probabilistic Reasoning (18)
  - Conditional Independence (5)
  - Bayesian Networks (13)

// msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt

- Semantics of Bayesian Networks (8)
- Constructing a Bayesian Network (34)
- Exact Inference in Bayesian Networks (4)
- Approximate Inference in Bayesian Networks (28)
```

3) Update the related README

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is
