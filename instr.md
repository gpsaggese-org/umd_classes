When running 

notes_to_pdf.py --input=msml610/lectures_source/Lesson03.1-Knowledge_representation.txt --output=msml610/lectures/Lesson03.1-Knowledge_representation.pdf --type=slides --toc_type=navigation --debug_on_error --skip_action=cleanup_before --skip_action=cleanup_after --slides_engine typst --no_fail_on_warning

In 

/Users/saggese/src/umd_classes2/msml610/lectures/tmp.notes_to_pdf.render_image2.typ

I see

- #strong[Definition];: #emph[Knowledge Representation (KR)] is the

without colors, so colorize_bullet_points_in_slide doesn't seem to work

but the tests

pytest ./helpers_root/helpers/test/test_hmarkdown_coloring.py

are passing

