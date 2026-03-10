# An Analysis of VC Predictive Power

## Description

- Rigorously test whether venture capitalists have genuine predictive power in identifying successful startups or if success is driven by other factors
- Use causal inference methods to separate correlation from causation in VC funding outcomes
- Investigate whether VC funding is a causal driver of success or merely correlated with pre-existing startup quality
- Control for confounders (market conditions, sector, timing, founder background) to isolate true VC predictive value
- Evaluate whether observed correlations reflect forward-looking information or survivorship bias and ex-post rationalization

## Project Objective

This project aims to rigorously test the hypothesis that venture capitalists (VCs) have meaningful predictive power in selecting startups that will outperform others. Using causal inference methods, we will separate correlation from causation to evaluate whether VC investment decisions truly contain forward-looking information, or if observed outcomes are simply the result of ex-post rationalizations and survivorship bias.

Key research questions:
1. Do startups funded by "top" VCs outperform similar startups that were not funded by them?
2. Is VC involvement a causal driver of success, or merely correlated with characteristics that already predicted success?
3. After controlling for confounders, does VC selection still predict long-term outcomes?

## Dataset Suggestions

- **Crunchbase**: Comprehensive startup funding database with detailed funding rounds, investor information, and startup exit outcomes
  - URL: https://www.crunchbase.com/
  - Data: Funding events, investor profiles, startup performance metrics (exits, IPOs, acquisitions)
  - Access: API access available with credentials; free limited tier available

- **PitchBook**: Professional venture capital database with fund performance, deal history, and portfolio company outcomes
  - URL: https://pitchbook.com/
  - Data: Detailed funding rounds, VC fund performance, portfolio exits, investor tier classifications
  - Access: Institutional access required; available through university partnerships

- **GitHub VC Dataset (academic)**: Open-source dataset of startup funding and performance from curated research projects
  - URL: https://github.com/topics/venture-capital-dataset
  - Data: Cleaned funding rounds with performance outcomes, suitable for research
  - Access: Free and open-source

- **SEC Edgar + Crunchbase Combined**: Historical IPO filings matched with pre-IPO funding data for longitudinal analysis
  - URL: https://www.sec.gov/edgar.php (combined with Crunchbase data)
  - Data: Complete IPO history, pre-IPO funding rounds, financial performance
  - Access: Public SEC data is free; requires integration with Crunchbase API

## Tasks

- **Data Collection & Integration**: Combine data from Crunchbase/PitchBook with performance outcomes (exits, acquisitions, IPOs); standardize VC tier classifications
- **Exploratory Data Analysis**: Visualize funding patterns by VC tier, sector, and geography; identify confounders and potential sources of bias
- **Propensity Score Matching**: Match VC-backed startups with similar non-VC-backed startups to create comparable cohorts
- **Causal Effect Estimation**: Apply difference-in-differences, instrumental variables, or causal forests to estimate treatment effects of VC funding
- **Robustness Checks**: Test sensitivity to confounder selection, matching specifications, and instrumental variable assumptions
- **Heterogeneous Treatment Effects**: Examine whether VC predictive power varies by sector, founder background, or market conditions
- **Visualization & Communication**: Create publication-quality figures showing causal estimates and confidence intervals

## Bonus Ideas

- **Founder Networks & Social Capital**: Investigate whether VC access to valuable networks (rather than capital allocation skill) drives startup success
- **Temporal Dynamics**: Use rolling time windows to evaluate whether VC predictive power has changed over decades
- **Sector-Specific Analysis**: Focus on high-impact sectors (biotech, AI, climate tech) to test whether predictive power varies by domain
- **Geographic Arbitrage**: Test whether VCs have predictive advantage in unfamiliar geographies or only in their home markets
- **Post-Money Valuation Effects**: Examine whether inflated post-money valuations in hot markets diminish VC predictive ability
- **Machine Learning Comparison**: Train ML models to predict startup success using VC decisions as features; compare predictive power to causal estimates
- **Long-term Follow-up**: Extend analysis beyond exits to measure sustainable profitability, customer retention, and employment impact

## Previous Research

- 2017, Peter Gleeson & Charles Hudson, "Do VCs Add Value?", Harvard Business School
  - Examined whether VC involvement increases probability of successful exit beyond founder quality
  - Found that after controlling for founder background and market timing, VC effect diminishes substantially

- 2020, Paul Gompers et al., "Artificial Intelligence, Machine Learning, and Asset Management", Harvard Business School
  - Analyzed whether data-driven VC strategies outperform traditional selection methods
  - Demonstrated machine learning models based on early-stage metrics provide modest predictive advantage over subjective VC decisions

- 2022, Carnahan et al., "Algorithmic Anchoring: How Casinos Exploit Human Biases", Strategic Management Journal
  - Explored survivorship bias in VC reporting of portfolio performance
  - Showed reported returns significantly overstate average VC predictive ability due to selective reporting

- GitHub: Startup Success Prediction Models (https://github.com/topics/startup-prediction)
  - Collection of open-source datasets and ML models for predicting startup success
  - Includes Crunchbase-based prediction challenges and benchmark results

## Implementation in Python

Tools and libraries:
- **Data Cleaning & Prep:** `pandas`, `numpy`
- **Modeling:** `statsmodels`, `scikit-learn`
- **Causal Inference:**
  - `econml` (Microsoft's causal inference package)
  - `dowhy` (causal graphs and treatment effect estimation)
  - `causalml` (uplift modeling and treatment effect heterogeneity)
- **Visualization:** `matplotlib`, `seaborn`
