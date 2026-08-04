<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides001.png){width=80%}

</center>

<center>

# 2 / 30: Why Traditional ML Falls Short

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides002.png){width=80%}

</center>

- **Traditional machine learning optimizes prediction accuracy on a fixed
  distribution**: Traditional machine learning models are designed to perform
  well on a specific set of data, assuming that the data distribution remains
  constant. This approach focuses on achieving high accuracy but can overlook
  important aspects needed for effective decision-making.

- **Causality: modeling correlation, not mechanisms**: Traditional models often
  identify patterns and correlations in data without understanding the
  underlying causes. This means they might predict outcomes accurately but fail
  to explain why those outcomes occur, which is crucial for making informed
  decisions.

- **Uncertainty: no quantification of what the model does not know**: These
  models typically do not account for uncertainty or the limits of their
  knowledge. Without understanding the confidence or uncertainty in predictions,
  decision-makers might rely too heavily on the model's outputs without
  considering potential risks or errors.

- **Business objective: a prediction is not a decision**: While a model can
  predict outcomes, it doesn't inherently align with business goals or
  strategies. Decision-making requires integrating predictions with business
  objectives, which traditional models do not address.

- **Dynamics: the world reacts to the actions informed by the prediction**: The
  environment in which decisions are made is dynamic and can change in response
  to actions taken based on model predictions. Traditional models often fail to
  account for these feedback loops, leading to decisions that might not be
  effective in a changing context.

- **Each gap turns a technically accurate model into a poor decision-maker**:
  Even if a model is technically accurate, these gaps can lead to poor
  decision-making. Understanding and addressing these limitations is crucial for
  developing models that not only predict accurately but also support effective
  and informed decisions.

<center>

# 3 / 30: From Data Science to Decision Science

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides003.png){width=80%}

</center>

- **Data science and decision science optimize for different things**
  - **Goal**: In _data science_, the main aim is to _predict outcomes_. This
    means using data to forecast what might happen in the future. On the other
    hand, _decision science_ focuses on _choosing the best actions_. It’s about
    figuring out what steps to take to achieve the best results.

  - **Question**: Data science asks, _“What will happen?”_ It’s about
    understanding future possibilities. Decision science asks, _“What should we
    do?”_ It’s about deciding on the best course of action based on the data.

  - **Method**: Data science uses _statistical models and machine learning_ to
    make predictions. Decision science uses _causal models and decision theory_
    to understand the impact of different actions and make informed choices.

  - **Output**: The result of data science is a _forecast_, which is a
    prediction of future events. Decision science provides an _action plan_,
    considering uncertainty and expected outcomes.

  - **Metric**: Data science measures success with _accuracy, AUC, and RMSE_,
    which are technical metrics. Decision science focuses on _business outcomes
    and ROI_, which are more aligned with business goals.

  - **Data**: Data science relies on _observations_ from past data. Decision
    science uses these observations along with _causal structure_ to understand
    how different factors influence outcomes.

- **Key idea**: Simply providing a prediction is not enough if a business needs
  to make a decision. Even if a prediction is very accurate, it doesn’t help
  much unless it guides the business on what actions to take.

<center>

# 4 / 30: Causal vs Predictive Questions

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides004.png){width=80%}

</center>

- **Every business question has a predictive form and a causal form, and only
  one of them says what to do**
  - In business and data analysis, questions can be framed in two ways:
    _predictive_ and _causal_.
  - **Predictive Question**: This type of question focuses on forecasting or
    predicting future outcomes based on existing data. For example, "Which
    customers will churn?" aims to identify customers likely to leave.
  - **Causal Question**: This type of question seeks to understand the effect of
    an action or change. For instance, "What action prevents churn?" looks for
    strategies to retain customers.
  - The table illustrates examples of both types of questions across different
    scenarios, highlighting the difference between predicting an outcome and
    understanding the cause of an outcome.

- **@Key idea@**
  - **Predictive questions**: These can be answered using observational data,
    which means data collected without any intervention. This is useful for
    tasks like monitoring trends or setting up alerts. However, it doesn't guide
    decision-making because it doesn't explain why something happens.
  - **Causal questions**: To answer these, we need causal models or experiments,
    such as randomized controlled trials. These questions are crucial for making
    informed decisions and designing effective policies because they help us
    understand the impact of specific actions or changes.

<center>

# 5 / 30: The Analytics Maturity Ladder

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides005.png){width=80%}

</center>

- **The Analytics Maturity Ladder**: This concept illustrates the progression of
  an organization's ability to use data effectively. It is structured into four
  levels, each representing a different stage of analytical sophistication.

