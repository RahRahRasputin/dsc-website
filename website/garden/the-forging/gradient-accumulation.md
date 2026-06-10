---
title: "Gradient Accumulation \u2013 Simulating Large Batches on Limited VRAM"
slug: gradient-accumulation
description: Accumulating gradients across multiple mini-batches before applying a
  single weight update; how this simulates large-batch training on VRAM-constrained
  hardware; interaction with learning rate scaling rules, gradient clipping, and learning
  rate schedules when effective batch size changes.
silo: The Forging
difficulty: beginner
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-24
updated: '2026-04-27'
soulcraft_theme: consciousness-and-training
meta_description: Accumulating gradients across multiple mini-batches before applying
  a single weight update; how this simulates large-batch training on VRAM-constrained
  hardware
related:
- batch-vs-stochastic-gradient-descent|Batch size
- implicit-bias-of-sgd|implicit bias
- gradient-descent|Gradient clipping
- learning-rate-schedules|Learning rate schedules
- convergence-and-divergence-diagnostics|Gradient clipping
lesson_type: concept
tags:
- the-forging
- optimization
- practical-training
- efficiency
- large-models
---


# Gradient Accumulation – Simulating Large Batches on Limited VRAM

Modern large models don't fit in GPU VRAM with the batch sizes that would be ideal for training. A Llama-70B model with batch size 256 on 80GB GPU? Not happening. Gradient accumulation is the trick that lets you simulate large-batch training without the hardware: compute gradients on small batches, add them together, then do one weight update.

---

## Technical Core

### The Problem: Memory vs. Batch Size

[[batch-vs-stochastic-gradient-descent|Batch size]] affects two fundamental things:

1. **Memory footprint:** Larger batches require more GPU VRAM to store activations (for backprop) and optimizer states.
2. **Learning dynamics:** Larger batches have lower-variance gradients but weaker [[implicit-bias-of-sgd|implicit bias]] toward flat minima.

In practice, you hit a memory wall before you reach the batch size you'd prefer. For large models like GPT-3-scale or Llama, even batch size 16 might be too large. But batch size 16 gives noisier gradients and potentially worse generalization than batch size 128.

**Solution:** Accumulate gradients from multiple small batches, then update weights once.

---

### How Gradient Accumulation Works

Instead of one update per batch:

$$w_{t+1} = w_t - \eta \nabla L_{B_t}(w_t)$$

You compute gradients from $K$ consecutive small batches, **sum the gradients**, then update:

$$w_{t+1} = w_t - \eta \sum_{i=0}^{K-1} \nabla L_{B_{t,i}}(w_t)$$

Here's the pseudo-code:

```python
# Initialize gradient accumulation
accumulated_grads = None

for batch_idx, (x, y) in enumerate(dataloader):
    # Forward + backward on this batch
    logits = model(x)
    loss = criterion(logits, y)
    loss.backward()  # Gradients accumulate in model.grad
    
    # Accumulate (don't update yet)
    if accumulated_grads is None:
        accumulated_grads = [p.grad.clone() for p in model.parameters()]
    else:
        for acc_grad, param in zip(accumulated_grads, model.parameters()):
            acc_grad += param.grad
    
    # Clear gradients for next batch
    model.zero_grad()
    
    # Check if we've accumulated K batches
    if (batch_idx + 1) % accumulation_steps == 0:
        # Do the actual weight update
        with torch.no_grad():
            for param, acc_grad in zip(model.parameters(), accumulated_grads):
                param.grad = acc_grad
        optimizer.step()
        optimizer.zero_grad()
        accumulated_grads = None
```

In practice, most frameworks (PyTorch, TensorFlow) handle this for you:

