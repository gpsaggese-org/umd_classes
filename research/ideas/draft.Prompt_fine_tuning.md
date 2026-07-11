Convert this logic in a Python script

- There should be a dir with inputs and desired outputs

```
Your goal is to create a prompt that summarizes text in the same way I would do
it

# Step 1
- Read `<TEXT>` https://rlhfbook.com/c/01-introduction and save it into `input.md`

# Step 2
- Loop
  - Execute `prompt.md` to generate a summary of the <TEXT> in file `output.md`
  - Compare the content of `output.md` to the desired `target.md`
  - Modify `prompt.md` in order to generate a summary of `<TEXT>` closer to
    `target.md`
- Keep iterating loop until you generate you generate an output.md from <TEXT>

# Step 3
- Evaluate out of sample
```
