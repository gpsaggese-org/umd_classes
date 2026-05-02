# YData-profiling Tutorial

This project demonstrates how to use YData-profiling for automated exploratory
data analysis and how profiling results can support a regression modeling
workflow.

The tutorial uses the Baltimore housing dataset. It shows how to generate data
profile reports, inspect data quality issues, clean the dataset, train a
regression model, and evaluate the model with RMSE and R-squared.

## Quick Start

From the project directory, build the Docker image:

```bash
./docker_build.sh
```

Start Jupyter Lab:

```bash
./docker_jupyter.sh
```

Then open Jupyter Lab in a browser and run the notebooks in this order:

1. `ydata_profiling.API.ipynb`
   - Introduces the basic YData-profiling API.
   - Shows how to create and export HTML profile reports.
   - Demonstrates the project wrapper functions.

2. `ydata_profiling.example.ipynb`
   - Loads the Baltimore housing dataset.
   - Generates an automated profiling report.
   - Cleans and prepares the dataset.
   - Trains a regression model.
   - Evaluates the model using RMSE and R-squared.

## Project Structure

```text
.
├── data/
│   └── baltim.csv
├── outputs/
│   ├── simple_demo_profile.html
│   ├── simple_demo_profile_from_wrapper.html
│   └── baltim_example_profile.html
├── src/
│   ├── run_profiling.py
│   └── ydata_profiling_utils.py
├── ydata_profiling.API.ipynb
├── ydata_profiling.example.ipynb
├── requirements.txt
├── Dockerfile
└── README.md
```

## Expected Outputs

Running the notebooks generates HTML profiling reports in the `outputs/`
directory.

The example notebook also trains a regression model to predict `PRICE` in the
Baltimore housing dataset and reports:

- RMSE
- R-squared

In the current run, the example model produced approximately:

```text
RMSE: 12.6307
R2: 0.6915
```

## Notes

YData-profiling is used before modeling to quickly inspect variable types,
missing values, distributions, correlations, and other data quality issues.
These insights guide the cleaning and feature preparation steps before model
training.