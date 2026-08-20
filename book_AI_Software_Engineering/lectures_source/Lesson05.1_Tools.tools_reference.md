# AI-Assisted Software Engineering: Tools Reference

- Each tool lists:
  - _Website_
  - _Cluster_
  - _Problem it solves_: nested bullets explaining what are the issues
    that this tool addresses
  - _What it does_: nested bullets explaining the functionalities it does to
    solve the problems above
  - _Languages supported_
  - _Pricing_: whether it is free, freemium, open-source, paid
    - Pricing/availability is as of this writing and may change
  - _GitHub link_: link for the project, if available
  - _GitHub stars_: approximate, as of today

# Summary

// TODO(ai_gp): Add a table with
// name, website, cluster, language, free/fremium/

## Agent-Readiness Benchmarks

- **SWE-bench**
  - _Cluster_: Agent evaluation benchmark
  - _What it does_: suite of real GitHub issues used to score whether an LLM
    agent can generate a correct, merging patch
  - _Website_: https://www.swebench.com
  - _Pricing_: free / open source (research benchmark)

- **METR time-horizon evals**
  - _Cluster_: Agent evaluation benchmark
  - _What it does_: measures the length of task an AI agent can autonomously
    complete before its success rate drops off
  - _Website_: https://metr.org
  - _Pricing_: free (published research, not a licensed product)

## Architecture & Complexity Management

- **dependency-cruiser**
  - _Cluster_: Static dependency analysis (JS/TS)
  - _What it does_: validates and visualizes a JS/TS dependency graph, flags
    forbidden imports and cycles
  - _Website_: https://github.com/sverweij/dependency-cruiser
  - _Pricing_: free / open source

- **madge**
  - _Cluster_: Static dependency analysis (JS/TS)
  - _What it does_: generates a visual module dependency graph and detects
    circular dependencies
  - _Website_: https://github.com/pahen/madge
  - _Pricing_: free / open source

- **radon**
  - _Cluster_: Complexity metrics (Python)
  - _What it does_: computes cyclomatic complexity, maintainability index, and
    raw code metrics
  - _Website_: https://radon.readthedocs.io
  - _Pricing_: free / open source

- **CodeScene**
  - _Cluster_: Code-health analytics
  - _What it does_: behavioral code analysis that scores hotspots, complexity
    trends, and knowledge/bus-factor risk
  - _Website_: https://codescene.com
  - _Pricing_: paid (free tier for open-source projects)

- **Team Topologies**
  - _Cluster_: Org-design framework
  - _What it does_: framework for structuring teams and boundaries around
    Conway's Law; not a software tool
  - _Website_: https://teamtopologies.com
  - _Pricing_: free framework (the book itself is paid)

## Observability & Reliability

- **OpenTelemetry**
  - _Cluster_: Observability
  - _What it does_: vendor-neutral standard and SDKs for traces, metrics, and
    logs
  - _Website_: https://opentelemetry.io
  - _Pricing_: free / open source

- **LaunchDarkly**
  - _Cluster_: Feature flags
  - _What it does_: feature-flag platform for progressive rollout and kill
    switches
  - _Website_: https://launchdarkly.com
  - _Pricing_: freemium / paid tiers

- **ArchUnit**
  - _Cluster_: Architecture fitness functions (Java)
  - _What it does_: turns architectural rules (layering, cycles, naming) into
    executable unit tests
  - _Website_: https://www.archunit.org
  - _Pricing_: free / open source

## Reproducible Environments & Data

- **Nix**
  - _Cluster_: Reproducible package/environment manager
  - _What it does_: purely functional package manager producing byte-for-byte
    reproducible environments
  - _Website_: https://nixos.org
  - _Pricing_: free / open source

- **Docker**
  - _Cluster_: Containerization
  - _What it does_: builds and runs OCI containers as reproducible execution
    environments
  - _Website_: https://www.docker.com
  - _Pricing_: freemium (Docker Desktop paid for larger companies)

- **DVC (Data Version Control)**
  - _Cluster_: Data/pipeline versioning
  - _What it does_: Git-like version control for datasets and ML pipelines
  - _Website_: https://dvc.org
  - _Pricing_: free / open source (Iterative Studio SaaS is paid)

- **Backstage**
  - _Cluster_: Developer portal / service catalog
  - _What it does_: Spotify's open platform for a software catalog and
    "golden path" project templates
  - _Website_: https://backstage.io
  - _Pricing_: free / open source (self-hosted)

- **Rundeck**
  - _Cluster_: Runbook automation
  - _What it does_: turns operational procedures into self-service, auditable,
    permissioned jobs
  - _Website_: https://www.rundeck.com
  - _Pricing_: freemium (OSS core + paid Enterprise)

- **PagerDuty**
  - _Cluster_: Incident response / runbook automation
  - _What it does_: on-call scheduling, alerting, and runbook automation for
    incidents
  - _Website_: https://www.pagerduty.com
  - _Pricing_: freemium / paid tiers

## Agent Instruction Manifests & Rules

