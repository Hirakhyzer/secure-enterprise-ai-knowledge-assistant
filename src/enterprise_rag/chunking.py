"""Document chunking for citation-grounded retrieval."""

from __future__ import annotations

import re

import pandas as pd


def split_sentences(text: str) -> list[str]:
    """Split text into simple sentence-like units for transparent citations."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def chunk_documents(documents: pd.DataFrame, max_sentences: int = 2) -> pd.DataFrame:
    """Create small chunks with document metadata and stable chunk IDs."""
    rows: list[dict] = []
    for doc in documents.itertuples(index=False):
        sentences = split_sentences(doc.content)
        for start in range(0, len(sentences), max_sentences):
            chunk_text = " ".join(sentences[start : start + max_sentences])
            chunk_index = start // max_sentences
            rows.append({
                "chunk_id": f"{doc.doc_id}::C{chunk_index:02d}",
                "doc_id": doc.doc_id,
                "title": doc.title,
                "department": doc.department,
                "classification": doc.classification,
                "allowed_roles": doc.allowed_roles,
                "chunk_index": chunk_index,
                "text": chunk_text,
            })
    return pd.DataFrame(rows)
