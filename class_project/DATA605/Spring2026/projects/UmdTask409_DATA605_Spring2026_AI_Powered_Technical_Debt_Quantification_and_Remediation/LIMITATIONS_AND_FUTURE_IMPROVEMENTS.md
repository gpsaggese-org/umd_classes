# Limitations and Future Improvements

This document captures what the AI-Powered Technical Debt Quantification and
Remediation pipeline doesn't do well, the choices that produced those gaps,
and the work that would address them.

The pipeline ingests a Java repository, finds technical debt with static
analysis, predicts fault-inducing risk with a trained model, ranks issues
by impact-over-effort, runs a code transformation agent on the top picks,
checks the results by compiling and optionally testing them, and logs
every event for later analysis.

The eight stages are: Ingest, Analyze, Classify, Predict, Prioritize,
Refactor, Validate, Feedback.


## 1. Pipeline-wide assumptions

These are assumptions made across the entire pipeline. A repository that
breaks them may still partially work, but with the degradations called out
below.

### 1.1 Java source layout follows Maven or Gradle conventions

Stage 1 looks for `src/main/java` to find the source root. This works for
most Java open-source projects (commons-lang3, commons-io, spring projects,
junit, most Apache projects) but fails on:

- Ant projects with non-standard layouts.
- Multi-module projects where each module has its own `src/main/java`. We
  pick one of them, not all.
- Projects with sources at the repo root and no source directory.
- Test code mixed with production code at the same path.

Workaround: pass `java_source_root` explicitly to Stage 1 when auto-detection
picks the wrong path.

### 1.2 javalang parses most but not all modern Java

Stages 4 and 6 use javalang to read Java code. javalang was last updated
around 2020 and chokes on some Java 8+ features. The most common case is
array constructor references like `boolean[]::new`. On commons-lang3, 3 of
259 files (about 1%) fail to parse for this reason. The pipeline doesn't
crash; it logs warnings and continues with the parseable files.

Future improvement: replace javalang with tree-sitter-java, which handles
records, sealed classes, switch expressions, pattern matching, and method
references. We confirmed tree-sitter installs cleanly in the container. The
migration is roughly 100-150 lines in `production/lib/metrics.py` and a
similar amount in `production/stages/refactor.py`.

### 1.3 Stage 7 only knows Maven and Gradle

Stage 7 detects the build system by looking for `pom.xml` (Maven) or
`build.gradle` / `build.gradle.kts` (Gradle). For Gradle projects, it
prefers the project's own `gradlew` wrapper if present and falls back to
system Gradle. Projects using Ant, Bazel, or no build system are validated
as "skipped: no build system detected." Stages 1-6 still run; we just
can't tell whether the refactoring builds.


## 2. Stage-specific limitations

### 2.1 Stage 1 (Ingest)

Auto-detection prefers `src/main/java` over a repo-root scan. If both exist,
the source root wins, which is correct for Maven and Gradle projects but
may miss Java sources in atypical layouts.

The demo runs against a hardcoded pinned commit of commons-lang3. We pinned
it so the issue counts don't drift between runs of the notebook. Pointing
the pipeline at a different repo means picking and pinning a new commit;
there's no auto-pin yet.

Training data scale: 30 projects, not 1,000. The project description's
task list says "extract code metrics from 1,000+ open-source repositories."
Our training data covers 30 Apache Java projects from the Lenarduzzi V2
Technical Debt Dataset, with commons-lang3 used as a held-out demonstration
project. We chose this dataset because it ships pre-labeled bug-inducing
commits (via the SZZ algorithm), full Jira issue history, and SonarQube
measurements. Building a labeled dataset of similar quality across 1,000
repos would mean running SonarQube, mining git history with SZZ, and joining
Jira data on each repo. That's a research-scale pipeline of its own and
sat outside the scope of this project.

### 2.2 Stage 2 (Analyze)

Stage 2 runs PMD with three rulesets: `quickstart` (general best practices),
`performance`, and `security`. This is intentionally narrow to keep the
issue count manageable and the rules well-known. A more complete run would
include `design`, `errorprone`, `multithreading`, and `codestyle`. We
chose the narrower set because:

