How to use https://github.com/juliusbrussee/caveman with claude code

How to download and install skill
npm install -g @anthropic-ai/claude-code

npx skills add JuliusBrussee/caveman

claude


Tool

Purpose

caveman

Compress output

cavemem

Compress memory/context

cavekit

Spec-driven workflow

caveman-code

Full coding agent with compression built in


RTK (compress tool output)

Instead of compressing Claude’s responses, RTK compresses terminal output before it reaches the model. Large logs, test failures, and build output are often the biggest token consumer. Community reports claim 60–90% reductions in command-output tokens.


4. Enable Caveman only during implementation phases
5. Turn Caveman off during architecture discussions and code reviews
