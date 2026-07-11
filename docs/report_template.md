# Secure Enterprise AI Knowledge Assistant — Report Template

> Populate this report only with outputs generated from the synthetic lab or an authorized local document set.

## Scenario

- Data origin: [synthetic / authorized local enterprise corpus]
- Query set: [synthetic labels / reviewed enterprise test questions]
- Roles evaluated: [list]
- Retrieval model: [TF-IDF / local embeddings / reranker]
- Security boundary: [documented]

## Evaluation table

| Metric | Value | Boundary |
| --- | ---: | --- |
| Retrieval accuracy on answerable queries | [generated] | Synthetic or reviewed labels |
| Refusal accuracy | [generated] | Synthetic or reviewed labels |
| Access-control correctness | [generated] | Role policy dependent |
| Mean citation coverage | [generated] | Chunk-marker coverage |
| Hallucination-risk rate | [generated] | Heuristic checker |

## Figures

- `outputs/figures/synthetic_rag_metrics.png`
- `outputs/figures/synthetic_query_status.png`
- `outputs/figures/synthetic_access_matrix.png`

## Security review

- [RBAC filtering approach]
- [Audit log verification]
- [Citations and refusal behavior]
- [Remaining risks]

## Limitations

- [Synthetic or real-data boundary]
- [Retrieval limitations]
- [Grounding checker limitations]
- [Governance and compliance requirements]
