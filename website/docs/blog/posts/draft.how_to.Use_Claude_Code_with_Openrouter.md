# Configure Openrouter

- Create keys for the providers you already have
  https://platform.claude.com/settings/workspaces/default/keys

- Then do BYOK

- https://openrouter.ai/workspaces/default/byok

An openrouter key looks like

OPENROUTER_API_KEY=sk-or-v1-...

An Anthropic key looks like

ANTHROPIC_KEY=sk-ant-api03-...

An OpenAI key looks like

OPENAI_API_KEY=sk-proj-...

# Test Openrouter

- The available models are
curl https://openrouter.ai/api/v1/models -H "Authorization: Bearer $OPENROUTER_API_KEY" | jq '.data[].id' | sort

- Test a completion
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5",
    "messages": [
      {
        "role": "user",
        "content": "Reply with the word OK"
      }
    ]
  }'


# Configure ClaudeCode
export ANTHROPIC_DEFAULT_HAIKU_MODEL=openai/gpt-5
export ANTHROPIC_DEFAULT_OPUS_MODEL=openai/gpt-5
export ANTHROPIC_DEFAULT_SONNET_MODEL=openai/gpt-5
export ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1/anthropic
export ANTHROPIC_AUTH_TOKEN=$OPENROUTER_API_KEY

unset ANTHROPIC_KEY

The env looks like
> env  | sort | grep ANT
ANTHROPIC_AUTH_TOKEN=sk-or-v1-...
ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1/anthropic
ANTHROPIC_DEFAULT_HAIKU_MODEL=openai/gpt-5
ANTHROPIC_DEFAULT_OPUS_MODEL=openai/gpt-5
ANTHROPIC_DEFAULT_SONNET_MODEL=openai/gpt-5

Test that the models are available through the API

#
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5",
    "messages": [
      {
        "role": "user",
        "content": "Reply with the word OK"
      }
    ]
  }'


export ANTHROPIC_BASE_URL=https://openrouter.ai/api
export ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1
export ANTHROPIC_API_KEY=sk-or-v1

unset ANTHROPIC_API_KEY




> export ANTHROPIC_BASE_URL=https://openrouter.ai/api

saggese@gpmac.local venv:(client_venv.helpers) branch:'gp_scratch' ~/src/umd_classes1
> vi quick_test.py

saggese@gpmac.local venv:(client_venv.helpers) branch:'gp_scratch' ~/src/umd_classes1
> python quick_test.py
Endpoint : https://openrouter.ai/api
Model    : openai/gpt-5
Testing...

SUCCESS

#!/usr/bin/env python3

import os
import sys
from anthropic import Anthropic

BASE_URL = os.environ["ANTHROPIC_BASE_URL"]
API_KEY = os.environ["ANTHROPIC_AUTH_TOKEN"]
MODEL = os.environ["ANTHROPIC_DEFAULT_HAIKU_MODEL"]

if not API_KEY:
    print("ERROR: ANTHROPIC_AUTH_TOKEN is not set")
    sys.exit(1)

print(f"Endpoint : {BASE_URL}")
print(f"Model    : {MODEL}")
print("Testing...\n")

try:
    client = Anthropic(
        api_key=API_KEY,
        base_url=BASE_URL,
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=20,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: API_OK"
            }
        ],
    )

    text = "".join(
        block.text
        for block in response.content
        if getattr(block, "type", None) == "text"
    )

    print("SUCCESS")
    #print("Response:", repr(text))

except Exception as e:
    print("FAILED")
    #print(type(e).__name__)
    #print(str(e))
    sys.exit(2)


> echo $ANTHROPIC_BASE_URL
https://openrouter.ai/api

It works!


export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek/deepseek-v4-flash
export ANTHROPIC_DEFAULT_SONNET_MODEL=anthropic/haiku-4.5
export ANTHROPIC_DEFAULT_OPUS_MODEL=anthropic/haiku-4.5

> env | grep ANTH
ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek/deepseek-v4-flash
ANTHROPIC_DEFAULT_OPUS_MODEL=anthropic/haiku-4.5
ANTHROPIC_BASE_URL=https://openrouter.ai/api
ANTHROPIC_AUTH_TOKEN=sk-or-v1-...
ANTHROPIC_DEFAULT_SONNET_MODEL=anthropic/haiku-4.5


Test the model

> cc
 ▐▛███▜▌   Claude Code v2.1.158
 ▝▜█████▛▘  deepseek/deepseek-v4-flash · API Usage Billing
   ▘▘ ▝▝    ~/src/umd_classes1


   ❯ /model

   ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
     Select model
       Switch between Claude models. Your pick becomes the default for new
       sessions. For other/previous model names, specify with --model.

           1. Default (recommended)         Use the default model (currently
              anthropic/haiku-4.5[1m]) · $5/$25 per Mtok
                  2. anthropic/haiku-4.5           Custom Opus model
                      3. anthropic/haiku-4.5           Custom Sonnet model
                        ❯ 4. deepseek/deepseek-v4-flash ✔  Custom Haiku model

                          ● High effort (default) ←/→ to adjust

                            Enter to set as default · s to use this session only
                            · Esc to cancel

