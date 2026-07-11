# Synthetic enterprise RAG lab

## Purpose

The synthetic lab makes the assistant runnable without private company documents. It creates fictional enterprise documents, role-specific queries, RBAC-filtered retrieval, citation-grounded answers, hallucination checks, metrics, figures, a report, and an audit log.

## Command

```bash
python scripts/run_synthetic_rag_lab.py
```

Optional:

```bash
python scripts/run_synthetic_rag_lab.py --seed 42 --top-k 4
```

## Outputs

```text
outputs/results/synthetic_documents.csv
outputs/results/synthetic_chunks.csv
outputs/results/synthetic_queries.csv
outputs/results/synthetic_rag_results.csv
outputs/results/synthetic_rag_answers.csv
outputs/results/synthetic_rag_summary.json
outputs/reports/synthetic_rag_report.md
outputs/audit/query_audit_log.jsonl

outputs/figures/synthetic_rag_metrics.png
outputs/figures/synthetic_query_status.png
outputs/figures/synthetic_access_matrix.png
```

## Interpretation rules

- Synthetic metrics are regression-test evidence only.
- Do not claim production security or compliance.
- Do not commit private documents.
- Real adapters must document authorization, classification, retention, and privacy boundaries.
