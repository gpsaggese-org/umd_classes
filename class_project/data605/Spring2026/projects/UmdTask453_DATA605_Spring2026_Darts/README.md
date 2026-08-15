# Darts — S&P 500 Market Direction Forecasting & Intelligent Sector Rotation

## Project Overview

This project uses Python Pandas and Darts to forecast S&P 500 index
prices using macroeconomic indicators as external covariates and
predicts which market sectors will outperform in the near future.
It combines S&P 500 direction forecasting with an intelligent sector
rotation recommender backed entirely by model predictions historical
correlations and risk adjusted scores — not manual rules.

## Key Results

| Metric | Value |
|--------|-------|
| Best validation MAPE | 0.65% (Stacking Ensemble) |
| Improvement over baseline | 65.8% vs NaiveSeasonal |
| In-regime direction accuracy | 76.6% (2023 walk forward windows) |
| Market regimes detected | 5 (automatic via silhouette score) |
| Weekly recommendations pre-computed | 339 (2018-2024, no look-ahead bias) |
| Models trained | 18 across 6 families |
| SHAP selected features | 7 from 46 candidates |

## Completed Workflow

1. Data collection — S&P 500 + 11 sector ETFs + 16 macro indicators
   via yfinance and FRED API. XLC reconstructed from 16 verified
   SPDR constituents for pre-launch 2018 period.
2. Data preprocessing and exploratory data analysis — business day
   alignment release-aware forward fill and 4 EDA visualizations.
3. Feature engineering — 46 features including technical indicators
   calendar features macro derived features and event flags for
   FOMC dates CPI releases and holiday adjacent days.
4. Model training — 18 models across 6 families: 4 baseline
   7 statistical 1 probabilistic 5 ML and 1 Prophet. Best single
   window result: LightGBM MAPE 1.12% Direction 93.1%.
5. Feature selection via SHAP values — two step process combining
   correlation filter at 0.95 threshold with SHAP importance at
   90% threshold. Selected 7 optimal features improving MAPE from
   1.10% to 0.95% and R2 from -0.14 to +0.21.
6. Hyperparameter tuning via Optuna Bayesian optimization —
   TPESampler with 20 trials per model. XGBoost improved by 63%
   from MAPE 1.88% to 0.70%.
7. Ensemble modeling — simple average weighted average and stacking
   with Ridge Regression meta model. Stacking achieves MAPE 0.65%
   — 7.09% improvement over best individual model.
8. Sector rotation engine — K-Means clustering with silhouette score
   automatically detected 5 market regimes. Five factor composite
   scoring with Ridge Regression weights generates weekly BUY
   NEUTRAL AVOID recommendations. Regime attribution analysis reveals
   how macro context drives different sector outcomes within the same
   regime. 339 weekly recommendations pre-computed with no
   look-ahead bias.
9. Library comparison — Darts vs Statsmodels vs Prophet evaluated
   on identical data. Darts NaiveSeasonal achieves best MAPE 1.94%
   in 0.01 seconds validating Darts as the primary library.
10. External factor impact analysis — FOMC dates CPI releases and
    holiday adjacent days analyzed across top 5 models. RandomForest
    73% worse on FOMC days. LightGBM 44% better on FOMC days
    validating event flag features.
11. Walk forward validation — 12 non-overlapping 30 day windows
    July 2023 to December 2024. In-regime 2023 windows achieve
    MAPE 2.78% and direction accuracy 76.6%. Out-of-distribution
    2024 AI boom windows show MAPE 17.7% validating the need for
    regime confidence scoring.
12. Docker setup — Dockerfile with build-essential gcc g++ for
    shap compilation. All dependencies pinned in requirements.txt
    including optuna 3.6.1. Docker build verified successful.

## Data Sources

| Source | Data | Period |
|--------|------|--------|
| Yahoo Finance | S&P 500 price | 2018-2024 |
| Yahoo Finance | 11 sector ETFs | 2018-2024 |
| Yahoo Finance | VIX TNX IRX OIL DXY | 2018-2024 |
| FRED API | CPI FED_RATE UNEMPLOYMENT and others | 2018-2024 |

## Setup and Installation

### Option 1 — Local Installation
```bash
# Clone the repository.
git clone https://github.com/gpsaggese/gpsaggese.github.io.git
cd gpsaggese.github.io/class_project/data605/Spring2026/projects/UmdTask453_DATA605_Spring2026_Darts

# Create virtual environment.
python -m venv venv
source venv/bin/activate

# Install dependencies.
pip install -r requirements.txt

# Set FRED API key.
export FRED_API_KEY=your_api_key_here

# Launch Jupyter.
jupyter lab darts.example.ipynb
```

### Option 2 — Docker
```bash
# Build Docker image.
docker build -t darts_project .

# Run container.
docker run -it -p 8888:8888 \
    -e FRED_API_KEY=your_api_key_here \
    -v $(pwd):/workspace \
    darts_project

# Inside container launch Jupyter.
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

## Requirements

- Python 3.12
- FRED API key (free at https://fred.stlouisfed.org/docs/api/api_key.html)
- Docker (optional)
- 8GB RAM recommended

## Author

- GitHub: [@RushilJoshi07](https://github.com/RushilJoshi07)

## Issue

- [#453](https://github.com/gpsaggese/gpsaggese.github.io/issues/453)