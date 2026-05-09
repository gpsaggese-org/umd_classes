# Project narrative: what we built and why

This document walks through every stage of the AI-Powered Technical Debt
Quantification and Remediation pipeline. For each stage, it answers four
questions: what does this stage do, why does it exist, how does it work,
and what did we get when we ran it.

It's meant for someone who already read the README and saw the demo, and
now wants to understand the choices behind the architecture. The
README tells you how to run the pipeline. The LIMITATIONS file tells
you what doesn't work yet. This file tells you the story of why the
pipeline looks the way it does.


## The problem

Technical debt is the cost a software team pays later for shortcuts they
took earlier. A method written in a hurry that swallows exceptions, a
class that grew too big to navigate, a deprecated API still in use
years after a better one shipped. Every codebase accumulates debt, and
every team eventually has to choose between paying it down or letting
it slow them down.

The project description asks us to build a machine learning system that
finds debt automatically, predicts how risky each instance is, ranks
the issues by impact-to-effort ratio, suggests refactorings using a
language model, and validates that those refactorings actually compile
and pass tests. The system should work on real Java code with no manual
configuration beyond pointing it at a repository.

We chose to demonstrate this on commons-lang3, an Apache utility library
that's mature, public, and not in our training data. The pipeline is
designed to work on any Maven or Gradle Java project; commons-lang3 is
where we proved the foundation holds.


## Stage 1: Ingest

**What.** Clone the target repository and find its Java source root.

**Why.** Every later stage needs to know where the Java files live and
where the git history lives. Without those two paths, nothing else
works.

**How.** We use a pinned commit hash so the demo produces identical
issue counts on every run. If we cloned the latest commit, every run
of the notebook would show different numbers as the codebase evolved.
Source root detection looks for `src/main/java`, the standard Maven
layout that almost every Apache Java project uses.

**Result.** The pipeline gets two paths: the cloned repo at a known
commit, and the source root containing 259 Java files for commons-lang3.


## Stage 2: Analyze

**What.** Run a static analyzer over every Java file and collect a list
of issues.

**Why.** Static analyzers know hundreds of patterns that correlate with
bugs, bad style, or maintainability problems. Things like methods that
return `null` where an empty list would be safer, exception handlers
that swallow errors silently, unused imports. Detecting these by hand
across a codebase isn't feasible; a tool that knows the patterns is.

**How.** We use PMD, an open-source static analyzer for Java. PMD reads
Java source files and flags every place a known rule is violated. We
chose PMD over SonarQube because PMD runs fully offline with no server,
which means the pipeline works on any machine without setup. SonarQube
would have given us richer metrics but would have required running a
local server, which goes against the project's open-source spirit. We
configure PMD with three rulesets: quickstart (general best practices),
performance, and security.

**Result.** PMD found 522 issues across the 259 Java files in
commons-lang3. Each issue carries a rule name, file, line number, and
priority from 1 (most severe) to 5 (least severe).


## Stage 3: Classify

**What.** Sort each PMD issue into one of five categories from the
project description: code smells, architectural violations, performance
issues, outdated patterns, and concurrency issues.

**Why.** A raw PMD rule name like AvoidCatchingGenericException doesn't
tell a team lead anything. A category does. The project description
specifically asks for these five categories, so we need a mapping from
PMD's vocabulary to the project's vocabulary.

**How.** Namratha built a CSV that maps every one of the 301 PMD rules
to a category by hand. Stage 3 just looks each issue's rule up in the
CSV and tags it. This is rule-based, not a trained classifier; the
manual mapping itself is the ground truth.

**Result.** On commons-lang3: 376 code smells, 89 architectural
violations, 55 performance issues, 2 concurrency issues, 0 outdated
patterns. Most issues land in code smells because that's what PMD's
quickstart ruleset is best at finding.


## Stage 4: Predict fault probability

**What.** For every issue, attach a probability that the host commit
(the commit where the issue was last touched) is bug-inducing.

