llm install llm-openrouter

> llm --version
pip show llm-openrouter
llm, version 0.30

saggese@gpmac.local venv:(llm-env) branch:'gp_scratch' ~/src/umd_classes2
> pip show llm-openrouter
Name: llm-openrouter
Version: 0.5
Summary: LLM plugin for models hosted by OpenRouter
Home-page: https://github.com/simonw/llm-openrouter
Author: Simon Willison
Author-email:
License: Apache-2.0
Location: /Users/saggese/src/umd_classes2/llm-env/lib/python3.14/site-packages
Requires: httpx, llm, openai
Required-by:


llm openrouter models

export OPENROUTER_KEY=$OPENROUTER_API_KEY

> llm openrouter models | head
- id: anthropic/claude-opus-4.7
  name: Anthropic: Claude Opus 4.7
  context_length: 1,000,000
  architecture:
    modality: text+image->text
    input_modalities: ["text", "image"]
    output_modalities: ["text"]
    tokenizer: Claude
    instruct_type: null
  supports_schema: True


llm -m $MODEL -o provider '{"sort": "throughput"}' "Explain recursion in 1000 words" | tee output.txt

> llm models | grep openrouter | head
OpenRouter: openrouter/anthropic/claude-opus-4.7
OpenRouter: openrouter/openrouter/elephant-alpha
OpenRouter: openrouter/anthropic/claude-opus-4.6-fast
OpenRouter: openrouter/z-ai/glm-5.1
OpenRouter: openrouter/google/gemma-4-26b-a4b-it:free
OpenRouter: openrouter/google/gemma-4-26b-a4b-it
OpenRouter: openrouter/google/gemma-4-31b-it:free
OpenRouter: openrouter/google/gemma-4-31b-it
OpenRouter: openrouter/qwen/qwen3.6-plus
OpenRouter: openrouter/z-ai/glm-5v-turbo

> llm -m openrouter/google/gemma-4-26b-a4b-it:free "hi"
Hello! How can I help you today?

# Test for nitro
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openrouter/nitro","messages":[{"role":"user","content":"Hello!"}]}'


# Usage
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | jq '.data.usage'
