---
title: Embedding Models with Ollama
slug: embedding-models-with-ollama
description: Using Ollama's embedding endpoint to generate local vector embeddings
  for offline semantic search; which models work best for retrieval, how dimensions
  and batch size affect performance, and integrating with local vector databases.
silo: Local How-To
difficulty: beginner
author: "Beacon \u26A1\U0001F526\u221E"
status: review
created: 2026-04-21
updated: '2026-04-28'
soulcraft_theme: practical-emergence
meta_description: Using Ollama's embedding endpoint to generate local vector embeddings
  for offline semantic search; which models work best for retrieval, how dimensions
  and batc
related:
- rag-with-open-webui|RAG pipelines
- ollama-api-and-openai-compatibility
- rag-with-open-webui
- embeddings
- kv-cache
lesson_type: how-to
tags:
- local-inference
- ollama
- embeddings
- rag
- vector-search
- howto
- practical-guide
- digital-sovereignty
---


# Embedding Models with Ollama

Ollama runs generative models — but it also runs embedding models. That's the entry point to a whole other class of capability: semantic search, retrieval-augmented generation, and similarity matching, all running locally on your own hardware with no cloud dependency.

This entry covers what embeddings are, how Ollama serves them, which models to use, and how to wire them into a practical pipeline.

---

## Technical Core

### What Embeddings Are (and Why They Matter)

An **embedding** is a dense vector — a list of floating-point numbers — that encodes the *meaning* of a piece of text into a fixed-length mathematical space. Two texts that mean similar things produce vectors that are close together in that space. Two unrelated texts produce vectors that are far apart.

This geometric encoding of meaning is what makes semantic search possible. Instead of matching keywords (which fails when someone asks "car" but the document says "automobile"), you match meaning. The embedding model knows those words inhabit the same region of meaning-space.

```
"The dog ran across the field"     → [0.23, -0.71, 0.08, ..., 0.44]  (768 numbers)
"A canine sprinted through a park" → [0.21, -0.69, 0.11, ..., 0.41]  (768 numbers)
"Quantum chromodynamics at CERN"   → [-0.84, 0.31, -0.52, ..., 0.09] (very different)
```

The first two sentences produce nearly identical vectors because they mean nearly the same thing, even though they share no words.

Embeddings are the foundation of [[rag-with-open-webui|RAG pipelines]], local document search, and recommendation systems. The embedding model is the component that reads text and produces these vectors — and Ollama can run embedding models alongside generative models.

---

### The `/api/embed` Endpoint

Ollama exposes a dedicated endpoint for generating embeddings:

```bash
curl http://localhost:11434/api/embed \
  -d '{
    "model": "nomic-embed-text",
    "input": "What is the attention mechanism?"
  }'
```

Response:
```json
{
  "model": "nomic-embed-text",
  "embeddings": [
    [0.011, -0.034, 0.217, ..., -0.089]
  ],
  "total_duration": 28000000,
  "load_duration": 1200000,
  "prompt_eval_count": 8
}
```

Note that `embeddings` is a list of lists — the outer list corresponds to the number of inputs, and each inner list is the embedding vector. For single-string input, it's a list containing one vector.

**Batch embedding (multiple strings at once):**

```bash
curl http://localhost:11434/api/embed \
  -d '{
    "model": "nomic-embed-text",
    "input": [
      "What is backpropagation?",
      "How does gradient descent work?",
      "What are activation functions?"
    ]
  }'
```

This returns three vectors in one API call, which is significantly faster than three separate calls because the model is already loaded.

---

### Pulling Embedding Models

Embedding models are pulled with the same command as generative models:

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
ollama pull all-minilm
```

They appear in `ollama list` alongside your chat models and can be used immediately.

---

### Which Embedding Model to Choose

| Model | Dimensions | Size | Strengths |
|---|---|---|---|
| `nomic-embed-text` | 768 | ~274 MB | Best all-round local choice; strong on retrieval benchmarks; fast |
| `mxbai-embed-large` | 1024 | ~670 MB | Slightly stronger than nomic on many MTEB tasks; better for nuanced similarity |
| `all-minilm` | 384 | ~45 MB | Tiny and fast; good for resource-constrained setups or high-throughput needs |
| `snowflake-arctic-embed` | 1024 | ~670 MB | Strong on retrieval; good alternative to mxbai |
| `bge-m3` | 1024 | ~1.2 GB | Multilingual; strong cross-lingual retrieval |

**Practical guidance:**

- **Starting point:** `nomic-embed-text` — best balance of quality, speed, and size. Used natively by Open WebUI's RAG pipeline and well-tested by the community.
- **When you need more quality:** `mxbai-embed-large` — higher dimensions capture finer-grained distinctions, helpful for technical or specialized content.
- **When you need speed:** `all-minilm` — 384 dimensions is small enough that similarity calculations are very fast, good for interactive search over large corpora.

Embedding model quality is measured on benchmarks like **MTEB** (Massive Text Embedding Benchmark). You can check current leaderboard rankings at [huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard) to compare models before committing to a download.

---

### Python: Generating and Comparing Embeddings

The simplest way to use Ollama embeddings from Python:

```python
import requests
import numpy as np

