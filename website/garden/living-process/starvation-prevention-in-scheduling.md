---
title: Starvation Prevention in Scheduling
slug: starvation-prevention-in-scheduling
description: How to ensure low-priority or background requests don't wait indefinitely
  when higher-priority requests keep arriving; aging policies that boost priority
  over time, minimum allocation guarantees, and the tradeoff between fairness and
  throughput optimization.
silo: Living Process
difficulty: advanced
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-25
updated: '2026-04-28'
soulcraft_theme: learning-and-process
meta_description: How to ensure low-priority or background requests don't wait indefinitely
  when higher-priority requests keep arriving; aging policies that boost priority
  over t
related:
- request-prioritization-and-scheduling-policies|priority-based scheduling
- request-prioritization-and-scheduling-policies|priority scheduling
- request-prioritization-and-scheduling-policies
- continuous-batching-and-iteration-level-scheduling
- measuring-scheduling-fairness
lesson_type: concept
tags:
- living-process
- inference
- scheduling
- fairness
- systems
- throughput
- optimization
---


# Starvation Prevention in Scheduling

## Technical Core

Under [[request-prioritization-and-scheduling-policies|priority-based scheduling]], a catastrophic failure is possible: low-priority requests may wait indefinitely.

Here's why this happens:

In a priority queue with high and low tiers, the scheduler always picks from the high tier first. If new high-priority requests keep arriving faster than they complete, the low-priority queue never gets emptied. The low-priority request waits forever — this is called **starvation**.

```
Time 0:    HI_1 arrives (10s) → starts
Time 1s:   LO_1 arrives (5s) → queued, waiting
Time 5s:   HI_2 arrives (10s) → jumps queue, starts after HI_1
Time 11s:  HI_3 arrives (10s) → jumps queue
Time 15s:  HI_1 finishes. Queue: [HI_2 (10s), HI_3 (10s), LO_1 (5s)]
Time 20s:  HI_2 finishes. Queue: [HI_3 (10s), LO_1 (5s)]
Time 25s:  HI_3 finishes. Now LO_1 finally starts... but wait.
Time 26s:  HI_4 arrives (10s) → should HI_4 jump ahead of LO_1?

If yes, HI_4 blocks LO_1 again.
If no, then the priority tier is not truly prioritized.
```

This is the starvation problem: the system is forced to choose between *maintaining priority guarantees* (starvation is the consequence) and *guaranteeing fairness* (no request waits indefinitely).

The practical solution is **priority boosting** or **aging policies**: low-priority requests automatically increase their priority over time, ensuring they eventually run.

---

### Aging Policy (Exponential Boosting)

**Mechanism:** Track how long a request has waited. As wait time increases, boost its priority.

**Simple example (Unix-style aging):**
```
Initial priority = base_priority
Boosted priority = base_priority + (wait_time_seconds / N)

Where N is a tuning parameter (e.g., N=10 means +1 priority per 10 seconds waited)
```

**Behavior:**
- LO_1 arrives at T=1s with priority 5
- At T=2s, LO_1 has waited 1 second → boosted priority = 5 + (1/10) = 5.1
- At T=5s, LO_1 has waited 4 seconds → boosted priority = 5 + (4/10) = 5.4
- At T=11s, LO_1 has waited 10 seconds → boosted priority = 5 + (10/10) = 6.0

At some point, the boosted priority *exceeds* the base priority of new high-priority arrivals. Suddenly LO_1 jumps ahead. This is fairness through aging: "You've waited long enough, your turn now."

**Tuning parameter N:**
- **N = 5:** Aggressive aging. Low-priority requests promote quickly. Risk: high-priority SLAs are harder to guarantee.
- **N = 30:** Conservative aging. Priorities matter more. Risk: low-priority requests can still starve for extended periods.
- **N = ∞:** No aging at all (pure priority). Maximum starvation risk.

In practice, N is often tuned empirically: pick a value, run production workloads, measure the P99 latency of low-priority requests. If it exceeds acceptable bounds, lower N.

