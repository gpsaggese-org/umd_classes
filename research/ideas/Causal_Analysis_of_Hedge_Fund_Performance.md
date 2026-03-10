# Causal Analysis of Hedge Fund Performance

## Description

- Quantify the contribution of manager skill versus luck to hedge fund returns
- Analyze performance across market conditions, fund strategies, and time periods
- Apply causal inference techniques to isolate skill from random variation
- Compare hedge fund managers to establish skill distribution and persistence
- Study how fund characteristics (age, size, fee structure) relate to skill and luck
- Identify systematic underperformance and investigate potential causal factors

## Project Objective

The goal is to build a causal model that separates skill from luck in hedge fund performance. Using historical hedge fund data, students will apply causal inference methods to measure the degree to which manager outperformance can be attributed to genuine skill versus favorable market conditions or randomness. The project aims to answer: **What fraction of hedge fund returns can be explained by manager skill, and how persistent is this skill over time?**

## Dataset Suggestions

1. **CRSP Hedge Fund Database**
   - Source: Center for Research in Security Prices (University of Chicago)
   - URL: https://www.crsp.org/products/hedge-fund-database
   - Data: Monthly returns, fund characteristics, strategy classification, management fees, AUM
   - Access: Institutional subscription or academic license required

2. **Morningstar Alternative Investments Database**
   - Source: Morningstar
   - URL: https://www.morningstar.com/products/hedge-fund-database
   - Data: Historical performance, fund factsheets, manager tenure, strategy allocation
   - Access: Institutional access or direct purchase required

3. **BarclayHedge Database**
   - Source: Barclay Hedge
   - URL: https://www.barclayhedge.com/research/indices/
   - Data: Monthly index returns by strategy, constituent fund data, performance statistics
   - Access: Free public indices; detailed fund-level data requires subscription

4. **EDHEC Alternative Indices**
   - Source: EDHEC-Risk Institute
   - URL: https://www.edhec.edu/en/rethinking-finance/edhec-research
   - Data: Hedge fund indices by strategy, factor exposures, performance metrics
   - Access: Publicly available index data with free downloads

## Tasks

- **Data Collection and Cleaning**: Aggregate hedge fund returns from multiple sources, handle missing data, and standardize fund identifiers
- **Baseline Risk Adjustment**: Calculate risk-adjusted returns (Sharpe ratio, information ratio) and fund-specific factor exposures
- **Causal Decomposition**: Apply causal inference methods to estimate the skill component of returns separate from market/factor effects
- **Persistence Analysis**: Test whether manager skill persists across time periods and market regimes
- **Comparative Benchmarking**: Compare skill metrics across fund strategies, sizes, and fee structures
- **Statistical Validation**: Perform robustness checks and significance testing on skill estimates

## Bonus Ideas

- Develop a forward-looking skill predictor to rank managers by estimated future performance
- Investigate whether fund fees are correlated with manager skill or are simply transfers of returns
- Analyze the relationship between manager turnover and skill, and identify factors driving skilled manager departures
- Build an interactive dashboard showing skill vs luck attribution across different fund cohorts
- Compare skill persistence in hedge funds versus traditional mutual funds or factor-based strategies
- Study manager survivorship bias and its impact on estimated skill distributions

## Previous Research

- Saggese et al., Causal Analysis of Agent Skill and Luck, https://github.com/gpsaggese/gpsaggese.github.io/blob/master/papers/Causal_Analysis_of_Agent_Skill_And_Luck/Causal_Analysis_of_Agent_Skill_And_Luck.pdf
  - Developed a causal framework to decompose agent performance into skill and luck components
  - Applied methodology to quantify the contribution of skill versus randomness in competitive settings

- 2010, Fama & French, Luck versus Skill in Mutual Fund Performance, https://www.jstor.org/stable/25721416
  - Established baseline methods for separating manager skill from luck using statistical decomposition
  - Found that most mutual fund outperformance is attributable to luck rather than skill

- 2015, Mclean & Pontiff, Does Academic Research Destroy Stock Market Anomalies?, https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.12217
  - Studied how documented trading anomalies degrade after academic publication
  - Relevant to understanding survivorship bias and market efficiency effects on fund performance

- 2020, Arnott et al., How Can 'Active' Investing Outperform? An Analysis of the Lies, Damned Lies, and Statistics of Outperformance, https://www.researchaffiliates.com/documents/799-how-can-active-investing-outperform.pdf
  - Analyzed the components of active management outperformance (skill, beta, leverage, fees)
  - Quantified the role of risk-taking and fee structures in explaining hedge fund returns
