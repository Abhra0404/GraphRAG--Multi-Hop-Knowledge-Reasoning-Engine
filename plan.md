# GraphRAG --- Multi-Hop Knowledge Reasoning Engine

## 1. Project Vision

Build a production-oriented GraphRAG system that combines:

-   Document ingestion
-   Vector retrieval
-   Entity and relation extraction
-   Knowledge graphs
-   Multi-hop graph traversal
-   Query planning
-   Evidence fusion
-   LLM-based answer generation
-   Explainable reasoning paths
-   Quantitative evaluation

The system should answer questions that require connecting information
across multiple entities, documents, and relationships.

------------------------------------------------------------------------

## 2. Core Objective

Given a natural-language question:

1.  Understand the query.
2.  Identify important entities and relationships.
3.  Retrieve relevant semantic context using vector search.
4.  Retrieve relevant entities and relationships from the knowledge
    graph.
5.  Plan and execute multi-hop traversal.
6.  Rank and fuse evidence.
7.  Generate a grounded answer.
8.  Return the supporting sources and reasoning path.

### Success criterion

GraphRAG should demonstrate measurable improvement over vanilla vector
RAG on multi-hop questions while remaining grounded in retrieved
evidence.

------------------------------------------------------------------------

# 3. Development Roadmap

## V0 --- Foundation

### Goals

Set up the project and infrastructure.

### Tasks

-   [ ] Initialize Python project
-   [ ] Configure environment management
-   [ ] Add FastAPI
-   [ ] Add PostgreSQL
-   [ ] Add Neo4j
-   [ ] Add Qdrant
-   [ ] Add Redis
-   [ ] Add Docker Compose
-   [ ] Add structured logging
-   [ ] Add configuration management
-   [ ] Add health-check endpoints
-   [ ] Add pytest
-   [ ] Add CI workflow

### Definition of Done

All infrastructure starts locally with one command and health checks
pass.

------------------------------------------------------------------------

## V1 --- Vanilla RAG Baseline

### Goals

Build a conventional RAG system before adding graph reasoning.

### Pipeline

``` text
Document
   ↓
Parser
   ↓
Chunker
   ↓
Embedding Model
   ↓
Qdrant
   ↓
Top-K Retrieval
   ↓
Context Builder
   ↓
LLM
   ↓
Answer
```

### Tasks

-   [ ] PDF parser
-   [ ] Markdown/TXT parser
-   [ ] Chunking strategy
-   [ ] Metadata model
-   [ ] Embedding pipeline
-   [ ] Qdrant collection
-   [ ] Similarity search
-   [ ] RAG prompt
-   [ ] Answer generation
-   [ ] Source attribution
-   [ ] Baseline evaluation dataset

### Definition of Done

The system can answer single-hop questions from an indexed corpus with
source references.

------------------------------------------------------------------------

## V2 --- Knowledge Graph Construction

### Goals

Transform the document corpus into a structured knowledge graph.

### Pipeline

``` text
Documents
   ↓
Chunks
   ↓
Entity Extraction
   ↓
Entity Normalization
   ↓
Relation Extraction
   ↓
Confidence Scoring
   ↓
Neo4j
```

### Initial Node Types

-   Person
-   Organization
-   Company
-   University
-   Paper
-   Concept
-   Technology
-   Dataset
-   Model
-   Location

### Initial Relationship Types

-   AUTHORED
-   WORKED_AT
-   FOUNDED
-   STUDIED_AT
-   INFLUENCED
-   DEVELOPED
-   USES
-   RELATED_TO
-   PART_OF
-   CREATED
-   CONTRIBUTED_TO

### Tasks

-   [ ] Entity extraction
-   [ ] Relation extraction
-   [ ] Entity normalization
-   [ ] Duplicate entity resolution
-   [ ] Node creation
-   [ ] Edge creation
-   [ ] Provenance tracking
-   [ ] Extraction confidence
-   [ ] Graph indexes
-   [ ] Graph inspection queries

### Definition of Done

Documents can automatically produce a queryable Neo4j graph with
provenance.

------------------------------------------------------------------------

## V3 --- Hybrid Retrieval

### Goals

Combine semantic retrieval with graph retrieval.

### Pipeline

``` text
                    Query
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Vector Search      Entity Linking
             │                 │
             │                 ▼
             │            Graph Search
             │                 │
             └────────┬────────┘
                      ▼
                Evidence Fusion
                      ↓
                 Context Builder
                      ↓
                     LLM
```

### Tasks

-   [ ] Entity linker
-   [ ] Vector retriever
-   [ ] Graph retriever
-   [ ] Candidate path retrieval
-   [ ] Evidence deduplication
-   [ ] Relevance scoring
-   [ ] Context fusion
-   [ ] Hybrid retrieval API

