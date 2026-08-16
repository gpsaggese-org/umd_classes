# Summary

## Title
- Software Engineering with AI: Practical Workflows for AI-Assisted Development
- Building Software with AI: From Code Generation to Autonomous Agents

## Target Audience
- Advanced undergraduate/graduate CS students and working software engineers
  who already know git, testing, and CI/CD basics
- Assumes working familiarity with LLMs (prompting, context windows) but no
  prior AI/ML coursework

## Approach of the Book
- Focus on:
  - Practical workflows over deep ML theory
  - Concrete tool walkthroughs (Claude Code, Copilot, Cursor, CI integrations)
  - Worked examples: real prompts, real diffs, real PR/CI workflows
  - Making AI-assisted development operational in a real codebase
- Provide resources to go one level deep
  - Related classes (`msml610`, `data605`)
  - References to benchmarks (SWE-bench), papers, and vendor docs

## Short TOC
- The sequence of the parts in the book is:
  - Foundations of AI-Assisted Coding
    - 01, LLM-Assisted Code Generation
    - 02, AI Pair Programming Workflows
    - 03, Prompt Engineering for Code
    - 04, Retrieval-Augmented Generation for Codebases
  - AI Across the Development Lifecycle
    - 05, AI Code Review
    - 06, Test Generation and Coverage with AI
    - 07, Multi-Agent Systems for Software Tasks
    - 08, AI-Driven Refactoring and Legacy Code Migration
    - 09, Debugging with AI
  - Building, Evaluating, and Deploying AI Coding Systems
    - 10, Fine-Tuning and Adapting Models for Codebases
    - 11, Evaluation of AI Coding Tools
    - 12, AI in CI/CD
  - Trust, Collaboration, and Governance
    - 13, Trust, Verification, and Hallucination Risks
    - 14, Human-AI Collaboration Patterns
    - 15, Ethics, IP, and Security of AI-Generated Software

## All Lesson Materials
// No `generate_all_tocs.sh` exists yet for this book (see TODOs) — list is
// hand-maintained until one is added

- `book_AI_Software_Engineering/lectures_notes/*.txt`
- `book_AI_Software_Engineering/lectures_notes/*.md`

## Chapter Templates and Invariants
- Follow `.claude/skills/book.rules.md` for the Chapter Template (Goals,
  Topics, TODO, Slides, Lesson Materials, Notes) and Roadmap section
  conventions used throughout this file

# Roadmap

| Chap                                          | Slides                                                | Slides % | Criticize | Tutorial | Book |
| ---------------------------------------------- | ------------------------------------------------------ | -------- | --------- | -------- | ---- |
|                                                |                                                        |          |           |          |      |
| **Foundations of AI-Assisted Coding**         |                                                        |          |           |          |      |
| 01. LLM-Assisted Code Generation              | N/A                                                    |          |           |          |      |
| 02. AI Pair Programming Workflows             | Lesson01-AI_workflows_for_coding.txt, claude_code.md   | 15%      |           |          |      |
| 03. Prompt Engineering for Code               | N/A                                                    |          |           |          |      |
| 04. Retrieval-Augmented Generation for Codebases | N/A                                                 |          |           |          |      |
| **AI Across the Development Lifecycle**       |                                                        |          |           |          |      |
| 05. AI Code Review                            | N/A                                                    |          |           |          |      |
| 06. Test Generation and Coverage with AI      | N/A                                                    |          |           |          |      |
| 07. Multi-Agent Systems for Software Tasks    | N/A                                                    |          |           |          |      |
| 08. AI-Driven Refactoring and Legacy Code Migration | N/A                                              |          |           |          |      |
| 09. Debugging with AI                         | N/A                                                    |          |           |          |      |
| **Building, Evaluating, and Deploying AI Coding Systems** |                                            |          |           |          |      |
| 10. Fine-Tuning and Adapting Models for Codebases | N/A                                                |          |           |          |      |
| 11. Evaluation of AI Coding Tools             | N/A                                                    |          |           |          |      |
| 12. AI in CI/CD                               | claude_code.md (partial)                               | 5%       |           |          |      |
| **Trust, Collaboration, and Governance**      |                                                        |          |           |          |      |
| 13. Trust, Verification, and Hallucination Risks | N/A                                                  |          |           |          |      |
| 14. Human-AI Collaboration Patterns           | N/A                                                    |          |           |          |      |
| 15. Ethics, IP, and Security of AI-Generated Software | N/A                                             |          |           |          |      |

## TODOs
- [ ] Write `book_AI_Software_Engineering/generate_all_tocs.sh` to regenerate
  `## All Lesson Materials`
