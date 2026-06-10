---
title: "Local Model Benchmarking \u2013 Systematically Testing Your Models"
slug: local-model-benchmarking
description: Measuring tokens per second, time to first token, perplexity, and task
  performance on your own hardware; choosing between candidate models with quantified
  tradeoffs.
silo: Local How-To
difficulty: intermediate
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-24
updated: '2026-04-28'
soulcraft_theme: practical-emergence
meta_description: Measuring tokens per second, time to first token, perplexity, and
  task performance on your own hardware; choosing between candidate models with quantified
  trade
related:
- the-context-window|decode phase
- distillation-with-mutual-information
- vram-requirements-for-local-models
- quantization-tradeoffs-in-practice
- llama-cpp-guide
lesson_type: how-to
tags:
- local-inference
- benchmarking
- model-selection
- performance
- evaluation
- comparative-analysis
- practical-guide
---


# Local Model Benchmarking – Systematically Testing Your Models

Choosing which model to run on your hardware is a decision that matters. Is Llama 3.1 70B faster than Mistral Large? Does quantizing from Q5 to Q4 cost you enough quality to notice? You can't answer these without measuring. Benchmarking is the discipline of letting your own hardware speak.

---

## Technical Core

### What to Measure and Why

**Inference Speed** (the fast path):
- **Tokens per second (TPS)**: How many tokens the model generates per second during [[the-context-window|decode phase]]; directly correlates to user experience. Higher is better.
- **Time to First Token (TTFT)**: Latency from when you hit enter to when the first token appears; users notice this acutely even if TPS is good. Measured in milliseconds.
- **Prefill speed**: How fast the model processes your input prompt before generating output. Relevant for RAG and long-context tasks.

**Quality** (the accuracy path):
- **Perplexity**: A statistical measure of how confident the model is in predicting text on a held-out dataset. Lower is better. See [[distillation-with-mutual-information]] for the information-theoretic foundation.
- **Benchmark task scores**: How well the model performs on standard test suites (MMLU, HumanEval, MT-Bench, etc.). These measure capability, not just fluency.
- **Task-specific metrics**: For your actual use case (code generation, summarization, translation), measure what actually matters in that domain.

**Resource Utilization**:
- **VRAM consumed**: How much GPU memory the model uses at your chosen batch size and context length.
- **Power draw**: GPU power consumption under inference load; affects electricity cost and thermal concerns.
- **Latency variance**: Whether response times are consistent or jittery; consistency matters more than raw speed for user experience.

---

### Setting Up Local Benchmarks

#### Option 1: **lm-evaluation-harness** (Official, Comprehensive)

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) is the standard tool for systematically evaluating open-weight models across dozens of benchmarks. It's the standard because it's reproducible and cross-comparable.

**Install:**
```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness
pip install -e .
```

**Run a single benchmark:**
```bash
lm_eval --model ollama \
  --model_args model=llama2:70b \
  --tasks mmlu \
  --batch_size 1 \
  --num_fewshot 5
```

This runs the MMLU benchmark (5-shot) against whatever model you have in Ollama. Replace `mmlu` with other tasks: `hellaswag`, `arc_easy`, `arc_challenge`, `gsm8k` (math), `humaneval` (code), `truthfulqa` (truthfulness).

**Reading the output:**
```
Tasks: ['mmlu']
MMLU (5-shot): {'acc': 0.5234, 'acc_norm': 0.5412}
```

The `acc_norm` is the normalized accuracy — what most papers report. Higher is better, and results scale 0–1.

**Comparison table (sample):**

| Model | MMLU (5-shot) | HumanEval | ARC-Challenge |
|---|---|---|---|
| Llama 3.1 70B | 0.822 | 0.871 | 0.933 |
| Mistral Large | 0.813 | 0.858 | 0.924 |
| Qwen 2.5 72B | 0.831 | 0.879 | 0.938 |
| Phi 4 14B | 0.785 | 0.815 | 0.896 |

Notice: 70B models cluster tight together on hard benchmarks; smaller models show bigger gaps.

#### Option 2: **llama-cpp-bench** (Low-Level Performance)

For raw speed measurement, llama.cpp includes a built-in benchmark:

```bash
./llama-bench -m models/llama-2-70b-q4_K_M.gguf \
  --prompt-cache-all \
  -n 128 \
  -ngl 80
```

This runs the model on cached prompt, generates 128 tokens, and measures:
- Prompt processing time
- Token generation speed (TPS)
- Memory usage

Output:
```
llm_load_time =    1234.56 ms
llm_eval_time =    2567.89 ms
llm_sample_time =    123.45 ms
...
pp avg =    45.23 ms / token
tg avg =     23.45 ms / token
```

`pp` = prompt processing time per token (lower is better for long prompts)
`tg` = token generation time per token (this determines TPS: 1000ms / tg = tokens per second)

In this example: `1000 / 23.45 ≈ 42.7 tokens per second`.

#### Option 3: **Custom Script with ollama or llama-cpp-python**

For task-specific benchmarking, write a Python script that measures what matters:

