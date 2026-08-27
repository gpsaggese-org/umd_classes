# Topics

- Each lesson should be around 30 slides and correspond to a chapter of a book
```
> grep "^* " msml610/lectures_source/Lesson01.1-AI_and_Machine_Learning.txt | wc -l
```

Lesson00-Class.txt

// Shrink?
Lesson01.1-AI_and_Machine_Learning.txt (18)
Lesson01.2-The_Foundations_of_AI.txt (13)
Lesson01.3-Brief_History_of_AI.txt (26)

// Shrink?
Lesson02.1-A_Map_of_Machine_Learning.txt
Lesson02.2-ML_Paradigms.txt

// Keep
Lesson02.3-ML_Techniques_Input_Processing.txt
Lesson02.4-ML_Techniques_Model_Learning.txt
Lesson02.5-ML_Techniques_Model_Evaluation.txt
Lesson02.6-ML_Techniques_How_To_Do_Research.txt

Lesson03.1-Knowledge_representation.txt

// Move
Lesson04.1-Models.txt
Lesson04.2-Models.txt
Lesson04.3-Models.txt

## Learning Theory
Lesson05.1-Learning_Theory.txt
Lesson05.2-Overfitting.txt
Lesson05.3-Learn_Validation.txt

## Probabilistic ML
Lesson06.1-Bayesian_Networks.txt
Lesson06.2-Using_Bayesian_Networks.txt
Lesson07.1-Intro_to_Probabilistic_Programming.txt
Lesson07.2-Posterior_Based_Decisions.txt
Lesson07.3-Hierarchical_Models.txt
Lesson07.4-Generalized_Linear_Models.txt
Lesson07.5-Bayesian_Model_Comparison.txt

## Causal ML
Lesson08.1-Causal_AI_intro.txt
Lesson08.2-Causal_Networks.txt
Lesson08.3-Do_Calculus.txt

Lesson08.4.txt
Lesson08.5-Experimentation.txt

## Forecasting and Decision Making
Lesson09.1-Reasoning_over_time.txt
Lesson09.2-Hidden_Markov_Models.txt
Lesson09.3-Multi_Armed_Bandits.txt
Lesson09.7-Advanced_Bandits.txt
Lesson09.4-gh_Filter.txt
Lesson09.5-Kalman_Filter.txt
Lesson09.6-Dynamic_Bayesian_Networks.txt

Lesson10.1-Timeseries_forecasting.txt
Lesson10.2-Causal_Inference_for_Time_Series.txt
Lesson11.1-Decision_Making_with_Causal_Models.txt

// Move
Lesson11.2-Probabilistic_deep_learning.txt

// Move
Lesson12.1-Reinforcement_learning.txt

// Move
Lesson12.2-Causal_Discovery.txt

// ?
Lesson13.1-Explainability.txt

# Workflows

## Overview

Extract headers and create a comprehensive syllabus from all lecture materials using
the `for_loop_lessons.py` orchestration script.

## Slides

### Iterate on the Slides

- Generate slides when editing the source
  ```bash
  > gen_slides.py msml610/lectures_source/Lesson01.1-Intro.smd
  > gen_slides.py msml610/01.1 --daemon
  > gen_slides.py msml610/01.1 --daemon
  ```

- The file is generated in `lectures_pdf.tmp`

## Slides Commentary

### Generate for One Lecture
```
> gen_lecture_commentary.py msml610/01.1 --image_type jpg
```

### Generate for All Lectures

```
> for_loop_lessons.py --class data605 --action generate_lecture_commentary --lectures "01.1-02"

> publish_class_links.py --dir msml610 --out_file ./links.html --do_not_fail_on_warnings --use_master

> open book_springer/lecture_commentary/Lesson04.1_Knowledge_Representation.book_chapter.html
```


### Publish the lecture commentary on the website

website/update_class_links.sh


## Course Syllabus

### Generate Complete Course Syllabus

- Extract all lecture headers and create a consolidated syllabus:

  ```bash
  > cd /Users/saggese/src/umd_classes1
  > for_loop_lessons.py --class msml610 --action generate_toc
  ```

This generates:
- **Output file**: `msml610/all_tocs.md`
- **Content**: All lecture headers organized hierarchically (up to 5 levels deep)
- **Format**: Markdown with lecture structure preserved

### Generate Syllabus for Specific Lectures

- Extract headers from a subset of lectures using pattern matching:
  ```bash
  # Single lecture pattern
  > for_loop_lessons.py --class msml610 --lectures "01*" --action generate_toc

  # Multiple lecture patterns (colon-separated)
  > for_loop_lessons.py --class msml610 --lectures "01*:02*:03.1" --action generate_toc

  # Continuous range (inclusive)
  > for_loop_lessons.py --class msml610 --lectures "01.1-03.2" --action generate_toc
  ```

### Output Format

- The syllabus markdown file contains structured headers with proper indentation:
  ```markdown
  # Lesson01.1-Intro.txt

  ## Main Topic
  ### Subtopic 1
  #### Sub-subtopic
  ### Subtopic 2

  # Lesson01.2-Topic.txt

  ## Another Main Topic
  ...
  ```

- This provides a complete overview of the course curriculum and lecture structure
