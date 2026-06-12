Improve the output of jupytext.py by making it less verbose at INFO level

E.g., this warnings should be print at DEBUG by passing a variable log_level to
those function so that callers can decide if they want more or less verbosity

07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'book.from_corr_to_decision/related_books.md' doesn't exist: skipping
07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'tutorials/pgmpy/Dockerfile.python_slim' doesn't exist: skipping
07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'tutorials/pgmpy/Dockerfile.ubuntu' doesn't exist: skipping
07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'tutorials/pgmpy/Dockerfile.uv' doesn't exist: skipping
07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'website/docs/blog/posts/draft.how_to.Claude_Code.md' doesn't exist: skipping
07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'website/docs/blog/posts/draft.how_to.Compare_LLM_models.md' doesn't exist: skipping
07:05:03 - WARN  hsystem.py _remove_files_non_present:460               File 'website/docs/blog/posts/draft.how_to.Use_Claude.md' doesn't exist: skipping
07:05:03 - WARN  hsystem.py remove_dirs:477                             Removed dirs: helpers_root
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: book.from_corr_to_decision/book_map.md
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: class_project/project_template/README.md
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: class_project/project_template/docker_bash.sh
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: class_project/project_template/docker_cmd.sh
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: class_project/project_template/utils.sh
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: extract_cc_log.py
07:05:03 - WARN  jupytext.py _filter_ipynb_files:59                     Skipping non-.ipynb file: instr.md


- This is ok to print

07:05:03 - INFO  jupytext.py _main:374              Processing file: tutorials/gymnasium/gymnasium.01.API.Env.ipynb

- This should be at DEBUG level
07:05:03 - INFO  jupytext.py _is_notebook_in_sync:236                   Checking sync status...
07:05:03 - INFO  jupytext.py _extract_python_from_notebook:218          Execute 'jupytext --to py:percent tutorials/gymnasium/gymnasium.01.API.Env.ipynb -o tmp.jupytext_diff.gymnasium.01.API.Env.py'
07:05:04 - INFO  jupytext.py _extract_python_from_notebook:220          Extracted Python code to: tmp.jupytext_diff.gymnasium.01.API.Env.py
07:05:04 - INFO  jupytext.py _is_notebook_in_sync:240                   Execute 'diff tutorials/gymnasium/gymnasium.01.API.Env.py tmp.jupytext_diff.gymnasium.01.API.Env.py'

- This should be printed as warning

07:05:04 - WARN  jupytext.py _is_notebook_in_sync:246                   Files are NOT in sync - there are differences
07:05:04 - WARN  jupytext.py _test:264              Notebook 'tutorials/gymnasium/gymnasium.01.API.Env.ipynb' and paired .py file are NOT in sync

- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`

- When writing unit tests for follow the instructions in
  `.claude/skills/testing.rules.md`

- If the task is not perfectly clear, you MUST not perform it, but ask for
  clarifications
  - When the task is complex, create a `plan.md` with 5 bullet points explaining
    what the plan is