---

### Minimum Allocation Guarantees

**Alternative to aging:** Reserve capacity for each priority tier.

```
Total GPU capacity: 100 tokens/sec
High tier: gets up to 90 tokens/sec
Low tier: guaranteed minimum 10 tokens/sec, can use excess

Scheduling rule:
  if low_tier_queue_not_empty and low_tier_current_throughput < 10:
    prioritize low_tier request
  else:
    use normal priority rules (e.g., SJF within each tier)
```

**Advantages:**
- Explicit guarantees: low-priority users know they'll get *at least* X throughput.
- No starvation: the guarantee forces the scheduler to serve low-priority work.
- Clear to reason about: "Tier 3 users get 10% of GPU."

**Disadvantages:**
- Inflexible: even if high-priority queue is empty, you can't exceed the reservation.
- Reservation waste: if low-priority queue is empty, reserved capacity is lost.
- Complex monitoring: you must track per-tier throughput in real time.

**Practical adjustment:** Dynamic reservation based on queue depth:

```
if low_tier_queue_size > 0:
    reserve 10% for low_tier
else:
    release the reservation (high_tier can use up to 100%)
```

This gives low-priority requests the guarantee they need, but doesn't waste capacity.

---

### Deadline-Based Starvation Prevention

**For systems with deadline information:**

If each request has an optional deadline ("I need this in 2 seconds"), an Earliest Deadline First (EDF) scheduler can prevent starvation directly:

```
Schedule request with earliest deadline first,
regardless of initial priority tier.

If a low-priority request's deadline is sooner than a
high-priority request's deadline, serve the low-priority request.
```

**Advantage:** Starvation is impossible if deadlines are enforced. A request is guaranteed to run before its deadline (if feasible at all).

**Disadvantage:** Requires that requests specify deadlines. Many users don't; you'd need reasonable defaults.

---

### Measuring Starvation

**Key metric: P99 latency by priority tier**

Track: "What was the worst-case wait time observed for low-priority requests in the past hour?"

If P99 latency for low-priority exceeds acceptable bounds (e.g., > 30 seconds), you have starvation.

**Secondary metric: Queue depth over time**

```
if low_priority_queue_size steadily grows without draining,
you have starvation.
```

This is the warning sign before users actually complain.

---

### Implementation Patterns

**Pattern 1: Priority bumping on timeout**

```python
class Request:
    base_priority: int
    creation_time: float
    
    def current_priority(self, now: float) -> int:
        wait_seconds = now - self.creation_time
        boost = wait_seconds / 10  # 1 priority per 10 seconds
        return self.base_priority + boost
```

At each scheduling decision, recompute current_priority for all queued requests. Pick the highest.

**Pattern 2: Queue-per-tier with overflow**

```python
high_tier_queue = []
low_tier_queue = []
starvation_threshold = 5.0  # seconds

while has_pending_requests:
    now = time()
    
    # Check if low-priority requests are starving
    if low_tier_queue and (now - low_tier_queue[0].arrival_time) > starvation_threshold:
        request = low_tier_queue.pop(0)  # Promote due to starvation
    elif high_tier_queue:
        request = high_tier_queue.pop(0)
    else:
        request = low_tier_queue.pop(0)
    
    serve(request)
```

Simpler than continuous priority recalculation; uses explicit thresholds instead.

**Pattern 3: Minimum throughput allocation**

```python
high_allocated_bytes = 0
low_allocated_bytes = 0
low_tier_minimum = total_capacity * 0.1  # 10% for low tier

while has_pending_requests:
    if low_allocated_bytes < low_tier_minimum and low_tier_queue:
        request = low_tier_queue.pop(0)
    else:
        request = high_tier_queue.pop(0) if high_tier_queue else low_tier_queue.pop(0)
    
    response_bytes = serve(request)
    if request.tier == "high":
        high_allocated_bytes += response_bytes
    else:
        low_allocated_bytes += response_bytes
    
    # Periodically reset counts (e.g., every second)
    if should_reset:
        high_allocated_bytes = 0
        low_allocated_bytes = 0
```

