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

## RTK: Compress Tool Output Too

- The draft also mentions [RTK](https://github.com/juliusbrussee/caveman) (Real
  Token Killer), a companion tool that compresses _terminal output_ before it
  reaches the model
- Large logs, test failures, and build output are often the biggest token
  consumer
- Community reports claim 60-90% reductions in command-output tokens

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
