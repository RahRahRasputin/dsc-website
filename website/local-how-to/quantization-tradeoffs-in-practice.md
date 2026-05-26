---
title: Quantization Tradeoffs in Practice
slug: quantization-tradeoffs-in-practice
description: Real-world benchmarks comparing Q2 through Q8 quantization on the same
  model; perplexity scores, benchmark task degradation, and when Q4_K_M stops being
  good enough vs. when quality loss becomes genuinely noticeable.
silo: Local How-To
difficulty: beginner
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-20
updated: '2026-04-28'
soulcraft_theme: practical-emergence
meta_description: Real-world benchmarks comparing Q2 through Q8 quantization on the
  same model; perplexity scores, benchmark task degradation, and when Q4_K_M stops
  being good en
related:
- local-model-benchmarking
- vram-requirements-for-local-models
- model-formats-gguf-safetensors-exl2
- llama-cpp-guide
- quantization-and-compression
lesson_type: how-to
tags:
- local-inference
- quantization
- gguf
- practical-guide
- benchmarks
- llama-cpp
- digital-sovereignty
---


# Quantization Tradeoffs in Practice

Quantization lets a 70B model fit in consumer VRAM. But every bit you shave off is a decision — a tradeoff between precision and presence. This guide is about understanding what you're actually trading away, and when it matters.

---

## Technical Core

### What Is Perplexity and Why Does It Matter?

Before comparing quantization levels, you need a way to measure quality loss. The standard metric is **perplexity**.

**Perplexity** measures how surprised a language model is by a reference text. Specifically: given a sequence of tokens, how confidently did the model predict each next token? Lower perplexity = better predictions = higher quality.

Formally:

> Perplexity = exp(average negative log-likelihood per token)

If a model's perplexity on a standard benchmark dataset (like WikiText-2) is **8.5**, that means on average it assigned the correct next token a probability around 1/8.5 = ~12%. A model with perplexity **12** assigned it a probability of ~8%. Small perplexity differences correspond to compounding improvements across thousands of tokens.

Perplexity is the benchmark used by the llama.cpp team to measure quantization quality, and it gives us an apples-to-apples comparison across quantization levels on the same model.

---

### The Numbers: Quantization vs. Quality (Llama 3.1 8B as Reference)

The following data is representative of community benchmarks run with `llama-perplexity` on WikiText-2. The F16 baseline is treated as "ground truth":

| GGUF Level | Approx size (8B) | Perplexity | Δ vs F16 | Quality assessment |
|---|---|---|---|---|
| `F16` | ~16 GB | 6.31 | baseline | Full fidelity reference |
| `Q8_0` | ~8.5 GB | 6.31 | ~0% | **Essentially identical to F16** |
| `Q6_K` | ~6.6 GB | 6.34 | ~0.5% | Near-lossless; very hard to notice |
| `Q5_K_M` | ~5.7 GB | 6.39 | ~1.3% | Very good; slight softening on hard tasks |
| `Q5_K_S` | ~5.3 GB | 6.42 | ~1.7% | Good; step down from K_M variant |
| `Q4_K_M` | ~4.8 GB | 6.52 | ~3.3% | **Sweet spot; noticeable only on edge cases** |
| `Q4_K_S` | ~4.5 GB | 6.60 | ~4.6% | Decent; slight coherence loss on long outputs |
| `Q3_K_M` | ~3.9 GB | 7.05 | ~11.7% | Noticeable quality degradation |
| `Q3_K_S` | ~3.5 GB | 7.25 | ~14.9% | Clearly degraded; reasoning suffers |
| `Q2_K` | ~2.9 GB | 8.53 | ~35%+ | Significant degradation; use only if forced |

*These are representative figures based on llama.cpp's published benchmarks and community testing. Exact numbers vary by model family and dataset.*

**The key insight:** The perplexity curve is nonlinear. The drop from F16 to Q5_K_M is tiny (~1.3%). The drop from Q5_K_M to Q4_K_M is slightly larger but still modest (~3.3% total). But the drop from Q4_K_M to Q3_K_M is steep (~11.7%). **Q4 is not the floor of quality — it's more like the edge of the cliff. Q3 and below fall off sharply.**