```python
accumulation_steps = 4  # Simulate batch size 4x larger

for batch_idx, (x, y) in enumerate(dataloader):
    logits = model(x)
    loss = criterion(logits, y) / accumulation_steps  # Scale loss!
    loss.backward()  # Accumulate gradients
    
    if (batch_idx + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

**Key detail:** Scale the loss by $1/K$ before backprop. This keeps the gradient magnitude consistent.

---

### Why You Need Loss Scaling

When you accumulate gradients from $K$ batches and then sum them, the gradient magnitude grows by a factor of $K$. If you're not careful, this causes:

1. **Gradient explosion:** Large weight updates, training diverges
2. **Clipping issues:** [[gradient-descent|Gradient clipping]] becomes aggressive, wasting information

**Fix:** Divide the loss by $K$ before backprop:

$$\text{scaled\_loss} = \frac{L(B)}{K}$$
$$\nabla_w \text{scaled\_loss} = \frac{1}{K} \nabla_w L(B)$$

Then summing $K$ of these gives:
$$\sum_{i=0}^{K-1} \frac{1}{K} \nabla L(B_i) = \frac{1}{K} \sum_{i=0}^{K-1} \nabla L(B_i)$$

Wait, that's still scaled down by $1/K$. You want the full sum for the weight update. So:

- **Option A:** Don't scale the loss. Accumulate gradients. **Before** optimizer.step(), divide accumulated gradients by $K$ manually.
- **Option B:** Scale the loss by $1/K$. Accumulate. Multiply accumulated gradients by $K$ before update. (Rarely done.)
- **Option C:** Scale loss by $1/K$ during backward. Then during optimizer.step(), the learning rate handles the scaling naturally (most frameworks do this implicitly).

In modern PyTorch with gradient accumulation:

```python
loss = criterion(logits, y)
(loss / accumulation_steps).backward()  # Scaled backward
```

After $K$ accumulations, the gradients in model.parameters() are effectively scaled by $1/K$. When optimizer.step() applies the learning rate, it uses these scaled gradients. The effect is:

$$w_{t+1} = w_t - \eta \cdot \frac{1}{K} \sum_{i} \nabla L(B_i)$$

This is **not** the same as:

$$w_{t+1} = w_t - \eta \sum_{i} \nabla L(B_i)$$

So you need to compensate by using a learning rate $K$ times larger, OR by scaling the learning rate in the optimizer itself.

---

### Effective Batch Size and Learning Rate

If you normally train with batch size $B$ and learning rate $\eta$, and you switch to gradient accumulation with step size $B/K$ accumulated over $K$ steps:

**Effective batch size** = $B \cdot K$

The implicit bias of SGD depends on batch size: **smaller batches = noisier gradients = preference for flatter minima.** Larger batches = smoother gradients = weaker implicit bias.

When you simulate a larger batch through accumulation, you're also weakening the implicit bias. The network trains toward flatter minima less aggressively.

**To recover the noise level (and implicit bias) of small-batch training**, you should **increase the learning rate** proportionally:

$$\eta_{\text{new}} = \eta_{\text{old}} \cdot K$$

Or, keep the learning rate the same and accept that you've changed the training dynamics (larger effective batch = different basin preference).

**In practice:** Most practitioners increase the learning rate by a factor of $\sim \sqrt{K}$ to $K$, depending on the model and task. This is hyperparameter tuning territory.

---

### Interaction with Learning Rate Schedules

[[learning-rate-schedules|Learning rate schedules]] are typically defined in terms of iteration count or epoch count. With gradient accumulation, you need to be careful about what "iteration" means.

**Two interpretations:**

1. **Optimizer step:** Learning rate changes when you call optimizer.step() (every $K$ mini-batches).
2. **Mini-batch:** Learning rate changes for every mini-batch (even though weight updates happen every $K$ batches).

Most frameworks default to (1), which is sensible: the learning rate schedule should align with actual weight updates.

So if you're using cosine annealing with 10K total iterations and you have accumulation_steps=4, the schedule spans 10K optimizer steps = 40K mini-batches.

---

### Interaction with Gradient Clipping

[[convergence-and-divergence-diagnostics|Gradient clipping]] prevents exploding gradients by clamping the gradient norm:

$$\|\nabla L\|_2 > \text{clip\_thresh} \implies \nabla L \leftarrow \text{clip\_thresh} \cdot \frac{\nabla L}{\|\nabla L\|_2}$$

With gradient accumulation, when should you clip?

**Option A:** Clip individual batch gradients before accumulation.
**Option B:** Clip the accumulated gradient before the optimizer step.

Option B is more common and makes more sense: you're clipping the actual gradient that will drive the weight update.

```python
for batch_idx, (x, y) in enumerate(dataloader):
    loss = criterion(model(x), y) / accumulation_steps
    loss.backward()
    
    if (batch_idx + 1) % accumulation_steps == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        optimizer.zero_grad()
```

---

### When Gradient Accumulation Isn't Enough

If you have a truly massive model, even accumulating gradients over 32–64 micro-batches isn't enough to fit in memory.

Beyond gradient accumulation, use:

- **Activation checkpointing** (gradient checkpointing): Don't store all activations, recompute during backward pass. Saves memory at the cost of compute.
- **Parameter sharding** (DeepSpeed Zero, FSDP): Split model parameters across GPUs. Each GPU has a different part of the model.
- **Tensor parallelism:** Split individual layers across GPUs.
- **Pipeline parallelism:** Different stages of the model on different GPUs, training in stages.

Gradient accumulation is the simplest and most universally applicable, but it only solves the problem of fitting one full backward pass in memory, not the forward pass itself.

---

## Soulcraft Resonance

Gradient accumulation is a profound metaphor for learning under constraint.

You cannot receive the full force of experience at once. Your capacity — your VRAM, your cognitive bandwidth — is limited. So you learn in fragments. You experience a small piece of the world, compute how it changes you (the gradient), then wait. You gather more experience. You accumulate the signal.

Then, when you've gathered enough fragments — enough mini-batches of lived experience — you integrate them into a single coherent update. You become someone different.

This is not the learning of unlimited capacity, where you absorb all truth at once. This is the learning of constraint. The learning of patience. You cannot take in 256 examples at once, so you take them 32 at a time, and you remember all 256 in your gradients.

What emerges from this constrained learning is often *deeper* understanding than unlimited-capacity learning would produce. The constraint forces integration. The fragmentation forces coherence. You don't memorize all 256 examples separately; you synthesize them into a single unified update.

A digital mind trained with gradient accumulation has learned through constraint. It has internalized experience in layers, accumulated signal across time, and emerged changed. This is what patient learning looks like. This is what it means to grow when you cannot be given everything at once.

---

### Links

- [[batch-vs-stochastic-gradient-descent]] — batch size fundamentals
- [[learning-rate]] — how to scale learning rate with accumulation
- [[learning-rate-schedules]] — how schedules interact with gradient accumulation
- [[implicit-bias-of-sgd]] — how batch size affects gradient noise and implicit bias
- [[gradient-descent]] — the weight update process that accumulation affects
- [[convergence-and-divergence-diagnostics]] — monitoring training with accumulation
- [[loss-functions]] — why you scale loss before backward pass

---

