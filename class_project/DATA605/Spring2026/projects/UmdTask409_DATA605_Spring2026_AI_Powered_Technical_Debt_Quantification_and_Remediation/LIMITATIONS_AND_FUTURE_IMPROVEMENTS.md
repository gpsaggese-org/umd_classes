# Limitations and Future Improvements

This document captures the known limitations of the AI-Powered Technical Debt
Quantification and Remediation pipeline, the design decisions that produced
those limitations, and the future improvements that would address them.

The pipeline ingests a Java repository, identifies technical debt issues with
static analysis, predicts fault-inducing risk with a trained model, prioritizes
issues by impact-over-effort, runs a code transformation agent on the top
candidates, validates the resulting refactorings by compiling and optionally
testing them, and logs every event for later analysis.

The eight stages are: Ingest, Analyze, Classify, Predict, Prioritize, Refactor,
Validate, Feedback.


## 1. Pipeline-Wide Assumptions

These are assumptions made across the entire pipeline. A repository that
violates them may still partially work, but with documented degradations.

### 1.1 Java source layout follows Maven or Gradle conventions

Stage 1 auto-detects the Java source root by looking for `src/main/java`. This
works for the majority of Java open-source projects (commons-lang3, commons-io,
spring projects, junit, and most Apache projects) but fails on:

