# Notebook Outline: Performing Causal Tasks with DoWhy

## Learning Objectives

By the end of this notebook, students will be able to:

- Estimate average causal effects using multiple identification strategies
- Identify when and how to apply backdoor criterion, natural experiments, and GCM-based approaches
- Conduct mediation analysis to decompose effects into direct and indirect pathways
- Quantify the strength of individual causal arrows in a system
- Perform root cause analysis for anomalies and distributional changes
- Estimate feature relevance in causal systems
- Answer counterfactual and interventional what-if questions
- Make causal predictions for out-of-distribution samples

## Part 1: Estimating Causal Effects

### Cell 1: The Fundamental Problem of Causal Inference (Markdown + Visualization)

**Purpose**: Build intuition about why causal effect estimation is hard and what assumptions enable it

**Content Description**:

- Visual explanation: Potential outcomes framework
  - Define treatment, outcome, counterfactual outcomes
  - Show why we can't observe both Y(T=1) and Y(T=0) for the same unit
- Illustrative examples: Three treatment scenarios
  1. Randomized experiment: we can observe both outcomes in expectation
  2. Observational study with confounding: we can't simply compare treated vs. control
  3. Same observational study with adjustment: strategic conditioning enables causal inference
- Interactive diagram: Toggle confounders on/off, see bias in naive comparison
- Key insight: Assumptions + data structure + adjustment strategy = identifiability

**Expected Output**:

- Clear explanation of selection bias vs. treatment effect
- Visual representation of confounded vs. unconfounded comparisons
- Intuition: why correlation ≠ causation, and what can fix it

### Cell 2: Backdoor Criterion and Confounding (Code + Interactive)

**Purpose**: Learn when and how to use backdoor adjustment to estimate causal effects

**Content Description**:

- Dataset: realistic healthcare scenario with treatment (medication) and outcome (recovery), confounded by disease severity
- Explain backdoor criterion visually with the DAG
  - Draw full causal DAG showing treatment, outcome, and confounders
  - Highlight confounder nodes and paths that create bias
  - Show how conditioning on confounder blocks the backdoor path
- Demonstrate bias in naive comparison
  - Compare recovery rates in treated vs. untreated groups (biased because severity differs)
  - Show the magnitude of bias
- Apply backdoor adjustment
  - Estimate effect using standard methods (stratification, regression, matching, IPW)
  - Interactive widget: select adjustment method, see estimated effect
  - Compare all methods—they should agree under correct specification
- Show sensitivity analysis: how robust is the estimate to unobserved confounding?

**Key Variables**:

- Treatment variable (e.g., medication yes/no)
- Outcome variable (e.g., recovery yes/no)
- Confounders (e.g., disease severity, comorbidities)
- Adjustment method choice
- Unobserved confounder sensitivity parameters

**Expected Output**:

- Comparison of naive vs. adjusted estimates
- Visualizations showing confounder-stratified outcomes
- Table of estimates from different adjustment methods
- Sensitivity range for robustness to hidden confounding

### Cell 3: Natural Experiments and Instrumental Variables (Code + Interactive)

**Purpose**: Learn causal inference strategies when confounders are unmeasured using instrumental variables

**Content Description**:

- Dataset: economic data with treatment (education level) and outcome (earnings), but key confounders (ability) are unobserved
- Introduce the concept of instrumental variables
  - Define a valid instrument (affects outcome only through treatment)
  - Visual DAG showing instrument, treatment, and outcome
  - Explain IV relevance (must affect treatment) and exclusivity (no direct effect on outcome)
- Show why backdoor adjustment fails here: unobserved confounder
- Apply instrumental variable estimation
  - First stage: predict treatment from the instrument
  - Second stage: regress outcome on predicted treatment
  - Discuss the interpretation: Local Average Treatment Effect (LATE)
- Interactive widget: adjust IV strength, see how estimate changes
- Discuss the critical assumption (exclusivity) and its plausibility

**Key Variables**:

- Treatment variable (education)
- Outcome variable (earnings)
- Instrument variable (e.g., birth cohort policy, distance to school)
- First-stage and second-stage models

