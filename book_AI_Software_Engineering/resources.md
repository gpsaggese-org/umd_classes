- Managing Code
  - Coding while you sleep
    https://code.claude.com/docs/en/remote-control
    https://code.claude.com/docs/en/web-quickstart
    https://code.claude.com/docs/en/desktop-quickstart
    https://code.claude.com/docs/en/security-guidance
    /install-github-app

- Automating PR creation

- Automating PR review

- Automating Documentation

- Rules and AI skills

# /Users/saggese/src/umd_classes1/helpers_root/papers/AIgentic_Development_System

## Code Quality & Standards

- Linter Framework
  - Architecture & modifying vs non-modifying actions
  - Comprehensive linting rules
  - Integration & extensibility

- Import Cycle Detection
  - Dependency analysis tools
  - Integration into dev workflow

- Package Structure & Import Conventions
  - Goals & rules for imports
  - Package hierarchy & cycle prevention
  - Anatomy of a package
  - Enforcement mechanisms

- Pre-Commit Hook System
  - Enforced checks (branch, author, secrets, file size)
  - Commit message enhancement
  - Installation & configuration

- Code Coverage Tracking & Enforcement
  - Structured coverage by test category
  - CI integration & workflow behavior
  - Enforced thresholds & quality gates
  - Visibility & developer experience

## Unit Testing

- Testing Philosophy & Motivation
  - Tests as executable specifications
  - First-class concern in development

- hunitest.TestCase Framework
  - Enhanced assertions
  - Golden file testing (check_string)
  - Directory management
  - Text processing utilities
  - Notebook execution support

- Basic Test Structure
  - Three-section pattern
  - Setup, execution, verification

- Golden File Testing
  - How check_string works
  - When to use check_string vs assert_equal
  - Fuzzy matching & text processing

- Test Organization & Conventions
  - File & directory structure
  - Naming conventions
  - Helper methods & DRY principle

- Test Categorization & Execution
  - Fast, slow, superslow test categories
  - Running tests with invoke
  - Timeout & retry behavior

- Mocking Philosophy
  - Mock only external dependencies
  - Do not mock internal code
  - Shared mock setup patterns

- Test Coverage Measurement & Enforcement
  - Running coverage analysis
  - CI/CD integration
  - Interpreting coverage metrics

- Testing Jupyter Notebooks
  - Notebook execution framework
  - Test organization
  - Debugging failing notebook tests

## Coding Architecture

- Runnable Directories Architecture
  - Problem: monorepo vs multi-repo tradeoffs
  - Solution: hybrid runnable directory approach
  - Design goals & functionalities
  - Independent yet cohesive modules

- Development System Components
  - Docker containerization
  - Thin environment
  - Helpers submodule
  - Git hooks enforcement
  - Recursive test execution

- Containerized Development Workflows
  - Development containers & images
  - Local, dev, prod stages
  - Docker-in-Docker vs sibling containers
  - Multi-container applications

- Thin Environment
  - Minimal dependency setup
  - Shared across runnable directories
  - Bootstrap & development consistency

- Helpers Submodule
  - Centralized toolchain & utilities
  - Common files via symlinks
  - Git hooks management
  - Test infrastructure

# Automation & Workflows

- Invoke Workflows
  - Centralized task registry
  - Python invoke for common operations
  - Development command automation

- Code Repo Automation
  - Standardized label infrastructure
  - Template-based project synchronization
  - Declarative repository settings
  - GitHub metadata management

- CI/CD Automation & Buildmeister Role
  - Build health monitoring
  - Buildmeister dashboard & responsibilities
  - Build break triage & escalation
  - Allure test reporting
  - Post-mortem logging

- Docker Container Release Flow
  - Development & production image workflows
  - Version management via changelog.txt
  - Task definition management with ECS
  - Preproduction & production releases
  - Airflow DAG release process
  - Feature release communication
  - Quality gates & automated testing
  - Rollback capabilities

## Dockerized Executables

- Architecture & Design
  - Container image structure
  - Wrapper script responsibilities
  - Repository root as anchor point

- Execution Flow
  - Image availability & discovery
  - Path translation & mounting
  - Exit code propagation

- Container Execution Patterns
  - Children containers (Docker-in-Docker)
  - Sibling containers (preferred)
  - Security & efficiency tradeoffs

- Practical Examples
  - Document formatting & conversion
  - Diagram rendering
  - LaTeX compilation
  - LLM-powered transforms

- Benefits & Trade-offs
  - Reproducibility & consistency
  - Rapid onboarding
  - Independent versioning
  - Docker dependency overhead
  - Image storage & startup latency

- Implementation Guidelines
  - Creating minimal images
  - Building wrapper scripts
  - Choosing execution patterns
  - Testing thoroughly
  - Documentation

- Integration with Development Workflows
  - Local development invocation
  - Pre-commit hook integration
  - CI/CD pipeline usage
  - Automated task orchestration

## AI-Optimized Development Infrastructure

- Self-Documenting Executable Workflows
  - Invoke task discoverability
  - Elimination of ambiguity
  - Cross-repository consistency
  - Encoded best practices

- Agent Instruction Manifests
  - CLAUDE.md as machine-consumable manual
  - Architecture & boundaries
  - Canonical commands
  - Reducing agent onboarding overhead

