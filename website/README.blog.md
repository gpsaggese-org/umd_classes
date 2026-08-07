# Blog Posts

- This document tracks the work on the blogs
- Blogs are ranked from _most ready_ (near-publishable) to _least ready_ (raw
  scratchpad).
  - Criteria: front matter completeness, TL;DR quality, content structure, and polish.

# Published Blogs

- To extract dates and paths use:
  ```
  > website/find_published_blogs.sh
  ```

## Published Blogs

- 2026-06-24: `website/docs/blog/posts/TIL.Autoreload_in_vim.md`
- 2026-06-22: `website/docs/blog/posts/how_to.Render_md_from_terminal.md`
- 2026-06-21: `website/docs/blog/posts/in_10_mins.helpers_open_md.md`
- 2026-06-12: `website/docs/blog/posts/how_to.Use_OpenRouter.md`
- 2026-06-05: `website/docs/blog/posts/how_to.Use_Claude_Code_with_Openrouter.md`
- 2026-05-29: `website/docs/blog/posts/how_to.LLM_effort.md`
- 2026-05-22: `website/docs/blog/posts/how_to.Count_cost.md`
- 2026-05-15: `website/docs/blog/posts/how_to.Compare_LLM_models.md`
- 2026-05-08: `website/docs/blog/posts/in_30_mins.helpers_llm_cli.md`
- 2026-05-01: `website/docs/blog/posts/in_30_mins.simonw_llm_cli.md`
- 2026-04-24: `website/docs/blog/posts/in_30_mins.mdm_unified_markdown_manager.md`
- 2026-04-17: `website/docs/blog/posts/in_30_mins.Python_Code_Coverage.md`
- 2026-04-10: `website/docs/blog/posts/in_60_mins.CausalML.md`
- 2026-04-03: `website/docs/blog/posts/in_60_mins.BambooAI.md`
- 2026-03-27: `website/docs/blog/posts/in_60_mins.TorchRL_MAC.md`
- 2026-03-20: `website/docs/blog/posts/how_to.Connect_Claude_Code_to_Gmail.md`
- 2026-03-13: `website/docs/blog/posts/in_60_mins.AutoGen.md`
- 2026-03-06: `website/docs/blog/posts/in_60_mins.Tensorflow.md`
- 2026-02-27: `website/docs/blog/posts/in_30_mins.Python_Packaging.md`
- 2026-02-20: `website/docs/blog/posts/in_30_mins.uv.md`
- 2026-02-13: `website/docs/blog/posts/in_30_mins.ripgrep.md`
- 2026-02-06: `website/docs/blog/posts/Welcome_to_Our_Blog.md`

Total: 22 published blogs

# Draft Blogs

## High-priority

- `website/docs/blog/posts/draft.in_30_mins.helpers_caching.md`
  - `helpers_root/docs/tools/helpers/all.hcache_simple.explanation.md`
  - `helpers/hcache_simple.py`