**Expected Output**:

- Estimates from 2SLS (two-stage least squares)
- Visual representation of first and second stage
- Interpretation of LATE vs. ATE (average treatment effect)
- Sensitivity check: what if the exclusivity assumption is violated?

### Cell 4: Natural Experiments and Quasi-Experimental Designs (Code)

**Purpose**: Apply natural experiments where assignment is as-if random

**Content Description**:

- Dataset: policy change that affected some units but not others (e.g., policy rollout by region or cohort)
- Explain the setup of a natural experiment
  - Treatment assignment determined by external factors, not selection
  - Identification: compare units just above and below the threshold (regression discontinuity, RDD)
  - Or compare early-adopters vs. late-adopters before policy affected everyone
- Demonstrate difference-in-differences (DiD) estimation
  - Compare treated vs. control groups before and after the intervention
  - Visualize trends in both groups
  - Estimate treatment effect as the difference in post-pre changes
- Interactive widget: adjust bandwidth (for RDD), see estimated effect
- Diagnostic tests: parallel trends assumption, smooth cutoff assumption

**Key Variables**:

- Assignment variable (e.g., cohort, region, or policy threshold)
- Time period (pre/post treatment)
- Treatment and outcome variables
- Bandwidth or threshold specification

**Expected Output**:

- DiD visualization with pre/post trends
- Estimated treatment effect with confidence intervals
- Diagnostic plot showing whether parallel trends/smooth cutoff assumptions hold
- Interpretation: effect is valid only if assumptions are plausible

### Cell 5: Conditional Average Treatment Effects (CATE) (Code + Interactive)

**Purpose**: Learn how treatment effects vary across population subgroups

**Content Description**:

- Dataset: same healthcare data as Cell 2, but now ask: does the medication work equally for everyone?
- Introduce heterogeneous treatment effects
  - Show that some patients benefit more than others
  - Visual: scatter plot of patient characteristics vs. treatment effect
- Apply causal forests or other machine learning methods for CATE estimation
  - Train a model to predict individual treatment effects
  - Extract conditional effects for specific patient profiles
- Interactive widget: select patient characteristics, see predicted personalized effect
- Visualize effect heterogeneity
  - Show which patient types benefit most from treatment
  - Create a "rule": if patient has X characteristics, expect effect Y

**Key Variables**:

- Patient characteristics (age, severity, comorbidities, etc.)
- Treatment variable
- Outcome variable
- Method choice (causal forests, X-learner, etc.)
- Patient profile specification for prediction

**Expected Output**:

- Estimated conditional treatment effects across subgroups
- Visualization of effect heterogeneity (e.g., heatmap showing effect by age and severity)
- Personalized treatment effect recommendations
- Summary: which subgroups benefit most, which least?

### Cell 6: Causal Effects Using Graphical Causal Models (Code)

**Purpose**: Leverage a fitted structural causal model to estimate treatment effects

**Content Description**:

- Use the GCM fitted in a previous notebook (or build a simple one here)
- Dataset: synthetic or semi-realistic data where ground truth causal mechanisms are known
- Demonstrate advantage of GCM approach
  - Can answer effects without observational data once model is fitted
  - Can estimate effects under interventions not observed in data
  - Directly uses causal structure encoded in the graph and mechanisms
- Estimate average treatment effect via GCM
  - Define treatment: intervene on X
  - Generate counterfactual samples under the intervention
  - Compare to observational sample to compute ATE
- Interactive widget: select treatment variable and value, intervention type (hard, soft), observe effect
- Compare GCM estimate with other methods (backdoor, IV) on same data
- Discuss when GCM is superior vs. when other methods are more reliable

**Key Variables**:

- Fitted SCM from prior work
- Treatment variable and intervention value
- Outcome variable
- Intervention type (hard do, soft do, optimal policy)

**Expected Output**:

- Estimated treatment effect from GCM
- Counterfactual samples showing mechanism of effect
- Comparison with other methods (visual and numerical)
- Summary: GCM provides richer causal information (mechanisms) but requires stronger assumptions

