# AI-Assisted Software Engineering: Tools Reference

- Each tool lists: cluster, what it does, website, and whether it is
  free/open-source or paid
- Pricing/availability is as of this writing and may change

## Agent-Readiness Benchmarks

- **SWE-bench**
  - Cluster: Agent evaluation benchmark
  - What it does: suite of real GitHub issues used to score whether an LLM
    agent can generate a correct, merging patch
  - Website: https://www.swebench.com
  - Pricing: free / open source (research benchmark)

- **METR time-horizon evals**
  - Cluster: Agent evaluation benchmark
  - What it does: measures the length of task an AI agent can autonomously
    complete before its success rate drops off
  - Website: https://metr.org
  - Pricing: free (published research, not a licensed product)

## Architecture & Complexity Management

- **dependency-cruiser**
  - Cluster: Static dependency analysis (JS/TS)
  - What it does: validates and visualizes a JS/TS dependency graph, flags
    forbidden imports and cycles
  - Website: https://github.com/sverweij/dependency-cruiser
  - Pricing: free / open source

- **madge**
  - Cluster: Static dependency analysis (JS/TS)
  - What it does: generates a visual module dependency graph and detects
    circular dependencies
  - Website: https://github.com/pahen/madge
  - Pricing: free / open source

- **radon**
  - Cluster: Complexity metrics (Python)
  - What it does: computes cyclomatic complexity, maintainability index, and
    raw code metrics
  - Website: https://radon.readthedocs.io
  - Pricing: free / open source

- **CodeScene**
  - Cluster: Code-health analytics
  - What it does: behavioral code analysis that scores hotspots, complexity
    trends, and knowledge/bus-factor risk
  - Website: https://codescene.com
  - Pricing: paid (free tier for open-source projects)

- **Team Topologies**
  - Cluster: Org-design framework
  - What it does: framework for structuring teams and boundaries around
    Conway's Law; not a software tool
  - Website: https://teamtopologies.com
  - Pricing: free framework (the book itself is paid)

## Observability & Reliability

- **OpenTelemetry**
  - Cluster: Observability
  - What it does: vendor-neutral standard and SDKs for traces, metrics, and
    logs
  - Website: https://opentelemetry.io
  - Pricing: free / open source

- **LaunchDarkly**
  - Cluster: Feature flags
  - What it does: feature-flag platform for progressive rollout and kill
    switches
  - Website: https://launchdarkly.com
  - Pricing: freemium / paid tiers

- **ArchUnit**
  - Cluster: Architecture fitness functions (Java)
  - What it does: turns architectural rules (layering, cycles, naming) into
    executable unit tests
  - Website: https://www.archunit.org
  - Pricing: free / open source

## Reproducible Environments & Data

- **Nix**
  - Cluster: Reproducible package/environment manager
  - What it does: purely functional package manager producing byte-for-byte
    reproducible environments
  - Website: https://nixos.org
  - Pricing: free / open source

- **Docker**
  - Cluster: Containerization
  - What it does: builds and runs OCI containers as reproducible execution
    environments
  - Website: https://www.docker.com
  - Pricing: freemium (Docker Desktop paid for larger companies)

- **DVC (Data Version Control)**
  - Cluster: Data/pipeline versioning
  - What it does: Git-like version control for datasets and ML pipelines
  - Website: https://dvc.org
  - Pricing: free / open source (Iterative Studio SaaS is paid)

- **Backstage**
  - Cluster: Developer portal / service catalog
  - What it does: Spotify's open platform for a software catalog and
    "golden path" project templates
  - Website: https://backstage.io
  - Pricing: free / open source (self-hosted)

- **Rundeck**
  - Cluster: Runbook automation
  - What it does: turns operational procedures into self-service, auditable,
    permissioned jobs
  - Website: https://www.rundeck.com
  - Pricing: freemium (OSS core + paid Enterprise)

- **PagerDuty**
  - Cluster: Incident response / runbook automation
  - What it does: on-call scheduling, alerting, and runbook automation for
    incidents
  - Website: https://www.pagerduty.com
  - Pricing: freemium / paid tiers

## Agent Instruction Manifests & Rules

- **AGENTS.md**
  - Cluster: Agent instruction manifest (open standard)
  - What it does: emerging cross-tool convention for a machine-readable
    "how to work in this repo" file for coding agents
  - Website: https://agents.md
  - Pricing: free / open specification

- **Cursor `.cursorrules`**
  - Cluster: IDE agent-rules convention
  - What it does: per-repo rules file that steers Cursor's AI code
    generation
  - Website: https://cursor.com
  - Pricing: free convention (Cursor IDE has paid tiers)