- **Organizations climb four levels of analytical sophistication**:
  - **Level 1: Descriptive** - This is the starting point where organizations
    use tools like dashboards and reports to understand _what happened_ in the
    past. It's about summarizing historical data.
  - **Level 2: Predictive** - At this stage, organizations use machine learning
    and forecasting to predict _what will happen_ in the future. This involves
    analyzing trends and patterns to make informed guesses.
  - **Level 3: Causal** - Here, the focus shifts to understanding _why things
    happen_ and exploring _what if scenarios_ using tools like Directed Acyclic
    Graphs (DAGs) and do-calculus. This level is about identifying
    cause-and-effect relationships.
  - **Level 4: Decision** - The final level involves using causal models
    combined with utility to determine _what should be done_. This is about
    making informed decisions based on the insights gained from previous levels.

- **Problem**: Many organizations find themselves stuck at Level 2. They are
  good at predicting outcomes but struggle to understand the underlying causes
  or decide on the best course of action.

- **Key idea**: The book emphasizes the importance of advancing to Levels 3
  and 4. This transition involves moving from merely predicting outcomes to
  understanding causality and making decisions based on that understanding.

- **The Cost of Ignoring Causality**: Ignoring causality can lead to misleading
  conclusions, as correlation does not imply causation. Understanding the true
  cause-and-effect relationships is crucial for making effective decisions.

<center>

# 6 / 30: Correlation Encodes Confounding as Causation

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides006.png){width=80%}

</center>

- **Problem**: A purely predictive model focuses on learning the probability of
  an outcome, $\Pr(Y | X)$, based on historical data. This means it captures all
  associations in the data, whether they are meaningful or not.
  - The model is designed to answer the question _"what will happen?"_, but it
    does not address _"what should we do?"_. This is a crucial distinction
    because knowing what will happen doesn't necessarily guide us on the best
    course of action.
  - The model assumes that the world remains unchanged, even though the
    predictions it makes can influence actions that alter the world.

- **Example**: Consider the correlation between ice cream sales and drowning
  deaths, which are both high during hot weather.
  - A predictive model might suggest that _"more ice cream sales lead to more
    drownings"_, which is technically accurate but misleading.
  - If a decision is made based on this correlation, such as _"banning ice cream
    to reduce drownings"_, it could lead to poor outcomes because it ignores the
    real cause.
  - The true confounder here is hot weather, which increases both ice cream
    sales and drowning incidents.

- **Key idea**:
  - There is a fundamental difference between observational and interventional
    probabilities: $\Pr(Y | X)$ (observational) is not the same as
    $\Pr(Y | do(X))$ (interventional).
  - Relying on $\Pr(Y | X)$ for decision-making can lead to incorrect
    conclusions because it treats correlation as causation, which can result in
    decisions that backfire.

<center>

# 7 / 30: Missing Interventions and Counterfactuals

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides007.png){width=80%}

</center>

- **Problem**: When we use correlation models, they can tell us what is
  currently happening, but they can't answer questions about potential changes
  or reasons behind the data. This means they are limited to describing the
  present situation without exploring hypothetical scenarios or underlying
  causes.

- **Two classes of business question stay permanently out of reach**:
  - **Intervention**: This type of question asks about the effects of a specific
    action. For example, if a company reduces its prices by 10%, it wants to
    know how this will affect the number of products sold and the overall
    revenue. Correlation models can't predict these outcomes because they don't
    account for changes.
  - **Counterfactual**: These questions explore hypothetical scenarios. For
    instance, a business might want to know if a customer would have stayed if
    they had been offered a discount. Correlation models can't answer this
    because they only look at existing data, not what could have happened under
    different circumstances.

- **Example**: Consider a tutoring program that seems to be linked with higher
  exam scores. The question arises whether the tutoring directly causes the
  improvement in scores, or if students who are already strong are more likely
  to participate in the tutoring program. Observational data alone can't clarify
  this because it doesn't show causation, only correlation.

- **Key idea**: To answer questions about interventions and counterfactuals, we
  need a causal model. This type of model helps us understand the
  cause-and-effect relationships, rather than just predicting outcomes based on
  existing data.

<center>

# 8 / 30: Selection Bias and the Missing Counterfactual

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides008.png){width=80%}

</center>

- **Selection Bias and the Missing Counterfactual**
  - _Problem_: When we look at historical data, we only see the outcomes of
    decisions that were actually made. We don't have information about what
    could have happened if different decisions were made.
    - For example, in loan data, we have information about people who were
      approved for loans and their outcomes, but we often lack data on those who
      were rejected.
    - This is different from confounding, which affects the relationship between
      variables that are recorded. Selection bias is about which data points are
      recorded in the first place, and this issue is present before we even
      start building any models.

- **Example**: Consider a credit model that is trained using data from loans
  that were approved.
  - This model can learn patterns about who repays loans among those who were
    approved, but it doesn't have any information about those who were rejected.
    Therefore, it can't predict whether rejected applicants would have repaid
    their loans.

- **Key idea**: A model might perform well on the data it has seen, but it might
  not be useful for making decisions about the broader population that the
  business is interested in.
  - This highlights the importance of understanding the limitations of your data
    and the potential blind spots in your model's predictions.

<center>

# 9 / 30: Interference and Spillovers Across Units

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides009.png){width=80%}

</center>

