"""Figures generated from local synthetic or authorized RAG runs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _path(path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def plot_retrieval_metrics(metrics: dict, path: str | Path) -> None:
    """Plot core synthetic-lab RAG control metrics."""
    keys = ["retrieval_accuracy_on_answerable_queries", "refusal_accuracy", "access_control_correctness", "mean_citation_coverage"]
    labels = ["Retrieval", "Refusal", "Access control", "Citation coverage"]
    values = [float(metrics.get(key, 0.0)) for key in keys]
    figure, axis = plt.subplots(figsize=(7.8, 4.8))
    axis.bar(labels, values)
    axis.set_ylim(0, 1.05)
    axis.set_ylabel("Score")
    axis.set_title("Synthetic enterprise RAG control metrics")
    axis.grid(True, axis="y", alpha=0.25)
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)


def plot_query_status(results: pd.DataFrame, path: str | Path) -> None:
    """Plot outcome statuses across synthetic role queries."""
    counts = results["status"].value_counts().sort_values(ascending=True)
    figure, axis = plt.subplots(figsize=(7.8, 4.8))
    axis.barh(counts.index, counts.values)
    axis.set_xlabel("Query count")
    axis.set_title("RAG query outcomes by policy status")
    axis.grid(True, axis="x", alpha=0.25)
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)


def plot_access_matrix(documents: pd.DataFrame, path: str | Path) -> None:
    """Plot role-document access matrix for the synthetic corpus."""
    roles = sorted({role for roles in documents["allowed_roles"] for role in roles})
    matrix = []
    for doc in documents.itertuples(index=False):
        matrix.append([1 if role in doc.allowed_roles else 0 for role in roles])
    figure, axis = plt.subplots(figsize=(9, 5.5))
    image = axis.imshow(matrix, aspect="auto")
    axis.set_xticks(range(len(roles))); axis.set_xticklabels(roles, rotation=45, ha="right")
    axis.set_yticks(range(len(documents))); axis.set_yticklabels(documents["doc_id"].tolist())
    axis.set_title("Synthetic role-document access matrix")
    figure.colorbar(image, ax=axis, label="Allowed")
    figure.tight_layout(); figure.savefig(_path(path), dpi=260); plt.close(figure)