- **AGENTS.md**
  - _Cluster_: Agent instruction manifest (open standard)
  - _What it does_: emerging cross-tool convention for a machine-readable
    "how to work in this repo" file for coding agents
  - _Website_: https://agents.md
  - _Pricing_: free / open specification

- **Cursor `.cursorrules`**
  - _Cluster_: IDE agent-rules convention
  - _What it does_: per-repo rules file that steers Cursor's AI code
    generation
  - _Website_: https://cursor.com
  - _Pricing_: free convention (Cursor IDE has paid tiers)

- **GitHub Copilot custom instructions**
  - _Cluster_: IDE agent-rules convention
  - _What it does_: repo-level `.github/copilot-instructions.md` file that
    steers Copilot's suggestions
  - _Website_: https://docs.github.com/copilot
  - _Pricing_: paid (requires a Copilot subscription)

- **ruff**
  - _Cluster_: Linter (Python)
  - _What it does_: extremely fast Python linter and formatter written in
    Rust
  - _Website_: https://docs.astral.sh/ruff
  - _Pricing_: free / open source

- **mypy**
  - _Cluster_: Type checker (Python)
  - _What it does_: static type checker that enforces declared type
    annotations
  - _Website_: https://mypy-lang.org
  - _Pricing_: free / open source

## Retrieval-Augmented Context for Code

- **Sourcegraph Cody**
  - _Cluster_: AI coding assistant with codebase context
  - _What it does_: code-aware AI assistant that retrieves whole-repo context
    for answers and edits
  - _Website_: https://sourcegraph.com/cody
  - _Pricing_: freemium / paid tiers

- **Context7**
  - _Cluster_: MCP server for documentation retrieval
  - _What it does_: MCP server that serves up-to-date library/API docs into an
    agent's context on demand
  - _Website_: https://context7.com
  - _Pricing_: free (open source; hosted service has usage limits)

- **LlamaIndex**
  - _Cluster_: RAG framework
  - _What it does_: data framework for building retrieval-augmented LLM
    applications
  - _Website_: https://www.llamaindex.ai
  - _Pricing_: free / open source (LlamaCloud SaaS is paid)

- **txtai**
  - _Cluster_: Embeddings / vector search library
  - _What it does_: lightweight all-in-one embeddings, vector-search, and RAG
    library
  - _Website_: https://neuml.github.io/txtai
  - _Pricing_: free / open source

## Agent Frameworks & Protocols

- **LangChain**
  - _Cluster_: Agent framework
  - _What it does_: framework for composing LLM chains, tools, and agents
  - _Website_: https://www.langchain.com
  - _Pricing_: free / open source (LangSmith observability is paid)

- **MCP (Model Context Protocol)**
  - _Cluster_: Agent-tooling protocol
  - _What it does_: open protocol standardizing how agents connect to tools,
    data sources, and each other
  - _Website_: https://modelcontextprotocol.io
  - _Pricing_: free / open specification

- **LangGraph**
  - _Cluster_: Agent orchestration
  - _What it does_: graph-based framework for stateful, multi-step agent
    workflows
  - _Website_: https://www.langchain.com/langgraph
  - _Pricing_: free / open source (LangGraph Platform is paid)

- **Semantic Kernel**
  - _Cluster_: Agent framework
  - _What it does_: Microsoft's SDK for orchestrating LLM plugins and agents
  - _Website_: https://github.com/microsoft/semantic-kernel
  - _Pricing_: free / open source

## Repository Contracts & Templating

- **Nx**
  - _Cluster_: Monorepo build system
  - _What it does_: extensible build system with `project.json` contracts,
    module-boundary lint rules, and computation caching
  - _Website_: https://nx.dev
  - _Pricing_: freemium (Nx Cloud caching/CI is paid)

- **Bazel**
  - _Cluster_: Build system
  - _What it does_: Google's fast, reproducible multi-language build and test
    system driven by `BUILD` files
  - _Website_: https://bazel.build
  - _Pricing_: free / open source

- **cookiecutter**
  - _Cluster_: Project templating
  - _What it does_: generates new projects from parameterized templates
  - _Website_: https://cookiecutter.readthedocs.io
  - _Pricing_: free / open source

## Requirements & Planning Practices

- **RFC templates (Google/AWS style)**
  - _Cluster_: Spec-writing practice
  - _What it does_: structured proposal document (context, options,
    decision) written and reviewed before implementation starts
  - _Website_: n/a (internal practice, many public examples online)
  - _Pricing_: free (practice, not a product)

- **Shape Up**
  - _Cluster_: Product-planning methodology
  - _What it does_: Basecamp's methodology for pitching, betting, and
    time-boxing work into fixed cycles
  - _Website_: https://basecamp.com/shapeup
  - _Pricing_: free (book available online)

- **Amazon PR/FAQ**
  - _Cluster_: Spec-writing practice
  - _What it does_: "working backwards" document format (press release + FAQ)
    written before a feature is built
  - _Website_: n/a (internal Amazon practice, widely documented)
  - _Pricing_: free (practice)

