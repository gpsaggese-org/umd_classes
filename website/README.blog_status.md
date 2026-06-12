# Blog Posts

- This document tracks the work on the blogs
- Blogs are ranked from _most ready_ (near-publishable) to _least ready_ (raw
  scratchpad).
  - Criteria: front matter completeness, TL;DR quality, content structure, and polish.

# Published Blogs

- To find the ones that are already published
  ```
  > \grep -i "draft:" website/docs/blog/posts/*.md | grep -i false
  website/docs/blog/posts/how_to.Compare_LLM_models.md:draft: false
  website/docs/blog/posts/how_to.Connect_Claude_Code_to_Gmail.md:draft: false
  website/docs/blog/posts/in_30_mins.helpers_llm_cli.md:draft: false
  ...
  ```

- To extract dates and paths use:
  ```
  > website/find_published_blogs.sh
  ```

- The published ones are:
  - 2026-06-09: `website/docs/blog/posts/how_to.Compare_LLM_models.md`
  - 2026-05-30: `website/docs/blog/posts/in_30_mins.helpers_llm_cli.md`
  - 2026-04-19: `website/docs/blog/posts/in_30_mins.simonw_llm_cli.md`
  - 2026-03-29: `website/docs/blog/posts/in_30_mins.mdm_unified_markdown_manager.md`
  - 2026-03-21: `website/docs/blog/posts/in_30_mins.Python_Code_Coverage.md`
  - 2026-03-18: `website/docs/blog/posts/in_60_mins.CausalML.md`
  - 2026-03-15: `website/docs/blog/posts/in_60_mins.BambooAI.md`
  - 2026-03-03: `website/docs/blog/posts/in_60_mins.TorchRL_MAC.md`
  - 2026-02-28: `website/docs/blog/posts/how_to.Connect_Claude_Code_to_Gmail.md`
  - 2026-02-21: `website/docs/blog/posts/in_60_mins.Tensorflow.md`
  - 2026-02-21: `website/docs/blog/posts/in_60_mins.AutoGen.md`
  - 2026-02-14: `website/docs/blog/posts/in_30_mins.uv.md`
  - 2026-02-14: `website/docs/blog/posts/in_30_mins.Python_Packaging.md`
  - 2026-02-10: `website/docs/blog/posts/in_30_mins.ripgrep.md`
  - 2026-02-06: `website/docs/blog/posts/Welcome_to_Our_Blog.md`

# Draft Blogs

## High-priority

- `website/docs/blog/posts/draft.how_to.Use_Claude_Code_with_Openrouter.md`
- `website/docs/blog/posts/draft.how_to.Use_OpenRouter.md`
- `website/docs/blog/posts/draft.how_to.Count_cost.md`
- `website/docs/blog/posts/draft.how_to.LLM_effort.md`

## Tier 1: Ready — Well-structured, near-publishable

- `website/docs/blog/posts/Intro_to_Bayesian_Optimization.md`
  - Complete post, good TL;DR, well-structured with code examples and references. Small issue: marked `draft: true` but could publish.
- `website/docs/blog/posts/Ax_Multi_Objective_Optimization_On_Marketing_Campaigns.md`
  - Near-complete. Good content, code, references. Missing TL;DR (uses `# Summary` style intro).
- `website/docs/blog/posts/draft.in_60_mins.GluonTS.md`
  - Very comprehensive. Only issue: `draft: True` (capital T) in front matter, minor formatting inconsistency.

## Tier 2: Good Content — Needs minor polish

- `website/docs/blog/posts/draft.in_60_mins.TorchRL_MAC.md`
  - Well-structured, good TL;DR, complete content. Draft-format ready for review.
- `website/docs/blog/posts/draft.pidev_vs_claude_code_comparison.md`
  - Complete comparison post with good TL;DR.
- `website/docs/blog/posts/draft.in_30_mins.pi_dev.md`
  - Comprehensive tutorial with examples. Ready after light editing.
- `website/docs/blog/posts/draft.how_to.Convert_PDF_to_Markdown.md`
  - Good content coverage. TL;DR now fixed to proper format.
- `website/docs/blog/posts/draft.how_to.Use_Claude.md`
  - Good outline with many sections. Needs content filled in empty sections.
- `website/docs/blog/posts/draft.how_to.Claude_skills.md`
  - Decent content about Claude Skills. Needs restructuring and summary.

## Tier 3: Partial — Needs significant work

- `website/docs/blog/posts/draft.how_to.Use_Claude_Code.md`
  - Has structure and some content, but reads like internal notes. Needs rewriting.
- `website/docs/blog/posts/draft.how_to.Claude_Code.md`
  - Very brief (42 lines). Just setup instructions.
- `website/docs/blog/posts/draft.how_to.Claude_Artifacts.md`
  - Short but coherent tutorial. Needs expansion and TL;DR.
- `website/docs/blog/posts/draft.how_to.Github_Copilot_Review.md`
  - Very brief (20 lines). Needs much more content.
- `website/docs/blog/posts/draft.how_to.Use_Claude_Code_Workflows.md`
  - Mixed content — some instructional, some raw notes.
- `website/docs/blog/posts/draft.how_to.Create_Hook_To_Run_Ruff_In_Claude_Code.md`
  - Minimal content (JSON config snippet only). TL;DR now fixed.
- `website/docs/blog/posts/draft.how_to.VS_Code_Quick_Fix.md`
  - Minimal content (JSON config snippet only). TL;DR now fixed.
- `website/docs/blog/posts/draft.how_to.VS_Code_and_containers.md`
  - Barely started — just two URLs.
- `website/docs/blog/posts/draft.Writing_Books_For_Humans_and_AI.md`
  - Has good guidelines but no front matter originally (added now). Needs TL;DR and structure.
- `website/docs/blog/posts/draft.GWS.md`
  - Rough notes with terminal output. TL;DR and front matter now added.

## Tier 4: Scratchpad — Raw notes, not yet a blog post

- `website/docs/blog/posts/draft.how_to.Compare_LLM_models.md`
  - Raw data tables with no narrative. Good reference data but not a blog post.
- `website/docs/blog/posts/draft.how_to.Use_Claude_Code_with_Openrouter.md`
  - Raw configuration notes and terminal output.
- `website/docs/blog/posts/draft.how_to.Use_Local_LLMs_On_Mac.md`
  - Raw terminal session output.
- `website/docs/blog/posts/draft.how_to.Use_OpenRouter.md`
  - Raw command snippets.
- `website/docs/blog/posts/draft.how_to.Count_cost.md`
  - Just two URLs.
- `website/docs/blog/posts/draft.how_to.format_markdown.md`
  - Just two URLs.
- `website/docs/blog/posts/draft.debug.md`
  - Scratchpad/debug notes.
- `website/docs/blog/posts/draft.blog_template.md`
  - Template file — not a blog post. TL;DR is boilerplate placeholder.

## Non-draft posts (published) with issues

- `website/docs/blog/posts/draft.how_to.LLM_effort.md`
  - Published but very short (~70 lines). Empty TL;DR (now fixed).
- `website/docs/blog/posts/in_30_mins.Python_Code_Coverage.md`
  - Published. Had 4 `TODO(ai_gp)` comments — now resolved.