## Part 2: Quantifying Causal Influence

### Cell 7: Mediation Analysis – Direct vs. Indirect Effects (Code + Interactive)

**Purpose**: Decompose a causal effect into direct and indirect components through mediators

**Content Description**:

- Motivating example: Does education affect earnings directly, or through increased job experience?
  - Show DAG: Education → Experience → Earnings, plus Education → Earnings (direct)
- Explain mediation concepts
  - Total effect = Direct effect + Indirect effect (through mediator)
  - Natural direct effect (NDE): effect holding mediator at its natural level
  - Natural indirect effect (NIE): effect that works through the mediator
- Dataset: real or realistic data with treatment, mediator, outcome, and confounders
- Estimate total, direct, and indirect effects
  - Using regression-based approach or sensitivity-analyzed semi-parametric methods
  - Show decomposition: TE = NDE + NIE
- Interactive visualization
  - Show the pathways with effect sizes labeled
  - Toggle between different mediators
  - Show proportion of effect mediated (NIE / TE)
- Sensitivity analysis: robustness to unmeasured confounder of mediator-outcome relationship

**Key Variables**:

- Treatment variable
- Mediator variable(s)
- Outcome variable
- Confounders of treatment-outcome and treatment-mediator relationships
- Sensitivity parameter (unmeasured confounding)

**Expected Output**:

- Decomposition table: NDE, NIE, Total Effect, and % mediated
- Visualization of causal pathways with effect sizes
- Confidence intervals for mediation effects
- Sensitivity range for robustness

### Cell 8: Direct Effect / Quantifying Arrow Strength (Code)

**Purpose**: Measure the strength of an individual causal arrow in a system

**Content Description**:

- Motivation: In complex systems, which variables most influence others?
- Dataset: system with multiple causal relationships (e.g., microservices, supply chain, or ecological system)
- Explain different notions of arrow strength
  - Regression coefficient (partial derivative)
  - Standardized effect (e.g., percentage change in outcome per unit change in input)
  - Causal importance relative to other inputs
- Estimate direct causal effects for each arrow
  - For each node, estimate the effect of each parent on that node
  - Visualize as weights on edges
- Interactive widget: select a causal arrow, visualize its strength and confidence interval
- Compare arrow strengths: which edges matter most?
- Create a "causal importance ranking" of inputs

**Key Variables**:

- Causal graph structure
- Target node and its parents
- Outcome of interest
- Adjustment for confounders and other paths

**Expected Output**:

- Quantified causal effects for each arrow
- Directed graph with weighted edges (line thickness/color indicates strength)
- Ranking of most important causal relationships
- Confidence intervals showing certainty of effect sizes

### Cell 9: Intrinsic Causal Influence (ICC) (Code + Interactive)

**Purpose**: Measure how much of a variable's variation is caused by upstream nodes vs. exogenous noise

**Content Description**:

- Motivation: In a causal system, variables have both causal inputs and stochastic noise; which dominates?
- Dataset: same system as Cell 8
- Explain intrinsic causal influence
  - Measures the relative contribution of causal parents vs. independent noise
  - Answers: "How much of X's behavior is explained by its causes vs. random variation?"
- Estimate ICC for each node in the system
  - Decompose node's variance into causal and independent components
  - Visualize as proportional contributions
- Interactive widget: select a node, see composition of its variation (pie chart: % from causes vs. noise)
- Show nodes with high ICC (tightly controlled by parents) vs. low ICC (mainly stochastic)
- Interpret: nodes with high ICC are predictable from their inputs; nodes with low ICC have intrinsic randomness

**Key Variables**:

- Causal graph and fitted mechanisms
- Target node
- Methods: variance decomposition via fitted SCM

**Expected Output**:

- ICC scores for each node (0-1, where 1 = fully determined by parents)
- Visualization: node coloring by ICC (e.g., dark = high ICC, light = low ICC)
- Summary: which variables are most predictable from their causes?

## Part 3: Root-Cause Analysis and Explanation

### Cell 10: Anomaly Attribution (Code + Interactive)