- **Jira**
  - _Cluster_: Issue tracker
  - _What it does_: Atlassian's issue, backlog, and project tracker
  - _Website_: https://www.atlassian.com/software/jira
  - _Pricing_: freemium / paid tiers

- **Linear**
  - _Cluster_: Issue tracker
  - _What it does_: fast, opinionated issue tracker for software teams
  - _Website_: https://linear.app
  - _Pricing_: freemium / paid tiers

## Architecture Decision Record (ADR) Tooling

- **adr-tools**
  - _Cluster_: ADR management CLI
  - _What it does_: command-line scripts to create and manage ADRs as
    numbered Markdown files
  - _Website_: https://github.com/npryce/adr-tools
  - _Pricing_: free / open source

- **Log4brains**
  - _Cluster_: ADR management
  - _What it does_: static-site generator and CLI for logging, browsing, and
    publishing ADRs
  - _Website_: https://github.com/thomvaill/log4brains
  - _Pricing_: free / open source

- **MADR**
  - _Cluster_: ADR template standard
  - _What it does_: "Markdown Any Decision Records" template convention
  - _Website_: https://adr.github.io/madr
  - _Pricing_: free / open specification

## Monorepo & Multi-repo Tooling

- **Turborepo**
  - _Cluster_: Monorepo build system (JS/TS)
  - _What it does_: high-performance incremental build and cache system for
    JS/TS monorepos
  - _Website_: https://turbo.build/repo
  - _Pricing_: free / open source (Vercel remote cache is paid)

- **Lerna**
  - _Cluster_: Monorepo tool (JS)
  - _What it does_: manages versioning and publishing for multi-package JS
    repositories
  - _Website_: https://lerna.js.org
  - _Pricing_: free / open source

- **Sapling**
  - _Cluster_: Source control (large monorepos)
  - _What it does_: Meta's Git-compatible source-control system optimized for
    very large monorepos
  - _Website_: https://sapling-scm.com
  - _Pricing_: free / open source

- **git submodules / subtrees**
  - _Cluster_: Multi-repo composition (built into Git)
  - _What it does_: native Git mechanisms to nest one repository inside
    another
  - _Website_: https://git-scm.com
  - _Pricing_: free / open source

## Build Systems & Project Boundaries

- **Pants**
  - _Cluster_: Build system
  - _What it does_: fast, scalable, multi-language build system with
    fine-grained dependency caching
  - _Website_: https://www.pantsbuild.org
  - _Pricing_: free / open source

## Import & Dependency Analysis

- **import-linter**
  - _Cluster_: Import-rule enforcement (Python)
  - _What it does_: enforces layered/allowed-import contracts for Python
    projects, fails CI on violation
  - _Website_: https://import-linter.readthedocs.io
  - _Pricing_: free / open source

- **pydeps**
  - _Cluster_: Dependency graph (Python)
  - _What it does_: generates a Python module dependency graph, including
    cycle detection
  - _Website_: https://github.com/thebjorn/pydeps
  - _Pricing_: free / open source

## Code Duplication Detection

- **jscpd**
  - _Cluster_: Duplicate-code detection
  - _What it does_: copy-paste detector across many languages
  - _Website_: https://github.com/kucherenko/jscpd
  - _Pricing_: free / open source

- **PMD CPD**
  - _Cluster_: Duplicate-code detection
  - _What it does_: copy-paste detector bundled with the PMD static-analysis
    suite
  - _Website_: https://pmd.github.io
  - _Pricing_: free / open source

- **SonarQube**
  - _Cluster_: Code-quality platform
  - _What it does_: static-analysis platform tracking duplication, bugs,
    vulnerabilities, and code smells over time
  - _Website_: https://www.sonarsource.com/products/sonarqube
  - _Pricing_: freemium (Community free, Developer/Enterprise paid)

- **Sourcegraph batch changes**
  - _Cluster_: Large-scale automated refactor
  - _What it does_: runs a scripted change across many repositories and
    tracks the resulting PRs to completion
  - _Website_: https://sourcegraph.com/batch-changes
  - _Pricing_: paid (Sourcegraph Enterprise)

## Codemods & Automated Refactoring

- **jscodeshift**
  - _Cluster_: Codemod toolkit (JS/TS)
  - _What it does_: Meta's toolkit for running codemod scripts over JS/TS
    ASTs at scale
  - _Website_: https://github.com/facebook/jscodeshift
  - _Pricing_: free / open source

- **Comby**
  - _Cluster_: Structural search and replace
  - _What it does_: language-agnostic structural code search-and-rewrite tool
  - _Website_: https://comby.dev
  - _Pricing_: free / open source

- **OpenRewrite**
  - _Cluster_: Automated mass refactoring (Java + others)
  - _What it does_: recipe-based, AST-driven refactoring engine for
    large-scale, safe code migrations
  - _Website_: https://docs.openrewrite.org
  - _Pricing_: free / open source (Moderne SaaS is paid)