- **Problem**: The standard assumption in machine learning is that each unit's
  outcome is influenced solely by its own treatment.
  - In real-world scenarios like _marketplaces_, _pricing strategies_, and
    _social networks_, this assumption often doesn't hold true. Here, the
    actions or treatments applied to one unit can affect others, leading to
    interference or spillovers.

- **Example**: Consider a situation where a discount is offered exclusively to
  group A.
  - This discount might lead to a reduction in purchases by group B, a
    phenomenon known as "cannibalization."
  - This happens because both groups might be competing for the same limited
    resources or are interconnected through a social network.
  - As a result, group B cannot serve as a proper comparison or counterfactual
    for group A, complicating the analysis of the treatment's effect.

- **Key idea**: When the action of one unit influences the outcome of another,
  it introduces bias into the estimation of the treatment effect.
  - This bias persists even if the predictive model itself is highly accurate.
  - Understanding and accounting for these interactions is crucial for making
    reliable inferences in such interconnected systems.

<center>

# 10 / 30: Simpson's Paradox

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides010.png){width=80%}

</center>

- **Simpson's Paradox**: This is a statistical phenomenon where a trend that
  appears in different groups of data reverses when these groups are combined.
  It highlights how misleading aggregated data can be, as it may hide or distort
  the true relationships present in the subgroups.

- **Example**: Consider a study on a drug's effectiveness:
  - **Male Group**: With the drug, 93% recover (81 out of 87), while without it,
    87% recover (234 out of 270).
  - **Female Group**: With the drug, 73% recover (192 out of 263), while without
    it, 69% recover (55 out of 80).
  - **Combined Group**: When both groups are combined, the recovery rate with
    the drug is 78% (273 out of 350), but without the drug, it is 83% (289 out
    of 350). This suggests the drug is less effective when looking at the
    combined data, which contradicts the subgroup findings.

- **Graph Explanation**: The diagram illustrates the relationships between
  gender, drug choice, and recovery. Gender influences both the likelihood of
  receiving the drug and the recovery outcome, creating a confounding effect.

- **Key Insight**: This paradox shows that a model or conclusion that seems
  correct when looking at the overall data can be misleading or incorrect when
  applied to individual segments. It underscores the importance of analyzing
  data at multiple levels to avoid incorrect conclusions.

<center>

# 11 / 30: Berkson's Paradox

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides011.png){width=80%}

</center>

- **Definition**: A _collider_ is a variable that is affected by two or more
  independent causes. Think of it as a point where different influences meet.
  For example, if two separate factors both lead to a particular outcome, that
  outcome is the collider.

- **Fact**: When we condition on a collider, it can create a false or misleading
  association between the causes. This phenomenon is known as Berkson's paradox.
  Essentially, by focusing on the collider, we might mistakenly see a connection
  between the causes that doesn't actually exist.

- **Example**: Consider a workplace scenario where both statistics skill and
  flattery influence who gets promoted. In the general population, these two
  traits are independent. However, if we only look at those who are promoted, we
  might notice that those who are not skilled in statistics tend to be good at
  flattery. This negative association is an illusion created by conditioning on
  the collider (promotion).

- **Key idea**: It's crucial to understand that conditioning on the wrong
  variable can create a false correlation. This means that even if we include a
  variable in our analysis, it might not help us understand the true causal
  relationships. Instead, it can lead us to believe there's a connection where
  none exists. This highlights the importance of careful variable selection in
  data analysis to avoid drawing incorrect conclusions.

<center>

# 12 / 30: Discarding Domain Knowledge and Mechanisms

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides012.png){width=80%}

</center>

- **Problem**: When we rely solely on correlation-based models, we often ignore
  important domain knowledge, such as the underlying structure, physics,
  economics, or causal relationships. This means that instead of using what we
  already know about how things work, we let the model find patterns in the
  data, which might not always be meaningful or correct.
  - **No principled way to inject constraints or priors**: Without a way to
    incorporate known constraints or prior knowledge, the model might make
    decisions based on irrelevant or misleading patterns.

- **Example**: Consider a classifier designed to distinguish between wolves and
  huskies. It might achieve high accuracy by focusing on the presence of _snow_
  in the background of images, rather than the actual features of the animals.
  - **Accurate for the wrong reason**: The model performs well in the test
    environment but fails when conditions change, such as when there is no snow.
    This makes the model unreliable and not generalizable.

- **Key idea**: A model that ignores the underlying mechanisms of the data will
  inherit all the quirks and biases present in the training data. This can lead
  to incorrect predictions and a lack of trust in the model's decisions. It's
  crucial to consider how the data was collected and to incorporate domain
  knowledge to build more robust and reliable models.

<center>

# 13 / 30: Point Estimates Without Error Bars

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides013.png){width=80%}

</center>

- **Problem**: In many business scenarios, we deal with "small data" problems
  where there is a lot of uncertainty. However, typical machine learning models
  often give us a single number as if it were completely accurate.
  - These models do not provide error bars, posterior distributions, or any
    indication of how much the estimate might be off. This can be misleading
    because it doesn't show the potential range of outcomes.

