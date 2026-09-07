# GraphRAG --- System Architecture

## 1. High-Level Architecture

``` text
                         ┌───────────────┐
                         │     Client    │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         └───────┬───────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
          Ingestion API     Query API       Graph API
                │                │
                ▼                ▼
          Ingestion Engine  Query Planner
                │                │
                ▼         ┌──────┴───────┐
          Extraction       │              │
                │          ▼              ▼
                ▼      Vector Search   Graph Search
          Graph Builder      │              │
                │            │              │
                ▼            └──────┬───────┘
             Neo4j                  ▼
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

# 2. Ingestion Architecture

``` text
                 Document
                    │
                    ▼
              Document Parser
                    │
                    ▼
                 Cleaner
                    │
                    ▼
                 Chunker
                    │
             ┌──────┴──────┐
             ▼             ▼
        Embeddings     Extraction
             │             │
             ▼             ▼
           Qdrant      Entities/Relations
                           │
                           ▼
                         Neo4j
```

------------------------------------------------------------------------

# 3. Query Architecture

``` text
User Query
    │
    ▼
Query Analyzer
    │
    ├── Intent
    ├── Entities
    ├── Constraints
    └── Estimated hops
    │
    ▼
Query Planner
    │
    ├───────────────┐
    ▼               ▼
Vector Retrieval   Graph Retrieval
    │               │
    │               ▼
    │          Graph Traversal
    │               │
    └───────┬───────┘
            ▼
      Candidate Evidence
            │
            ▼
       Reranker/Fusion
            │
            ▼
      Context Builder
            │
            ▼
            LLM
            │
            ▼
     Grounded Response
```

------------------------------------------------------------------------

# 4. Component Responsibilities

## API Layer

Responsible for:

-   HTTP requests
-   Request validation
-   Response serialization
-   Authentication boundary
-   Error handling

------------------------------------------------------------------------

## Ingestion Engine

Responsible for:

-   File parsing
-   Cleaning
-   Chunking
-   Metadata
-   Ingestion orchestration

------------------------------------------------------------------------

## Extraction Engine

Responsible for:

-   Entity extraction
-   Relation extraction
-   Entity normalization
-   Confidence scoring

------------------------------------------------------------------------

## Graph Engine

Responsible for:

-   Neo4j connection
-   Node creation
-   Edge creation
-   Graph queries
-   Traversal
-   Path generation

------------------------------------------------------------------------

## Retrieval Engine

Responsible for:

-   Vector retrieval
-   Entity retrieval
-   Graph retrieval
-   Candidate generation
-   Reranking

------------------------------------------------------------------------

## Reasoning Engine

Responsible for:

-   Query decomposition
-   Hop planning
-   Traversal planning
-   Evidence aggregation
-   Answer verification

------------------------------------------------------------------------

## Generation Engine

Responsible for:

-   Prompt construction
-   LLM invocation
-   Structured output
-   Grounded answer generation

------------------------------------------------------------------------

# 5. Graph Data Model

## Entity

``` text
Entity
├── id
├── name
├── type
├── description
├── aliases
├── embedding
└── confidence
```

## Relationship

``` text
Relationship
├── source_id
├── target_id
├── type
├── confidence
├── source_document_id
└── source_chunk_id
```

------------------------------------------------------------------------

# 6. Provenance Model

Every important graph assertion should be traceable.

``` text
Document
   │
   ▼
Chunk
   │
   ▼
Extraction
   │
   ├── Entity
   │
   └── Relationship
```

This allows:

``` text
Answer
  ↓
Evidence
  ↓
Chunk
  ↓
Document
```

------------------------------------------------------------------------

# 7. Hybrid Retrieval Strategy

For a query Q:

``` text
VectorScore(Q, chunk)
```

measures semantic similarity.

Graph retrieval measures structural relevance:

``` text
GraphScore(Q, path)
```

A combined score can eventually be modeled as:

``` text
FinalScore =
    α × VectorScore
  + β × GraphScore
  + γ × EvidenceScore
  + δ × PathScore
```

The weights should be configurable and evaluated experimentally.

------------------------------------------------------------------------

# 8. Multi-Hop Traversal

Initial implementation:

``` text
BFS traversal
+
relationship filtering
+
maximum hop depth
+
candidate scoring
```

Example:

``` text
A
├──r1──> B
│        └──r2──> C
│                  └──r3──> D
└──r4──> E
         └──r5──> F
```

Candidate paths:

``` text
A → B → C → D
A → E → F
```

The reasoning engine ranks these paths based on query relevance and
evidence quality.

------------------------------------------------------------------------

# 9. Context Construction

The LLM should not receive the entire graph.

Instead:

``` text
Query
 ↓
Relevant subgraph
 ↓
Relevant chunks
 ↓
Evidence ranking
 ↓
Compact context
 ↓
LLM
```

Context should contain:

1.  Relevant entities
2.  Relevant relationships
3.  Supporting text
4.  Source identifiers
5.  Reasoning path

------------------------------------------------------------------------

# 10. Explainability

Every final answer should ideally expose:

``` json
{
  "answer": "...",
  "reasoning_path": [
    {
      "from": "Entity A",
      "relation": "RELATION",
      "to": "Entity B"
    }
  ],
  "evidence": [
    {
      "document_id": "...",
      "chunk_id": "..."
    }
  ]
}
```

------------------------------------------------------------------------

# 11. Failure Handling

The system should handle:

### Unknown entity

Fallback to vector retrieval.

### Ambiguous entity

Return multiple candidates and rerank.

### No graph path

Use semantic retrieval.

### Conflicting evidence

Surface the conflict rather than silently choosing one claim.

### Low confidence

Tell the generation layer to avoid overclaiming.

------------------------------------------------------------------------

# 12. Deployment

``` text
                    Docker Network
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
   FastAPI             Worker             Redis
       │
       ├──────────────┬────────────────┐
       ▼              ▼                ▼
 PostgreSQL         Qdrant           Neo4j
       │
       └──────────────┬────────────────┘
                      ▼
                     LLM
```

------------------------------------------------------------------------

# 13. Scalability Direction

Future improvements:

-   Async ingestion
-   Batch embeddings
-   Background graph construction
-   Query caching
-   Connection pooling
-   Graph indexes
-   Vector index tuning
-   Distributed workers
-   Streaming generation
-   Observability
-   Rate limiting

------------------------------------------------------------------------

# 14. Security Direction

-   Input validation
-   File-type validation
-   Upload size limits
-   Prompt-injection defenses
-   Tenant isolation if multi-user
-   Secrets outside source control
-   API authentication
-   Rate limiting
-   Audit logs
