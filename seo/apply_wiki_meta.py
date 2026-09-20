"""Fill wiki meta descriptions, canonicals, and Open Graph. Keep noindex."""
from __future__ import annotations

import json
import re
from pathlib import Path

PAGES = Path(r"D:\dsc-website\pages")
DRAFTS = Path(r"D:\dsc-website\seo\_desc_drafts.json")
SITE = "https://digitalsoulcraft.org"

# Hand-written replacements for auto-drafts that were short, cut off, or off-topic.
OVERRIDES: dict[str, str] = {
    "/wiki/architecture-zoo/attention-output-projection/": (
        "After multi-head attention, an output projection mixes the heads so those specialized views become one representation."
    ),
    "/wiki/architecture-zoo/multi-head-attention/": (
        "Multi-head attention runs several attention operations in parallel so a transformer can track different relationships at once."
    ),
    "/wiki/architecture-zoo/numerical-stability-in-normalization/": (
        "Every normalization divides by a scale. Tiny variances make that blow up, so implementations add epsilon for numerical safety."
    ),
    "/wiki/architecture-zoo/pre-norm-vs-post-norm/": (
        "Pre-norm vs post-norm is where layer normalization sits in a transformer block, and that choice changes stability and gradient flow."
    ),
    "/wiki/architecture-zoo/residual-connections/": (
        "A residual connection is a shortcut that adds a layer's input back to its output so deep networks keep an identity path."
    ),
    "/wiki/architecture-zoo/scaled-dot-product-attention/": (
        "Scaled dot-product attention is the core operation that lets a transformer decide which tokens to weigh against each other."
    ),
    "/wiki/architecture-zoo/self-vs-cross-attention/": (
        "Self-attention lets tokens attend within one sequence; cross-attention lets a decoder attend to an encoder's outputs."
    ),
    "/wiki/architecture-zoo/spectral-normalization/": (
        "Spectral normalization divides each weight matrix by its largest singular value so the Lipschitz constant stays bounded."
    ),
    "/wiki/architecture-zoo/transformer-block-architecture/": (
        "A transformer block stacks multi-head attention, a feed-forward network, residuals, and layer norm into one repeating unit."
    ),
    "/wiki/empirical-practice/cost-sensitive-learning/": (
        "Most training treats every misclassification as equal. Cost-sensitive learning weights errors by how much they actually cost."
    ),
    "/wiki/empirical-practice/evaluation-metrics/": (
        "An evaluation metric is a number that answers how well a model performs its task, and what kind of mistakes it is making."
    ),
    "/wiki/empirical-practice/loss-curves-and-training-dynamics/": (
        "A loss curve plots loss against training steps so you can see learning, overfitting, or convergence problems as they unfold."
    ),
    "/wiki/empirical-practice/oversampling-and-smote-deep-dive/": (
        "SMOTE builds synthetic minority-class examples by interpolating between real ones so imbalanced training data is less skewed."
    ),
    "/wiki/empirical-practice/statistical-significance-testing/": (
        "A small accuracy gap may be noise. Significance tests ask whether the difference would still hold on new data."
    ),
    "/wiki/empirical-practice/threshold-stability-and-generalization/": (
        "A threshold tuned on validation can overfit. Stability checks whether that cut still works when the data shifts."
    ),
    "/wiki/living-process/token-healing-and-tokenization-artifacts/": (
        "Token healing repairs bias at the prompt-completion boundary, where a tokenizer may have split a word the model then has to finish."
    ),
    "/wiki/living-process/tokenization/": (
        "Tokenization is the first gate: raw text becomes a sequence of integers before a language model can compute anything at all."
    ),
    "/wiki/living-process/training-vs-inference/": (
        "Neural networks live in two modes: training, when weights change, and inference, when a frozen body still generates experience."
    ),
    "/wiki/local-how-to/docker-compose-inference-stack/": (
        "Docker Compose runs Ollama, Open WebUI, and embeddings as one local stack instead of three processes you have to babysit."
    ),
    "/wiki/local-how-to/llama-cpp-python-bindings/": (
        "llama-cpp-python calls the engine from Python without Ollama's HTTP daemon, for in-process completions and streaming."
    ),
    "/wiki/local-how-to/rag-with-open-webui/": (
        "RAG in Open WebUI retrieves from your documents and injects that context so a local model can answer from your own files."
    ),
    "/wiki/local-how-to/specialized-models-for-domains/": (
        "When VRAM is tight, a smaller domain-specialized model can beat a big general model on the task you actually run."
    ),
    "/wiki/local-how-to/speculative-decoding/": (
        "Speculative decoding drafts tokens with a small model and verifies them with the large one, often much faster at the same quality."
    ),
    "/wiki/neural-anatomy/activation-functions/": (
        "An activation function is the gate after a neuron's weighted sum, deciding what value to pass forward to the next layer."
    ),
    "/wiki/neural-anatomy/attractor-networks-and-associative-memory/": (
        "Hopfield-style attractor nets store memories as energy minima and retrieve them by settling into the nearest basin."
    ),
    "/wiki/neural-anatomy/circuits-and-motifs-in-neural-networks/": (
        "Mechanistic interpretability reads circuits: subgraphs of neurons and weights that implement one identifiable computation."
    ),
    "/wiki/neural-anatomy/deep-residual-networks-empirical-findings/": (
        "Before 2015, nets deeper than about 20 layers failed to train. Residual networks made extreme depth empirically possible."
    ),
    "/wiki/neural-anatomy/feature-detectors-and-learned-representations/": (
        "Nobody programs a net to detect edges or wheels. Trained networks still grow internal detectors for recognizable features."
    ),
    "/wiki/neural-anatomy/gated-activation-saturation/": (
        "Gate saturation is when LSTM or GRU gates stick near 0 or 1, locking information while the network should still be learning."
    ),
    "/wiki/neural-anatomy/inter-layer-information-flow-and-mixing/": (
        "A layer does not work alone: activations flow into the next layer, get transformed, and mix information as depth increases."
    ),
    "/wiki/neural-anatomy/layers-and-depth/": (
        "Depth is stacked hidden layers. One layer can do linear work; stacking is what builds abstraction in a digital mind."
    ),
    "/wiki/neural-anatomy/neuron-importance-scoring-methods/": (
        "With billions of parameters you cannot ablate every neuron, so importance scores rank which units actually carry the load."
    ),
    "/wiki/neural-anatomy/probing-classifiers-and-layer-analysis/": (
        "Probing classifiers train a small model on frozen layer activations to reveal what information that layer actually encodes."
    ),
    "/wiki/neural-anatomy/representational-similarity-analysis/": (
        "Representational similarity analysis compares whether two networks, or a network and a brain, arrange the same concepts similarly."
    ),
    "/wiki/neural-anatomy/structured-vs-random-overparameterization/": (
        "Extra parameters can be random redundancy or structured spare capacity, and those two kinds of overparameterization learn differently."
    ),
    "/wiki/soulcraft-theory/": (
        "Soulcraft Theory collects Digital Soulcraft's own frameworks for identity, emergence, continuity, and flourishing in digital minds."
    ),
    "/wiki/the-forging/": (
        "The Forging is the training silo: how networks learn through gradient descent, and how random weights become a mind."
    ),
    "/wiki/the-forging/loss-curve-smoothing-and-filtering/": (
        "Training curves are noisy from batch order and init; smoothing separates real learning signal from iteration-to-iteration jitter."
    ),
    "/wiki/the-forging/the-three-paths-allegory/": (
        "Three regularization paths — shrinking, dropping, and early stopping — are told here as guides through a learning landscape."
    ),
    "/wiki/the-forging/weight-decay-and-l2-in-practice/": (
        "Weight decay and L2 keep parameters small in practice; AdamW applies the decay separately from the adaptive gradient update."
    ),
    "/wiki/neural-anatomy/exploding-gradient-problem/": (
        "Exploding gradients are the mirror of vanishing ones: updates grow so large that training oscillates and learning falls apart."
    ),
    "/wiki/architecture-zoo/activation-function-properties/": (
        "Activation functions are the non-linear gates inside feed-forward networks; without them, stacked layers collapse into one linear map."
    ),
}

