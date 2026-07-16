Understand why running

lint_txt.py -i book_springer/book/Lesson02.01_From_Data_Science_To_Decision_Science.tex --action prettier -v DEBUG 2>&1 | tee log.txt

the following incorrect transformations are performed

From

```
% git_hash=f15bc6b9, timestamp=2026-07-15 14:41:12 EDT
%%%% Chapter file for Why Decisions, Not Predictions %%%%
% This chapter file can be compiled standalone or included in the root book.tex
```

to

```
% git_hash=f15bc6b9, timestamp=2026-07-15 14:41:12 EDT %%%% Chapter file for Why Decisions, Not Predictions %%%% % This chapter file can be compiled standalone or included in the root book.tex
```

From
```
% From: '* Why Traditional ML Falls Short'
\textbf{Why Traditional ML Falls Short}
```

to

```
% From: '* Why Traditional ML Falls Short' \textbf{Why Traditional ML Falls Short}
```
