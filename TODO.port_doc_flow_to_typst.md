# Step 0:

- [x] Implement TODOs
- [x] Add pictures of screen with ./dev_scripts_helpers/system_tools/capture_iterm_command.py --command "(cd ~/src/umd_classes2/helpers_root; clear; glow TODO.convert_slides_into_book.md)" --output_file screenshot1.png
- [x] Refresh the README.blog.md
- [x] Convert to Python dev_scripts_helpers/documentation/open_md.sh
- [ ] Test dev_scripts_helpers/documentation/open_md.sh
- [ ] Finish website/docs/blog/posts/draft.how_to.Render_md_from_terminal.md

# Step 1: Document current system
helpers_root/dev_scripts_helpers/documentation/README.md
helpers_root/dev_scripts_helpers/documentation/README.notes_to_pdf.md

website/docs/blog/posts/draft.in_30_mins.helpers_typesetting_system.md
-> create blog

# Step 2: Document typst and slides

website/README.blog.md

website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md
- Create blog

website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.all_examples.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/polylux.hello_world.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.all_examples.typ
website/docs/blog/posts/draft.how_to.Use_typst_for_slides.md.mats/touying.hello_world.typ
website/docs/blog/posts/draft.how_to.latex_vs_typst_for_typsetting.md

# Step 3: Extend the flow and document it
dev_scripts_helpers/documentation/notes_to_pdf.py

notes_to_pdf.py --input=data605/lectures_source/Lesson01.1-Intro.txt --output=data605/lectures/Lesson01.1-Intro.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst

Cause: my typst path used container_type = "pandoc_only", which points at the bare pandoc/core:3.7 image. That image isn't built/pulled locally (only pandoc_texlive and pandoc_latex get auto-built), so the assert fails.

# Step 4: Reorg dev_scripts_helpers/documentation
- Too many files