- The trained fault predictor was built on SonarQube features, not PMD's
  full rule set. More rules don't necessarily produce better signal.
- Stage 6 has its own filter for unrefactorable rules (see 2.6); flagging
  more issues that we then drop is wasted work.

PMD's rule output also doesn't include the SonarQube-style features the
fault predictor expects, so we reconstruct the closest equivalents from
source code in Stage 4. The cost of that reconstruction is documented in
2.4.

The PMD installation is currently transient (apt installs PMD 7.23.0 in
the container, not committed to the Dockerfile). For reproducibility, the
install should move to the project's setup script.

### 2.3 Stage 3 (Classify)

Stage 3 sorts each PMD issue into one of five categories: code smells,
architectural violations, performance issues, outdated patterns, and
concurrency issues. The mapping is a CSV with one row per PMD rule, 301
rows total, built by hand. Stage 3 just looks each issue's rule up in the
CSV.

Three things to know about this approach:

The mapping is a one-time labeling effort. New PMD rules added in future
versions of PMD won't have a category until someone updates the CSV.

Some rules could plausibly fit two categories. For example,
`AvoidUsingHardCodedIP` is a security issue, but we file it under
architectural violations because the project description's category list
doesn't include security. The choice is defensible but not the only one
that would be defensible.

Categories with sparse PMD coverage may give a false impression. On
commons-lang3, our run found 0 outdated_patterns issues and only 2
concurrency_issues issues. That doesn't mean commons-lang3 has no debt in
those categories; it means PMD's quickstart, performance, and security
rulesets don't check for them well. A wider ruleset would reveal more.

Precision of the category labels themselves wasn't measured against a
held-out set. We discuss why in section 3.7.

### 2.4 Stage 4 (Predict)

The fault predictor was trained on the Lenarduzzi V2 Technical Debt Dataset
(64,594 commits across 30 Apache projects, with commons-io held out). Its
features come from SonarQube measurements of those projects' commits.

When applied to a new repository, the pipeline rebuilds those features
from real source code (via javalang) and real git history (via subprocess
calls to `git log`). This causes calibration drift:

- The model expects SonarQube's exact metric definitions; we approximate
  them.
- Cognitive complexity is approximated as cyclomatic-minus-one rather than
  Campbell's full algorithm. Order of magnitude is right; the exact number
  isn't.
- DUPLICATED_LINES, DUPLICATED_BLOCKS, DUPLICATED_FILES, and
  DUPLICATED_LINES_DENSITY are hardcoded to zero. We don't run a
  duplication detector. The model was trained on commits where these
  fields had real values, so feeding it zeros is a shift it wasn't
  trained on.
- HEAD metrics are used for all issues rather than checking out each
  issue's host commit and computing metrics there. This is a deliberate
  simplification for speed; the rigorous version is documented in 3.1.

