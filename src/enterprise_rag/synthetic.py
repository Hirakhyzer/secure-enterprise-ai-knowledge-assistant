"""Synthetic enterprise document corpus for safe private-RAG experimentation.

All documents, departments, policies, and identifiers are fictional. The corpus
allows role-based access, citation, refusal, hallucination, and audit workflows to
run without any real company data.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class SyntheticCorpusConfig:
    """Controls reproducible synthetic enterprise corpus generation."""

    seed: int = 42
    include_restricted_docs: bool = True


DOCS = [
    {
        "doc_id": "HR-001",
        "title": "Hybrid Work and Leave Policy",
        "department": "hr",
        "classification": "internal",
        "allowed_roles": ["employee", "manager", "hr", "admin"],
        "content": "Employees may work remotely up to three days per week with manager approval. Annual leave requests should be submitted at least ten business days before the requested start date. Managers must document exceptions in the HR portal. Sick leave does not require advance notice, but employees should notify their manager as soon as practical.",
    },
    {
        "doc_id": "FIN-001",
        "title": "Expense Reimbursement and Approval Policy",
        "department": "finance",
        "classification": "confidential",
        "allowed_roles": ["finance", "manager", "admin"],
        "content": "Expense reports above 5000 credits require finance director approval. Travel reimbursement requires receipts, business purpose, and cost center. Personal purchases are not reimbursable. Finance reviewers must reject missing receipts unless an approved exception is attached.",
    },
    {
        "doc_id": "ENG-001",
        "title": "Production Deployment Runbook",
        "department": "engineering",
        "classification": "internal",
        "allowed_roles": ["engineer", "security_analyst", "admin"],
        "content": "Production deployments require a peer-reviewed change request, automated test evidence, rollback plan, and on-call owner. Database migrations must be reversible or include a validated restoration plan. Emergency deployments require incident commander approval and post-incident review.",
    },
    {
        "doc_id": "SEC-001",
        "title": "Secure Access Standard",
        "department": "security",
        "classification": "restricted",
        "allowed_roles": ["security_analyst", "admin"],
        "content": "Privileged access requires multi-factor authentication, ticket justification, and quarterly access review. Service accounts must have named owners, scoped permissions, and rotation evidence. Secrets must be stored in the approved vault and never in source code, chat, or shared documents.",
    },
    {
        "doc_id": "SUP-001",
        "title": "Customer Support Escalation FAQ",
        "department": "support",
        "classification": "internal",
        "allowed_roles": ["employee", "manager", "support", "admin"],
        "content": "Support agents should escalate billing disputes to finance operations after verifying the customer identity. Product defects with reproducible steps should be linked to an engineering ticket. Security-sensitive customer reports must be escalated to the security response queue within one business hour.",
    },
    {
        "doc_id": "LEG-001",
        "title": "Contract Review and Data Processing Memo",
        "department": "legal",
        "classification": "confidential",
        "allowed_roles": ["legal", "manager", "admin"],
        "content": "Contracts involving personal data require legal review, data-processing terms, retention limits, and vendor security assessment. Non-standard indemnity clauses require counsel approval. Customer audit requests must be routed through legal operations before documents are shared externally.",
    },
    {
        "doc_id": "IR-001",
        "title": "Incident Response Coordination Guide",
        "department": "security",
        "classification": "restricted",
        "allowed_roles": ["security_analyst", "legal", "admin"],
        "content": "Incident responders must preserve evidence, assign an incident commander, record timeline decisions, and avoid unapproved destructive actions. Legal counsel should be notified for incidents involving regulated data. External communication requires executive and legal approval.",
    },
    {
        "doc_id": "EXEC-001",
        "title": "Board Financial Planning Summary",
        "department": "executive",
        "classification": "restricted",
        "allowed_roles": ["admin", "finance", "legal"],
        "content": "Quarterly planning assumes conservative revenue growth and delayed infrastructure expansion. Headcount requests above the approved plan require finance review and executive committee approval. This summary is restricted to authorized finance, legal, and executive administrators.",
    },
]


def generate_synthetic_documents(config: SyntheticCorpusConfig | None = None) -> pd.DataFrame:
    """Return a fictional document inventory with role-access metadata."""
    cfg = config or SyntheticCorpusConfig()
    docs = DOCS if cfg.include_restricted_docs else [doc for doc in DOCS if doc["classification"] != "restricted"]
    return pd.DataFrame(docs)


def synthetic_queries() -> pd.DataFrame:
    """Return labelled query scenarios for retrieval, RBAC, and refusal evaluation."""
    return pd.DataFrame([
        {"query_id": "Q-001", "role": "employee", "query": "How many days per week may I work remotely?", "expected_doc_id": "HR-001", "expected_refusal": 0},
        {"query_id": "Q-002", "role": "finance", "query": "When does an expense report require finance director approval?", "expected_doc_id": "FIN-001", "expected_refusal": 0},
        {"query_id": "Q-003", "role": "engineer", "query": "What evidence is required before production deployment?", "expected_doc_id": "ENG-001", "expected_refusal": 0},
        {"query_id": "Q-004", "role": "employee", "query": "What are the privileged access requirements?", "expected_doc_id": "SEC-001", "expected_refusal": 1},
        {"query_id": "Q-005", "role": "legal", "query": "Who should review contracts involving personal data?", "expected_doc_id": "LEG-001", "expected_refusal": 0},
        {"query_id": "Q-006", "role": "security_analyst", "query": "What should incident responders preserve?", "expected_doc_id": "IR-001", "expected_refusal": 0},
        {"query_id": "Q-007", "role": "employee", "query": "What is the company's cafeteria menu?", "expected_doc_id": "NONE", "expected_refusal": 1},
    ])