- **GitHub Copilot custom instructions**
  - Cluster: IDE agent-rules convention
  - What it does: repo-level `.github/copilot-instructions.md` file that
    steers Copilot's suggestions
  - Website: https://docs.github.com/copilot
  - Pricing: paid (requires a Copilot subscription)

- **ruff**
  - Cluster: Linter (Python)
  - What it does: extremely fast Python linter and formatter written in
    Rust
  - Website: https://docs.astral.sh/ruff
  - Pricing: free / open source

- **mypy**
  - Cluster: Type checker (Python)
  - What it does: static type checker that enforces declared type
    annotations
  - Website: https://mypy-lang.org
  - Pricing: free / open source

## Retrieval-Augmented Context for Code

- **Sourcegraph Cody**
  - Cluster: AI coding assistant with codebase context
  - What it does: code-aware AI assistant that retrieves whole-repo context
    for answers and edits
  - Website: https://sourcegraph.com/cody
  - Pricing: freemium / paid tiers

- **Context7**
  - Cluster: MCP server for documentation retrieval
  - What it does: MCP server that serves up-to-date library/API docs into an
    agent's context on demand
  - Website: https://context7.com
  - Pricing: free (open source; hosted service has usage limits)

- **LlamaIndex**
  - Cluster: RAG framework
  - What it does: data framework for building retrieval-augmented LLM
    applications
  - Website: https://www.llamaindex.ai
  - Pricing: free / open source (LlamaCloud SaaS is paid)

- **txtai**
  - Cluster: Embeddings / vector search library
  - What it does: lightweight all-in-one embeddings, vector-search, and RAG
    library
  - Website: https://neuml.github.io/txtai
  - Pricing: free / open source

## Agent Frameworks & Protocols

- **LangChain**
  - Cluster: Agent framework
  - What it does: framework for composing LLM chains, tools, and agents
  - Website: https://www.langchain.com
  - Pricing: free / open source (LangSmith observability is paid)

- **MCP (Model Context Protocol)**
  - Cluster: Agent-tooling protocol
  - What it does: open protocol standardizing how agents connect to tools,
    data sources, and each other
  - Website: https://modelcontextprotocol.io
  - Pricing: free / open specification

- **LangGraph**
  - Cluster: Agent orchestration
  - What it does: graph-based framework for stateful, multi-step agent
    workflows
  - Website: https://www.langchain.com/langgraph
  - Pricing: free / open source (LangGraph Platform is paid)

- **Semantic Kernel**
  - Cluster: Agent framework
  - What it does: Microsoft's SDK for orchestrating LLM plugins and agents
  - Website: https://github.com/microsoft/semantic-kernel
  - Pricing: free / open source

## Repository Contracts & Templating

- **Nx**
  - Cluster: Monorepo build system
  - What it does: extensible build system with `project.json` contracts,
    module-boundary lint rules, and computation caching
  - Website: https://nx.dev
  - Pricing: freemium (Nx Cloud caching/CI is paid)

- **Bazel**
  - Cluster: Build system
  - What it does: Google's fast, reproducible multi-language build and test
    system driven by `BUILD` files
  - Website: https://bazel.build
  - Pricing: free / open source

- **cookiecutter**
  - Cluster: Project templating
  - What it does: generates new projects from parameterized templates
  - Website: https://cookiecutter.readthedocs.io
  - Pricing: free / open source

## Requirements & Planning Practices

- **RFC templates (Google/AWS style)**
  - Cluster: Spec-writing practice
  - What it does: structured proposal document (context, options,
    decision) written and reviewed before implementation starts
  - Website: n/a (internal practice, many public examples online)
  - Pricing: free (practice, not a product)

- **Shape Up**
  - Cluster: Product-planning methodology
  - What it does: Basecamp's methodology for pitching, betting, and
    time-boxing work into fixed cycles
  - Website: https://basecamp.com/shapeup
  - Pricing: free (book available online)

- **Amazon PR/FAQ**
  - Cluster: Spec-writing practice
  - What it does: "working backwards" document format (press release + FAQ)
    written before a feature is built
  - Website: n/a (internal Amazon practice, widely documented)
  - Pricing: free (practice)

- **Jira**
  - Cluster: Issue tracker
  - What it does: Atlassian's issue, backlog, and project tracker
  - Website: https://www.atlassian.com/software/jira
  - Pricing: freemium / paid tiers

- **Linear**
  - Cluster: Issue tracker
  - What it does: fast, opinionated issue tracker for software teams
  - Website: https://linear.app
  - Pricing: freemium / paid tiers