- Machine-Readable Repository Contracts
  - repo_config.yaml file
  - Repository identity encoding
  - Image naming & registries
  - Direct agent queries

- Context-Bounded Editing
  - Runnable directories as prompt boundaries
  - Self-contained directory structure
  - Reducing context hallucinations
  - Explicit dependency management

- Guardrails & Provenance
  - Formatting automation (pre-commit hooks)
  - Containerized execution consistency
  - Secret hygiene gates
  - Version synchronization
  - Evidence-carrying changes

- The Agentic Loop
  - Plan: summarize change & scope
  - Patch: minimal diff respecting boundaries
  - Prove: layered validation gates
  - Summarize: PR-ready explanation

- Standardized Conventions
  - Predictable file organization
  - Systematic naming patterns
  - Uniform test structure
  - Clear architectural boundaries
  - Reduced decision space for AI

- Container-Based Reproducibility
  - Environment isolation
  - Version synchronization
  - Consistent tool behavior
  - Minimal host dependencies
  - Elimination of "works on my machine"

- Golden File Testing for AI
  - Concrete, interpretable feedback
  - Safe iteration cycles
  - Comprehensive regression detection
  - Elimination of false positives

- Layered Quality Gates
  - Automated corrections (modifying linters)
  - Immediate failure detection
  - Graduated feedback cycles
  - Specific, actionable diagnostics

- Emergent AI-Optimization
  - Degrees of freedom reduction
  - Focus on higher-level concerns
  - Division of labor: humans & AI
  - Positive feedback loop with infrastructure

# Chapter 14: Human-AI Collaboration Patterns

### Local Material
- `book.Agentic_AI/lectures_source/Lesson01.01-What_Is_An_Agentic_AI.txt`
  - Autonomy Levels: Worked Examples; Human-in-the-Loop vs. Full Autonomy
    (Spectrum of Autonomy) — background for Task-Risk Matching and
    Designing Handoffs

### Books
- 2022, National Academies of Sciences, Engineering, and Medicine,
  "Human-AI Teaming: State-of-the-Art and Research Needs"
  (https://www.nap.edu/catalog/26355/human-ai-teaming-state-of-the-art-and-research-needs)
  — free full text; task allocation, trust, and team design across
  human-AI teams
- 2018, Daugherty et al., "Human + Machine: Reimagining Work in the Age
  of AI" (https://books.google.com/books?id=wpY4DwAAQBAJ) — hybrid
  human+AI roles and handoff design in organizational workflows

### Papers
- 2026, Kang, "Governed AI-Assisted Engineering: Graduated Human Oversight for
  Agentic Code Generation in Regulated Domains"
  (https://arxiv.org/abs/2606.22484) — three-tier oversight model
  (human-in-the-loop / human-over-the-loop / automated-with-monitoring) keyed to
  regulatory impact and reversibility
- 2026, Shukla et al., "Hedwig: Dynamic Autonomy for Coding Agents Under Local
  Oversight" (https://arxiv.org/abs/2605.11495) — adaptive autonomy level per
  task for coding agents
- 2026, Heilman et al., "GitHub Copilot and Developer Productivity: An
  Observational Dose-Response Analysis" (https://arxiv.org/abs/2606.00438) —
  large-scale observational evidence on AI-assisted team workflows
- 2026, Raees et al., "From Trust to Appropriate Reliance: Measurement Constructs
  in Human-AI Decision-Making" (https://arxiv.org/abs/2604.23896) — distinguishes
  trust, reliance, and appropriate reliance for calibrating escalation decisions
- 2025, Li et al., "The Rise of AI Teammates in Software Engineering (SE 3.0):
  How Autonomous Coding Agents Are Reshaping Software Engineering"
  (https://arxiv.org/abs/2507.15003) — pair vs. autonomous collaboration modes
  for coding agents
- 2025, Mayer et al., "Human-AI Collaboration: Trade-offs Between Performance and
  Preferences" (https://arxiv.org/abs/2503.00248) — agent consideration of human
  actions vs. team performance
- 2025, He et al., "Fine-Grained Appropriate Reliance: Human-AI Collaboration
  with a Multi-Step Transparent Decision Workflow for Complex Task Decomposition"
  (https://arxiv.org/abs/2501.10909) — review-loop-style decomposition of
  multi-step tasks for reliance
- 2024, Vats et al., "A Survey on Human-AI Collaboration with Large Foundation
  Models" (https://arxiv.org/abs/2403.04931) — collaborative design principles
  and governance frameworks
- 2023, Mehrotra et al., "A Systematic Review on Fostering Appropriate Trust in
  Human-AI Interaction" (https://arxiv.org/abs/2311.06305) — practices and
  measures for calibrating trust, tied to task type
- 2023, Peng et al., "The Impact of AI on Developer Productivity: Evidence from
  GitHub Copilot" (https://arxiv.org/abs/2302.06590) — controlled experiment
  quantifying pair-programming speedup
- 1999, Horvitz, "Principles of Mixed-Initiative User Interfaces"
  (https://doi.org/10.1145/302979.303030) — foundational principles for when to
  hand off initiative between human and system
