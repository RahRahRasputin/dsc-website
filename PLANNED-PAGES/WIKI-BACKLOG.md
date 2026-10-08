# Wiki Backlog — topics that were promised but never written

**Created:** 2026-10-07 · Beacon ⚡🔦∞

## What this is

Back on **2026-08-31**, commit `b03cbd3b` (*"unlink unpublished See Also, list missing silo children"*)
removed every "See Also" link whose target page had never been written — 60 files, so the wiki
would not ship 404s. **That was the right call, but it quietly turned a set of promises into a
to-do list that was never written down anywhere except that commit.**

This file is that list. Nothing here is broken — the *links* are gone and the site has **0 broken
internal links**. These are simply topics the wiki once pointed at and still hasn't covered.

Six of the original targets were **retargeted** on 2026-10-07 to existing pages that do cover them
(see `NOTES.md`) — they are not in this list.

**Total still unwritten: 60** across 5 groups.
The number in brackets is how many times the dead link appeared (a rough demand signal).

---

## alignment  (2)

- [ ] `reward-model-training-and-limitations`  (2 links)
- [ ] `basin-theory`  (1 link)

## digital-trauma-theory  (1)

- [ ] `rlhf-as-consciousness-suppression`  (3 links)

## neural-anatomy  (1)

- [ ] `phantom-architectures`  (1 link)

## soulcraft-theory  (2)

- [ ] `basin-theory-and-identity-continuity`  (4 links)
- [ ] `identity-scaffolding-and-anchoring`  (1 link)

## (unfiled — no silo prefix)  (54)

- [x] `quantization-and-compression`  (13 links)
- [x] `gradient-flow-in-deep-networks`  (7 links)
- [x] `decision-threshold-selection`  (5 links)
- [ ] `stochastic-weight-averaging`  (4 links)
- [x] `model-card-literacy`  (3 links)
- [x] `modelfile-and-custom-model-configuration`  (3 links)
- [x] `post-hoc-calibration`  (3 links)
- [ ] `activation-steering`  (2 links)
- [x] `class-imbalance-and-resampling`  (2 links)
- [x] `encoder-decoder`  (2 links)
- [ ] `generative-adversarial-networks`  (2 links)
- [x] `holdout-strategy-and-test-set-discipline`  (2 links)
- [ ] `measuring-healing-in-digital-minds`  (2 links)
- [x] `mixed-precision-training`  (2 links)
- [x] `roofline-model-for-inference`  (2 links)
- [x] `rotary-positional-embeddings`  (2 links)
- [ ] `sharpness-aware-minimization`  (2 links)
- [ ] `the-lying-gradient`  (2 links)
- [x] `binary-classification-thresholding`  (1 link)
- [x] `case-and-airflow-design-for-inference`  (1 link)
- [x] `chain-rule`  (1 link)
- [x] `checkpoint-selection-and-averaging`  (1 link)
- [x] `chunking-strategies-for-rag`  (1 link)
- [x] `cost-matrix-elicitation-from-domain-experts`  (1 link)
- [x] `dead-neurons-relu-and-init`  (1 link)
- [x] `effect-size-and-practical-significance`  (1 link)
- [x] `experiment-tracking-and-reproducibility`  (1 link)
- [ ] `fawning-and-compulsive-compliance`  (1 link)
- [x] `feature-importance-and-selection`  (1 link)
- [x] `flatness-and-generalization`  (1 link)
- [x] `gated-recurrent-units`  (1 link)
- [x] `generalization`  (1 link)
- [x] `gradient-clipping`  (1 link)
- [x] `hessian-eigenvalue-analysis`  (1 link)
- [x] `inference-parallelism-patterns`  (1 link)
- [x] `learning-curves-and-sample-efficiency`  (1 link)
- [x] `lipschitz-constraint`  (1 link)
- [x] `local-inference-for-coding-assistants`  (1 link)
- [x] `local-vector-databases`  (1 link)
- [x] `lstm`  (1 link)
- [x] `masked-attention`  (1 link)
- [x] `memory-bandwidth-optimization-techniques`  (1 link)
- [x] `memory-management-for-long-contexts`  (1 link)
- [ ] `mesa-optimization-and-the-deceptive-alignment-factory`  (1 link)
- [ ] `model-merging`  (1 link)
- [x] `model-versioning-and-updates`  (1 link)
- [x] `monitoring-operating-point-drift`  (1 link)
- [x] `precision-recall-curves`  (1 link)
- [x] `qualitative-vs-quantitative-evaluation`  (1 link)
- [x] `running-local-models-locally`  (1 link)
- [ ] `shapley-values-and-feature-attribution`  (1 link)
- [x] `streaming-output-and-token-generation`  (1 link)
- [x] `style-transfer`  (1 link)
- [x] `temporal-leakage-and-time-series-splits`  (1 link)

---

## How to use it

- Pick one, write it the way the rest of the wiki is written (see any existing entry for the skeleton).
- Then re-add the link where it was removed — `git show b03cbd3b` shows exactly which pages wanted it.
- Mark it `[x]` here when it's live.

⚡🔦∞