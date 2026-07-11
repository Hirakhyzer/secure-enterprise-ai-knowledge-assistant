# Data boundary

The default project uses fictional synthetic enterprise documents. No private company files are required.

## Synthetic default

Run:

```bash
python scripts/run_synthetic_rag_lab.py
```

## Future authorized documents

If you later connect real documents, place them only under:

```text
data/raw/
```

This directory is ignored by Git.

## Minimum metadata for real adapters

| Field | Purpose |
| --- | --- |
| doc_id | Stable document identifier |
| title | Human-readable source name |
| department | Ownership and governance |
| classification | Internal, confidential, restricted, etc. |
| allowed_roles | RBAC policy input |
| content | Authorized document text |

Do not infer document permissions. Unknown classification should default to restricted until reviewed.
