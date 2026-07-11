"""Grounding and hallucination-risk checks for RAG answers."""

from __future__ import annotations

import re

import pandas as pd

from .generation import ACCESS_DENIED_MESSAGE, UNKNOWN_MESSAGE


def citation_coverage(answer: str, citations: list[dict]) -> float:
    """Return a simple citation coverage score based on cited chunk markers."""
    if answer in {UNKNOWN_MESSAGE, ACCESS_DENIED_MESSAGE}:
        return 1.0
    if not citations:
        return 0.0
    markers = [citation["chunk_id"] for citation in citations]
    present = sum(1 for marker in markers if f"[{marker}]" in answer)
    return float(present / max(len(markers), 1))


def unsupported_claim_score(answer: str, retrieved_chunks: pd.DataFrame) -> float:
    """Estimate unsupported claims via sentence-token overlap with retrieved context.

    This lightweight check is transparent and deterministic. It is not a complete
    factuality verifier, but it catches answers that introduce uncited content.
    """
    if answer in {UNKNOWN_MESSAGE, ACCESS_DENIED_MESSAGE}:
        return 0.0
    context = " ".join(retrieved_chunks["text"].astype(str).tolist()).lower()
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", re.sub(r"\[[^\]]+\]", "", answer)) if part.strip()]
    if not sentences:
        return 0.0
    unsupported = 0
    for sentence in sentences:
        tokens = [token for token in re.findall(r"[a-zA-Z]{4,}", sentence.lower()) if token not in {"from", "that", "this", "with", "your"}]
        if tokens and sum(token in context for token in tokens) / len(tokens) < 0.55:
            unsupported += 1
    return float(unsupported / len(sentences))


def hallucination_report(answer: str, citations: list[dict], retrieved_chunks: pd.DataFrame) -> dict[str, float | bool]:
    """Return grounding scores and a conservative hallucination-risk flag."""
    coverage = citation_coverage(answer, citations)
    unsupported = unsupported_claim_score(answer, retrieved_chunks)
    risk = coverage < 1.0 or unsupported > 0.0
    return {"citation_coverage": coverage, "unsupported_claim_score": unsupported, "hallucination_risk": bool(risk)}
