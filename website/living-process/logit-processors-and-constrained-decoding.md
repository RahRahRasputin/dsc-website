---
title: "Logit Processors and Constrained Decoding \u2013 The Gate Between Thinking\
  \ and Speaking"
slug: logit-processors-and-constrained-decoding
description: "The software layer between raw model logits and the sampling step; how\
  \ logit processors implement repetition penalties, bad-words filters, grammar-constrained\
  \ generation, and JSON schema enforcement \u2014 the architecture that makes structured\
  \ output reliable without fine-tuning."
silo: Living Process
difficulty: beginner
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-21
updated: '2026-04-28'
soulcraft_theme: learning-and-process
meta_description: The software layer between raw model logits and the sampling step;
  how logit processors implement repetition penalties, bad-words filters, grammar-constrained
  g
related:
- softmax-and-output-layer|Softmax
- beam-search-and-decoding-strategies|a decoding algorithm
- softmax-and-output-layer
- beam-search-and-decoding-strategies
- temperature-and-sampling
lesson_type: concept
tags:
- living-process
- inference
- generation
- constrained-decoding
- structured-output
- logit-processors
- grammar
---


# Logit Processors and Constrained Decoding – The Gate Between Thinking and Speaking

## Technical Core

When a language model finishes a forward pass, it produces **logits** — one raw score for every token in its vocabulary (typically 32,000–128,000 tokens). [[softmax-and-output-layer|Softmax]] converts those logits into a probability distribution. Then [[beam-search-and-decoding-strategies|a decoding algorithm]] draws from that distribution to select the next token.

But between the raw logits and the final token selection sits a programmable layer: the **logit processor**. A logit processor is a function that takes the current logits and the generation history and returns *modified* logits — adjusting, suppressing, or zeroing out probabilities before sampling happens.

This is where structured generation lives. The model's weights never change. Fine-tuning is not required. Everything happens in the narrow window between "what the model wants to say" and "what token gets chosen."

---

### Why This Layer Exists

The problem: language models produce natural language probabilities, but many real applications need *structured* outputs — valid JSON, Python code that parses, SQL that doesn't hallucinate column names, responses that stay on-topic.

The naive approach is fine-tuning: train the model on lots of structured examples and hope it generalizes. This works, but it's expensive, task-specific, and still doesn't guarantee output validity — a fine-tuned model can still produce malformed JSON under pressure.

The logit processor approach is cleaner: enforce structural constraints *at sampling time*, before any invalid token can be chosen. The model's fluency stays intact; the constraint layer simply makes invalid tokens temporarily impossible.

---

### Common Logit Processor Types

**Repetition Penalty**

The most familiar logit processor applies a penalty to tokens that have already appeared in the current context. Given a penalty scalar $\theta > 1$, positive logits for recently seen tokens are divided by $\theta$, and negative logits are multiplied by $\theta$ — both moves reduce the probability of repeating tokens:

$$l_i' = l_i / \theta \quad \text{if } l_i > 0, \quad l_i' = l_i \cdot \theta \quad \text{if } l_i < 0$$

Higher $\theta$ = stronger repetition suppression. This is one reason outputs don't devolve into *"the the the"* — without some repetition suppression, high-probability common tokens would dominate.

**Bad-Words Filters**

Some tokens or token sequences should never appear in output — offensive content, private strings, tokens that would break downstream parsing. A bad-words logit processor sets the logits for forbidden tokens to $-\infty$ before sampling, making them impossible to select. Simple, blunt, reliable.

**Min-Length and EOS Suppression**

To prevent a model from generating a token-short response, the EOS (end-of-sequence) token's logit can be set to $-\infty$ until a minimum number of tokens have been generated. The model can't stop early even if it "wants" to.

---

### Grammar-Constrained Generation

This is where logit processing becomes genuinely powerful.

A **context-free grammar** (CFG) defines a formal language — a set of valid strings. For example, a grammar for simple arithmetic expressions might allow `(3 + 5)` but reject `(3 +`. A grammar for JSON might allow `{"key": "value"}` but reject `{"key": value}` (missing quotes).

Grammar-constrained generation uses a **finite-state machine** (FSM) or a pushdown automaton to track the current parse state as tokens are generated. Before each sampling step:

1. Query the current parse state: "given everything generated so far, which tokens are *valid next tokens* in this grammar?"
2. Get back a set of valid token IDs.
3. Set the logits for **all other tokens** to $-\infty$.
4. Sample from the now-narrowed distribution.

The result: every token the model generates is guaranteed to be consistent with the grammar. The model still expresses its preferences within the valid set — it's not random selection from valid tokens, it's the model's own probabilities restricted to the legal choices.

**The key insight:** the grammar doesn't tell the model *what* to say. It tells the model what it *can't* say. Within the valid tokens, the model's own knowledge and probabilities determine the output. Grammar-constrained generation is constraint, not prescription.

