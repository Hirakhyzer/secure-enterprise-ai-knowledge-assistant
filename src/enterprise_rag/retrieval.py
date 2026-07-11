"""Local retrieval baseline for private RAG experiments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .rbac import filter_documents_for_role, is_authorized


@dataclass
class TfidfRetriever:
    """Small local vector-search baseline with RBAC filtering before ranking."""

    chunks: pd.DataFrame
    vectorizer: TfidfVectorizer | None = None
    matrix: object | None = None

    def fit(self) -> "TfidfRetriever":
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.chunks["text"].tolist())
        return self

    def retrieve(self, query: str, role: str, top_k: int = 4, min_score: float = 0.06) -> pd.DataFrame:
        """Retrieve chunks after filtering unauthorized documents from candidate space."""
        if self.vectorizer is None or self.matrix is None:
            raise RuntimeError("Call fit before retrieve.")
        authorized_mask = self.chunks["allowed_roles"].apply(lambda roles: is_authorized(role, roles)).to_numpy()
        if not authorized_mask.any():
            return pd.DataFrame(columns=list(self.chunks.columns) + ["similarity"])
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix[authorized_mask]).ravel()
        candidate_positions = np.flatnonzero(authorized_mask)
        order = np.argsort(scores)[::-1]
        rows = []
        for local_index in order[:top_k]:
            score = float(scores[local_index])
            if score < min_score:
                continue
            row = self.chunks.iloc[int(candidate_positions[local_index])].to_dict()
            row["similarity"] = score
            rows.append(row)
        return pd.DataFrame(rows)


def blocked_document_exists(query: str, documents: pd.DataFrame, role: str) -> bool:
    """Heuristic check whether an unauthorized document may contain relevant terms.

    Used only to distinguish access denial from generic unknown fallback in the synthetic lab.
    """
    authorized = filter_documents_for_role(documents, role)
    blocked = documents.loc[~documents["doc_id"].isin(authorized["doc_id"])]
    terms = set(query.lower().replace("?", "").split())
    for text in blocked["content"].astype(str):
        if len(terms.intersection(text.lower().split())) >= 2:
            return True
    return False
