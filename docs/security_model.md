# Security model

## Security goals

1. Enforce role-based access before retrieval.
2. Generate answers only from authorized retrieved chunks.
3. Provide citations for supported claims.
4. Refuse when evidence is unavailable or restricted.
5. Keep private documents out of Git.
6. Log query decisions for auditability.

## Non-goals

- This repository is not a production identity provider.
- It is not a full data-loss-prevention system.
- It is not a certified compliance platform.
- It does not guarantee legal, HR, security, or financial correctness.
- It does not train or fine-tune a model on private documents.

## Threats considered

| Threat | Mitigation in the lab |
| --- | --- |
| Unauthorized document leakage | Candidate chunks are RBAC-filtered before ranking |
| Unsupported answer claims | Citation coverage and unsupported-claim checks |
| Missing evidence | Unknown fallback response |
| Restricted evidence | Access-limited refusal response |
| Sensitive token exposure | Demonstration redaction rules |
| Audit tampering | Hash-chained JSONL audit log |

## Deployment caution

A real deployment would require enterprise identity integration, document classification governance, encryption, key management, network controls, monitoring, prompt-injection testing, human review, privacy review, and legal/compliance approval.