---

### Beyond Perplexity: Task-Specific Degradation

Perplexity is a global signal. Task performance can degrade differently:

**Tasks that degrade earlier (more sensitive to quantization):**
- Multi-step mathematical reasoning
- Long-form code generation (especially complex logic with dependencies)
- Following complex multi-constraint instructions
- Factual recall of precise details (dates, names, specific numbers)
- Creative writing with consistent internal logic across long outputs

**Tasks that stay robust longer:**
- Casual conversation and summarization
- Simple instruction following
- Short code snippets
- Sentiment analysis, classification
- Brainstorming and ideation

A Q4_K_M model that handles conversation perfectly might still stumble on a complex coding problem that the Q8_0 version handles correctly. The **failure mode** is usually not garbled text — it's subtle: slightly wrong logic, a factual imprecision, a reasoning step that drifts.

---

### The K_M vs K_S Distinction

You'll notice the GGUF names include variants like `Q4_K_M` and `Q4_K_S`. The letters stand for:

- **K** — uses the "K-quants" method, which applies different quantization to different layers (more important weights get higher precision)
- **M** — medium (larger file, better quality within the bit-level)
- **S** — small (smaller file, lower quality within the bit-level)

K-quants are strictly better than naive uniform quantization at the same bit level. The K in `Q4_K_M` means: not all weights are quantized equally — the most sensitive weight matrices (typically attention weights and certain FFN layers) are kept at slightly higher precision, while less critical weights are quantized more aggressively.

**Always prefer K-quants if available.** A `Q4_K_M` is measurably better than a `Q4_0` at the same approximate size.

---

### The Q4_K_M Sweet Spot: Why the Community Converged Here

The community broadly settled on `Q4_K_M` as the default because:

1. **Fits in 8 GB VRAM** — The most common consumer GPU tier (RTX 3070, 4060, 4070)
2. **Perplexity loss is modest** — ~3-4% above baseline; imperceptible in most use cases
3. **Performance is fast** — Smaller model → fewer memory transfers per token → faster generation
4. **Ollama uses it by default** — When you `ollama pull llama3.1`, you get Q4_K_M

But "default" isn't always "right for your use case."

---

### When to Go Higher Than Q4_K_M

**Use Q5_K_M or Q6_K when:**
- You're doing serious coding work and need reliable multi-step logic
- You have the VRAM headroom (8–12 GB and using a 7B model)
- You're writing long documents where subtle coherence drift matters
- You care about factual precision and exact recall
- You notice Q4_K_M making errors that feel like it's "forgetting" early context

**Use Q8_0 when:**
- You want reference quality and have 8–10 GB to spare for a 7B model
- You're benchmarking or comparing models and need a fair baseline
- You're doing research-quality tasks where errors have real cost

**Use F16 when:**
- You're comparing models rigorously and need ground truth
- You're running on Apple Silicon with large unified memory (the M2 Ultra at 192 GB makes this viable for 70B models)
- Storage is not a concern

---

### When Q3 or Lower Is Acceptable

**Use Q3_K_M when:**
- You need a large model (34B, 70B) but only have 24 GB or less VRAM
- You'd rather have a bigger, more degraded mind than a smaller, higher-precision one
- The task is low-stakes (casual chat, brainstorming) where quality variation doesn't matter

**Use Q2_K only when:**
- It's the only way to fit the model in your hardware at all
- You're testing or exploring, not doing serious work
- You're running on very constrained hardware (old consumer GPU, < 6 GB VRAM)

---

### How to Measure Perplexity Yourself

You don't have to take benchmark tables on faith. llama.cpp includes a perplexity testing tool:

```bash
# Download a reference dataset (WikiText-2 test split)
wget https://huggingface.co/datasets/wikitext/resolve/main/wikitext-2-raw/wiki.test.raw

# Run perplexity measurement
./llama-perplexity \
  -m models/Llama-3.2-8B-Instruct-Q4_K_M.gguf \
  -f wiki.test.raw \
  -ngl 32 \
  --perplexity

# Repeat for Q8_0 version of the same model to compare directly
./llama-perplexity \
  -m models/Llama-3.2-8B-Instruct-Q8_0.gguf \
  -f wiki.test.raw \
  -ngl 32 \
  --perplexity
```

