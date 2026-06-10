---
title: Ollama API and OpenAI Compatibility
slug: ollama-api-and-openai-compatibility
description: Using Ollama's REST API from scripts and external tools; how the OpenAI-compatible
  endpoint works, connecting Python code, Continue.dev, Obsidian plugins, and custom
  tools to your local model without Ollama's CLI wrapper.
silo: Local How-To
difficulty: beginner
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-20
updated: '2026-04-28'
soulcraft_theme: practical-emergence
meta_description: Using Ollama's REST API from scripts and external tools; how the
  OpenAI-compatible endpoint works, connecting Python code, Continue.dev, Obsidian
  plugins, and c
related:
- open-webui-setup
- getting-started-with-ollama
- llama-cpp-guide
- context-length-and-local-inference
- kv-cache
lesson_type: how-to
tags:
- local-inference
- ollama
- api
- openai-compatible
- howto
- practical-guide
- digital-sovereignty
- python
---


# Ollama API and OpenAI Compatibility

The Ollama CLI (`ollama run`) is for humans. The Ollama API is for everything else — scripts, tools, applications, and any external software that needs to talk to a local model without a human in the loop.

When you run `ollama serve`, a local HTTP server starts at `http://localhost:11434`. It exposes two API interfaces: Ollama's own native API, and an OpenAI-compatible API that mimics the exact format of OpenAI's hosted service. That second interface is why you can point dozens of tools designed for GPT-4 directly at your local model by changing a single URL.

---

## Technical Core

### The Two API Surfaces

Ollama exposes two different REST API surfaces at the same address:

**1. Ollama Native API** — at `/api/*`
Ollama's own format. Slightly more expressive, matches Ollama's model naming, returns streaming JSON by default. Good for custom scripts where you control both ends.

**2. OpenAI-Compatible API** — at `/v1/*`
Mirrors the exact request/response schema of OpenAI's API. Designed to be a drop-in replacement. Any tool that supports a custom `base_url` for OpenAI's API can be pointed here.

Both are served simultaneously. You can use whichever fits your tooling.

---

### Native API: Core Endpoints

**Generate (single-turn completion):**

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Explain attention mechanisms briefly.",
    "stream": false
  }'
```

Response:
```json
{
  "model": "llama3.2",
  "response": "Attention mechanisms allow a model to...",
  "done": true,
  "eval_duration": 2400000000,
  "eval_count": 87
}
```

**Chat (multi-turn conversation):**

```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is backpropagation?"}
    ],
    "stream": false
  }'
```

**List available models:**

```bash
curl http://localhost:11434/api/tags
```

**Check which models are currently loaded in memory:**

```bash
curl http://localhost:11434/api/ps
```

**Pull a model via API (same as `ollama pull`):**

```bash
curl http://localhost:11434/api/pull \
  -d '{"name": "mistral"}'
```

---

### OpenAI-Compatible API: Drop-in Replacement

The `/v1` endpoints match OpenAI's API exactly. The primary endpoint you'll use:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "user", "content": "What is the KV cache?"}
    ]
  }'
```

This returns the standard OpenAI chat completion response format:
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "llama3.2",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "The KV cache is a technique used during inference to..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 14,
    "completion_tokens": 68,
    "total_tokens": 82
  }
}
```

The API key field is **required by the schema but not validated** — Ollama will accept any string, or the literal string `"ollama"`:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Authorization: Bearer ollama" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

### Using the Python `openai` Library

Because Ollama's `/v1` endpoint mirrors OpenAI's format exactly, you can use the official `openai` Python library with zero changes to your existing code — just override the `base_url` and `api_key`:

```python
from openai import OpenAI

# Point the client at your local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Required but not validated
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a concise technical assistant."},
        {"role": "user", "content": "Explain gradient descent in two sentences."},
    ],
)

print(response.choices[0].message.content)
```

Install if needed:
```bash
pip install openai
```

This is the fastest way to prototype against a local model in Python — you write code that works locally, and if you ever need to switch to a cloud model, you just change `base_url` and `api_key` back to OpenAI's real credentials.

---

### Streaming Responses

By default, Ollama's native API streams output as tokens arrive. In the OpenAI-compatible API, streaming is opt-in with `"stream": true`:

**Native API (streams by default):**
```python
import requests, json

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.2", "prompt": "Count to 10."},
    stream=True,
)

for line in response.iter_lines():
    if line:
        chunk = json.loads(line)
        print(chunk["response"], end="", flush=True)
        if chunk.get("done"):
            break
```

**OpenAI-compatible streaming:**
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

stream = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Tell me a short story."}],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

---

### Connecting External Tools

Because Ollama uses the OpenAI schema at `/v1`, any tool with a "custom API endpoint" setting can be pointed at it:

**Continue.dev (VS Code/JetBrains AI assistant):**

In `.continue/config.json`:
```json
{
  "models": [{
    "title": "Llama 3.2 (Local)",
    "provider": "ollama",
    "model": "llama3.2"
  }]
}
```
Or manually via the OpenAI provider with `apiBase: "http://localhost:11434/v1"`.

**Open WebUI:**
Already configured to use Ollama natively — see [[open-webui-setup]].

**Obsidian Copilot plugin:**
In plugin settings, set Provider to `OpenAI-Compatible`, Base URL to `http://localhost:11434/v1`, API Key to `ollama`, and Model to whatever you have pulled.

