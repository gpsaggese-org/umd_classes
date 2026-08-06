# Plan: Fix notebook.rules.md violations in probabilistic_inference.ipynb

## Context

A rules check (`/skill.check_against_rules`) was run on
`tutorials/pgmpy/probabilistic_inference.ipynb` against `.claude/skills/notebook.rules.md`.
Multiple violations were found. This plan fixes them in priority order.

---

## Files to modify

- `tutorials/pgmpy/probabilistic_inference.py` (Jupytext source, synced to `.ipynb`)
- `tutorials/pgmpy/probabilistic_inference_utils.py` (utility functions)

After edits, sync the `.ipynb` from the `.py` source via Jupytext.

---

## Phase 1: Quick fixes in the notebook `.py` (no behavior change)

### 1a. Remove duplicate Cell 6.1 code cell
The block at lines 262-272 is an exact duplicate of the first Cell 6.1 code cell
(lines 245-249) plus a print block. Delete the second copy entirely.

### 1b. Remove print blocks that duplicate markdown explanations
Print blocks after `plt.show()` restate what the following markdown explanation
cell already says. Remove these print blocks:
- Cell 5.2 (`probabilistic_inference.py:197-204`): remove the 8-line `print(...)` block
- Cell 7.1 (`:299-300`): remove 2-line `print(...)` block

### 1c. Fix non-ASCII character
Line 258: change `≤15 variables` to `<=15 variables` in the markdown cell.

### 1d. Uncomment logging initialization
Cell 1.2 (lines 49-51): uncomment the three commented-out initialization calls:
```python
hnotebook.config_notebook()
hdbg.init_logger(verbosity=logging.INFO, use_exec_path=False)
hnotebook.set_logger_to_print(_LOG)
```

---

## Phase 2: Add required structured markdown for interactive cells

The rule requires interactive cells to have a markdown cell with four sections:
**Goal**, **Plots**, **Parameters**, **Key observations**.

Cells that are missing this (or have only free-form text):
- Cell 3.2: CPD visualization widget -- no explanation markdown at all
- Cell 5.3: Evidence explorer -- has free-form bullets, needs restructuring into the 4 sections
- Cell 7.2: Gibbs sampling interactive -- no explanation markdown at all
- Cell 7.3: Joint distribution explorer -- has free-form bullets, needs restructuring
- Cell 8.1: Larger network interactive -- has free-form bullets, needs restructuring

For each, write/replace the markdown cell that follows the code cell with the
standard 4-section format (3-5 bullets per section).

---

## Phase 3: Fix `figsize` hard-coding in utils static plot functions

All static plot functions currently hard-code `figsize` inside the function body.
Add an optional `figsize` parameter following the rule pattern:

```python
def cell4_1_forward_sample_and_plot(
    model: DiscreteBayesianNetwork,
    *,
    n_samples: int = 1000,
    figsize: Optional[Tuple[int, int]] = None,
) -> None:
    if figsize is None:
        figsize = plt.rcParams["figure.figsize"]
    ...
```

Apply to these functions in `probabilistic_inference_utils.py`:
- `cell4_1_forward_sample_and_plot` (line 248: `figsize=(14, 4)`)
- `cell4_2_compare_exact_and_sampling` (line 306)
- `cell5_1_condition_on_evidence` (line 361)
- `cell5_2_compare_exact_and_sampling` (line 427)
- `cell6_1_compare_inference_algorithms` (line 602)
- `cell7_1_map_query_demo` (line 652)
- `cell8_2_practical_workflow_demo` (line 1143)

The `_visualize_network_impl` / `cell2_2_visualize_network` already accepts `figsize`
as a parameter -- no change needed there.

---

## Phase 4: Migrate interactive widgets to htutori idiom

This is the largest change. Five functions in `probabilistic_inference_utils.py`
use raw `ipywidgets` instead of the standard `htutori` helpers.

### Import to add at top of utils file
```python
import helpers.htutorial as htutori
```

### Functions to migrate

