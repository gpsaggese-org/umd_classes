# DataPrep Tutorial
This project demonstrates how to use DataPrep (Python) for data analysis, specifically to predict the California Housing Dataset target variable (MedHouseVal)

# Workflow

From the directory, build the docker image 
```bash
  > ./docker_build.sh
  ```
Open Jupyter Lab 
```bash
  > ./docker_jupyter.sh -p 8888
  ```

After opening Jupyter in a browser, running the following notebooks (.ipynb)

1. DataPrep.API
- Introduces basic DataPrep uses and documentation
- Shows how to use get_report() to generate data summary
- Shows how to clean data and plot using dataprep


2. DataPrep.example
- loads California Housing Data
- exploratory analyses using Dataprep summary visualizations
- feature engineering for strong model performance
- LinearRegression model trained and evaluated
- More feature engineering according to data spreads as shown in DataPrep visualizations
- LinearRegression 2nd model (attempt higher accuracy)
- RandomForest model deployment and evaluation
- Compare and contrast model performance