- **Example**: Consider a demand forecast that predicts _"1,200 units next
  month"_. This number alone doesn't tell us if the actual demand could be
  anywhere between 1,100 and 1,300 units or as wide as 400 to 3,000 units.
  - These different ranges would lead to very different decisions about how much
    inventory to keep. Without knowing the range, businesses might either
    overstock or understock.

- **Example**: If a model predicts that a stock price will increase by 1%, the
  actions you take depend heavily on the prediction's uncertainty.
  - If the prediction is 1% with a margin of error of +/- 2% at a 95% confidence
    level, it suggests ignoring the prediction because the range is too wide.
  - Conversely, if the prediction is 1% with a margin of error of +/- 0.01% at
    the same confidence level, it suggests a high level of certainty, making it
    a good opportunity to buy.

- **Key idea**: Decision-makers need to understand the spread or range of an
  estimate just as much as they need to know the central value. This helps in
  making informed decisions by considering the uncertainty involved.

<center>

# 14 / 30: Epistemic vs Aleatoric Uncertainty Conflated

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides014.png){width=80%}

</center>

- **Problem**: Standard models often combine two distinct types of uncertainty
  into a single metric.
  - _Aleatoric uncertainty_ refers to the inherent randomness in the outcome
    itself. This type of uncertainty is unavoidable and is due to the inherent
    variability in the process. For example, the result of a fair coin flip is
    inherently uncertain and cannot be predicted with certainty.
  - _Epistemic uncertainty_ arises from a lack of knowledge or data. This type
    of uncertainty can be reduced by gathering more information or using a
    better model. For instance, predicting the prevalence of a rare disease with
    only a few recorded cases involves high epistemic uncertainty because the
    data is insufficient.

- **Importance of Separation**: If a model does not distinguish between these
  uncertainties, it might fail to recognize situations it has never encountered
  before. This can lead to overconfidence in predictions, especially in
  unfamiliar scenarios where the model should actually be more cautious.

- **Example**: Consider a fraud detection model that predicts a low risk for a
  new transaction pattern. This low risk could mean:
  - The transaction is genuinely low risk, reflecting aleatoric uncertainty.
  - The model has never encountered this pattern before, indicating epistemic
    uncertainty.

- **Key Idea**: Epistemic uncertainty can be reduced by collecting more data,
  whereas aleatoric uncertainty cannot. Treating both uncertainties as a single
  value can mislead decisions about when additional data collection is
  necessary. Understanding the difference helps in making informed decisions
  about model improvement and data gathering.

<center>

# 15 / 30: No Abstention: Systems That Never Say "I Don't Know"

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides015.png){width=80%}

</center>

- **Problem**: A standard classifier or regressor is designed to always provide
  an output, regardless of whether the input data is similar to what it has seen
  during training.
  - This means there is no built-in mechanism for the system to abstain from
    making a decision or to defer the decision to another process or human when
    it encounters unfamiliar data.
  - This can lead to unreliable or incorrect decisions, especially when the
    input data is significantly different from the training data.

- **Example**: Consider a loan-approval model that is trained on a specific set
  of applicant profiles.
  - If this model encounters an applicant profile that is very different from
    any it has seen before, it will still produce a confident decision—either
    approval or denial.
  - Ideally, in such uncertain situations, the model should be able to recognize
    its limitations and refer the case to a human expert for further evaluation.

- **Key idea**: Decision systems that lack the ability to express uncertainty or
  say _"I don't know"_ are not suitable for making critical decisions.
  - In high-stakes scenarios, such as financial approvals or medical diagnoses,
    the inability to defer uncertain cases can lead to significant errors and
    consequences.
  - Trust in automated systems can be improved by incorporating mechanisms that
    allow them to acknowledge uncertainty and seek human intervention when
    necessary.

<center>

# 16 / 30: Overfitting and the Statistical Significance Traps

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides016.png){width=80%}

</center>

- **Problem**: Overfitting occurs when a model learns the noise in the training
  data instead of the actual signal. This happens because there are no
  constraints or assumptions to limit how well the model fits the data. Without
  these boundaries, the model can become too complex and perform poorly on new,
  unseen data.

- **Statistical significance traps** make overfitting worse:
  - _P-hacking_: This is when researchers repeatedly test their data until they
    find a statistically significant result (p-value less than 0.05). This
    practice increases the likelihood of finding false positives, meaning
    results that appear significant but are actually due to chance.
  - _Multiple comparisons_: When many tests are conducted simultaneously, the
    probability of finding at least one statistically significant result by
    chance increases. This can lead to misleading conclusions.
  - _Burning the test set_: If the same test data is used repeatedly for model
    tuning, it effectively becomes part of the training data. This means the
    model is no longer being evaluated on truly unseen data, leading to
    overfitting.

- **Key idea**: Overfitting is not just a one-time error. It builds up over time
  as the same data is used repeatedly for model evaluation and tuning. Each
  additional look at the data increases the risk of overfitting, making it
  crucial to use proper validation techniques and avoid common pitfalls.

