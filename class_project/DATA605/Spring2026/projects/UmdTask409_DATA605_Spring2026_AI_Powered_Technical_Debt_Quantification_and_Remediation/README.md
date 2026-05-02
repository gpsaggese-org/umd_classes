# AI-Powered Technical Debt Quantification and Remediation

A working pipeline that takes a Java repository and produces ranked technical debt issues plus AI-generated refactorings, validated by actually compiling the changes back into the codebase. Built for DATA605 at UMD, Spring 2026.

This README is the entry point. It tells you what's here, why it's organized the way it is, and exactly how to run it. There's also a troubleshooting section at the bottom for when things go wrong, because they will.

## What this project does

Most teams know they have technical debt. Almost none of them know which debt to fix first, or whether their fix actually works. The conventional answer is "use SonarQube and pay attention to the warnings," but that requires either a paid SonarQube license or expensive engineering time to triage findings manually.

We built an automated pipeline that does the whole loop with open-source tools:

1. Find issues in the source code (PMD).
2. Predict which issues live in commits likely to introduce faults (a trained XGBoost model on the Lenarduzzi V2 Technical Debt Dataset).
3. Rank the issues by impact-over-effort and pick a top-N set.
4. Send each top issue to a local code-generation model (Qwen2.5-Coder).
5. Compile the suggested refactoring back into the real codebase. Optionally run the test suite.
6. Log everything to a database for later analysis.

Eight stages total. Every stage feeds into the next. We test on Apache commons-lang3, a real, large, well-maintained Java library. The model finds 522 issues, ranks them, attempts the top 10, and 8 of those 10 compile cleanly. One of the two we tested with `mvn test` passes all 57,939 commons-lang3 tests; the other compiles fine but breaks two specific tests because the model produced a semantically wrong refactoring. We use this contrast to show why we have *two* validation layers instead of one.

The research question we set out to answer:

> Can a fully open-source pipeline that combines ML-based fault prediction with local LLM code generation achieve effective technical debt remediation without commercial tools or API access?

The honest answer: yes for the demo, with caveats listed in `LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md`. We are not claiming this replaces SonarQube. We are claiming it is a working proof that the open-source ecosystem has caught up enough to do this whole loop end-to-end without paying anyone.

## What's in this folder

```
.
├── README.md                              <- you are here
├── LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md <- honest list of what we did not do
│
├── ai_technical_debt.API.ipynb            <- tour of every tool used
├── ai_technical_debt.example.ipynb        <- end-to-end pipeline on commons-lang3
├── ai_technical_debt_utils.py             <- MVP utilities (database, training, etc.)
│
├── production/                            <- the actual pipeline
│   ├── stages/                            <-   one file per stage (8 stages)
│   ├── lib/                               <-   shared helpers (metrics, etc.)
│   ├── scripts/                           <-   runnable scripts (training, runner)
│   ├── tests/                             <-   159 unit tests
│   ├── data/                              <-   trained model, 3B records, mappings
│   └── spikes/                            <-   exploratory work (not in CI)
│
├── Dockerfile                             <- builds the container
├── requirements.txt                       <- Python dependencies
├── docker_build.sh                        <- builds the image
├── docker_jupyter.sh                      <- starts Jupyter
├── docker_bash.sh                         <- starts an interactive shell
└── docker_clean.sh                        <- removes the container/image
```

### Why two places for code: utils.py and production/

This is the question that comes up first. Let me explain.

The MVP (the original starter code we inherited) put everything in `ai_technical_debt_utils.py`. That file has 38 functions: database access, feature engineering, ML model training, code-quality validation, BLEU scoring, retrieval indexing, refactoring helpers. It works. It does what the rubric expects.

But our project extended the MVP with a full 8-stage production pipeline, and putting all of that into one file would have made it 3000+ lines of unrelated functionality. So we organized the new pipeline code into a `production/` package with one file per stage, plus shared lib code, plus tests, plus runnable scripts.

We discussed this with Prof. Saggese before deciding. He approved keeping the package as long as nothing breaks.

Here is how the two pieces relate:

- `ai_technical_debt_utils.py` is the MVP's home. The functions there are *imported by* our production code (`production/stages/refactor.py` calls `validate_java_syntax`, `compute_bleu_against_reference`, `compute_confidence_score` from the utils file) and *demonstrated by* the API notebook.
- `production/` is the production pipeline. Eight stage files, one per stage of the pipeline. The example notebook walks through them on a real codebase.

You can think of `ai_technical_debt_utils.py` as the "library of low-level helpers we built during the MVP phase" and `production/` as "the pipeline we built on top." Both are required; neither is redundant.