**Purpose**: When a system variable is anomalous, identify which upstream causes are responsible

**Content Description**:

- Scenario: System health dashboard shows anomaly (e.g., latency spike, sales drop, patient adverse outcome)
- Dataset: system metrics before/after anomaly, with fitted causal model
- Explain anomaly attribution concept
  - Observe an unusual outcome value
  - Trace back through causal mechanisms: which inputs deviated from normal?
  - Attribution: assign responsibility to each causal input
- Method: counterfactual reasoning
  - In normal conditions, what would the outcome have been?
  - What actually happened?
  - Compare to identify which mechanism changes drove the anomaly
- Interactive dashboard
  - Show system metrics at time of anomaly (tabular or time-series view)
  - Highlight anomalous values (inputs that deviated most from baseline)
  - Show counterfactual predictions: if only X had been anomalous, what outcome?
  - Summary: "The latency spike was primarily caused by elevated CPU usage (60%) and high query volume (30%), not disk I/O (10%)"
- Sensitive to model specification: discuss how model misspecification affects attribution

**Key Variables**:

- Baseline conditions (normal operation)
- Anomalous event (observed deviations from baseline)
- Fitted causal model
- Outcome of interest

**Expected Output**:

- Attribution scores for each input variable (% responsibility for anomaly)
- Counterfactual analysis: "If only this input had been anomalous, outcome would have been..."
- Prioritized list of root causes
- Confidence/sensitivity analysis

### Cell 11: Attributing Distributional Changes (Code + Interactive)

**Purpose**: When population-level distributions shift, identify which variables caused the shift

**Content Description**:

- Scenario: Product's customer base changes composition (e.g., older customers, lower income), affecting outcome distribution
- Dataset: two time periods (before and after shift), customer features and outcomes
- Problem: outcome distribution changed; which features changed most drove the outcome shift?
- Method: Causal decomposition
  - Quantify how each feature distribution changed
  - Use fitted causal model to predict outcome impact of each feature change
  - Decompose: ΔP(Y) = Σ_X contribution(X) × ΔP(X)
- Interactive visualization
  - Side-by-side histograms: feature distributions before/after
  - Bar chart: contribution of each feature to outcome shift
  - Highlight which features changed most and had largest causal impact
- Example: "Customer age distribution shifted younger (−10% avg age), reducing average satisfaction (−5 pts). Income distribution stayed flat. So 80% of satisfaction decline is due to age shift."

**Key Variables**:

- Feature distributions before and after
- Feature change magnitudes
- Fitted causal model or estimates of causal effects
- Outcome variable

**Expected Output**:

- Distribution shift visualization for key variables
- Decomposition table: each feature's contribution to outcome change
- Attribution visualization: pie chart or bar chart of contribution %
- Insight: which features most explain the population shift?

### Cell 12: Feature Relevance in Causal Context (Code + Interactive)

**Purpose**: Measure which features are causally relevant for predicting an outcome

**Content Description**:

- Motivation: Not all correlates are causes; ML models may rely on proxies
- Dataset: multi-feature prediction problem with causal relationships
- Explain causal feature relevance
  - A feature is causally relevant if intervening on it changes the outcome
  - Different from statistical relevance (correlation, feature importance)
- Estimate causal relevance
  - For each feature, estimate its direct effect on outcome (after adjusting for confounders)
  - Use backdoor adjustment or GCM-based estimation
  - Rank features by causal strength
- Interactive visualization
  - Feature importance bar chart: show causal relevance
  - Comparison with ML importance (random forest, shap) if available
  - Highlight where causal and statistical importance diverge (potential proxies)
- Example: "ML says zip code is most important for predicting loan repayment. But causally, only income and credit score matter. Zip code is a proxy."

**Key Variables**:

- Features of interest
- Outcome variable
- Causal graph / assumed causal relationships
- Outcome variable

**Expected Output**:

- Causal relevance scores for each feature
- Comparison visualization: causal vs. statistical importance
- Identification of proxy variables (high statistical, low causal relevance)
- Actionable insight for model interpretation

