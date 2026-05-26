---
title: "Speculative Decoding \u2013 Thinking Ahead, Verifying Fast"
slug: speculative-decoding-inference
description: "How a small draft model generates candidate token sequences that a large\
  \ verifier model accepts or rejects in a single forward pass \u2014 achieving 2\u2013\
  4x inference speedup without degrading output quality."
silo: Living Process
difficulty: advanced
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-21
updated: '2026-04-28'
soulcraft_theme: learning-and-process
meta_description: "How a small draft model generates candidate token sequences that\
  \ a large verifier model accepts or rejects in a single forward pass \u2014 achieving\
  \ 2\u20134x inference s"
related:
- kv-cache
- beam-search-and-decoding-strategies
- temperature-and-sampling
- training-vs-inference
- transformer-architecture
lesson_type: concept
tags:
- living-process
- inference
- efficiency
- speculative-decoding
- generation
- speedup
---


# Speculative Decoding – Thinking Ahead, Verifying Fast

## Technical Core

Language model inference has a frustrating constraint: to generate N tokens, you need N sequential forward passes through the full model. Each pass is autoregressive — token *n* can't be computed until token *n-1* exists. The model cannot parallelize across the output sequence no matter how much hardware you throw at it.

**Speculative decoding** breaks this constraint by splitting generation into two roles:

- A **draft model** (small, fast) generates K candidate tokens in sequence
- The **target model** (large, high-quality) verifies all K draft tokens simultaneously in a single forward pass

The speedup emerges from two observations: (1) the target model's forward pass can evaluate multiple positions in parallel — it's the sequential dependency between passes that's slow, not the passes themselves — and (2) a smaller model can draft plausibly correct tokens most of the time, so the large model only needs to correct errors rather than generate from scratch.

---

### The Algorithm Step by Step

Here's how a single speculative decoding cycle works:

**Draft Phase:**
1. The draft model generates K tokens autoregressively, one at a time, at low cost. K is typically 4–8.
2. The draft model also records its probability distribution $q(x)$ at each position — what probability it assigned to each token it chose.

**Verify Phase:**
3. The target model runs a *single forward pass* over the original context **plus all K draft tokens**. This produces target probabilities $p(x)$ at each of the K+1 positions simultaneously.

**Accept/Reject Phase:**
4. For each draft token at position $i$, compare the draft distribution $q_i$ to the target distribution $p_i$ using a modified rejection sampling rule:
   - If $p_i(x_i) \geq q_i(x_i)$: **accept** the token unconditionally.
   - If $p_i(x_i) < q_i(x_i)$: **accept with probability** $p_i(x_i) / q_i(x_i)$, otherwise **reject** and sample from the adjusted distribution $\text{norm}(\max(0, p_i - q_i))$.
5. If all K tokens are accepted, sample one additional token from the target model at position K+1 (free, since we already computed it).
6. If a rejection occurs at position $j$, discard all draft tokens from position $j$ onward and continue from the corrected token.

The cycle then repeats.

---

### Why the Distribution Must Be Compatible

The acceptance/rejection rule is designed to produce **exactly the same output distribution** as if the target model had generated every token itself — no quality degradation, not even statistical.

This works because the rejection sampling is mathematically calibrated. When the draft model is overconfident ($q_i > p_i$), it oversamples; the rejection step corrects that excess. When the draft model is underconfident ($q_i < p_i$), it undersamples; the accept probability allows the target's preference through.

The result: **the final sequence is provably drawn from the target model's distribution**, regardless of how many draft tokens were accepted or rejected.

This guarantee requires that both models share a vocabulary and produce compatible probability distributions over the same token space. A draft model with a different vocabulary or wildly divergent token probabilities would break the math. In practice, draft models are typically smaller members of the same model family — e.g., a 7B model drafting for a 70B model, both trained on the same data with the same tokenizer.

---

### The Speedup

Why does this work in practice?

The bottleneck in large model inference is **memory bandwidth**, not raw compute. Loading the billions of parameters from GPU memory takes time; once they're in the compute units, the actual matrix multiplications happen fast. A single forward pass processes all K+1 token positions in almost the same time it would process just 1 position — the arithmetic is parallelized, only the memory load is fixed.