### Definition of Done

A query can retrieve both textual evidence and graph evidence.

------------------------------------------------------------------------

## V4 --- Multi-Hop Reasoning Engine

### Goals

Support questions requiring multiple graph traversal steps.

### Example

``` text
Company
  ↓ founded_by
Founder
  ↓ studied_at
University
  ↓ known_for
Research Field
```

### Pipeline

``` text
Question
   ↓
Query Analyzer
   ↓
Query Decomposition
   ↓
Entity Linking
   ↓
Hop Planning
   ↓
Graph Traversal
   ↓
Path Ranking
   ↓
Evidence Collection
   ↓
LLM
```

### Tasks

-   [ ] Query decomposition
-   [ ] Relationship prediction
-   [ ] Hop estimation
-   [ ] Traversal planner
-   [ ] BFS/DFS traversal
-   [ ] Path constraints
-   [ ] Path scoring
-   [ ] Evidence collection
-   [ ] Maximum-hop safeguards
-   [ ] Multi-hop answer synthesis

### Definition of Done

The system can correctly answer benchmark questions requiring 2--4 hops.

------------------------------------------------------------------------

## V5 --- Advanced Reasoning

### Goals

Improve robustness and reasoning quality.

### Features

-   Dynamic hop selection
-   Path reranking
-   Entity disambiguation
-   Relation confidence
-   Contradiction detection
-   Evidence weighting
-   Query rewriting
-   Answer verification
-   Fallback to vector-only retrieval
-   Fallback to graph-only retrieval

### Future research direction

Train a learned path-ranking model that scores candidate graph paths
based on query-path compatibility.

------------------------------------------------------------------------

## V6 --- Evaluation & Research

### Goals

Scientifically compare retrieval strategies.

### Systems

1.  Vanilla RAG
2.  Graph-only RAG
3.  Hybrid GraphRAG
4.  Hybrid GraphRAG + reranking

### Retrieval Metrics

-   Recall@K
-   Precision@K
-   MRR
-   Hit Rate

### Generation Metrics

-   Faithfulness
-   Answer relevance
-   Context relevance
-   Citation correctness

### Graph Metrics

-   Entity linking accuracy
-   Relation extraction accuracy
-   Path accuracy
-   Hop accuracy

### Final experiment

Determine whether graph-based retrieval provides a measurable advantage
on multi-hop questions.

------------------------------------------------------------------------

# 4. API Surface

## POST /documents

Upload and ingest a document.

## POST /documents/index

Trigger indexing and graph construction.

## POST /query

Run GraphRAG reasoning.

Example response:

``` json
{
  "answer": "...",
  "confidence": 0.91,
  "entities": [],
  "reasoning_path": [],
  "sources": []
}
```

## GET /documents/{id}

Retrieve document metadata.

## GET /entities/{id}

Retrieve an entity and its graph neighborhood.

## GET /graph/path

Retrieve a graph path between entities.

## GET /health

Infrastructure health check.

------------------------------------------------------------------------

# 5. Storage Model

## PostgreSQL

Use for application metadata:

-   Documents
-   Chunks
-   Ingestion jobs
-   Query logs
-   Evaluation results

## Qdrant

Use for:

-   Chunk embeddings
-   Semantic retrieval
-   Optional entity embeddings

## Neo4j

Use for:

-   Entities
-   Relationships
-   Graph traversal
-   Provenance relationships

## Redis

Use for:

-   Background jobs
-   Caching
-   Temporary state

------------------------------------------------------------------------

# 6. Non-Functional Requirements

-   Reproducible local development
-   Dockerized infrastructure
-   Typed Python code
-   Unit and integration tests
-   Structured logs
-   Configurable LLM and embedding providers
-   Configurable retrieval parameters
-   Maximum traversal depth
-   Evidence provenance
-   No unsupported claims without evidence
-   Evaluation reproducibility

------------------------------------------------------------------------

# 7. Milestones

  Milestone   Result
  ----------- ------------------------
  M1          Infrastructure running
  M2          Vanilla RAG
  M3          Knowledge graph
  M4          Hybrid retrieval
  M5          Multi-hop reasoning
  M6          Explainable answers
  M7          Evaluation
  M8          Production polish

------------------------------------------------------------------------

# 8. Final Demo

The final demo should show:

``` text
User Question
      ↓
Query Planner
      ↓
Entity Identification
      ↓
Vector Retrieval + Graph Traversal
      ↓
Candidate Paths
      ↓
Evidence Ranking
      ↓
LLM
      ↓
────────────────────────────
Answer
Reasoning Path
Sources
Confidence
────────────────────────────
```

The project is complete when the system is demonstrably better at
multi-hop questions than the vanilla RAG baseline.
