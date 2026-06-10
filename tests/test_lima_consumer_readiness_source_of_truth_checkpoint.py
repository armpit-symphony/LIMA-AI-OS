from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "consumer_readiness_source_of_truth_checkpoint"
    / "consumer_readiness_source_of_truth_checkpoint.json"
)


def _fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _checkpoint_text() -> str:
    return (REPO_ROOT / _fixture()["checkpoint_path"]).read_text(encoding="utf-8")


def _audit_text() -> str:
    return (REPO_ROOT / _fixture()["audit_path"]).read_text(encoding="utf-8")


def test_checkpoint_fixture_paths_exist() -> None:
    fixture = _fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["checkpoint_scope"] == "consumer_readiness_source_of_truth"
    assert (REPO_ROOT / fixture["checkpoint_path"]).exists()
    assert (REPO_ROOT / fixture["audit_path"]).exists()


def test_checkpoint_covers_required_consumer_families() -> None:
    fixture = _fixture()
    text = _checkpoint_text()

    for consumer in fixture["covered_consumers"]:
        assert consumer in text

    assert "future bot, shell, workstation, service, device, robot, drone, and office automation shells" in text


def test_checkpoint_declares_consumer_repos_proof_only() -> None:
    text = _checkpoint_text()

    assert "Consumer repositories are readiness/proof-only right now." in text
    assert "All consumer repos remain blocked from runtime integration." in text
    assert "consumer integration remains blocked" in text


def test_required_gates_block_consumer_runtime_integration() -> None:
    fixture = _fixture()
    text = _checkpoint_text()

    for gate in fixture["required_gates_before_consumer_integration"]:
        assert gate in text

    assert "No consumer repo may integrate LIMA runtime paths until all of the following are complete" in text
    assert "no package proof means no consumer runtime integration" in text
    assert "no isolated install proof means no consumer runtime integration" in text
    assert "no public API freeze means no consumer runtime integration" in text
    assert "no consumer-owned proof packet audit means no consumer runtime integration" in text


def test_forbidden_surfaces_remain_blocked_until_gates_pass() -> None:
    fixture = _fixture()
    text = _checkpoint_text()

    for surface in fixture["forbidden_until_gates_pass"]:
        assert surface in text

    assert "operator-approved controlled local build-backend environment" in text
    assert "does not authorize:" in text


def test_allowed_consumer_posture_is_readiness_only() -> None:
    fixture = _fixture()
    text = _checkpoint_text()

    for item in fixture["allowed_consumer_posture"]:
        assert item in text

    assert "prepare repo-owned proof plans" in text
    assert "prepare redacted proof packet drafts" in text


def test_audit_records_checkpoint_as_source_of_truth() -> None:
    text = _audit_text()

    assert "PASS." in text
    assert "source-of-truth checkpoint" in text
    assert "No consumer repo may integrate LIMA runtime paths" in text
    assert "build-backend approval does not authorize consumer integration" in text


def test_static_checkpoint_tests_do_not_use_execution_surfaces() -> None:
    source = pathlib.Path(__file__).read_text(encoding="utf-8")

    forbidden = (
        "import " + "subprocess",
        "import " + "socket",
        "import " + "threading",
        "pip " + "install",
        "python -m " + "build",
    )
    for item in forbidden:
        assert item not in source


def test_checkpoint_recommends_operator_response_archive_next() -> None:
    fixture = _fixture()
    text = _checkpoint_text()

    assert fixture["recommended_next_branch"] == "archive-lima-build-backend-operator-response"
    assert f"`{fixture['recommended_next_branch']}`" in text