**Why.** Rule severity alone isn't enough to rank issues. A
high-severity issue in a file that's never modified matters less than
a medium-severity issue in a hot, recently-touched file. We want a
single number that combines rule severity, code complexity, and
churn.

**How.** We trained an XGBoost classifier on the Lenarduzzi V2 Technical
Debt Dataset. XGBoost is a gradient-boosted tree algorithm that's
strong at tabular classification problems with mixed numeric features.
The Lenarduzzi V2 dataset is a 1.4 GB SQLite database of 30 Apache Java
projects with bug labels, Jira issues, commit history, and SonarQube
measurements pre-joined together. The bug labels come from the SZZ
algorithm, which traces every bug-fix commit backward through git
history to identify which earlier commit introduced the bug.

The classifier learns from 24 features: 19 SonarQube-style code metrics
(cyclomatic complexity, lines of code, code smell count, technical
debt index, and so on) plus 5 churn features (lines added, lines
removed, number of authors, commit count, file age). We held out
commons-io as the test set, the same protocol we use for the
regression models in the next section.

**Result.** Holdout AUC of 0.884. AUC is a metric for ranking quality:
0.5 is random, 1.0 is perfect, and 0.884 means the classifier orders
risky commits well. On commons-lang3, the predicted probabilities range
from 0.10 to 0.60 with mean 0.32. The numbers are squashed compared to
what a freshly calibrated model would produce because we infer on
PMD-derived features instead of SonarQube features, but the relative
ranking is what matters and the ranking holds up.


## Stage 5: Prioritize

**What.** Rank the 522 issues by impact-over-effort and then pick the
issues on the Pareto front.

**Why.** With finite developer time, you want to fix issues with the
best return per unit of work first. A rule that takes 2 minutes to fix
and prevents a real bug beats a rule that takes 20 minutes and only
improves style.

**How.** We compute an impact score for each issue that combines fault
probability (from Stage 4), severity (from PMD's priority field), and
ruleset weight (Performance and Multithreading get a small boost
because they're customer-visible). We compute an effort estimate based
on PMD priority and ruleset, anchored on empirical effort medians from
992,704 issues in the Lenarduzzi dataset. Then we sort by impact
divided by effort.

The Pareto front is a multi-objective optimization concept. An issue
is on the Pareto front if no other issue has both more impact and less
effort. Anything not on the front is dominated by something else, so
you'd never pick it first. The Pareto front gives you the trade-off
frontier: pick any point on it depending on how much effort you can
spend.

**Result.** The top-ranked issues cluster in concurrency-heavy files
like ThreadUtils and LockingVisitors. Four issues land on the Pareto
front, representing genuine impact-vs-effort trade-offs. These are the
issues we send to Stage 6.


## The three regression models (a parallel analysis)

**What.** Three XGBoost regressors that estimate how technical debt
affects three project-level outcomes: defect density per file, issue
resolution time in hours, and team velocity in commits per developer
per month.

**Why.** The project description asks for these three specifically.
They give a team lead numbers that are useful in their own right
beyond just a list of issues. "Which file is going to be the next bug
magnet?" is a different question from "which open issue is most
urgent?", and both are worth answering.

**How.** Each model is trained on Lenarduzzi V2, with commons-io held
out, using log-transformed targets to handle long tails (some files
have hundreds of bugs, some Jira issues take 50 hours, etc.).

**Model A: defect density.** Predicts how many bug-inducing commits a
file accumulates over its lifetime. Features are pure churn metrics:
lines added, lines removed, commit count, distinct authors, file age,
test directory flag.

**Model B: resolution time.** Predicts hours to close a Jira issue.
Features are issue type, priority, votes, watch count, description
length, summary length.

**Model C: team velocity.** Predicts commits per developer per month
for a project-month. Features come from git (number of authors,
bug-inducing commit count, project age) and from SonarQube (NCLOC,
complexity, code smells, SQALE technical debt index).

**Result.** Holdout R² in log space: A is 0.78 (solid), B is -0.38
(worse than predicting the mean), C is 0.42 (modest). Model A's
top-10 predicted bug magnets in commons-io are FileUtils, IOUtils, and
FilenameUtils, which is exactly what someone familiar with commons-io
would expect. Model B's negative R² is an honest finding: TIME_SPENT
in Jira is self-reported and noisy, full of round-number guesses, and
the metadata features available don't capture the real drivers of
resolution time. Model C's predictions track the rough shape of
commons-io's actual velocity over 193 months, though the very tallest
spikes are under-predicted.

These three models sit beside the pipeline rather than inside it.
Model A could plausibly feed back into Stage 5's prioritization (its
features are computable from a fresh git clone), but Models B and C
need data that doesn't exist on a fresh clone (Jira for B, SonarQube
measurements for C).


