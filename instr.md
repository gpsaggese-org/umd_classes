Create a script class_scripts/create_book_toc_from_slides.py --output XYZ.md
--max_level 5

that

1) Read book.From_Data_To_Decisions/book_map.md

2) Parse the title of the chapter and the associated lessons

```
## 1: From Prediction Pipelines to Decision Pipelines

**Lessons**
- msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt
- ...
```

```
# 2: Bayesian Networks

**Lessons**
- msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt
- msml610/lectures_source/Lesson06.2-Using_Bayesian_Networks.txt
```

3) For each lesson call extract_toc_from

extract_toc_from_txt.py -i msml610/lectures_source/Lesson06.1-Bayesian_Networks.txt --max_level 5  --warn_on_malformed

4) Create a single file with all the chapters, lessons and 

```
# Title

## msml610/lectures_source/Lesson08.1-Causal_AI_intro.txt

<TOC>
```

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
