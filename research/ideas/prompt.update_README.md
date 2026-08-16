---
name: prompt.update_README
description: Update the readme with the content of the research ideas dir
model: haiku
--- 

# Goal
- Update the file `research/ideas/README.md` given the content of the research
  ideas in the directory `research/ideas/*.md`

# Workflow

## Find the New Files
- Extract the timestamp `<TIMESTAMP>` of the last update of the
  `research/ideas/README.md`, e.g.,
  ```
  // Last update timestamp: "Aug 3 10:54"
  ```
  - Find all the files in `research/ideas/*.md` that were modified or added after
    that date
    
- Create a list of files to process `<FILES>`
  - If a file has not been modified since `<TIMESTAMP>`, it doesn't need to be
    processed
  - If there are files in `research/ideas/*.md` that are not present in the table
    or their creation timestamp is newer than `<TIMESTAMP>`, then add them to
    list of file to process

## Template for Research Ideas
- The template for each research idea is `research/ideas/template.research_idea.md`

## Update the Table

- For each file in `<FILES>` complete a row in the same format (to the best of
  your ability) as the table in the README
  ```
  | File | Links | Status | Assignee | Specs Complete | GitHub Issue | Result |
  ```
- Update the table with the information
- Sort the rows by descending "Specs Complete"

## Update the Timestamp
- Update the timestamp of the README with the current timestamp