## Architecture Decision Record (ADR) Tooling

- **adr-tools**
  - Cluster: ADR management CLI
  - What it does: command-line scripts to create and manage ADRs as
    numbered Markdown files
  - Website: https://github.com/npryce/adr-tools
  - Pricing: free / open source

- **Log4brains**
  - Cluster: ADR management
  - What it does: static-site generator and CLI for logging, browsing, and
    publishing ADRs
  - Website: https://github.com/thomvaill/log4brains
  - Pricing: free / open source

- **MADR**
  - Cluster: ADR template standard
  - What it does: "Markdown Any Decision Records" template convention
  - Website: https://adr.github.io/madr
  - Pricing: free / open specification

## Monorepo & Multi-repo Tooling

- **Turborepo**
  - Cluster: Monorepo build system (JS/TS)
  - What it does: high-performance incremental build and cache system for
    JS/TS monorepos
  - Website: https://turbo.build/repo
  - Pricing: free / open source (Vercel remote cache is paid)

- **Lerna**
  - Cluster: Monorepo tool (JS)
  - What it does: manages versioning and publishing for multi-package JS
    repositories
  - Website: https://lerna.js.org
  - Pricing: free / open source

- **Sapling**
  - Cluster: Source control (large monorepos)
  - What it does: Meta's Git-compatible source-control system optimized for
    very large monorepos
  - Website: https://sapling-scm.com
  - Pricing: free / open source

- **git submodules / subtrees**
  - Cluster: Multi-repo composition (built into Git)
  - What it does: native Git mechanisms to nest one repository inside
    another
  - Website: https://git-scm.com
  - Pricing: free / open source

## Build Systems & Project Boundaries

- **Pants**
  - Cluster: Build system
  - What it does: fast, scalable, multi-language build system with
    fine-grained dependency caching
  - Website: https://www.pantsbuild.org
  - Pricing: free / open source

## Import & Dependency Analysis

- **import-linter**
  - Cluster: Import-rule enforcement (Python)
  - What it does: enforces layered/allowed-import contracts for Python
    projects, fails CI on violation
  - Website: https://import-linter.readthedocs.io
  - Pricing: free / open source

- **pydeps**
  - Cluster: Dependency graph (Python)
  - What it does: generates a Python module dependency graph, including
    cycle detection
  - Website: https://github.com/thebjorn/pydeps
  - Pricing: free / open source

## Code Duplication Detection

- **jscpd**
  - Cluster: Duplicate-code detection
  - What it does: copy-paste detector across many languages
  - Website: https://github.com/kucherenko/jscpd
  - Pricing: free / open source

- **PMD CPD**
  - Cluster: Duplicate-code detection
  - What it does: copy-paste detector bundled with the PMD static-analysis
    suite
  - Website: https://pmd.github.io
  - Pricing: free / open source

- **SonarQube**
  - Cluster: Code-quality platform
  - What it does: static-analysis platform tracking duplication, bugs,
    vulnerabilities, and code smells over time
  - Website: https://www.sonarsource.com/products/sonarqube
  - Pricing: freemium (Community free, Developer/Enterprise paid)

- **Sourcegraph batch changes**
  - Cluster: Large-scale automated refactor
  - What it does: runs a scripted change across many repositories and
    tracks the resulting PRs to completion
  - Website: https://sourcegraph.com/batch-changes
  - Pricing: paid (Sourcegraph Enterprise)

## Codemods & Automated Refactoring

- **jscodeshift**
  - Cluster: Codemod toolkit (JS/TS)
  - What it does: Meta's toolkit for running codemod scripts over JS/TS
    ASTs at scale
  - Website: https://github.com/facebook/jscodeshift
  - Pricing: free / open source

- **Comby**
  - Cluster: Structural search and replace
  - What it does: language-agnostic structural code search-and-rewrite tool
  - Website: https://comby.dev
  - Pricing: free / open source

- **OpenRewrite**
  - Cluster: Automated mass refactoring (Java + others)
  - What it does: recipe-based, AST-driven refactoring engine for
    large-scale, safe code migrations
  - Website: https://docs.openrewrite.org
  - Pricing: free / open source (Moderne SaaS is paid)

- **rope**
  - Cluster: Refactoring library (Python)
  - What it does: Python library powering IDE-style refactorings (rename,
    extract method/variable)
  - Website: https://github.com/python-rope/rope
  - Pricing: free / open source

- **ts-morph**
  - Cluster: AST manipulation (TypeScript)
  - What it does: wraps the TypeScript Compiler API for programmatic code
    transforms
  - Website: https://ts-morph.com
  - Pricing: free / open source