- `helpers/hllm.py`
    Underlying LLM completion interface
  - [`notebooks/hllm.tutorial.ipynb`](https://github.com/causify-ai/helpers/blob/master/helpers/notebooks/hllm.tutorial.ipynb):
  Jupyter notebook with `hllm` usage examples

- `website/docs/blog/posts/draft.in_5_mins.helpers_cc.md`

- `website/docs/blog/posts/draft.in_15_mins.helpers_hunit_test.md`

- `website/docs/blog/posts/draft.in_30_mins.helpers_hllm_decorator.md`

- `lint_text.py`
- `linters2/lint.py`
- `linters2/lint_cc.py`

- helpers/hcheck_types.py + dassert

- `helpers_root/import_check/detect_import_cycles.py`
  - `helpers_root/docs/tools/all.import_check.reference.md`

- `linters2/normalize_import.py`

- `helpers_root/dev_scripts_helpers/system_tools/create_links.py`
  - `docs/tools/dev_system/all.replace_common_files_with_script_links.md`

- `website/docs/blog/posts/draft.in_5_mins.helpers_render_images.md`
  - `helpers_root/dev_scripts_helpers/documentation/render_images.py`
  - `helpers_root/dev_scripts_helpers/documentation/test/test_render_images.py`
  - `dev_scripts_helpers/documentation/render_images.README.md`

- `website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md`

- `helpers_root/docs/documentation_meta/all.architecture_diagrams.explanation.md`
- `helpers_root/docs/documentation_meta/all.diataxis.explanation.md`
- `helpers_root/docs/documentation_meta/all.gdocs.how_to_guide.md`
- `helpers_root/docs/documentation_meta/all.google_technical_writing.how_to_guide.md`
- `helpers_root/docs/documentation_meta/all.markdown_tools.explanation.md`
- `helpers_root/docs/documentation_meta/all.plotting_in_latex.how_to_guide.md`
- `helpers_root/docs/documentation_meta/all.writing_docs.how_to_guide.md`
- `helpers_root/dev_scripts_helpers/system_tools/README.md`

- Blogs from `helpers_root/papers/AIgentic_Development_System/`

### Typst
  website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md
  website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.all_examples.typ
  website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.hello_world.typ
  website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.all_examples.typ
  website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.hello_world.typ
  website/docs/blog/posts/draft.how_to.latex_vs_typst_for_typsetting.md

### Typesetting flow
  website/docs/blog/posts/draft.in_30_mins.helpers_typesetting_system.md
  dev_scripts_helpers/documentation/README.md
  dev_scripts_helpers/documentation/README.notes_to_pdf.md

- Invoke bash_print_tree
  - `helpers_root/docs/tools/all.invoke_git_branch_copy.how_to_guide.md`

- Invoke workflow
  - `helpers_root/docs/tools/all.invoke_workflows.how_to_guide.md`

- Linter
  - `helpers_root/docs/tools/linter/all.developing_linter.how_to_guide.md`
  - `helpers_root/linters2/README.md`

- Pre-commit
  - `helpers_root/linters2/lint.README.md`

- `helpers_root/docs/tools/all.invoke_git_branch_copy.how_to_guide.md`

- https://docs.google.com/spreadsheets/d/1FpBI4tysk2kMSNeTc3WTGOw8KZkr4yG85nfDwqu8Fdo/edit?gid=1995318049#gid=1995318049
- https://docs.google.com/document/d/1_G5bgSSxrC1EMA1eOx3KXNifj6XFSdZ6cebeZJKpywY/edit?tab=t.ihrvh5211a4x#heading=h.tdzvl3alcciy
- /Users/saggese/src/csfy1/blog/docs/posts

- Profiling ./helpers_root/docs/tools/all.profiling.how_to_guide.md

- Pre-commit hooks helpers_root/dev_scripts_helpers/git/git_hooks/pre-commit.py

## TIL

- How to 
  .claude/statusline.sh
  .claude/settings.local.json

## From notes

/Users/saggese/src/notes1/blog/posts

/Users/saggese/src/notes1/notes
  - cs.software_development.txt - Software dev practices
  - cs.The_clean_coder.Martin.2011.txt
  - cs.The_pragmatic_programmer.txt
  - IN_PROGRESS.cs.A_philosophy_of_software_design.Ousterout.2018.txt
  - IN_PROGRESS.cs.Clean_architecture.Martin.2017.txt
  - IN_PROGRESS.cs.Design_it.Keeling.2017.txt

python.pytest.txt
python.asyncio.txt
python.mypy.txt
python.mock.txt
python.invoke.txt

# Drafts

## List of Drafts (ranked by readiness)

| File | Words | Ready % | Comment |
|------|-------|---------|---------|
| `website/docs/blog/posts/draft.Ax_Multi_Objective_Optimization_On_Marketing_Campaigns.md` | 1713 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.Claude_Paid_Plans.md` | 1015 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.Intro_to_Bayesian_Optimization.md` | 1553 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.how_to.Coding_Agents.md` | 1873 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.how_to.Convert_PDF_to_Markdown.md` | 1544 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.in_10_mins.helpers_hllm.md` | 1477 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.in_15_mins.helpers_hunit_test.md` | 1488 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.in_30_mins.pi_dev.md` | 1537 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.in_5_mins.helpers_render_images.md` | 1086 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.in_60_mins.GluonTS.md` | 2564 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.pidev_vs_claude_code_comparison.md` | 1930 | 75% | Nearly complete |
| `website/docs/blog/posts/draft.article.2026.Ribeiro_et_al.Why_Should_I_Trust_You.md` | 629 | 60% | Needs final polish |
| `website/docs/blog/posts/draft.how_to.Apple_Container.md` | 660 | 60% | Needs final polish |
| `website/docs/blog/posts/draft.how_to.Claude_skills.md` | 917 | 60% | Needs final polish |
| `website/docs/blog/posts/draft.how_to.Use_Local_LLMs_On_Mac.md` | 925 | 60% | Needs final polish |
| `website/docs/blog/posts/draft.shortcuts.GitHub_CLI.md` | 902 | 60% | Needs final polish |
| `website/docs/blog/posts/draft.how_to.Automate_Coding_with_LLM.md` | 1748 | 55% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.how_to.Compress_LLM_in_out_tokens.md` | 2084 | 55% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.how_to.Read_other_people_code.md` | 1235 | 55% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.how_to.Use_Claude_Code.md` | 1872 | 55% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.in_30_mins.helpers_caching.md` | 1599 | 55% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.in_30_mins.helpers_hllm_decorator.md` | 1525 | 55% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.TIL.Apple_container_running_notebook.md` | 714 | 40% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.Writing_Books_For_Humans_and_AI.md` | 470 | 40% | Needs refinement |
| `website/docs/blog/posts/draft.how_to.latex_vs_typst_for_typsetting.md` | 483 | 40% | Needs refinement |
| `website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md` | 345 | 30% | Add structure |
| `website/docs/blog/posts/draft.GWS.md` | 118 | 20% | Needs more detail |
| `website/docs/blog/posts/draft.debug.md` | 109 | 20% | Needs more detail |
| `website/docs/blog/posts/draft.how_to.Claude_Artifacts.md` | 225 | 20% | Needs more detail |
| `website/docs/blog/posts/draft.how_to.Github_Copilot_Review.md` | 110 | 20% | Needs more detail |
| `website/docs/blog/posts/draft.how_to.Produce_professional_images.md` | 229 | 20% | Needs more detail |
| `website/docs/blog/posts/draft.in_5_mins.helpers_cc.md` | 341 | 20% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.LLM_issues.md` | 76 | 10% | Add structure |
| `website/docs/blog/posts/draft.My_AI_Policy.md` | 120 | 10% | Add structure |
| `website/docs/blog/posts/draft.Reducing_hllm_cli_import_time.md` | 61 | 10% | Add structure |
| `website/docs/blog/posts/draft.blog_template.md` | 22 | 10% | Add structure |
| `website/docs/blog/posts/draft.carrer_advice.md` | 58 | 10% | Add structure |
| `website/docs/blog/posts/draft.hermes.md` | 29 | 10% | Add structure |
| `website/docs/blog/posts/draft.hiring_is_broken.md` | 250 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.AI_Coding_Assistant.md` | 53 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Apply_Coding_AI_to_ML_Data_Science.md` | 267 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Claude_Code_and_tmux.md` | 19 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Claude_powerups.md` | 203 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Codebase_local_kg.md` | 246 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Conventional_Commits.md` | 31 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Create_Hook_To_Run_Ruff_In_Claude_Code.md` | 82 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Merge_PRs.md` | 47 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.Use_Claude_Code_Workflows.md` | 286 | 10% | Remove TODO/WIP marks |
| `website/docs/blog/posts/draft.how_to.Use_tiny_docker_template.md` | 20 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.VS_Code_Quick_Fix.md` | 105 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.VS_Code_and_containers.md` | 58 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.branch_copy.md` | 4 | 10% | Add structure |
| `website/docs/blog/posts/draft.how_to.format_markdown.md` | 81 | 10% | Add structure |
| `website/docs/blog/posts/draft.ideas.Deterministic_skills.md` | 91 | 10% | Add structure |
| `website/docs/blog/posts/draft.in_30_mins.helpers_typesetting_system.md` | 29 | 10% | Add structure |

Total: 56 draft blogs

# Publishing Checklist

- Create
  ```bash
  claude> /blog.create_from_notes XYZ
  ```

- Set the target
  ```bash
  FILE="..."
  echo "Processing $FILE ..."
  MODEL="--model deepseek/deepseek-v4-flash"
  MODEL=""
  ```

- Make sure there are no TODOs
  ```bash
  > cc -p "/coding.todoai_gp $FILE"
  ```

- Detect and remove AI slop, if any
  ```bash
  > cc -p "/blog.humanize $FILE"
  ```

- Add links to rest of the blogs
  ```bash
  > cc -p "/blog.add_links $FILE"
  ```

- To lint the text use
  ```
  > website/format_blog.sh <FILE>
  ```

- Render
  ```
  > render_images.py -i website/docs/blog/posts/$FILE
  > git add ...
  ```

- Check how it's rendered
  ```bash
  > open_md.py --input website/docs/blog/posts/how_to.Render_md_from_terminal.md --mode github
  ```

- Mark ready for publishing
  ```bash
  > website/mark_blog_as_ready.py --file $FILE
  ```

- Preview the website
  ```bash
  > website/preview_website.sh
  ```

- Fix all the problematic blogs, if any
  ```
  > cc -p "Run website/preview_website.sh and fix the problems following .claude/skills/blog.rules.md"
  ```

- Publish the website
  ```bash
  > website/publish_website.sh
  ```

- Update the readme:
  ```bash
  > cc -p "Execute website/prompt.update_README_blog.md"
  ```