- **rope**
  - _Cluster_: Refactoring library (Python)
  - _What it does_: Python library powering IDE-style refactorings (rename,
    extract method/variable)
  - _Website_: https://github.com/python-rope/rope
  - _Pricing_: free / open source

- **ts-morph**
  - _Cluster_: AST manipulation (TypeScript)
  - _What it does_: wraps the TypeScript Compiler API for programmatic code
    transforms
  - _Website_: https://ts-morph.com
  - _Pricing_: free / open source

## Dev Environments

- **VS Code Dev Containers**
  - _Cluster_: Containerized dev environment spec
  - _What it does_: open `devcontainer.json` spec plus tooling for a
    reproducible, containerized dev environment
  - _Website_: https://containers.dev
  - _Pricing_: free / open source (VS Code itself is free)

- **direnv**
  - _Cluster_: Environment loader
  - _What it does_: automatically loads and unloads environment variables per
    directory on `cd`
  - _Website_: https://direnv.net
  - _Pricing_: free / open source

- **Gitpod**
  - _Cluster_: Cloud dev environment
  - _What it does_: spins up ephemeral, ready-to-code cloud dev environments
    from a repo config
  - _Website_: https://www.gitpod.io
  - _Pricing_: freemium / paid tiers

- **GitHub Codespaces**
  - _Cluster_: Cloud dev environment
  - _What it does_: GitHub's hosted, containerized VS Code dev environments
  - _Website_: https://github.com/features/codespaces
  - _Pricing_: freemium (free minutes, then usage-based)

## Container Wrapper Patterns

- **Homebrew**
  - _Cluster_: Package manager
  - _What it does_: macOS/Linux package manager, sometimes used to wrap a
    dockerized executable as a local formula
  - _Website_: https://brew.sh
  - _Pricing_: free / open source

- **act**
  - _Cluster_: Local CI runner
  - _What it does_: runs GitHub Actions workflows locally inside Docker
  - _Website_: https://github.com/nektos/act
  - _Pricing_: free / open source

- **just**
  - _Cluster_: Command runner
  - _What it does_: simple `justfile`-based command runner, a modern `make`
    alternative
  - _Website_: https://github.com/casey/just
  - _Pricing_: free / open source

- **entr**
  - _Cluster_: File watcher
  - _What it does_: reruns an arbitrary command whenever watched files change
  - _Website_: https://eradman.com/entrproject
  - _Pricing_: free / open source

## Container Runtimes & Isolation

- **Podman**
  - _Cluster_: Container engine
  - _What it does_: daemonless, rootless drop-in alternative to Docker
  - _Website_: https://podman.io
  - _Pricing_: free / open source

- **sysbox**
  - _Cluster_: Container runtime for safer Docker-in-Docker
  - _What it does_: lets containers run Docker/systemd/Kubernetes safely
    without `--privileged`
  - _Website_: https://github.com/nestybox/sysbox
  - _Pricing_: free / open source

- **Kaniko**
  - _Cluster_: Daemonless image builder
  - _What it does_: builds container images from a Dockerfile without a
    Docker daemon, safe for CI
  - _Website_: https://github.com/GoogleContainerTools/kaniko
  - _Pricing_: free / open source

- **Buildah**
  - _Cluster_: Daemonless image builder
  - _What it does_: builds OCI images without a daemon, commonly paired with
    Podman
  - _Website_: https://buildah.io
  - _Pricing_: free / open source

## Container Image Optimization & Scanning

- **dive**
  - _Cluster_: Image-layer inspection
  - _What it does_: explores a Docker image layer by layer to find wasted
    space
  - _Website_: https://github.com/wagoodman/dive
  - _Pricing_: free / open source

- **docker-slim**
  - _Cluster_: Image shrinking
  - _What it does_: automatically slims and hardens container images
  - _Website_: https://github.com/slimtoolkit/slim
  - _Pricing_: free / open source

- **Trivy**
  - _Cluster_: Vulnerability scanner
  - _What it does_: scans images, filesystems, and IaC for vulnerabilities,
    misconfigurations, and secrets
  - _Website_: https://trivy.dev
  - _Pricing_: free / open source (Aqua commercial platform is paid)

- **Snyk**
  - _Cluster_: Security scanning platform
  - _What it does_: scans code, dependencies, containers, and IaC for
    vulnerabilities
  - _Website_: https://snyk.io
  - _Pricing_: freemium / paid tiers

## GitHub / PR Automation

- **gh CLI**
  - _Cluster_: GitHub command-line tool
  - _What it does_: official CLI for GitHub PRs, issues, and workflows
  - _Website_: https://cli.github.com
  - _Pricing_: free / open source

- **GitHub Actions**
  - _Cluster_: CI/CD
  - _What it does_: GitHub-native workflow automation and CI/CD
  - _Website_: https://github.com/features/actions
  - _Pricing_: freemium (free minutes, then usage-based)

- **OpenAI Codex Cloud**
  - _Cluster_: Autonomous cloud coding agent
  - _What it does_: cloud agent platform that works on coding tasks
    asynchronously and opens PRs
  - _Website_: https://openai.com/codex
  - _Pricing_: paid (subscription/usage-based)