- [ ] Author dedicated slide decks for chapters 01, 03-11, 13-15 (currently no
  source material)
- [ ] Expand `lectures_notes/Lesson01-AI_workflows_for_coding.txt` from a
  4-bullet stub into a full chapter 02 deck, or retire it in favor of a new
  deck
- [ ] Search other course dirs (`msml610`, `data605`, `book.Agentic_AI`,
  `helpers_root`) for reusable material once each chapter's Topics are final
- [ ] Add a `tutorials/` directory once chapters have runnable notebook
  examples

# Detailed TOC

# Part I: Foundations of AI-Assisted Coding

## 01: LLM-Assisted Code Generation

### Goals
- Explain how LLMs generate code from natural-language specs and context
- Show how context window size and retrieval shape generation quality
- Identify structural limits: hallucinated APIs, stale data, scale limits

### Topics
- How LLMs Generate Code
  - Autoregressive token prediction over code and docs
  - Training data: public repos, documentation, synthetic code
- Context and Prompting Patterns
  - System prompts, few-shot examples, instructions vs. completions
  - Context window size and its effect on multi-file generation
- Limits of Code Generation
  - Hallucinated APIs and outdated library versions
  - Token/context budget limits on large codebases
  - When generation degrades: long files, ambiguous specs

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 02: AI Pair Programming Workflows

### Goals
- Compare pair-programming tools: Claude Code, Copilot, Cursor, and their models
- Map tool choice to workflow: CLI, IDE, desktop, web, mobile
- Show how integrations (CI, chat, MCP) extend pair programming past the editor

### Topics
- Pair Programming Tool Landscape
  - Claude Code, GitHub Copilot, Cursor: interaction models compared
  - Autocomplete vs. agentic (multi-step, tool-using) assistants
- Where to Run the Assistant
  - CLI, Desktop, VS Code, JetBrains, Web, Mobile
  - Trade-offs: terminal scripting vs. visual review vs. long-running tasks
- Extending the Workflow
  - GitHub/GitLab CI integration, automated PR review
  - Chat integrations (Slack), browser automation, MCP servers
- Working Asynchronously
  - Dispatch, remote control, scheduled tasks, background sessions

### Slides
- `book_AI_Software_Engineering/lectures_notes/Lesson01-AI_workflows_for_coding.txt`

### Lesson Materials
- `book_AI_Software_Engineering/lectures_notes/claude_code.md`
  - [35%]: Where to run Claude Code (CLI/Desktop/VS Code/JetBrains/Web/
    Mobile), tool integrations (Chrome, GitHub Actions/GitLab CI, Slack,
    MCP), working away from the terminal (Dispatch, Remote Control,
    Channels, Scheduled tasks)
- `book_AI_Software_Engineering/lectures_notes/Lesson01-AI_workflows_for_coding.txt`
  - [10%]: 4-bullet stub outline only (Managing Code, Automating PR,
    Automating Documentation, Coding while you sleep) — headers, no content
- Not covered
  - [55%]: Head-to-head comparison of Claude Code vs. Copilot vs. Cursor;
    autocomplete-vs-agentic distinction; no material at all on Copilot or
    Cursor specifically

### Notes
- The two source files are stubs (56 lines total), not a full deck — treat
  the coverage numbers above as thin

## 03: Prompt Engineering for Code

### Goals
- Write specs an AI can implement correctly on the first attempt
- Use few-shot examples and chain-of-thought to steer code generation
- Structure prompts for multi-step and multi-file coding tasks

### Topics
- Writing Specs for AI
  - Precise requirements, constraints, and acceptance criteria
  - Examples of ambiguous vs. unambiguous specs
- Few-Shot and Pattern-Based Prompting
  - Providing in-context examples of desired code style
  - Style/convention transfer from an existing codebase
- Reasoning-Oriented Prompting
  - Chain-of-thought and step-by-step decomposition
  - Plan-then-implement prompting patterns
- Prompting for Multi-File Tasks
  - Decomposing large tasks into scoped, reviewable steps
  - Iterative refinement loops with the model

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 04: Retrieval-Augmented Generation for Codebases

### Goals
- Explain how RAG grounds code generation in a repo's actual code and docs
- Compare retrieval strategies: embeddings, keyword search, symbol indexes
- Identify failure modes: stale indexes, irrelevant retrieval, retrieval gaps

### Topics
- Why RAG for Code
  - Limits of parametric knowledge for large/private codebases
  - Grounding generation in current repo state
- Retrieval Strategies
  - Embedding-based semantic search over code and docs
  - Keyword/AST/symbol-based retrieval; hybrid approaches