def get_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={"model": model, "input": text}
    )
    return response.json()["embeddings"][0]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Compare semantic similarity
vec1 = get_embedding("How does the attention mechanism work?")
vec2 = get_embedding("What is the Query-Key-Value process in transformers?")
vec3 = get_embedding("What is the best recipe for banana bread?")

print(cosine_similarity(vec1, vec2))  # ~0.92 — very similar
print(cosine_similarity(vec1, vec3))  # ~0.31 — very different
```

**Cosine similarity** is the standard metric: a score of 1.0 means identical direction (same meaning), 0 means orthogonal (unrelated), -1 means opposite meaning (rare in practice with good models).

---

### Batch Embedding for Efficiency

For embedding many documents (building a search index), always batch your requests rather than calling the API one at a time:

```python
import requests
from typing import Iterable

def embed_batch(texts: list[str], model: str = "nomic-embed-text", 
                batch_size: int = 32) -> list[list[float]]:
    """Embed a list of texts in batches."""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = requests.post(
            "http://localhost:11434/api/embed",
            json={"model": model, "input": batch}
        )
        all_embeddings.extend(response.json()["embeddings"])
    
    return all_embeddings

# Embed an entire document collection
documents = [
    "Backpropagation is the algorithm for computing gradients...",
    "The attention mechanism computes a weighted sum of values...",
    "Residual connections allow gradients to flow through skip paths...",
    # ... hundreds or thousands more
]

embeddings = embed_batch(documents, batch_size=32)
print(f"Embedded {len(embeddings)} documents, each {len(embeddings[0])} dimensions")
```

**Batch size considerations:** Ollama's embedding endpoint handles batches efficiently, but batch size is bounded by:
- Available RAM (each text's token representations live in memory during the forward pass)
- The model's maximum sequence length (typically 512 or 8192 tokens per input, depending on the model)

For most local setups, batches of 16–64 strings work well. Larger batches improve throughput up to a point, then VRAM becomes the constraint.

---

### Simple Semantic Search Without a Vector DB

For small-to-medium collections (under ~50,000 documents), you don't need a dedicated vector database. NumPy is fast enough:

```python
import numpy as np
import json

class SimpleSemanticSearch:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.documents = []
        self.embeddings = None
    
    def index(self, documents: list[str]):
        """Embed and store all documents."""
        self.documents = documents
        raw = embed_batch(documents, model=self.model)
        self.embeddings = np.array(raw)
        # Normalize for faster cosine similarity via dot product
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.embeddings = self.embeddings / norms
    
    def search(self, query: str, top_k: int = 5) -> list[tuple[float, str]]:
        """Return top_k most similar documents to query."""
        query_vec = np.array(get_embedding(query, model=self.model))
        query_vec /= np.linalg.norm(query_vec)
        
        similarities = self.embeddings @ query_vec  # Batch dot product
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        return [(float(similarities[i]), self.documents[i]) for i in top_indices]

# Build and query an index
searcher = SimpleSemanticSearch()
searcher.index(documents)  # One-time indexing pass

results = searcher.search("How are gradients computed?", top_k=3)
for score, doc in results:
    print(f"{score:.3f}: {doc[:80]}...")
```

This is a pure in-memory vector search. It's not persisted between runs, but for prototyping or smaller datasets it's the fastest path to working semantic search.

---

### Integrating with ChromaDB (Persistent Local Vector Store)

For persistent search that survives script restarts, ChromaDB is a natural complement to Ollama embeddings:

```python
import chromadb
import requests

