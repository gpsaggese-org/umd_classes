---
name: prompt.update_README
description: Update the readme with the content of the research ideas dir
model: haiku
--- 

# Goal
- Update the `<README>` file `class_project/project_descriptions/README.md` given
  the content of the files in the directory
  `class_project/data605` and `class_project/msml610`

# Workflow

## Find the Files
- Create a list of files to process `<FILES>`

## Create List of Files to Process

- For each file in `<FILES>` complete a row in the same format as the table
  in the README (to the best of your ability)
  ```
  | Project name | Status | Authors | GitHub Issue | Result | Session |
  ```