<center>

# 17 / 30: Optimizing the Wrong Objective

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides017.png){width=80%}

</center>

- **Problem**: In machine learning, models often focus on optimizing a _proxy
  metric_ like clicks or accuracy. These metrics are easier to measure but don't
  always align with the true business goals, such as increasing revenue,
  improving customer retention, or enhancing user wellbeing. This misalignment
  can lead to models that perform well on paper but don't actually benefit the
  business in meaningful ways.

- **Definition**: _Goodhart's law_ is a concept that highlights a common pitfall
  in optimization. It states that when a proxy metric becomes the target of
  optimization, it loses its effectiveness as a true measure of success. This
  happens because the model starts to exploit the metric rather than genuinely
  improving the underlying business outcome.

- **Example**: Consider a recommendation system that is optimized solely for
  click-through rate. While it might increase the number of clicks, it could do
  so by promoting sensational or misleading content. This might boost short-term
  engagement but can harm long-term user trust and satisfaction, which are more
  important for sustained business success.

- **Key idea**: The metric you choose to optimize becomes the de facto goal of
  your business. This means that if you focus on the wrong metric, you might
  achieve high performance in that area but fail to meet the actual business
  objectives you intended to address. It's crucial to ensure that the metrics
  you optimize align closely with your true business goals.

<center>

# 18 / 30: Symmetric Losses for Asymmetric Errors

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides018.png){width=80%}

</center>

- **Problem**: The issue with standard loss functions like log-loss and mean
  squared error is that they assume all errors are equal in size and importance.
  - In real-world applications, especially in business, not all errors have the
    same impact. Some errors can be more costly than others, and treating them
    equally can lead to suboptimal decisions.

- **Example**:
  - In stock return predictions, a false negative (failing to predict a loss)
    can be more damaging than a false positive (predicting a loss that doesn't
    happen). This is because there's a limit to how many losses one can endure,
    but no limit to gains.

- **Example**:
  - In fraud detection, the cost of a false negative (missing a fraud) is
    different from a false positive (flagging a legitimate transaction as
    fraud). A model that is 95% accurate but blocks many legitimate transactions
    can be very costly, despite its high accuracy.

- **Key idea**: It's crucial to incorporate cost asymmetry directly into the
  model's objective function. This means designing the model to account for
  different costs of errors from the start, rather than trying to adjust for
  these differences later in the decision-making process or after the model is
  deployed. This approach ensures that the model's decisions align better with
  real-world business priorities and costs.

<center>

# 19 / 30: Multi-Objective Decisions Under Constraints

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides019.png){width=80%}

</center>

- **@Problem@**: Real-world decisions often involve balancing multiple goals
  while adhering to various constraints such as budget, capacity, and legal
  requirements.
  - In many situations, it's not enough to use a single number or _scalar loss_
    to represent the outcome of a decision. This is because decisions often need
    to consider multiple factors and stakeholders, each with their own
    priorities and constraints.

- **@Example@**: Consider a hospital that needs to choose a cancer therapy. The
  decision involves weighing multiple factors such as the five-year survival
  rate, the quality of life for the patient, and the cost of the treatment.
  - There isn't a single "best" therapy option that works for everyone. The best
    choice depends on how much importance is placed on each of these factors.
    For instance, one therapy might be more cost-effective but offer a lower
    quality of life, while another might be more expensive but improve survival
    rates.

- **@Key idea@**: When we try to simplify a decision that involves multiple
  objectives into a single loss function, we risk losing sight of the trade-offs
  involved.
  - Instead of making these trade-offs clear, collapsing them into one number
    can obscure the different priorities and constraints that need to be
    considered. It's important to keep these trade-offs explicit to make
    informed and balanced decisions.

## From Scores to Actionable Decisions

- This section likely discusses how to move from evaluating options based on
  scores or metrics to making real-world decisions that take into account the
  complexities and constraints of the situation.

<center>

# 20 / 30: Black-Box Scores Are Not Recommendations

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides020.png){width=80%}

</center>

- **Problem**: The main issue with black-box scores is that they can rank or
  evaluate units (like customers or cases) but do not provide any actionable
  insights or reasons behind the scores. This means that while you might know
  how something is ranked, you don't know what actions to take or why it is
  ranked that way. This lack of transparency can be problematic when trying to
  make informed decisions.

- **Example**: Consider a churn score, which predicts the likelihood of a
  customer leaving a service. A score might tell you that a customer has a high
  probability of churning, say 0.8, but it doesn't tell you what you can do to
  prevent it. A more useful recommendation would be specific, such as suggesting
  that offering a discount could reduce the churn probability by 12 points. This
  example highlights the importance of identifying the _lever_ (the action to
  take), the _effect_ (the expected outcome), and the _unit_ (the specific
  customer or case).

- **Fact**: In fields like credit, hiring, and healthcare, there is a growing
  demand for explanations alongside scores. Regulators and stakeholders require
  these explanations to ensure that decisions are fair, transparent, and
  justifiable. Simply providing a score without context or reasoning is often
  not sufficient.