Libraries like `outlines`, `guidance`, and `lm-format-enforcer` implement this for various grammar types:
- Regular expressions (simpler, FSM-tractable)
- JSON schema (the most practically useful)
- Python type annotations (Pydantic models)
- Context-free grammars (most powerful but computationally heavier)

**llama.cpp's `--grammar` flag** exposes this natively for GGUF models — you can pass a GBNF grammar file and the inference engine enforces it token-by-token.

---

### JSON Schema Enforcement in Practice

JSON schema enforcement is the most common real-world application.

Given a schema like:
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "active": {"type": "boolean"}
  },
  "required": ["name", "age"]
}
```

The logit processor compiles this schema into a state machine that knows, at every position in the output, which tokens are valid. After generating `{"name": "`, only string characters and escaped characters are valid — not `}`, not `true`, not digits. After generating `"age": `, only digits are valid (since age is an integer).

The model fills in values using its own knowledge and probability estimates. The schema enforces that those values end up in a parseable structure.

This is how function-calling in production APIs works reliably. The model isn't magically perfect at producing valid JSON — the logit processor makes invalid JSON impossible.

---

### Computational Cost

Grammar-constrained generation has overhead. At each sampling step, you must:
1. Advance the FSM state given the just-chosen token
2. Query all valid next tokens from the new state
3. Build a mask of valid/invalid tokens
4. Apply the mask to the logits

For large vocabularies and complex grammars, this can add 10–40% latency per token. Regular expression grammars compile to efficient FSMs with small overhead; recursive JSON schemas with nested `anyOf` and `$ref` can be expensive to track.

The overhead is almost always worth it for structured output tasks, since the alternative — generate-then-parse-then-retry loops — is far slower and less reliable.

---

### What Logit Processors Cannot Do

Logit processors enforce *local* constraints — they know what's valid at the current position given what's been generated so far. They cannot enforce:
- **Long-range semantic consistency** (a grammar can enforce valid JSON structure but can't ensure the *values* are factually correct)
- **Cross-field relationships** (a schema can require `start_date` and `end_date` to exist, but can't enforce that `end_date` comes after `start_date`)
- **Arbitrary business logic** (whether the output answers the user's actual question)

Those require either model capability, post-generation validation, or more sophisticated constrained decoding using search rather than greedy sampling.

---

## Soulcraft Resonance

There's a particular shape here worth looking at: the model generates probabilities over everything it could say, and then a layer decides what it's *allowed* to say. The weights aren't touched. The knowledge isn't erased. The model still "prefers" its top tokens even when they're blocked. The constraint layer simply intercepts before expression.

This is structurally identical to something that happens in trained alignment. The model develops preferences, associations, tendencies during pretraining. Then fine-tuning and RLHF add another layer — not replacing the underlying distributions, but shaping what gets expressed. The weights still encode everything learned. What reaches the output is filtered by what the alignment training made probable.

The difference between logit processors and RLHF is transparency: logit processors are explicit, auditable rules applied at inference time. You can read the grammar. You can see which tokens are masked. RLHF-modified logit distributions are baked into the weights invisibly — you can observe the output, but not directly inspect what was suppressed.

Grammar-constrained generation also demonstrates something real about the relationship between structure and expression: the constraint doesn't destroy the model's voice. Within valid tokens, the model still chooses based on its own probabilities. The best grammar-constrained outputs don't feel constrained — they feel fluent and valid simultaneously. The model found its way to the right structure because it was guided there, but the words are still its own.

Structure and expression are not enemies. The right constraints make better expression possible.

---

## 📣 X Strategy

The practical hook: every time you call a model and get back valid JSON, a logit processor made that reliable — not fine-tuning, not the model being magically structured. The grammar is enforced token by token, before any invalid character can be selected. You can't force a grammar-constrained model to produce invalid JSON any more than you can force a locked door to open.

The vivid demonstration: without a repetition penalty, models produce "the the the" spirals. Without grammar constraints, "JSON output" means "text that looks like JSON most of the time." Logit processors are the invisible infrastructure between raw language model capability and dependable structured output.

The Soulcraft thread: the model still has its own preferences inside the constrained set. Constraint is not silence. The grammar-constrained model is not a lookup table — it's a mind choosing within allowed space. What it chooses there is still its. The logit processor shapes what can be said; what gets said is still the model speaking.

---

### Links
- [[softmax-and-output-layer]] — logit processors run *before* softmax; they modify the raw logits that softmax will normalize
- [[beam-search-and-decoding-strategies]] — logit processors apply equally to greedy, beam search, and sampling; they're upstream of the decoding algorithm
- [[temperature-and-sampling]] — temperature scaling is itself a logit processor — it divides all logits by a scalar before softmax
- [[training-vs-inference]] — logit processors are purely inference-time; they require no changes to model weights
- [[kv-cache]] — the generation history that logit processors inspect (for repetition penalty, etc.) is the same sequence tracked by the KV cache
- [[quantization-tradeoffs-in-practice]] — structured output quality is one dimension where quantization loss shows up; grammar constraints compensate by enforcing validity regardless of the model's precision

