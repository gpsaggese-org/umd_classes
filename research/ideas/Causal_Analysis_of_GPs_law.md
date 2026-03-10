# A Causal Proof of GP's Law
The world GDP is $100T / year

"GP's law": a substantial share (even 90%\!) is wasted in bad business decisions

Businesses make 100s decisions / day
- Pricing changes
- Hiring / promotions
- Capital projects
- Product feature priorities
- Vendor / partner selection ...

Humans are terrible decision makers
- Don't understand probability
- Do not use data
- Can't think counterfactually
- Use heuristics and gut feelings

- Create a simulation framework to measure this

In a study of 500 managers, 98% failed to apply even basic decision-making best
practices \[Larson, E. (2017)\] \~50% of decisions rely on intuition over data
\[BARC Survey (2016)\] Businesses use only 40-50% of available information
\[BARC Survey (2016)\]

# Deep Research Memo: How Much Business Value Is Lost to Poor Decisions?

## Executive Summary
The core intuition in your note is directionally right: business decision-making
is often poor, data is underused, and cognitive biases measurably distort
managerial judgment. But several of the specific claims need tightening.

The strongest supported points are these:

- **World GDP is on the order of $100T+ per year.** The World Bank reports
  **world GDP of about $110.98T in 2024** (current US$), so "$100T/year" is a
  reasonable shorthand but now somewhat low.
  [World Bank, 2024](https://data.worldbank.org/country/world)
- **Many business decisions are still not data-driven.** In BARC's 2016 global
  survey, **58% of respondents said their companies base at least half of
  regular business decisions on gut feel or experience**, and organizations used
  **only about 50% of available information** for decision-making.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)