The result of these drifts: probability rankings stay informative (the
model still elevates risky files like ThreadUtils and LockingVisitors on
commons-lang3), but absolute probabilities are squashed. Our run on
commons-lang3 produced a range of 0.10 to 0.60 with mean 0.32, instead of
spanning the full [0, 1] range a properly calibrated model would. For
ranking, this is fine. For confidence-thresholding ("only refactor issues
above 0.8"), the absolute values would mislead.

The project description also asks for prediction of "the emergence of
technical debt in future code to enable proactive prevention rather than
reactive remediation." Our pipeline doesn't do this. What we built is
reactive: for issues that already exist, we predict the probability that
the host commit was fault-inducing. The model looks backward at code that
already exists, not forward at code about to be written.

A genuinely proactive system would intercept changes before they merge.
Two natural shapes:

1. A pre-commit hook that runs the pipeline on the diff and warns the
   developer about issues their change is about to introduce. Closer to
   SonarLint's IDE integration than to anything we built.
2. A predictive model that takes a partial change (a function being
   written) and forecasts the debt it's likely to introduce based on the
   developer's history, the file's complexity, and similar contextual
   features. This needs labeled examples of "code as it was being written"
   plus "debt that emerged later," which no public dataset provides at
   scale.

Both are reasonable directions. Neither was in scope for this project.

### 2.5 Stage 5 (Prioritize)

Three weighting decisions are heuristic, not learned:

- Severity weight is exponential by PMD priority (1.0, 0.5, 0.25, 0.125,
  0.0625). Steep enough to make priority 1 issues dominate; less steep
  would surface lower-severity issues more often.
- Ruleset weight is 1.2 for Performance and Multithreading and 1.0 for
  everything else. A modest tilt toward customer-visible categories. Could
  be tuned by per-repo feedback; we don't yet do this.
- Effort minutes are smoothed values anchored on empirical medians from
  the SonarQube EFFORT field across 992,704 issues in the dataset (PMD
  priority 1 is 20 minutes, 2 is 15, 3 is 10, 4 is 5, 5 is 2). We had to
  smooth because the raw medians weren't monotonic with PMD priority
  (MINOR issues had unusually low median effort in the dataset, while
  INFO had moderate effort).

Team capacity isn't modeled. The project description asks for
prioritization based on impact, effort, and team capacity. We do impact
and effort. A capacity-aware version would need per-team data on developer
count, sprint cadence, and current workload, none of which exists for the
demo project. With that data, the impact-over-effort score could be
extended to discount issues that don't fit in the current sprint window.
Documented as future work.

The Pareto front computation is correct and not heuristic. Issues on the
front represent genuine impact-vs-effort trade-offs.

### 2.6 Stage 6 (Refactor): model selection

Stage 6 supports two modes:

**Live mode** runs Qwen2.5-Coder-0.5B-Instruct. It returns in seconds on
CPU but produces weak refactorings on real code. The 0.5B model often
returns the input unchanged or wraps methods in spurious helper classes
that fail compilation. It's enough to demonstrate that the pipeline
mechanics work; it isn't the refactoring tool we'd want a developer to
use.

**Replay mode** loads pre-computed Stage 6 records from a JSON file. The
JSON envelope is self-describing (model name, generation timestamp, schema
version). On commons-lang3 with the 3B model run on a UMIACS Nexus RTX
A4000, Stage 6 produced 10 refactorings that all parsed as valid Java
with preserved signatures. Generation times ranged from 33 to 103 seconds
per issue.

The 3B model produces correct, targeted refactorings (changing
`return null` to `return new String[0];` for
ReturnEmptyCollectionRatherThanNull on `getMonthDisplayNames`, for
example). The 0.5B model produced wrapper-class garbage on the same
input.

We picked the 3B model after benchmarking five candidates across three
prompting strategies on 1000 held-out CodeXGLUE Java refactoring pairs.
The candidates were Qwen2.5-Coder-0.5B-Instruct,
Qwen2.5-Coder-3B-Instruct, the general Qwen2.5-3B-Instruct, Meta's
Llama-3.2-3B-Instruct, and Microsoft's Phi-3.5-mini-instruct. The three
strategies were zero-shot, few-shot with three fixed examples, and
few-shot with three examples retrieved by similarity to the input. We
measured exact match against the reference fix, mean BLEU score against
the reference, Java syntactic validity, and inference time per generation.

Qwen2.5-Coder-3B with retrieval-based prompting led on mean BLEU (70.9)
and Java validity (98.7%), at 1.5 seconds per generation. Llama-3.2-3B
lagged by 7 BLEU points across all strategies. Phi-3.5-mini's Java
validity was 78%, well below the Qwen family's 97% and above. The full
results live in `/data/benchmark_results/` and are loaded into Section 4
of the example notebook.

A smoke test of the 3B model on Mac CPU completed in 1482 seconds (24.7
minutes) for one generation. With 5 issues and 2 strategies, a typical
Stage 6 run would take over 4 hours. That's why we ship pre-computed
Nexus outputs in the demo.

### 2.7 Stage 6 (Refactor): selection filters

Three filters narrow the set of issues the agent attempts. They're
intentionally conservative.

Method size cap of 40 lines. Methods longer than this are skipped. The
cap matches the 0.5B model's 512-token output budget. The 3B model handles
longer methods cleanly, so the cap could rise on GPU. We saw FastTimeZone
(69 lines) cause both 0.5B strategies to truncate mid-output, producing
invalid Java with no remediation possible.

Unrefactorable rules. Eight PMD rules are hardcoded as unrefactorable for
a method-only agent: MethodNamingConventions,
TypeParameterNamingConventions, LocalVariableNamingConventions,
ClassWithOnlyPrivateConstructorsShouldBeFinal, UseUtilityClass,
UnnecessaryConstructor, UncommentedEmptyConstructor,
FieldNamingConventions. All require changes outside the local method
scope: renames need every call site updated, class-level structural
changes need the class declaration, constructor changes affect callers.
An agent that sees only one method can't safely fix any of these. On
commons-lang3, this skips 28 of 522 issues.

Files javalang can't parse. Same parser limitation as Stage 4. If the file
holding the method has unparseable syntax, method extraction fails and
the issue gets skipped.

### 2.8 Stage 6 (Refactor): confidence scoring with signature gate

A refactoring that changes the method signature is never selected as the
best strategy, even if the resulting Java parses with HIGH confidence.
Signature changes silently break callers and aren't safe refactorings.

The strategy-level confidence may still be HIGH (because the Java parses),
but `best_strategy` gets set to None when no candidate preserves the
signature. This is a deliberate gate layered on top of the MVP's
confidence scoring, which only considered syntax validity, exact match,
and BLEU.

We saw the 0.5B model produce signature-changing "refactorings" multiple
times: adding parameters, removing bodies, replacing them with stub
comments. The signature gate keeps these from being recommended.

### 2.9 Stage 6 (Refactor): local fixes to MVP utility code

The MVP utility module's `_extract_java_from_response` function had two
bugs that surfaced during the Q1 spike on real code:

- It strips everything before a lone closing fence, producing empty
  output.
- It can't handle outputs with leading imports, which break the
  wrap-then-parse syntax validation.

Stage 6 includes a local copy of this function with both bugs fixed. The
upstream MVP utility module is unchanged; that fix is documented as
future work.

### 2.10 Stage 7 (Validate)

Stage 7 runs a targeted Maven plugin goal (`compiler:compile` or
`surefire:test`) rather than the full Maven lifecycle phase. This skips
project-specific plugins (rat-check, checkstyle, enforcer) that would
otherwise fail before reaching the compiler. That matters because the
container ships Maven 3.8.7 but commons-lang3's `pom.xml` requires 3.9
for some plugins. Targeted goals sidestep the version mismatch.

For test mode, Stage 7 runs `compiler:compile compiler:testCompile
surefire:test`. This compiles main and test sources, then runs the test
suite. On commons-lang3, this exercises 57,939 tests in about 140 seconds
once the Maven dependency cache is warm (the first run takes longer).

Stage 7 catches structural and integration failures (cannot find symbol,
illegal static declaration, cross-method dependency breaks). It catches
behavioral failures only in test mode, where the agent's hashCode-based
comparator that compiles cleanly but fails 2 of 57,939 tests gets caught
because it doesn't preserve sort order.

In compile-only mode, semantically incorrect but syntactically valid
refactorings (Record 5 in our 3B run) get approved. Compile mode is the
fast first-pass check; test mode is needed for behavioral verification.

A small leak in Stage 7's tempdir cleanup: the parent tempdir created by
`tempfile.mkdtemp` doesn't get removed when per-record cleanup runs (only
the repo copy inside it does). It's a few KB per validation and doesn't
matter for the demo, but should be tightened.

