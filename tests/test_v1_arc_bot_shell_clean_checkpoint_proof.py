"""Static checks for the V1 Arc-Bot-shell clean checkpoint proof."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_arc_bot_shell_clean_checkpoint_proof.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_arc_bot_shell_clean_checkpoint_fixture_and_doc_exist() -> None:
    fixture = _load_fixture()

    assert fixture["proof_id"] == "v1_arc_bot_shell_clean_checkpoint_proof"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["verdict"] == "PASS_ARC_BOT_SHELL_CLEAN_CHECKPOINT_RECORDED"
    assert (REPO_ROOT / fixture["document"]).exists()


def test_v1_arc_bot_shell_clean_checkpoint_records_commit_and_validation() -> None:
    fixture = _load_fixture()
    arc = fixture["arc_bot_shell"]

    assert arc["repository"] == "armpit-symphony/Arc-Bot-shell"
    assert arc["branch"] == "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
    assert arc["previous_dirty_checkpoint"] == "2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0"
    assert arc["clean_checkpoint_commit"] == "5932c579b75ebb85980f1a40cf1bf0306fe22c6a"
    assert arc["local_status_clean_after_push"] is True
    assert arc["pushed_to_origin"] is True
    assert fixture["validation"] == {
        "full_pytest": "326 passed",
        "compileall": "passed",
        "git_diff_check": "passed_with_line_ending_warnings_only",
        "git_diff_cached_check": "passed",
        "arc_worker_smoke": "27 passed",
    }


def test_v1_arc_bot_shell_clean_checkpoint_boundaries() -> None:
    boundaries = _load_fixture()["boundaries"]

    assert boundaries["arc_bot_shell_clean_checkpoint_proof_recorded"] is True
    for key, value in boundaries.items():
        if key == "arc_bot_shell_clean_checkpoint_proof_recorded":
            continue
        assert value is False, key


def test_v1_arc_bot_shell_clean_checkpoint_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["document"]).read_text(encoding="utf-8")

    assert "# V1 Arc-Bot-shell Clean Checkpoint Proof" in text
    assert fixture["verdict"] in text
    assert fixture["arc_bot_shell"]["clean_checkpoint_commit"] in text
    assert "326 passed" in text
    assert "27 passed" in text
    assert "LIMA remains `CANDIDATE_ONLY`" in text
    assert "V1.0.0 branch or tag authorized by this proof: no." in text


def test_v1_arc_bot_shell_clean_checkpoint_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["document"]).read_text(encoding="utf-8")

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