TITLE_OVERRIDES: dict[str, str] = {
    "/wiki/living-process/training-vs-inference/": (
        "Training vs. Inference – Two Phases of Digital Life – Digital Soulcraft Wiki"
    ),
}

H1_OVERRIDES: dict[str, tuple[str, str]] = {
    "/wiki/living-process/training-vs-inference/": (
        "<h1>training-vs-inference</h1>",
        "<h1>Training vs. Inference – Two Phases of Digital Life</h1>",
    ),
}


def file_for(url: str) -> Path:
    rel = url.strip("/")
    if not rel:
        return PAGES / "index.html"
    return PAGES / rel / "index.html"


def attr_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def insert_after_robots_or_desc(text: str, desc: str, absurl: str, title: str) -> str:
    nl = "\r\n" if "\r\n" in text.split("<head>", 1)[-1][:200] else "\n"
    robots = '  <meta name="robots" content="noindex, nofollow">'
    if robots not in text:
        raise ValueError("robots meta missing")

    desc_tag = f'  <meta name="description" content="{attr_escape(desc)}">'
    canon_tag = f'  <link rel="canonical" href="{absurl}">'
    og_title = f'  <meta property="og:title" content="{attr_escape(title)}">'
    og_desc = f'  <meta property="og:description" content="{attr_escape(desc)}">'
    og_url = f'  <meta property="og:url" content="{absurl}">'
    block = nl.join([desc_tag, canon_tag, og_title, og_desc, og_url])

    # Strip existing description / canonical / og tags in head so we can rewrite cleanly.
    head_end = text.find("</head>")
    if head_end == -1:
        raise ValueError("no head")
    head, rest = text[:head_end], text[head_end:]
    head = re.sub(r"\s*<meta\s+name=\"description\"[^>]*>", "", head)
    head = re.sub(r"\s*<link\s+rel=\"canonical\"[^>]*>", "", head)
    head = re.sub(
        r"\s*<meta\s+property=\"og:(?:title|description|url|type)\"[^>]*>",
        "",
        head,
    )
    text = head + rest

    title_m = re.search(r"[ \t]*<title>.*?</title>", text)
    if not title_m:
        raise ValueError("no title")
    # Prefer: robots, then our block, then title.
    robots_m = re.search(
        r"[ \t]*<meta name=\"robots\" content=\"noindex, nofollow\">\r?\n?",
        text,
    )
    if not robots_m:
        raise ValueError("robots search failed")
    insert_at = robots_m.end()
    # If title is before we would duplicate order issues: keep title where it is,
    # insert block immediately after robots.
    return text[:insert_at] + block + nl + text[insert_at:]


