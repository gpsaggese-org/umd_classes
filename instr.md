In ./helpers_root/dev_scripts_helpers/documentation/preprocess_notes.py add
a transform that converts links between ! into text that resembles a link
(blue with underlying) using 

From
[ELMS](https://umd.instructure.com/courses/1391619/pages/homepage)

to


[\textcolor{blue}{\underline{ELMS}}](https://umd.instructure.com/courses/1391619/pages/homepage)

From

- From https://gpsaggese.github.io/blog/my-ai-policy/

to

- From [\textcolor{blue}{\underline{https://gpsaggese.github.io/blog/my-ai-policy/}}](https://www.linkedin.com/in/gpsaggese/)

Use msml610/lectures_source/Lesson00-Class.smd to find examples
