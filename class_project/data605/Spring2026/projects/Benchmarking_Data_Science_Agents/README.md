# Benchmarking Data Science Agents: A Comparative Study

## Team Members
- Venkata Sripada
- Amulya Grace Bandlamudi

## Project Overview
This project builds a reproducible big data pipeline to collect, process, and 
compare publicly available AI benchmark datasets, including Chatbot Arena, 
MLE-Bench, SWE-bench, and GAIA. The goal is to understand how different 
benchmarks evaluate AI capabilities across dimensions such as human preference, 
ML engineering, code repair, and multi-step reasoning.

We collected 35,000+ rows of real benchmark data via the HuggingFace Datasets 
API and Kaggle API, processed 68,000+ rows using a DuckDB-powered analytical 
pipeline, and performed clustering, win rate analysis, and capability gap 
analysis across 1,274 agents. The project uses PyArrow for columnar storage, 
DuckDB for zero-copy SQL analytics, LangGraph for pipeline orchestration, and 
a Gemini/Claude LLM for automated interpretation of results.

The pipeline produces a unified agent × benchmark matrix, 6 visualizations, 
and a comparative research report examining how benchmark design choices affect 
what AI capabilities are measured and how agents are ranked.

## Objectives
- Collect benchmark leaderboard data
- Analyze benchmark structure and evaluation metrics
- Compare performance across different AI agents
- Perform clustering and correlation analysis on benchmark results
- Visualize benchmark differences and capability gaps
- Produce a final research report

## Tools and Technologies
- Python
- Pandas
- NumPy
- Matplotlib / Seaborn
- Scikit-learn
- Jupyter Notebook
- (Optional) PySpark for large-scale data processing

## Methodology
1. Data collection from benchmark leaderboards
2. Data cleaning and dataset integration
3. Exploratory data analysis
4. Statistical analysis and correlation analysis      
5. Clustering benchmarks and agent performance
6. Visualization and interpretation of results
7. Final analysis.

## Expected Outcome
The project aims to identify differences between data science benchmarks and determine which benchmarks better represent real-world data science tasks. We expect to find capability gaps where some agents perform well on coding tasks but struggle with multi-step reasoning and workflow-based tasks.

## Repository Structure

```
Benchmarking_Data_Science_Agents/
│
├── README.md          # Project overview and instructions
├── data/              # Collected benchmark datasets
├── notebooks/         # Jupyter notebooks for analysis
├── src/               # Python scripts for data processing and analysis
├── results/           # Output files, plots, and tables
├── report/            # Final report and documentation
└── references/        # Papers and benchmark documentation
```
