### [x] Convert render_typst.sh into run_typst.py similar to
helpers_root/dev_scripts_helpers/documentation/run_latex.py

Use a similar interface to run_latex.py since they are similar
in function, save them close to each

Also look at
helpers_root/dev_scripts_helpers/documentation/notes_to_pdf.py
to see structure and interface

Use the --action approach

- render_images.py is an optional step
- Assert if there are warnings, unless --no_abort_on_warnings

## Result
- `helpers_root/dev_scripts_helpers/typst/run_typst.py` already existed
  (committed in the `helpers_root` submodule), with the `--action` CLI,
  `compile`/`open_pdf`/`render_images` actions, `--no_abort_on_warnings`,
  and daemon mode, mirroring `run_latex.py`'s structure
  - It lives in a new `dev_scripts_helpers/typst/` dir (alongside the other
    `.typ` template files), not next to `run_latex.py`, since it groups
    with the other Typst-specific assets
- Fixed a bug found by the existing test suite: `_DEFAULT_ACTIONS` wrongly
  included `render_images`, making it run by default and contradicting
  both the docstring and `test_run_typst.py::Test_run_typst_py::test1`
  - Removed it from `_DEFAULT_ACTIONS`; all 11 tests in
    `test_run_typst.py` pass now
- Not done: nothing outstanding for this item