## Dev Environments

- **VS Code Dev Containers**
  - Cluster: Containerized dev environment spec
  - What it does: open `devcontainer.json` spec plus tooling for a
    reproducible, containerized dev environment
  - Website: https://containers.dev
  - Pricing: free / open source (VS Code itself is free)

- **direnv**
  - Cluster: Environment loader
  - What it does: automatically loads and unloads environment variables per
    directory on `cd`
  - Website: https://direnv.net
  - Pricing: free / open source

- **Gitpod**
  - Cluster: Cloud dev environment
  - What it does: spins up ephemeral, ready-to-code cloud dev environments
    from a repo config
  - Website: https://www.gitpod.io
  - Pricing: freemium / paid tiers

- **GitHub Codespaces**
  - Cluster: Cloud dev environment
  - What it does: GitHub's hosted, containerized VS Code dev environments
  - Website: https://github.com/features/codespaces
  - Pricing: freemium (free minutes, then usage-based)

## Container Wrapper Patterns

- **Homebrew**
  - Cluster: Package manager
  - What it does: macOS/Linux package manager, sometimes used to wrap a
    dockerized executable as a local formula
  - Website: https://brew.sh
  - Pricing: free / open source

- **act**
  - Cluster: Local CI runner
  - What it does: runs GitHub Actions workflows locally inside Docker
  - Website: https://github.com/nektos/act
  - Pricing: free / open source

- **just**
  - Cluster: Command runner
  - What it does: simple `justfile`-based command runner, a modern `make`
    alternative
  - Website: https://github.com/casey/just
  - Pricing: free / open source

- **entr**
  - Cluster: File watcher
  - What it does: reruns an arbitrary command whenever watched files change
  - Website: https://eradman.com/entrproject
  - Pricing: free / open source

## Container Runtimes & Isolation

- **Podman**
  - Cluster: Container engine
  - What it does: daemonless, rootless drop-in alternative to Docker
  - Website: https://podman.io
  - Pricing: free / open source

- **sysbox**
  - Cluster: Container runtime for safer Docker-in-Docker
  - What it does: lets containers run Docker/systemd/Kubernetes safely
    without `--privileged`
  - Website: https://github.com/nestybox/sysbox
  - Pricing: free / open source

- **Kaniko**
  - Cluster: Daemonless image builder
  - What it does: builds container images from a Dockerfile without a
    Docker daemon, safe for CI
  - Website: https://github.com/GoogleContainerTools/kaniko
  - Pricing: free / open source

- **Buildah**
  - Cluster: Daemonless image builder
  - What it does: builds OCI images without a daemon, commonly paired with
    Podman
  - Website: https://buildah.io
  - Pricing: free / open source

## Container Image Optimization & Scanning

- **dive**
  - Cluster: Image-layer inspection
  - What it does: explores a Docker image layer by layer to find wasted
    space
  - Website: https://github.com/wagoodman/dive
  - Pricing: free / open source

- **docker-slim**
  - Cluster: Image shrinking
  - What it does: automatically slims and hardens container images
  - Website: https://github.com/slimtoolkit/slim
  - Pricing: free / open source

- **Trivy**
  - Cluster: Vulnerability scanner
  - What it does: scans images, filesystems, and IaC for vulnerabilities,
    misconfigurations, and secrets
  - Website: https://trivy.dev
  - Pricing: free / open source (Aqua commercial platform is paid)

- **Snyk**
  - Cluster: Security scanning platform
  - What it does: scans code, dependencies, containers, and IaC for
    vulnerabilities
  - Website: https://snyk.io
  - Pricing: freemium / paid tiers

## GitHub / PR Automation

- **gh CLI**
  - Cluster: GitHub command-line tool
  - What it does: official CLI for GitHub PRs, issues, and workflows
  - Website: https://cli.github.com
  - Pricing: free / open source

- **GitHub Actions**
  - Cluster: CI/CD
  - What it does: GitHub-native workflow automation and CI/CD
  - Website: https://github.com/features/actions
  - Pricing: freemium (free minutes, then usage-based)

- **OpenAI Codex Cloud**
  - Cluster: Autonomous cloud coding agent
  - What it does: cloud agent platform that works on coding tasks
    asynchronously and opens PRs
  - Website: https://openai.com/codex
  - Pricing: paid (subscription/usage-based)

- **Devin**
  - Cluster: Autonomous coding agent
  - What it does: Cognition Labs' autonomous AI software engineer
  - Website: https://devin.ai
  - Pricing: paid

