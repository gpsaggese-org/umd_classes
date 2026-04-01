# Darts — S&P 500 Market Direction Forecasting & Intelligent Sector Rotation

## Project Overview
This project uses Python, Pandas, and Darts to forecast S&P 500 index prices 
using macroeconomic indicators as external covariates and predicts which market 
sectors will outperform in the near future. It combines S&P 500 direction 
forecasting with an intelligent sector rotation recommender backed entirely by 
model predictions, historical correlations, and risk adjusted scores, not manual 
rules.

## Planned Workflow
1. Data collection (S&P 500 + 11 sector ETFs + 22 macro indicators via yfinance & FRED API)
2. Data preprocessing & exploratory data analysis
3. Feature engineering (technical indicators, calendar features, release-date-aware forward fill, holiday & FOMC event flags)
4. Model training — Baseline, Statistical (VARIMA), Probabilistic, ML models
5. Feature selection via SHAP values
6. Hyperparameter tuning via grid search
7. Ensemble modeling — Statistical ensemble + ML ensemble
8. Sector rotation recommendation engine
9. Library comparison (Darts vs Facebook Prophet vs Statsmodels)
10. External factor impact analysis (holidays, FOMC dates, CPI release dates)
11. Evaluation using MAE, RMSE, MAPE, sMAPE, and R²
12. Visualization — forecasts, SHAP plots, sector rotation dashboard, leaderboard

## Author
- GitHub: [@RushilJoshi07](https://github.com/RushilJoshi07)

## Issue
- [#453](https://github.com/gpsaggese/gpsaggese.github.io/issues/453)
