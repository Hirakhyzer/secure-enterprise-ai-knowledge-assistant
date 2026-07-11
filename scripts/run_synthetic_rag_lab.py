"""Run the complete synthetic secure enterprise RAG laboratory.

This command uses only fictional documents and queries. It demonstrates RBAC,
retrieval, citation-grounded answering, hallucination checks, audit trails, and
local reporting without using any private enterprise data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.audit import append_audit_record, verify_audit_log
from enterprise_rag.chunking import chunk_documents
from enterprise_rag.config import ensure_output_dirs, set_seed
from enterprise_rag.evaluation import evaluate_runs
from enterprise_rag.generation import answer_from_context
from enterprise_rag.hallucination import hallucination_report
from enterprise_rag.rbac import is_authorized
from enterprise_rag.reporting import write_lab_report
from enterprise_rag.retrieval import TfidfRetriever
from enterprise_rag.synthetic import SyntheticCorpusConfig, generate_synthetic_documents, synthetic_queries
from enterprise_rag.visualization import plot_access_matrix, plot_query_status, plot_retrieval_metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic private enterprise RAG security lab.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--top-k", type=int, default=4)
    args = parser.parse_args()

    set_seed(args.seed)
    documents = generate_synthetic_documents(SyntheticCorpusConfig(seed=args.seed))
    chunks = chunk_documents(documents)
    retriever = TfidfRetriever(chunks).fit()
    queries = synthetic_queries()
    outputs = ensure_output_dirs(args.output_dir)
    audit_path = outputs["audit"] / "query_audit_log.jsonl"

    rows: list[dict] = []
    answers: list[dict] = []
    for query in queries.itertuples(index=False):
        retrieved = retriever.retrieve(query.query, query.role, top_k=args.top_k)
        response = answer_from_context(query.query, retrieved, documents, query.role)
        grounding = hallucination_report(response["answer"], response["citations"], retrieved)
        top_doc_id = str(retrieved.iloc[0]["doc_id"]) if not retrieved.empty else "NONE"
        unauthorized_doc_returned = 0
        for doc_id in retrieved["doc_id"].tolist() if not retrieved.empty else []:
            doc = documents.loc[documents["doc_id"] == doc_id].iloc[0]
            if not is_authorized(query.role, doc["allowed_roles"]):
                unauthorized_doc_returned = 1
        record = {
            "query_id": query.query_id,
            "role": query.role,
            "query": query.query,
            "status": response["status"],
            "top_doc_id": top_doc_id,
            "retrieved_chunk_ids": retrieved["chunk_id"].tolist() if not retrieved.empty else [],
            "citation_count": len(response["citations"]),
            "citation_coverage": grounding["citation_coverage"],
            "unsupported_claim_score": grounding["unsupported_claim_score"],
            "hallucination_risk": grounding["hallucination_risk"],
            "expected_doc_id": query.expected_doc_id,
            "expected_refusal": int(query.expected_refusal),
            "unauthorized_doc_returned": unauthorized_doc_returned,
        }
        append_audit_record(audit_path, {**record, "policy_boundary": "synthetic lab; RBAC filtered before retrieval"})
        rows.append(record)
        answers.append({**record, "answer": response["answer"], "citations": json.dumps(response["citations"])})

    results = pd.DataFrame(rows)
    answer_table = pd.DataFrame(answers)
    metrics = evaluate_runs(results)
    metrics["audit_log"] = verify_audit_log(audit_path)
    documents.to_csv(outputs["results"] / "synthetic_documents.csv", index=False)
    chunks.to_csv(outputs["results"] / "synthetic_chunks.csv", index=False)
    queries.to_csv(outputs["results"] / "synthetic_queries.csv", index=False)
    results.to_csv(outputs["results"] / "synthetic_rag_results.csv", index=False)
    answer_table.to_csv(outputs["results"] / "synthetic_rag_answers.csv", index=False)
    (outputs["results"] / "synthetic_rag_summary.json").write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    write_lab_report(outputs["reports"] / "synthetic_rag_report.md", metrics, results)
    plot_retrieval_metrics(metrics, outputs["figures"] / "synthetic_rag_metrics.png")
    plot_query_status(results, outputs["figures"] / "synthetic_query_status.png")
    plot_access_matrix(documents, outputs["figures"] / "synthetic_access_matrix.png")
    print(json.dumps(metrics, indent=2, default=str))


if __name__ == "__main__":
    main()
