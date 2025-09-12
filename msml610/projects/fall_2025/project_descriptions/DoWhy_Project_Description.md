**Description**

DoWhy is a Python library designed for causal inference that allows users to model causal relationships and perform causal reasoning. It provides a unified framework for defining causal graphs, estimating causal effects, and testing for causal assumptions. By leveraging DoWhy, users can analyze observational data to understand the impact of interventions and make informed decisions.

Features of DoWhy:
- Facilitates causal graph creation and manipulation.  
- Supports various causal inference methods including matching, stratification, and instrumental variables.  
- Provides tools for testing causal assumptions and robustness checks.  

---

### Project 1: Analyzing the Impact of Education on Income  
**Difficulty**: 1 (Easy) 

**Project Objective**  
Estimate the causal effect of educational attainment on individual income levels, focusing on a straightforward average treatment effect estimation.  

**Dataset Suggestions**  
- [World Bank Education Statistics](https://datacatalog.worldbank.org/search/dataset/0038480) (education attainment & income indicators by country).  
- Alternative: [OECD Education & Earnings Dataset](https://data.oecd.org/eduatt/) (individual-level samples with income and education).  

**Tasks**  
- **Define Causal Graph**: Build a simple graph with education as treatment, income as outcome, controlling for age, gender.  
- **Estimate Treatment Effect**: Apply DoWhy with methods like propensity score matching.  
- **Model Comparison**: Compare results with regression-based adjustment.  
- **Test Assumptions**: Conduct robustness checks for unobserved confounding.  
- **Interpret Results**: Visualize income differences across education levels.  

**Bonus Ideas (Optional)**  
- Compare causal effects by gender or region.  
- Explore years of education vs. categorical education levels.  

---

### Project 2: Evaluating the Effect of Marketing Campaigns on Sales  
**Difficulty**: 2 (Medium) 

**Project Objective**  
Assess the causal impact of marketing campaigns on retail sales revenue, accounting for seasonality and other confounders.  

**Dataset Suggestions**  
- [Retail Store Sales Data](https://www.kaggle.com/datasets/irfanasrullah/retail-store-sales-data) (transactional data with time dimension).  

**Tasks**  
- **Construct Causal Graph**: Include campaign activity, sales revenue, seasonality, and economic variables.  
- **Define Treatment**: Mark campaign-active periods vs. non-campaign periods.  
- **Estimate Effects**: Use DoWhy with matching, regression discontinuity, and stratification.  
- **Sensitivity Analysis**: Test robustness of estimates against unobserved confounders.  
- **Visualization**: Plot causal effects over time and confidence intervals.  

**Bonus Ideas (Optional)**  
- Compare campaign types (holiday vs. discount vs. digital).  
- Extend analysis to measure retention effects (long-term vs. short-term boosts).  

---

### Project 3: Understanding the Effect of Air Quality on Health Outcomes  
**Difficulty**: 3 (Hard) 

**Project Objective**  
Investigate the causal effect of air quality (e.g., PM2.5 levels) on respiratory health outcomes, accounting for socio-economic and geographic confounders.  

**Dataset Suggestions**  
- [EPA Air Quality System (AQS) Data](https://www.epa.gov/outdoor-air-quality-data).  
- Pair with [CDC/NCHS Mortality Data](https://www.cdc.gov/nchs/nvss/deaths.htm) or Kaggle respiratory health datasets for outcome measures.  

**Tasks**  
- **Develop Causal Framework**: Build a graph with air quality as treatment, health outcomes as effects, controlling for socioeconomic/demographic factors.  
- **Causal Estimation**: Apply DoWhy with multiple methods (matching, regression, instrumental variables).  
- **Instrumental Variable Analysis**: Use weather/wind direction as an IV for pollution exposure.  
- **Robustness Checks**: Conduct placebo tests by randomizing the treatment assignment to ensure no spurious effects are detected. Perform sensitivity analysis using DoWhy’s built-in tools (e.g., model.refute_estimate) to check how results change under hidden confounding or alternative model specifications. 
- **Non-linear Effects**: Explore whether effects vary at high vs. low PM2.5 levels.  

**Bonus Ideas (Optional)**  
- Assess effects of clean air policy interventions.  
- Run subgroup analysis (e.g., children vs. elderly).  