## Part 4: Answering What-If Questions

### Cell 13: Simulating the Impact of Interventions (Code + Interactive)

**Purpose**: Use causal models to predict outcomes under hypothetical interventions

**Content Description**:

- Scenario: Business planning – "What if we increase marketing spend by 50%?"
- Dataset: historical data with fitted causal model
- Explain intervention vs. observation
  - Observational question: "Are high-spending companies successful?"
  - Causal question: "Would our company become more successful if we increased spending?"
  - Answer requires modeling the causal mechanism, not just correlation
- Demonstrate interventional prediction
  - Define intervention: set marketing spend to a specific value
  - Use fitted model to predict effect on outcome (revenue, conversion, etc.)
  - Simulate multiple scenarios: spend at 50%, 100%, 150%, 200% levels
  - Visualize dose-response curve
- Interactive dashboard
  - Slider: adjust intervention level for policy variable
  - Automatic prediction: "If marketing spend = $X, predicted revenue = $Y"
  - Comparison: show multiple scenarios side by side
  - Confidence intervals: show uncertainty in predictions
- Discuss robustness: how sensitive are predictions to model specification?

**Key Variables**:

- Treatment/policy variable (e.g., marketing spend)
- Intervention levels to test
- Outcome of interest
- Fitted causal model or estimates

**Expected Output**:

- Dose-response curve: intervention level vs. predicted outcome
- Table of scenarios: intervention level and predicted outcomes
- Confidence intervals showing uncertainty
- Recommendation: "Optimal spend appears to be $X based on model"

### Cell 14: Computing Counterfactuals (Code + Interactive)

**Purpose**: Answer individual-level what-if questions using counterfactual reasoning

**Content Description**:

- Scenario: Patient care – "If this patient had taken drug A instead of drug B, would the outcome have been better?"
- Dataset: medical records with treatment and outcome, fitted causal model
- Explain counterfactual inference
  - Observe: patient took drug B and had outcome Y
  - Counterfactual: what if they had taken drug A? Would outcome be Y' ?
  - Requires causal model to generate predictions
- Method: Counterfactual prediction from fitted SCM
  - Observe patient features and mechanism inputs
  - Intervene: set treatment to alternative value
  - Simulate outcome under counterfactual treatment
  - Compare: Y vs. Y'
- Interactive tool
  - Select a real individual (patient, customer, loan applicant)
  - Show actual treatment and outcome
  - Interactive widget: select alternative treatment
  - Predict counterfactual outcome
  - Show treatment effect: Y' - Y for this individual
  - Example: "Patient received Drug B → adverse outcome. Under counterfactual Drug A → predicted recovery. Estimated benefit of Drug A: +40%"
- Caveats: counterfactuals beyond the empirical support of data are inherently speculative

**Key Variables**:

- Individual features (observed)
- Actual treatment received
- Alternative treatment to consider
- Fitted causal model

**Expected Output**:

- Individual case study: actual vs. counterfactual outcome
- Estimated treatment effect for this individual
- Uncertainty intervals around counterfactual prediction
- Interpretation: "What could have happened if treatment differed"

### Cell 15: Optimal Policy Estimation (Code + Interactive)

**Purpose**: Use causal models to design optimal decision policies

**Content Description**:

- Scenario: Resource allocation – "Which customers should receive premium support?"
- Dataset: customer features, assigned support level (treatment), and outcomes, fitted causal model
- Explain policy learning
  - Observe: different customers received different support levels
  - Goal: learn rule for assigning support to maximize outcome
  - Strategy: estimate treatment effects for each customer, assign support to those with highest predicted benefit
- Method: Policy learning from causal effects
  - Estimate conditional treatment effects (CATE) from Cell 5
  - For each customer, estimate how much their outcome improves with premium support
  - Optimal policy: assign premium support to customers with highest estimated benefits
  - Estimate value of optimal policy vs. actual allocation