## Stage 6: AI-powered refactoring

**What.** For the top-ranked issues, suggest a refactored version of
the affected method.

**Why.** This is the headline of the project. The description
specifically asks for code transformations with before-and-after
comparisons and confidence scores. Finding and ranking issues is only
half the value; suggesting fixes is the other half.

**How.** We use Qwen2.5-Coder-3B-Instruct, an open-source code
generation model from Hugging Face. Code generation models are
language models trained or fine-tuned specifically on source code, so
they understand syntax and idioms better than general-purpose models.
The prompt names the PMD rule, gives the rule's description, shows the
original method, and asks for a refactored version that preserves the
signature.

We picked the 3B model after running a benchmark across five candidates
and three prompting strategies. The candidates were
Qwen2.5-Coder-0.5B-Instruct, Qwen2.5-Coder-3B-Instruct, the general
Qwen2.5-3B-Instruct, Meta's Llama-3.2-3B-Instruct, and Microsoft's
Phi-3.5-mini-instruct. The strategies were zero-shot (just ask the
model to refactor), few-shot static (include three fixed example
refactorings in the prompt), and few-shot retrieval (include three
examples retrieved by similarity to the input). We measured each
combination on 1000 held-out CodeXGLUE Java refactoring pairs.
CodeXGLUE is a benchmark suite from Microsoft that includes paired
Java methods (buggy version, fixed version) drawn from real GitHub
commit history, so it's a realistic test of refactoring ability.

