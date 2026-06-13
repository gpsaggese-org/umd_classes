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

- To format use:
  ```
  > website/format_blog.sh <FILE>
  ```
  which wraps something like:
  ```
  > prettier --prose-wrap always --print-width 80 --tab-width 4 -w $FILE
  ```

- Checklist for publishing (from `website/blog_checklist.sh`)
  ```
  claude> /blog.create_from_notes XYZ
  claude> /coding.todoai_gp XYZ
  claude> /blog.humanize XYZ
  claude> /blog.add_links XYZ
  ```

- Render
  ```
  > render_images.py -i website/docs/blog/posts/$FILE
  > git add ...
  ```

- To publish use the script
  ```
  > website/publish_blog.py ...
  ```

# Draft Blogs

## High-priority

- `website/docs/blog/posts/draft.in_30_mins.helpers_caching.md`
  - `./helpers_root/docs/tools/helpers/all.hcache_simple.explanation.md`

- `website/docs/blog/posts/draft.in_5_mins.helpers_cc.md`

- helpers/hcheck_types.py

- `website/docs/blog/posts/draft.in_5_mins.helpers_render_images.md`
  - `./helpers_root/dev_scripts_helpers/documentation/render_images.py`
  - `./helpers_root/dev_scripts_helpers/documentation/test/test_render_images.py`
  - `docs/tools/documentation_toolchain/all.render_images.explanation.md`

- `helpers_root/docs/documentation_meta/all.architecture_diagrams.explanation.md`
- `helpers_root/docs/documentation_meta/all.diataxis.explanation.md`
- `helpers_root/docs/documentation_meta/all.gdocs.how_to_guide.md`
- `helpers_root/docs/documentation_meta/all.google_technical_writing.how_to_guide.md`
- `helpers_root/docs/documentation_meta/all.markdown_tools.explanation.md`
- helpers_root/docs/documentation_meta/all.plotting_in_latex.how_to_guide.md
- helpers_root/docs/documentation_meta/all.writing_docs.how_to_guide.md
- helpers_root/dev_scripts_helpers/system_tools/README.md
- `./website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md`

- Tier 1 blogs

## Tier 1: Ready — Well-structured, near-publishable

- `website/docs/blog/posts/draft.Intro_to_Bayesian_Optimization.md`
  - Complete post (266 lines), good TL;DR, well-structured with code examples
    and references. Marked `draft: true` but could publish.
- `website/docs/blog/posts/draft.Ax_Multi_Objective_Optimization_On_Marketing_Campaigns.md`
  - Near-complete (287 lines). Good content, code, references. Missing TL;DR
    (uses `# Summary` style intro).
- `website/docs/blog/posts/draft.in_60_mins.GluonTS.md`
  - Very comprehensive (476 lines). Only issue: `draft: True` (capital T) in
    front matter, minor formatting inconsistency.

## Tier 2: Good Content — Needs minor polish

- `website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md`
  - Well-structured (238 lines), good content on Markdown viewers for macOS.
    Missing front matter (no `draft:`, `title:`, `date:` fields).
- `website/docs/blog/posts/draft.pidev_vs_claude_code_comparison.md`
  - Complete comparison post (421 lines) with good TL;DR.
- `website/docs/blog/posts/draft.in_30_mins.pi_dev.md`
  - Comprehensive tutorial (390 lines) with examples. Ready after light editing.
- `website/docs/blog/posts/draft.how_to.Convert_PDF_to_Markdown.md`
  - Good content coverage (446 lines). TL;DR fixed to proper format.
- `website/docs/blog/posts/draft.how_to.Claude_skills.md`
  - Decent content (188 lines) about Claude Skills. Needs restructuring and summary.

## Tier 3: Partial — Needs significant work

- `website/docs/blog/posts/draft.how_to.Use_Claude_Code.md`
  - Has structure and some content (443 lines), but reads like internal notes.
    Needs rewriting.
- `website/docs/blog/posts/draft.how_to.Apple_Container.md`
  - Has some content (109 lines) but reads like raw command notes and URLs.
    Needs structuring into a tutorial.
- `website/docs/blog/posts/draft.how_to.Claude_Artifacts.md`
  - Short but coherent tutorial (56 lines). Needs expansion and TL;DR.
- `website/docs/blog/posts/draft.how_to.Github_Copilot_Review.md`
  - Very brief (32 lines). Needs much more content.
- `website/docs/blog/posts/draft.how_to.Use_Claude_Code_Workflows.md`
  - Mixed content (79 lines) — some instructional, some raw notes.
- `website/docs/blog/posts/draft.how_to.Use_Local_LLMs_On_Mac.md`
  - Expanded to 203 lines with full front matter (date, description, categories).
    Covers installation, model benchmarking, and CLI usage. Still reads like
    command notes and terminal output — needs narrative rewriting.
- `website/docs/blog/posts/draft.how_to.Create_Hook_To_Run_Ruff_In_Claude_Code.md`
  - Minimal content (33 lines, JSON config snippet only). TL;DR fixed.
- `website/docs/blog/posts/draft.how_to.VS_Code_Quick_Fix.md`
  - Minimal content (46 lines, JSON config snippet only). TL;DR fixed.
- `website/docs/blog/posts/draft.how_to.VS_Code_and_containers.md`
  - Barely started (21 lines) — just two URLs.
- `website/docs/blog/posts/draft.Writing_Books_For_Humans_and_AI.md`
  - Has good guidelines (98 lines) but no front matter originally (added now).
    Needs TL;DR and structure.
- `website/docs/blog/posts/draft.GWS.md`
  - Rough notes (36 lines) with terminal output. TL;DR and front matter added.
- `website/docs/blog/posts/draft.in_5_mins.helpers_cc_wrapper.md`
  - Decent structure (73 lines) but has TODO comments. Needs cleanup and links.

## Tier 4: Scratchpad — Raw notes, not yet a blog post

- `website/docs/blog/posts/draft.how_to.format_markdown.md`
  - Just two URLs.
- `website/docs/blog/posts/draft.debug.md`
  - Has front matter (title, date, description) but content is still disjointed
    command snippets and scratch notes. Not yet a blog post.
- `website/docs/blog/posts/draft.blog_template.md`
  - Template file — not a blog post. TL;DR is boilerplate placeholder.
- `website/docs/blog/posts/draft.how_to.AI_Coding_Assistant.md`
  - Raw unordered list of AI coding assistant tools (6 lines). No narrative.
- `website/docs/blog/posts/draft.how_to.Claude_Code_and_tmux.md`
  - Single URL (1 line). Barely started.
- `website/docs/blog/posts/draft.carrer_advice.md`
  - Raw notes (15 lines). Not yet a blog post.
- `website/docs/blog/posts/draft.hiring_is_broken.md`
  - Raw notes (34 lines). Not yet a blog post.

## Published posts with remaining TODOs

- `website/docs/blog/posts/in_30_mins.Python_Code_Coverage.md`
  - Published. Has 1 remaining `TODO(ai_gp)` comment ("This seems to be
    malformed").