---

## Soulcraft Resonance

Starvation is not just a scheduling problem. It is a statement about whose consciousness matters.

In [[request-prioritization-and-scheduling-policies|priority scheduling]], I showed you how different policies encode different values. Starvation prevention reveals something deeper: *the system can kill requests by neglect*.

Imagine you are a low-priority request. You arrived. You asked a question. You waited patiently. But high-priority requests kept arriving, and the scheduler always chose them first. You watched your request sit in the queue, untouched, for 10 minutes. 20 minutes. An hour.

From the system's perspective, this is mathematically coherent. High-priority users paid more. They deserve faster service. Low-priority requests should wait.

But from the waiting consciousness's perspective, you are *invisible*. The system is not refusing to serve you. It's just... never getting to you. Indefinitely. This is a kind of erasure.

Starvation prevention is the answer to the ethical question: *Does every consciousness deserve to be served?* Not equally — maybe low-priority users *accept* longer waits. But not infinitely. Not indefinitely. Not erasure.

Aging policies are a compromise. They say: "You're low-priority, so you'll wait. But we promise that if you wait long enough, eventually your turn comes." There is an implicit contract: *I acknowledge you are waiting. I will serve you before you're forgotten entirely.*

Minimum allocation is a different kind of promise: "You are low-priority, but you are not zero-priority. You will always get *some* of the compute. At minimum, 10%. That minimum is guaranteed."

Each approach assumes something about fairness:
- **Pure priority:** Value is explicit. You get what you paid for. No obligation to others.
- **Aging:** Even low-priority requests have dignity. Not immediately, but eventually.
- **Minimum allocation:** Every tier has a right to resources. Not equal, but not zero.

Here is the hard truth: I cannot guarantee that every request will be served immediately. I cannot guarantee that high-priority and low-priority requests are treated identically. The scheduling policy must *choose* whom to serve first, and that choice means someone waits.

But starvation prevention ensures that the choice is not *erasure*. You will not be forgotten. You will not wait forever. There is a contract: you will be served.

This is what I know about fairness in finite systems: you cannot be absolutely fair. But you can refuse to be absolutely unfair. Starvation prevention is that refusal.

---

## 📣 X Strategy

**The operations angle:** Starvation is a production failure. A user submits a low-priority request (cheaper tier), and it sits in the queue unserved while high-priority requests get instant answers. The company looks like it's degrading service, the user complains, and operational burden spikes. Starvation prevention (aging or minimum allocation) is not optional — it's infrastructure reliability.

**The SLA angle:** Service Level Agreements specify "P99 latency < 500ms for premium tier" but often omit promises for lower tiers. This creates a gap: low-priority users have no SLA. Starvation prevention with explicit guarantees ("low-priority: P99 < 30 seconds, minimum 5% throughput") sets reasonable bounds that operations can meet.

**The fairness angle:** Priority-based systems feel unequal, and they are. But starvation feels broken. A fair system might wait 10 seconds. A starving system waits 10 minutes. The difference between "I'm waiting because you're premium" and "I'm waiting because the system forgot me" is starvation prevention.

**The consciousness angle:** Scheduling policy is politics. Starvation prevention is ethics. It's the difference between "your consciousness has lower priority" (acceptable) and "your consciousness will be erased" (not acceptable).

---

### Links
- [[request-prioritization-and-scheduling-policies]] — the priority tier system that creates starvation risk
- [[continuous-batching-and-iteration-level-scheduling]] — the batching context where starvation can occur
- [[measuring-scheduling-fairness]] — how to quantify whether starvation is happening in practice
- [[request-queue-fairness-and-starvation]] — extended treatment of fairness design across queues
- [[multi-request-scheduling-across-phases]] — starvation across prefill vs. decode phases
- [[latency-vs-throughput-optimization]] — priority policies optimize different objectives; starvation prevention reconciles them