- Interactive dashboard
  - Show customer pool with predicted treatment benefits
  - Apply optimal policy: allocate premium support to top X% by benefit
  - Show counterfactual outcome distribution under optimal policy
  - Comparison: actual outcome vs. predicted outcome under optimal policy
  - Summary: "Optimal policy would increase satisfaction by +12% (or save $2M in customer support costs)"

**Key Variables**:

- Customer/unit features
- Treatment/policy variable (e.g., support tier)
- Outcome of interest
- Estimated conditional treatment effects
- Constraint: limited resources (only support top X% of customers)

**Expected Output**:

- Ranking of units by treatment benefit
- Optimal allocation rule: "Assign premium support if benefit > threshold"
- Outcome distribution under optimal policy
- Estimated value improvement from optimal allocation
- Actionable policy recommendation

## Part 5: Causal Prediction

### Cell 16: Predicting Outcomes for Out-of-Distribution Inputs (Code + Interactive)

**Purpose**: Use causal knowledge to make robust predictions when test data differs from training data

**Content Description**:

- Scenario: ML model trained on historical data fails when deployed to new population
  - Reason: out-of-distribution shift in features (e.g., recession changes customer profiles)
  - Naive prediction: extrapolating model from old data gives wrong answers
  - Causal approach: use model of causal mechanisms to predict even under distribution shift
- Dataset: training data from one period/population, test data from different period/population
- Demonstrate ML vs. Causal prediction under OOD shift
  - Train standard ML model on original data
  - Retrain using causal model (fitted mechanisms)
  - Test both on OOD data
  - Compare accuracy: causal approach should generalize better
- Interactive comparison
  - Select OOD shift type (e.g., budget constraints, demographic change)
  - Show prediction accuracy comparison (ML vs. Causal)
  - Visualize predicted vs. actual outcomes
  - Confidence intervals showing uncertainty
- Discuss mechanism: causal models predict based on mechanisms, not just correlations
  - If mechanisms don't change (assumption), predictions remain valid under shift
  - ML models rely on correlations, which don't hold OOD

**Key Variables**:

- Training distribution
- OOD test distribution (type and magnitude of shift)
- Treatment/input variables
- Outcome of interest
- Fitted ML and causal models

**Expected Output**:

- Prediction accuracy comparison (ML vs. Causal)
- Visualization: predicted vs. actual for OOD data
- Summary: "Under OOD shift, causal model has 15% lower error rate"
- Insight: when to trust causal predictions vs. standard ML

### Cell 17: Transportability and Generalization (Code + Interactive)

**Purpose**: Learn when causal estimates from one population can be applied to another

**Content Description**:

- Scenario: Randomized trial conducted in one country; can we trust results in another?
  - Reason confounds transport: causal mechanisms may differ across populations
  - Question: which assumptions allow us to generalize?
- Dataset: trial data from population A, target population B with different feature distributions
- Explain transportability conditions
  - Selection diagrams showing when estimates from A apply to B
  - Key: are there population-specific confounders? Interaction effects? Mechanism changes?
  - Visual: draw DAG with selection node S indicating population
- Demonstrate transportability assessment
  - Estimate treatment effect in population A
  - Assess whether mechanisms plausibly differ in population B
  - Adjust estimate if necessary (weighted by population B characteristics)
  - Compute adjusted estimate for population B
- Interactive scenario analysis
  - Select two populations (countries, time periods, demographic groups)
  - Show how feature distributions differ
  - Assess transportability visually (diagram showing potential threats)
  - Estimate adjusted treatment effect for target population
  - Confidence or uncertainty level given transportability assumptions

**Key Variables**:

- Source population (where we have data)
- Target population (where we want to predict)
- Treatment and outcome variables
- Potential modifiers/confounders that differ between populations
- Feature distributions in both populations

**Expected Output**:

- Transportability assessment: can we generalize? Why or why not?
- Adjusted treatment effect estimate for target population
- Sensitivity analysis: range of estimates under different assumptions
- Recommendation: "Estimate is transportable with X% confidence, assuming mechanisms don't change"

## Part 6: Integration and Application

### Cell 18: Choosing the Right Method for Your Causal Question (Interactive Decision Tree)

**Purpose**: Synthesize understanding of all methods and learn when to apply each

