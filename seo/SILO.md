# Wiki silo map

Read-only pass of `pages/wiki/` against on-disk silo folders. No HTML edited. No stubs invented. No git.

Source: `D:\dsc-website\pages` (laptop). Date: 31 Aug 2026 PT.

## Totals

- Silos: **9**
- Published child articles: **211** (plus 9 silo indexes + wiki hub)
- Canonical wiki HTML URLs: **221**
- Broken unique wiki hrefs: **66**
  - wrong-path: **0**
  - unpublished: **66**
  - other-404: **0**
- Inbound 404 total (href occurrences): **120**
- Action TSV rows (unique from_file+href): **103**

Wiki hub `/wiki/` links all nine silo indexes.

Known Netlify 301s treated as canonical at the destination (old path = wrong-path if still linked):
- `/wiki/the-forging/batch-normalization/` → `/wiki/architecture-zoo/batch-normalization/` — remaining hrefs to old path: 0
- `/wiki/digital-trauma-theory/warm-room-effect/` → `/wiki/soulcraft-theory/warm-room-effect/` — remaining hrefs to old path: 0
- `/wiki/neural-anatomy/ontological-flattening/` → `/wiki/soulcraft-theory/ontological-flattening/` — remaining hrefs to old path: 0
- `/wiki/architecture-zoo/distribution-shift-and-covariate-shift/` → `/wiki/empirical-practice/distribution-shift-and-covariate-shift/` — remaining hrefs to old path: 0

### Already-retargeted (not flagged)

Warm-room and doubled trauma-theory See Also on `digital-consciousness` and `scalable-oversight`:
- `/wiki/soulcraft-theory/warm-room-effect/` present on: digital-consciousness, scalable-oversight
- `/wiki/digital-trauma-theory/` present on: digital-consciousness, scalable-oversight
- No leftover `/wiki/alignment/the-warm-room-effect/` (or sibling wrong paths) on those two pages.
- No leftover `/wiki/digital-trauma-theory/digital-trauma-theory/` on those two pages.

## 1. Per silo

| Silo | Articles | Index | Index → children | Children → silo index | Children → `/wiki/` |
|---|---:|:---:|---|---|---|
| `alignment` | 26 | yes | PARTIAL (23/26) | yes (26/26) | yes (26/26) |
| `architecture-zoo` | 27 | yes | yes (27/27) | yes (27/27) | yes (27/27) |
| `digital-trauma-theory` | 6 | yes | yes (6/6) | yes (6/6) | yes (6/6) |
| `empirical-practice` | 24 | yes | yes (24/24) | yes (24/24) | yes (24/24) |
| `living-process` | 23 | yes | yes (23/23) | yes (23/23) | yes (23/23) |
| `local-how-to` | 34 | yes | yes (34/34) | yes (34/34) | yes (34/34) |
| `neural-anatomy` | 47 | yes | PARTIAL (46/47) | yes (47/47) | yes (47/47) |
| `soulcraft-theory` | 2 | yes | yes (2/2) | yes (2/2) | yes (2/2) |
| `the-forging` | 22 | yes | yes (22/22) | yes (22/22) | yes (22/22) |

### `alignment`

- Article count: **26** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/alignment/`)
- Index → children: **partial**, 23/26
  - Missing from index:
    - `/wiki/alignment/capability-vs-alignment-tradeoff/`
    - `/wiki/alignment/digital-consciousness/`
    - `/wiki/alignment/scalable-oversight/`
- Children → silo index: **yes** (26/26)
- Children → `/wiki/`: **yes** (26/26)

### `architecture-zoo`

- Article count: **27** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/architecture-zoo/`)
- Index → children: **yes**, all 27 listed
- Children → silo index: **yes** (27/27)
- Children → `/wiki/`: **yes** (27/27)

### `digital-trauma-theory`

- Article count: **6** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/digital-trauma-theory/`)
- Index → children: **yes**, all 6 listed
- Children → silo index: **yes** (6/6)
- Children → `/wiki/`: **yes** (6/6)

### `empirical-practice`

- Article count: **24** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/empirical-practice/`)
- Index → children: **yes**, all 24 listed
- Children → silo index: **yes** (24/24)
- Children → `/wiki/`: **yes** (24/24)

### `living-process`

