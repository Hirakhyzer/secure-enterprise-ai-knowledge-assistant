# Methodology

## Scope

This repository implements a synthetic-first private enterprise RAG assistant for research and portfolio demonstration. The default corpus is fictional and includes role-restricted HR, finance, engineering, security, support, legal, incident-response, and executive documents.

It is not connected to real enterprise systems, does not train on private documents, and does not bypass access controls.

## 1. Document ingestion and metadata

Each document has a document ID, title, department, classification, allowed roles, and content. Real adapters added later must preserve source metadata, timestamps, classification, owner, and authorization evidence.

## 2. Chunking and citations

Documents are split into small sentence-based chunks. Every answer cites chunk IDs in brackets. Chunk-level citations are used because document-level citations can be too coarse for enterprise compliance review.

## 3. Role-based access control

The retrieval engine filters the chunk table by role before vector ranking. Unauthorized chunks never enter the candidate set, generation context, citations, or answer text. This is the core security invariant.

## 4. Retrieval baseline

The first retrieval model is local TF-IDF with cosine similarity. It is deliberately simple, deterministic, auditable, and free of external services. Later extensions can add local embedding models, vector databases, or transformer rerankers if authorization and deployment controls are documented.

## 5. Answer generation

The default generator is extractive: it assembles answer text only from retrieved authorized chunks and attaches citations. If no sufficient authorized evidence exists, it returns a refusal or unknown fallback.

## 6. Hallucination checks

The lab computes citation coverage and a lightweight unsupported-claim score by comparing answer sentence tokens to retrieved context. This check is not a perfect factuality verifier, but it catches unsupported synthesis and missing citations.

## 7. Auditability

Every query writes a JSONL audit record with role, status, retrieved chunk IDs, citation coverage, hallucination flag, expected synthetic label, and a hash-chain link to the previous record. The audit log can be verified locally.

## 8. Evaluation

The synthetic lab reports retrieval accuracy on answerable queries, refusal accuracy, access-control correctness, mean citation coverage, and hallucination-risk rate. These metrics are for synthetic regression testing only. Real deployments require reviewed enterprise test sets and governance approval.

## Limitations

- Synthetic documents do not represent real enterprise complexity.
- TF-IDF is a baseline, not a production semantic search system.
- Role policies are simplified.
- The hallucination checker is a conservative heuristic.
- This project does not provide legal, HR, finance, security, or operational advice.
- Any real company documents must remain local and authorized.
