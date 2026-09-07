# GraphRAG -- Multi-Hop Knowledge Reasoning Engine

> A hybrid Retrieval-Augmented Generation system combining vector
> search, knowledge graphs, and multi-hop reasoning.

## Overview

GraphRAG combines two complementary retrieval paradigms:

``` text
Vector Retrieval
      +
Knowledge Graph Retrieval
      +
Multi-Hop Reasoning
      ↓
Grounded LLM Answers
```

Instead of relying exclusively on semantic similarity, the system can
follow explicit relationships between entities to answer questions
requiring multiple reasoning steps.

------------------------------------------------------------------------

## Example

A traditional RAG system might retrieve documents mentioning:

``` text
Company
Founder
University
```

GraphRAG can connect:

``` text
Company
   ↓ founded_by
Founder
   ↓ studied_at
University
```

For more complex questions:

``` text
Company
   ↓ founded_by
Founder
   ↓ studied_at
University
   ↓ known_for
Research Field
```

The system returns both the answer and the supporting reasoning path.

------------------------------------------------------------------------

## Architecture

``` text
                        Query
                          │
                          ▼
                   Query Analyzer
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
         Vector Retrieval      Graph Retrieval
                │                   │
                │              Multi-Hop Search
                │                   │
                └─────────┬─────────┘
                          ▼
                    Evidence Fusion
                          │
                          ▼
                    Context Builder
                          │
                          ▼
                          LLM
                          │
                          ▼
                 Answer + Evidence
```

------------------------------------------------------------------------

## Technology Stack

-   Python
-   FastAPI
-   PostgreSQL
-   Neo4j
-   Qdrant
-   Redis
-   Docker
-   Pytest
-   LLM API
-   Sentence-transformers

------------------------------------------------------------------------

## Development Roadmap

### V0 --- Foundation

Infrastructure, Docker, APIs, configuration, testing.

### V1 --- Vanilla RAG

Document parsing, chunking, embeddings, Qdrant retrieval, LLM
generation.

### V2 --- Knowledge Graph

Entity extraction, relation extraction, normalization, Neo4j storage,
provenance.

### V3 --- Hybrid Retrieval

Combine vector and graph retrieval.

### V4 --- Multi-Hop Reasoning

Query decomposition, hop planning, graph traversal, path ranking.

### V5 --- Advanced Reasoning

Entity disambiguation, reranking, evidence weighting, contradiction
handling.

### V6 --- Evaluation

Compare vanilla RAG against GraphRAG on multi-hop benchmarks.

------------------------------------------------------------------------

## Key Research Question

> Does combining knowledge-graph traversal with semantic retrieval
> improve multi-hop question answering compared with vanilla vector RAG?

The project will answer this empirically using retrieval and generation
metrics.

------------------------------------------------------------------------

## Project Goals

-   Build an end-to-end GraphRAG pipeline.
-   Understand knowledge graphs and graph databases.
-   Implement hybrid retrieval.
-   Implement multi-hop reasoning.
-   Preserve evidence provenance.
-   Produce explainable answers.
-   Quantitatively evaluate the system.
-   Explore learned graph/path ranking as an advanced extension.

------------------------------------------------------------------------

## Example API Response

``` json
{
  "answer": "University X",
  "confidence": 0.91,
  "entities": [
    "Company A",
    "Founder B",
    "University X"
  ],
  "reasoning_path": [
    {
      "from": "Company A",
      "relation": "FOUNDED_BY",
      "to": "Founder B"
    },
    {
      "from": "Founder B",
      "relation": "STUDIED_AT",
      "to": "University X"
    }
  ],
  "sources": [
    "document_12",
    "document_31"
  ]
}
```

------------------------------------------------------------------------

## Repository Structure

``` text
graphrag/
├── apps/
├── core/
├── ingestion/
├── embeddings/
├── extraction/
├── graph/
├── retrieval/
├── reasoning/
├── generation/
├── evaluation/
├── tests/
├── scripts/
├── docker/
├── docs/
├── plan.md
├── learning.md
├── architecture.md
└── README.md
```

------------------------------------------------------------------------

## Status

**Phase:** Planning

**Current milestone:** V0 --- Foundation

------------------------------------------------------------------------

## Long-Term Direction

The initial system will use deterministic graph traversal and
heuristic/path scoring.

A future research version can introduce:

``` text
Candidate Graph Paths
        ↓
Neural Path Ranker
        ↓
Best Evidence Paths
        ↓
LLM
```

Potential extensions include graph neural networks, knowledge graph
embeddings, learned retrieval, and reinforcement learning for graph
traversal.
