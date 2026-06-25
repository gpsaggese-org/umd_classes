- This document shows how to create a tutorial for a package

- Create the skeleton of the project
  ```bash
  > export PROJ=...
  > class_project/create_project.py ---dst_dir tutorials/${PROJ}
  ```

- Commit the changes
  ```bash
  > git add tutorials/${PROJ}
  > git commit -am "Add template"
  > git push
  ```

## Create the README

- Create the blog entry for the tutorial
  ```
  claude> /blog.write_tutorial_readme ${PROJ}
  ```

- Find information about:
  - Installation
  - Documentation
  - Tutorial

- Edit `requirements.txt` to add the packages pinning down to the last version
  of the important packages

- Build the container
  ```bash
  > docker_build.sh
  ```

- Edit `tutorials/${PROJ}/${PROJ}.py`


## Create Notebook about API intro

- Create a short README for the blog:
  ```
  claude> /notebook.create_api_intro ... https://....html and save it in tutorials/${PROJ}/${PROJ}.01.API.XYZ.ipynb
  ```
- The file is `.claude/skills/notebook.create_api_intro/SKILL.md`

## Create Notebook about Examples

// TODO(gp): Improve this

- Create `notebook_outline.probabilistic_inference.md`
  ```
  claude> /notebook.create_outline https://pgmpy.org/guides/probabilistic_inference.html
  ```
- Review the outline

- Create the notebook
  ```
  claude> /notebook.implement_outline tutorials/pgmpy/notebook_outline.probabilistic_inference.md
  ```
- This creates:
  - probabilistic_inference.ipynb
  - probabilistic_inference_utils.py

- Create paired Python
  ```
  > jupytext.py --action pair --files probabilistic_inference.ipynb
  ```

- Fix / improve the `*_utils.py`
  ```
  > linters2/lint_cc.py --files tutorials/pgmpy/probabilistic_inference_utils.py
  ```

- Make sure everything runs end to end
  ```
  > docker_cmd.sh "python /git_root/tutorials/pgmpy/probabilistic_inference.py"
  ```

- Edit and improve the notebook
  ```
  > docker_jupyter.sh
  http://localhost:8888/lab/tree/git_root/tutorials/pgmpy/probabilistic_inference.ipynb
  ```
