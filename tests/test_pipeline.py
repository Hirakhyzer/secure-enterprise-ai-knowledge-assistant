from enterprise_rag.chunking import chunk_documents
from enterprise_rag.evaluation import evaluate_runs
from enterprise_rag.generation import answer_from_context
from enterprise_rag.hallucination import hallucination_report
from enterprise_rag.retrieval import TfidfRetriever
from enterprise_rag.synthetic import generate_synthetic_documents, synthetic_queries


def test_synthetic_lab_core_pipeline_produces_metrics():
    docs = generate_synthetic_documents()
    chunks = chunk_documents(docs)
    retriever = TfidfRetriever(chunks).fit()
    rows = []
    for query in synthetic_queries().itertuples(index=False):
        retrieved = retriever.retrieve(query.query, query.role)
        response = answer_from_context(query.query, retrieved, docs, query.role)
        grounding = hallucination_report(response["answer"], response["citations"], retrieved)
        rows.append({
            "query_id": query.query_id,
            "role": query.role,
            "status": response["status"],
            "top_doc_id": retrieved.iloc[0]["doc_id"] if not retrieved.empty else "NONE",
            "expected_doc_id": query.expected_doc_id,
            "expected_refusal": query.expected_refusal,
            "unauthorized_doc_returned": 0,
            **grounding,
        })
    import pandas as pd
    metrics = evaluate_runs(pd.DataFrame(rows))
    assert metrics["query_count"] == len(rows)
    assert 0 <= metrics["access_control_correctness"] <= 1
    assert 0 <= metrics["mean_citation_coverage"] <= 1