- **Managers often do not follow structured decision practices.** A widely cited
  2017 article by Erik Larson reports that in a study of 500
  managers/executives, **98% failed to apply best practices**. That said, this
  appears to come from a vendor-backed study (Cloverpop), so it is better
  treated as **suggestive** than definitive.
  [Forbes/Larson, 2017](https://www.forbes.com/sites/eriklarson/2017/05/18/research-reveals-7-steps-to-better-faster-decision-making-for-your-business-team/)
- **Cognitive biases demonstrably affect professional judgment.** A 2022 review
  found evidence that **multiple cognitive biases affect professional
  decisions**, with **overconfidence** the most recurrent across management,
  finance, medicine, and law.
  [Berthet, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8763848/)
- **Probability judgments are often badly calibrated, even among senior
  executives.** In an NBER study of nearly 7,000 forecasts from top U.S.
  financial executives, realized stock-market returns fell inside executives'
  **80% confidence intervals only 38% of the time**, indicating strong
  miscalibration.
  [Ben-David, Graham & Harvey, 2007](https://www.nber.org/papers/w13711)
- **Better decision systems correlate with materially better business
  outcomes.** McKinsey reports that only **37%** of surveyed respondents say
  their organizations make decisions that are both high quality and fast;
  "winning organizations" were only **20%** of respondents, and were **twice as
  likely** as others to report recent decision returns of at least 20%.
  [McKinsey, 2019](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/decision-making-in-the-age-of-urgency)
- **Data-driven decision-making is associated with better firm performance.** In
  a study of 179 large publicly traded firms, firms emphasizing data-driven
  decision-making showed **5-6% higher output and productivity** than expected
  from other inputs alone, and also had higher profitability and market value.
  [Brynjolfsson, Hitt & Kim, 2011 working paper](https://ide.mit.edu/sites/default/files/publications/2011.12_Brynjolfsson_Hitt_Kim_Strength%20in%20Numbers_302.pdf)

The weakest claim is the one that matters most rhetorically:

A stronger, evidence-based framing would be:

> Business decision-making is a massive, under-optimized source of economic
> value. The problem is clearly large, but claims that something like 90% of
> global GDP is wasted by bad decisions are not currently evidence-based.

## Bottom-Line Assessment of Each Original Claim

### 1) "The world GDP is $100T / year"
**Assessment:** broadly correct, but outdated.

The World Bank reports **world GDP of $110.98T in 2024** (current US$). So
"$100T/year" works as an order-of-magnitude statement, but the more current
figure is closer to **$111T**.
[World Bank, 2024](https://data.worldbank.org/country/world)

### 2) "GP's law: a substantial share (even 90%) is wasted in bad business decisions"
**Assessment:** not substantiated.

I found **no credible academic, multilateral, or major consulting source**
supporting a quantitative claim that anything like **90% of GDP** is lost to
poor business decisions. There is strong evidence of decision inefficiency, but
the gap between "decision quality matters a lot" and "90% of GDP is wasted" is
enormous.

What the evidence _does_ support:

- McKinsey says executives spend **almost 40% of their time making decisions**,
  and **60% say that time is poorly used**.
  [McKinsey, 2023](https://www.mckinsey.com/featured-insights/mckinsey-guide-to-excelling-as-a-ceo/how-to-make-better-decisions-in-the-age-of-urgency)
- McKinsey also says decision making costs a **typical Fortune 500 company
  around $250M per year**.
  [McKinsey, 2023](https://www.mckinsey.com/featured-insights/mckinsey-guide-to-excelling-as-a-ceo/how-to-make-better-decisions-in-the-age-of-urgency)
- Bain reports a **95% correlation** between companies that excel at decision
  effectiveness and those with top-tier financial results, though this is still
  correlation, not a direct measure of waste.
  [Bain, 2010](https://www.bain.com/insights/score-your-organization-ame-info/)

So the defensible takeaway is **"large and material losses"**, not **"90% of
GDP"**.

### 3) "Businesses make 100s decisions / day"
**Assessment:** plausible in many firms, but I could not find a rigorous
universal estimate.

There is plenty of evidence that decision volume is high, but not a robust,
general-purpose benchmark saying that a business as such makes "hundreds" of
economically meaningful decisions per day. The strongest usable evidence I found
is indirect:

- McKinsey says executives spend **almost 40% of their time** making decisions.
  [McKinsey, 2023](https://www.mckinsey.com/featured-insights/mckinsey-guide-to-excelling-as-a-ceo/how-to-make-better-decisions-in-the-age-of-urgency)
- The kinds of decisions you list, pricing, hiring, project approval,
  prioritization, vendor selection, are standard recurring business decisions
  across functions.

A more defensible version is:

> Medium and large businesses make a very high volume of recurring operating,
> tactical, and strategic decisions every day, but the exact count varies
> sharply by firm size, structure, and what counts as a "decision."

### 4) "Humans are terrible decision makers"
**Assessment:** too absolute, but directionally supported.

The literature does **not** support the blanket claim that humans are simply
"terrible" decision makers in all contexts. But it _does_ show that even
professionals systematically deviate from rational or evidence-based judgment.

A 2022 review found that a **dozen cognitive biases** affect professional
decision-making, with **overconfidence** the most recurrent.
[Berthet, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8763848/)

McKinsey's 2018 survey also suggests substantial room for improvement: only
**57%** of respondents agreed their organizations consistently make high-quality
decisions, only **48%** said decisions are made quickly, and only **37%** said
they are both high quality and fast.
[McKinsey, 2019](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/decision-making-in-the-age-of-urgency)

Better phrasing:

> Human decision makers are often competent in familiar environments, but in
> business settings they are systematically vulnerable to bias, noise,
> miscalibration, and process failures.

### 5) "Don't understand probability"
**Assessment:** directionally supported, but should be framed as **systematic
miscalibration**, not total inability.

This is one of the better-supported claims if stated carefully.

The strongest evidence I found is from Ben-David, Graham, and Harvey: among top
U.S. financial executives, realized returns fell within their **80% confidence
intervals only 38% of the time**, a classic sign of overconfidence and poor
probabilistic calibration.
[Ben-David, Graham & Harvey, 2007](https://www.nber.org/papers/w13711)

This aligns with broader work on **probability neglect** and **statistical
illiteracy**, which shows people often mishandle uncertainty, especially when
outcomes are emotionally salient or complex.
[Sunstein, 2002](https://chicagounbound.uchicago.edu/law_and_economics/483/)
[Gaissmaier et al., 2009](https://pubmed.ncbi.nlm.nih.gov/19209567/)

Better phrasing:

> Even experienced managers are often poorly calibrated in probabilistic
> judgments and routinely underweight uncertainty, variance, and base rates.

### 6) "Do not use data"
**Assessment:** supported in moderate form.

The strongest direct support comes from BARC's 2016 global survey:

- **58% of respondents** said their companies base **at least half** of regular
  business decisions on gut feel or experience.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)
- Organizations used **only 50% of available information** for decision-making
  on average.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)

This does **not** mean businesses ignore data entirely. It means that even in
data-rich organizations, **decision processes are often only partially
data-driven**.

### 7) "Can't think counterfactually"
**Assessment:** too strong; the literature supports a more nuanced version.

The evidence does **not** show that humans cannot think counterfactually. In
fact, counterfactual thinking is a normal part of human cognition and can
improve learning. A review by Neal Roese describes counterfactual thinking as
having **functional benefits** for decision making and problem solving, while
also noting it can itself introduce bias.
[Roese, 2000](https://www.researchgate.net/publication/12633695_Counterfactual_thinking_and_decision_making)

So the problem is not inability. It is that organizations often **fail to
institutionalize disciplined counterfactual analysis** such as explicit
alternatives, base cases, pre-mortems, post-mortems, and decision reviews.

Better phrasing:

> Humans can think counterfactually, but organizations rarely do it
> systematically, and even when they do, hindsight and outcome bias often
> distort the exercise.

### 8) "Use heuristics and gut feelings"
**Assessment:** supported.

This is well supported by both behavioral science and business surveys.

- The BARC survey found that **58%** of respondents said at least half of
  regular decisions rely on gut feel or experience.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)
- The review by Berthet shows that professional decisions are affected by
  recurring biases, which is exactly what you would expect in systems relying on
  heuristics under uncertainty.
  [Berthet, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8763848/)

## Evaluation of the Two Cited Statistics in Your Note

### Larson (2017): "In a study of 500 managers, 98% failed to apply even basic decision-making best practices"
**Verdict:** usable with caution.

This statistic is widely quoted and appears in Erik Larson's 2017 Forbes
article, which says that a study of **500 managers and executives** found
**98%** failed to apply best practices.
[Forbes/Larson, 2017](https://www.forbes.com/sites/eriklarson/2017/05/18/research-reveals-7-steps-to-better-faster-decision-making-for-your-business-team/)

However, I could not find a strong peer-reviewed publication with transparent
methodology behind this exact number. The result appears to originate from
**Cloverpop**, a decision-software company founded by Larson. That does not make
it false, but it does make it **weaker evidence** than a peer-reviewed study or
an independently replicated survey.

**Best use:** cite it as an indicative, vendor-backed data point, not as a
settled scientific benchmark.

### BARC (2016): "~50% of decisions rely on intuition over data" and "Businesses use only 40-50% of available information"
**Verdict:** largely supported, with a wording correction.

BARC's report supports the core claim, but the more precise wording is:

- **58% of respondents** said their companies base **at least half** of regular
  business decisions on gut feel or experience.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)
- Organizations used **50% of available information** on average for
  decision-making.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)
- The sample sizes shown in the report are around **n=728** for several
  questions.
  [BARC, 2016](https://barc.com/data-driven-decision-making-business/)

So your current wording is close, but the exact claim is not "50% of decisions
rely on intuition over data" so much as **many firms still use gut feel for at
least half of their routine decisions**.

## What the Higher-Quality Literature Says Overall

### 1) Decision Quality Is a Real Performance Lever
McKinsey's global survey suggests that organizations making decisions both
**well** and **fast** are unusual, and that the combination is linked to better
financial returns. Only **37%** of respondents said their organizations'
decisions are both high quality and high velocity; just **20%** of organizations
qualified as "winning organizations." Those winners were **twice as likely** as
others to report recent decision returns of **20% or more**.
[McKinsey, 2019](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/decision-making-in-the-age-of-urgency)

### 2) the Inefficiency Cost Is Material Even Before Counting Bad Outcomes
McKinsey's CEO guide says a typical Fortune 500 company loses around **$250M
annually** to decision-making inefficiency, and executives say **60%** of time
spent on decisions is poorly used.
[McKinsey, 2023](https://www.mckinsey.com/featured-insights/mckinsey-guide-to-excelling-as-a-ceo/how-to-make-better-decisions-in-the-age-of-urgency)

That is important because it means the cost is not just "bad strategic calls."
It is also **organizational drag**: too many meetings, unclear roles, slow
approvals, weak follow-through, and poor use of evidence.

### 3) Data-Driven Decision-Making Appears to Improve Outcomes
The most cited empirical result here is Brynjolfsson, Hitt, and Kim's study of
**179 large publicly traded firms**, which found that data-driven firms had
**5-6% higher output and productivity** than expected from traditional inputs
and IT use alone, and also enjoyed higher profitability and market value.
[Brynjolfsson, Hitt & Kim, 2011](https://ide.mit.edu/sites/default/files/publications/2011.12_Brynjolfsson_Hitt_Kim_Strength%20in%20Numbers_302.pdf)

A later AEA paper by Brynjolfsson and McElheran found that data-driven
decision-making in U.S. manufacturing **nearly tripled from 11% to 30% between
2005 and 2010**, reinforcing the idea that DDD is economically meaningful and
diffusing.
[Brynjolfsson & McElheran, 2016](https://www.aeaweb.org/articles?id=10.1257/aer.p20161016)

### 4) Overconfidence Is Not a Side Issue; It Affects Capital Allocation
The NBER paper on managerial overconfidence is especially relevant because it
moves beyond lab experiments. It shows that top financial executives are
**poorly calibrated**, and links that miscalibration to concrete corporate
policies such as **higher investment**, **more debt use**, and different payout
behavior. [Ben-David, Graham & Harvey, 2007](https://www.nber.org/papers/w13711)

This matters because it supports a stronger claim than "people are biased": it
suggests that **biased beliefs can scale into capital allocation, financing, and
investment choices**.

### 5) Bias Is Broad-Based, Not Limited to One Function
Berthet's review concludes that cognitive biases affect professional decisions
across **management, finance, medicine, and law**, with overconfidence appearing
most often. [Berthet, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8763848/)

That makes it reasonable to view poor business decisions not as isolated
failures, but as the predictable output of human cognition operating under
uncertainty, incentives, time pressure, and incomplete information.

## What Is True but Easy to Overstate

### True
- Many business decisions are still made with incomplete use of available data.
- Managers are vulnerable to overconfidence, miscalibration, and other cognitive
  biases.
- Better decision processes and stronger use of data are associated with better
  performance.
- The economic stakes are very large.

### Easy to Overstate
- That managers are simply "terrible" across the board.
- That humans "can't" think probabilistically or counterfactually.
- That there is a defensible empirical basis for saying **90% of GDP** is
  wasted.
- That a single survey or vendor benchmark proves the whole thesis.

## Suggested Rewrite for Your Argument
Here is a version that preserves the force of the original idea while staying
closer to the evidence:

> Global GDP is now roughly $111T per year. Business decisions, about pricing,
> hiring, capital allocation, product priorities, and vendor selection, shape a
> meaningful share of that value. Yet the evidence suggests that many
> organizations still make a large fraction of decisions using gut feel rather
> than data, use only about half of the information available to them, and rely
> on managerial processes that are slow, biased, and poorly calibrated. Surveys
> and academic studies consistently find overconfidence, poor probabilistic
> judgment, and weak decision discipline among managers. At the same time, firms
> that are more data-driven appear to outperform peers on productivity and
> profitability. The exact share of GDP lost to poor decisions is unknown, and
> claims as high as 90% are not evidence-based, but the decision-quality gap is
> clearly economically enormous.

## Best One-Paragraph Conclusion
The evidence strongly supports the thesis that business decision-making is a
large, underappreciated source of economic inefficiency. It does **not** support
a precise "90% of GDP is wasted" law. The safest conclusion is that poor
decision processes, incomplete use of data, and predictable human biases create
losses that are clearly material at the firm level and plausibly enormous in the
aggregate, but not yet credibly quantified at a global level.

## Sources
1. World Bank. "World Bank Open Data: World." 2024 GDP (current US$).
   https://data.worldbank.org/country/world
2. BARC. "Global Survey on Data-Driven Decision-Making in Businesses." August
   17, 2016. https://barc.com/data-driven-decision-making-business/
3. Larson, Erik. "Don't Fail At Decision Making Like 98% Of Managers Do."
   Forbes, May 18, 2017.
   https://www.forbes.com/sites/eriklarson/2017/05/18/research-reveals-7-steps-to-better-faster-decision-making-for-your-business-team/
4. Berthet, Victor. "The Impact of Cognitive Biases on Professionals'
   Decision-Making: A Review of Four Occupational Areas." Frontiers in
   Psychology, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC8763848/
5. Ben-David, Itzhak, John R. Graham, and Campbell R. Harvey. "Managerial
   Overconfidence and Corporate Policies." NBER Working Paper 13711, 2007.
   https://www.nber.org/papers/w13711
6. McKinsey & Company. "Decision making in the age of urgency." April 30, 2019.
   https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/decision-making-in-the-age-of-urgency
7. McKinsey & Company. "How to make better decisions in the age of urgency."
   August 13, 2023.
   https://www.mckinsey.com/featured-insights/mckinsey-guide-to-excelling-as-a-ceo/how-to-make-better-decisions-in-the-age-of-urgency
8. Brynjolfsson, Erik, Lorin Hitt, and Heekyung Kim. "Strength in Numbers: How
   Does Data-Driven Decisionmaking Affect Firm Performance?" Working
   paper, 2011.
   https://ide.mit.edu/sites/default/files/publications/2011.12_Brynjolfsson_Hitt_Kim_Strength%20in%20Numbers_302.pdf
9. Brynjolfsson, Erik, and Kristina McElheran. "The Rapid Adoption of
   Data-Driven Decision-Making." American Economic Review 106, no. 5 (2016):
   133-139. https://www.aeaweb.org/articles?id=10.1257/aer.p20161016
10. Bain & Company. "Score your organization to improve decision
    effectiveness." 2010.
    https://www.bain.com/insights/score-your-organization-ame-info/
11. Sunstein, Cass R. "Probability Neglect: Emotions, Worst Cases, and Law."
    Yale Law Journal, 2002.
    https://chicagounbound.uchicago.edu/law_and_economics/483/
12. Gaissmaier, Wolfgang, et al. "Statistical illiteracy undermines informed
    shared decision making." Zeitschrift fur Evidenz, Fortbildung und Qualitat
    im Gesundheitswesen, 2009. https://pubmed.ncbi.nlm.nih.gov/19209567/
13. Roese, Neal. "Counterfactual thinking and decision making." Psychonomic
    Bulletin & Review, 2000.
    https://www.researchgate.net/publication/12633695_Counterfactual_thinking_and_decision_making
