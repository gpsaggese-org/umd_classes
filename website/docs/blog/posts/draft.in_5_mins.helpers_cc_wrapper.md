## The `cc` Convenience Wrapper

<!-- TODO(ai_gp): Point to the README of cc -->
<!-- TODO(ai_gp): Always use links to repo besides the path -->

- The repository provides a `cc` script at `dev_scripts_helpers/ai/` that wraps
  `claude` with sensible defaults for model selection and tmux integration

### Key Features

- Launches Claude Code interactively with `--dangerously-skip-permissions` for
  faster iteration
- Supports model selection via shorthand flags (Anthropic direct or various
  models through OpenRouter)
- Automatically configures the right environment variables depending on the
  chosen model
- Renames the tmux pane to `*CC*` during the session and restores it on exit
- Passes all additional arguments through to the underlying `claude` command

### Model Selection Flags

| Flag            | Description                                         |
| :-------------- | :-------------------------------------------------- |
| `--anth`        | Use Anthropic directly (clears OpenRouter env vars) |
| `--or_anth`     | Claude Haiku 4.5 via OpenRouter                     |
| `--ds`          | DeepSeek V4 Flash via OpenRouter (default)          |
| `--dsp`         | DeepSeek V4 Pro via OpenRouter                      |
| `--model MODEL` | Any model through OpenRouter                        |
| `--test`        | Run diagnostics (`claude doctor` + `/model`)        |

### Usage Examples

```bash
# Default: DeepSeek V4 Flash via OpenRouter
> cc

# Use Anthropic directly
> cc --anth

# Use Claude Haiku 4.5 via OpenRouter
> cc --or_anth

# Use a custom model through OpenRouter
> cc --model openrouter/meta-llama/llama-3.1-8b-instruct

# Run diagnostics
> cc --test
```

### Verifying the Model in Claude Code

- Once Claude Code launches with the `cc` wrapper, verify which model is active
  using the `/model` command:

    ```bash
    > cc
     ▐▛███▜▌   Claude Code v2.1.158
    ▝▜█████▛▘  deepseek/deepseek-v4-flash · API Usage Billing
      ▘▘ ▝▝    ~/src/xyz

    ❯ /model

    Select model
       Switch between Claude models. Your pick becomes the default for new
       sessions.

           1. Default (recommended)         Use the default model (currently
              anthropic/haiku-4.5) · $5/$25 per Mtok
           2. anthropic/haiku-4.5           Custom Opus model
           3. anthropic/haiku-4.5           Custom Sonnet model
         ❯ 4. deepseek/deepseek-v4-flash ✔  Custom Haiku model
    ```

