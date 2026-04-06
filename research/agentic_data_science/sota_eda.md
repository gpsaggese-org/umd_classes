# State of the Art in Agentic Exploratory Data Analysis

## Executive summary

Agentic exploratory data analysis (agentic EDA) is the application of
large language model (LLM) *agents*—systems that can plan, use tools
(e.g., SQL/Python), iterate, and self-correct—to the open-ended,
iterative work of understanding data, generating visual/statistical
probes, and synthesizing insights into reports or decisions. Recent
surveys define "LLM-based data agents" as autonomous or semi-autonomous
systems that interpret natural-language goals, plan/execute data-centric
tasks, and interact with external tools across workflows from EDA to
modeling. [[1]](https://arxiv.org/html/2412.14222v2)

From 2023–2026, the field has moved from *prompt-only copilots* toward
architectures that add (i) systematic planning and decomposition
(including graph-based task structures), (ii) tool-execution feedback
loops (self-debugging and verification), and (iii)
retrieval/knowledge-grounding (semantic models, notebook retrieval, and
skill libraries). This shift is visible in (a) benchmark
pressure—multi-step "data agent" tasks remain hard (e.g., very low
best-agent accuracy on DABStep’s hardest settings)
[[2]](https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com) and (b)
the emergence of systems that explicitly optimize plan quality,
verification, and provenance, such as DS-STAR’s plan-sufficiency judge
and iterative refinement [[3]](https://arxiv.org/abs/2509.21825),
RAGvis’s knowledge-graph–grounded EDA operation retrieval plus
self-correcting code execution
[[4]](https://github.com/google/ragvis), and agentic-model training
efforts like DeepAnalyze-8B that claim end-to-end autonomy from raw data
to "analyst-grade" reports with an agentic training paradigm.
[[5]](https://arxiv.org/abs/2510.16872)

On the industry side, conversational analytics products increasingly
rely on *governed semantic layers* (e.g., LookML, Snowflake semantic
models, Databricks Unity Catalog) to constrain and ground analytics,
while also embedding agent-like loops into notebooks/BI surfaces (e.g.,
Databricks "Data Science Agent", BigQuery "data agents", Copilot in
Power BI).
[[6]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)

Evaluation is rapidly maturing: benchmarks now span (i) single-file
code-and-answer tasks (DA-Code, DataSciBench),
[[7]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com) (ii)
open-ended scientific or business "insight discovery" with
partial-credit scoring (BLADE, InsightBench/InsightEval),
[[8]](https://arxiv.org/abs/2408.09667) (iii) heterogeneous
multi-source pipeline orchestration (KramaBench, FDABench),
[[9]](https://arxiv.org/abs/2506.06541) and (iv) visualization
generation/selection (VisEval, RAGvis).
[[10]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)

Key near-term research needs cluster around: reliable evaluation for
open-ended insight quality (beyond LLM-judges); systematic provenance
and reproducibility; secure tool use (sandboxing, least privilege,
prompt-injection resistance); and adaptive skill/tool selection that
scales to real enterprise stacks.
[[11]](https://arxiv.org/abs/2511.22884)

## Definitions and scope of agentic EDA

Exploratory data analysis (EDA) is the iterative process of
understanding a dataset (structure, quality, distributions,
relationships), forming hypotheses, and using lightweight
statistical/visual probes to surface patterns and anomalies—often before
formal modeling. Agentic EDA extends this by giving an LLM an
*operational role*: the system can decide what to do next, execute
actions in tools, and revise its approach based on intermediate results.

A widely used data-agent definition (from surveys) frames an "LLM-based
data agent" as autonomous or semi-autonomous software that understands
natural-language instructions, plans and executes data tasks, and
interacts with tools to achieve objectives "from exploratory data
analysis to machine learning model development."
[[12]](https://arxiv.org/html/2412.14222v2)

In practice, "agentic EDA" typically includes some (not always all) of
the following autonomy and tooling elements:

- **Iterative planning and decomposition** (e.g., decide which
  diagnostics/plots to run; break tasks into sub-questions).
  [[13]](https://arxiv.org/abs/2509.21825)
- **Tool use with execution feedback** (Python/SQL execution, error
  fixing, re-running).
  [[14]](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)
- **Insight synthesis** (structured reports with claims backed by
  computed outputs).
  [[15]](https://research.google/blog/ds-star-a-state-of-the-art-versatile-data-science-agent/)
- **Visualization selection/generation** as a first-class activity (not
  just "pretty plots," but semantically correct analysis operations and
  chart choices).
  [[10]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
- **Memory / provenance / governance** (retain intermediate context,
  record tool traces, and ground queries on semantic definitions).
  [[16]](https://arxiv.org/html/2407.06423v4)

It is useful to separate *agentic EDA* from adjacent but distinct areas:

- **Conversational BI / NLQ**: natural-language questions translated
  into governed queries over a semantic model (e.g., LookML). This can
  be agentic, but is often "single-shot Q&A" rather than open-ended
  exploration.
  [[17]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
- **NL2Vis**: generate a visualization given a natural-language spec
  (the spec is provided), while agentic EDA often includes *choosing*
  what to visualize without a precise user spec.
  [[10]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
- **Autonomous data science / ML engineering**: broader pipelines that
  include feature engineering/modeling/experimentation; agentic EDA is a
  core sub-loop that these systems frequently emphasize.
  [[18]](https://arxiv.org/abs/2509.21825)

## Research systems and representative papers

The table below focuses on systems/papers that materially shaped agentic
EDA capabilities, architectures, or evaluation between 2023–2026.

### Systems comparison table

<table style="width:85%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th>Name</th>
<th style="text-align: right;">Year</th>
<th>Architecture type</th>
<th>Key features</th>
<th>Primary source</th>
<th>Limitations / caveats</th>
</tr>
</thead>
<tbody>
<tr>
<td>LIDA</td>
<td style="text-align: right;">2023</td>
<td>LLM pipeline for visualization + narrative</td>
<td>Modular pipeline (summarization/goal exploration/vis
generation/infographics); positioned as a "language interface for data
analysis." <a
href="https://github.com/microsoft/lida?utm_source=chatgpt.com">[19]</a></td>
<td><a
href="https://github.com/microsoft/lida?utm_source=chatgpt.com">[20]</a></td>
<td>Primarily prompt/pipeline-driven; evaluation/faithfulness remains
challenging; can be brittle on schema ambiguity and complex tasks. <a
href="https://aclanthology.org/2025.emnlp-main.836.pdf">[21]</a></td>
</tr>
<tr>
<td>Data Formulator 2</td>
<td style="text-align: right;">2024</td>
<td>Human-in-the-loop visualization + transformation assistant</td>
<td>Interactive "create chart by describing intent" workflow; emphasizes
iterative transformation with AI assistance. <a
href="https://www.microsoft.com/en-us/research/project/lida-automatic-generation-of-grammar-agnostic-visualizations/?utm_source=chatgpt.com">[22]</a></td>
<td><a
href="https://www.microsoft.com/en-us/research/project/lida-automatic-generation-of-grammar-agnostic-visualizations/?utm_source=chatgpt.com">[22]</a></td>
<td>Not designed as a fully autonomous agent; relies on UI interaction
and user steering (by design). <a
href="https://www.microsoft.com/en-us/research/project/lida-automatic-generation-of-grammar-agnostic-visualizations/?utm_source=chatgpt.com">[22]</a></td>
</tr>
<tr>
<td>InfiAgent-DABench / DAAgent</td>
<td style="text-align: right;">2024</td>
<td>ReAct-style tool-executing agent benchmark + baseline agent</td>
<td>Benchmark explicitly for LLM agents on data analysis tasks with an
execution environment; includes automated evaluation via "closed-form"
formatting. <a
href="https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com">[23]</a></td>
<td><a
href="https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com">[24]</a></td>
<td>Dataset size is modest relative to real workloads; still limited in
heterogeneity vs multi-source enterprise settings. <a
href="https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com">[25]</a></td>
</tr>
<tr>
<td>DA-Code / DA-Agent</td>
<td style="text-align: right;">2024</td>
<td>Executable data-science code-gen benchmark</td>
<td>500 tasks across wrangling/ML/EDA with executable environment; SOTA
LLMs + baseline agent reach only ~30.5% accuracy in reported
experiments. <a
href="https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com">[26]</a></td>
<td><a
href="https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com">[26]</a></td>
<td>Strong dependence on coding/grounding; evaluation focuses on
correctness rather than "insight quality" in open-ended sense. <a
href="https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com">[7]</a></td>
</tr>
<tr>
<td>DS-Agent</td>
<td style="text-align: right;">2024</td>
<td>Agent + case-based reasoning for end-to-end data science</td>
<td>Uses case-based reasoning (CBR) to structure iterative improvement
using prior "cases" (e.g., Kaggle knowledge). <a
href="https://arxiv.org/abs/2402.17453">[27]</a></td>
<td><a href="https://arxiv.org/abs/2402.17453">[27]</a></td>
<td>More focused on model-building than pure EDA; quality depends on
case retrieval and domain match. <a
href="https://arxiv.org/abs/2402.17453">[28]</a></td>
</tr>
<tr>
<td>LAMBDA</td>
<td style="text-align: right;">2024</td>
<td>Multi-agent roles (programmer + inspector) + UI intervention</td>
<td>Open-source "code-free" multi-agent data analysis system with
programmer/inspector roles; supports user intervention and "knowledge
integration mechanism." <a
href="https://arxiv.org/abs/2407.17535">[29]</a></td>
<td><a href="https://arxiv.org/abs/2407.17535">[30]</a></td>
<td>Practical reliability depends on safe execution and human oversight;
system-level rigor varies by task and tooling setup. <a
href="https://arxiv.org/abs/2407.17535">[31]</a></td>
</tr>
<tr>
<td>InsightBench / AgentPoirot</td>
<td style="text-align: right;">2024</td>
<td>Multi-step "insight discovery" agent benchmark + baseline agent</td>
<td>100 business datasets with planted insights; evaluates end-to-end
analytics: propose questions → interpret → summarize insights + actions;
uses LLM-based evaluator (LLaMA-3-Eval). <a
href="https://arxiv.org/html/2407.06423v4">[32]</a></td>
<td><a href="https://arxiv.org/html/2407.06423v4">[33]</a></td>
<td>Synthetic data may not capture all real enterprise messiness;
LLM-as-judge evaluation can drift or encode biases; still an open
research issue. <a
href="https://arxiv.org/html/2407.06423v4">[34]</a></td>
</tr>
<tr>
<td>AgentAda</td>
<td style="text-align: right;">2025</td>
<td>Skill-library selection + RAG-based matcher + code generator</td>
<td>Learns/uses "analytics skills" from a library; pipeline: question
generator → RAG skill matcher → code generator; introduces KaggleBench
for evaluation and reports preference-based human eval. <a
href="https://arxiv.org/abs/2504.07421">[35]</a></td>
<td><a href="https://arxiv.org/abs/2504.07421">[35]</a></td>
<td>Skill coverage/curation becomes the bottleneck; evaluation of
"insightfulness" remains hard to automate at scale. <a
href="https://arxiv.org/abs/2504.07421">[36]</a></td>
</tr>
<tr>
<td>RAGvis</td>
<td style="text-align: right;">2025</td>
<td>KG-grounded EDA retrieval + self-correcting coding agent</td>
<td>Offline: build/enrich EDA knowledge graph from notebooks; Online:
retrieve+align EDA ops for new dataset, refine with LLM,
generate+execute+fix code; reports near-100% pass rates and improved
Recall@k vs LIDA on VisEval/KaggleVisBench. <a
href="https://github.com/google/ragvis">[4]</a></td>
<td><a
href="https://aclanthology.org/2025.emnlp-main.836.pdf">[37]</a></td>
<td>Executes LLM-generated code (explicit safety warning); depends on
notebook corpus quality and taxonomy alignment. <a
href="https://github.com/google/ragvis">[38]</a></td>
</tr>
<tr>
<td>Data Interpreter</td>
<td style="text-align: right;">2024–2025</td>
<td>Graph-based hierarchical planning + programmable nodes +
verification</td>
<td>Uses hierarchical graph modeling for task decomposition and
"programmable node generation" for refinement/verification; reports
large improvements on data-agent benchmarks (e.g., InfiAgent-DABench).
<a href="https://arxiv.org/abs/2402.18679">[39]</a></td>
<td><a
href="https://aclanthology.org/2025.findings-acl.1016/">[40]</a></td>
<td>Strong claims rely on evaluation setup and benchmark coverage;
system complexity raises reproducibility and monitoring needs. <a
href="https://github.com/Kaggle/kaggle-benchmarks">[41]</a></td>
</tr>
<tr>
<td>DS-STAR</td>
<td style="text-align: right;">2025</td>
<td>Multi-agent pipeline + plan sufficiency verification loop</td>
<td>Adds (i) data file analysis across heterogeneous formats, (ii) LLM
judge verifying plan sufficiency, (iii) sequential plan refinement;
reported SOTA on DABStep, KramaBench, DA-Code. <a
href="https://arxiv.org/abs/2509.21825">[3]</a></td>
<td><a href="https://arxiv.org/abs/2509.21825">[3]</a></td>
<td>Higher accuracy can come with higher cost/latency due to iterative
refinement; verification depends on judge reliability. <a
href="https://arxiv.org/abs/2509.21825">[42]</a></td>
</tr>
<tr>
<td>DeepAnalyze-8B</td>
<td style="text-align: right;">2025</td>
<td><em>Agentic model</em> (trained for orchestration) + open-source
model/code/data</td>
<td>Proposes curriculum-based agentic training with data-grounded
trajectory synthesis; claims end-to-end autonomous data science and
open-sources model/code/training data. <a
href="https://arxiv.org/abs/2510.16872">[43]</a></td>
<td><a href="https://arxiv.org/abs/2510.16872">[5]</a></td>
<td>As with any agentic code-executing system: needs safe sandboxing,
careful tool constraints, and robust evaluation; practical
generalization and bias remain active research topics. <a
href="https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/">[44]</a></td>
</tr>
<tr>
<td>TiInsight</td>
<td style="text-align: right;">2024</td>
<td>Staged EDA system (clarify/decompose → text-to-SQL →
visualization)</td>
<td>Production-oriented cross-domain EDA system: hierarchical data
context generation, question clarification/decomposition, text-to-SQL,
visualization; claims strong text-to-SQL accuracy on standard
benchmarks. <a href="https://arxiv.org/abs/2412.07214">[45]</a></td>
<td><a href="https://arxiv.org/abs/2412.07214">[45]</a></td>
<td>More "EDA via SQL+chart" than general agentic EDA; depends on
database schema modeling and intent clarification quality. <a
href="https://arxiv.org/abs/2412.07214">[45]</a></td>
</tr>
<tr>
<td>AgenticData</td>
<td style="text-align: right;">2025</td>
<td>Agentic analytics over heterogeneous data</td>
<td>Proposed as an "agentic data analytics system for heterogeneous
data" (CoRR). <a
href="https://dblp.org/rec/journals/corr/abs-2508-05002">[46]</a></td>
<td><a
href="https://dblp.org/rec/journals/corr/abs-2508-05002">[46]</a></td>
<td>Insufficient detail here to characterize the full stack without
deeper paper review; treat as representative of the "heterogeneous data
agent" direction. <a
href="https://dblp.org/rec/journals/corr/abs-2508-05002">[47]</a></td>
</tr>
</tbody>
</table>

### Additional notes on "state of the art" claims

"State of the art" is benchmark-dependent, and papers increasingly
report SOTA in specific regimes:

- **Multi-step heterogeneous analytics**: DS-STAR explicitly reports
  SOTA across DABStep, KramaBench, and DA-Code.
  [[3]](https://arxiv.org/abs/2509.21825)
- **Insight discovery**: InsightBench introduces an end-to-end
  benchmark + baseline agent AgentPoirot, but InsightEval argues
  InsightBench has flaws and proposes revised criteria and
  metrics—illustrating that "SOTA" can be unstable when the benchmark
  itself is evolving. [[34]](https://arxiv.org/html/2407.06423v4)
- **EDA visualization operation selection + reliability**: RAGvis
  reports substantial improvements over LIDA (Recall@k), near-100% code
  pass rates, and assesses visual quality via VLM-as-judge.
  [[37]](https://aclanthology.org/2025.emnlp-main.836.pdf)
- **Model-level agentic autonomy**: DeepAnalyze claims advantage over
  "workflow-based" agents using proprietary LLMs, using an agentic
  training approach and releasing model/code/data.
  [[43]](https://arxiv.org/abs/2510.16872)

## Industry products and platforms

Agentic EDA capabilities increasingly ship as "analytics agents"
embedded into the data stack: notebooks, BI tools, warehouses,
governance layers, and cloud-centric "data agents."

Below, "agentic" typically appears as: (i) conversational interfaces
grounded by a semantic model, (ii) generated SQL/Python with execution,
(iii) iterative refinement/error fixing, and (iv) governance/provenance
features (catalog grounding, logging, admin controls).

### Representative product directions (official docs / blogs)

**OpenAI[[48]](https://aclanthology.org/2025.emnlp-main.836.pdf)**:
ChatGPT’s "data analysis" experience supports interactive tables/charts
from uploaded data, and is positioned as a way to explore and visualize
datasets in-chat.
[[49]](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)
Separately, OpenAI’s "Deep research" guide describes models optimized
for browsing/searching and analysis, with support for tools including
web/file search and a code interpreter tool.
[[50]](https://developers.openai.com/api/docs/guides/deep-research/)

**Microsoft[[51]](https://arxiv.org/abs/2506.06541)**: Copilot in
Fabric/Power BI is positioned to "transform and analyze data, generate
insights, and create visualizations and reports," including a standalone
Copilot experience for finding and answering questions about data
sources accessible to the user.
[[52]](https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview)
(Tenant controls and operational constraints are emphasized in enabling
docs, reflecting enterprise governance concerns.)
[[53]](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi)

**Google
Cloud[[54]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com)**:
BigQuery supports "data agents" that carry table metadata and
instructions to answer questions about selected tables/views/UDFs,
indicating a first-party agent abstraction connected to warehouse
objects.
[[55]](https://docs.cloud.google.com/bigquery/docs/create-data-agents)
Looker’s Conversational Analytics explicitly uses Gemini and the LookML
semantic model as the "source of truth" for consistent metric
definitions, emphasizing semantic grounding as a core reliability
strategy.
[[56]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)

**Databricks[[57]](https://arxiv.org/abs/2402.17453)**: Databricks
"AI/BI" and "Genie spaces" describe a conversational interface that
domain experts configure with datasets, sample queries, and guidelines;
Genie can translate business questions into analytical queries and
produce visualizations, and continues updating as data/questions evolve.
[[58]](https://docs.databricks.com/aws/en/genie/) Databricks’
"Assistant Data Science Agent" blog describes an "autonomous partner" in
notebooks/SQL editor that explores data, generates/runs code, and fixes
errors, grounded in Unity Catalog.
[[59]](https://www.databricks.com/blog/introducing-databricks-assistant-data-science-agent)

**Snowflake[[60]](https://github.com/google/ragvis)**: Cortex Analyst
is described as a managed NL-to-structured-data analytics capability
available via REST API and based on a "Semantic Model," aimed at
reliable answering over structured data.
[[61]](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
Cortex Agents are positioned as orchestration that can call tools like
Cortex Analyst and Cortex Search, bridging structured + unstructured
within the Snowflake perimeter.
[[62]](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents)

**Amazon Web
Services[[63]](https://aclanthology.org/2025.emnlp-main.836.pdf)**:
Amazon Q in QuickSight supports natural language querying and adding
visuals/dashboards via "Ask" experiences; QuickSight Topics act as a
semantic index mapping terms to fields/values to generate correct
answers.
[[64]](https://aws.amazon.com/blogs/mt/gain-insights-with-natural-language-query-into-your-aws-environment-using-amazon-cloudtrail-and-amazon-q-in-quicksight/)

**Tableau[[65]](https://github.com/Kaggle/kaggle-benchmarks)**:
Tableau Agent is positioned as a conversational assistant to explore
data, create visualizations, and uncover insights; official help docs
emphasize using the assistant alongside the Tableau UI for faster visual
analysis.
[[66]](https://help.tableau.com/current/online/en-us/web_author_einstein.htm)

**NVIDIA[[67]](https://arxiv.org/abs/2511.22884)**: Security guidance
for sandboxing agentic workflows stresses isolating code execution,
minimizing exposed secrets, and enforcing least privilege—highly
relevant to analytics agents that run generated code.
[[68]](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)

### Industry pattern: semantic grounding as "anti-hallucination infrastructure"

Across warehouses/BI tools, a consistent reliability theme is **semantic
grounding**: the agent is constrained by curated metric definitions,
table metadata, governance catalogs, and controlled query surfaces
(e.g., LookML, Snowflake semantic models, QuickSight topics, Databricks
catalog).
[[69]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
This aligns with research findings that "tool orchestration and
multimodal reasoning remain unresolved challenges" and that many systems
still lack explicit trust/safety mechanisms—creating pressure for
enterprise-grade constraints. [[70]](https://arxiv.org/abs/2510.04023)

## Common architectures and component stacks

Most agentic EDA systems can be described as variations on a
**plan–act–observe–reflect** loop, with explicit components for
planning, tool routing, memory/provenance, and synthesis. Surveys
covering dozens of data science agents highlight planning style, tool
orchestration depth, and trust/safety mechanisms as key cross-cutting
design dimensions. [[71]](https://arxiv.org/abs/2510.04023)

### Core components

**Planner / decomposer.**  
High-performing systems often make planning explicit (and revisable).
DS-STAR’s core idea is a sequential plan that starts simple and is
iteratively refined until a judge verifies "sufficiency."
[[3]](https://arxiv.org/abs/2509.21825) Data Interpreter formalizes a
graph-based decomposition structure (hierarchical graph modeling) to
manage dependent subproblems and dynamic intermediate data.
[[72]](https://arxiv.org/abs/2402.18679)

**Tool-use layer (SQL/Python/visualization).**  
Tool execution is the defining capability separating "agentic" from pure
chat. In practice, this includes Python environments
(notebooks/sandboxes), SQL engines, and plotting libraries.
[[73]](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)

**Memory and workspace.**  
"Memory" here includes retained dataset summaries, derived tables,
intermediate code/results, and retrieved artifacts (e.g., notebook
snippets). DeepAnalyze’s demo emphasizes a workspace that can manage
heterogeneous files and export reports.
[[74]](https://github.com/ruc-datalab/DeepAnalyze/blob/main/demo/chat_v2/README.md)

**Critic / verifier / judge.**  
A prominent 2024–2026 direction is *verification-centric agents*: plan
sufficiency judges (DS-STAR), [[75]](https://arxiv.org/abs/2509.21825)
code-execution pass-rate objectives and self-correction (RAGvis),
[[21]](https://aclanthology.org/2025.emnlp-main.836.pdf) and
LLM-as-judge evaluation for insight quality (InsightBench, InsightEval).
[[34]](https://arxiv.org/html/2407.06423v4)

**Visualization engine.**  
RAGvis treats EDA as a sequence of semantically typed operations and
evaluates recall against a taxonomy of EDA operations and chart
attributes, plus visual quality via a VLM judge.
[[37]](https://aclanthology.org/2025.emnlp-main.836.pdf) VisEval
provides a benchmark for visualization generation methods (NL2Vis) with
labeled ground truth.
[[76]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)

**Provenance and logging.**  
Reproducibility requires capturing prompts, tool calls, intermediate
data artifacts, and environment metadata. Evaluation frameworks like
Kaggle Benchmarks explicitly focus on structured task definitions and
reproducible runs. [[77]](https://github.com/Kaggle/kaggle-benchmarks)
InsightBench reports multi-seed runs and documents evaluation
metrics/prompt details to support reproducibility.
[[32]](https://arxiv.org/html/2407.06423v4)

### Typical architecture diagram

    flowchart TB
      U[User goal / question] --> P[Planner & Decomposer]
      P -->|subtasks| R[Retriever / Context Builder]
      R -->|schema, docs, prior notebooks| M[(Memory / Workspace)]

      P --> T[Tool Router]
      T --> SQL[SQL Engine]
      T --> PY[Python Sandbox / Notebook Kernel]
      T --> VIZ[Visualization Library]

      SQL --> O[Observations: tables/metrics]
      PY --> O
      VIZ --> O

      O --> C[Critic / Verifier]
      C -->|revise plan| P
      C -->|fix code| T

      O --> S[Report / Insight Synthesizer]
      S --> OUT[Charts + narrative + recommendations]

      subgraph Provenance
        L[Trace log: prompts, tool calls, artifacts]
      end

      P --> L
      T --> L
      O --> L
      S --> L

This abstraction maps cleanly onto many concrete systems: DS-STAR’s plan
verification loop (P↔C), [[75]](https://arxiv.org/abs/2509.21825)
RAGvis’s retrieval of EDA ops + self-correcting code execution
(R/T/PY/VIZ/C), [[4]](https://github.com/google/ragvis) and AgentAda’s
skill matcher + code generator (R plus a "skill library" tool selection
layer). [[35]](https://arxiv.org/abs/2504.07421)

### Agent loop diagram

    sequenceDiagram
      participant User
      participant Agent as EDA Agent
      participant Tools as Tools (SQL/Python/Viz)
      participant Judge as Critic/Judge
      participant Log as Provenance Log

      User->>Agent: Goal + data sources
      Agent->>Log: Record goal, dataset metadata
      Agent->>Agent: Plan / decompose
      Agent->>Tools: Execute step (query / code / plot)
      Tools-->>Agent: Result or error
      Agent->>Log: Store code, outputs, artifacts
      Agent->>Judge: Verify (plan sufficiency / correctness / insight quality)
      Judge-->>Agent: Feedback (revise / continue)
      alt Needs revision
        Agent->>Agent: Update plan or repair code
        Agent->>Tools: Re-execute
      else Sufficient
        Agent->>Agent: Synthesize insights + visuals
        Agent->>Log: Final report + trace summary
        Agent-->>User: Report with figures + claims
      end

### Visual grounding examples

## Benchmarks and evaluation datasets

Evaluation is central because EDA is open-ended: there are many valid
analysis paths, "partially correct" plans, and multiple ways to express
correct insights. BLADE explicitly focuses on evaluating *approaches* to
open-ended research questions (not just final numeric answers) and
provides computational matching methods to compare agent decisions to
expert-derived ground truth. [[78]](https://arxiv.org/abs/2408.09667)

Recent benchmarks emphasize different slices of agentic EDA:

- **Executable correctness**: can the agent write/run correct code to
  produce a target answer? (DA-Code, DataSciBench).
  [[7]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com)
- **Multi-step reasoning over data + docs**: can the agent iteratively
  process data and cross-reference instructions across steps? (DABStep).
  [[2]](https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com)
- **End-to-end insight discovery**: can the agent decide what questions
  to ask and tell a coherent story? (InsightBench, InsightEval).
  [[34]](https://arxiv.org/html/2407.06423v4)
- **Pipeline orchestration across heterogeneous files/sources**: can the
  system design and execute a multi-stage pipeline from "data lake" to
  insight? (KramaBench, FDABench).
  [[9]](https://arxiv.org/abs/2506.06541)
- **Visualization generation and semantic correctness**: can it
  pick/generate correct charts and code paths? (VisEval, RAGvis
  metrics).
  [[10]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
- **Data governance tasks**: can it perform governance-oriented work
  (quality/correctness of data itself)? (DataGovBench).
  [[79]](https://arxiv.org/html/2512.04416v2)

### Benchmarks table

<table style="width:85%;">
<colgroup>
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 21%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr>
<th>Benchmark</th>
<th>Tasks</th>
<th>Metrics (typical)</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>InfiAgent-DABench (DAEval)</td>
<td>Agent-based analysis questions over CSVs with execution environment;
questions are converted to closed-form for auto-eval. <a
href="https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com">[23]</a></td>
<td>Accuracy / auto-graded outputs; success under tool execution. <a
href="https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com">[25]</a></td>
<td><a
href="https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com">[24]</a></td>
</tr>
<tr>
<td>DA-Code</td>
<td>500 agentic data science code tasks (wrangling/ML/EDA) in executable
environment; best reported accuracy ~30.5%. <a
href="https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com">[26]</a></td>
<td>Exact correctness/accuracy in executable sandbox. <a
href="https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com">[26]</a></td>
<td><a
href="https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com">[26]</a></td>
</tr>
<tr>
<td>DSBench</td>
<td>Realistic data science tasks: 466 data analysis + 74 modeling tasks;
reports low agent success rates and "relative performance gap." <a
href="https://arxiv.org/abs/2409.07703">[80]</a></td>
<td>Task success rate; RPG and cost/time analyses (paper-dependent). <a
href="https://arxiv.org/html/2409.07703v1">[81]</a></td>
<td><a href="https://arxiv.org/abs/2409.07703">[82]</a></td>
</tr>
<tr>
<td>DataSciBench</td>
<td>Broad benchmark with semi-automated GT generation +
Task–Function–Code evaluation framework; compares API and open models.
<a href="https://arxiv.org/abs/2502.13897">[83]</a></td>
<td>Evaluation via precisely defined metrics/programmatic rules (TFC);
model comparisons. <a
href="https://arxiv.org/abs/2502.13897">[83]</a></td>
<td><a href="https://arxiv.org/abs/2502.13897">[84]</a></td>
</tr>
<tr>
<td>DABStep</td>
<td>450+ multi-step data analysis challenges derived from a financial
analytics platform; combines code-based data processing and reasoning
over heterogeneous documentation. <a
href="https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com">[85]</a></td>
<td>Accuracy; difficulty-stratified performance; strong performance gap
reported. <a
href="https://huggingface.co/blog/dabstep?utm_source=chatgpt.com">[86]</a></td>
<td><a
href="https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com">[2]</a></td>
</tr>
<tr>
<td>KramaBench</td>
<td>End-to-end "data lake to insight" pipelines; 104 challenges spanning
1700 files, 24 sources, 6 domains; evaluates orchestration. <a
href="https://arxiv.org/abs/2506.06541">[87]</a></td>
<td>Pipeline correctness + intermediate step evaluation (framework
provided). <a href="https://github.com/mitdbg/KramaBench">[88]</a></td>
<td><a href="https://arxiv.org/abs/2506.06541">[87]</a></td>
</tr>
<tr>
<td>FDABench</td>
<td>2,007 tasks for multi-source analytical scenarios combining
structured and unstructured data; evaluates quality, accuracy, latency,
token cost. <a
href="https://arxiv.org/abs/2509.02473?utm_source=chatgpt.com">[89]</a></td>
<td>Response quality/accuracy; latency; token cost; system trade-offs.
<a
href="https://arxiv.org/abs/2509.02473?utm_source=chatgpt.com">[90]</a></td>
<td><a
href="https://arxiv.org/abs/2509.02473?utm_source=chatgpt.com">[90]</a></td>
</tr>
<tr>
<td>InsightBench</td>
<td>100 business datasets with planted insights; evaluates end-to-end
analytics and uses LLaMA-3-Eval as a primary metric. <a
href="https://arxiv.org/html/2407.06423v4">[32]</a></td>
<td>LLM-as-judge insight similarity; ROUGE variants; multi-step scoring.
<a href="https://arxiv.org/html/2407.06423v4">[32]</a></td>
<td><a href="https://arxiv.org/html/2407.06423v4">[33]</a></td>
</tr>
<tr>
<td>InsightEval</td>
<td>Expert-curated benchmark addressing shortcomings in InsightBench;
proposes criteria and novel metrics for exploratory performance +
novelty. <a href="https://arxiv.org/abs/2511.22884">[91]</a></td>
<td>Insight metrics + novelty measurement; exploratory performance
metric. <a href="https://arxiv.org/abs/2511.22884">[91]</a></td>
<td><a href="https://arxiv.org/abs/2511.22884">[92]</a></td>
</tr>
<tr>
<td>BLADE</td>
<td>12 datasets + research questions from scientific literature; ground
truth from expert analyses; evaluates agent decisions on open-ended
data-driven science. <a
href="https://arxiv.org/abs/2408.09667">[78]</a></td>
<td>Automated matching to expert analyses; multifaceted evaluation
beyond a single answer. <a
href="https://arxiv.org/abs/2408.09667">[93]</a></td>
<td><a href="https://arxiv.org/abs/2408.09667">[78]</a></td>
</tr>
<tr>
<td>VisEval</td>
<td>Large NL2Vis benchmark (2,524 queries across 146 DBs) with labeled
ground truth and automated evaluation toolkit. <a
href="https://arxiv.org/html/2407.00981v1">[94]</a></td>
<td>Execution/semantic correctness of generated visualizations; toolkit
support. <a
href="https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/">[95]</a></td>
<td><a
href="https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/">[95]</a></td>
</tr>
<tr>
<td>AIDABench</td>
<td>End-to-end data analytics benchmark with 600+ tasks across question
answering, visualization, and file generation. <a
href="https://arxiv.org/abs/2603.15636?utm_source=chatgpt.com">[96]</a></td>
<td>End-to-end task completion across modalities (paper-defined). <a
href="https://arxiv.org/abs/2603.15636?utm_source=chatgpt.com">[96]</a></td>
<td><a
href="https://arxiv.org/abs/2603.15636?utm_source=chatgpt.com">[96]</a></td>
</tr>
<tr>
<td>DataGovBench</td>
<td>Data governance tasks grounded in real-world scenarios; targets
correctness/quality of data itself, beyond answer generation. <a
href="https://arxiv.org/html/2512.04416v2">[79]</a></td>
<td>Task success across governance workflows (paper-defined). <a
href="https://arxiv.org/html/2512.04416v2">[79]</a></td>
<td><a href="https://arxiv.org/html/2512.04416v2">[79]</a></td>
</tr>
</tbody>
</table>

### Evaluation toolchains and reproducibility infrastructure

Beyond benchmark datasets, **evaluation harnesses** are appearing as
products/community infrastructure. Kaggle’s Benchmarks initiative and
the `kaggle-benchmarks` library emphasize reproducibility by capturing
inputs/outputs and providing a structured framework for tasks and
assertions. [[97]](https://github.com/Kaggle/kaggle-benchmarks) This
kind of harness is directly useful for agentic EDA, where stochasticity
and hidden intermediate steps otherwise make comparisons unreliable.

## Capabilities, failure modes, and research agenda

### Typical capabilities of agentic EDA systems

Across research systems and products, common "agentic EDA" capabilities
cluster into recurring task families:

1\) **Data access and understanding** - Load and inspect diverse data
artifacts (CSV, logs, documents; sometimes databases).
[[98]](https://arxiv.org/abs/2509.21825)  
- Summarize schema/column semantics and detect data quality issues.
DS-STAR emphasizes automatic exploration and context extraction across
diverse formats. [[3]](https://arxiv.org/abs/2509.21825)  
- In enterprise tools, this is mediated by catalogs/semantic layers
(LookML, semantic models) for consistent definitions.
[[17]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)

2\) **Exploration probes: statistics + visualization** - Produce
univariate/bivariate/multivariate plots and summary tables; RAGvis
explicitly models EDA operations with a taxonomy and evaluates semantic
correctness (Recall@k, pass rate).
[[21]](https://aclanthology.org/2025.emnlp-main.836.pdf)  
- Generate visualization recommendations, often using benchmarks like
VisEval or internal notebook corpora.
[[10]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)

3\) **Iterative, multi-step reasoning** - Multi-step sequences that
combine code-based transformations with contextual reasoning over
documentation. DABStep is explicitly built to test this.
[[2]](https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com)  
- Plan refinement and verification loops (DS-STAR) or graph-based
decomposition for dynamic dependencies (Data Interpreter).
[[99]](https://arxiv.org/abs/2509.21825)

4\) **Insight discovery and reporting** - Generate narrative insights
and recommended actions (InsightBench:
descriptive/diagnostic/predictive/prescriptive insights).
[[32]](https://arxiv.org/html/2407.06423v4)  
- Produce "analyst-grade" structured reports and exportable artifacts
(DeepAnalyze demo explicitly supports Markdown/PDF export).
[[100]](https://github.com/ruc-datalab/DeepAnalyze/blob/main/demo/chat_v2/README.md)

### Common failure modes observed in benchmarks and deployments

Agentic EDA failures are not just "hallucinations" in text—they’re often
**workflow failures**: wrong plan, wrong tool choice, wrong query, or
correct code with incorrect interpretation.

**Low task success on realistic multi-step benchmarks.**  
DABStep reports a substantial performance gap, with very low accuracy
for the strongest agents in the published benchmark context, indicating
that multi-step, doc-grounded analytics remains unsolved.
[[86]](https://huggingface.co/blog/dabstep?utm_source=chatgpt.com)
DSBench similarly reports that even the best agents struggle, solving
only a minority of realistic analysis tasks (e.g., 34.12% of data
analysis tasks in the authors’ evaluation).
[[81]](https://arxiv.org/html/2409.07703v1) DA-Code reports low
accuracy (~30.5% for current best LLMs in their experiments),
reinforcing that "execute correct code end-to-end" is still hard.
[[26]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com)

**Planning errors and "analysis myopia."**  
Multiple systems motivate themselves by arguing that LLMs produce
suboptimal plans or cannot verify plan sufficiency without ground
truth—DS-STAR directly targets this with plan verification.
[[3]](https://arxiv.org/abs/2509.21825)

**Tool-selection and retrieval brittleness.**  
Agents can fail by selecting the wrong tool or using the correct tool
incorrectly. This is not only a capability issue but also a security
risk (see below). [[101]](https://arxiv.org/abs/2504.19793)

**Code reliability vs semantic correctness trade-off.**  
RAGvis separates (i) retrieval of EDA operation intent and (ii) code
generation/execution, reporting near-100% pass rates while also
measuring semantic recall of EDA operations, illustrating that "runs
without error" is not the same as "correct analysis."
[[21]](https://aclanthology.org/2025.emnlp-main.836.pdf)

**Evaluation misalignment and judge instability.**  
InsightBench uses LLM-based evaluation (LLaMA-3-Eval), while InsightEval
argues existing insight benchmarks have format/objective flaws and
proposes new criteria and metrics—highlighting that evaluation itself is
an active research frontier.
[[34]](https://arxiv.org/html/2407.06423v4)

### Reproducibility, safety, and evaluation recommendations

**Reproducibility and provenance** - Treat agentic EDA as an *executable
experiment*: log prompts, tool calls, code, dataset hashes/versions,
random seeds, and environment details; many modern evaluation harnesses
are built precisely to capture such structured runs.
[[77]](https://github.com/Kaggle/kaggle-benchmarks)  
- Prefer **programmatic metrics** (execution accuracy, exact match on
computed outputs) where possible, and explicitly separate them from
**insight-quality metrics** (novelty, usefulness, decision relevance),
which often need hybrid evaluation (human + automated).
[[102]](https://arxiv.org/abs/2408.09667)  
- When using LLM-as-judge, run multi-judge or judge-calibration
experiments and report sensitivity (model choice, prompt templates,
order effects). The benchmark literature increasingly documents such
evaluation strategies. [[103]](https://arxiv.org/html/2407.06423v4)

**Safety: sandboxing, least privilege, and prompt-injection
resistance** - Any agent that executes generated code must run inside
strong isolation. RAGvis includes an explicit warning that it executes
LLM-generated code on the local machine.
[[104]](https://github.com/google/ragvis) NVIDIA’s guidance emphasizes
starting sandboxes with minimal secrets and injecting only task-scoped
credentials through safer mechanisms.
[[68]](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)  
- Treat retrieved content as untrusted. The "Indirect Prompt Injection"
line of work argues LLM-integrated applications blur data and
instructions and can be exploited by injected prompts in retrieved data.
[[105]](https://arxiv.org/abs/2302.12173)  
- Tool libraries themselves can be attack surfaces: ToolHijacker
demonstrates prompt injection attacks that target tool selection by
inserting malicious tool documents into a tool library.
[[106]](https://arxiv.org/abs/2504.19793)  
- Use layered defenses: policy constraints + tool allowlists + output
validation + provenance logging. (Prompt injection is emphasized as a
top risk in OWASP guidance.)
[[107]](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)  
- If deploying broadly, evaluate "agent misuse" separately from "benign
performance." AgentHarm provides a benchmark for harmful multi-step
agent behavior, reflecting that agents can remain highly capable when
jailbroken. [[108]](https://arxiv.org/abs/2410.09024)

### Prioritized short-term research agenda (concrete projects/experiments)

The following projects are scoped to be feasible in months (not years),
and to produce publishable, actionable results.

**Project: Verification-first agentic EDA with measurable trade-offs**  
Build a DS-STAR–style verification loop (plan sufficiency judge +
iterative refinement) and evaluate systematically across DA-Code and
DABStep. Report Pareto curves: accuracy vs cost (LLM calls/tokens) vs
latency, and ablate judge types (LLM vs programmatic validators).
[[109]](https://arxiv.org/abs/2509.21825)

**Project: Provenance-native "analysis graph" standard +
replayability**  
Implement a provenance "analysis graph" capturing dataset versions,
transformations, metrics, plots, and narrative claims, with one-click
replay. Compare user trust and debugging time against baseline
notebook-only traces. Ground evaluation using InsightBench-style planted
insights and BLADE-style approach matching to expert analyses.
[[110]](https://arxiv.org/html/2407.06423v4)

**Project: Skill library vs free-form tool use**  
Replicate AgentAda’s skill-matching approach and compare against
"free-form code generation" agents on insight discovery
(InsightBench/InsightEval) and code-oriented tasks (DA-Code). Measure:
success, novelty, repeated-pattern bias, and robustness to domain shift
(new datasets/skilled methods).
[[111]](https://arxiv.org/abs/2504.07421)

**Project: Secure execution + prompt-injection red team for data
agents**  
Construct a "data-agent prompt injection suite": inject malicious
instructions into (i) documentation, (ii) tool descriptions, (iii)
dataset metadata/field strings, and measure compromise rates (wrong
tool, data exfiltration attempt, policy violations). Evaluate defenses:
strict tool allowlists, context isolation, and sandbox credential
brokering. Base threat models on established prompt-injection work and
tool-selection attacks. [[112]](https://arxiv.org/abs/2302.12173)

**Project: Unified benchmark slice for agentic EDA visualization
correctness**  
Combine VisEval-style labeled visualization tasks with RAGvis’s
EDA-operation taxonomy and pass-rate instrumentation. The goal is to
separate: (a) correct chart *semantics* vs (b) correct code execution vs
(c) visual readability. Use RAGvis’s metrics (Recall@k, Pass Rate@k, VLM
score) as a starting template.
[[113]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)

### Likely near-term trajectory (next 2–3 years)

Several trajectories are strongly suggested by 2025–2026 evidence:

1\) **From "prompt agents" to verification- and provenance-first
agents.**  
Benchmarks show large gaps on multi-step tasks (DABStep, DA-Code),
motivating verification-centric designs (DS-STAR, RAGvis).
[[114]](https://huggingface.co/blog/dabstep?utm_source=chatgpt.com)
Expect verification modules, programmatic validators, and traceability
to become standard, not optional.

2\) **Enterprise analytics agents will converge around semantic
grounding + governed tool surfaces.**  
Looker’s explicit use of semantic models as "source of truth,"
Snowflake’s semantic models for Cortex Analyst, and Databricks’ Unity
Catalog grounding all point toward a convergent design pattern:
constrain the agent’s degrees of freedom using curated semantics and
governance.
[[115]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)

3\) **Tool ecosystems will standardize via protocols like MCP,
increasing both capability and risk.**  
The Model Context Protocol (MCP) was introduced as an open standard for
connecting AI tools to data sources and has rapidly gained ecosystem
support; OpenAI documents MCP support in its tooling guidance, and
LangChain provides MCP integration/adapters.
[[116]](https://www.anthropic.com/news/model-context-protocol) This
will accelerate agentic EDA by making "connectors" composable—but also
expands the attack surface (prompt injection in tools/resources),
increasing the importance of sandboxing and robust security posture.
[[117]](https://arxiv.org/abs/2302.12173)

4\) **Agentic EDA will bifurcate into two "SOTA" tracks:**  
- **Model-centric autonomy** (agentic models trained for orchestration,
e.g., DeepAnalyze-8B) [[118]](https://arxiv.org/abs/2510.16872)  
- **System-centric reliability** (retrieval + semantic modeling +
verification, often with smaller models and stronger constraints, e.g.,
RAGvis showing competitive performance even with smaller open models in
its evaluations)
[[21]](https://aclanthology.org/2025.emnlp-main.836.pdf)

Surveys already note that many systems emphasize
EDA/visualization/modeling while neglecting trust/safety mechanisms;
pushing SOTA will increasingly require measurable safety and governance,
not just accuracy. [[119]](https://arxiv.org/abs/2510.04023)



[[1]](https://arxiv.org/html/2412.14222v2)
[[12]](https://arxiv.org/html/2412.14222v2)
https://arxiv.org/html/2412.14222v2

<https://arxiv.org/html/2412.14222v2>

[[2]](https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com)
[[85]](https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com)
DABstep: Data Agent Benchmark for Multi-step Reasoning

<https://arxiv.org/abs/2506.23719?utm_source=chatgpt.com>

[[3]](https://arxiv.org/abs/2509.21825)
[[13]](https://arxiv.org/abs/2509.21825)
[[18]](https://arxiv.org/abs/2509.21825)
[[42]](https://arxiv.org/abs/2509.21825)
[[75]](https://arxiv.org/abs/2509.21825)
[[98]](https://arxiv.org/abs/2509.21825)
[[99]](https://arxiv.org/abs/2509.21825)
[[109]](https://arxiv.org/abs/2509.21825)
https://arxiv.org/abs/2509.21825

<https://arxiv.org/abs/2509.21825>

[[4]](https://github.com/google/ragvis)
[[38]](https://github.com/google/ragvis)
[[60]](https://github.com/google/ragvis)
[[104]](https://github.com/google/ragvis)
https://github.com/google/ragvis

<https://github.com/google/ragvis>

[[5]](https://arxiv.org/abs/2510.16872)
[[43]](https://arxiv.org/abs/2510.16872)
[[118]](https://arxiv.org/abs/2510.16872)
https://arxiv.org/abs/2510.16872

<https://arxiv.org/abs/2510.16872>

[[6]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
[[17]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
[[56]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
[[69]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
[[115]](https://docs.cloud.google.com/looker/docs/conversational-analytics-overview)
https://docs.cloud.google.com/looker/docs/conversational-analytics-overview

<https://docs.cloud.google.com/looker/docs/conversational-analytics-overview>

[[7]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com)
[[26]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com)
[[54]](https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com)
DA-Code: Agent Data Science Code Generation Benchmark for Large Language
Models

<https://arxiv.org/abs/2410.07331?utm_source=chatgpt.com>

[[8]](https://arxiv.org/abs/2408.09667)
[[78]](https://arxiv.org/abs/2408.09667)
[[93]](https://arxiv.org/abs/2408.09667)
[[102]](https://arxiv.org/abs/2408.09667)
https://arxiv.org/abs/2408.09667

<https://arxiv.org/abs/2408.09667>

[[9]](https://arxiv.org/abs/2506.06541)
[[51]](https://arxiv.org/abs/2506.06541)
[[87]](https://arxiv.org/abs/2506.06541)
https://arxiv.org/abs/2506.06541

<https://arxiv.org/abs/2506.06541>

[[10]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
[[76]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
[[95]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
[[113]](https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/)
https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/

<https://www.microsoft.com/en-us/research/publication/viseval-a-benchmark-for-data-visualization-in-the-era-of-large-language-models/>

[[11]](https://arxiv.org/abs/2511.22884)
[[67]](https://arxiv.org/abs/2511.22884)
[[91]](https://arxiv.org/abs/2511.22884)
[[92]](https://arxiv.org/abs/2511.22884)
https://arxiv.org/abs/2511.22884

<https://arxiv.org/abs/2511.22884>

[[14]](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)
[[49]](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)
[[73]](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)
https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt

<https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt>

[[15]](https://research.google/blog/ds-star-a-state-of-the-art-versatile-data-science-agent/)
https://research.google/blog/ds-star-a-state-of-the-art-versatile-data-science-agent/

<https://research.google/blog/ds-star-a-state-of-the-art-versatile-data-science-agent/>

[[16]](https://arxiv.org/html/2407.06423v4)
[[32]](https://arxiv.org/html/2407.06423v4)
[[33]](https://arxiv.org/html/2407.06423v4)
[[34]](https://arxiv.org/html/2407.06423v4)
[[103]](https://arxiv.org/html/2407.06423v4)
[[110]](https://arxiv.org/html/2407.06423v4)
https://arxiv.org/html/2407.06423v4

<https://arxiv.org/html/2407.06423v4>

[[19]](https://github.com/microsoft/lida?utm_source=chatgpt.com)
[[20]](https://github.com/microsoft/lida?utm_source=chatgpt.com) LIDA:
Automatic Generation of Visualizations and ...

<https://github.com/microsoft/lida?utm_source=chatgpt.com>

[[21]](https://aclanthology.org/2025.emnlp-main.836.pdf)
[[37]](https://aclanthology.org/2025.emnlp-main.836.pdf)
[[48]](https://aclanthology.org/2025.emnlp-main.836.pdf)
[[63]](https://aclanthology.org/2025.emnlp-main.836.pdf)
https://aclanthology.org/2025.emnlp-main.836.pdf

<https://aclanthology.org/2025.emnlp-main.836.pdf>

[[22]](https://www.microsoft.com/en-us/research/project/lida-automatic-generation-of-grammar-agnostic-visualizations/?utm_source=chatgpt.com)
LIDA

<https://www.microsoft.com/en-us/research/project/lida-automatic-generation-of-grammar-agnostic-visualizations/?utm_source=chatgpt.com>

[[23]](https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com)
[[24]](https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com)
[[25]](https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com)
InfiAgent-DABench: Evaluating Agents on Data Analysis Tasks

<https://arxiv.org/abs/2401.05507?utm_source=chatgpt.com>

[[27]](https://arxiv.org/abs/2402.17453)
[[28]](https://arxiv.org/abs/2402.17453)
[[57]](https://arxiv.org/abs/2402.17453)
https://arxiv.org/abs/2402.17453

<https://arxiv.org/abs/2402.17453>

[[29]](https://arxiv.org/abs/2407.17535)
[[30]](https://arxiv.org/abs/2407.17535)
[[31]](https://arxiv.org/abs/2407.17535)
https://arxiv.org/abs/2407.17535

<https://arxiv.org/abs/2407.17535>

[[35]](https://arxiv.org/abs/2504.07421)
[[36]](https://arxiv.org/abs/2504.07421)
[[111]](https://arxiv.org/abs/2504.07421)
https://arxiv.org/abs/2504.07421

<https://arxiv.org/abs/2504.07421>

[[39]](https://arxiv.org/abs/2402.18679)
[[72]](https://arxiv.org/abs/2402.18679)
https://arxiv.org/abs/2402.18679

<https://arxiv.org/abs/2402.18679>

[[40]](https://aclanthology.org/2025.findings-acl.1016/)
https://aclanthology.org/2025.findings-acl.1016/

<https://aclanthology.org/2025.findings-acl.1016/>

[[41]](https://github.com/Kaggle/kaggle-benchmarks)
[[65]](https://github.com/Kaggle/kaggle-benchmarks)
[[77]](https://github.com/Kaggle/kaggle-benchmarks)
[[97]](https://github.com/Kaggle/kaggle-benchmarks)
https://github.com/Kaggle/kaggle-benchmarks

<https://github.com/Kaggle/kaggle-benchmarks>

[[44]](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)
[[68]](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/)
https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/

<https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/>

[[45]](https://arxiv.org/abs/2412.07214)
https://arxiv.org/abs/2412.07214

<https://arxiv.org/abs/2412.07214>

[[46]](https://dblp.org/rec/journals/corr/abs-2508-05002)
[[47]](https://dblp.org/rec/journals/corr/abs-2508-05002)
https://dblp.org/rec/journals/corr/abs-2508-05002

<https://dblp.org/rec/journals/corr/abs-2508-05002>

[[50]](https://developers.openai.com/api/docs/guides/deep-research/)
https://developers.openai.com/api/docs/guides/deep-research/

<https://developers.openai.com/api/docs/guides/deep-research/>

[[52]](https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview)
https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview

<https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview>

[[53]](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi)
https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi

<https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-enable-power-bi>

[[55]](https://docs.cloud.google.com/bigquery/docs/create-data-agents)
https://docs.cloud.google.com/bigquery/docs/create-data-agents

<https://docs.cloud.google.com/bigquery/docs/create-data-agents>

[[58]](https://docs.databricks.com/aws/en/genie/)
https://docs.databricks.com/aws/en/genie/

<https://docs.databricks.com/aws/en/genie/>

[[59]](https://www.databricks.com/blog/introducing-databricks-assistant-data-science-agent)
https://www.databricks.com/blog/introducing-databricks-assistant-data-science-agent

<https://www.databricks.com/blog/introducing-databricks-assistant-data-science-agent>

[[61]](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst

<https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst>

[[62]](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents)
https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents

<https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents>

[[64]](https://aws.amazon.com/blogs/mt/gain-insights-with-natural-language-query-into-your-aws-environment-using-amazon-cloudtrail-and-amazon-q-in-quicksight/)
https://aws.amazon.com/blogs/mt/gain-insights-with-natural-language-query-into-your-aws-environment-using-amazon-cloudtrail-and-amazon-q-in-quicksight/

<https://aws.amazon.com/blogs/mt/gain-insights-with-natural-language-query-into-your-aws-environment-using-amazon-cloudtrail-and-amazon-q-in-quicksight/>

[[66]](https://help.tableau.com/current/online/en-us/web_author_einstein.htm)
https://help.tableau.com/current/online/en-us/web_author_einstein.htm

<https://help.tableau.com/current/online/en-us/web_author_einstein.htm>

[[70]](https://arxiv.org/abs/2510.04023)
[[71]](https://arxiv.org/abs/2510.04023)
[[119]](https://arxiv.org/abs/2510.04023)
https://arxiv.org/abs/2510.04023

<https://arxiv.org/abs/2510.04023>

[[74]](https://github.com/ruc-datalab/DeepAnalyze/blob/main/demo/chat_v2/README.md)
[[100]](https://github.com/ruc-datalab/DeepAnalyze/blob/main/demo/chat_v2/README.md)
https://github.com/ruc-datalab/DeepAnalyze/blob/main/demo/chat_v2/README.md

<https://github.com/ruc-datalab/DeepAnalyze/blob/main/demo/chat_v2/README.md>

[[79]](https://arxiv.org/html/2512.04416v2)
https://arxiv.org/html/2512.04416v2

<https://arxiv.org/html/2512.04416v2>

[[80]](https://arxiv.org/abs/2409.07703)
[[82]](https://arxiv.org/abs/2409.07703)
https://arxiv.org/abs/2409.07703

<https://arxiv.org/abs/2409.07703>

[[81]](https://arxiv.org/html/2409.07703v1)
https://arxiv.org/html/2409.07703v1

<https://arxiv.org/html/2409.07703v1>

[[83]](https://arxiv.org/abs/2502.13897)
[[84]](https://arxiv.org/abs/2502.13897)
https://arxiv.org/abs/2502.13897

<https://arxiv.org/abs/2502.13897>

[[86]](https://huggingface.co/blog/dabstep?utm_source=chatgpt.com)
[[114]](https://huggingface.co/blog/dabstep?utm_source=chatgpt.com)
DABStep: Data Agent Benchmark for Multi-step Reasoning

<https://huggingface.co/blog/dabstep?utm_source=chatgpt.com>

[[88]](https://github.com/mitdbg/KramaBench)
https://github.com/mitdbg/KramaBench

<https://github.com/mitdbg/KramaBench>

[[89]](https://arxiv.org/abs/2509.02473?utm_source=chatgpt.com)
[[90]](https://arxiv.org/abs/2509.02473?utm_source=chatgpt.com)
FDABench: A Benchmark for Data Agents on Analytical Queries over
Heterogeneous Data

<https://arxiv.org/abs/2509.02473?utm_source=chatgpt.com>

[[94]](https://arxiv.org/html/2407.00981v1)
https://arxiv.org/html/2407.00981v1

<https://arxiv.org/html/2407.00981v1>

[[96]](https://arxiv.org/abs/2603.15636?utm_source=chatgpt.com)
[2603.15636] AIDABench: AI Data Analytics Benchmark

<https://arxiv.org/abs/2603.15636?utm_source=chatgpt.com>

[[101]](https://arxiv.org/abs/2504.19793)
[[106]](https://arxiv.org/abs/2504.19793)
https://arxiv.org/abs/2504.19793

<https://arxiv.org/abs/2504.19793>

[[105]](https://arxiv.org/abs/2302.12173)
[[112]](https://arxiv.org/abs/2302.12173)
[[117]](https://arxiv.org/abs/2302.12173)
https://arxiv.org/abs/2302.12173

<https://arxiv.org/abs/2302.12173>

[[107]](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
https://genai.owasp.org/llmrisk/llm01-prompt-injection/

<https://genai.owasp.org/llmrisk/llm01-prompt-injection/>

[[108]](https://arxiv.org/abs/2410.09024)
https://arxiv.org/abs/2410.09024

<https://arxiv.org/abs/2410.09024>

[[116]](https://www.anthropic.com/news/model-context-protocol)
https://www.anthropic.com/news/model-context-protocol

<https://www.anthropic.com/news/model-context-protocol>
