# Create a project

- Create the dir
  ```bash
  > class_project/create_project.py ---dst_dir tutorials/pgmpy
  ```

- Commit the changes
  ```bash
  > git add tutorials/pgmpy
  > git commit -am "Add template"
  > git push
  ```
- Edit `requirements.txt` to add the packages pinning down to the last version
  of the important packages

- Build the container
  ```bash
  > docker_build.sh
  ```

- Edit `tutorials/pgmpy/pgmpy*.py`

# Create a Tutorial

- Create a tutorial
  ```
  claude> /blog.write_tutorial_tool_in_30_mins pgmpy
  ```

# Create a notebook about one topic

## Using `/notebook.create_outline` and `/notebook.implement_outline`

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

## Using /notebook.implement_for_package_API

- The skill `./helpers_root/.claude/skills/notebook.implement_for_package_API/SKILL.md` is more complete
  ```
  claude> /notebook.implement_for_package_API pgmpy https://pgmpy.org/guides/probabilistic_inference.html and save it in tutorials/pgmpy/pgmpy.01.API.probabilistic_inference.ipynb
  ```

  ```
  claude> /notebook.implement_for_package_API pgmpy https://pgmpy.org/guides/datasets.html and save it in tutorials/pgmpy/pgmpy.02.API.datasets.ipynb
  ```

  claude> /notebook.implement_for_package_API pgmpy https://pgmpy.org/guides/example_models.html and save it in tutorials/pgmpy/pgmpy.03.API.example_models.ipynb

  - [Example Models](https://pgmpy.org/guides/example_models.html)