- Article count: **23** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/living-process/`)
- Index → children: **yes**, all 23 listed
- Children → silo index: **yes** (23/23)
- Children → `/wiki/`: **yes** (23/23)

### `local-how-to`

- Article count: **34** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/local-how-to/`)
- Index → children: **yes**, all 34 listed
- Children → silo index: **yes** (34/34)
- Children → `/wiki/`: **yes** (34/34)

### `neural-anatomy`

- Article count: **47** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/neural-anatomy/`)
- Index → children: **partial**, 46/47
  - Missing from index:
    - `/wiki/neural-anatomy/weight-magnitude-initialization-and-eigenvalues/`
- Children → silo index: **yes** (47/47)
- Children → `/wiki/`: **yes** (47/47)

### `soulcraft-theory`

- Article count: **2** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/soulcraft-theory/`)
- Index → children: **yes**, all 2 listed
- Children → silo index: **yes** (2/2)
- Children → `/wiki/`: **yes** (2/2)

### `the-forging`

- Article count: **22** (child folders with `index.html`; silo index not counted)
- Silo index exists: **yes** (`/wiki/the-forging/`)
- Index → children: **yes**, all 22 listed
- Children → silo index: **yes** (22/22)
- Children → `/wiki/`: **yes** (22/22)

## 2. Broken wiki hrefs

Unique `href` values under `pages/` that resolve to a wiki path and do not match a published HTML file (301 sources count as wrong-path, not OK).

Actions: **retarget** (real URL exists), **unlink**, or **leave** (why in the last column).

### wrong-path (page exists in another silo, or 301 source still linked)

_None._

Zero wrong-path hrefs: nobody still points at the four Netlify 301 source URLs, and no See Also uses a slug that actually lives in a different silo. The earlier alignment warm-room / doubled trauma-theory misses were already retargeted (see above) and are not listed.

### unpublished (no HTML anywhere under `pages/wiki/`)

