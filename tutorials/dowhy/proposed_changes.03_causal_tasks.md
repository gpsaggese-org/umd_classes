# Proposed changes: `dowhy.03_causal_tasks`

- Reviewed against `.claude/skills/notebook.rules.md`,
  `.claude/skills/notebook.create_outline/SKILL.md`,
  `.claude/skills/notebook.implement_outline/SKILL.md`
- Files affected: `dowhy.03_causal_tasks.ipynb` / `.py`,
  `dowhy_03_causal_tasks_utils.py`

## What already complies

- Part/Cell header hierarchy is correct and sequential
  (`# Part 1` ... `## Cell 1.1`)
- `cellX_Y_*()` util function names match the cell headers
- Utils organized with section dividers in cell order
- Dataframes are shown via `display()`

## Proposed changes (by effort)

### Quick wins (low risk)

1. Remove non-ASCII characters from markdown and code
   - Rule: `notebook.rules.md` -> "Non-ASCII Characters", "Avoid
     Capitalization, Emojis, and HTML"
   - Locations in `dowhy.03_causal_tasks.py`:
     - `:87,88,100,152,210,264` — `->` / `<-` arrows: replace with `->` / `<-`
     - `:88` — `~=`: replace with `~=` or LaTeX `$\approx$`
     - `:277` — `R^2`: replace with `R^2`
     - `:441,444` — `in`: replace with `in`
     - `:229,496` — en-dash `-` in headers: replace with `-`
   - Location in `dowhy_03_causal_tasks_utils.py`:
     - `:296` — `label="True ATE ~= 0.2"`: replace `~=` with `~=`

### Markdown / pedagogical

4. Convert prose paragraphs to nested bullet lists and use LaTeX for math
   - Rule: `notebook.rules.md` -> "Use Nested Bullet Lists", "Use LaTeX
     Notation"
   - Example: `dowhy.03_causal_tasks.py:79-88` is paragraph prose with
     `~= 10`; rewrite as nested bullets and use `$\approx 10$`

5. Add the required markdown sections before each interactive cell
   - Rule: `notebook.rules.md` -> "Markdown Cell Content for Interactive Cells"
   - Each widget cell (e.g. `## Cell 1.2`, `## Cell 1.3`, `## Cell 1.5`,
     `## Cell 3.1`, `## Cell 4.1`, `## Cell 4.2`, `## Cell 4.3`, `## Cell 5.2`,
     `## Cell 6.1`) needs a markdown cell with **Goal**, **Plots**,
     **Parameters**, **Key observations** (3-5 bullets each)

### Large refactors (touch `dowhy_03_causal_tasks_utils.py`)

6. Migrate all 9 interactive widgets to the `htutori` idiom
   - Rule: `notebook.rules.md` -> "Interactive Idiom for Notebooks", "Widgets"
   - Functions: `cell1_2_interactive_adjustment_methods` (`:267`),
     `cell1_3_interactive_iv_strength` (`:387`),
     `cell1_5_interactive_patient_profile` (`:626`),
     `cell3_1_interactive_anomaly_dashboard` (`:1308`),
     `cell4_1_interactive_intervention` (`:1694`),
     `cell4_2_interactive_counterfactual` (`:1788`),
     `cell4_3_interactive_policy` (`:1944`),
     `cell5_2_interactive_population_comparison` (`:2159`),
     `cell6_1_interactive_decision_tree` (`:2230`)
   - Replace raw `ipywidgets.Dropdown/Output/VBox` with:
     - `htutori.build_widget_control()` / `build_log_widget_control()`
     - Seed widget placed first
     - +/- buttons and value display on each widget

7. Adopt the multi-panel layout for interactive cells
   - Rule: `notebook.rules.md` -> "The Multiple-Panel Layout Pattern"
   - Use a 1xn layout: panels 1-3 for data, panel 4 a wheat comment box via
     `htutori.add_fitted_text_box()`; replace single-panel `plt.subplots`
     (e.g. `utils.py:287`)

8. Make every plotting function accept `figsize`
   - Rule: `notebook.rules.md` -> "Configurable Figure Sizes"
   - All 12 plotting functions hard-code `_SINGLE_PANEL_FIGSIZE` etc.
     (`utils.py:23-26`); add an optional `figsize` parameter that defaults to
     `plt.rcParams["figure.figsize"]`

9. Prefer pandas and seaborn over numpy and matplotlib
   - Rule: `notebook.rules.md` -> "Prefer Pandas and Seaborn"
   - 0 seaborn imports; 15 hard-coded `np.random.seed`; heavy numpy data
     manipulation
   - Migrate data manipulation to pandas and plots to seaborn where it reduces
     verbosity
