# Create a 
class_project/create_project.py ---dst_dir tutorials/pgmpy

Next steps:
- Commit the changes
```
> git add tutorials/pgmpy
> git commit -am "Add template"
> git push
```
- Change `tutorials/pgmpy/requirements.txt`
- Edit `tutorials/pgmpy/pgmpy*.py

Edit vi requirements.txt to add the packages pinning down to the last version

docker_build.sh

# 

https://pgmpy.org/documentation.html

https://pgmpy.org/guides/probabilistic_inference.html

https://pgmpy.org/guides/datasets.html

Create a tutorial
/blog.write_tutorial_tool_in_30_mins pgmpy

# Create a notebook about one topic
/notebook.create_outline https://pgmpy.org/guides/probabilistic_inference.html

which creates notebook_outline.probabilistic_inference.md

/notebook.implement_outline tutorials/pgmpy/notebook_outline.probabilistic_inference.md

This creates
probabilistic_inference.ipynb
probabilistic_inference_utils.py

jupytext.py --action pair --files probabilistic_inference.ipynb

linters2/lint_cc.py --files tutorials/pgmpy/probabilistic_inference_utils.py

docker_jupyter.sh
http://localhost:8888/lab/tree/git_root/tutorials/pgmpy/probabilistic_inference.ipynb

#
docker_cmd.sh "python /git_root/tutorials/pgmpy/probabilistic_inference.py"

