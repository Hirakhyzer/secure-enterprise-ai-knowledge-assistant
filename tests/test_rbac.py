from enterprise_rag.rbac import filter_documents_for_role, is_authorized
from enterprise_rag.synthetic import generate_synthetic_documents


def test_employee_cannot_access_restricted_security_document():
    docs = generate_synthetic_documents()
    visible = filter_documents_for_role(docs, "employee")
    assert "SEC-001" not in set(visible["doc_id"])
    sec = docs.loc[docs["doc_id"] == "SEC-001"].iloc[0]
    assert not is_authorized("employee", sec["allowed_roles"])


def test_admin_can_access_all_documents():
    docs = generate_synthetic_documents()
    visible = filter_documents_for_role(docs, "admin")
    assert set(visible["doc_id"]) == set(docs["doc_id"])
