"""Docs checks for the Phase 3.1 kernel pipeline fixture map."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "PHASE_3_1_NONPRODUCTION_KERNEL_PIPELINE_FIXTURE_MAP.md"


def test_kernel_pipeline_fixture_map_doc_exists_and_lists_required_boundaries() -> None:
    assert DOC_PATH.exists()

    text = DOC_PATH.read_text(encoding="utf-8")

    for fixture_dir in (
        "tests/fixtures/sparkbot_payloads/",
        "tests/fixtures/intent_envelopes/",
        "tests/fixtures/guardian_requests/",
        "tests/fixtures/fake_guardian_decisions/",
    ):
        assert fixture_dir in text

    for safety_gate in (
        "docs/ADAPTER_SAFETY_GATE.md",
        "docs/INTENTENVELOPE_SAFETY_GATE.md",
        "docs/GUARDIAN_REQUEST_SAFETY_GATE.md",
        "docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md",
    ):
        assert safety_gate in text

    for required_text in (
        "not an executable pipeline",
        "does not authorize actions",
        "does not persist audit data",
        "phase-3-2-nonproduction-kernel-pipeline-map-readiness-review",
    ):
        assert required_text in text