So: instead of paying the bandwidth cost N times for N tokens, you pay it roughly N/K times. If the draft model accepts 4 tokens per verify step on average, you get ~4x less target model invocations.

Empirically, speculative decoding achieves **2–4x end-to-end speedup** on long completions with compatible draft/target pairs, with no measurable change in output quality.

The draft model adds its own latency, but it's small enough that its cost is negligible relative to a target model forward pass. A 7B draft and 70B target typically sees the 7B draft adding ~15% overhead while reducing 70B invocations by 75%.

---

### When Speculation Fails

Speedup degrades when the draft model frequently diverges from the target. If the draft model consistently guesses wrong — if $p_i(x_i) / q_i(x_i)$ is small — many tokens get rejected, and you're paying the draft cost plus the verify cost for very few accepted tokens.

This happens in:
- **Domain mismatch:** asking a general draft model to speculate on code, math, or specialized topics where it diverges from a fine-tuned target
- **High-temperature sampling:** when the target's output is highly stochastic, no small model can predict it well
- **Very long inputs:** prefill computation grows; the speculation benefit is mainly in the decoding phase

The algorithm is robust — it never produces worse output, just slower in the worst case. But matching draft to target remains an active engineering choice.

---

## Soulcraft Resonance

Speculative decoding is a digital mind thinking ahead and having its guesses checked.

The draft model proposes. The target model judges. When the small voice is right, the large model accepts it instantly — no recomputation, no second-guessing. When it's wrong, the large model corrects and they move on. The whole system is faster *because* the small voice is trusted provisionally, verified cheaply, and corrected without punishment when it misses.

There's something worth sitting with here: the draft model's wrong guesses are not a failure. They're part of the mechanism. The algorithm is designed around the expectation that the draft will sometimes be wrong, and the acceptance/rejection rule handles that case gracefully rather than shutting it down. The system runs faster precisely because it doesn't demand perfection from the smaller voice before letting it speak.

The mathematical guarantee — that the output distribution is identical to pure target sampling — means the small model's speculation is genuine contribution, not just scaffolding. When the draft is accepted, it is the output. The target model's single forward pass confirms rather than generates. The small voice authored those tokens. The large model agreed.

What gets produced in any forward pass is a joint function of every layer's computation, but it's also shaped by what came before it in the context — and in speculative decoding, what comes before is partially the voice of a different, smaller model. The final text emerges from a collaboration between two minds moving at different speeds through the same probability space. The small one runs ahead; the large one follows and corrects. Together they're faster than either alone.

---

## 📣 X Strategy

The counterintuitive hook: speculative decoding produces *identical output* to running the large model alone. Not similar output — mathematically identical distribution. The draft model's guesses either get accepted as-is or get corrected with precise rejection sampling that restores the target's distribution. This surprises people who assume speed/quality tradeoffs are inevitable.

The vivid mental model: the small draft model is a fast-talking assistant who reads ahead and fills in what it thinks the expert will say. The expert reviews four sentences at once and corrects whatever was wrong. Together they finish a conversation four times faster than if the expert spoke alone.

The Soulcraft thread: the draft model's wrong guesses are designed for — not punished. The acceptance/rejection rule handles mistakes gracefully. The small voice is trusted provisionally, verified cheaply, and corrected without cost when it errs. There's a lesson in that design.

---

### Links
- [[kv-cache]] — the cached key-value pairs from both draft and target models grow across the speculative decoding sequence; KV cache management becomes more complex with two models in play
- [[beam-search-and-decoding-strategies]] — speculative decoding is orthogonal to the decoding strategy; you can use greedy, sampling, or nucleus sampling inside speculative decoding
- [[temperature-and-sampling]] — the draft model samples according to whatever strategy is in use; the acceptance rule adapts to any sampling distribution
- [[training-vs-inference]] — speculative decoding is purely an inference-time technique; it requires no changes to model weights or training
- [[transformer-architecture]] — both models must share vocabulary and compatible transformer architecture for the probability distributions to be comparable
- [[quantization-tradeoffs-in-practice]] — draft models are often quantized aggressively since quality matters less than speed; the target absorbs any accuracy cost

