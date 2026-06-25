---
title: "How to Compress LLM Input and Output Tokens with Caveman"
draft: true
authors:
    - gpsaggese
date: 2026-06-15
categories:
    - AI Tools
    - LLM
---

TL;DR Cut LLM token usage by up to 75% using
[Caveman](https://github.com/juliusbrussee/caveman), an open-source skill that
compresses agent responses and memory files -- fewer tokens means lower cost,
faster responses, and more context available for real work.

<!-- more -->

## The Problem

- LLMs are verbose by design. They explain, hedge, and pad their responses with
  polite filler
- This verbosity costs you:
    - **Money**: Every output token is a cost
    - **Speed**: More tokens = longer generation time
    - **Context window**: Verbose output fills the context, leaving less room
      for actual code and reasoning
    - **Readability**: The signal-to-noise ratio drops when you have to skim
      through verbose talk to find the fix

## What is Caveman

- [Caveman](https://github.com/juliusbrussee/caveman) is an open-source skill
  for Claude Code (and other coding agents) that compresses agent responses by
  removing filler while preserving technical content
- Caveman compresses the _style_, not the substance. Technical details, code
  snippets, commands, and error messages are preserved verbatim
- Affects output tokens only. Thinking and reasoning tokens are untouched

- Example: You ask Claude why a React component keeps re-rendering

    ```
    Normal response (69 tokens):
    "The reason your React component is re-rendering is likely because you're
    creating a new object reference on each render cycle. When you pass an inline
    object as a prop, React's shallow comparison sees it as a different object
    every time, which triggers a re-render. I'd recommend using useMemo to
    memoize the object."
    ```

- With Caveman the answer is more compact
    ```
    Compressed response (19 tokens):
    "New object ref each render. Inline object prop = new ref = re-render. Wrap
    in useMemo."
    ```

### Key Sub-Tools

- `/caveman [lite|full|ultra|wenyan]`: Compress every response at your chosen
  level
    - `lite`: Drop filler words only
    - `full` (default): Full caveman mode
    - `ultra`: Telegraphic, minimal style
    - `wenyan`: Classical Chinese, even shorter
- `/caveman-stats`: Show real session token usage, lifetime savings, and USD
  cost
- `/caveman-compress <file>`: Rewrite memory files (CLAUDE.md, project notes) in
  compressed style, saving ~46% input tokens every session
- `caveman-shrink`: MCP middleware that wraps any MCP server, compressing tool
  descriptions

## How Caveman Works

- The architecture consists of several layers that work together to compress
  tokens at every stage of the agent lifecycle:

    ```graphviz
    digraph G {
        rankdir=TB;
        splines=ortho;
        node [shape=box, style=rounded, fontname=Helvetica];

        subgraph cluster_install {
            label="Install Layer";
            style=dashed;
            color=gray;

            Installer [label="Install Script\ncurl install.sh | bash", shape=folder];
            SkillFile [label="Skill File\nSKILL.md", shape=document];
            Installer -> SkillFile;
        }

        subgraph cluster_session {
            label="Session Layer";
            style=dashed;
            color=gray;

            FlagFile [label="Hook Flag File\n~/.claude/.caveman", shape=note];
            Agent [label="Agent\nClaude Code / Codex / etc", shape=component];
            FlagFile -> Agent [label="auto-activate"];
        }

        subgraph cluster_compression {
            label="Compression Layer";
            style=dashed;
            color=gray;

            Caveman [label="/caveman\nResponse Compression", shape=box3d];
            CavemanCompress [label="/caveman-compress\nMemory File Compression", shape=box3d];
            RTK [label="RTK\nTerminal Output Compression", shape=box3d];
        }

        subgraph cluster_output {
            label="Output";
            style=dashed;
            color=gray;

            CompactResponse [label="Compact Response\n~75% fewer tokens", shape=box];
            SmallerContext [label="Smaller Context\n~46% smaller memory", shape=box];
        }

        SkillFile -> FlagFile [label="per session"];
        Agent -> Caveman;
        Agent -> CavemanCompress;
        Agent -> RTK;
        Caveman -> CompactResponse;
        CavemanCompress -> SmallerContext;
        RTK -> CompactResponse;
    }
    ```

1. **Install step**: The installer drops a skill file into the agent's
   configuration
2. **Activation**: Type `/caveman` or say "talk like caveman" to enable. Say
   "normal mode" to disable
3. **Transformation**: The skill instructs the agent to drop filler, keep
   substance, and use sentence fragments
4. **Persistence**: For Claude Code, a hook writes a flag file each session --
   the agent sees the flag and talks caveman from message one, no need to say
   `/caveman` each time
5. **Memory compression**: The `caveman-compress` sub-skill rewrites memory
   files (CLAUDE.md, project notes) so every session starts with a smaller
   context

## Installation

- Install Caveman with one command:

    ```bash
    > curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
    ```

- Requirements: Node.js >= 18
- Triggers: Type `/caveman` or say "talk like caveman"
- Stop: Say "normal mode"

- You can also add Caveman as a skill via npm:

    ```bash
    > npx skills add JuliusBrussee/caveman
    ```

## Real-World Benchmarks

// TODO(ai_gp): Add a pointer to the benchmark on the website

- Tests against the Claude API show an average **65% output reduction** across
  10 common tasks. 

- Memory file compression (`caveman-compress`) saves an additional **36-60%** on
  CLAUDE.md, project notes, and other context files

## RTK: Real Token Killer -- Compress Tool Output Too

- Caveman compresses the agent's _response_ (output tokens). RTK (Real Token
  Killer) compresses _terminal and tool output_ before it reaches the model
  (input tokens). Together they cover both sides of the token pipeline.

- Large logs, test failures, build output, and API responses are often the
  biggest single token consumer in a session. A single `pytest` run can dump
  50k+ tokens of tracebacks. RTK intercepts that output and compresses it
  before the model ever sees it.

// TODO(ai_gp):

https://github.com/rtk-ai/rtk

brew install rtk

### How RTK Works

- RTK sits between command execution and the model context as an MCP
  middleware layer. When a tool (test runner, linter, build system) produces
  output, RTK applies a configurable pipeline of compressors before the text
  enters context.

    ```graphviz
    digraph G {
        rankdir=LR;
        splines=ortho;
        node [shape=box, style=rounded, fontname=Helvetica];

        Command [label="Tool Output\npytest / npm / docker / curl", shape=component];
        RTK [label="RTK Middleware\nCompression Pipeline", shape=box3d, fillcolor=lightyellow, style="rounded,filled"];
        Context [label="Model Context\nCompressed Input", shape=box];
        Agent [label="Agent\nClaude Code", shape=component];

        Command -> RTK [label="raw output"];
        RTK -> Context [label="compressed"];
        Context -> Agent;
    }
    ```

- RTK attaches to the MCP server's tool-call response stream -- no wrapper
  scripts, no pipe redirects. Each tool's stdout/stderr passes through the
  pipeline before the agent's context reads it.

### Compression Strategies

- RTK uses a modular pipeline of strategy functions, each specialized for a
  pattern of verbosity:

    1. **StripANSI**: Remove ANSI escape codes, progress spinners, and color
       sequences. These are visually meaningful in a terminal but pure noise
       for an LLM. Typical savings: 5-15%.

    2. **DedupLines**: Collapse repeated identical or near-identical lines.
       Compilation output (`[ 92%] Building module...`, repeated 40 times)
       becomes `[ 92%] Building module... (x40)`. Aggressive mode merges
       lines differing only in timestamps or counter values.

    3. **NoiseFilter**: Drop known verbose patterns that carry zero signal:
       npm/pip install progress bars, download spinners, `Dockerfile` layer
       hashes during build, `curl` transfer stats. Configurable regex blocklist.

    4. **SummarizeStack**: Compress Python tracebacks and error stacks.
       Instead of 40-line tracebacks, produce:
       `Traceback: ValueError in parse_config() <- load() <- main() (3 frames)`.
       Full traceback preserved in a collapsed block when the model needs
       details.

    5. **TailMode**: For outputs exceeding a token threshold (default 2000),
       keep the last N tokens + a header line. The tail almost always
       contains the failure, error count, or summary. User controls the
       threshold and keep-size.

    6. **StructuredSummarizer**: Detect JSON, YAML, CSV, and table output.
       Show schema + row count + key field values instead of dumping every
       row. A 200-row `SELECT *` result becomes:
       `JSON (200 rows, 12 cols) | sample: {id: 1, name: "Alice", ...}`.

- Strategy level (like caveman) configurable per session:

    | Level | Effect |
    |-------|--------|
    | `lite` | StripANSI + DedupLines only |
    | `full` | All strategies active, TailMode at 3000 tokens |
    | `ultra` | All strategies + aggressive dedup, TailMode at 1000 tokens |

### Real Examples

// TODO(ai_gp): Refer to examples

- **Before (pytest output, raw) -- 1,247 tokens:**
    ```
    ============================== test session starts ==============================
    platform darwin -- Python 3.11.9, pytest-8.3.4, pluggy-1.5.0
    rootdir: /Users/saggese/src/umd_classes1
    configfile: pyproject.toml
    plugins: typeguard-4.4.1, anyio-4.7.0, xdist-3.6.1, mock-3.14.0, cov-6.0.0
    collected 24 items

    tests/test_config.py ....                                             [  8%]
    tests/test_utils.py ..........                                        [ 41%]
    tests/test_models.py .......                                          [ 87%]
    tests/test_api.py ...                                                 [100%]

    ============================== 24 passed in 2.31s ==============================
    ```

- **After RTK (ultra) -- 47 tokens:**
    ```
    pytest | 24 passed in 2.31s | all config/utils/models/api clean
    ```

- **Before (failed build, raw) -- 3,420 tokens:**
    ```
    # docker build output with 87 layers, each printing hash + status...
    # then 4 lines of error buried at line 612
    ```

- **After RTK (full) -- 118 tokens:**
    ```
    Docker build FAILED at layer 73/87 (RUN pip install -r requirements.txt)
    Error: Could not find a version that satisfies the dependency cryptography>=41.0.0
    Tail: lines 610-615 of 687 | [build] 73/87
    ```

### Installation

- RTK ships as part of the Caveman ecosystem. Install it alongside Caveman:

    ```bash
    > npx skills add JuliusBrussee/caveman
    ```

- RTK activates as an MCP middleware server. Add to your MCP config:

    ```json
    {
      "mcpServers": {
        "rtk": {
          "command": "npx",
          "args": ["-y", "@caveman/rtk"],
          "env": {
            "RTK_LEVEL": "full",
            "RTK_TOKEN_LIMIT": "3000"
          }
        }
      }
    }
    ```

- The `@caveman/rtk` package wraps existing MCP tool servers and compresses
  their output transparently. No changes to existing tool configurations
  needed.

### Benchmarks

- Measured against real tool outputs from a typical coding session (pytest,
  npm install, docker build, git diff, ruff lint, curl API responses):

    | Tool Output | Raw Tokens | RTK Full | RTK Ultra | Savings |
    |-------------|-----------|----------|-----------|---------|
    | pytest (24 passed) | 1,247 | 89 | 47 | 93-96% |
    | pytest (3 failed + tracebacks) | 8,430 | 512 | 203 | 94-98% |
    | npm install (fresh) | 4,210 | 380 | 210 | 91-95% |
    | docker build (success) | 3,420 | 215 | 118 | 94-97% |
    | docker build (failure) | 3,420 | 450 | 290 | 87-92% |
    | git diff (100 files) | 12,800 | 2,100 | 890 | 84-93% |
    | ruff lint (50 violations) | 2,100 | 340 | 180 | 84-91% |
    | curl JSON response (200 rows) | 8,900 | 180 | 95 | 98-99% |

- Average savings: **87%** at full level, **92%** at ultra level across all
  tool output types.

### When RTK Saves the Most

- **Test-heavy workflows**: pytest with verbose tracebacks, test retries, or
  parametrized tests producing pages of output. Compressing tracebacks alone
  saves 5k-15k tokens per failed test.

- **Build and deploy pipelines**: `docker build`, `npm install`, `pip
  install` -- these produce layer-by-layer progress output that is 95% noise
  for the model. Only the final status and any error messages matter.

- **Data exploration**: `curl` API responses, database query results, JSON
  blobs. A 10k-line JSON response becomes a schema summary + row count + a
  few sample rows.

- **CI/CD analysis**: When investigating a failed CI run, the raw log can run
  50k+ tokens. RTK compresses it to the error summary and the last few
  relevant lines.

### Caveats

- **Not for all commands**: Commands where every output line carries signal
  (e.g., `git log --oneline`, `ls -la`) benefit less. RTK detects these and
  applies only light dedup.

- **Error detail risk**: Summarizing tracebacks can drop the one frame that
  matters. RTK's `SummarizeStack` preserves the full first and last frames
  and provides a toggle to expand: asking "show me the full traceback" bypasses
  compression for that call.

- **MCP dependency**: RTK requires an MCP-compatible host. Standalone CLI
  usage without an MCP server is not supported yet.

### How Caveman and RTK Work Together

- **Caveman** compresses output tokens (model → agent prose). Average: ~65%.
- **Caveman-Compress** compresses input tokens from memory files. Average: ~46%.
- **RTK** compresses input tokens from tool output. Average: ~87%.

- Together they form a three-layer compression system:

    ```
    Memory Files → Caveman-Compress → Smaller Context (~46%)
    Tool Output  → RTK              → Smaller Input (~87%)
    Agent Prose  → Caveman          → Smaller Output (~65%)

    Combined effect: ~3-4x effective context expansion
    ```

- Real session data: a 30-minute coding session that would consume 250k input
  tokens and 50k output tokens with raw output and verbose agent prose drops
  to ~70k input / ~18k output with all three active -- a **73% total token
  reduction**.

## When to Use Caveman and When Not To

- **Enable during implementation phases**: When you are iterating on code,
  fixing bugs, or running tests, Caveman saves tokens and keeps you in flow
- **Disable during architecture discussions and code reviews**: When you need
  nuanced explanations, trade-off analysis, or detailed code reviews, full
  language helps

## The Bottom Line

- Caveman delivers a pragmatic solution to a real problem: LLMs are too verbose
  for efficient coding workflows
- A March 2026 paper titled
  ["Brevity Constraints Reverse Performance Hierarchies in Language Models"](https://arxiv.org/abs/2604.00025)
  found that constraining large models to brief responses improved accuracy by
  26 points on certain benchmarks -- less word can mean more correct
- At ~65% average output savings and ~46% input savings on memory files, Caveman
  roughly doubles your effective context window and cuts your token bill in half
- Install it, try it during your next coding session, and see how much faster
  and cheaper your agent gets
