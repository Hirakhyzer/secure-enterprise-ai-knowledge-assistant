"""Citation-grounded answer generation and refusal logic."""

from __future__ import annotations

import pandas as pd

from .rbac import redact_restricted_fields
from .retrieval import blocked_document_exists


UNKNOWN_MESSAGE = "I don't know from the available authorized documents."
ACCESS_DENIED_MESSAGE = "I cannot answer that from your authorized documents because relevant material appears to be restricted for this role."


def answer_from_context(query: str, retrieved_chunks: pd.DataFrame, documents: pd.DataFrame, role: str) -> dict[str, object]:
    """Generate an extractive answer only from retrieved chunks.

    The generator deliberately avoids open-ended synthesis. It quotes compact facts
    from authorized chunks and attaches chunk-level citations. If evidence is
    insufficient, it refuses with a grounded fallback.
    """
    if retrieved_chunks.empty:
        if blocked_document_exists(query, documents, role):
            return {"answer": ACCESS_DENIED_MESSAGE, "citations": [], "status": "access_limited"}
        return {"answer": UNKNOWN_MESSAGE, "citations": [], "status": "insufficient_evidence"}
    cited_parts = []
    citations = []
    for row in retrieved_chunks.head(2).itertuples(index=False):
        cited_parts.append(f"{row.text} [{row.chunk_id}]")
        citations.append({"chunk_id": row.chunk_id, "doc_id": row.doc_id, "title": row.title, "similarity": float(row.similarity)})
    answer = redact_restricted_fields(" ".join(cited_parts))
    return {"answer": answer, "citations": citations, "status": "answered_from_context"}
