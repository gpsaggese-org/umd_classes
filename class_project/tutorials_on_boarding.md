- Go through the tutorials and create an issue called "Clean up XYZ" for your
  tutorials

- The issue should have the following steps:

- [ ] Read `class_project/project_template/README.md`
  - Is there anything unclear, incorrect, or that can be improved?
- [ ] Carefully look at all the code `class_project/project_template`
  - Make sure that you understand everything perfectly
- [ ] Read `class_project/README.md`
  - Is there anything unclear, incorrect, or that can be improved?
- [ ] Become familiar with the Claude Skills in `helpers_root/.claude/skills`
  we use to maintain the code base
  - The Skills are a living documentation of how we do things
    ```
    > md skill X_in_60_m
    ...

    > md skill describe coding

    coding.factor_common_code ....... Identify and refactor duplicated code blocks into shared functions across Python files
    coding.find_doc ................. Find documentation files for a given dir, file, class, or function and summarize in 3 bullet points
    coding.fix_bloated_imports ...... Fix Python imports of large packages needed only for few functions in a module
    ...

    > md skill describe notebooks
    ...
    ```
  - Make sure that you understand everything perfectly
  - Is there anything unclear, incorrect, or that can be improved?


- [ ] Read very carefully the reference tutorial, i.e., the one that is closest
  to the "perfect" style
  - Currently is XYZ
- [ ] Read 2-3 tutorials built by other people to make sure that you see and
  internalize the patters

- [ ] Read 

- Use a professional tone

- Focus only on the examples without repeating content
  - Everything should be said only once and in the right place

- Each tutorial need to have
  - [ ] Add unit tests for the dir such as
    `class_project/project_template/test/test_docker_all.py`

- Avoid AI slop at any cost
  - Humans can sense it and once it's detected everything else sounds horrible
  - We will not put out low quality content
  - A tutorial / blog can't be "throw a prompt in Claude Code and copy-paste
    the result"
