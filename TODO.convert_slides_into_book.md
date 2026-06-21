- [x] Create a map from book.from_corr_to_decision/book_map.md

class_scripts/create_book_toc_from_slides.py --max_number 2 --max_level 2

- [ ] Add comments to README

# The old flow
`./class_scripts/gen_book_chapter.py`
`./class_scripts/generate_book_chapter.py`

The output looks like 
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/data605/book/Lesson01.1-Intro.book_chapter.pdf

# The new flow 

- The style is like:
  vi msml610/book/aima_style.typ

TODO(gp): Improve the figure handling

Generate the text from the slides
```
claude> msml610/book/prompt.slides_to_text.txt
```

TODO(gp): Improve the prompt

```
> render_images.py -i msml610/book/Lesson06.2-Using_Bayesian_Networks.typ
> typst compile --root . msml610/book/aima_style_example.typ && open msml610/book/aima_style_example.pdf
> typst compile --root . msml610/book/Lesson06.2-Using_Bayesian_Networks.typ && open msml610/book/Lesson06.2-Using_Bayesian_Networks.pdf
```