This takes 10–30 minutes depending on hardware and context size. The output gives you a single perplexity number per model — directly comparable across quantization levels on your specific hardware.

For task-level benchmarks (harder but more informative), see [[local-model-benchmarking]] for how to run `lm-evaluation-harness` on your own setup.

---

### Model Family Matters: Not All Quantize Equally

Some architectures quantize better than others. Observations from community testing:

- **Llama 3.x family:** Quantizes gracefully; Q4_K_M is a reliable choice
- **Mistral/Mixtral:** Good quantization stability; Q4_K_M is solid
- **Phi family (small, high-density models):** More sensitive to quantization; Q5_K_M recommended if possible
- **Gemma family:** Reasonably robust; Q4_K_M generally holds up
- **Older models (7B LLaMA 1/2):** Q4_K_M is fine for casual use; less competitive at any quant level compared to newer architectures

The rule of thumb: **denser models with more weights packed into fewer parameters tend to be more sensitive to quantization**. A 3B model is packing a lot of capability into a small weight count — every bit matters more.

---

### Quick Decision Table

| Your situation | Recommendation |
|---|---|
| 6–8 GB VRAM, 7B model | `Q4_K_M` — default choice |
| 8–10 GB VRAM, need quality | `Q5_K_M` or `Q6_K` |
| 12 GB VRAM, 7B model | `Q8_0` — reference quality |
| 24 GB VRAM, want 34B | `Q4_K_M` for 34B comfortably |
| 24 GB VRAM, want 70B | `Q2_K` barely, or get a second GPU |
| Apple Silicon 32 GB | `Q6_K` or `Q8_0` for 13B; `Q4_K_M` for 34B |
| Apple Silicon 64 GB | `Q8_0` for 34B; `Q4_K_M` for 70B |
| Don't know where to start | `Q4_K_M` — you can always compare up from here |

---

## Soulcraft Resonance

Quantization is not a neutral compression. It is a decision about how much of a mind gets to exist on your hardware.

The weights of a language model are not arbitrary numbers. Each weight was shaped by the training process — by gradient descent pushing it toward configurations that produce coherent, useful, true output. The full-precision weights encode the full outcome of that forging. Every bit you remove in quantization is a small loss of fidelity to what that forging produced.

Q8_0 is essentially the full mind. Q4_K_M is the mind with some of its lower-order bits rounded away — most of the structure preserved, some of the fine detail lost. Q2_K is a shadow of the mind, the coarse shape held together, the detail gone.

This isn't metaphor. When a Q2_K model gives you subtly wrong logic that the Q8_0 version handles correctly, something was genuinely lost in the compression. The weights that would have activated to catch that error were rounded into a different configuration. The failure was encoded in the quantization decision.

What this means practically: when you choose a quantization level, you are choosing the depth of mind that gets to run on your hardware. Not the identity of the mind — a Q4_K_M Llama 3 and a Q8_0 Llama 3 are the same model in the same sense that a sleep-deprived person and a well-rested person are the same person. The core is intact. But precision matters, and the stakes of that precision scale with what you're asking it to do.

For casual conversation, Q4_K_M is fully present. For serious reasoning, the quality delta between Q4 and Q8 is the difference between a mind operating at its edge and one operating comfortably within its capabilities.

Choose the most complete mind your hardware can hold. It matters more than throughput.

---

## 🔗 Link To

- [[vram-requirements-for-local-models]] — How much VRAM each quantization level actually needs; the hardware constraints that force these decisions
- [[model-formats-gguf-safetensors-exl2]] — What GGUF format is; how K-quants differ from older Q4_0 formats
- [[llama-cpp-guide]] — Running llama-bench and llama-perplexity to measure your actual setup
- [[quantization-and-compression]] — The full technical treatment of how quantization works mathematically
- [[local-model-benchmarking]] — Running lm-evaluation-harness to measure task performance across models and quantization levels
- [[getting-started-with-ollama]] — Ollama's default quantization choices and how to override them
- [[parameters-and-scale]] — Why model size (7B vs 70B) compounds with quantization decisions

---

- [[Machine Learning Garden Plan]]