- **Key idea**: For a prediction to be truly useful, it must come with a
  recommendation that includes an actionable lever and an explanation. A bare
  prediction, without these elements, falls short of providing the guidance
  needed to make informed decisions. This underscores the importance of moving
  beyond just scores to include actionable insights and explanations.

<center>

# 21 / 30: The Cost of Solving Sub-Problems Separately

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides021.png){width=80%}

</center>

- **Problem**: In many decision-making processes, we often break down the
  problem into smaller parts and optimize each part separately. For example, we
  might have a prediction model that forecasts future events, and then we use a
  separate rule to decide what actions to take based on those predictions. This
  approach can be inefficient because each part is optimized without considering
  the overall goal.

- **Example**: Consider an inventory system where we first predict how much of a
  product will be needed and then use a fixed rule to decide when to reorder.
  Even if the prediction is accurate, the system might not perform well overall
  because the reorder rule doesn't adapt to changes in demand or inventory
  costs. A better approach would be to train the system to directly minimize the
  total inventory cost, considering both prediction and action together.

- **Fact**: Research shows that machine learning models that are trained
  end-to-end, meaning they optimize the entire process from prediction to action
  as a single unit, tend to perform better than systems where each part is
  optimized separately. This is true for decision-making systems as well, where
  the goal is to make the best possible decision based on available data.

- **Key idea**: When we optimize each part of a decision-making process in
  isolation, we miss out on potential improvements that come from considering
  how each part interacts with the others. The overall decision-making process
  is not necessarily optimized just because each individual part is.

<center>

# 22 / 30: The Static-World Assumption Breaks

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides022.png){width=80%}

</center>

- **Problem**: When we use machine learning models, we often assume that the
  world stays the same as when the model was trained. However, in reality, any
  decision or change can alter the world, which means the data distribution the
  model was trained on might no longer be valid. This is known as the
  "static-world assumption" breaking.

- **Three ways the world moves out from under a static model**:
  - _Concept shift_: This occurs when the relationship between inputs and
    outcomes changes. For example, the probability of an outcome given certain
    inputs, $\Pr(Y | X)$, is different now.
  - _Covariate shift_: Here, the input distribution $\Pr(X)$ changes, but the
    relationship between inputs and outcomes remains the same.
  - _Label shift_: This happens when the distribution of outcomes $\Pr(Y)$
    itself changes, regardless of the inputs.

- **Example**: Consider a card-fraud detection model trained on last year's
  data.
  - _Concept shift_: If fraudsters change their tactics, a transaction pattern
    that was once safe might now indicate fraud, altering $\Pr(Y | X)$.
  - _Covariate shift_: If contactless payments become more common, the input
    distribution $\Pr(X)$ changes, even if fraud tactics remain the same.
  - _Label shift_: If a data breach occurs, the overall fraud rate might
    increase, changing $\Pr(Y)$.
  - The model cannot detect these shifts on its own, which can lead to poor
    performance.

- **Example**: A house-price prediction model trained on data before the
  pandemic.
  - Remote work changes the value of commute distance, representing a _concept
    shift_.
  - Lower interest rates increase average sale prices, causing a _label shift_.

- **Key idea**: Models that understand the underlying _causal mechanisms_ rather
  than just patterns tend to perform better when the data distribution changes.
  This is because causal mechanisms are generally more stable than surface-level
  correlations, allowing the model to adapt more gracefully to changes.

<center>

# 23 / 30: Feedback Loops and Bias Amplification

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides023.png){width=80%}

</center>

- **Problem**: The main issue here is that when a model makes predictions, those
  predictions can influence the world in a way that changes the data it will see
  in the future. This means that the model is not just passively observing the
  world but actively shaping it. As a result, the data it uses for retraining is
  affected by its own previous predictions, which can lead to problems if not
  managed carefully.

- **Example**:
  - Consider a recommender system that suggests sensational content because it
    gets more clicks. This leads to more sensational content being clicked on,
    which then becomes part of the training data for the next iteration of the
    model. As a result, the model continues to recommend even more sensational
    content, creating a cycle that amplifies the initial bias towards
    sensationalism.
  - In another scenario, if a neighborhood is over-policed, it results in more
    arrests. This arrest data is then used to train a model that identifies the
    neighborhood as high-risk, which justifies further policing. This cycle
    continues, reinforcing the initial bias and potentially leading to unfair
    treatment of the neighborhood.

- **Key idea**: The core concept here is that feedback loops can take a small
  initial bias and make it grow over time. This happens because the model is
  continuously trained on data that is influenced by its own past decisions.
  It's important to recognize and address these feedback loops to prevent biases
  from becoming more pronounced and leading to unfair or inaccurate outcomes.

<center>

# 24 / 30: Performativity: When the Prediction Changes the Outcome

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides024.png){width=80%}

</center>

