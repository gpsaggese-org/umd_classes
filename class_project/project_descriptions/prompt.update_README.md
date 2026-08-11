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

## Find the New Files
- Extract the timestamp `<TIMESTAMP>` of the last update of the `<README>` file
  ```
  // Last update timestamp: "Aug 3 10:54"
  ```
  - Find all the dirs in `class_project/` that were modified or added after
    
- Create a list of files to process `<FILES>`
  - If a file was not modified since `<TIMESTAMP>`, it doesn't need to be
    processed
  - If there are files in `research/ideas/*.md` that are not present in the table
    or their creation timestamp is newer than `<TIMESTAMP>`, then add them to
    list of file to process

## Create List of Files to Process

- For each file in `<FILES>` complete a row in the same format as the table
  in the README
  ```
  | File | Links | Status | Assignee | Specs Complete | GitHub Issue | Result |
  ```
  - Completing to the best of your ability

- Update the table with the information
- Sort the rows by descending "Specs Complete"

## Update the Timestamp
- Update the timestamp of the `<README>` with the current timestamp