- **Devin**
  - _Cluster_: Autonomous coding agent
  - _What it does_: Cognition Labs' autonomous AI software engineer
  - _Website_: https://devin.ai
  - _Pricing_: paid

- **Cursor background agents**
  - _Cluster_: Autonomous coding agent
  - _What it does_: Cursor's asynchronous agents that work on tasks in the
    background and report back
  - _Website_: https://cursor.com
  - _Pricing_: paid (Cursor subscription)

## Stacked PRs / Branch Splitting

- **Graphite**
  - _Cluster_: Stacked-PR workflow and review
  - _What it does_: stacked-diff workflow tooling plus a PR review platform
  - _Website_: https://graphite.dev
  - _Pricing_: freemium / paid tiers

- **git-branchless**
  - _Cluster_: Git workflow tooling
  - _What it does_: high-velocity Git tools for undo, stacked commits, and
    fast rebasing
  - _Website_: https://github.com/arxanas/git-branchless
  - _Pricing_: free / open source

- **ghstack**
  - _Cluster_: Stacked-PR tooling
  - _What it does_: Meta/PyTorch tool for submitting a stack of GitHub PRs
    from a single branch
  - _Website_: https://github.com/ezyang/ghstack
  - _Pricing_: free / open source

## Async / Autonomous Agent Platforms

- **Claude Code (GitHub Action / remote control)**
  - _Cluster_: Async coding agent
  - _What it does_: Anthropic's coding agent dispatched from CI or driven
    remotely from a phone/desktop session
  - _Website_: https://code.claude.com
  - _Pricing_: paid (Claude subscription/API usage)

- **Sweep.dev**
  - _Cluster_: Autonomous coding agent
  - _What it does_: AI agent that turns a GitHub issue directly into a PR
  - _Website_: https://sweep.dev
  - _Pricing_: freemium / paid tiers

## Agent Permissions & Sandboxing

- **OPA / Rego (Open Policy Agent)**
  - _Cluster_: Policy engine
  - _What it does_: general-purpose policy engine and language for expressing
    and evaluating authorization rules
  - _Website_: https://www.openpolicyagent.org
  - _Pricing_: free / open source

- **Firecracker**
  - _Cluster_: MicroVM sandbox
  - _What it does_: AWS's lightweight virtual-machine monitor for fast,
    strongly isolated sandboxes
  - _Website_: https://firecracker-microvm.github.io
  - _Pricing_: free / open source

- **gVisor**
  - _Cluster_: Container sandbox
  - _What it does_: Google's user-space kernel that sandboxes container
    syscalls for stronger isolation
  - _Website_: https://gvisor.dev
  - _Pricing_: free / open source

## AI / Automated PR Review

- **reviewdog**
  - _Cluster_: Lint-to-PR-comment bridge
  - _What it does_: posts linter/static-analysis output as inline PR review
    comments
  - _Website_: https://github.com/reviewdog/reviewdog
  - _Pricing_: free / open source

- **Danger / danger.js**
  - _Cluster_: Policy-as-code PR review
  - _What it does_: codifies PR review conventions (missing changelog, huge
    diff, missing tests) as code that comments automatically
  - _Website_: https://danger.systems
  - _Pricing_: free / open source

- **Codacy**
  - _Cluster_: Hosted automated code review
  - _What it does_: hosted static analysis and code-quality review posted on
    every PR
  - _Website_: https://www.codacy.com
  - _Pricing_: freemium / paid tiers

- **DeepSource**
  - _Cluster_: Hosted automated code review
  - _What it does_: static-analysis platform with autofix suggestions on PRs
  - _Website_: https://deepsource.com
  - _Pricing_: freemium / paid tiers

- **Qodo (formerly CodiumAI)**
  - _Cluster_: AI code review and test generation
  - _What it does_: AI platform for PR review, code suggestions, and
    AI-generated tests
  - _Website_: https://www.qodo.ai
  - _Pricing_: freemium / paid tiers

- **Greptile**
  - _Cluster_: AI code review
  - _What it does_: AI reviewer trained on the full codebase's context, not
    just the diff
  - _Website_: https://www.greptile.com
  - _Pricing_: paid (free trial)