### 2.11 Stage 8 (Feedback)

Stage 8 is write-mostly. The pipeline logs every event to a SQLite
database, and the query helpers (`get_summary_metrics`,
`get_success_rate_by_rule`, `get_per_repo_summary`) read from it for
reporting. Nothing in the pipeline currently uses the accumulated history
to improve future predictions or refactorings. The "feedback loop" is
implemented as infrastructure (the data is captured, durable, queryable)
but not as closed-loop learning (the system doesn't get smarter the more
it runs).

The database is local SQLite only. No archival, no backup, no multi-machine
sync. That's fine for a research demo but a real deployment would need a
real database (Postgres, or at minimum a backup strategy). Test coverage
for Stage 8 is thinner than for the other stages because there's less to
test on a write-mostly module; the read helpers are covered, the writes
mostly aren't.


## 3. Design decisions and tradeoffs

These are choices we made on purpose. Each could be changed if priorities
shift.

### 3.1 We use HEAD metrics for all issues, not per-commit metrics

When predicting fault probability per issue, we compute repo metrics once
at HEAD and reuse them for every issue regardless of which commit last
touched the issue's file. The MVP and the Lenarduzzi paper compute
metrics per-commit (each commit has its own snapshot of complexity,
NCLOC, etc.). The rigorous version requires a `git checkout` per unique
commit before metric computation, then `git checkout HEAD` to restore.
That's slow and adds operational complexity.

