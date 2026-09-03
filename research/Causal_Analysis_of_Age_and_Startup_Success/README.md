# A Causal Analysis of Age and Startup Success

## 1. Project Overview

This project investigates whether **founder age has a causal effect on
startup success**, or whether the widely observed correlation between age
and success is explained by confounding factors — industry experience,
network/financial capital, and team composition.

Popular narratives about entrepreneurship celebrate very young founders, but
large-scale empirical research (Azoulay et al. 2018; Zhao et al. 2021)
suggests a more nuanced picture: the average successful founder is
middle-aged, and much of the apparent "age advantage" may be a proxy for
accumulated human, social, and financial capital rather than an independent
causal effect of age itself.

The goal is not simply to measure a correlation, but to apply causal
inference methods — regression adjustment, propensity score matching, DAG-based
confounder identification, and sensitivity analysis — to estimate how much of
the age–success relationship is likely causal, and how much is explained
away once relevant confounders are accounted for.

---

## 2. Background and Motivating Literature

### 2.1 Azoulay, Jones, Kim & Miranda (2018) — NBER Working Paper No. 24489
Analyzed 2.7 million U.S. founders (2007–2014) using Census microdata.

- Average founder age: 41.9 years
- Average age among the top 0.1% fastest-growing firms: 45 years
- A 50-year-old founder is ~1.8x more likely than a 30-year-old to build a
  top-growth firm
- Older founders were roughly twice as likely to achieve a successful exit
- Prior industry experience strongly predicts success — suggesting age may
  proxy for accumulated human capital

### 2.2 Zhao, Seibert & Lumpkin (2021) — Meta-analysis, Journal of Business Venturing
Synthesized 102 independent samples.

- Weak positive linear relationship between age and success overall
- Evidence of a U-shaped (nonlinear) relationship
- Effect direction depends heavily on the success metric used:

| Success Measure       | Relationship with Age |
|------------------------|------------------------|
| Firm Growth             | Negative               |
| Financial Performance   | Positive               |
| Firm Size               | Positive               |
| Subjective Success      | Positive               |
| Survival                 | No significant effect  |

### 2.3 Takeaway
Both studies converge on the same conclusion: **age is likely a proxy for
other forms of capital** (human, social, financial) rather than a direct
causal driver. This project tests that proxy hypothesis directly using
causal inference methods rather than relying on correlational summaries.

---

## 3. Problem Statement

> Do older founders succeed *because* they are older, or does age simply
> travel together with other things that really matter — industry know-how,
> bigger networks, more savings — which are the true drivers of success?

The core methodological challenge is **confounding**: age correlates with
industry experience, financial resources, and social capital, all of which
independently affect success. A naive correlation between age and success
conflates the effect of age itself with the effects of these accumulated
resources. Causal inference methods are used to strip away as much of this
confounding as the data allows, and to be explicit about what remains
unaddressed.

---

## 4. Causal Design

### 4.1 Treatment
**Founder age** — modeled as continuous, with a quadratic term (age²) to
capture the U-shaped relationship suggested by prior literature. Also
binarized (e.g. founded before 35 vs. founded 45+) as a robustness check for
matching-based methods.

### 4.2 Outcome
**Startup success** — primary definition: acquisition or IPO (binary).
Growth and funding are treated as secondary outcomes in separate models
rather than combined into a single composite measure.

### 4.3 Confounders (pre-treatment — control for these directly)
Variables that existed independently of the founder's age and could bias
both age and success:
- Industry
- Geography
- Founding year
- Team size
- Education

### 4.4 Mediators (post-treatment — analyzed separately, not controlled for directly)
Variables that are themselves *caused by* age and that go on to affect
success. Controlling for these in the same model as age would introduce
post-treatment bias and understate the true effect of age:
- Prior industry experience
- Network / financial capital

Testing how much the age coefficient shrinks when mediators are added is
itself a key finding (see Hypothesis H3 below) — it quantifies how much of
age's effect runs *through* these channels versus acting independently.

### 4.5 Unobserved Confounder
**Founder ability** (skill, judgment, drive) — not observable in any
available dataset. This cannot be controlled for directly. It is instead
addressed explicitly via sensitivity analysis (Rosenbaum bounds), which
quantifies how strong an unmeasured confounder would need to be to overturn
the estimated effect.

### 4.6 Causal DAG (conceptual structure)

```
                 Observed confounders
        (industry, geography, founding year,
              team size, education)
              /                      \
             v                        v
     Founder age  ── direct effect? ──>  Startup success
        |    \                          ^    ^
        |     \                        /      \
        |      v                     /         \
        |   Prior industry ---------            |
        |   experience (mediator)                |
        |                                        |
        v                                        |
   Network / financial ------------------------>-
   capital (mediator)

   Founder ability (UNOBSERVED) --(dashed)--> age AND success
   [handled via sensitivity analysis, not direct control]
```

Confounders point into both age and success and are controlled for directly.
Mediators are caused by age and go on to affect success — analyzed
separately to avoid post-treatment bias. Founder ability is an unobserved
common cause of both age and success, and is the central limitation of this
analysis — addressed via sensitivity analysis rather than ignored.

---

## 5. Research Hypotheses

- **H1** — Founder age has a positive association with high-growth startup
  success up to middle age.
- **H2** — The relationship between founder age and startup success is
  nonlinear (U-shaped).
- **H3** — Prior industry experience mediates the effect of age on startup
  success (i.e., the age coefficient shrinks substantially once experience
  is added to the model).
- **H4** — The direction and magnitude of the age effect depends on which
  success metric is used.

---

## 6. Data Sources