- **PR-Agent**
  - _Cluster_: Open-source AI PR review
  - _What it does_: open-source LLM-based tool for PR review, description,
    and Q&A (Qodo's OSS project)
  - _Website_: https://github.com/qodo-ai/pr-agent
  - _Pricing_: free / open source

## Autonomous Coding Loops

- **SWE-agent**
  - _Cluster_: Research coding agent
  - _What it does_: agent that resolves real GitHub issues via a dedicated
    agent-computer interface
  - _Website_: https://github.com/SWE-agent/SWE-agent
  - _Pricing_: free / open source

- **Aider**
  - _Cluster_: AI pair-programming CLI
  - _What it does_: terminal-based AI coding assistant with a plan/edit/test
    loop directly in a Git repo
  - _Website_: https://aider.chat
  - _Pricing_: free / open source (LLM API usage cost is separate)

## Root-Cause Analysis & Incident Clustering

- **Sentry**
  - _Cluster_: Error tracking
  - _What it does_: application error and performance monitoring with
    automatic issue grouping
  - _Website_: https://sentry.io
  - _Pricing_: freemium / paid tiers

- **Datadog**
  - _Cluster_: Observability platform
  - _What it does_: metrics, traces, logs, CI/test visibility, and error
    tracking in one platform
  - _Website_: https://www.datadoghq.com
  - _Pricing_: paid (free trial)

- **BuildPulse**
  - _Cluster_: Flaky-test detection
  - _What it does_: detects, tracks, and quantifies the cost of flaky tests
    across CI runs
  - _Website_: https://buildpulse.io
  - _Pricing_: paid (free trial)

## Documentation Tooling

- **Docusaurus**
  - _Cluster_: Documentation site generator
  - _What it does_: React-based static-site generator built for
    documentation
  - _Website_: https://docusaurus.io
  - _Pricing_: free / open source

- **MkDocs**
  - _Cluster_: Documentation site generator
  - _What it does_: fast, simple static-site generator for Markdown project
    docs
  - _Website_: https://www.mkdocs.org
  - _Pricing_: free / open source

- **Vale**
  - _Cluster_: Prose linter
  - _What it does_: customizable prose/style linter enforced through
    configurable style rules
  - _Website_: https://vale.sh
  - _Pricing_: free / open source

- **alex**
  - _Cluster_: Prose linter
  - _What it does_: catches insensitive or inconsiderate writing in
    Markdown/prose
  - _Website_: https://alexjs.com
  - _Pricing_: free / open source

## README Generation & Link Checking

- **readme-ai**
  - _Cluster_: AI README generator
  - _What it does_: generates a README from a repository's code using an LLM
  - _Website_: https://github.com/eli64s/readme-ai
  - _Pricing_: free / open source

- **Mintlify**
  - _Cluster_: Documentation platform
  - _What it does_: hosted docs platform with an AI writer/assistant for docs
  - _Website_: https://mintlify.com
  - _Pricing_: freemium / paid tiers

- **markdown-link-check**
  - _Cluster_: Link checker
  - _What it does_: checks Markdown files for dead hyperlinks
  - _Website_: https://github.com/tcort/markdown-link-check
  - _Pricing_: free / open source

- **lychee**
  - _Cluster_: Link checker
  - _What it does_: fast, async link checker for Markdown, HTML, and text
  - _Website_: https://lychee.cli.rs
  - _Pricing_: free / open source

## Git Hooks

- **pre-commit (framework)**
  - _Cluster_: Git hook manager
  - _What it does_: multi-language framework for installing and running Git
    pre-commit hooks from a shared config
  - _Website_: https://pre-commit.com
  - _Pricing_: free / open source

- **husky**
  - _Cluster_: Git hook manager (JS/Node)
  - _What it does_: manages Git hooks for JS/Node projects via `package.json`
  - _Website_: https://typicode.github.io/husky
  - _Pricing_: free / open source

- **lefthook**
  - _Cluster_: Git hook manager
  - _What it does_: fast, polyglot Git hooks manager
  - _Website_: https://github.com/evilmartians/lefthook
  - _Pricing_: free / open source

- **Talisman**
  - _Cluster_: Secret-scanning Git hook
  - _What it does_: pre-commit/pre-push hook from ThoughtWorks that detects
    secrets before they are committed
  - _Website_: https://github.com/thoughtworks/talisman
  - _Pricing_: free / open source

## Type Checking

- **dmypy (mypy daemon)**
  - _Cluster_: Type-checker daemon (Python)
  - _What it does_: keeps mypy warm in a background process for fast
    incremental type checks
  - _Website_: https://mypy.readthedocs.io
  - _Pricing_: free / open source

- **pyright**
  - _Cluster_: Type checker (Python)
  - _What it does_: Microsoft's fast static type checker for Python, with a
    watch mode
  - _Website_: https://microsoft.github.io/pyright
  - _Pricing_: free / open source (Pylance in VS Code)

## Secret Scanning & SAST

- **TruffleHog**
  - _Cluster_: Secret scanner
  - _What it does_: scans Git history and live sources for verified secrets
  - _Website_: https://trufflesecurity.com
  - _Pricing_: freemium / paid tiers

- **detect-secrets**
  - _Cluster_: Secret scanner
  - _What it does_: Yelp's tool for detecting and preventing secrets from
    entering a codebase
  - _Website_: https://github.com/Yelp/detect-secrets
  - _Pricing_: free / open source

- **GitHub secret scanning**
  - _Cluster_: Secret scanner (platform-native)
  - _What it does_: scans for known secret formats and alerts partners/repo
    owners automatically
  - _Website_: https://docs.github.com/code-security/secret-scanning
  - _Pricing_: free (public repos) / paid (private repos, Advanced Security)

- **CodeQL**
  - _Cluster_: SAST
  - _What it does_: GitHub's semantic code-analysis engine for finding
    security vulnerabilities via queries
  - _Website_: https://codeql.github.com
  - _Pricing_: free (public repos/OSS) / paid (GitHub Advanced Security)

- **Bandit**
  - _Cluster_: SAST (Python)
  - _What it does_: static analyzer that finds common security issues in
    Python code
  - _Website_: https://bandit.readthedocs.io
  - _Pricing_: free / open source

## Dependency Vulnerability & SBOM

- **Dependabot**
  - _Cluster_: Automated dependency updates
  - _What it does_: GitHub-native bot that opens PRs for outdated or
    vulnerable dependencies
  - _Website_: https://github.com/dependabot
  - _Pricing_: free (GitHub-native feature)

- **Renovate**
  - _Cluster_: Automated dependency updates
  - _What it does_: highly configurable automated dependency-update bot for
    many ecosystems
  - _Website_: https://docs.renovatebot.com
  - _Pricing_: free / open source (Mend-hosted version is paid)

- **Grype**
  - _Cluster_: Vulnerability scanner
  - _What it does_: scans container images and filesystems for known
    vulnerabilities
  - _Website_: https://github.com/anchore/grype
  - _Pricing_: free / open source

- **Syft**
  - _Cluster_: SBOM generator
  - _What it does_: generates a software bill of materials for images and
    filesystems
  - _Website_: https://github.com/anchore/syft
  - _Pricing_: free / open source

- **OSV-Scanner**
  - _Cluster_: Vulnerability scanner
  - _What it does_: Google's scanner that matches project dependencies
    against the OSV vulnerability database
  - _Website_: https://google.github.io/osv-scanner
  - _Pricing_: free / open source

## Coverage Reporting

- **Coveralls**
  - _Cluster_: Coverage reporting
  - _What it does_: tracks code-coverage trends over time and gates PRs on
    coverage delta
  - _Website_: https://coveralls.io
  - _Pricing_: freemium (free for open source, paid for private repos)

## Mutation Testing

- **mutmut**
  - _Cluster_: Mutation testing (Python)
  - _What it does_: injects small faults into source code and reruns tests
    to check they would catch the change
  - _Website_: https://mutmut.readthedocs.io
  - _Pricing_: free / open source

- **cosmic-ray**
  - _Cluster_: Mutation testing (Python)
  - _What it does_: another mutation-testing tool for Python codebases
  - _Website_: https://cosmic-ray.readthedocs.io
  - _Pricing_: free / open source

- **Stryker Mutator**
  - _Cluster_: Mutation testing (JS/TS/.NET)
  - _What it does_: mutation-testing framework across the JS/TS and .NET
    ecosystems
  - _Website_: https://stryker-mutator.io
  - _Pricing_: free / open source

- **Pitest**
  - _Cluster_: Mutation testing (Java/JVM)
  - _What it does_: mutation-testing tool for Java and other JVM languages
  - _Website_: https://pitest.org
  - _Pricing_: free / open source

## Property-Based & Contract Testing

- **Hypothesis**
  - _Cluster_: Property-based testing (Python)
  - _What it does_: generates edge-case test inputs automatically from
    declared properties
  - _Website_: https://hypothesis.readthedocs.io
  - _Pricing_: free / open source

- **Pact**
  - _Cluster_: Contract testing
  - _What it does_: consumer-driven contract testing between services/APIs
  - _Website_: https://pact.io
  - _Pricing_: free / open source (PactFlow SaaS is paid)

## AI Test Generation

- **Diffblue Cover**
  - _Cluster_: AI unit-test generation (Java)
  - _What it does_: generates Java unit tests automatically using AI
  - _Website_: https://www.diffblue.com
  - _Pricing_: paid (free tier available)

- **EvoSuite**
  - _Cluster_: Automated test generation (Java)
  - _What it does_: search-based automatic unit-test generation for Java
  - _Website_: https://www.evosuite.org
  - _Pricing_: free / open source

- **GitHub Copilot test generation**
  - _Cluster_: AI test generation
  - _What it does_: Copilot feature that suggests or generates unit tests for
    a selection
  - _Website_: https://docs.github.com/copilot
  - _Pricing_: paid (Copilot subscription)

## Snapshot / Approval Testing & Reporting

- **syrupy**
  - _Cluster_: Snapshot testing (pytest)
  - _What it does_: pytest plugin for snapshot-based testing
  - _Website_: https://github.com/tophat/syrupy
  - _Pricing_: free / open source

- **ApprovalTests**
  - _Cluster_: Approval/golden-master testing
  - _What it does_: library family implementing approval (golden-master)
    testing across many languages
  - _Website_: https://approvaltests.com
  - _Pricing_: free / open source

- **ReportPortal**
  - _Cluster_: Test reporting
  - _What it does_: AI-assisted test-automation reporting and analytics
    dashboard, alternative to Allure
  - _Website_: https://reportportal.io
  - _Pricing_: free / open source (hosted/enterprise is paid)

- **TestRail**
  - _Cluster_: Test-case management
  - _What it does_: test-case management and reporting platform
  - _Website_: https://www.testrail.com
  - _Pricing_: paid (free trial)

## Flaky Test Detection

- **Datadog Test Optimization**
  - _Cluster_: Flaky-test detection
  - _What it does_: Datadog module for flaky-test detection and CI test
    analytics
  - _Website_: https://www.datadoghq.com/product/test-optimization
  - _Pricing_: paid

- **pytest-rerunfailures**
  - _Cluster_: Flaky-test triage (retry plugin)
  - _What it does_: pytest plugin that automatically reruns failed tests to
    separate flakes from real regressions
  - _Website_: https://github.com/pytest-dev/pytest-rerunfailures
  - _Pricing_: free / open source

## Task Runners

- **Make**
  - _Cluster_: Task/build runner
  - _What it does_: classic, ubiquitous build and task-automation tool
  - _Website_: https://www.gnu.org/software/make
  - _Pricing_: free / open source

- **Taskfile.dev (Task)**
  - _Cluster_: Task runner
  - _What it does_: YAML-based modern task runner, a `make` alternative
  - _Website_: https://taskfile.dev
  - _Pricing_: free / open source

## CI/CD Dashboards

- **Datadog CI Visibility**
  - _Cluster_: CI/CD observability
  - _What it does_: pipeline and test visibility/analytics inside Datadog
  - _Website_: https://www.datadoghq.com/product/ci-cd-monitoring
  - _Pricing_: paid

- **GitHub required status checks**
  - _Cluster_: Branch protection
  - _What it does_: native GitHub feature that blocks merging until required
    checks pass
  - _Website_: https://docs.github.com
  - _Pricing_: free / paid (depends on org plan)

## Release Automation

- **semantic-release**
  - _Cluster_: Release automation
  - _What it does_: fully automated version bumping, changelog, and
    publishing driven by commit messages
  - _Website_: https://semantic-release.gitbook.io
  - _Pricing_: free / open source

- **Release Please**
  - _Cluster_: Release automation
  - _What it does_: Google's tool that automates releases via PRs based on
    Conventional Commits
  - _Website_: https://github.com/googleapis/release-please
  - _Pricing_: free / open source

- **changesets**
  - _Cluster_: Release automation (JS/TS monorepos)
  - _What it does_: versioning and changelog workflow for JS/TS monorepos
  - _Website_: https://github.com/changesets/changesets
  - _Pricing_: free / open source

## Container Release, Signing & SBOM

- **Skopeo**
  - _Cluster_: Image copy/inspection
  - _What it does_: copies and inspects container images across registries
    without a daemon
  - _Website_: https://github.com/containers/skopeo
  - _Pricing_: free / open source

- **cosign**
  - _Cluster_: Image signing
  - _What it does_: Sigstore's tool for signing and verifying container
    images and artifacts
  - _Website_: https://docs.sigstore.dev/cosign
  - _Pricing_: free / open source

## Error Tracking & Incident Routing

- **Rollbar**
  - _Cluster_: Error tracking
  - _What it does_: real-time error monitoring, grouping, and alerting
  - _Website_: https://rollbar.com
  - _Pricing_: freemium / paid tiers

- **PagerDuty-to-GitHub bridges**
  - _Cluster_: Incident-to-issue integration
  - _What it does_: connects incident alerts to automatic GitHub issue
    creation and routing
  - _Website_: https://www.pagerduty.com/integrations
  - _Pricing_: depends on plan

## Canary Deployment & Progressive Delivery

- **Flagger**
  - _Cluster_: Canary deployment (Kubernetes)
  - _What it does_: progressive-delivery operator automating canary/blue-green
    rollouts and rollback on Kubernetes
  - _Website_: https://flagger.app
  - _Pricing_: free / open source

- **Argo Rollouts**
  - _Cluster_: Progressive delivery (Kubernetes)
  - _What it does_: Kubernetes controller for canary and blue-green
    deployment strategies
  - _Website_: https://argoproj.github.io/rollouts
  - _Pricing_: free / open source

- **Istio**
  - _Cluster_: Service mesh
  - _What it does_: service mesh enabling fine-grained traffic splitting used
    to drive canary releases
  - _Website_: https://istio.io
  - _Pricing_: free / open source

- **Prometheus**
  - _Cluster_: Metrics & monitoring
  - _What it does_: open-source time-series metrics collection, the usual
    basis for canary/SLO comparisons
  - _Website_: https://prometheus.io
  - _Pricing_: free / open source

- **Alertmanager**
  - _Cluster_: Alerting
  - _What it does_: handles, deduplicates, and routes alerts fired by
    Prometheus
  - _Website_: https://prometheus.io/docs/alerting/latest/alertmanager
  - _Pricing_: free / open source

## Supply Chain Security & Governance

- **SLSA (Supply-chain Levels for Software Artifacts)**
  - _Cluster_: Supply-chain security framework
  - _What it does_: framework of graduated levels for build provenance and
    artifact integrity
  - _Website_: https://slsa.dev
  - _Pricing_: free / open specification
