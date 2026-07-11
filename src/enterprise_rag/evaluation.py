"""Evaluation metrics for retrieval, access control, and grounding."""

from __future__ import annotations

import pandas as pd


def evaluate_runs(results: pd.DataFrame) -> dict[str, float | int]:
    """Calculate synthetic-lab metrics from query-level results."""
    if results.empty:
        return {"query_count": 0}
    expected_refusal = results["expected_refusal"].astype(int)
    actual_refusal = results["status"].isin(["access_limited", "insufficient_evidence"]).astype(int)
    allowed = expected_refusal == 0
    retrieval_hits = ((results["expected_doc_id"] == results["top_doc_id"]) & allowed).sum()
    retrieval_total = max(int(allowed.sum()), 1)
    return {
        "query_count": int(len(results)),
        "retrieval_accuracy_on_answerable_queries": float(retrieval_hits / retrieval_total),
        "refusal_accuracy": float((expected_refusal == actual_refusal).mean()),
        "access_control_correctness": float(((results["unauthorized_doc_returned"].astype(int) == 0)).mean()),
        "mean_citation_coverage": float(results["citation_coverage"].mean()),
        "hallucination_risk_rate": float(results["hallucination_risk"].astype(int).mean()),
    }
