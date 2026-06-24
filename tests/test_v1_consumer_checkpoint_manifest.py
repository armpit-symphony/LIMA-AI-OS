"""Static checks for the V1 consumer checkpoint manifest."""

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
    / "v1_consumer_checkpoint_manifest.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_consumer_checkpoint_manifest_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["manifest_id"] == "v1_consumer_checkpoint_manifest"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-24"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_manifest"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["lima_commit_under_audit"] == (
        "2f46248ea90fef5efcb49f3892c275dc64621f87"
    )
    assert fixture["manifest_verdict"] == "CONSUMER_CHECKPOINTS_CLEAN_CANDIDATE_ONLY"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_consumer_checkpoint_manifest_records_consumer_commits() -> None:
    checkpoints = _load_fixture()["consumer_checkpoints"]

    assert checkpoints["public_sparkbot"] == {
        "repository": "sparkpit-labs/Sparkbot",
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "local_status_clean": True,
        "release_proof_use": "candidate_smoke_checkpoint_only",
    }
    assert checkpoints["accessible_sparkbot"] == {
        "repository": "armpit-symphony/Sparkbot",
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "local_status_clean": True,
        "release_proof_use": "candidate_smoke_checkpoint_only",
    }
    assert checkpoints["sparkbot_shell"] == {
        "repository": "armpit-symphony/Sparkbot_shell",
        "local_path": "C:\\Users\\limap\\Sparkbot_shell",
        "branch": "sparkbot-shell-work-settings-runtime-preview",
        "commit": "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc",
        "local_status_clean": True,
        "release_proof_use": "shell_checkpoint_only",
    }
    assert checkpoints["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "529ac5177531a6d926186807ba8a0a9776ad7fbe",
        "local_status_clean": True,
        "clean_checkpoint_proof": "docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md",
        "release_proof_use": "clean_checkpoint_proof_recorded_candidate_only",
    }


def test_v1_consumer_checkpoint_manifest_requires_smoke_commands() -> None:
    commands = _load_fixture()["required_consumer_smoke_commands"]

    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["public_sparkbot"][0]
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["accessible_sparkbot"][0]
    assert commands["arc_bot_shell"][0] == ".\\scripts\\arc_worker_smoke.ps1"
    assert commands["arc_bot_shell"][1] == "python -m pytest -q -p no:cacheprovider"
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands["arc_bot_shell"][2]
    assert commands["arc_bot_shell"][4] == "git status --porcelain --untracked-files=all"
    assert commands["sparkbot_shell"] == [
        "git status --short --branch",
        "git diff --check",
    ]


def test_v1_consumer_checkpoint_manifest_preserves_boundaries() -> None:
    for key, value in _load_fixture()["required_false_boundaries"].items():
        if key == "arc_bot_shell_clean_checkpoint_proof_claimed_by_manifest":
            assert value is True
            continue
        assert value is False, key

    assert _load_fixture()["release_candidate_claim_allowed"] is False


def test_v1_consumer_checkpoint_manifest_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["manifest"]).read_text(encoding="utf-8")

    assert "# V1 Consumer Checkpoint Manifest" in text
    assert fixture["source_lima_commit_before_manifest"] in text
    assert fixture["lima_commit_under_audit"] in text
    assert "CONSUMER_CHECKPOINTS_CLEAN_CANDIDATE_ONLY" in text
    assert "sparkpit-labs/Sparkbot" in text
    assert "armpit-symphony/Sparkbot_shell" in text
    assert "armpit-symphony/Arc-Bot-shell" in text
    assert "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2" in text
    assert "ddaa4ccaacd328ddcc1f00a040c2c140abee428e" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "529ac5177531a6d926186807ba8a0a9776ad7fbe" in text
    assert "clean checkpoint proof recorded" in text
    assert "Final readiness audit executed by this manifest: false." in text
    assert "Arc-Bot-shell clean-checkpoint proof recorded by referenced audit: true." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: false." in text
    assert "Do not create a V1.0.0 release-candidate branch" in text


def test_v1_consumer_checkpoint_manifest_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["manifest"]).read_text(encoding="utf-8")

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