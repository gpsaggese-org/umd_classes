When running gen_lecture_commentary.py book_springer 02.1
- Run git add on the md file generated
- Generalize the --no_incremental for also generating the PNG files
- Generate also an html version of the PDF output
- Add an option --use_figure_border to generate a border around
  the

  </center>
  # 2 / 30: Why Traditional ML Falls Short
  </center>
  <center>
  ![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides002.png){width=80%}
  </center>

using a Latex directive like

\begin{center}
\fbox{\includegraphics[width=0.8\linewidth]{book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides002.png}}
\end{center}

that includes both the title and the picture

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