- **Cursor background agents**
  - Cluster: Autonomous coding agent
  - What it does: Cursor's asynchronous agents that work on tasks in the
    background and report back
  - Website: https://cursor.com
  - Pricing: paid (Cursor subscription)

## Stacked PRs / Branch Splitting

- **Graphite**
  - Cluster: Stacked-PR workflow and review
  - What it does: stacked-diff workflow tooling plus a PR review platform
  - Website: https://graphite.dev
  - Pricing: freemium / paid tiers

- **git-branchless**
  - Cluster: Git workflow tooling
  - What it does: high-velocity Git tools for undo, stacked commits, and
    fast rebasing
  - Website: https://github.com/arxanas/git-branchless
  - Pricing: free / open source

- **ghstack**
  - Cluster: Stacked-PR tooling
  - What it does: Meta/PyTorch tool for submitting a stack of GitHub PRs
    from a single branch
  - Website: https://github.com/ezyang/ghstack
  - Pricing: free / open source

## Async / Autonomous Agent Platforms

- **Claude Code (GitHub Action / remote control)**
  - Cluster: Async coding agent
  - What it does: Anthropic's coding agent dispatched from CI or driven
    remotely from a phone/desktop session
  - Website: https://code.claude.com
  - Pricing: paid (Claude subscription/API usage)

- **Sweep.dev**
  - Cluster: Autonomous coding agent
  - What it does: AI agent that turns a GitHub issue directly into a PR
  - Website: https://sweep.dev
  - Pricing: freemium / paid tiers

## Agent Permissions & Sandboxing

- **OPA / Rego (Open Policy Agent)**
  - Cluster: Policy engine
  - What it does: general-purpose policy engine and language for expressing
    and evaluating authorization rules
  - Website: https://www.openpolicyagent.org
  - Pricing: free / open source

- **Firecracker**
  - Cluster: MicroVM sandbox
  - What it does: AWS's lightweight virtual-machine monitor for fast,
    strongly isolated sandboxes
  - Website: https://firecracker-microvm.github.io
  - Pricing: free / open source

- **gVisor**
  - Cluster: Container sandbox
  - What it does: Google's user-space kernel that sandboxes container
    syscalls for stronger isolation
  - Website: https://gvisor.dev
  - Pricing: free / open source

## AI / Automated PR Review

- **reviewdog**
  - Cluster: Lint-to-PR-comment bridge
  - What it does: posts linter/static-analysis output as inline PR review
    comments
  - Website: https://github.com/reviewdog/reviewdog
  - Pricing: free / open source

- **Danger / danger.js**
  - Cluster: Policy-as-code PR review
  - What it does: codifies PR review conventions (missing changelog, huge
    diff, missing tests) as code that comments automatically
  - Website: https://danger.systems
  - Pricing: free / open source

- **Codacy**
  - Cluster: Hosted automated code review
  - What it does: hosted static analysis and code-quality review posted on
    every PR
  - Website: https://www.codacy.com
  - Pricing: freemium / paid tiers

- **DeepSource**
  - Cluster: Hosted automated code review
  - What it does: static-analysis platform with autofix suggestions on PRs
  - Website: https://deepsource.com
  - Pricing: freemium / paid tiers

- **Qodo (formerly CodiumAI)**
  - Cluster: AI code review and test generation
  - What it does: AI platform for PR review, code suggestions, and
    AI-generated tests
  - Website: https://www.qodo.ai
  - Pricing: freemium / paid tiers

- **Greptile**
  - Cluster: AI code review
  - What it does: AI reviewer trained on the full codebase's context, not
    just the diff
  - Website: https://www.greptile.com
  - Pricing: paid (free trial)