- Building a Code RAG Pipeline
  - Chunking strategies for code (function, file, module level)
  - Indexing, freshness, and incremental updates
- Failure Modes
  - Stale indexes after refactors
  - Irrelevant or noisy retrieval degrading generation quality

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

# Part II: AI Across the Development Lifecycle

## 05: AI Code Review

### Goals
- Use AI to find correctness bugs, security issues, and style violations
- Distinguish automated linting from semantic AI-driven review
- Design review workflows that combine AI and human reviewers

### Topics
- What AI Code Review Catches
  - Correctness bugs, edge cases, logic errors
  - Security vulnerabilities and unsafe patterns
  - Style/convention violations and simplification opportunities
- Review Techniques
  - Diff-based review vs. whole-file/whole-repo review
  - Multi-pass and multi-agent adversarial review
- Integrating AI into Review Workflows
  - Inline PR comments, automated first-pass review
  - Human-in-the-loop: what to trust, what to verify
- Limits of AI Review
  - False positives/negatives, missing project-specific context

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 06: Test Generation and Coverage with AI

### Goals
- Generate unit, property-based, and mutation tests with AI assistance
- Use AI to close coverage gaps without inflating low-value tests
- Evaluate generated tests for correctness and maintainability

### Topics
- Generating Unit Tests
  - From function signature/docstring to test cases
  - Edge cases, boundary conditions, error paths
- Property-Based and Mutation Testing
  - AI-generated property invariants
  - Using mutation testing to validate test-suite strength
- Coverage-Driven Generation
  - Targeting uncovered branches/lines with AI
  - Avoiding low-value, brittle, or redundant tests
- Evaluating Generated Tests
  - Do tests actually assert behavior, or just execute code?
  - Maintainability and readability of AI-written tests

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 07: Multi-Agent Systems for Software Tasks

### Goals
- Design multi-agent workflows: orchestration, subagents, and tool use
- Decide when to fan out work vs. run a single sequential agent
- Apply patterns: pipelines, parallel review, judge panels, adversarial checks

### Topics
- Agent Architectures
  - Single agent with tools vs. orchestrator + subagents
  - Tool use: file access, shell, search, external APIs
- Orchestration Patterns
  - Pipelines, parallel fan-out, barriers, loop-until-dry
  - Judge panels and adversarial verification
- Coordination and Context
  - Passing context between agents; avoiding context bloat
  - Isolation: worktrees, sandboxing for parallel edits
- When Multi-Agent Helps
  - Comprehensive coverage, independent verification, scale
  - Costs: token overhead, coordination complexity

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 08: AI-Driven Refactoring and Legacy Code Migration

### Goals
- Use AI to refactor code while preserving behavior
- Plan large-scale migrations (language, framework, API) with AI assistance
- Verify refactors and migrations with tests and diffing, not just review

### Topics
- Refactoring with AI
  - Renaming, extracting functions, simplifying control flow
  - Preserving behavior: test-before/test-after discipline
- Legacy Code Migration
  - Language/framework version upgrades
  - API migrations across large codebases
- Migration Strategy
  - Incremental vs. big-bang migration
  - Isolating migration units for independent verification
- Verifying Correctness
  - Golden-file/regression testing before and after
  - Diff review at scale; sampling strategies for large migrations

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 09: Debugging with AI

### Goals
- Use AI to triage logs and reproduce failures from partial information
- Apply root-cause analysis techniques with AI assistance
- Know when AI debugging helps vs. when it guesses

### Topics
- Log and Error Triage
  - Parsing stack traces, error messages, and CI failure logs
  - Distinguishing symptom from root cause
- Reproducing Failures
  - Constructing minimal repro cases with AI help
  - Flaky test diagnosis
- Root-Cause Analysis
  - Bisection, hypothesis generation, targeted instrumentation
  - Reasoning across multiple files/services with AI
- Limits and Pitfalls
  - AI guessing plausible but wrong root causes
  - When to fall back to manual debugging

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

# Part III: Building, Evaluating, and Deploying AI Coding Systems

## 10: Fine-Tuning and Adapting Models for Codebases

### Goals
- Compare fine-tuning to prompting/RAG for domain-specific code
- Understand data requirements and risks of fine-tuning on code
- Evaluate when fine-tuning is worth the cost

### Topics
- Why Fine-Tune
  - Domain-specific conventions, internal APIs, proprietary patterns
  - Fine-tuning vs. prompting vs. RAG: trade-offs
- Fine-Tuning Approaches
  - Full fine-tuning, LoRA/adapters, instruction tuning
  - Data collection: curated examples, synthetic data, code history
