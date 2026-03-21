# Causal Analysis of Financial Tradability - Docker Edition

## Overview

Comprehensive framework for analyzing the causal relationship between trading horizons and market predictability in cryptocurrency markets.

project objectives to be covered:
- Data collection and preprocessing (Binance API with fallback to synthetic data)
- Feature engineering (25+ technical indicators)
- Predictability analysis across multiple horizons
- Hit rate and PnL analysis with transaction costs
- Causal inference methods (elasticity, decay models, instrumental variables)
- Market regime detection (trending, mean-reverting, volatile)
- Monte Carlo simulation (10,000 scenarios)
- Walk-forward validation (out-of-sample testing)
- Cross-market correlation analysis
- Bonus: RL environment preparation

## Architecture

Two-file implementation:
- financial_trading_utils.py: Single module with all utility functions 
- master.ipynb: Main analysis notebook with 13 analysis steps

No separate Docker utility files - all functions in financial_trading_utils.py.

## Installation and Setup

### Step 1: Prepare Files

Create project directory with:
- financial_trading_utils.py (all functions)
- master.ipynb (main analysis)
- requirements_docker.txt (dependencies)
- Dockerfile (provided)
- docker_*.sh scripts (provided)
- docker_name.sh (configuration)

### Step 2: Dependency Management

This project uses `uv` for efficient Python dependency management within the Docker container. The system works as follows:

- **`requirements.in`** — Lists top-level package dependencies
- **`requirements.txt`** — Auto-generated pinned versions for reproducibility

The Docker container comes with all dependencies pre-compiled and synced. If you need to update dependencies manually:

```bash
# Compile top-level packages into pinned requirements
uv pip compile requirements.in -o requirements.txt

# Sync the environment with the compiled list
uv pip sync requirements.txt
```

### Step 3: Configure Docker

Edit docker_name.sh:
```bash
nano docker_name.sh
```

Change IMAGE_NAME to your project name.

### Step 4: Prepare Dependencies

Rename file:
```bash
cp requirements_docker.txt requirements.txt
```

### Step 5: Build Docker Image

```bash
bash docker_build.sh
```

First build: 2-3 minutes

### Step 6: Start Jupyter Lab

```bash
bash docker_jupyter.sh
```

Access at http://localhost:8888

### Step 7: Run Analysis

Open master.ipynb and run cells 1-13 sequentially.

Analysis completes in 5-10 minutes.

## Contents of financial_trading_utils.py

Single module with all functions organized by category:

### Data Collection
- fetch_binance_klines(): Fetch OHLCV from Binance API
- generate_synthetic_ohlcv(): Create synthetic data for testing

### Data Preprocessing
- preprocess_data(): Complete cleaning pipeline
- synchronize_dataframes(): Multi-asset synchronization

### Feature Engineering
- create_all_features(): 25+ technical indicators
- create_multi_horizon_targets(): Multi-horizon targets

### Predictability Analysis
- analyze_predictability_by_horizon(): Train models, evaluate accuracy
- Models: Logistic Regression, Random Forest

### Hit Rate and PnL
- calculate_hit_rate_requirement(): Minimum win rate for profitability
- analyze_pnl_by_horizon(): Expected PnL analysis

### Causal Inference
- analyze_horizon_causal_effect(): Causal relationship analysis
- estimate_instrumental_variables(): IV identification

### Market Analysis
- detect_market_regimes(): Regime classification
- analyze_with_transaction_costs(): Cost impact
- calculate_cross_market_correlation(): Multi-asset analysis

### Simulation
- run_monte_carlo_simulation(): 10,000 outcome scenarios

### Validation
- perform_walk_forward_validation(): Out-of-sample testing

### Utilities
- get_summary_statistics(): Data summary
- export_results(): CSV export

## Contents of master.ipynb

13 analysis sections:

1. Setup - Load utilities
2. Data Collection - Fetch OHLCV data
3. Preprocessing - Clean and validate
4. Feature Engineering - Create 25+ indicators
5. Predictability Analysis - Train models on 4 horizons
6. Hit Rate and PnL - Profitability analysis
7. Causal Inference - Horizon-predictability relationship
8. Market Regimes - Detect trending/mean-reverting/volatile
9. Transaction Costs - Impact analysis
10. Monte Carlo - 10,000 simulation scenarios
11. Visualizations - 6 comprehensive plots
12. Walk-Forward Validation - Out-of-sample testing
13. Summary and Export - Results to CSV


## Output Files

- predictability_results.csv: Accuracy by horizon
- pnl_analysis.csv: Profitability metrics
- features_dataset.csv: Complete feature matrix
- market_regimes.csv: Regime classifications
- walk_forward_validation.csv: Out-of-sample results
- comprehensive_analysis.png: 6-subplot visualization
- monte_carlo_analysis.png: MC distribution and Q-Q plot

## Docker Commands


## Customization

Edit master.ipynb cells:
- Change date range in cell 2
- Use different symbol (ETHUSDT, etc.)
- Adjust horizons in cell 4
- Modify PnL parameters in cell 5
- Change MC parameters in cell 9

No Docker rebuild needed for code changes.

## Key Features

All project objectives implemented:
- Complete data pipeline with API fallback
- 25+ technical indicators covering all categories
- Multi-horizon predictability testing
- Causal analysis with elasticity and decay models
- Instrument variable identification
- Market regime detection (4 categories)
- Transaction cost modeling
- Monte Carlo with VaR/CVaR metrics
- Walk-forward validation
- Cross-market correlation framework
- Bonus: RL environment preparation

## Troubleshooting

### Port 8888 in use
```bash
bash docker_jupyter.sh -p 8889
```

### API connection failed
Notebook automatically generates synthetic data.

### Docker build fails
Check Docker is running and disk space available.

### Import errors in notebook
Ensure financial_trading_utils.py is in same directory as master.ipynb.

## References

Project addresses research from:
- Easley & O'Hara (2020) - Microstructure effects on predictability
- Arnott et al. (2019) - Horizon-dependent strategy performance
- Krauss & Do (2022) - Deep learning for price prediction
- Ritter et al. (2021) - Hit rate and PnL relationships

Data: [Kaggle Cryptocurrency Dataset](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data) (free, no authentication)

## Next Steps

After running:
1. Review CSV results
2. Examine PNG visualizations
3. Modify parameters for sensitivity analysis
4. Test on different assets
5. Extend with custom indicators/models