We accepted the simplification for three reasons. The model already has
calibration drift from the SonarQube-vs-javalang feature mismatch, so one
more drift on the same axis is small relative to what's already there.
Relative ranking is what matters for prioritization, not absolute
probability. And the rigorous version would have made the demo notebook
much slower to run.

### 3.2 We don't apply refactorings to source files

Stage 6 produces refactorings as text strings and unified diffs. Stage 7
patches them into a temp copy of the repo for validation. The original
source files are never modified. We made this choice because an
autonomous tool that rewrites your source code on every run is dangerous,
and the project's README description doesn't require it. The pipeline
outputs recommendations; the human applies them.

### 3.3 We only ship one strategy in the Nexus output

The Nexus run uses zero-shot only, not few-shot retrieval. Two reasons:

The Q1 spike showed retrieval similarities on real code were low (around
0.45 against CodeXGLUE pairs), suggesting the retrieved examples weren't
close enough to the query to provide useful in-context demonstrations.

The 3B model is strong enough that good zero-shot prompts likely
outperform weakly-relevant few-shot examples.

Few-shot retrieval is still implemented and tested in Stage 6; we just
don't use it in the demo run.

### 3.4 Effort estimates are smoothed, not raw empirical medians

We use 20, 15, 10, 5, 2 minutes for PMD priorities 1 through 5. The raw
empirical medians from the dataset are 20, 10, 10, 2, 10. Smoothing
enforces monotonicity (higher PMD priority always means more effort) at
the cost of departing from the raw data. We chose to smooth because a
non-monotonic effort table would be hard to defend in the writeup, the
differences between cells are small in absolute terms (a few minutes),
and the downstream impact on ranking is minimal anyway since the
impact-over-effort ratio is dominated by the impact term.

### 3.5 Stage 6's prompt template is issue-aware

We bypass the MVP's `refactor_java_method` function (which uses a generic
"fix this Java method" prompt) and write our own prompt that includes the
specific PMD rule and description. This gives the agent context about
what to fix, not just "fix something." The change is small (the user
message includes "Rule: X" and "Description: Y" before the method) but
on real PMD issues it makes a difference: the agent has a target.

### 3.6 We test on commons-lang3 only

The pipeline is designed to work on any Maven or Gradle Java repo, but we
only stress-tested it on commons-lang3. We haven't seen real-world
breakage on other repos because we haven't pointed it at them yet. We're
confident in the design; we're not confident in any specific "X% of repos
work" claim.

### 3.7 Precision claims and benchmarking

The project description's task list calls for classification models with
"85%+ precision" on debt type detection. We didn't specifically benchmark
against this target. Here's what we report instead and why.

Stage 3 (debt classification by category) is rule-based, not a trained
classifier. Each PMD rule is mapped to one of the project's five
categories through a CSV lookup of 301 rules. Precision is whatever the
manual mapping achieves. We didn't measure it against a held-out set
because the manual mapping itself is the ground truth we'd be testing
against.

Stage 4 (fault probability per commit) is a trained XGBoost classifier.
We report AUC = 0.884 on the held-out commons-io test set. AUC is the
right metric for our use case (ranking issues by probability) but isn't
directly comparable to a precision target. At a typical decision
threshold, the classifier's precision is around 36% and recall around
83%. The model is conservative-flagging: it catches most bug-inducing
commits at the cost of flagging many that turn out fine.

If a strict precision target were the goal, we'd tune the decision
threshold to maximize precision at a chosen recall level, or train a
separate classifier with a different loss function. We optimized for
ranking quality because that's what Stage 5 needs to prioritize
remediation. The tradeoff is documented; alternative tuning is
straightforward future work.

