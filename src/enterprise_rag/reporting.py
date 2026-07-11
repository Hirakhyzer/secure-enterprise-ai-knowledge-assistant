"""Local reports for the synthetic enterprise RAG lab."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def write_lab_report(path: str | Path, metrics: dict[str, Any], results: pd.DataFrame) -> None:
    """Write a Markdown report with explicit synthetic/private-data boundary."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Secure Enterprise AI Knowledge Assistant — Synthetic Lab Report",
        "",
        "> **Synthetic-data warning:** all documents and queries are fictional. This report demonstrates private-RAG controls but is not an evaluation on real company documents.",
        "",
        "## Metrics",
        "",
    ]
    for key, value in metrics.items():
        lines.append(f"- **{key}**: `{value}`")
    lines.extend(["", "## Query outcomes", "", "| Query | Role | Status | Top document | Citation coverage | Hallucination risk |", "| --- | --- | --- | --- | ---: | --- |"])
    for row in results.itertuples(index=False):
        lines.append(f"| {row.query_id} | {row.role} | {row.status} | {row.top_doc_id} | {row.citation_coverage:.2f} | {row.hallucination_risk} |")
    lines.extend([
        "",
        "## Security boundary",
        "",
        "The assistant retrieves from role-authorized chunks only, cites chunk IDs, refuses insufficient or restricted questions, and writes a hash-linked audit log. It does not train on private documents or bypass document permissions.",
    ])
    destination.write_text("\n".join(lines), encoding="utf-8")
