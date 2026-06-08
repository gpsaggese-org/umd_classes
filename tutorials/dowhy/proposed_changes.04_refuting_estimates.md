# Proposed changes: `dowhy.04_refuting_estimates`

- Reviewed against `.claude/skills/notebook.rules.md`,
  `.claude/skills/notebook.create_outline/SKILL.md`,
  `.claude/skills/notebook.implement_outline/SKILL.md`
- Files affected: `dowhy.04_refuting_estimates.ipynb` / `.py`,
  `dowhy_04_refuting_estimates_utils.py`

## What already complies

- Markdown cells use **Goal** / **Key Concepts** / **Interpretation** bullets
- LaTeX is used well for math (e.g. `$Z \sim N(0, 1)$`,
  `$Y = 2X + 0.8Z + N(0, 1)$`)
- `cellN_*()` util function names match the cell headers

## Proposed changes (by effort)

### Quick wins (low risk)

1. Fix bare dataframe display
   - Rule: `notebook.rules.md` -> "Showing Results"
   - `dowhy.04_refuting_estimates.py:319`: `job_df.head()` -> use
     `display(job_df.head())`

2. Remove non-ASCII characters
   - Rule: `notebook.rules.md` -> "Non-ASCII Characters"
   - `dowhy.04_refuting_estimates.py:88,258`: `R^2` -> `R^2`

### Structural (main issue)

3. Reorganize the flat cell list into the Part/Cell hierarchy
   - Rule: `notebook.rules.md` -> "Markdown Header Structure and Naming"
   - Current: flat level-1 `# Cell 1` ... `# Cell 12` with no Parts
   - Required: `#` reserved for `# Part N:` headers; cells use
     `## Cell <part>.<id>:`
   - Proposed grouping:
     - `# Part 1: Foundations of Refutation`
       - `## Cell 1.1` Why we cannot prove causality (current Cell 1)
       - `## Cell 1.2` Introduction to refutation methods (Cell 2)
       - `## Cell 1.3` Synthetic data with known truth (Cell 3)
       - `## Cell 1.4` Naive estimation reveals the problem (Cell 4)
     - `# Part 2: Negative-Control Refutations`
       - `## Cell 2.1` Placebo treatment (Cell 5)
       - `## Cell 2.2` Dummy outcome (Cell 6)
       - `## Cell 2.3` Random common cause (Cell 7)
       - `## Cell 2.4` Data subsample (Cell 8)
     - `# Part 3: Sensitivity Analysis`
       - `## Cell 3.1` Sensitivity to unobserved confounding (Cell 9)
       - `## Cell 3.2` Comparing estimators via refutations (Cell 10)
     - `# Part 4: Application and Synthesis`
       - `## Cell 4.1` Real data: job training impact (Cell 11)
       - `## Cell 4.2` Synthesis and decision framework (Cell 12)
   - Rename matching `cellN_*()` functions in
     `dowhy_04_refuting_estimates_utils.py` to `cell<part>_<id>_*()` to keep
     names synced (rule: "Sync Function Names with Cell Numbers")

### Larger / optional

4. Prefer pandas and seaborn over numpy and matplotlib
   - Rule: `notebook.rules.md` -> "Prefer Pandas and Seaborn"
   - 0 seaborn imports; migrate plots to seaborn where it reduces verbosity

5. Consider adding interactive exploration
   - Rule: `notebook.create_outline` -> core goal "Interactive exploration";
     `notebook.rules.md` -> "Interactive Cells"
   - The notebook is entirely static, unlike `03`. Candidate interactive cells:
     confounder strength in the synthetic DGP, placebo/subsample counts,
     sensitivity confounder-strength sweep
   - If added, follow the `htutori` idiom, multi-panel layout, and interactive
     markdown sections (see `03` proposal items 5-7)