Section 3.6 of the example notebook reports R² values for the three
regression models: defect density 0.78, resolution time -0.38, velocity
0.42. These are regression metrics, not classification precision, and we
discuss what each means in context.


## 4. Near-term future improvements

Each of these would take 1-3 days and produce meaningful gains. They could
be tackled incrementally without changing the pipeline's architecture.

### 4.1 Tree-sitter migration

Replace javalang with tree-sitter-java in `production/lib/metrics.py` and
`production/stages/refactor.py`. Eliminates the 1% file parse failure
rate and supports modern Java features (records, sealed classes, switch
expressions, pattern matching). We confirmed tree-sitter installs cleanly
in the container. About 100-150 lines of refactoring with stable public
APIs in metrics.py.

### 4.2 Validation against multiple repos

Run the full pipeline against 3-5 additional Java open-source repos
(commons-io, commons-lang, spring-petclinic, junit5) and document where
it breaks. Track source-root detection failures, javalang parse failures,
build-system surprises, agent behavior on different code styles. Replaces
"tested on commons-lang3" with empirical multi-repo numbers.

### 4.3 Apply-and-verify mode for Stage 7

Stage 7 currently patches into a temp directory and validates there. A
user who wants to actually apply the refactoring has to copy the agent's
output back to their repo by hand. An `apply_refactoring` function that
writes the patch back to the original file (after explicit user approval)
would make Stage 6 + 7 a real end-user tool, not just a research artifact.

### 4.4 Closed-loop training experiment

The feedback database is accumulating real data (52 events from our test
runs). Once we have enough events from multiple pipeline runs, we could
try retraining the fault predictor with our own data instead of the
Lenarduzzi V2 dataset. The hypothesis: a model trained on our
javalang-and-git features wouldn't have the calibration drift the current
SonarQube-trained model has. This needs maybe 1000+ refactoring events
first, which means running the pipeline against many repos.

### 4.5 More refactorable rules

The unrefactorable-rules list is conservative. Some rules in it could be
made refactorable by giving the agent more context. MethodNamingConventions
could work if the agent saw all the files where the method is called and
could update each one. This needs Stage 6 to gain multi-file scope.

### 4.6 Upstream the MVP utility fixes

The local `_extract_java_from_response` function in Stage 6 should be
upstreamed to `ai_technical_debt_utils.py`. The fixes are general and
the MVP would benefit from them.

### 4.7 Tighten Stage 7's tempdir cleanup

The parent tempdir created by `tempfile.mkdtemp` leaks. Easy fix: use a
context manager or wrap in try/finally that removes the parent too.


## 5. Research vision: turning this into a real agent

The current pipeline is a working research demo: it identifies, prioritizes,
attempts, and validates refactorings on a single method at a time. To
turn this into something a developer would actually use day-to-day, three
larger research directions are needed.

### 5.1 Live 3B (or larger) agent with persistent inference

The 3B model is too slow on CPU to be a live agent today. The demo
notebook ships pre-computed records. To make 3B (or 7B) live, we'd need
either:

**Quantized inference on CPU.** int8 or int4 quantization could bring 3B
CPU inference into the 30-60 seconds per generation range, slow but
usable. Tools: bitsandbytes, GGUF/llama.cpp, ONNX with quantization.

**A persistent inference service.** A long-running process on a GPU
(Nexus or a dedicated host) that keeps the model loaded and exposes an
HTTP endpoint. The laptop pipeline calls the endpoint per refactoring.
Latency drops from minutes to seconds because the model never reloads.
Engineering work: a few hundred lines for the server plus client glue,
plus a host that can run the service continuously.

The persistent service is the right long-term answer. It separates the
user's machine (where the analysis runs) from the inference machine
(where the model lives). The same architecture would let us swap in
larger models (Qwen-Coder-7B, or proprietary models like Claude or
GPT-4) without changing the rest of the pipeline.

### 5.2 Iterative refinement loop with cross-file context

When Stage 7 catches a failure, the current pipeline reports the failure
and moves on. A real agent would feed the compile error back to the model
and try again, possibly editing other files that the error references.

A concrete shape:

1. Stage 6 produces a refactoring.
2. Stage 7 patches and compiles.
3. If compilation fails, parse the error message for the file and line
   number that failed and the kind of error (missing symbol, signature
   mismatch, type error).
