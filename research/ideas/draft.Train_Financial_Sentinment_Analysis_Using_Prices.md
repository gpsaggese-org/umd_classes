# Train Financial Sentiment Analysis Using Price Response as Labels

## Status
- **Status**: draft
- **Complete Specs**: 15%
- **Assignee**: TBD

## Core Idea
- Standard financial sentiment models (e.g., FinBERT) are trained on
  human-labeled positive/negative/neutral news, which is expensive to produce
  and reflects human judgment of tone, not market impact
- Instead, fine-tune an LLM to predict sentiment using the *subsequent market
  price response* to a news item as a weak, automatically-generated label
  (e.g., price moved up X% in the following N minutes/hours => "positive")
- Key question: does a price-derived label produce a sentiment signal that is
  more predictive of *future* price moves than a human-labeled sentiment
  signal, or does it just learn to echo already-priced-in information
  (look-ahead/leakage risk)?

## Formalization
- Label: `y_i = sign(return(t_i, t_i + Δ))` for news item `i` published at
  `t_i`, for some horizon `Δ`
- Model: `ŷ_i = f_θ(text_i)` trained to predict `y_i`
- Evaluate on a held-out, strictly-later time period; compare predictive power
  of `ŷ` for *out-of-sample* returns against a human-labeled-sentiment
  baseline (e.g., FinBERT scores) and against a naive momentum baseline

## Key Examples
- **Earnings announcements**: label by post-announcement price drift; compare
  against analyst-labeled sentiment of the same announcement text
- **Macro news**: label by index-level move following a macro release; check
  whether the model learns genuine content signal or just keyword-level
  momentum artifacts (e.g., "rate cut" => up, regardless of context)

## Questions
1. Does price-derived labeling produce a sentiment signal with genuine
   out-of-sample predictive power, or does it overfit to look-ahead/leakage
   in the labeling window?
2. How sensitive are results to the choice of horizon `Δ` and to controlling
   for overall market movement (excess return vs. raw return as the label)?
3. Does this approach transfer across asset classes (equities vs. FX vs.
   crypto), or is it tied to one market's specific news-to-price dynamics?

## Research Topics
- Weak/self-supervised labeling from market data
- Look-ahead bias and leakage control in event-study-style labeling
- Comparison against existing financial sentiment benchmarks (FinBERT,
  Loughran-McDonald dictionary)

## Next steps
- [ ] Assemble a news+price dataset with precise timestamps
- [ ] Define the label (return horizon, excess-return control)
- [ ] Fine-tune a baseline model and compare against FinBERT-style sentiment
- [ ] Backtest predictive power out-of-sample, checking for leakage

## References
- Araci, D. (2019). _FinBERT: Financial Sentiment Analysis with Pre-trained
  Language Models_
