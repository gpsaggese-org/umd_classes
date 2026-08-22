---
title: "A Queue of AI Coding Agents"
draft: true
authors:
  - gpsaggese
date: 2026-08-20
categories:
  - AI Coding
  - Developer Tools
---

TL;DR: A flow to run a queue of AI agents that fix issues asynchronously.

<!-- more -->

This is my flow to have a queue of AI agents fixing asynchrnously issues

- My coding set up is:
  - GitHub (GH)
  - Claude Code (CC)
  - `ai_helpers` repo

# Overview

- Create a list of issues with specs that can be executed asynchronously
- Create automatically GH issues
- Assign the GH issues to CC to generate a PR

# Getting Tasks in the Queue

- The core pattern is
  - Queue: GitHub Issues (with a specific label or assigned to a specific user)
  - Trigger: a GitHub Actions that triggers when an issue is labeled assigned
    marking it as part of the Queue
  - Agent: Claude Code, running in the GH Actions, read the issue, write the
    code and open a PR for human review

- I maintain a markdown file called `ai_task_queue.md` with everything that I
  would like to be done

// TODO(gp): Check ./helpers_root/dev_scripts_helpers/ai/todo_janitor.template.md

- The format of the queue is like:
  ```
  # Ready

  ## [ ] Use System_to_one_line() in Hgit.py

  ## [ ] <GitHub Issue Title>

  <Specs>

  # Backlog

  ...

  # Done

  ...
  ```