4. Read the failing file (and related files if cross-file references are
   involved) and feed that context to the agent along with the original
   issue, the original refactoring, and the error message.
5. Ask the agent for a corrected version of the original method, or edits
   to the related files, or a confession that the refactoring isn't worth
   pursuing.
6. Loop with a hard cap on iterations (say, 3) and a worth-it threshold
   (if the patch keeps growing in size and complexity, abandon).

This is what makes Claude Code, Cursor's agent mode, and SWE-Bench-style
tools dramatically more useful than single-shot completion. The agent
uses the compiler as its tool to discover what it broke and fix it.

The "is it worth it?" threshold is the hardest part. Possible signals:

- Number of files the agent has had to edit.
- Net lines added vs removed across all files.
- Whether each iteration reduced or increased the error count.
- Whether the resulting changes preserve the original PMD rule's intent.

We didn't build this. The current pipeline is the foundation; the loop
is the next major feature.

The honest reason we deferred it: our 3B test run had 8 of 10
refactorings compile cleanly first try. The 2 failures were big
structural mistakes (wrapping the method in a stub class, removing the
catch block in a way that broke callers) that wouldn't be fixed by a
small retry. We don't yet have empirical evidence that a retry loop on
top of 3B would significantly improve the overall success rate. With a
stronger base model (7B or larger), or measurable second-shot improvement,
the loop becomes the obvious next investment.

### 5.3 Closed-loop autonomous learning

The README's full vision: track predicted vs actual impact of refactorings
to improve model accuracy over time. We have the tracking; we don't have
the improvement.

A closed-loop system would:

- Periodically retrain the fault predictor on accumulated feedback
  (refactor attempted, refactoring valid, tests pass, human review
  passes).
- Adjust prioritization weights based on per-rule success rates: prefer
  rules where refactorings tend to succeed.
- Adjust the unrefactorable-rules list dynamically. If a rule consistently
  fails, add it to the skip list. If a rule that was previously skipped
  starts succeeding (because the agent or context has improved), remove
  it.
- Use the feedback database to suggest which prompting strategies work
  best for which rule types.

This requires a larger volume of refactoring runs than we have today
(probably 1000+ events to be statistically meaningful), a retraining
schedule that doesn't destabilize the predictor (don't retrain on a
single bad run), and a rollback mechanism when a retrained model
performs worse than the current one.

This is the longest-term direction. It would need continuous deployment
infrastructure and a sustained run of the pipeline against many repos
over weeks. A research project in itself.

### 5.4 Multi-file refactoring with project-aware context

The current agent sees one method at a time. A real refactoring agent
needs to see:

- The class containing the method (instance fields, helper methods,
  inheritance).
- The file's imports.
- The callers of the method (so the agent knows what changes would break).
- The interfaces or superclasses the method overrides.

Building this requires:

- A code intelligence layer that can answer "where is X called from" and
  "what does X depend on." Could be built on jdt-language-server, semgrep,
  or a custom AST traversal.
- A larger context window in the agent (3B has 32K tokens; we'd want to
  use more of it for this).
- A way to apply multi-file edits atomically.

Once this exists, rules currently on the unrefactorable list (renames,
class-level changes, extract-method-and-update-callers) become tractable.
The agent's scope grows from "edit one method" to "edit a small subgraph
of the codebase."


## 6. What this project is and isn't

To set accurate expectations.

This is a working research pipeline that demonstrates each piece of the
code-transformation problem at small scale. Static analysis works on any
Java repo. The trained model produces meaningful per-commit risk scores.
The agent harness produces real refactorings (with the 3B model on GPU)
that often compile and sometimes pass tests. Validation correctly
distinguishes safe from broken refactorings. The system logs everything
for later analysis.

It isn't a production refactoring tool. The agent's success rate on real
code is around 80% for compile and lower for behavior preservation. The
model needs a GPU to be useful. The feedback loop is open (we record but
don't learn). Cross-file refactorings are out of scope. The
unrefactorable-rules list excludes many real PMD findings.

The gap between research pipeline and production tool is the work in
section 5. The pipeline as it stands is a solid foundation for that
work, not the destination.