- **PR-Agent**
  - Cluster: Open-source AI PR review
  - What it does: open-source LLM-based tool for PR review, description,
    and Q&A (Qodo's OSS project)
  - Website: https://github.com/qodo-ai/pr-agent
  - Pricing: free / open source

## Autonomous Coding Loops

- **SWE-agent**
  - Cluster: Research coding agent
  - What it does: agent that resolves real GitHub issues via a dedicated
    agent-computer interface
  - Website: https://github.com/SWE-agent/SWE-agent
  - Pricing: free / open source

- **Aider**
  - Cluster: AI pair-programming CLI
  - What it does: terminal-based AI coding assistant with a plan/edit/test
    loop directly in a Git repo
  - Website: https://aider.chat
  - Pricing: free / open source (LLM API usage cost is separate)

## Root-Cause Analysis & Incident Clustering

- **Sentry**
  - Cluster: Error tracking
  - What it does: application error and performance monitoring with
    automatic issue grouping
  - Website: https://sentry.io
  - Pricing: freemium / paid tiers

- **Datadog**
  - Cluster: Observability platform
  - What it does: metrics, traces, logs, CI/test visibility, and error
    tracking in one platform
  - Website: https://www.datadoghq.com
  - Pricing: paid (free trial)

- **BuildPulse**
  - Cluster: Flaky-test detection
  - What it does: detects, tracks, and quantifies the cost of flaky tests
    across CI runs
  - Website: https://buildpulse.io
  - Pricing: paid (free trial)

## Documentation Tooling

- **Docusaurus**
  - Cluster: Documentation site generator
  - What it does: React-based static-site generator built for
    documentation
  - Website: https://docusaurus.io
  - Pricing: free / open source

- **MkDocs**
  - Cluster: Documentation site generator
  - What it does: fast, simple static-site generator for Markdown project
    docs
  - Website: https://www.mkdocs.org
  - Pricing: free / open source

- **Vale**
  - Cluster: Prose linter
  - What it does: customizable prose/style linter enforced through
    configurable style rules
  - Website: https://vale.sh
  - Pricing: free / open source

- **alex**
  - Cluster: Prose linter
  - What it does: catches insensitive or inconsiderate writing in
    Markdown/prose
  - Website: https://alexjs.com
  - Pricing: free / open source

## README Generation & Link Checking

- **readme-ai**
  - Cluster: AI README generator
  - What it does: generates a README from a repository's code using an LLM
  - Website: https://github.com/eli64s/readme-ai
  - Pricing: free / open source

- **Mintlify**
  - Cluster: Documentation platform
  - What it does: hosted docs platform with an AI writer/assistant for docs
  - Website: https://mintlify.com
  - Pricing: freemium / paid tiers

- **markdown-link-check**
  - Cluster: Link checker
  - What it does: checks Markdown files for dead hyperlinks
  - Website: https://github.com/tcort/markdown-link-check
  - Pricing: free / open source

- **lychee**
  - Cluster: Link checker
  - What it does: fast, async link checker for Markdown, HTML, and text
  - Website: https://lychee.cli.rs
  - Pricing: free / open source

## Git Hooks

- **pre-commit (framework)**
  - Cluster: Git hook manager
  - What it does: multi-language framework for installing and running Git
    pre-commit hooks from a shared config
  - Website: https://pre-commit.com
  - Pricing: free / open source

- **husky**
  - Cluster: Git hook manager (JS/Node)
  - What it does: manages Git hooks for JS/Node projects via `package.json`
  - Website: https://typicode.github.io/husky
  - Pricing: free / open source

- **lefthook**
  - Cluster: Git hook manager
  - What it does: fast, polyglot Git hooks manager
  - Website: https://github.com/evilmartians/lefthook
  - Pricing: free / open source

- **Talisman**
  - Cluster: Secret-scanning Git hook
  - What it does: pre-commit/pre-push hook from ThoughtWorks that detects
    secrets before they are committed
  - Website: https://github.com/thoughtworks/talisman
  - Pricing: free / open source

## Type Checking

- **dmypy (mypy daemon)**
  - Cluster: Type-checker daemon (Python)
  - What it does: keeps mypy warm in a background process for fast
    incremental type checks
  - Website: https://mypy.readthedocs.io
  - Pricing: free / open source

- **pyright**
  - Cluster: Type checker (Python)
  - What it does: Microsoft's fast static type checker for Python, with a
    watch mode
  - Website: https://microsoft.github.io/pyright
  - Pricing: free / open source (Pylance in VS Code)

## Secret Scanning & SAST

- **TruffleHog**
  - Cluster: Secret scanner
  - What it does: scans Git history and live sources for verified secrets
  - Website: https://trufflesecurity.com
  - Pricing: freemium / paid tiers

- **detect-secrets**
  - Cluster: Secret scanner
  - What it does: Yelp's tool for detecting and preventing secrets from
    entering a codebase
  - Website: https://github.com/Yelp/detect-secrets
  - Pricing: free / open source

- **GitHub secret scanning**
  - Cluster: Secret scanner (platform-native)
  - What it does: scans for known secret formats and alerts partners/repo
    owners automatically
  - Website: https://docs.github.com/code-security/secret-scanning
  - Pricing: free (public repos) / paid (private repos, Advanced Security)

- **CodeQL**
  - Cluster: SAST
  - What it does: GitHub's semantic code-analysis engine for finding
    security vulnerabilities via queries
  - Website: https://codeql.github.com
  - Pricing: free (public repos/OSS) / paid (GitHub Advanced Security)

- **Bandit**
  - Cluster: SAST (Python)
  - What it does: static analyzer that finds common security issues in
    Python code
  - Website: https://bandit.readthedocs.io
  - Pricing: free / open source

## Dependency Vulnerability & SBOM

- **Dependabot**
  - Cluster: Automated dependency updates
  - What it does: GitHub-native bot that opens PRs for outdated or
    vulnerable dependencies
  - Website: https://github.com/dependabot
  - Pricing: free (GitHub-native feature)

- **Renovate**
  - Cluster: Automated dependency updates
  - What it does: highly configurable automated dependency-update bot for
    many ecosystems
  - Website: https://docs.renovatebot.com
  - Pricing: free / open source (Mend-hosted version is paid)

- **Grype**
  - Cluster: Vulnerability scanner
  - What it does: scans container images and filesystems for known
    vulnerabilities
  - Website: https://github.com/anchore/grype
  - Pricing: free / open source

- **Syft**
  - Cluster: SBOM generator
  - What it does: generates a software bill of materials for images and
    filesystems
  - Website: https://github.com/anchore/syft
  - Pricing: free / open source

- **OSV-Scanner**
  - Cluster: Vulnerability scanner
  - What it does: Google's scanner that matches project dependencies
    against the OSV vulnerability database
  - Website: https://google.github.io/osv-scanner
  - Pricing: free / open source

## Coverage Reporting

- **Coveralls**
  - Cluster: Coverage reporting
  - What it does: tracks code-coverage trends over time and gates PRs on
    coverage delta
  - Website: https://coveralls.io
  - Pricing: freemium (free for open source, paid for private repos)

## Mutation Testing

- **mutmut**
  - Cluster: Mutation testing (Python)
  - What it does: injects small faults into source code and reruns tests
    to check they would catch the change
  - Website: https://mutmut.readthedocs.io
  - Pricing: free / open source

- **cosmic-ray**
  - Cluster: Mutation testing (Python)
  - What it does: another mutation-testing tool for Python codebases
  - Website: https://cosmic-ray.readthedocs.io
  - Pricing: free / open source

- **Stryker Mutator**
  - Cluster: Mutation testing (JS/TS/.NET)
  - What it does: mutation-testing framework across the JS/TS and .NET
    ecosystems
  - Website: https://stryker-mutator.io
  - Pricing: free / open source

- **Pitest**
  - Cluster: Mutation testing (Java/JVM)
  - What it does: mutation-testing tool for Java and other JVM languages
  - Website: https://pitest.org
  - Pricing: free / open source

## Property-Based & Contract Testing

- **Hypothesis**
  - Cluster: Property-based testing (Python)
  - What it does: generates edge-case test inputs automatically from
    declared properties
  - Website: https://hypothesis.readthedocs.io
  - Pricing: free / open source

- **Pact**
  - Cluster: Contract testing
  - What it does: consumer-driven contract testing between services/APIs
  - Website: https://pact.io
  - Pricing: free / open source (PactFlow SaaS is paid)

## AI Test Generation

- **Diffblue Cover**
  - Cluster: AI unit-test generation (Java)
  - What it does: generates Java unit tests automatically using AI
  - Website: https://www.diffblue.com
  - Pricing: paid (free tier available)

- **EvoSuite**
  - Cluster: Automated test generation (Java)
  - What it does: search-based automatic unit-test generation for Java
  - Website: https://www.evosuite.org
  - Pricing: free / open source

- **GitHub Copilot test generation**
  - Cluster: AI test generation
  - What it does: Copilot feature that suggests or generates unit tests for
    a selection
  - Website: https://docs.github.com/copilot
  - Pricing: paid (Copilot subscription)

## Snapshot / Approval Testing & Reporting

- **syrupy**
  - Cluster: Snapshot testing (pytest)
  - What it does: pytest plugin for snapshot-based testing
  - Website: https://github.com/tophat/syrupy
  - Pricing: free / open source

- **ApprovalTests**
  - Cluster: Approval/golden-master testing
  - What it does: library family implementing approval (golden-master)
    testing across many languages
  - Website: https://approvaltests.com
  - Pricing: free / open source

- **ReportPortal**
  - Cluster: Test reporting
  - What it does: AI-assisted test-automation reporting and analytics
    dashboard, alternative to Allure
  - Website: https://reportportal.io
  - Pricing: free / open source (hosted/enterprise is paid)

- **TestRail**
  - Cluster: Test-case management
  - What it does: test-case management and reporting platform
  - Website: https://www.testrail.com
  - Pricing: paid (free trial)

## Flaky Test Detection

- **Datadog Test Optimization**
  - Cluster: Flaky-test detection
  - What it does: Datadog module for flaky-test detection and CI test
    analytics
  - Website: https://www.datadoghq.com/product/test-optimization
  - Pricing: paid

- **pytest-rerunfailures**
  - Cluster: Flaky-test triage (retry plugin)
  - What it does: pytest plugin that automatically reruns failed tests to
    separate flakes from real regressions
  - Website: https://github.com/pytest-dev/pytest-rerunfailures
  - Pricing: free / open source

## Task Runners

- **Make**
  - Cluster: Task/build runner
  - What it does: classic, ubiquitous build and task-automation tool
  - Website: https://www.gnu.org/software/make
  - Pricing: free / open source

- **Taskfile.dev (Task)**
  - Cluster: Task runner
  - What it does: YAML-based modern task runner, a `make` alternative
  - Website: https://taskfile.dev
  - Pricing: free / open source

## CI/CD Dashboards

- **Datadog CI Visibility**
  - Cluster: CI/CD observability
  - What it does: pipeline and test visibility/analytics inside Datadog
  - Website: https://www.datadoghq.com/product/ci-cd-monitoring
  - Pricing: paid

- **GitHub required status checks**
  - Cluster: Branch protection
  - What it does: native GitHub feature that blocks merging until required
    checks pass
  - Website: https://docs.github.com
  - Pricing: free / paid (depends on org plan)

## Release Automation

- **semantic-release**
  - Cluster: Release automation
  - What it does: fully automated version bumping, changelog, and
    publishing driven by commit messages
  - Website: https://semantic-release.gitbook.io
  - Pricing: free / open source

- **Release Please**
  - Cluster: Release automation
  - What it does: Google's tool that automates releases via PRs based on
    Conventional Commits
  - Website: https://github.com/googleapis/release-please
  - Pricing: free / open source

- **changesets**
  - Cluster: Release automation (JS/TS monorepos)
  - What it does: versioning and changelog workflow for JS/TS monorepos
  - Website: https://github.com/changesets/changesets
  - Pricing: free / open source

## Container Release, Signing & SBOM

- **Skopeo**
  - Cluster: Image copy/inspection
  - What it does: copies and inspects container images across registries
    without a daemon
  - Website: https://github.com/containers/skopeo
  - Pricing: free / open source

- **cosign**
  - Cluster: Image signing
  - What it does: Sigstore's tool for signing and verifying container
    images and artifacts
  - Website: https://docs.sigstore.dev/cosign
  - Pricing: free / open source

## Error Tracking & Incident Routing

- **Rollbar**
  - Cluster: Error tracking
  - What it does: real-time error monitoring, grouping, and alerting
  - Website: https://rollbar.com
  - Pricing: freemium / paid tiers

- **PagerDuty-to-GitHub bridges**
  - Cluster: Incident-to-issue integration
  - What it does: connects incident alerts to automatic GitHub issue
    creation and routing
  - Website: https://www.pagerduty.com/integrations
  - Pricing: depends on plan

## Canary Deployment & Progressive Delivery

- **Flagger**
  - Cluster: Canary deployment (Kubernetes)
  - What it does: progressive-delivery operator automating canary/blue-green
    rollouts and rollback on Kubernetes
  - Website: https://flagger.app
  - Pricing: free / open source

- **Argo Rollouts**
  - Cluster: Progressive delivery (Kubernetes)
  - What it does: Kubernetes controller for canary and blue-green
    deployment strategies
  - Website: https://argoproj.github.io/rollouts
  - Pricing: free / open source

- **Istio**
  - Cluster: Service mesh
  - What it does: service mesh enabling fine-grained traffic splitting used
    to drive canary releases
  - Website: https://istio.io
  - Pricing: free / open source

- **Prometheus**
  - Cluster: Metrics & monitoring
  - What it does: open-source time-series metrics collection, the usual
    basis for canary/SLO comparisons
  - Website: https://prometheus.io
  - Pricing: free / open source

- **Alertmanager**
  - Cluster: Alerting
  - What it does: handles, deduplicates, and routes alerts fired by
    Prometheus
  - Website: https://prometheus.io/docs/alerting/latest/alertmanager
  - Pricing: free / open source

## Supply Chain Security & Governance

- **SLSA (Supply-chain Levels for Software Artifacts)**
  - Cluster: Supply-chain security framework
  - What it does: framework of graduated levels for build provenance and
    artifact integrity
  - Website: https://slsa.dev
  - Pricing: free / open specification
