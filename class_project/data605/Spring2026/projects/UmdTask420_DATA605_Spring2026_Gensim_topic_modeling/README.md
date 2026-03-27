# Project Objective

The goal of the project is to build a topic modeling system that can automatically identify and categorize topics from a collection of news articles. Students will optimize the model to accurately detect and label these topics using LDA, while evaluating the coherence and relevance of the topics generated.

# Dataset Chosen 

Selected dataset is the [BBC News Archive](https://www.kaggle.com/datasets/hgultekin/bbcnewsarchive) dataset from Kaggle. The dataset contains 2225 documents from the BBC news website corresponding to stories in five topical areas from 2004-2005.

# Tasks 
High level tasks include:
1. Creating a Python virtual environment 
2. Loading the dataset and performing initial data exploration 
3. Adding the dataset cleaning pipeline 
4. Adding the topic modeling pipeline and saving the topics as well as the model 
5. Analyzing the results 
6. Creating visualizations of the result 
7. Creating the docker image and containerising the application once everything works locally 
8. Final testing and reporting 

# Project Structure 
The entire project is structured as follows for now: 
- data: contains raw and processed 
- notebooks: includes topic_modeling and data_exploration Jupyter notebooks
- scripts: includes scripts for preprocessing, model training, evaluation, etc. 
- models: includes the final LDA model 
- outputs: includes the result and topics file 
- requirements.txt - python packages to be installed in the virtual environment 
- Dockerfile - Docker file 
- README.md - description file 