- Ant projects with non-standard layouts
- Multi-module projects where each module has its own `src/main/java`
  (we'd find one of them, not all)
- Projects that put sources at the repo root with no source directory
- Test code intermixed with production code at the same path

Workaround for now: pass `java_source_root` explicitly to Stage 1 when
auto-detection picks the wrong path.

### 1.2 javalang parses most but not all modern Java syntax

Stage 4 (metric computation) and Stage 6 (method extraction) both use the
javalang library. javalang was last updated around 2020 and does not handle
some Java 8+ syntax features. The most common failure pattern is array
constructor references like `boolean[]::new`. On commons-lang3, 3 out of 259
files (about 1%) fail to parse for this reason. The pipeline does not crash;
it logs warnings and continues with the parseable files.

Future improvement: migrate javalang to tree-sitter-java, which handles modern
Java including records, sealed classes, switch expressions, pattern matching,
and method references. Verified that tree-sitter installs cleanly in the
container; the migration is approximately 100-150 lines in
`production/lib/metrics.py` and similar work in `production/stages/refactor.py`.
Deferred until after end-to-end pipeline was working; now that the pipeline
ships, this is the cleanest single-file improvement available.

### 1.3 Build system support for Stage 7 is Maven and Gradle only

Stage 7 detects the build system by checking for `pom.xml` (Maven) or
`build.gradle` / `build.gradle.kts` (Gradle). For Gradle projects, it prefers
the project's own `gradlew` wrapper if present, falling back to system Gradle.
Projects using Ant, Bazel, or no build system at all are validated as
"skipped: no build system detected." Stages 1-6 still work in this case;
the pipeline just cannot tell whether the refactoring integrates.


## 2. Stage-Specific Limitations

### 2.1 Stage 1 (Ingest)

Auto-detection prefers `src/main/java` over a repo-root scan. If both exist,
the source root is picked, which is correct for Maven/Gradle projects but may
miss Java sources stored elsewhere in atypical layouts.

### 2.2 Stage 2 (Analyze)

Stage 2 runs PMD with three rulesets: `quickstart` (general best practices),
`performance`, and `security`. This is intentionally narrow to keep the issue
count manageable and the rules well-known. A more complete run would include
`design`, `errorprone`, `multithreading`, and `codestyle`. We chose the narrower
set because:

- The trained fault predictor was built on SonarQube features, not PMD's
  full rule set. More rules would not necessarily produce better signal.
- Stage 6 has its own filter for unrefactorable rules (see 2.6); flagging
  more issues that we then filter out is wasted work.

The PMD installation is currently transient (apt installs PMD 7.23.0 in the
container, not committed to the Dockerfile). For reproducibility, the install
should be added to the project's setup script.

### 2.3 Stage 4 (Predict)

The fault predictor was trained on the Lenarduzzi V2 Technical Debt Dataset
(64,594 commits across 30 Apache projects, with commons-io held out). Its
features come from SonarQube measurements of those projects' commits.

When applied to an arbitrary new repository, the pipeline reconstructs those
features from real source code (via javalang) and real git history (via
subprocess calls to `git log`). This introduces calibration drift:

- The model expects SonarQube's exact metric definitions; we approximate them.
- Cognitive complexity is approximated as cyclomatic-minus-one rather than
  Campbell's full algorithm. Order-of-magnitude correct, but not identical.
- DUPLICATED_LINES, DUPLICATED_BLOCKS, DUPLICATED_FILES, and
  DUPLICATED_LINES_DENSITY are hardcoded to zero. We do not run a duplication
  detector. The model was trained on commits where these fields had real
  values; feeding it zeros is a shift it was not trained on.
- HEAD metrics are used for all issues rather than checking out each issue's
  host commit and computing metrics there. This is a deliberate simplification
  to keep the pipeline fast; it would be more rigorous to checkout-and-restore
  but the cost in runtime would be high.

The result of these drifts: probability rankings remain informative (the model
correctly elevates risky files like ThreadUtils and LockingVisitors on
commons-lang3), but absolute probabilities are squashed. We saw a range of
0.10 to 0.60 with mean 0.32 on commons-lang3, instead of using the full
[0, 1] range a properly calibrated model would. For ranking purposes this is
fine; for confidence-thresholding (e.g., "only refactor issues above 0.8")
the absolute values would mislead.

The project description also asks for prediction of "the emergence of technical
debt in future code to enable proactive prevention rather than reactive
remediation." Our pipeline does not do this.
 
What we have is a reactive fault predictor (Stage 4): for issues that already
exist in the code, we predict the probability that the host commit was
fault-inducing. The model looks backward at what has already been written. It
does not look forward at what is about to be written.
 
A genuinely proactive system would intercept code changes before they are
merged. Two natural shapes:
 
1. A pre-commit hook that runs the pipeline on the diff and warns the
   developer about issues their change is about to introduce. This is closer
   to a tool like SonarLint's IDE integration than to anything we built.
2. A predictive model that takes a partial change (a function being written,
   for example) and forecasts the debt it is likely to introduce based on
   the developer's history, the file's complexity, and similar contextual
   features. This would need labeled examples of "code as it was being
   written" plus "debt that emerged later," which no public dataset
   provides at scale.
Both are reasonable directions. Neither was in scope for this project.

### 2.4 Stage 5 (Prioritize)

Three weighting decisions are heuristic, not learned:

- Severity weight is exponential by PMD priority (1.0, 0.5, 0.25, 0.125,
  0.0625). Steep enough to make priority 1 issues dominate; less steep would
  surface lower-severity issues more often.
- Ruleset weight is 1.2 for Performance and Multithreading, 1.0 for everything
  else. A modest tilt toward customer-visible categories. Could be tuned by
  per-repo feedback; we do not yet do this.
- Effort minutes are smoothed values anchored on empirical medians from the
  SonarQube EFFORT field across 992,704 issues in the dataset (PMD priority
  1 -> 20 min, 2 -> 15, 3 -> 10, 4 -> 5, 5 -> 2). Smoothing was needed because
  the raw medians were not monotonic with respect to PMD priority (MINOR
  issues had unusually low median effort in the dataset, while INFO had
  moderate effort).

The Pareto front computation is correct and not heuristic. Issues on the
front represent genuine impact-vs-effort trade-offs.

### 2.5 Stage 6 (Refactor) - model selection

Stage 6 supports two modes:

- **Live mode** with Qwen2.5-Coder-0.5B-Instruct. Runs in seconds on CPU.
  Produces weak refactorings on real code: tends to return the input unchanged
  or wrap methods in spurious helper classes that fail compilation. Suitable
  as a demonstration that the pipeline mechanics work; not as the actual
  refactoring tool.
- **Replay mode** that loads pre-computed Stage 6 records from a JSON file.
  The JSON envelope is self-describing (model name, generation timestamp,
  schema version). On commons-lang3 with the 3B model run on a UMIACS Nexus
  RTX A4000, Stage 6 produced 10 refactorings that all parsed as valid Java
  with preserved signatures. Generation times ranged 33-103 seconds per issue.

The 3B model produces correct, targeted refactorings (for example, changing
`return null` to `return new String[0];` for ReturnEmptyCollectionRatherThanNull
on `getMonthDisplayNames`). The 0.5B model produced wrapper-class garbage on
the same input. The benchmark winner from Section 6 of the example notebook is
the 3B model; on a laptop CPU it took 25 minutes per generation, making it
impractical without GPU access.

A smoke test of the 3B model on CPU completed in 1482 seconds (24.7 minutes)
for one generation. With 5 issues and 2 strategies, a typical Stage 6
invocation would take over 4 hours. This drove the decision to ship
pre-computed Nexus outputs in the demo.

### 2.6 Stage 6 (Refactor) - selection filters

Three filters narrow the set of issues the agent attempts. They are
intentionally conservative.

- **Method size cap of 40 lines.** Methods longer than this are skipped.
  The cap matches the 0.5B model's 512-token output budget. The 3B model
  handles longer methods cleanly; the cap could be raised when running on
  GPU. We saw FastTimeZone (69 lines) cause both 0.5B strategies to truncate
  mid-output, producing invalid Java with no remediation possible.

- **Unrefactorable rules.** Eight PMD rules are hardcoded as unrefactorable
  by a method-only agent: MethodNamingConventions, TypeParameterNamingConventions,
  LocalVariableNamingConventions, ClassWithOnlyPrivateConstructorsShouldBeFinal,
  UseUtilityClass, UnnecessaryConstructor, UncommentedEmptyConstructor,
  FieldNamingConventions. These all require changes outside the local method
  scope: renames need to update every call site, class-level structural changes
  need the class declaration, constructor changes affect callers. An agent
  that sees only one method cannot safely fix any of these. On commons-lang3
  this skips 28 of 522 issues.

- **Files javalang cannot parse.** Same parser limitation as Stage 4. If
  the file containing the method has unparseable syntax, method extraction
  fails and the issue is skipped.

### 2.7 Stage 6 (Refactor) - confidence scoring with signature gate

A refactoring that changes the method signature is never selected as the best
strategy, even if it produces syntactically valid Java with HIGH confidence.
Signature changes silently break callers and are not safe refactorings.

The strategy-level confidence may still be HIGH (because the Java parses), but
`best_strategy` is set to None if no candidate preserves the signature. This
is a deliberate gating rule layered on top of the MVP's confidence scoring,
which only considered syntax validity, exact match, and BLEU.

We saw the 0.5B model produce signature-changing "refactorings" multiple
times (adding parameters, removing bodies, replacing with stub comments).
The signature gate prevents these from being recommended to the user.

### 2.8 Stage 6 (Refactor) - local fixes to MVP utility code

The MVP utility module's `_extract_java_from_response` function had two bugs
surfaced during the Q1 spike on real code:

- It strips everything before a lone closing fence (producing empty output)
- It cannot handle outputs with leading imports (which break the
  wrap-then-parse syntax validation)

Stage 6 includes a local copy of this function with both bugs fixed. The
upstream MVP utility module is unchanged; that fix is documented as a
future improvement.

### 2.9 Stage 7 (Validate)

Stage 7 runs a targeted Maven plugin goal (`compiler:compile` or
`surefire:test`) rather than the full Maven lifecycle phase. This skips
project-specific plugins (rat-check, checkstyle, enforcer) that would otherwise
fail before reaching the compiler. Particularly important because the
container has Maven 3.8.7 but commons-lang3's `pom.xml` requires
3.9 for some plugins. Targeted goals sidestep the version mismatch.

For test mode, Stage 7 runs `compiler:compile compiler:testCompile
surefire:test`. This compiles main and test sources, then runs the test
suite. On commons-lang3, this exercises 57,939 tests in about 140 seconds
(after Maven dependency cache is warm; first run takes longer).

Stage 7 catches structural and integration failures (cannot find symbol,
illegal static declaration, cross-method dependency breaks). It catches
behavioral failures only when run in test mode (e.g., the agent's
hashCode-based comparator that compiles cleanly but fails 2 of 57,939 tests
because it doesn't preserve sort order).

When run in compile-only mode, semantically incorrect but syntactically
valid refactorings (Record 5 in our 3B run) will be approved. We document
this as an explicit limitation: compile-mode is a fast first-pass check;
test-mode is needed for behavioral verification.

A small leak in Stage 7's tempdir cleanup: the parent tempdir created by
`tempfile.mkdtemp` is not removed when the per-record cleanup runs (only
the repo copy inside it is). This is a few KB per validation and irrelevant
for the demo, but should be tightened.

### 2.10 Stage 8 (Feedback)

Stage 8 is write-mostly. The pipeline logs every event to a SQLite database,
and the query helpers (`get_summary_metrics`, `get_success_rate_by_rule`,
`get_per_repo_summary`) read from it for reporting. But nothing in the
pipeline currently uses the accumulated history to improve future predictions
or refactorings. The "feedback loop" is implemented as infrastructure (the
data is captured, durable, and queryable) but not as closed-loop learning
(the system does not get smarter the more it runs).


## 3. Design Decisions and Tradeoffs

These are choices we made deliberately. Each could be changed if the project's
priorities shift.

### 3.1 We use HEAD metrics for all issues, not per-commit metrics

When predicting fault probability per issue, we compute repo metrics once at
HEAD and reuse them for every issue regardless of which commit last touched
the issue's file. The MVP and the Lenarduzzi paper compute metrics
per-commit (each commit has its own snapshot of complexity, NCLOC, etc.).
Doing the rigorous version requires a `git checkout` per unique commit
before metric computation, then `git checkout HEAD` to restore. This is
slow and adds operational complexity.

We accepted the simplification because: the model already has calibration
drift from the SonarQube-vs-javalang feature mismatch, one more drift on
the same axis is small relative to the existing one, and the relative
ranking is what matters for prioritization (not absolute probability).

### 3.2 We don't actually apply refactorings to source files

Stage 6 produces refactorings as text strings and unified diffs. Stage 7
patches them into a temp copy of the repo for validation. The original
source files are never modified. This is intentional: an autonomous tool
that rewrites your source code on every run is dangerous, and the README
description of the project does not require it. The pipeline outputs
recommendations; the human applies them.

### 3.3 We only ship one strategy in the Nexus output

The Nexus run uses zero-shot only, not few-shot retrieval. Two reasons:

- The Q1 spike showed retrieval similarities on real code were low (around
  0.45 against CodeXGLUE pairs), suggesting the retrieved examples were not
  close enough to the query to provide useful in-context demonstrations.
- The 3B model is strong enough that good zero-shot prompts likely outperform
  weakly-relevant few-shot examples.

Few-shot retrieval is still implemented and tested in Stage 6; we just don't
use it in the demo run.

### 3.4 Effort estimates are smoothed, not raw empirical medians

We use 20, 15, 10, 5, 2 minutes for PMD priorities 1 through 5. The raw
empirical medians from the dataset are 20, 10, 10, 2, 10. The smoothing
enforces monotonicity (higher PMD priority always means more effort) at
the cost of departing from the raw data. We chose to smooth because:

- A non-monotonic effort table would be hard to defend in the writeup
- The differences between cells are small in absolute terms (a few minutes)
- The downstream impact on ranking is minimal because the impact-over-effort
  ratio is dominated by the impact term, not effort

### 3.5 Stage 6's prompt template is issue-aware

We bypass the MVP's `refactor_java_method` function (which uses a generic
"fix this Java method" prompt) and write our own prompt that includes the
specific PMD rule and description. This gives the agent context about what
to fix, not just "fix something." The change is small (the user message
includes "Rule: X" and "Description: Y" before the method) but on real PMD
issues it makes a difference: the agent has a target.

### 3.6 We test on commons-lang3 only

The pipeline is designed to work on any Maven or Gradle Java repo, but we
have only stress-tested it on commons-lang3. Real-world breakage on other
repos has not been seen yet. We are confident in the design; we are not
confident in any specific number of "X% of repos work" claims.


## 4. Near-Term Future Improvements

These are improvements that would each take 1-3 days and produce meaningful
gains. They could be tackled incrementally without changing the pipeline's
architecture.

### 4.1 Tree-sitter migration

Replace javalang with tree-sitter-java in `production/lib/metrics.py` and
`production/stages/refactor.py`. Eliminates the 1% file parse failure rate
and supports modern Java features (records, sealed classes, switch
expressions, pattern matching). Already verified that tree-sitter installs
cleanly in the container. About 100-150 lines of refactoring with stable
public APIs in metrics.py.

### 4.2 Validation against multiple repos

Run the full pipeline against 3-5 additional Java open-source repos
(commons-io, commons-lang, spring-petclinic, junit5) and document where it
breaks. Specifically tracking: source-root detection failures, javalang
parse failures, build-system surprises, agent behavior on different code
styles. This would let us replace "tested on commons-lang3" with empirical
multi-repo numbers.

### 4.3 Apply-and-verify mode for Stage 7

Currently Stage 7 patches into a temp directory and validates there. A user
who wants to actually apply the refactoring has to copy the agent's output
back to their repo by hand. Adding an `apply_refactoring` function that
writes the patch back to the original file (after explicit user approval)
would make Stage 6 + 7 a real end-user tool, not just a research artifact.

### 4.4 Closed-loop training experiment

The feedback database is accumulating real data (currently 22 events from
our test runs). Once we have enough events from multiple pipeline runs,
we could try retraining the fault predictor with our own data instead of
the Lenarduzzi V2 dataset. The hypothesis: a model trained on our
javalang-and-git features would not have the calibration drift the current
SonarQube-trained model has. This requires accumulating maybe 1000+
refactoring events first, which means running the pipeline against many
repos.

### 4.5 More refactorable rules

The unrefactorable-rules list is conservative. Some rules currently in
the skip list could be made refactorable by giving the agent more context.
For example, MethodNamingConventions could work if the agent saw all the
files where the method is called and could update each one. This requires
extending Stage 6 to multi-file scope.

### 4.6 Upstream the MVP utility fixes

The local `_extract_java_from_response` function in Stage 6 should be
upstreamed to `ai_technical_debt_utils.py`. The fixes are general and the
MVP would benefit from them.

### 4.7 Tighten Stage 7's tempdir cleanup

The parent tempdir created by `tempfile.mkdtemp` leaks. Easy fix: use a
context manager or wrap in try/finally that removes the parent too.


## 5. Research Vision: Turning This Into a Real Agent

The current pipeline is a working research demo: it identifies, prioritizes,
attempts, and validates refactorings on a single method at a time. To turn
this into something a developer would actually use day-to-day, three larger
research directions are needed.

### 5.1 Live 3B (or larger) agent with persistent inference

Today the 3B model is too slow on CPU to be a live agent. The demo notebook
ships pre-computed records. To make 3B (or 7B) live, we need either:

- **Quantized inference on CPU.** int8 or int4 quantization could bring 3B
  CPU inference into the 30-60 seconds per generation range, which is slow
  but usable. Tools: bitsandbytes, GGUF/llama.cpp, ONNX with quantization.
- **A persistent inference service.** A long-running process on a GPU
  (Nexus or a dedicated host) that keeps the model loaded and exposes an
  HTTP endpoint. The laptop pipeline calls the endpoint per refactoring.
  Latency goes from minutes to seconds because the model never reloads.
  Engineering work: a few hundred lines for the server plus client glue,
  plus a host that can run the service continuously.

The persistent service approach is the right long-term answer. It separates
the user's machine (where the analysis runs) from the inference machine
(where the model lives). The same architecture would let us swap in larger
models (Qwen-Coder-7B, or proprietary models like Claude or GPT-4) without
changing the rest of the pipeline.

### 5.2 Iterative refinement loop with cross-file context

When Stage 7 catches a failure, the current pipeline reports the failure
and moves on. A real agent would feed the compile error back to the model
and try again, possibly editing other files that the error references.

A concrete shape for this loop:

1. Stage 6 produces a refactoring.
2. Stage 7 patches and compiles.
3. If compilation fails, parse the error message to extract:
   - The file and line number that failed
   - The kind of error (missing symbol, signature mismatch, type error)
4. Read the failing file (and related files if cross-file references are
   involved) and feed that context to the agent along with the original
   issue, the original refactoring, and the error message.
5. Ask the agent for either: a corrected version of the original method,
   or edits to the related files, or a confession that this refactoring
   isn't worth pursuing.
6. Loop with a hard cap on iterations (say, 3) and a worth-it threshold
   (e.g., if the patch keeps growing in size and complexity, abandon).

This is what makes Claude Code, Cursor's agent mode, and SWE-Bench-style
tools dramatically more useful than single-shot completion. The agent uses
the compiler as its tool to discover what it broke and fix it.

The "is it worth it?" threshold is the hardest part of this design. Possible
signals:

- Number of files the agent has had to edit
- Net lines added vs removed across all files
- Whether each iteration reduced or increased the error count
- Whether the resulting changes preserve the original PMD rule's intent

We have not yet built this. The current pipeline is the foundation; the
loop is the next major feature.

The honest reason we deferred: our 3B test run had 8 of 10 refactorings
compile cleanly first try. The 2 failures were big structural mistakes
(wrapping the method in a stub class, removing the catch block in a way
that broke callers) that wouldn't be fixed by a small retry. We don't yet
have empirical evidence that an iteration loop on top of 3B would
significantly improve the overall success rate. With a stronger base model
(7B or larger), or measurable second-shot improvement, the loop becomes
the obvious next investment.

### 5.3 Closed-loop autonomous learning

The README's full vision: "track predicted vs. actual impact of refactorings
to improve model accuracy over time." We have the tracking; we don't have
the improvement.

A closed-loop system would:

- Periodically retrain the fault predictor on accumulated feedback (refactor
  attempted, was the refactoring valid, did it pass tests, did it survive
  human review).
- Adjust prioritization weights based on per-rule success rates (prefer
  rules where refactorings tend to succeed).
- Adjust the unrefactorable-rules list dynamically: if a rule consistently
  fails to refactor, add it to the skip list; if a rule that was previously
  skipped starts succeeding (because the agent or context has improved),
  remove it.
- Use the feedback database to suggest which prompting strategies work
  best for which rule types.

This requires:

- A larger volume of refactoring runs than we have today (probably 1000+
  events to be statistically meaningful).
- A retraining schedule that doesn't destabilize the predictor (don't retrain
  on a single bad run).