| Source | Contains | Access | Role |
|---|---|---|---|
| Crunchbase (Kaggle export) | Founder names, funding rounds, industry, employee count, company status | Free Kaggle download | Core dataset |
| Y Combinator company dataset | Batch year, status, industry, founders | Kaggle / public scrape | Core dataset (cleaner ground truth on outcomes) |
| LinkedIn / public bios | Founder education end-date, used as an age proxy | Manual / semi-automated | Age proxy — hardest step, see limitations |
| Census Bureau / BLS APIs | Industry growth rates, regional economic indicators, employment trends | Free public API | Macro confounders |

**Known limitation:** neither Crunchbase nor the YC dataset provides
founder birthdate directly. The NBER study used proprietary Census
microdata unavailable to this project. Founder age will be estimated as a
proxy (founding year − estimated graduation year + ~22), which introduces
noise and missingness that will be documented explicitly as a limitation
rather than treated as ground truth.

---

## 7. Procedure / Task Breakdown

### Step 1 — Data Collection & Integration
- Pull YC company list and Crunchbase founder/company data
- Estimate founder age via education-date proxy
- Merge datasets via fuzzy name matching (company + founder)
- Attach Census/BLS macro confounders by founding year × industry × region
- Define binary outcome variable (acquired/IPO = 1, else 0), with a
  documented cutoff date

### Step 2 — Exploratory Data Analysis (EDA)
- Distribution of founder ages, industries, funding rounds, outcomes
- Visualize raw age–success correlation and identify obvious confounders
- Segment by industry, geography, team composition for heterogeneity

### Step 3 — Confounder Identification & DAG Construction
- Formalize the DAG (Section 4.6) in code (e.g. via DoWhy)
- Validate variable classification (confounder vs. mediator) against domain
  knowledge and the literature in Section 2
- Document all causal assumptions explicitly

### Step 4 — Primary Modeling
- Regression: `success ~ age + age² + industry_FE + year_FE + team_size + geography + education`
- Mediation model: adds prior_industry_experience + network/financial
  capital, to test H3 (how much the age coefficient shrinks)

### Step 5 — Propensity Score Matching (robustness check)
- Binarize age (e.g. <35 vs. 45+)
- Estimate propensity scores on confounders only (not mediators)
- Match via nearest-neighbor within caliper
- Estimate Average Treatment Effect (ATE) on the matched sample
- Compare direction/magnitude against the regression estimate

### Step 6 — Sensitivity Analysis & Robustness Checks
- Rosenbaum bounds: quantify how strong an unobserved confounder (e.g.
  founder ability) would need to be to overturn the result
- Test whether results hold across industry subgroups and team sizes
- Compare PSM against alternative methods (inverse probability weighting,
  stratification) as available

### Step 7 — Interpretation & Reporting
- Visualize treatment effect heterogeneity across industries/demographics
- Report: does age have an independent causal effect, or is it explained
  away by confounders/mediators?
- Explicitly address magnitude, practical significance, limitations
  (especially the unobserved-ability problem), and policy implications

---

## 8. Repository Structure

```
research/Causal_Analysis_of_Age_and_Startup_Success/
├── README.md                  This file
├── requirements.txt
├── data/
│   ├── raw/                   Crunchbase, YC, Census pulls (untouched)
│   ├── interim/                Cleaned, deduplicated, name-matched
│   └── processed/              Final merged founder-level dataset
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_dag_and_model_spec.ipynb
│   ├── 03_regression.ipynb
│   ├── 04_psm.ipynb
│   └── 05_sensitivity.ipynb
└── src/
    ├── data_collection.py      Data pulling and merging
    ├── matching.py               Propensity score matching
    ├── models.py                  Regression specs (primary + mediation)
    └── sensitivity.py             Rosenbaum bounds
```

---

## 9. Bonus / Stretch Ideas (not in core scope)

- **Instrumental variables**: market conditions at founding (e.g. recession,
  tech boom) as an instrument for age-cohort effects — hard to defend on
  exclusion-restriction grounds, treated as a stretch goal only
- **Time-to-exit survival analysis**: causal effect of age on time to
  IPO/acquisition
- **Heterogeneous treatment effects**: causal forests to detect nonlinear/
  interaction effects across industries
- **VC funding bias**: whether investor decisions themselves introduce age
  bias, mediating the age–success relationship
- **Founder replacement analysis**: startups with founder turnover vs.
  stable teams, to help isolate age from founder quality

---

## 10. Known Limitations

- **Founder ability is unobserved** and cannot be directly controlled for;
  this is the central threat to causal identification and is addressed via
  sensitivity analysis rather than ignored.
- **Founder age is a derived proxy** (via education dates), not ground
  truth, and will carry measurement error and missingness.
- **Name-matching across datasets** (Crunchbase ↔ YC ↔ LinkedIn) is
  imperfect and may introduce merge errors.
- **Success is operationalized narrowly** (acquisition/IPO) as the primary
  outcome; other reasonable definitions of "success" may yield different
  conclusions (see H4).

---

## References

- Azoulay, P., Jones, B. F., Kim, J. D., & Miranda, J. (2018). *Age and
  High-Growth Entrepreneurship.* NBER Working Paper No. 24489.
  https://www.nber.org/system/files/working_papers/w24489/w24489.pdf
- Zhao, H., Seibert, S. E., & Lumpkin, G. T. (2021). *The Relationship of
  Age and Entrepreneurial Success: A Meta-Analysis.* Journal of Business
  Venturing. https://www.sciencedirect.com/science/article/abs/pii/S0883902619302691
- Causal Inference: The Mixtape — https://mixtape.scunning.com/
- Introduction to Causal Inference (Brady Neal) — https://www.bradyneal.com/causal-inference-book
- DoWhy Library Documentation — https://py-why.github.io/dowhy/
