"""Role-based access control and redaction helpers."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


ROLE_HIERARCHY = {
    "employee": {"employee"},
    "manager": {"employee", "manager"},
    "engineer": {"employee", "engineer"},
    "security_analyst": {"employee", "security_analyst"},
    "finance": {"employee", "finance"},
    "legal": {"employee", "legal"},
    "hr": {"employee", "hr"},
    "support": {"employee", "support"},
    "admin": {"employee", "manager", "engineer", "security_analyst", "finance", "legal", "hr", "support", "admin"},
}


def effective_roles(role: str) -> set[str]:
    """Return roles implied by a user role."""
    if role not in ROLE_HIERARCHY:
        raise ValueError(f"Unknown role: {role}")
    return set(ROLE_HIERARCHY[role])


def is_authorized(role: str, allowed_roles: Iterable[str]) -> bool:
    """Return whether a role can access an object with allowed roles."""
    return bool(effective_roles(role).intersection(set(allowed_roles)))


def filter_documents_for_role(documents: pd.DataFrame, role: str) -> pd.DataFrame:
    """Return only documents authorized for the given role."""
    return documents.loc[documents["allowed_roles"].apply(lambda roles: is_authorized(role, roles))].reset_index(drop=True)


def redact_restricted_fields(text: str) -> str:
    """Redact simple secret-like tokens from generated answers and logs.

    This is a demonstration redactor and not a complete data-loss-prevention system.
    """
    patterns = [
        (r"(?i)(secret|token|password|api[_-]?key)\s*[:=]\s*\S+", r"\1=[REDACTED]"),
        (r"\b[A-Z0-9]{20,}\b", "[REDACTED_TOKEN]"),
    ]
    output = text
    for pattern, replacement in patterns:
        output = re.sub(pattern, replacement, output)
    return output
