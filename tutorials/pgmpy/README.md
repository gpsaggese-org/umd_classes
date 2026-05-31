# Create a project
```
> class_project/create_project.py ---dst_dir tutorials/pgmpy
```

- Commit the changes
  ```
  > git add tutorials/pgmpy
  > git commit -am "Add template"
  > git push
  ```
- Edit `requirements.txt` to add the packages pinning down to the last version
  of the important packages

- Build th container
  ```
  > docker_build.sh
  ```

- Edit `tutorials/pgmpy/pgmpy*.py

# 

https://pgmpy.org/documentation.html

https://pgmpy.org/guides/probabilistic_inference.html

https://pgmpy.org/guides/datasets.html

- Create a tutorial
  ```
  claude> /blog.write_tutorial_tool_in_30_mins pgmpy
  ```

# Create a notebook about one topic

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