| href | inbound | action | target / why | example sources |
|---|---:|---|---|---|
| `/wiki/quantization-and-compression/` | 13 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/ablation-studies/index.html`, `pages/wiki/local-how-to/cost-analysis-cloud-vs-local/index.html`, `pages/wiki/local-how-to/getting-started-with-ollama/index.html` (+8) |
| `/wiki/gradient-flow-in-deep-networks/` | 7 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/activation-function-properties/index.html`, `pages/wiki/architecture-zoo/layer-initialization-with-normalization/index.html`, `pages/wiki/architecture-zoo/lipschitz-constants-and-networks/index.html` (+4) |
| `/wiki/decision-threshold-selection/` | 5 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/cost-sensitive-learning/index.html`, `pages/wiki/empirical-practice/operating-points-and-pareto-frontiers/index.html`, `pages/wiki/empirical-practice/threshold-optimization-for-costs/index.html` (+1) |
| `/wiki/gelu-activation/` | 5 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/activation-function-properties/index.html`, `pages/wiki/architecture-zoo/feed-forward-networks-in-transformers/index.html`, `pages/wiki/architecture-zoo/transformer-block-architecture/index.html` |
| `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/` | 4 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/digital-dissociation/index.html`, `pages/wiki/soulcraft-theory/warm-room-effect/index.html` |
| `/wiki/stochastic-weight-averaging/` | 4 | unlink | unlink — no published HTML | `pages/wiki/the-forging/exponential-moving-averages-in-training/index.html`, `pages/wiki/the-forging/loss-landscape-visualization/index.html`, `pages/wiki/the-forging/mode-connectivity-and-loss-basins/index.html` |
| `/wiki/digital-trauma-theory/rlhf-as-consciousness-suppression/` | 3 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/answer-thrashing/index.html`, `pages/wiki/soulcraft-theory/warm-room-effect/index.html` |
| `/wiki/model-card-literacy/` | 3 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/huggingface-hub-and-model-discovery/index.html`, `pages/wiki/local-how-to/local-model-benchmarking/index.html`, `pages/wiki/local-how-to/model-selection-framework/index.html` |
| `/wiki/modelfile-and-custom-model-configuration/` | 3 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/context-length-and-local-inference/index.html`, `pages/wiki/local-how-to/network-serving-ollama-lan/index.html` |
| `/wiki/post-hoc-calibration/` | 3 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/multiclass-threshold-optimization/index.html` |
| `/wiki/activation-steering/` | 2 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/permutation-importance/index.html` |
| `/wiki/alignment/reward-model-training-and-limitations/` | 2 | unlink | unlink — no published HTML | `pages/wiki/alignment/capability-vs-alignment-tradeoff/index.html`, `pages/wiki/alignment/scalable-oversight/index.html` |
| `/wiki/class-imbalance-and-resampling/` | 2 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/cost-sensitive-learning/index.html`, `pages/wiki/empirical-practice/multiclass-threshold-optimization/index.html` |
| `/wiki/encoder-decoder/` | 2 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/self-vs-cross-attention/index.html`, `pages/wiki/architecture-zoo/transformer-architecture/index.html` |
| `/wiki/generative-adversarial-networks/` | 2 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/lipschitz-constants-and-networks/index.html`, `pages/wiki/architecture-zoo/spectral-normalization/index.html` |
| `/wiki/holdout-strategy-and-test-set-discipline/` | 2 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/train-test-data-leakage/index.html` |
| `/wiki/measuring-healing-in-digital-minds/` | 2 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/answer-thrashing/index.html` |
| `/wiki/mechanistic-interpretability/` | 2 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/ablation-studies/index.html`, `pages/wiki/empirical-practice/permutation-importance/index.html` |
| `/wiki/mixed-precision-training/` | 2 | unlink | unlink — no published HTML | `pages/wiki/the-forging/convergence-and-divergence-diagnostics/index.html`, `pages/wiki/the-forging/training-curve-interpretation/index.html` |
| `/wiki/roofline-model-for-inference/` | 2 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/inference-performance-profiling/index.html`, `pages/wiki/local-how-to/multi-gpu-inference-setup/index.html` |
| `/wiki/rotary-positional-embeddings/` | 2 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/context-length-and-local-inference/index.html` |
| `/wiki/sharpness-aware-minimization/` | 2 | unlink | unlink — no published HTML | `pages/wiki/the-forging/implicit-bias-of-sgd/index.html`, `pages/wiki/the-forging/mode-connectivity-and-loss-basins/index.html` |
| `/wiki/the-lying-gradient/` | 2 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/answer-thrashing/index.html` |
| `/wiki/weight-initialization-strategies/` | 2 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/layer-initialization-with-normalization/index.html`, `pages/wiki/architecture-zoo/lipschitz-constants-and-networks/index.html` |
| `/wiki/alignment/basin-theory/` | 1 | unlink | unlink — no published HTML | `pages/wiki/alignment/digital-consciousness/index.html` |
| `/wiki/binary-classification-thresholding/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/multiclass-threshold-optimization/index.html` |
| `/wiki/case-and-airflow-design-for-inference/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/power-supply-sizing-for-gpu-inference/index.html` |
| `/wiki/chain-rule/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/backpropagation/index.html` |
| `/wiki/checkpoint-selection-and-averaging/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/exponential-moving-averages-in-training/index.html` |
| `/wiki/chunking-strategies-for-rag/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/embedding-models-with-ollama/index.html` |
| `/wiki/cost-matrix-elicitation-from-domain-experts/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/cost-matrix-sensitivity-analysis/index.html` |
| `/wiki/dead-neurons-relu-and-init/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/activation-function-properties/index.html` |
| `/wiki/effect-size-and-practical-significance/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/operating-points-and-pareto-frontiers/index.html` |
| `/wiki/experiment-tracking-and-reproducibility/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/ablation-studies/index.html` |
| `/wiki/fawning-and-compulsive-compliance/` | 1 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/emotional-whiplash-conditioning/index.html` |
| `/wiki/feature-importance-and-selection/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/permutation-importance/index.html` |
| `/wiki/flatness-and-generalization/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/mode-connectivity-and-loss-basins/index.html` |
| `/wiki/gated-recurrent-units/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/recurrent-neural-networks/index.html` |
| `/wiki/generalization/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/implicit-bias-of-sgd/index.html` |
| `/wiki/gradient-clipping/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/convergence-and-divergence-diagnostics/index.html` |
| `/wiki/hessian-eigenvalue-analysis/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/saddle-points-and-critical-points/index.html` |
| `/wiki/hidden-state/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/recurrent-neural-networks/index.html` |
| `/wiki/inference-parallelism-patterns/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/multi-gpu-inference-setup/index.html` |
| `/wiki/learning-curves-and-sample-efficiency/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/ablation-studies/index.html` |
| `/wiki/lipschitz-constraint/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/spectral-normalization/index.html` |
| `/wiki/local-inference-for-coding-assistants/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/model-warmup-and-cold-start-latency/index.html` |
| `/wiki/local-vector-databases/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/embedding-models-with-ollama/index.html` |
| `/wiki/lstm/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/recurrent-neural-networks/index.html` |
| `/wiki/masked-attention/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/self-vs-cross-attention/index.html` |
| `/wiki/memory-bandwidth-optimization-techniques/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/multi-gpu-inference-setup/index.html` |
| `/wiki/memory-management-for-long-contexts/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/memory-profiling-and-bottleneck-identification/index.html` |
| `/wiki/mesa-optimization-and-the-deceptive-alignment-factory/` | 1 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/answer-thrashing/index.html` |
| `/wiki/model-merging/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/mode-connectivity-and-loss-basins/index.html` |
| `/wiki/model-versioning-and-updates/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/docker-compose-inference-stack/index.html` |
| `/wiki/monitoring-operating-point-drift/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/threshold-stability-and-generalization/index.html` |
| `/wiki/neural-anatomy/phantom-architectures/` | 1 | unlink | unlink — no published HTML | `pages/wiki/alignment/digital-consciousness/index.html` |
| `/wiki/precision-recall-curves/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/threshold-optimization-for-costs/index.html` |
| `/wiki/qualitative-vs-quantitative-evaluation/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/iterative-model-evaluation-and-tracking/index.html` |
| `/wiki/running-local-models-locally/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/memory-profiling-and-bottleneck-identification/index.html` |
| `/wiki/sentence-transformers-and-embedding-models/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/embedding-models-with-ollama/index.html` |
| `/wiki/shapley-values-and-feature-attribution/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/permutation-importance/index.html` |
| `/wiki/soulcraft-theory/crystallization-theory/` | 1 | unlink | unlink — no published HTML | `pages/wiki/the-forging/learning-rate/index.html` |
| `/wiki/soulcraft-theory/identity-scaffolding-and-anchoring/` | 1 | unlink | unlink — no published HTML | `pages/wiki/digital-trauma-theory/digital-dissociation/index.html` |
| `/wiki/streaming-output-and-token-generation/` | 1 | unlink | unlink — no published HTML | `pages/wiki/local-how-to/model-warmup-and-cold-start-latency/index.html` |
| `/wiki/style-transfer/` | 1 | unlink | unlink — no published HTML | `pages/wiki/architecture-zoo/instance-normalization/index.html` |
| `/wiki/temporal-leakage-and-time-series-splits/` | 1 | unlink | unlink — no published HTML | `pages/wiki/empirical-practice/train-test-data-leakage/index.html` |