If this organization is a problem for grading, the rubric requirement is "all code in `*_utils.py`," which is technically only met by the utils file. We argue (and Prof. Saggese accepted) that an 8-stage pipeline genuinely cannot live in one file without becoming unreadable, and the structure under `production/` is what an open-source maintainer would actually do.

## Step-by-step: how to run this

The whole thing runs in a Docker container. You don't install Python packages, Java, Maven, or PMD on your own machine. Just Docker.

Before you start, you need:

- Docker installed and running. macOS, Linux, or Windows with WSL2 should all work. We tested on macOS (Apple Silicon).
- About 4 GB of disk space for the container image.
- An internet connection for the first build (we download a few hundred MB of base packages).

### Step 1: clone the repo

```bash
git clone --recursive https://github.com/gpsaggese/umd_classes.git
cd umd_classes
git checkout UmdTask409_DATA605_Spring2026_AI_Powered_Technical_Debt_Quantification_and_Remediation
cd class_project/DATA605/Spring2026/projects/UmdTask409_DATA605_Spring2026_AI_Powered_Technical_Debt_Quantification_and_Remediation
```

The `--recursive` flag pulls submodules. The branch name is long because the rubric requires it.

If you already have the repo cloned without `--recursive`, run `git submodule update --init` from inside the repo to fetch submodules.

### Step 2: make the Docker scripts executable

```bash
chmod +x docker_*.sh
```

This is a one-time fix. Git sometimes drops the executable bit on shell scripts when they're cloned on different operating systems.

### Step 3: build the Docker image

```bash
./docker_build.sh
```

This takes 10-20 minutes the first time. Most of the wait is downloading and installing Java 17, Maven, PMD, and the Python packages we use (`pandas`, `transformers`, `torch`, `xgboost`, etc.).

If the build script fails with a flag error (`--progress` or similar), use this instead:

```bash
docker build -t gpsaggese/umd_ai_technical_debt .
```

Same result, just bypasses a wrapper that may have version mismatches with your Docker.

You'll know the build succeeded when you see something like:

```
Successfully built abc123def456
Successfully tagged gpsaggese/umd_ai_technical_debt:latest
```

### Step 4: launch Jupyter

```bash
./docker_jupyter.sh
```

This starts the container with Jupyter Lab inside it and tells you a URL. Look for a line like:

```
http://127.0.0.1:8888/lab?token=abc...
```

Copy the full URL (including the token) and open it in your browser.

If port 8888 is already in use (you have another Jupyter running), edit `docker_jupyter.sh` to use a different port, or stop the other Jupyter first.

### Step 5: open the notebooks

In the Jupyter file browser, you'll see two notebooks at the top level:

1. `ai_technical_debt.API.ipynb`: the tools tour.
2. `ai_technical_debt.example.ipynb`: the end-to-end pipeline demo.

We recommend reading them in that order. The API notebook explains every tool the project uses (PMD, javalang, XGBoost, Qwen-Coder, Maven, etc.) with small self-contained examples. The example notebook then runs the full pipeline on commons-lang3 using those tools.

### Step 6: run the API notebook

Open `ai_technical_debt.API.ipynb`. Run cells top to bottom (Shift+Enter on each cell, or "Run All" from the menu).

Total runtime: about 1-2 minutes. Each section is short and self-contained.

One thing to know about Section 8 (the Technical Debt Dataset): the dataset itself is 1.4 GB and not committed to git. The cell will try to download it from GitHub on first run. If you don't want the download, interrupt the cell (the kernel button in Jupyter, or Ctrl-C if the cell is hanging). The rest of the notebook works without it.

### Step 7: run the example notebook

Open `ai_technical_debt.example.ipynb`. Run cells top to bottom.

Total runtime: 5-6 minutes for a cold run. Most of that time is in Stage 7 (compile and test the refactorings using Maven). The two `mvn test` cells each take about 140 seconds.

Sections 5.2 and 5.3 are the climax. They run `mvn test` on the full commons-lang3 test suite (57,939 tests) twice. Once on a refactoring we expect to pass, once on a refactoring that compiles cleanly but is semantically broken. The contrast between those two cells is the project's main demonstration that compile-only validation is not enough.

### Optional: run the pipeline yourself from a script

We also include a unified runner that does the whole pipeline from the command line. From inside the container (`./docker_bash.sh`):

```bash
python production/scripts/run_pipeline.py \
  --repo /data/production/spikes/q1_agent_on_real_code/commons-lang \
  --records /data/production/data/refactor_records_3b.json \
  --top 10 \
  --repo-name commons-lang
```