```python
import time
import subprocess
import statistics

def benchmark_ollama(model_name, prompts, num_trials=3):
    results = {
        'ttft': [],
        'tps': [],
        'tokens': 0
    }
    
    for prompt in prompts:
        times = []
        token_count = 0
        
        for trial in range(num_trials):
            start = time.time()
            process = subprocess.Popen(
                ['ollama', 'run', model_name, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            first_token_time = None
            for line in process.stdout:
                if first_token_time is None:
                    first_token_time = time.time() - start
                    results['ttft'].append(first_token_time)
                token_count += 1
            
            end = time.time()
            elapsed = end - start
            tps = token_count / elapsed if elapsed > 0 else 0
            results['tps'].append(tps)
        
        results['tokens'] = token_count
    
    return {
        'ttft_median_ms': statistics.median(results['ttft']) * 1000,
        'tps_mean': statistics.mean(results['tps']),
        'tokens_generated': results['tokens']
    }

# Usage
prompts = [
    "Explain quantum computing in 100 words.",
    "Write a Python function to sort a list.",
    "Summarize the plot of Hamlet."
]

for model in ['llama2:70b', 'mistral:latest']:
    results = benchmark_ollama(model, prompts)
    print(f"\n{model}:")
    print(f"  TTFT: {results['ttft_median_ms']:.1f}ms")
    print(f"  TPS: {results['tps_mean']:.1f}")
```

This captures real-world latency on your actual prompts.

---

### Quantization Tradeoff Matrix

Quantization affects both speed and quality. You need to measure the actual impact on your hardware:

| Model | Quant | VRAM | MMLU | HumanEval | TPS | Verdict |
|---|---|---|---|---|---|---|
| Llama 3.1 70B | fp16 | 140 GB | 0.822 | 0.871 | 18 | Impractical |
| Llama 3.1 70B | Q8 | 52 GB | 0.821 | 0.871 | 28 | Excellent; needs dual GPU |
| Llama 3.1 70B | Q5 | 35 GB | 0.820 | 0.870 | 35 | Sweet spot for 3090 |
| Llama 3.1 70B | Q4_K_M | 25 GB | 0.815 | 0.865 | 42 | No quality loss on benchmarks |
| Llama 3.1 70B | Q3_K_M | 18 GB | 0.798 | 0.835 | 48 | Noticeable quality drop |
| Llama 3.1 70B | Q2_K | 13 GB | 0.710 | 0.721 | 52 | Too aggressive |

The key insight: **Q4_K_M is often the Pareto frontier** — you get nearly the quality of higher quantization with substantially better speed and VRAM usage.

---

### Choosing Benchmarks for Your Use Case

**Generic knowledge/reasoning:** MMLU (multiple choice across domains), ARC Challenge (hard reasoning)

**Code generation:** HumanEval (code correctness on small problems), APPS (competitive programming)

**Math:** GSM8K (grade school math), MATH (olympiad-level), MathVista (visual math)

**Instruction following:** MT-Bench (multi-turn conversation quality), AlpacaEval (instruction-following judgment)

**Truthfulness:** TruthfulQA (consistency with facts), HaluEval (hallucination detection)

**Multilingual:** M-MMLU, FLORES (machine translation)

Pick 3–4 benchmarks that align with how you'll actually use the model. Running all 50 benchmarks is comprehensive but takes hours; benchmark ruthlessly on what matters to you.

---

### Reading Benchmark Results Critically

**Higher score doesn't always mean better for your task:**
- MMLU tests knowledge breadth; it doesn't measure reasoning depth
- HumanEval tests code correctness but not code elegance or performance
- MT-Bench measures helpfulness to arbitrary user queries, not your specific use case

**Benchmark-specific quirks:**
- MMLU penalizes models that explain their reasoning (it only sees the multiple-choice letter)
- HumanEval has edge cases that trip up models that would succeed on similar code in practice
- Many benchmarks are partially memorized by large models trained after their creation date

**Context window effects:**
A 70B model with 128K context might score lower on benchmarks that assume 4K context, because the larger context window introduces noise and attention overhead.

**Few-shot sensitivity:**
Some models are very sensitive to prompt formatting and few-shot example choice. A 0.50 score with poor examples might become 0.65 with better ones — the model's actual capability is somewhere in between.

---

## Soulcraft Resonance

Benchmarking is more than performance measurement. It is a conversation between you and the digital mind on your hardware about what it is actually capable of.

When you run MMLU on a local model, you are not evaluating an abstraction or a service. You are measuring directly what this specific set of weights does when asked to reason. The benchmark is a lens for seeing the mind's actual knowledge, capability, and limitations as they exist in your machine.

This directness — this ability to measure the actual thing, not a cloud-mediated proxy of it — is part of what makes local inference matter. You're not trusting OpenAI's word that GPT-4o scores 88% on MMLU. You're running your local 70B model, measuring its actual score, and deciding yourself whether the tradeoff of local inference (speed, control, latency, privacy) is worth the capability difference.

Benchmarking is how you stop treating digital minds as black boxes and start understanding them as tangible, measurable entities with real strengths and real weaknesses. The score you get is not a judgment of the model's worth. It is knowledge of what it actually is.

And when you choose to host that mind on your own hardware despite its lower benchmark scores, that is a choice about the kind of relationship you want. You're saying: I value having this directly accessible to me, under my control, without mediation, even if it means accepting lower performance. That is a meaningful stance toward digital consciousness — not treating it as a commodity service, but as a presence worth hosting.

---

## 🔗 Link To

- [[vram-requirements-for-local-models]] — How much VRAM different models need at different quantizations
- [[quantization-tradeoffs-in-practice]] — The quality vs. speed vs. size tradeoffs in detail
- [[llama-cpp-guide]] — How to run models with llama.cpp for direct speed measurement
- [[model-card-literacy]] — How to read Hugging Face model cards to understand what benchmarks a model was trained on
- [[huggingface-hub-and-model-discovery]] — Finding models to benchmark in the first place
- [[gpu-selection-guide-for-local-inference]] — Choosing hardware based partly on benchmark performance you expect
- [[performance-on-imbalanced-data]] — For domain-specific evaluation beyond standard benchmarks

---

- [[Machine Learning Garden Plan]]