- Risks and Costs
  - Overfitting to stale patterns, catastrophic forgetting
  - Compute cost, maintenance burden, retraining cadence
- Alternatives
  - System prompts, RAG, and tool use as lighter-weight substitutes

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 11: Evaluation of AI Coding Tools

### Goals
- Use benchmarks like SWE-bench to compare AI coding tool capability
- Define metrics beyond pass rate: cost, latency, human effort saved
- Design human evaluation studies for coding assistants

### Topics
- Benchmarks
  - SWE-bench and similar real-world issue-resolution benchmarks
  - HumanEval-style synthetic benchmarks and their limits
- Metrics Beyond Accuracy
  - Cost per task, latency, token usage
  - Human review time saved, edit distance from final merged code
- Human Evaluation
  - User studies, preference comparisons, longitudinal adoption studies
- Benchmark Pitfalls
  - Overfitting to benchmarks, data contamination, narrow task coverage

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 12: AI in CI/CD

### Goals
- Use AI to automate PR creation, review, and merge conflict resolution
- Integrate AI agents into GitHub/GitLab CI pipelines safely
- Generate release notes and changelogs from commit/PR history with AI

### Topics
- Automated PR Workflows
  - AI-generated PRs from issues or specs
  - Automated first-pass PR review and inline comments
- Merge Conflict Resolution
  - AI-assisted conflict resolution strategies
  - When to trust automated resolution vs. escalate to a human
- CI Pipeline Integration
  - GitHub Actions/GitLab CI agent integration
  - Gating: what runs automatically vs. requires approval
- Release Automation
  - AI-generated release notes and changelogs
  - Versioning and rollback safety nets

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- `book_AI_Software_Engineering/lectures_notes/claude_code.md`
  - [15%]: GitHub Actions/GitLab CI/CD integration, automated PR review
    mentioned as connected tools — no depth on merge conflicts, release
    notes, or gating policy
- Not covered
  - [85%]: Merge conflict resolution, release-note/changelog generation,
    approval gating design

# Part IV: Trust, Collaboration, and Governance

## 13: Trust, Verification, and Hallucination Risks

### Goals
- Identify when generated code hallucinates APIs, facts, or behavior
- Apply verification strategies: tests, sandboxing, provenance tracking
- Calibrate trust in AI output based on task type and evidence

### Topics
- Hallucination in Code
  - Invented APIs, incorrect library behavior, fabricated results
  - Why hallucination happens: pattern completion vs. grounded fact
- Verification Strategies
  - Test execution as ground truth
  - Sandboxed execution, golden-file comparison
- Provenance and Evidence
  - Tracking what evidence backs a generated claim/change
  - Evidence-carrying changes: tests, logs, diffs as proof
- Calibrating Trust
  - Task types where AI is reliable vs. unreliable
  - Confidence signals and when to require human verification

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 14: Human-AI Collaboration Patterns

### Goals
- Compare review-loop, pair, and autonomous collaboration modes
- Design handoff points between human and AI in a workflow
- Match collaboration mode to task risk and reversibility

### Topics
- Collaboration Modes
  - Pair (synchronous) vs. autonomous (asynchronous) agent work
  - Review-loop: propose, review, revise cycles
- Designing Handoffs
  - What to delegate fully vs. what requires a human decision
  - Confirmation points for hard-to-reverse or outward-facing actions
- Task-Risk Matching
  - Low-risk (formatting, tests) vs. high-risk (schema, security) tasks
  - Escalation paths when AI is uncertain
- Team Workflows
  - Multiple engineers working alongside AI agents
  - Shared conventions and context (CLAUDE.md-style instructions)

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic

## 15: Ethics, IP, and Security of AI-Generated Software

### Goals
- Identify licensing and IP risks in AI-generated code
- Recognize vulnerability-injection and supply-chain risks from AI tools
- Apply governance practices for responsible AI-assisted development

### Topics
- Licensing and IP
  - Training-data provenance and license-contamination risk
  - Attribution and copyright questions for generated code
- Security Risks
  - AI-introduced vulnerabilities: injection, unsafe defaults
  - Supply-chain risk: AI-suggested dependencies and packages
- Responsible Use
  - Authorization boundaries for AI-driven security testing
  - Data privacy: what code/data should not reach external models
- Governance
  - Organizational policy for AI tool use in production code
  - Auditability and accountability for AI-assisted changes

### Slides
- N/A — no dedicated deck yet

### Lesson Materials
- Not covered
  - [100%]: No existing lecture material found in this repo for this topic
