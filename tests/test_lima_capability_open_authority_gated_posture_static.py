"""Static checks for the LIMA capability-open authority-gated posture doc."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "LIMA_CAPABILITY_OPEN_AUTHORITY_GATED_MODEL.md"
)


def test_capability_open_authority_gated_doc_exists() -> None:
    assert DOC_PATH.exists()


def test_capability_open_authority_gated_required_language() -> None:
    text = DOC_PATH.read_text(encoding="utf-8").lower()

    assert "capability-open" in text
    assert "authority-gated" in text
    assert "guiderail" in text
    assert "approval" in text
    assert "destructive edit/delete" in text
    assert "physical-world" in text
    assert "consumer integration still requires" in text
    assert "not product readiness" in text