- **Definition**: The term _performativity_ refers to a situation where a
  prediction itself influences the outcome it is trying to predict. This means
  that the act of making a prediction can change the reality of what is being
  predicted.

- **Example**: Consider a credit-risk score that is published. When borrowers
  see their scores, they might change their behavior, such as by paying off
  debts more quickly or avoiding new loans. This change in behavior can alter
  the actual default rate, which is the very thing the score was initially
  trying to predict. Thus, the prediction has influenced the outcome.

- **Example**: Think about a navigation app that suggests a particular route as
  the fastest. If many drivers follow this suggestion, the road can become
  congested, making it no longer the fastest route. The prediction that
  attracted the drivers ends up being invalidated by their collective response.

- **Key idea**: When predictions are performative, the relationship between the
  predicted outcome (Y) and the input features (X) is not stable. Instead, it
  becomes dependent on which predictive model is being used. This means that the
  model's deployment can change the very dynamics it is supposed to predict,
  making it a moving target rather than a fixed one.

<center>

# 25 / 30: No Exploration: Trapped in the Logged Policy

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides025.png){width=80%}

</center>

- **Problem**: When a model is built solely on observational data, it lacks the
  ability to explore beyond the actions recorded in the data. This means it is
  _trapped_ within the confines of the policy that generated the data.
  - The model cannot predict the outcomes of actions that were never taken in
    the past. This is known as a violation of _overlap_ or _positivity_.
    Essentially, if an action wasn't part of the historical data, the model has
    no basis to understand its effects.

- **Example**: Consider a pricing model that has been trained using historical
  data where prices never went below $20. This model is unable to predict what
  might happen if the price were set at $15 because it has no data to learn from
  at that price point. No matter how much data is available, if it doesn't
  include prices below $20, the model remains uninformed about lower prices.

- **Key idea**: To answer certain business questions, merely accumulating more
  historical data isn't enough. Instead, _deliberate intervention_ is necessary.
  This means actively trying new actions or strategies to gather data on their
  effects, which can then inform the model about scenarios not covered by past
  data.

<center>

# 26 / 30: Delayed and Long-Horizon Effects

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides026.png){width=80%}

</center>

- **Problem**: When we create a model that focuses on achieving immediate
  results, it often overlooks the long-term effects of its actions. This means
  the model might not be able to properly evaluate how its decisions impact
  future outcomes. Essentially, it struggles to connect current actions with
  their future consequences.

- **Example**: Consider a support team that is evaluated based on how quickly
  they can close support tickets. If their main goal is speed, they might close
  tickets without fully resolving the customer's issue. While this might look
  good in the short term, the real problem surfaces later. Customers might
  repeatedly complain or lose trust in the company, which is reflected in
  different metrics that appear months down the line.

- **Example**: A collections agency might focus on recovering as much money as
  possible in the current quarter. To do this, they might enforce strict
  repayment plans. However, these plans could lead to borrowers defaulting
  later. While the agency might see a temporary increase in recovered funds, it
  could suffer from a lower overall repayment rate and damage to its reputation
  in the long run.

- **Key idea**: It's important to recognize that short-term goals and long-term
  business objectives might not always align. Businesses should focus on the
  outcomes that truly matter to them, which are often the long-term results
  rather than the immediate gains.

<center>

# 27 / 30: Strategic and Adversarial Response

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides027.png){width=80%}

</center>

- **Strategic and Adversarial Response**: This slide discusses how people or
  entities might change their behavior once they know how a machine learning
  model evaluates them. This is important because it can lead to the model's
  predictions becoming less accurate over time.
  - **Problem**: Once a model is in use, people who are being evaluated by it
    may try to game the system to get better scores. Traditional machine
    learning assumes that people won't change their behavior in response to the
    model, but in real-world situations, especially in business, people often
    do.

  - **Example**: If the details of a credit-scoring model are made public,
    people might manipulate their financial behavior to improve their credit
    scores without actually becoming more creditworthy. Similarly, if a search
    engine's ranking algorithm is known, website owners might overuse certain
    keywords to improve their site's ranking, even if it doesn't improve the
    site's quality.

  - **Example**: If a tax-audit model flags tax returns with income above a
    certain threshold, self-employed individuals might report their income just
    below that threshold to avoid being audited, once they know the rule.

  - **Key idea**: A model that is trained on data from before it was deployed
    might not work well after deployment if people change their behavior in
    response to the model. This is because the model's predictions are based on
    past behavior, which may no longer be relevant.

- **Why This Matters**: Understanding strategic and adversarial responses is
  crucial for maintaining the effectiveness of machine learning models in
  dynamic environments. It highlights the need for continuous model updates and
  the consideration of human behavior in model design.

- **Roadmap**: This section likely outlines the steps or topics that will be
  covered next to address the issues of strategic and adversarial responses in
  machine learning.

<center>

# 28 / 30: Why AI Projects Fail

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides028.png){width=80%}

</center>