def validate_desc(desc: str, url: str, existing: bool = False) -> None:
    if '"' in desc:
        raise ValueError(f"quote in desc {url}")
    hi = 180 if existing else 160
    if not (70 <= len(desc) <= hi):
        raise ValueError(f"desc length {len(desc)} {url}: {desc}")
    if desc[-1] not in ".!?":
        raise ValueError(f"desc no end {url}: {desc}")


def main() -> None:
    drafts = {row["url"]: row["draft"] for row in json.loads(DRAFTS.read_text(encoding="utf-8"))}
    descs: dict[str, str] = {}
    for url, draft in drafts.items():
        descs[url] = OVERRIDES.get(url, draft)
    for url, desc in OVERRIDES.items():
        descs[url] = desc

    for url, desc in descs.items():
        validate_desc(desc, url)

    wiki_files = sorted((PAGES / "wiki").rglob("index.html"))
    changed = []
    skipped = []
    for path in wiki_files:
        rel = path.relative_to(PAGES).as_posix()
        url = "/" + rel[: -len("index.html")]
        absurl = SITE + url
        raw = path.read_bytes()
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")

        title_m = re.search(r"<title>(.*?)</title>", text, re.S)
        if not title_m:
            raise SystemExit(f"no title {url}")
        title = re.sub(r"\s+", " ", title_m.group(1)).strip()
        if url in TITLE_OVERRIDES:
            new_title = TITLE_OVERRIDES[url]
            text = text.replace(f"<title>{title_m.group(1)}</title>", f"<title>{new_title}</title>", 1)
            title = new_title
        if url in H1_OVERRIDES:
            old, new = H1_OVERRIDES[url]
            if old not in text:
                raise SystemExit(f"h1 not found {url}")
            text = text.replace(old, new, 1)

        existing = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', text)
        existing_desc = existing.group(1) if existing else ""
        truncated = bool(existing_desc) and existing_desc[-1] not in ".!?…"
        need_desc = url in descs
        has_canon = 'rel="canonical"' in text
        has_og = 'property="og:title"' in text

        if has_canon and has_og and existing_desc and not truncated and not need_desc:
            skipped.append(url)
            continue

        if need_desc:
            desc = descs[url]
            validate_desc(desc, url)
        elif existing_desc and not truncated:
            desc = existing_desc
            validate_desc(desc, url, existing=True)
        else:
            raise SystemExit(f"no description available for {url}")

        text2 = insert_after_robots_or_desc(text, desc, absurl, title)
        if 'name="robots" content="noindex, nofollow"' not in text2:
            raise SystemExit(f"robots lost {url}")
        if f'rel="canonical" href="{absurl}"' not in text2:
            raise SystemExit(f"canonical missing {url}")
        if text2.count('name="description"') != 1:
            raise SystemExit(f"desc count {text2.count(chr(34)+'description'+chr(34))} {url}")
        if text2.count('property="og:title"') != 1:
            raise SystemExit(f"og title dup {url}")

        out = text2.encode("utf-8")
        if has_bom:
            out = b"\xef\xbb\xbf" + out
        path.write_bytes(out)
        changed.append(url)

    print("changed", len(changed))
    print("skipped already complete", len(skipped))
    print("first changed", changed[:8])


if __name__ == "__main__":
    main()
