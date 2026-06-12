# Parsing Claude Code logs

When running Claude Code with `--print --output-format=stream-json`, every event
is written to stdout as a newline-delimited JSON stream (NDJSON). Each line is
a self-contained JSON record.

## Record types

// TODO(ai_gp): Add a short explanation of `type`

| Type | Subtype | What it contains |
|------|---------|------------------|
| `system` | `init` | Session metadata: model, tools, skills, config, version |
| `system` | `status` | Status transitions (e.g. `"requesting"`) |
| `system` | `thinking_tokens` | Estimated thinking token count (delta-based) |
| `stream_event` | `message_start` | Start of an LLM response: model name, provider (Alibaba/SiliconFlow), ttft_ms |
| `stream_event` | `content_block_start` | Start of a content block (thinking, tool_use, text, redacted_thinking) |
| `stream_event` | `content_block_delta` | Streaming text/thinking/input_json fragments within a block |
| `stream_event` | `content_block_stop` | End of a content block (signals a complete thinking or tool_use block) |
| `stream_event` | `message_delta` | End-of-request summary: input/output tokens, cost, speed tier |
| `stream_event` | `message_stop` | End of the message stream |
| `assistant` | | Complete assistant message with all content blocks (thinking, tool_use, text) |
| `user` | | User message containing tool_result blocks returned from tool execution |

## Key fields to extract

### Session metadata (`system/init`)

// TODO(ai_gp): Add a comment to explain what each block means

```json
{
  "model": "deepseek/deepseek-v4-flash",
  "claude_code_version": "2.1.173",
  "session_id": "fdac299b-...",
  "permissionMode": "bypassPermissions",
  "tools": ["Bash", "Read", "WebFetch", ...],
  "skills": ["notebook.create_api_intro", ...]
}
```

### Request cost (`stream_event/message_delta`)

```json
{
  "event": {
    "type": "message_delta",
    "usage": {
      "input_tokens": 26451,
      "output_tokens": 320,
      "output_tokens_details": { "thinking_tokens": 62 },
      "cost": 0.003630,
      "speed": "standard"
    }
  }
}
```

### Tool calls (`assistant` > content blocks with `type: "tool_use"`)

```json
{
  "type": "tool_use",
  "name": "WebFetch",
  "input": { "url": "...", "prompt": "..." }
}
```

### Tool results (`user` > content blocks with `type: "tool_result"`)

```json
{
  "type": "tool_result",
  "tool_use_id": "call_...",
  "is_error": false,
  "content": "...",
  "url": "https://...",
  "durationMs": 22074
}
```

## Using `jq`

One-liner to extract all tool calls with their names and inputs:

```bash
jq -r 'select(.type == "assistant") |
  .message.content[] | select(.type == "tool_use") |
  "\(.name) \(.id | .[0:20])"'
```

// TODO(ai_gp): Run each one-liner on log.txt and print an example

Extract per-request costs:

```bash
jq -r 'select(.type == "stream_event" and .event.type == "message_delta") |
  [.event.usage.input_tokens, .event.usage.output_tokens, .event.usage.cost] | @tsv'
```

Reconstruct thinking content by collecting all `thinking_delta` fragments:

```bash
jq -r 'select(.type == "stream_event" and .event.type == "content_block_delta"
  and .event.delta.type == "thinking_delta") | .event.delta.thinking' log.txt
```

## Using the extraction script

The repo includes `extract_cc_log.py` which does all of the above in one pass:

```bash
# Full narrative (thinking + costs + tools + text)
./extract_cc_log.py --file log.txt

# Only the text the assistant showed the user
./extract_cc_log.py --file log.txt --text_only

# Save to a file
./extract_cc_log.py --file log.txt --output_dir /tmp
```

## Log structure diagram

```
{"type":"system","subtype":"init",...}            # session init
{"type":"system","subtype":"status",...}          # requesting status
{"type":"stream_event","event":{"type":"message_start",...}}
{"type":"stream_event","event":{"type":"content_block_start",...}}
{"type":"stream_event","event":{"type":"content_block_delta",...}}  # ~200-2000x
{"type":"stream_event","event":{"type":"content_block_stop",...}}
... repeated per tool call ...
{"type":"assistant",...}                           # full message snapshot
{"type":"user",...}                                # tool results
{"type":"stream_event","event":{"type":"message_delta",...}}  # cost
{"type":"stream_event","event":{"type":"message_stop",...}}
```

Each request cycle is:
- `message_start`
- N × (`content_block_start` / `content_block_delta` / `content_block_stop`)
- `message_delta`
- `message_stop`
- `user` record carrying tool results back to the model
