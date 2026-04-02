# HuggingFace Text Classification Model

## Description

HuggingFace is an open-source platform that provides ready-to-use, state-of-the-art language models along with the tools needed to fine-tune, evaluate, and deploy them for any natural language task, without needing to build models from scratch.

This project builds a News Article Classification Pipeline on top of HuggingFace. Given a raw news article, the system ingests data from public news datasets (AG News, BBC News), fine-tunes transformer models, covering BERT, DistilBERT, and RoBERTa for multi-class topic classification, and serves predictions through a live inference endpoint and dashboard.

The full stack uses HuggingFace Transformers and Datasets for tokenization and fine-tuning, PyTorch as the training backend, Scikit-learn for evaluation metrics, FastAPI for inference serving, and Streamlit for the prediction dashboard.

## Project Specs: 
https://github.com/gpsaggese/gpsaggese.github.io/blob/master/class_project/data605/Spring2026/projects_descriptions/HuggingFace_Project_Description.md

**Authors**: @riyaapuri @stupatel17
**Assigned to**: @riyaapuri @stupatel17 @protocorn @gpsaggese