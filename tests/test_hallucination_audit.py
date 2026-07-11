from pathlib import Path

import pandas as pd

from enterprise_rag.audit import append_audit_record, verify_audit_log
from enterprise_rag.hallucination import hallucination_report


def test_hallucination_report_flags_missing_citation():
    chunks = pd.DataFrame([{"text": "Employees may work remotely up to three days per week."}])
    report = hallucination_report("Employees may work remotely up to three days per week.", [], chunks)
    assert report["hallucination_risk"]
    assert report["citation_coverage"] == 0.0


def test_audit_log_verifies_hash_chain(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_audit_record(path, {"query_id": "Q-1", "status": "answered"})
    append_audit_record(path, {"query_id": "Q-2", "status": "refused"})
    status = verify_audit_log(path)
    assert status["valid"]
    assert status["records"] == 2