This runs all 8 stages in sequence using pre-computed Stage 6 records (the agent ran on a UMIACS Nexus GPU; we ship the records). Total runtime about 1-2 minutes.

To run on a different Java repository, just change `--repo`. The pipeline auto-detects Maven and Gradle layouts. If you don't pass `--records`, the pipeline will run Stage 6 live with the smaller 0.5B model on CPU (slow and produces weak refactorings, but exercises the full flow).

### Optional: run the unit tests

There are 159 unit tests covering all stages. From inside the container:

```bash
cd /data
python -m unittest discover production/tests -v
```

Takes about 90 seconds. Should report `OK` at the end.

## Troubleshooting

### Docker build fails

**Symptom:** `./docker_build.sh` errors out partway through.

**Most common causes:**

1. **No internet or apt mirror is down.** The Dockerfile downloads packages from Ubuntu's repos and Maven Central. If your network blocks something, the build fails. Try running the build a second time; transient network errors often clear.

2. **Out of disk space.** The image is about 3.5 GB. The Docker build cache also takes space. Run `docker system df` to see usage and `docker system prune -a` to reclaim space (warning: this deletes all stopped containers and unused images).

3. **Wrong Docker version.** Some old Docker versions don't understand `--progress` flags. Build manually:
   ```bash
   docker build -t gpsaggese/umd_ai_technical_debt .
   ```

4. **PMD download fails.** The Dockerfile downloads PMD from a GitHub release. GitHub occasionally rate-limits unauthenticated requests. Wait a few minutes and retry.

If all else fails, paste the error message into a search engine. Most Docker build errors have well-known fixes.

### Jupyter says port 8888 is in use

**Symptom:** `./docker_jupyter.sh` errors with "bind: address already in use" or similar.

**Fix:** Either stop your other Jupyter (Ctrl-C in its terminal) or edit `docker_jupyter.sh` to map a different host port. Find the line `-p 8888:8888` and change the first 8888 to something else like 8899. Then access Jupyter at `http://localhost:8899/lab?token=...`.

### Container starts but Python imports fail

**Symptom:** A notebook cell errors with `ModuleNotFoundError: No module named 'production'` or similar.

**Cause:** The PYTHONPATH inside the container isn't set right. This usually means you're using a stale image from before our environment fixes.

**Fix:** Rebuild the image. From your host:

```bash
docker rmi gpsaggese/umd_ai_technical_debt
./docker_build.sh
./docker_jupyter.sh
```

### Stage 4 (Predict) takes longer than 5 minutes

**Symptom:** The Stage 4 cell in the example notebook hangs or runs for many minutes.

**Cause:** Stage 4 walks the AST of every Java file in the repo using javalang, then runs git operations to find each issue's host commit. On commons-lang3 (259 files, ~9000 commits), this normally takes 30-60 seconds. If it's much longer, something else is going on.

**Things to check:**

1. Is the disk thrashing? Stage 4 reads every file. If the repo is on a slow disk or network share, it'll be slow.
2. Is the git history huge? If you cloned the repo without `--depth`, you have all 9000+ commits. A `--depth 100` clone would be faster but might break the per-issue host-commit lookup.

If you really need to debug, add `logging.basicConfig(level=logging.DEBUG)` to Section 0 and watch what's happening per-file.

### Stage 7 (Validate) fails on every record

**Symptom:** Maven compile fails for all 10 records with "could not download dependency" or similar.

**Cause:** The first time Maven runs in the container, it downloads about 200 MB of dependencies from Maven Central. If that download fails (network, mirror down, etc.), every subsequent compile fails too.

**Fix:** From inside the container:

```bash
cd /tmp
git clone https://github.com/apache/commons-lang.git
cd commons-lang
mvn dependency:resolve
```

This pre-downloads the dependencies. After it succeeds, run Stage 7 again.

### Stage 7 fails with "javac not found" or "mvn not found"

**Symptom:** Stage 7 errors with command-not-found rather than compile errors.

**Cause:** Either Java or Maven isn't installed in the container, which means the Dockerfile didn't build properly.

**Fix:** Rebuild the image. The Dockerfile has explicit `apt-get install` blocks for Java 17 and Maven. If those didn't run, you have a broken image.

```bash
docker rmi gpsaggese/umd_ai_technical_debt
./docker_build.sh
```

### "PMD command not found" in Stage 2

**Symptom:** The Stage 2 cell in the example notebook errors with `pmd: command not found`.

**Cause:** PMD wasn't installed at the expected path during image build.

