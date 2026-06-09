from __future__ import annotations

import json
import pathlib
import tomllib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "build_backend_operator_response_archive"
    / "build_backend_operator_response_archive.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _design_text() -> str:
    return _text("design_path")


def _readiness_review_text() -> str:
    return _text("readiness_review_path")


def _independent_audit_text() -> str:
    return _text("independent_audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def _package_metadata() -> Mapping[str, Any]:
    fixture = _load_fixture()
    return tomllib.loads((REPO_ROOT / fixture["package_metadata_path"]).read_text(encoding="utf-8"))


def _combined_docs() -> str:
    return "\n".join((_design_text(), _readiness_review_text(), _independent_audit_text()))


def test_response_archive_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_build_backend_operator_response_archive_only"
    assert fixture["audit_status"] == "PASS"
    assert fixture["base_commit"] == "f0676c0c1c0e523aff2fd06ee982e15ff7dd6f4a"


def test_response_archive_fixture_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "design_path",
        "readiness_review_path",
        "independent_audit_path",
        "static_tests_audit_path",
        "package_metadata_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key

    for path in fixture["source_request_paths"]:
        assert (REPO_ROOT / path).exists(), path


def test_package_metadata_remains_declared_backend_without_workaround_change() -> None:
    fixture = _load_fixture()
    metadata = _package_metadata()

    assert metadata["build-system"]["build-backend"] == fixture["declared_build_backend"]
    assert fixture["declared_build_requirement"] in metadata["build-system"]["requires"]
    assert metadata["project"]["name"] == fixture["project_name"]
    assert metadata["project"]["version"] == fixture["project_version"]
    assert metadata["project"]["requires-python"] == fixture["requires_python"]
    assert fixture["package_include"] in metadata["tool"]["setuptools"]["packages"]["find"]["include"]


def test_current_backend_blocker_evidence_is_preserved() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for evidence in fixture["current_blocker_evidence"]:
        assert evidence in combined

    assert "This branch is design-only." in _design_text()
    assert "does not recommend package metadata changes" in _independent_audit_text()
    assert "no-network wheel build proof remains blocked" in _readiness_review_text()


def test_archive_principles_are_evidence_only_and_fail_closed() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for principle in fixture["archive_principles"]:
        assert principle in combined

    assert "archive boundary is properly separated from execution and build proof" in _independent_audit_text()
    assert "not convert prior planning text into approval" in _readiness_review_text()


def test_source_request_traceability_and_decision_set_are_preserved() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for path in fixture["source_request_paths"]:
        assert f"`{path}`" in combined

    for decision in fixture["operator_decisions"]:
        assert decision in combined

    assert "does not stand alone as implicit" in _independent_audit_text()
    assert "No archive path may infer approval from silence." in _design_text()


def test_required_archive_fields_are_documented_and_blocking() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for field in fixture["required_archive_fields"]:
        assert field in combined

    assert "Missing required archive fields must block any readiness or build-proof claim." in _design_text()
    assert "Missing required archive fields block readiness or build-proof claims." in _independent_audit_text()


def test_fail_closed_conditions_are_preserved() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for condition in fixture["fail_closed_conditions"]:
        assert condition in combined

    assert "The response archive remains fail-closed" in _independent_audit_text()
    assert "does not allow ambiguous authorization" in _independent_audit_text()


def test_redaction_contract_is_preserved() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for forbidden in fixture["redaction_forbidden_values"]:
        assert forbidden in combined

    for redacted_form in fixture["redacted_forms"]:
        assert redacted_form in _design_text()

    assert "The redaction contract is explicit enough for a later archive branch." in _independent_audit_text()


def test_future_archive_files_and_static_test_lane_are_narrow() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()
    static_audit = _static_tests_audit_text()

    for path in fixture["future_archive_allowed_files"]:
        assert path in combined

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in _readiness_review_text()
        assert f"`{path}`" in _independent_audit_text()
        assert f"`{path}`" in static_audit

    assert "No `lima/`, package metadata, public export, example, consumer repo, approval response, or runtime behavior changes are made." in static_audit


def test_install_build_publish_commands_remain_forbidden() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for command in fixture["forbidden_commands"]:
        assert command in combined

    assert "`pip " + "install`" in combined
    assert "`pip " + "wheel`" in combined
    assert "`python -m " + "build`" in combined
    assert "does not authorize dependency installation" in _independent_audit_text()


def test_runtime_consumer_and_physical_surfaces_remain_forbidden() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for surface in fixture["forbidden_surfaces"]:
        assert surface in combined

    assert "Forbidden until separately approved:" in _readiness_review_text()
    assert "The design does not approve forbidden surfaces." in _independent_audit_text()


def test_conditional_next_branches_do_not_skip_response_content() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _independent_audit_text()

    for branch in fixture["conditional_next_branches"].values():
        assert f"`{branch}`" in design
        assert f"`{branch}`" in audit

    assert "The design keeps next work conditional on actual response content" in audit
    assert "does not proceed directly to install or" in audit


def test_sparkbot_arc_remaining_blockers_stay_documented() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for blocker in fixture["remaining_blockers"]:
        assert blocker in combined

    assert "This design does not make LIMA ready for Sparkbot or Arc Bot." in _design_text()
    assert "This design does not make LIMA ready for Sparkbot or Arc Bot." in _independent_audit_text()


def test_static_tests_do_not_import_or_use_execution_surfaces() -> None:
    test_source = pathlib.Path(__file__).read_text(encoding="utf-8")
    forbidden_imports = ("import " + "subprocess", "import " + "socket", "import " + "threading")
    forbidden_calls = (
        "pip " + "install",
        "pip " + "wheel",
        "python -m " + "build",
        "vir" + "tualenv",
    )

    for forbidden in forbidden_imports + forbidden_calls:
        assert forbidden not in test_source


def test_static_tests_recommend_independent_audit_next() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    assert (
        fixture["recommended_next_branch"]
        == "audit-lima-build-backend-operator-response-archive-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_audit
