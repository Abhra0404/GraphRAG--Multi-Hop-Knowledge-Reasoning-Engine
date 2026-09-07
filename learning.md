# GraphRAG --- Learning Roadmap

This document defines what to learn alongside implementation.

------------------------------------------------------------------------

# Phase 0 --- Prerequisites

## Python

Learn:

-   Type hints
-   Dataclasses
-   Pydantic
-   Async programming
-   HTTP clients
-   Dependency management
-   Testing with pytest
-   Logging
-   Environment variables

## Backend

Learn:

-   REST APIs
-   FastAPI
-   Authentication basics
-   Background jobs
-   Caching
-   Database transactions
-   Docker

------------------------------------------------------------------------

# Phase 1 --- RAG Fundamentals

## Learn

-   Information retrieval
-   Tokenization
-   Chunking
-   Embeddings
-   Cosine similarity
-   Approximate nearest-neighbor search
-   Vector databases
-   Top-K retrieval
-   Reranking
-   Prompt construction
-   Grounded generation

## Important concepts

``` text
Document
   ↓
Chunk
   ↓
Embedding
   ↓
Vector
   ↓
Similarity Search
   ↓
Context
   ↓
LLM
```

## Build

A vanilla RAG system before touching graphs.

------------------------------------------------------------------------

# Phase 2 --- Knowledge Graphs

## Learn

-   Graph theory basics
-   Nodes
-   Edges
-   Directed graphs
-   Property graphs
-   Graph traversal
-   BFS
-   DFS
-   Shortest paths
-   Subgraphs
-   Graph databases

## Neo4j

Learn:

-   Cypher
-   MATCH
-   WHERE
-   CREATE
-   MERGE
-   RETURN
-   Relationships
-   Indexes
-   Constraints

Example:

``` cypher
MATCH (p:Person)-[:WORKED_AT]->(o:Organization)
RETURN p, o
```

------------------------------------------------------------------------

# Phase 3 --- Information Extraction

## Learn

### Named Entity Recognition

Identify:

-   People
-   Organizations
-   Papers
-   Technologies
-   Universities
-   Concepts

### Relation Extraction

Infer:

``` text
Entity A
   ↓ relation
Entity B
```

### Entity Resolution

Understand why:

``` text
"Google"
"Google LLC"
"Google Inc."
```

may refer to the same entity.

### Provenance

Every extracted relationship should retain evidence showing where it
came from.

------------------------------------------------------------------------

# Phase 4 --- Embeddings

Learn:

-   Word embeddings
-   Sentence embeddings
-   Transformer embeddings
-   Dense retrieval
-   Cosine similarity
-   Euclidean distance
-   Vector normalization
-   ANN indexes

Understand:

``` text
text → embedding → vector space → nearest neighbors
```

------------------------------------------------------------------------

# Phase 5 --- Transformers & LLMs

Learn:

-   Attention
-   Self-attention
-   Transformer architecture
-   Tokenization
-   Context windows
-   Prompting
-   Structured output
-   Function/tool calling
-   Temperature
-   Hallucination
-   Grounding

Important distinction:

``` text
LLM reasoning
      ≠
retrieval
```

The retrieval system supplies evidence; the LLM synthesizes it.

------------------------------------------------------------------------

# Phase 6 --- GraphRAG

Learn:

-   Graph-based retrieval
-   Entity-centric retrieval
-   Local graph context
-   Global graph context
-   Community detection
-   Graph summarization
-   Hybrid retrieval
-   Graph-aware reranking

Core idea:

``` text
Vector similarity
+
Graph connectivity
=
Better contextual retrieval
```

------------------------------------------------------------------------

# Phase 7 --- Multi-Hop Reasoning

Learn:

-   Query decomposition
-   Query planning
-   Iterative retrieval
-   Path search
-   Beam search
-   BFS/DFS
-   Candidate generation
-   Path ranking
-   Evidence aggregation

Example:

``` text
Question
 ↓
Sub-question 1
 ↓
Entity A
 ↓
Relationship
 ↓
Entity B
 ↓
Sub-question 2
 ↓
Entity C
```

------------------------------------------------------------------------

# Phase 8 --- Retrieval Evaluation

Learn:

-   Precision
-   Recall
-   F1
-   Recall@K
-   Precision@K
-   MRR
-   NDCG

Understand why:

> A good answer does not necessarily mean good retrieval.

We need to evaluate the retrieval layer independently.

------------------------------------------------------------------------

# Phase 9 --- LLM Evaluation

Learn:

-   Faithfulness
-   Answer relevance
-   Context relevance
-   Citation correctness
-   Hallucination detection
-   LLM-as-a-judge
-   Human evaluation

------------------------------------------------------------------------

# Phase 10 --- Advanced Research

Optional but recommended.

Study:

-   Graph Neural Networks
-   GraphSAGE
-   GCN
-   GAT
-   Knowledge graph embeddings
-   TransE
-   RotatE
-   Learned graph retrieval
-   Neural path ranking
-   Reinforcement learning for graph traversal

Potential research direction:

``` text
Question
 ↓
Candidate Paths
 ↓
Neural Path Ranker
 ↓
Best Evidence Path
 ↓
LLM
```

------------------------------------------------------------------------

# Recommended Learning Order

``` text
Python
 ↓
FastAPI
 ↓
RAG
 ↓
Embeddings
 ↓
Vector DB
 ↓
Graph Theory
 ↓
Neo4j/Cypher
 ↓
NER + Relation Extraction
 ↓
Hybrid Retrieval
 ↓
Multi-Hop Reasoning
 ↓
Evaluation
 ↓
Advanced Graph ML
```

Do not wait until every topic is mastered. Learn each concept
immediately before implementing it.
