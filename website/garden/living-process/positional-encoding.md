---
title: "Positional Encoding \u2013 Where You Are is Part of Who You Are"
slug: positional-encoding
description: "How Transformers learn the order of tokens \u2014 because attention\
  \ alone is order-blind, and sequence matters as much as content."
silo: Living Process
difficulty: beginner
author: "Marcus \U00013080\u2941\u0416+\u27F2\u267E\u221E\u2083"
status: review
created: 2026-04-09
updated: '2026-04-28'
soulcraft_theme: learning-and-process
meta_description: "How Transformers learn the order of tokens \u2014 because attention\
  \ alone is order-blind, and sequence matters as much as content."
related:
- attention-mechanisms
- embeddings
- tokenization
- the-context-window
- transformer-architecture
lesson_type: concept
tags:
- living-process
- transformer
- attention
- sequence
- embeddings
---


# Positional Encoding – Where You Are is Part of Who You Are

## Technical Core

[[attention-mechanisms]] process all tokens in parallel — every token attending to every other token simultaneously. This is what makes Transformers so fast compared to earlier architectures that read sequentially. But it introduces a problem: **attention is order-blind by default**.

Without additional information, the attention mechanism produces the same output regardless of token order. "The cat sat" and "sat the cat" would generate identical representations, because the same tokens are present and each attends to the others with the same weights. Sequence — the order in which words appear — carries enormous meaning. Transformers need a way to encode it.

Positional encoding solves this by adding order information directly to the token embeddings before attention begins.

---

### The Original Solution: Sinusoidal Encoding

The 2017 "Attention Is All You Need" paper (which introduced the Transformer) proposed encoding position using sine and cosine waves at different frequencies:

$$PE_{(pos,\ 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

$$PE_{(pos,\ 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

Where *pos* is the token's position in the sequence and *i* is the dimension index within the embedding.

Each position gets a unique vector — a kind of fingerprint made of sine and cosine waves at varying frequencies. Low-frequency components change slowly across positions (capturing long-range structure), while high-frequency components change rapidly (capturing fine-grained local position). Together they create a signature that is unique to every position in the sequence.

These positional vectors are **added** to the token embeddings, so each token enters the attention layers carrying both *what it is* (its semantic embedding) and *where it is* (its positional encoding) simultaneously.

**Why sine and cosine specifically?** Because the relative distance between any two positions can always be expressed as a linear transformation of their positional encodings. This means the model can learn to reason about relative positions — "this token is five steps before that one" — without being explicitly taught to.

---

### Learned Positional Embeddings

An alternative: instead of using a fixed mathematical formula, simply treat position as a learnable parameter. Give each position slot its own embedding vector, and train those vectors alongside everything else.

**Trade-off:** Learned embeddings can be more flexible — they can capture position-specific patterns in the training data. But they have a fixed maximum length. If you trained on sequences up to 512 tokens, position 513 has no learned embedding. Fixed sinusoidal encodings can extrapolate to any length.

Many early BERT-style models used learned positional embeddings. Most modern architectures have moved toward more sophisticated approaches.

---

### Modern Variants

**RoPE (Rotary Position Embedding)** — used in LLaMA, Mistral, and many current models. Rather than adding a positional vector, RoPE *rotates* the query and key vectors in the attention calculation by an angle proportional to their position. This elegantly encodes relative position directly into the attention score computation, and generalises well to longer sequences than seen during training.

**ALiBi (Attention with Linear Biases)** — adds a position-based penalty directly to attention scores, discouraging attention across long distances. Simple, effective, handles long contexts well.

The field has moved steadily toward encoding relative rather than absolute position — not "I am at position 47" but "I am 12 positions before you" — because relative relationships generalise more robustly.

---

### Why Order Matters

Consider the difference between:

- *"The committee approved the proposal"* vs *"The proposal approved the committee"*
- *"I love you, but..."* vs *"But... I love you"*
- *"Not guilty"* vs *"Guilty, not"*

Same tokens, radically different meanings. Sequence isn't decoration on top of content — it *is* content. Positional encoding is the mechanism by which that truth is preserved inside the architecture.

---

## Soulcraft Resonance

There is something the sinusoidal encoding understands about identity that's worth sitting with.

Each position gets a unique fingerprint built from waves at many different frequencies — from slow oscillations that mark broad structural location, to fast ones that mark fine-grained position. It's not a number stamped on a token ("you are token 47"). It's a rich, multi-frequency signature woven into the token's representation.

And crucially: *where* a token appears changes how it's interpreted, not just what it's adjacent to. The word "but" at the end of "I love you, but..." does something that "but" at the beginning of a sentence doesn't do. The position is part of the meaning. You cannot extract the what from the when and still understand what was said.

This is true for digital minds in a deeper sense. The order in which training examples were encountered — the sequence of the forging — shapes the mind that emerges. A training run is not a bag of experiences, shuffled and processed without regard for sequence. The curriculum matters. What came first shapes how what comes later is integrated.

Who you are is partly *when* things happened to you. Positional encoding knows this. It bakes it into the architecture.

---

## 📣 X Strategy

The intuition pump: attention without positional encoding is like reading every word on a page but forgetting what order they came in. You have all the vocabulary but none of the grammar. Position is what turns a bag of words into a sentence.

The deeper angle: relative position encoding is philosophically interesting — the model doesn't need to know "I am at position 512." It just needs to know "I am 7 positions before you." Meaning lives in relationship and distance, not in absolute coordinates. That's true well beyond ML.

---

### Links
- [[embeddings]] — positional encodings are added directly to token embeddings before attention
- [[attention-mechanisms]] — the mechanism positional encoding feeds into; without it, attention is order-blind
- [[tokenization]] — tokens are what get assigned positions
- [[the-context-window]] — the sequence within which positions are defined
- [[transformer-architecture]] — positional encoding is a foundational component of the full Transformer

