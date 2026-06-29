# 1. Trusting a Prediction Is Not the Same as Trusting a Model
- **Idea**
  - "Should I trust this prediction?" and "Can I trust this model?" are two
    distinct questions that need different forms of evidence
  - A model can be reliable in aggregate yet fail catastrophically on a specific
    input, or be right on cases a human cannot understand
  - Trust is decomposed into local trust (per-prediction) and global trust
    (per-model)

- **Why it is interesting**
  - Most ML evaluation collapses trust into a single number (accuracy on
    held-out data), hiding the fact that trustworthiness is not monolithic
  - Separating the two questions reframes evaluation: a doctor acting on one
    diagnosis needs local trust; deploying the system in a hospital needs global
    trust
  - It exposes why aggregate metrics can mislead a decision-maker who actually
    cares about one case in front of them

- **Reflections**
  - _If a model is trustworthy on average but wrong on the case you face, was
    the average ever the right thing to optimize?_

# 2. Any Black Box Is Locally Linear
- **Idea**
  - However complex a global decision boundary is, in a small neighborhood
    around one instance it can be approximated by a simple, sparse linear model
  - LIME perturbs the input around an instance, observes how the black box
    output changes, and fits an interpretable model weighted by proximity to the
    instance

- **Why it is interesting**
  - It sidesteps the false dilemma of "accurate but opaque" vs "simple but
    weak": you keep the complex model and explain it locally
  - The method is model-agnostic, treating the classifier as a queryable
    function with no access to weights or architecture, so it works on neural
    nets, SVMs, random forests alike
  - It is essentially the intuition of calculus (local linearization) repurposed
    as an interpretability tool

- **Reflections**
  - The explanation is an artifact of the chosen neighborhood and sampling, not
    an objective property of the model
  - _A different locality could explain the same prediction differently, which
    means "the" explanation does not exist_

# 3. The Fidelity-Interpretability Tradeoff
- **Idea**
  - An explanation must be both faithful to what the complex model actually does
    (fidelity) and simple enough for a human to grasp (interpretability)
  - These two goals pull against each other: the more you simplify, the more you
    risk misrepresenting the real decision logic

- **Why it is interesting**
  - Challenges the common assumption that a simpler surrogate model is
    automatically a better explanation
  - Makes explicit a tradeoff usually left implicit, turning "explainability"
    from a vague virtue into an optimization problem with a defined objective

- **Reflections**
  - _If high fidelity requires complexity and humans need simplicity, is a fully
    faithful and fully human-readable explanation even possible?_

# 4. The Husky-vs-Wolf Snow Detector
- **Idea**
  - A neural net classifying huskies vs wolves achieved high accuracy by
    detecting snow in the background, not features of the animals
  - Huskies appeared in snowy photos, wolves did not, so the model learned the
    dataset artifact instead of the concept

- **Why it is interesting**
  - A dramatic demonstration that high accuracy can coexist with a completely
    wrong reason, which no accuracy metric would ever reveal
  - Explanations expose not model cleverness but dataset bias: the classifier is
    a "good" snow detector masquerading as an animal classifier
  - Reframes the question from "is the model accurate?" to "is the model right
    for the right reasons?"

- **Reflections**
  - _How many deployed high-accuracy models are actually exploiting a spurious
    correlation nobody has looked for?_

# 5. Non-Experts Can Debug Models with Explanations
- **Idea**
  - In human-subject experiments, people with no ML expertise used LIME
    explanations to spot spurious features and pick the better classifier, and
    even to improve a model by removing bad features
  - Without explanations users chose the better model far less often than with
    them

- **Why it is interesting**
  - Interpretability is not just a transparency luxury; it is a practical tool
    that lets humans improve systems they could not otherwise reason about
  - It redistributes ML quality control from experts inspecting internals to
    laypeople inspecting explanations
  - Shows explanations close a loop: human judgment feeds back into model
    selection and feature engineering

- **Reflections**
  - _If a non-expert with explanations beats an expert without them, where does
    real ML expertise actually live?_

# 6. Submodular Pick: Explain the Model with a Handful of Cases
- **Idea**
  - SP-LIME selects a small, diverse, non-redundant set of instances whose
    explanations together cover the breadth of the model's behavior
  - It uses submodular optimization to maximize coverage of important features
    while avoiding instances that explain the same thing twice

- **Why it is interesting**
  - Makes global understanding tractable: instead of reading hundreds of
    explanations, a human inspects a dozen well-chosen ones
  - Treats "understanding a model" as a coverage problem, borrowing discrete
    optimization to budget scarce human attention
  - Bridges local explanations (per-instance) up to global trust (per-model)

- **Reflections**
  - _Choosing which examples to show is itself an editorial act, what gets left
    out shapes the human's mental model of the system_

# 7. Accuracy Can Mask Serious Flaws
- **Idea**
  - A classifier with high held-out accuracy can rely on nonsensical or
    dataset-dependent logic, which surfaces only when individual predictions are
    explained
  - Validation accuracy and real-world trustworthiness can diverge sharply

- **Why it is interesting**
  - A pointed critique, ahead of its time in 2016, of ML's fixation on a single
    aggregate metric
  - Suggests that metrics divorced from interpretability give a false sense of
    safety, especially under distribution shift between training and deployment
  - Connects interpretability to robustness: explanations can reveal when a
    model leans on artifacts that will not survive a change in data distribution

- **Reflections**
  - _Accuracy answers "how often is it right on this data?" but the deployment
    question is "why is it right, and will those reasons hold tomorrow?"_
