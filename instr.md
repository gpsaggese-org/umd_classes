### [ ] Convert render_typst.sh into run_typst.py similar to
helpers_root/dev_scripts_helpers/documentation/run_latex.py

Use a similar interface to run_latex.py since they are similar
in function, save them close to each

Also look at
helpers_root/dev_scripts_helpers/documentation/notes_to_pdf.py
to see structure and interface

Use the --action approach

- render_images.py is an optional step
- Assert if there are warnings, unless --no_abort_on_warnings