**`cell3_2_create_cpd_widget`** (currently uses `FloatSlider` + `ToggleButtons`):
- Replace `FloatSlider` with `htutori.build_widget_control(name="prior", ...)` for the disease prior
- Keep `ToggleButtons` for the evidence selector (no htutori equivalent for categorical)
- Convert from 3-panel to 4-panel layout: ax1=CPD heatmap, ax2=disease prior bar, ax3=posterior bar, ax4=comments panel via `htutori.add_fitted_text_box()`
- Use standard `with output: clear_output(wait=True)` idiom

**`cell7_2_gibbs_sampling_interactive`** (currently uses 2x `IntSlider` + `Button`):
- Replace first `IntSlider` (samples) with `htutori.build_log_widget_control(name="N", min_exp=6, max_exp=13, initial_exp=9, base=2)` (gives 64 to 8192)
- Replace second `IntSlider` (burn-in) with `htutori.build_widget_control(name="burn-in", min_val=0, max_val=2000, step=100, initial_value=200, is_float=False)`
- Add `seed` widget first: `htutori.build_widget_control(name="seed", min_val=0, max_val=99, step=1, initial_value=42, is_float=False)`
- Keep `Button` for "Run Sampling"
- Convert to 4-panel: chain trace, histogram of samples, running mean convergence, comments panel

**`cell5_3_create_evidence_explorer`** (uses 2x `Dropdown` + `Button`):
- Dropdown controls have no htutori equivalent; keep as `ipywidgets.Dropdown`
- Fix broken layout: currently creates `plt.subplots(1, 2)` then calls `_visualize_network_impl()` which creates a separate figure via graphviz -- the network ends up floating outside the subplot. Replace with 4 proper subplots (no embedded graphviz call).
- Convert to 4-panel: prior bars, posterior bars, delta bars, comments panel

**`cell7_3_joint_distribution_explorer`** (uses 2x `Dropdown`):
- Keep `Dropdown` controls
- Convert to 4-panel: joint heatmap, Disease marginal bar, Test marginal bar, comments panel

**`cell8_1_larger_network_interactive`** (uses 2x `Dropdown`):
- Keep `Dropdown` controls
- Fix same broken layout issue as cell5_3 (graphviz figure)
- Convert to 4-panel: posterior bar chart, network topology, scaling comparison, comments panel

### Standard pattern for every interactive function after migration
```python
def cellN_M_...(*, figsize=None):
    if figsize is None:
        figsize = (20, 5)
    seed_slider, seed_box = htutori.build_widget_control(name="seed", ...)
    param_slider, param_box = htutori.build_widget_control(name="param", ...)
    output = ipywidgets.Output()

    def update_plot(change=None):
        seed = seed_slider.value
        param = param_slider.value
        with output:
            clear_output(wait=True)
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=figsize)
            # ... fill ax1-ax3 ...
            ax4.axis("off")
            ax4.set_title("Comments", fontsize=14, fontweight="bold", pad=20)
            htutori.add_fitted_text_box(ax4, f"param={param}\n...")
            plt.tight_layout()
            plt.show()

    seed_slider.observe(update_plot, names="value")
    param_slider.observe(update_plot, names="value")
    update_plot()
    display(ipywidgets.VBox([
        ipywidgets.Label("Description:"),
        seed_box,
        param_box,
        output,
    ]))
```

---

## Phase 5: Sync `.ipynb` from `.py`

After all edits to `.py`:
```bash
cd tutorials/pgmpy
jupytext --sync probabilistic_inference.ipynb
```

---

## Verification

1. Run `jupytext --check probabilistic_inference.ipynb` to verify sync
2. Open notebook in Jupyter and run all cells top-to-bottom; confirm no errors
3. Verify each interactive widget renders with 4 panels
4. Confirm no non-ASCII characters: `grep -nP '[^\x00-\x7F]' probabilistic_inference.py`
5. Confirm no `print()` blocks below `plt.show()` in the notebook source