- **Most AI projects fail not because of failures at the modeling phase, but
  because they frame the problems incorrectly**
  - **Misalignment**: Often, AI models are designed to optimize a _proxy_ metric
    rather than the actual business goal. This means that while the model might
    perform well according to certain metrics, it doesn't necessarily contribute
    to the desired business outcomes. For example, a model might focus on
    increasing clicks rather than actual sales.
  - **Black boxes**: AI models can sometimes be complex and difficult to
    understand. When the outputs of a model cannot be easily explained,
    stakeholders may not trust or adopt the model's recommendations. This lack
    of transparency can hinder the integration of AI solutions into business
    processes.
  - **No lever**: Delivering a score or prediction without a clear action plan
    can render the model ineffective. Businesses need actionable insights, not
    just data points, to make informed decisions. If a model predicts customer
    churn but doesn't suggest retention strategies, it falls short.
  - **No feedback**: After deploying an AI model, it's crucial to monitor its
    performance continuously. Without feedback loops, there's no way to know if
    the model is still effective or if it needs adjustments. Continuous
    evaluation ensures the model remains aligned with business goals and adapts
    to changes over time.

- **Any accurate model that answers the wrong question is a failed project,
  however good its metrics look on a dashboard**
  - This point emphasizes that even if a model performs well according to
    technical metrics, it is considered a failure if it doesn't address the
    right business problem. It's crucial to ensure that the model's objectives
    align with the organization's goals to truly add value.

<center>

# 29 / 30: The Root Cause of the Four Costs

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides029.png){width=80%}

</center>

- **The Root Cause of the Four Costs**: This slide discusses the underlying
  issue that leads to four specific costs in decision-making processes. These
  costs arise when we focus too much on making accurate predictions without
  considering how these predictions affect the decisions we make.

- **Four Costs**: The costs mentioned are related to ignoring important factors
  like causality, uncertainty, the business objective, and dynamics. These are
  crucial elements that should be considered when making decisions based on
  data.

- **Root Cause**: The main problem is that we often optimize for prediction
  accuracy using a fixed data distribution. However, in reality, the decisions
  we make can change the distribution itself. This means that focusing solely on
  prediction accuracy can lead to poor decision quality.

- **Solution**: The book suggests using causal and probabilistic methods to
  address these issues. These approaches help in understanding the
  cause-and-effect relationships and the probabilities of different outcomes,
  leading to better decision-making.

- **Decision Loop**: The graph shows a loop where data is used to build a model,
  which informs a policy. This policy leads to actions, and the outcomes of
  these actions provide feedback. This feedback is then used to update the data,
  creating a continuous improvement cycle. This loop emphasizes the importance
  of adapting and retraining models based on new information to improve decision
  quality over time.

<center>

# 30 / 30: Book Roadmap

</center>

<center>

![](book_springer/lecture_commentary/Lesson02.1_From_Data_Science_To_Decision_Science.png/slides030.png){width=80%}

</center>

- **Book Roadmap**

* **The rest of the book builds the pipeline that proposes solutions for the
  problem highlighted in this chapter**
  - _Part II: Advanced Modeling Theory & Tools_ provides the essential tools and
    theories needed for understanding and building machine learning models. This
    includes:
    - **Knowledge Representation**: How to structure and represent information
      in a way that machines can understand.
    - **Probabilistic ML**: Focuses on Bayesian inference and understanding
      uncertainty in predictions, which is crucial for making informed
      decisions.
    - **Causal ML**: Involves Structural Causal Models (SCMs), do-calculus, and
      causal discovery, which help in understanding cause-and-effect
      relationships rather than just correlations.
  - _Part III: Data_ focuses on transforming domain knowledge into causal
    Directed Acyclic Graphs (DAGs) and creating causal data pipelines. It also
    addresses challenges like:
    - **Selection Bias**: Ensuring that the data used is representative and not
      skewed.
    - **Distribution Shift**: Handling changes in data distribution over time,
      which can affect model performance.
  - _Part IV: Decision-Making Theory & Tools_ translates causal models into
    actionable decisions. It covers:
    - **Decision Theory**: The study of principles and methods for making
      logical choices.
    - **Taxonomy of Decision Problems**: Categorizing different types of
      decision-making scenarios.
    - **Simple Decisions**: Includes methods like bandits and reinforcement
      learning (RL) for straightforward decision-making tasks.
    - **Complex Decisions**: Involves more advanced techniques like policy
      gradients and multi-agent systems for handling intricate decision-making
      processes.
    - **Agentic Causal Reasoning**: Understanding how agents can make decisions
      based on causal reasoning.
  - _Part V: Implementation, Deployment & Governance_ deals with the practical
    aspects of putting models into use, including:
    - **Stakeholder Alignment**: Ensuring that all parties involved have a
      shared understanding and goals.
    - **Deployment/Monitoring/Adaptation**: The process of launching models,
      keeping track of their performance, and making necessary adjustments.
    - **Trust, Explainability, Fairness, and Governance**: Building models that
      are transparent, fair, and adhere to ethical standards, which is crucial
      for gaining user trust and meeting regulatory requirements.
