#!/bin/bash -e
# > ls -1 MSML610/Lesson*
FILES="
MSML610/Lesson00-Class.txt
MSML610/Lesson01-Intro.txt
MSML610/Lesson02-Techniques.txt
MSML610/Lesson03-Knowledge_representation.txt
MSML610/Lesson04-Models.txt
MSML610/Lesson05-Theories.txt
MSML610/Lesson06-Bayesian_statistics.txt
MSML610/Lesson07-Probabilistic_programming.txt
MSML610/Lesson08-Reasoning_over_time.txt
MSML610/Lesson09-Causal_inference.txt
MSML610/Lesson10-Timeseries_forecasting.txt
MSML610/Lesson11-Probabilistic_deep_learning.txt
MSML610/Lesson12-Reinforcement_learning.txt
MSML610/Lesson91.Refresher_probability.txt
MSML610/Lesson92.Refresher_probability_distributions.txt
MSML610/Lesson93.Refresher_linear_algebra.txt
MSML610/Lesson94.Refresher_information_theory.txt
MSML610/Lesson95.Refresher_game_theory.txt
MSML610/Lesson95.Refresher_numerical_optimization.txt
MSML610/Lesson96.Refresher_stochastic_processes.txt
"

#FILES="
#MSML610/Lesson07-Probabilistic_programming.txt
#"

DST_DIR="pdfs"
rm -rf $DST_DIR || true
mkdir $DST_DIR

for FILE in $FILES; do
    echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    rm -rf tmp* figs*
    echo $FILE
    cmd="notes_to_pdf.py --input $FILE --output tmp.pdf --type slides --toc_type navigation --skip_action open"
    echo $cmd
    eval $cmd
    #
    ls $DST_DIR
    NEW_FILE=$(echo $FILE | sed 's/\.txt$/.pdf/')
    NEW_FILE=$(basename $NEW_FILE)
    cmd="mv tmp.pdf $DST_DIR/$NEW_FILE"
    echo $cmd
    eval $cmd
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
done

# cp -rf $DST_DIR/*.pdf ~/src/umd_data605_1/MSML610/lectures
