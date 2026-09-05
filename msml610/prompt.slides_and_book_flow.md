FILE=msml610/lectures_source/Lesson02.6-ML_Techniques_How_To_Do_Research.smd

- [ ] Apply review

/slides.review $FILE

Implement the high importance and the restructuring of the slides

- [ ] Add visuals and references

/slides.add_visuals $FILE
/slides.add_references $FILE

- [ ] Render

/slides.lint $FILE
/slides.fix_rendered_pdf $FILE