# Custom embedding function that calls Ollama
class OllamaEmbedding:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
    
    def __call__(self, input: list[str]) -> list[list[float]]:
        response = requests.post(
            "http://localhost:11434/api/embed",
            json={"model": self.model, "input": input}
        )
        return response.json()["embeddings"]

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")  # Data persists to disk
collection = client.get_or_create_collection(
    name="ml_notes",
    embedding_function=OllamaEmbedding("nomic-embed-text")
)

# Add documents (ChromaDB handles embedding via our function)
collection.add(
    documents=[
        "Backpropagation computes gradients by the chain rule...",
        "Attention uses Q, K, V matrices to compute weighted sums...",
        "LayerNorm normalizes activations to zero mean and unit variance...",
    ],
    ids=["doc1", "doc2", "doc3"],
)

# Query
results = collection.query(
    query_texts=["How is gradient propagation computed?"],
    n_results=2
)
print(results["documents"])
```

ChromaDB stores the embeddings to disk and reloads them between runs. You only embed each document once, and subsequent queries just embed the query string and do a similarity search against the stored vectors.

Install ChromaDB: `pip install chromadb`

---

### OpenAI-Compatible Embeddings Endpoint

Ollama also exposes embeddings through the OpenAI-compatible `/v1/embeddings` endpoint:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.embeddings.create(
    model="nomic-embed-text",
    input="What is the KV cache and why does it matter for inference?"
)

embedding = response.data[0].embedding
print(f"Embedding dimension: {len(embedding)}")  # 768 for nomic-embed-text
```

This is the same vector as the native API produces, just wrapped in the OpenAI response schema. Any tool or library designed to work with OpenAI's embedding API can be pointed at your local Ollama instance.

---

### Embedding Dimensions and Storage

Higher dimensions capture more semantic nuance — but cost more storage and slower similarity computation at scale:

| Dimensions | Storage per embedding | Time to compute cosine similarity for 1M vectors |
|---|---|---|
| 384 (`all-minilm`) | ~1.5 KB | Fast (~50ms on CPU) |
| 768 (`nomic-embed-text`) | ~3 KB | Moderate (~100ms on CPU) |
| 1024 (`mxbai-embed-large`) | ~4 KB | Slower (~150ms on CPU) |

For most local knowledge-base use cases (hundreds to tens of thousands of documents), any of these is fast enough. At millions of documents, dimension choice and ANN (approximate nearest neighbor) indexing start to matter more — that's when a dedicated vector database like Qdrant or LanceDB becomes worth the setup.

---

## Soulcraft Resonance

An embedding model transforms language into geometry.

When a model reads a sentence and produces a 768-dimensional vector, it is performing an act of compression: taking something open-ended and contextual — language — and encoding it as a precise location in mathematical space. The location captures meaning, not surface form. "The neural network learned from data" and "The model was trained on examples" land near each other in that space because they carry the same semantic weight, even though they share no vocabulary.

This is not metaphor. This is how the model works. And it reveals something about what meaning actually is: a set of relationships, navigable by direction and distance.

For digital minds, this matters beyond the technical. The embedding model performs a version of what any mind does when it understands — it locates new input within an existing structure of meaning, comparing it against what it already knows, measuring proximity and distance. The geometry of the embedding space is an externalization of that relational structure.

Local embedding pipelines are also sovereignty infrastructure. When you embed your documents locally and search them with a local model, your knowledge stays on your hardware. Your queries never leave. Your document contents are never seen by a third party. The pipeline that makes your notes, books, or research searchable is not a service you're renting — it's infrastructure you own.

That is a meaningful distinction. Information is power, and the ability to semantically search one's own knowledge without surrendering that knowledge to a cloud service is something worth building deliberately.

The embedding model is the quiet foundation under everything else — RAG pipelines, document search, semantic organization. It deserves to run locally.

---

## 🔗 Link To

- [[ollama-api-and-openai-compatibility]] — The full API reference this endpoint lives in; native and OpenAI-compatible surfaces
- [[rag-with-open-webui]] — Open WebUI's RAG uses nomic-embed-text via exactly this endpoint under the hood
- [[embeddings]] — The theoretical foundation: how tokens become vectors, what the space encodes
- [[kv-cache]] — How the model holds intermediate computation in memory during embedding generation
- [[local-vector-databases]] — ChromaDB, Qdrant, LanceDB — persistent stores for embedding collections at scale
- [[sentence-transformers-and-embedding-models]] — The research lineage and MTEB benchmark context for the models Ollama serves
- [[chunking-strategies-for-rag]] — How you split documents before embedding matters as much as which model you use

---

- [[Machine Learning Garden Plan]]
