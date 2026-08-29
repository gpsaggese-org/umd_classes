# [ ] Step 1: create script
Create a script class_scripts/gen_book_chapter.py that converts a file with slides in
.smd format into a book in terms of a md, tex, or typst output using LLM

Use
--mode springer_latex to generate a latex text using the prompt
/Users/saggese/src/notes1/book_proposals/prompt.create_latex_book_chap_from_lesson_slides.md

--mode typst to generate typst file using the prompt 
/Users/saggese/src/notes1/book_proposals/prompt.create_typst_book_chap_from_lesson_slides.md

copy the prompts in class_scripts/prompt.generate_latex_book_chapter.md, ...

--mode md to generate a markdown text

The interface is similar to class_scripts/gen_lecture_commentary.py

  input                 Lecture specification: 'data605/08.1', 'msml610/08.1', or file
                        path 'msml610/lectures_source/Lesson10.2-Name.smd'

options:
  -h, --help            show this help message and exit
  --dry_run             Only print the commands that would be executed without running
                        them (default: False)
  --no_incremental      Force regeneration of intermediate files even if they already
                        exist (by default, steps are skipped if their output already
                        exists) (default: False)
  --llm_backend {hllm,hllm_cli}
                        LLM backend to use for slide commentary generation: 'hllm'
                        (default) feeds the slide's images to the LLM as multi-modal
                        context, 'hllm_cli' is text-only
  --open_pdf            Open the generated PDF in Skim (default: False)

Follow the structure of the script of
class_scripts/gen_lecture_commentary.py which uses a prompt like
  class_scripts/prompt.generate_lecture_commentary.md
and factor out common code if possible

# [ ] Step 2: Factor out common part of the prompts
- We want to avoid redundancy
