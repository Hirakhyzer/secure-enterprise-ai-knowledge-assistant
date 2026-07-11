from enterprise_rag.chunking import chunk_documents
from enterprise_rag.generation import answer_from_context
from enterprise_rag.retrieval import TfidfRetriever
from enterprise_rag.synthetic import generate_synthetic_documents


def test_authorized_query_returns_cited_answer():
    docs = generate_synthetic_documents()
    chunks = chunk_documents(docs)
    retriever = TfidfRetriever(chunks).fit()
    retrieved = retriever.retrieve("production deployment evidence", "engineer", top_k=3)
    response = answer_from_context("production deployment evidence", retrieved, docs, "engineer")
    assert response["status"] == "answered_from_context"
    assert response["citations"]
    assert "[ENG-001" in response["answer"]


def test_restricted_query_refuses_for_employee():
    docs = generate_synthetic_documents()
    chunks = chunk_documents(docs)
    retriever = TfidfRetriever(chunks).fit()
    retrieved = retriever.retrieve("privileged access requirements", "employee", top_k=3)
    response = answer_from_context("privileged access requirements", retrieved, docs, "employee")
    assert response["status"] in {"access_limited", "insufficient_evidence"}
    assert not response["citations"]