- E.g., potential targets are:
  - Todos in the codebase marked with `TODO(ai_gp)` 
  - Ensuring that file have 100% code coverage by unit test
  - Make sure all files follow the style rules of the repo (e.g., 
  - Make sure all files pass the linter stage (e.g., `pyright` warnings)
  - Triage and propose a solution for unit tests that are disabled
  - Explore a research idea
  - One-off refactoring and code clean ups
  - Prototyping / "Tracer bullet" where I one-shot something to see what is
    its impact

- I tend to run certain classes of tasks 
  - Maintaining the documentation in sync with code
  - Making sure code coverage for the entire repo is high enough
  are more on a once-a-week or on a schedule, while the `ai_task_queue.md` are
  one-offs

- My approach is to add tasks in `ai_task_queue.md` as they come up, re-organize
  them, triage their importance over time, add specs and then mark them as ready for
  execution at a certain point

## The Unit of Work

- The unit of work is
  - A GitHub issue
  - A Git branch
  - A GitHub PR

- In general one GitHub issue can correspond to multiple Git branches / GitHub PR
  - E.g., the same refactoring can be done in "chunks" with follow up PRs (for both
    safety and ease of review)

### Feeding issues

- E.g., create a list of tasks from TODOs
  ```
  > rigtodo
  > rigtodo . py --todo ai_gp | tee cfile
  ```

- Note that not all TODOs might be ready to go, so I manually review the list of
  potential tasks and move them to `Ready` vs `Backlog`
  ```
  > vic
  ```
- Split and do `open cfile`
- Review the issues one by one
- Make sure that `cfile` is the desired one

### Add Specs

- Improve
  ```
  # Create instr.md with the instructions
  claude> /auto_task.criticize instr.md
  ```

- Create the list of CC tasks from the cfile
  ```
  claude> /coding.create_auto_todo cfile
  ```
- Review and edit `ai_task_queue.md`
- This is the master list of what needs to be done

- Ranks them by "simplicity" and "importance"
- Create a `ai_task_queue` with problem, solution, complexity, importance
- User reviews them and add a [ ] ready

- There is overlap with GitHub `gh` to manage issues but personally I prefer to batch
  the issues in a GH, keep working / refining them, and then push everything to
  GitHub with a script

- The workflow is:
  - Maintain / replenish `ai_task_queue.md`
  - Create GitHub issue
  - Create a branch / PR /
  - Let CC fix the issues (interacting on GitHub, running regressions, etc)
    and creating a PR when ready
  - (Optional) Check out the branch to make changes manually, when explaining
    something takes longer than just doing it
  - Review PR and merge it
  - Close GH Issue
  - Update `ai_task_queue.md` with the ones that were done

- This is the same workflow I used to use with collaborators with the main difference
  that now AI agents are doing the work (and there is a bump in throughput and often
  time in quality, at least for PR that pure implementation and not design)

- Other tasks can be executed on **GitHub**

  > git_create_issue_and_branch.py --gh_issue_title 'Implement TODOs' --gh_issue_body_file instr.md

  Attach the Git branch and the PR to the issue using a gh comment

  > gh pr comment

  Assign the task to Claude to let it go using the GH actions or use the Desktop


### An Alternative Local Flow

- There are also tasks that can / should be run **locally**
  - E.g., run the local regressions, more control and interactivity
  - I use the same approach as above but I work with the AI agent in worktrees
    (which is managed automatically together with GH Issue, Git branch, GH PR
    using proper tooling)
  ```
  > git_create_issue_and_branch.py --gh_issue_title 'Implement TODOs' --gh_issue_body_file instr.md --create_worktree
  > cd /Users/saggese/src/helpers1_worktree_1325; dev_scripts_helpers/thin_client/tmux.py --index 1325
  ```

- In some cases I want CC to commit directly in its branch (you know that I don't
like the agent do that while I am driving the development)

- Enable CC to commit (needed for local dev) using `control_cc_commit.py`

  ```
  claude> Implement the GitHub instructions from gh issue view 1325
  ```

- Commit after the first PR

- Review

- Run tests that were touched
  ```
  > i git_files --mode test_files --on-one-line --pbcopy
  > pytest_log $(pbpaste)
  #
  > pytest_log $(i git_files --mode test_files --on-one-line --only-print-files | remove_escape_chars.py -i -)
  ```

- .claude/todo_janitor.template.md

### Old instructions

//```
//# Create todo_janitor plan
//
//# Pick Issues to Fix
//
//## Make sure that the list is updated
//
//  ```
//  claude> Look at the last merged git PRs in master and in the current repo and mark the completed issues in plan.todo_janitor.md
//  ```
//
//## Pick an Issue and Create the Branch
//
//- Go in helpers1 tree (which is the one from which everything is orchestrated)
//
//- Pick an issue from `plan.todo_janitor.md` and create a `todo_janitor.issue.md`
//
//## Create CC Instructions
//
//- Create instructions for CC from `todo_janitor.instr.md`
//
//## Create the Branch / Worktree
//  ```
//  > create_git_worktree.py --gh_issue_title 'Clean up' --gh_issue_body_file todo_janitor.current_issue.md
//  > create_git_worktree.py --gh_issue_title "Rename invocations to sys_calls Throughout Codebase" --gh_issue_body body.txt --instr_file instr2.md
//
//  > create_git_worktree.py --gh_issue_id 1292 --instr_file instr2.md
//  ```
//
//> more instr2.md
//- Wait that all the checks are complete and passing
//  i gh_workflow_list
//
//- If the tests are passing, run all the tests locally
//  pytest_multi_build.py --target .
//
//- If there are not issues, then mark the PR as ready
//  gh pr  comment --body "All tests are passing"
//
//- Ask to review
//
//### Check that PR is ready to review
//
//> gh pr view
//gp_scratch_36 causify-ai/helpers#1330
//Draft • gpsaggese (GP Saggese) wants to merge 2 commits into master from gp_scratch_36 • about 4 minutes ago
//+2359 -836 • ✓ Checks passing
//
//### Update the CC task plan
//- Automate some of the work above
//  ```
//  orchestrate_task.py --plan ... --action
//
//  --action stage_todo calling create_git_worktree.py (
//      - create the body and instr.md
//      - update the todo
//  ```
//
//# Fix the issue
//- Go to helper...
//
//- git checkout HelpersTask1299_TODO_clean_up
//
//- Enable CC to commit
//  - Use .claude/cc_control
//```
//claude> Execute todo_janitor.template.md
//```
//
//## Commit the changes
//
//### [ ] Convert CC flow to script
//- Convert todo_janitor.template.md into a single script since CC doesn't
//  follow the directions
//
//````
