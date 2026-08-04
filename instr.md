Create a script called class_scripts/publish_class_links.py

--dir class/book (e.g., data605)
--out_file ...html

that creates an html page with links for each lesson in DIR 
(e.g., ~/src/umd_classes2/data605/lectures_source/Lesson01.1-Intro.txt)

to
1) Their PDF
~/src/umd_classes2/data605/lectures_pdf/Lesson01.1-Intro.pdf

2) The lectures commentary (html and pdf)

~/src/umd_classes2/data605/lectures_commentary/Lesson01.1-Intro.book_chapter.html
~/src/umd_classes2/data605/lectures_commentary/Lesson01.1-Intro.book_chapter.pdf

3) Lesson recap
data605/lectures_recap/Lesson01.1-Intro.recap.md

If there are missing files, report an error and break unless
the option --do_not_fail_on_warnings is specified

# Conventions
- When writing code you must always follow the instructions in
  `.claude/skills/coding.rules.md`
- When writing testing code you must always follow the instructions in
  `.claude/skills/testing.rules.md`

# Create a plan, if needed
- If the task is not perfectly clear
  - You MUST not perform it
  - Ask for clarifications
  - Create a `plan.md` in the same directory with 5 bullet points explaining what
    the plan is