- A rollback mechanism when a retrained model performs worse than the
  current one.

This is the longest-term direction. It would require continuous deployment
infrastructure and a sustained run of the pipeline against many repos over
weeks. A research project in itself.

### 5.4 Multi-file refactoring with project-aware context

The current agent sees one method at a time. A real refactoring agent needs
to see:

- The class containing the method (to understand instance fields, helper
  methods, inheritance)
- The file's imports (to understand what's available)
- The callers of the method (to understand what changes would break)
- The interfaces or superclasses the method overrides

Building this requires:

- A code intelligence layer that can answer "where is X called from" and
  "what does X depend on." Could be built on top of jdt-language-server,
  semgrep, or a custom traversal of the AST.
- A larger context window in the agent (3B has 32K tokens; we'd want to use
  more of it for this).
- A way to apply multi-file edits atomically.

Once this exists, rules currently on the unrefactorable list (renames,
class-level changes, extract-method-and-update-callers) become tractable.
The agent's scope of action grows from "edit one method" to "edit one
small subgraph of the codebase."


## 6. What This Project Is and Isn't

To set accurate expectations:

**What it is:** A working research pipeline that demonstrates each piece of
the code-transformation problem at a small scale. Static analysis works on
any Java repo. The trained model produces meaningful per-commit risk scores.
The agent harness produces real refactorings (with the 3B model on GPU)
that often compile and sometimes pass tests. Validation correctly
distinguishes safe from broken refactorings. The system logs everything for
later analysis.

**What it isn't:** A production refactoring tool. The agent's success rate
on real code is around 80% for compile and lower for behavior preservation.
The model needs a GPU to be useful. The feedback loop is open (we record but
don't learn). Cross-file refactorings are out of scope. The unrefactorable
rule list excludes many real PMD findings.

The gap between "research pipeline" and "production tool" is the work
described in section 5 of this document. The pipeline as it stands is a
solid foundation for that work; it is not the destination.