The metrics: exact match against the reference fix, mean BLEU score
against the reference (BLEU measures n-gram overlap, a standard
machine-translation metric that captures "how close did the model get"
even when the output isn't word-for-word identical), Java syntactic
validity (does the output parse as legal Java), and inference time per
generation.

Qwen2.5-Coder-3B with retrieval-based prompting led on mean BLEU (70.9)
and Java validity (98.7%), at 1.5 seconds per generation on the
benchmark hardware. Llama-3.2-3B lagged by 7 BLEU points across all
strategies. Phi-3.5-mini's Java validity was 78%, well below the Qwen
family's 97%-plus. The full results are saved as JSON files in
`production/data/benchmark_results/` and loaded into Section 4 of the
example notebook.

A practical constraint: the 3B model takes about 25 minutes per
generation on a Mac CPU. A single pipeline run with 10 issues would
take over 4 hours. To work around this we ran the 3B model once on the
UMIACS Nexus cluster using a GPU, saved 10 refactoring records to
JSON, and committed the JSON to the repo. The notebook loads these
saved records. The live laptop pipeline still runs end-to-end with the
smaller 0.5B model, so the system is reproducible without a GPU. The
professor and TA approved this approach in advance.

**Result.** For each of the 10 records, Stage 6 produces the original
method, the refactored method, a unified diff, BLEU score, signature
preservation flag, and a confidence label (HIGH, MEDIUM, or LOW). The
example we usually point to is
ReturnEmptyCollectionRatherThanNull, where the agent correctly
transformed `return null;` into `return new String[0];`. Signature
preserved, code parses, BLEU above 90, confidence HIGH.


## Stage 7: Validate

**What.** Take each suggested refactoring, splice it back into the
original file, and check that the project still compiles and the test
suite still passes.

**Why.** A refactoring that breaks the build isn't a refactoring, it's
a regression. We want a hard signal that the change is safe before
recommending it.

**How.** Stage 7 runs in two modes. Compile mode runs `mvn compile` on
the patched source and records pass or fail. This is fast (about 30
seconds per refactoring) and catches the obvious failures: syntax
errors, missing imports, type mismatches, references to methods that
no longer exist. Test mode runs `mvn test`, which executes the
project's full test suite. This catches the subtler failures: code
that compiles but produces wrong outputs, breaks an invariant, or
violates a contract some other piece of code depends on.

The test suite matters because it's the project's own definition of
correct behavior. The original commons-lang3 developers wrote about
58,000 small programs that each call a function with specific inputs
and verify the output. If our refactoring changes a method's logic in
a way that breaks even one test, the test suite catches it. Two
layers exist because compile mode is the cheap filter (a refactoring
that doesn't compile is dead on arrival) and test mode is the
expensive but rigorous final check.

**Result.** On our 10 Nexus 3B records, 8 pass compilation. The 2
that fail are AvoidCatchingGenericException and
UseLocaleWithCaseConversions, where the agent's refactoring removed
exception handling that surrounding code expected. We picked two
records to run end-to-end in test mode. Record 1
(ReturnEmptyCollectionRatherThanNull) passes all 57,939 tests.
Record 5 (CompareObjectsWithEquals) compiles cleanly but breaks two
tests because the agent's hashCode-based comparator doesn't match the
project's existing comparator semantics.

This gives a layered validation story: BLEU and signature checks catch
obvious problems cheaply, compilation is a stronger signal, and test
passing is the gold standard. Each layer filters out a different
class of false positive.


## Stage 8: Feedback

**What.** Log every refactoring attempt to a small SQLite database.

**Why.** The project description asks for a feedback loop that tracks
predicted versus actual impact of refactorings. Without storage there's
nothing to track.

**How.** Stage 6 writes a "refactored" event for every issue it
processes. Each event captures the original issue, the chosen
strategy, both candidate refactorings, the validation results from
Stage 7, and the confidence scores. The events go into
`production/data/feedback.sqlite` in a single `feedback` table with one
row per event. The query helpers (`get_summary_metrics`,
`get_success_rate_by_rule`, `get_per_repo_summary`) read from it for
reporting.

**Result.** After our test runs, the database holds 52 events covering
multiple refactoring attempts across the demo runs. The notebook shows
the most recent events directly from the database to demonstrate that
the infrastructure is real and populated.

Currently this is a write-only log. Closing the loop, retraining the
fault predictor on accumulated feedback or adjusting prioritization
based on per-rule success rates, would need many more refactoring
runs than fit in a single demo session. We documented closed-loop
learning as future work in the LIMITATIONS file.


## How the stages connect

The pipeline runs end-to-end as: clone the repo (Stage 1), find issues
(Stage 2), categorize them (Stage 3), score their risk (Stage 4),
rank them (Stage 5), refactor the top picks (Stage 6), validate the
results (Stage 7), and log everything (Stage 8). The three regression
models run alongside, reading from the same training data but feeding
project-level predictions rather than per-issue ones.

A typical run on commons-lang3 takes about 2 minutes for Stages 1
through 5, instant for Stage 6 in replay mode (loading the 10 Nexus
records from JSON), 5-10 minutes for Stage 7 in compile mode plus a
few extra minutes for the two records we test in test mode, and
milliseconds for Stage 8. The full demo notebook runs in about 15
minutes, end to end, on a Mac with the Docker container warmed up.

Each stage was built to be inspectable on its own. You can read PMD's
issue list before classification, see Stage 4's probability column
before prioritization runs, review Stage 6's diffs before Stage 7
validates them, and query the SQLite log directly to audit any past
event. Nothing is hidden behind a black-box endpoint; every
intermediate output is on disk and in the notebook.

That's the system. Eight pipeline stages, three regression models on
the side, one benchmark-driven model choice for the refactoring agent,
and a validation layer that catches real failures before they get
recommended. The README has the setup steps. The LIMITATIONS file has
the gaps. This file has the reasoning.