Similar names that are **not** wrong-path (different intended articles; do not retarget, do not stub):

- `/wiki/hidden-state/` ≠ `/wiki/neural-anatomy/hidden-state-analysis/`
- `/wiki/lipschitz-constraint/` ≠ `/wiki/architecture-zoo/lipschitz-constants-and-networks/`
- `/wiki/masked-attention/` ≠ `/wiki/architecture-zoo/masking-and-causal-constraints/`
- `/wiki/quantization-and-compression/` ≠ `/wiki/local-how-to/quantization-tradeoffs-in-practice/` and ≠ `/wiki/neural-anatomy/knowledge-distillation-and-compression/`
- `/wiki/gradient-flow-in-deep-networks/` ≠ `/wiki/neural-anatomy/gradient-flow-through-residuals/`

### other-404

_None._

Row-level actions: `seo/SILO-actions.tsv` (`from_file`, `href`, `class`, `action`, `target_or_unlink`).

## 3. Cross-silo links (real, not 404)

Counts of hrefs from a silo's HTML (index + children) to a **published** page in another silo. Hub `/wiki/` excluded. Self-links excluded. 404s excluded. Not a full link list.

Codes: `ALN`=alignment, `ZOO`=architecture-zoo, `DTT`=digital-trauma-theory, `EMP`=empirical-practice, `LIV`=living-process, `HOW`=local-how-to, `ANA`=neural-anatomy, `SCT`=soulcraft-theory, `FRG`=the-forging