**Fix:** Same as above. Rebuild the image. The Dockerfile downloads PMD 7.23.0 from GitHub releases and adds it to PATH.

### The example notebook's Section 5.2/5.3 takes way longer than 140 seconds

**Symptom:** A `mvn test` cell runs for 5+ minutes without finishing.

**Cause:** First-time Maven test runs download more dependencies than first-time compile runs. The full test suite needs additional libraries (junit, assertj, etc.).

**What to do:** Be patient on the first run. After the test dependencies are cached, subsequent runs are about 140 seconds. If it really hangs, check the cell's output for download progress; if you see Maven still downloading after 10 minutes, something is wrong with your Maven Central access. Try the dependency pre-resolve trick from earlier.

### Section 8 of the API notebook starts a 1.4 GB download

**Symptom:** Cell 30 of the API notebook seems to be hanging while downloading something.

**Cause:** That cell tries to download the Technical Debt Dataset V2, which is 1.4 GB. We documented this in the cell's warning markdown.

**What to do:**

- If you want the dataset (you only need it to retrain the fault predictor): wait for the download to finish.
- If you don't want the dataset: interrupt the cell. The rest of the notebook does not need it. Click the kernel "interrupt" button (the square icon in the toolbar) or use Kernel → Interrupt Kernel from the menu.

### "permission denied" on docker_bash.sh or other scripts

**Symptom:** Running a docker_*.sh script gives `permission denied`.

**Cause:** The executable bit got dropped. Usually happens when the repo was cloned on Windows and the scripts came from Linux/macOS.

**Fix:**

```bash
chmod +x docker_*.sh
```

### Tests fail when running the unit test suite

**Symptom:** `python -m unittest discover production/tests` reports failures.

**Possible causes:**

1. **commons-lang3 is missing.** Some integration tests check that commons-lang3 source exists at `/data/production/spikes/q1_agent_on_real_code/commons-lang/`. If you cleaned that directory, those tests are skipped (not failed). True failures usually mean something else.

2. **PMD or Maven isn't on PATH.** The Stage 2 and Stage 7 tests call out to PMD and Maven. If those aren't installed, the tests fail.

3. **Something we didn't anticipate.** Run with verbose mode to see exactly which test failed:
   ```bash
   python -m unittest discover production/tests -v 2>&1 | tail -50
   ```

If you see real test failures (not skips), something has drifted. Most likely cause: someone modified one of the stage files without updating the corresponding test. Check git history of `production/stages/` recently.

## Where to look for more

### Reading order, by depth

If you have 5 minutes:
- This README.

If you have 30 minutes:
- This README, then run the example notebook.

If you have an hour:
- This README, the example notebook, the API notebook.

If you have 3+ hours:
- All of the above plus `LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md`.

### Code organization, top down

- `production/scripts/run_pipeline.py`: the unified entry point. Reading this top to bottom gives you the high-level flow.
- `production/stages/*.py`: one file per stage. Each is documented with a docstring at the top.
- `production/lib/metrics.py`: the bulk of the metric computation logic that Stage 4 depends on.
- `ai_technical_debt_utils.py`: the MVP-era helpers. The functions are organized into sections (database, feature engineering, ML, prioritization, code quality, RAG).
- `production/tests/`: the tests. Each test file mirrors one stage file. Reading test code is often the fastest way to understand what a function actually does and what it expects.

### Honest framing

We built a research demonstration, not a production tool. The pipeline finds, ranks, attempts, and validates refactorings on Java code. On commons-lang3 it works. On other Java repos it should mostly work. There are real limitations (single-method refactorings only, GPU needed for the good model, no iterative retry on failures, no closed-loop learning yet). We listed all of them in `LIMITATIONS_AND_FUTURE_IMPROVEMENTS.md`. We are not pretending this replaces SonarQube or Cursor or any commercial tool.

What it does demonstrate is that the open-source ecosystem (PMD, javalang, XGBoost, Qwen-Coder, Maven, sacrebleu, SQLite, Docker) has caught up enough to do the whole technical-debt-to-refactoring loop end-to-end without proprietary dependencies. That is the contribution.

## Authors and acknowledgments

- Akhil Kambhatla (primary author)
- Namratha Jeethendra (PMD rule mapping CSV)
- Hemanth Thulasiraman (early scope discussions)

Supervised by Prof. GP Saggese, DATA605, University of Maryland College Park, Spring 2026.

The fault predictor was trained on the [Lenarduzzi V2 Technical Debt Dataset](https://github.com/clowee/The-Technical-Debt-Dataset). The agent uses [Qwen2.5-Coder-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct), run on UMIACS Nexus computing infrastructure.