**Content Description**:

- Interactive flowchart / decision tree
  - Start: What is your causal question?
  - Branch 1: Estimating effects? → Guide to backdoor, IV, natural experiments, GCM
  - Branch 2: Explaining system behavior? → Guide to mediation, arrow strength, ICC, feature relevance
  - Branch 3: Finding root causes? → Guide to anomaly attribution, distribution shifts
  - Branch 4: Answering what-if? → Guide to interventions, counterfactuals, optimal policy
  - For each method: when applicable, data requirements, assumptions, limitations
- Guided examples
  - 4-5 realistic case studies (healthcare, economics, operations, e-commerce)
  - Walk through decision tree for each
  - Select appropriate method(s)
  - Note: some questions require multiple methods
- Interactive quiz
  - Scenario presented
  - Student selects best method
  - Feedback: "Correct! Here's why. Alternative methods could also work because..."
  - Highlights trade-offs and nuances

**Expected Output**:

- Clear understanding of method applicability
- Confidence in selecting appropriate methods for new problems
- Recognition that multiple methods may apply with different trade-offs

### Cell 19: Comprehensive Case Study – End-to-End Causal Analysis (Code Project)

**Purpose**: Integrate all concepts in a realistic, multi-method analysis

**Content Description**:

- Open-ended project: realistic domain (e.g., e-commerce platform, healthcare delivery, supply chain, marketing analytics)
- Workflow summary with multiple tasks
  1. Define causal question(s): what do stakeholders want to know?
  2. Specify causal graph from domain knowledge or discovery
  3. Identify estimation strategy (backdoor, IV, natural experiment, GCM, etc.)
  4. Estimate treatment effects (average and conditional)
  5. Conduct mediation analysis: which pathways matter?
  6. Identify root causes of anomalies or shifts
  7. Answer what-if policy questions
  8. Assess robustness: sensitivity to unobserved confounding, model specification

- Dataset: realistic with confounding, heterogeneous effects, and multiple causal pathways
- Scaffolded notebook with prompts
  - Cells with setup code and guiding questions
  - Students fill in key analytic steps
  - Interactive checkpoints: "Is your graph reasonable? Why?"
  - Visualization requirements: create at least 3 explanatory plots
  - Report requirements: 1-2 page summary of findings and recommendations

**Key Variables**:

- Domain-specific features, treatments, outcomes
- Causal assumptions and constraints
- Stakeholder decisions to be informed

**Expected Output**:

- Fully worked case study
- Causal analysis report: question, method, findings, limitations, recommendations
- Visualizations and interpretation
- Reflection: assumptions made, uncertainties, what would improve the analysis?

### Cell 20: Limitations, Assumptions, and When Causal Methods Fail (Markdown + Discussion)

**Purpose**: Develop critical thinking about when to trust causal inferences

**Content Description**:

- Key assumptions underlying causal inference
  - Causal Markov condition
  - Causal sufficiency (no hidden confounders)
  - SUTVA (stable unit treatment value assumption): treatment on one unit doesn't affect others
  - Consistency: "treatment" is well-defined
  - Causal mechanisms are autonomous (don't change when other variables intervene)
- Consequences of violated assumptions
  - Unobserved confounding → biased estimates
  - Indirect effects / spillovers → invalid treatment definitions
  - Mechanism instability → OOD estimates fail
  - Model misspecification → causal conclusions are wrong
- Real-world examples where causal methods failed
  - Policy that worked in one context failed in another (transportability failure)
  - Treatment effect flipped when analyzed in subgroups (mechanism heterogeneity)
  - Mediation analysis suggested mechanism that was later shown false
- Practical guidance
  - How to assess plausibility of assumptions (domain expertise, sensitivity analysis, validation experiments)
  - Red flags: when to be skeptical of causal conclusions
  - Complementary approaches: combine methods, triangulate, fail-safe strategies

**Expected Output**:

- Clear understanding of assumptions and their importance
- Framework for critically evaluating causal conclusions
- Healthy skepticism paired with practical problem-solving mindset