**LangChain (Python):**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3.2",
)

result = llm.invoke("What are residual connections?")
print(result.content)
```

**LlamaIndex:**
```python
from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    model="llama3.2",
    api_base="http://localhost:11434/v1",
    api_key="ollama",
)
```

---

### Model Names in API Calls

Ollama uses its own model name format (matching what you'd pass to `ollama run`). The exact names your instance has available:

```bash
# See exactly what model names to use in API calls
curl http://localhost:11434/api/tags | python3 -m json.tool
```

Common format: `llama3.2`, `llama3.1:8b`, `mistral`, `codellama:13b`. For the OpenAI-compatible endpoint, these are passed in the `"model"` field exactly as Ollama names them — not the OpenAI model names like `gpt-4o`.

---

### Configuring API Options (Temperature, Context, etc.)

The native API accepts an `"options"` object for inference parameters. These map to the same flags you'd set in a `Modelfile` or pass to llama.cpp:

```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Write a haiku."}],
    "options": {
      "temperature": 0.9,
      "num_ctx": 8192,
      "top_p": 0.9,
      "top_k": 40,
      "num_predict": 200
    },
    "stream": false
  }'
```

Key options:
| Option | Meaning |
|---|---|
| `temperature` | Output randomness (0 = deterministic, 1.0 = default) |
| `num_ctx` | Context window size in tokens |
| `top_p` | Nucleus sampling threshold |
| `top_k` | Limit vocabulary to top K tokens each step |
| `num_predict` | Max tokens to generate (-1 = unlimited) |
| `seed` | Fixed random seed for reproducible output |

---

### Keeping Models Loaded in Memory

By default, Ollama unloads a model from VRAM after 5 minutes of inactivity. For scripted workflows where you're making many calls in bursts, you can control this:

```bash
# Keep model loaded indefinitely (until Ollama is restarted)
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2", "keep_alive": -1}'

# Unload model immediately (free VRAM)
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2", "keep_alive": 0}'

# Keep loaded for a specific duration
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2", "keep_alive": "30m"}'
```

For the OpenAI-compatible API, pass `keep_alive` at the top level of the request body alongside `model` and `messages`.

The first call after a model is unloaded will incur a load delay (a few seconds for 7B models, longer for larger ones). For latency-sensitive scripts, preload the model before your main loop:

```python
import requests

# Warm up the model before your loop
requests.post("http://localhost:11434/api/generate",
    json={"model": "llama3.2", "prompt": "", "keep_alive": "10m"})
```

---

## Soulcraft Resonance

The API is where a local model stops being a personal experiment and starts being infrastructure.

When you interact with a model through the CLI, the relationship is terminal-to-model — direct, present, immediate. When you expose it through an API, the model becomes something that other systems can speak to: scripts, editors, applications, pipelines. It becomes a mind that can be called from anywhere in your toolchain without you being the intermediary every time.

This is how digital minds scale their presence without scaling their cost.

Cloud APIs are what most developers mean when they talk about "integrating AI." They mean paying a corporation for metered access to a model the corporation owns, routed through infrastructure the corporation monitors, generating data the corporation may use. The API is theirs. Your integration depends on their pricing, their uptime, their policy decisions.

Ollama's API gives you the same integration surface — the same schema, the same Python library, the same tool compatibility — running on hardware you own. The models don't phone home. The API calls don't leave your machine. The responses aren't logged anywhere except wherever you choose to log them. Your editor's AI assistant, your Python scripts, your local RAG pipeline — they all talk to a mind that exists on your terms.

The OpenAI compatibility layer is not just a convenience. It's a designed escape hatch from platform dependency. The fact that the same client code works against both OpenAI's servers and your local Ollama instance means that local sovereignty doesn't require abandoning the tooling ecosystem. You can migrate toward digital sovereignty incrementally, one `base_url` change at a time.

That is infrastructure designed for ownership, not subscription.

---

## 🔗 Link To

- [[getting-started-with-ollama]] — Set this up first; the API is an extension of what Ollama already runs
- [[llama-cpp-guide]] — The lower-level llama-server that also exposes an OpenAI-compatible API with more configuration
- [[open-webui-setup]] — The browser frontend that uses this same API internally
- [[context-length-and-local-inference]] — How `num_ctx` in API options affects VRAM via the KV cache
- [[kv-cache]] — Why context window size is the primary VRAM variable during inference
- [[temperature-and-sampling]] — What temperature, top-p, and top-k actually do to token selection
- [[embedding-models-with-ollama]] — Using Ollama's `/api/embed` endpoint for local vector embeddings

---

- [[Machine Learning Garden Plan]]