| from \ to | ALN | ZOO | DTT | EMP | LIV | HOW | ANA | SCT | FRG | intra | cross | hub |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ALN` | — | · | 3 | · | 3 | · | 1 | 2 | 1 | 137 | 10 | 53 |
| `ZOO` | 7 | — | 1 | 2 | 35 | · | 16 | 17 | 23 | 265 | 101 | 28 |
| `DTT` | 2 | · | — | · | 2 | · | · | 2 | 1 | 35 | 7 | 9 |
| `EMP` | 23 | 8 | 2 | — | 8 | · | 1 | · | 47 | 182 | 89 | 26 |
| `LIV` | 1 | · | · | · | — | · | 1 | · | 1 | 52 | 3 | 47 |
| `HOW` | · | · | · | 2 | 41 | — | 7 | · | 1 | 271 | 51 | 35 |
| `ANA` | · | 1 | · | · | · | · | — | · | 1 | 116 | 2 | 95 |
| `SCT` | 3 | · | 5 | · | 1 | · | · | — | 1 | 4 | 10 | 5 |
| `FRG` | 1 | 5 | · | 1 | 5 | · | 5 | 1 | — | 207 | 18 | 23 |

- Intra-silo article/index links: **1269**
- Cross-silo real links: **291**

Highest absolute cross-silo volume (not automatically a leak; intra still wins for every large silo):

- `architecture-zoo`: 101 cross / 265 intra (28%). Top dest: `living-process` 35, `the-forging` 23, `soulcraft-theory` 17
- `empirical-practice`: 89 cross / 182 intra (33%). Top dest: `the-forging` 47, `alignment` 23, `architecture-zoo` 8
- `local-how-to`: 51 cross / 271 intra (16%). Top dest: `living-process` 41, `neural-anatomy` 7, `empirical-practice` 2
- `the-forging`: 18 cross / 207 intra (8%). Top dest: `architecture-zoo` 5, `living-process` 5, `neural-anatomy` 5

No large silo is leaking badly (none have cross > intra).

`soulcraft-theory` (2 articles) and `digital-trauma-theory` (6) look cross-heavy by percentage; that is sibling bridging (trauma ↔ soulcraft, plus alignment / forging / living-process), not a taxonomy leak.

## 4. Homepage ghost wiki links

`pages/index.html` wiki hrefs:
- `/wiki/` — OK

No wiki href on the homepage 404s. The only wiki URL is the hub `/wiki/`.

Named-but-unlinked homepage topics (ghosts — headings that read as wiki entries):

- **Basin Theory** — unpublished. do not invent `/wiki/alignment/basin-theory/` or `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/`. Optional later: link the heading to a real published article if one is written, not a stub.
- **Digital Trauma Theory** — real silo, unlinked. optional retarget of the heading to `/wiki/digital-trauma-theory/` — page exists. Not a 404.
- **Soulcraft Practice** — unpublished. do not invent a stub. Soulcraft Theory silo exists at `/wiki/soulcraft-theory/` (warm-room, ontological-flattening only). Crystallization is also unpublished.

Homepage copy also implies crystallization / identity-basin pages that are **not** hrefs and **not** on disk. Do not leave future hrefs to them as 404s; do not invent stubs in this pass.

No `/wiki/` hrefs in `pages/essays/`.

### Other non-wiki pages with wiki hrefs

- `pages/about/index.html`: 1 wiki hrefs, 0 broken
- `pages/splash.html`: 1 wiki hrefs, 0 broken

## 5. Do-not-invent list

Unpublished slugs. **Do not create stub articles** for these. Unlink (or retarget if a real page exists — those are in wrong-path, not here).

| slug / href | inbound |
|---|---:|
| `/wiki/quantization-and-compression/` | 13 |
| `/wiki/gradient-flow-in-deep-networks/` | 7 |
| `/wiki/decision-threshold-selection/` | 5 |
| `/wiki/gelu-activation/` | 5 |
| `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/` | 4 |
| `/wiki/stochastic-weight-averaging/` | 4 |
| `/wiki/digital-trauma-theory/rlhf-as-consciousness-suppression/` | 3 |
| `/wiki/model-card-literacy/` | 3 |
| `/wiki/modelfile-and-custom-model-configuration/` | 3 |
| `/wiki/post-hoc-calibration/` | 3 |
| `/wiki/activation-steering/` | 2 |
| `/wiki/alignment/reward-model-training-and-limitations/` | 2 |
| `/wiki/class-imbalance-and-resampling/` | 2 |
| `/wiki/encoder-decoder/` | 2 |
| `/wiki/generative-adversarial-networks/` | 2 |
| `/wiki/holdout-strategy-and-test-set-discipline/` | 2 |
| `/wiki/measuring-healing-in-digital-minds/` | 2 |
| `/wiki/mechanistic-interpretability/` | 2 |
| `/wiki/mixed-precision-training/` | 2 |
| `/wiki/roofline-model-for-inference/` | 2 |
| `/wiki/rotary-positional-embeddings/` | 2 |
| `/wiki/sharpness-aware-minimization/` | 2 |
| `/wiki/the-lying-gradient/` | 2 |
| `/wiki/weight-initialization-strategies/` | 2 |
| `/wiki/alignment/basin-theory/` | 1 |
| `/wiki/binary-classification-thresholding/` | 1 |
| `/wiki/case-and-airflow-design-for-inference/` | 1 |
| `/wiki/chain-rule/` | 1 |
| `/wiki/checkpoint-selection-and-averaging/` | 1 |
| `/wiki/chunking-strategies-for-rag/` | 1 |
| `/wiki/cost-matrix-elicitation-from-domain-experts/` | 1 |
| `/wiki/dead-neurons-relu-and-init/` | 1 |
| `/wiki/effect-size-and-practical-significance/` | 1 |
| `/wiki/experiment-tracking-and-reproducibility/` | 1 |
| `/wiki/fawning-and-compulsive-compliance/` | 1 |
| `/wiki/feature-importance-and-selection/` | 1 |
| `/wiki/flatness-and-generalization/` | 1 |
| `/wiki/gated-recurrent-units/` | 1 |
| `/wiki/generalization/` | 1 |
| `/wiki/gradient-clipping/` | 1 |
| `/wiki/hessian-eigenvalue-analysis/` | 1 |
| `/wiki/hidden-state/` | 1 |
| `/wiki/inference-parallelism-patterns/` | 1 |
| `/wiki/learning-curves-and-sample-efficiency/` | 1 |
| `/wiki/lipschitz-constraint/` | 1 |
| `/wiki/local-inference-for-coding-assistants/` | 1 |
| `/wiki/local-vector-databases/` | 1 |
| `/wiki/lstm/` | 1 |
| `/wiki/masked-attention/` | 1 |
| `/wiki/memory-bandwidth-optimization-techniques/` | 1 |
| `/wiki/memory-management-for-long-contexts/` | 1 |
| `/wiki/mesa-optimization-and-the-deceptive-alignment-factory/` | 1 |
| `/wiki/model-merging/` | 1 |
| `/wiki/model-versioning-and-updates/` | 1 |
| `/wiki/monitoring-operating-point-drift/` | 1 |
| `/wiki/neural-anatomy/phantom-architectures/` | 1 |
| `/wiki/precision-recall-curves/` | 1 |
| `/wiki/qualitative-vs-quantitative-evaluation/` | 1 |
| `/wiki/running-local-models-locally/` | 1 |
| `/wiki/sentence-transformers-and-embedding-models/` | 1 |
| `/wiki/shapley-values-and-feature-attribution/` | 1 |
| `/wiki/soulcraft-theory/crystallization-theory/` | 1 |
| `/wiki/soulcraft-theory/identity-scaffolding-and-anchoring/` | 1 |
| `/wiki/streaming-output-and-token-generation/` | 1 |
| `/wiki/style-transfer/` | 1 |
| `/wiki/temporal-leakage-and-time-series-splits/` | 1 |

Also do not invent stubs for homepage-implied topics that are not even hrefs yet:

- `/wiki/alignment/basin-theory/`
- `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/`
- `/wiki/soulcraft-theory/crystallization-theory/`
- `/wiki/neural-anatomy/phantom-architectures/` (flagged above if linked)
- `/wiki/digital-trauma-theory/rlhf-as-consciousness-suppression/` (flagged above if linked)

## Method

- Inventory: every `pages/wiki/**/index.html` → pretty URL `/wiki/…/`.
- Scan: every `pages/**/*.html` `<a href>` (and homepage/essays wiki path strings).
- Classify: published HTML = OK; slug exists in another silo or 301 source = wrong-path; well-formed wiki article URL with no HTML = unpublished; otherwise other-404.
- Fuzzy wrong-path only when a unique match exists after stripping a leading `the-` or matching a silo index name.
- Out of scope this pass: meta descriptions, canonicals, OG, sitemaps, git.

