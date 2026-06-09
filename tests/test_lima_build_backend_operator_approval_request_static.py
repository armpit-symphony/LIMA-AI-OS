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
    / "build_backend_operator_approval_request"
    / "build_backend_operator_approval_request.json"
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


def test_operator_approval_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_build_backend_operator_approval_request_only"
    assert fixture["audit_status"] == "PASS"
    assert fixture["base_commit"] == "f34e7abdd5f900912cb9fdf413635ea36b342f53"


def test_operator_approval_fixture_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "design_path",
        "readiness_review_path",
        "independent_audit_path",
        "static_tests_audit_path",
        "package_metadata_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_package_metadata_remains_declared_backend_without_workaround_change() -> None:
    fixture = _load_fixture()
    metadata = _package_metadata()

    assert metadata["build-system"]["build-backend"] == fixture["declared_build_backend"]
    assert fixture["declared_build_requirement"] in metadata["build-system"]["requires"]
    assert metadata["project"]["name"] == fixture["project_name"]
    assert metadata["project"]["version"] == fixture["project_version"]
    assert metadata["project"]["requires-python"] == fixture["requires_python"]
    assert fixture["package_include"] in metadata["tool"]["setuptools"]["packages"]["find"]["include"]


def test_design_preserves_current_backend_blocker_evidence() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for evidence in fixture["current_blocker_evidence"]:
        assert evidence in combined

    assert "This branch is design-only." in _design_text()
    assert "The design preserves:" in _readiness_review_text()
    assert "does not propose package metadata changes as a workaround" in _independent_audit_text()


def test_operator_decisions_are_explicit_and_fail_closed() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    assert set(fixture["operator_decisions"]) == {"option_a", "option_b", "option_c", "option_d"}
    for decision in fixture["operator_decisions"].values():
        assert decision in combined

    assert "If the operator does not explicitly approve one of these" in _design_text()
    assert "Silence or ambiguous approval is not treated as authorization." in _independent_audit_text()
    assert "does not treat silence or ambiguous approval as authorization" in _readiness_review_text()


def test_approval_record_template_fields_are_preserved() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _independent_audit_text()))

    for field in fixture["approval_template_fields"]:
        assert field in combined

    assert "Archive-ready operator response template:" in _design_text()
    assert "The template is sufficient to distinguish approval" in _independent_audit_text()


def test_required_evidence_after_approval_is_preserved() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for evidence in fixture["required_evidence_after_approval"]:
        assert evidence in combined

    assert "Missing evidence blocks package build readiness claims." in _design_text()
    assert "Missing evidence blocks package build readiness claims." in _independent_audit_text()


def test_future_verification_flow_stays_separate_and_blocker_aware() -> None:
    fixture = _load_fixture()
    combined = "\n".join((_design_text(), _independent_audit_text()))

    for step in fixture["future_verification_flow"]:
        assert step in combined

    assert "Archive approval response." in combined
    assert "If backend import fails, stop and record blocker." in combined
    assert "Keep artifacts outside the repo." in combined


def test_install_build_publish_commands_remain_forbidden() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for command in fixture["forbidden_commands"]:
        assert command in combined

    audit = _independent_audit_text()
    assert "does not authorize dependency installation" in audit
    assert "environment creation" in audit
    assert "`pip " + "install`" in audit
    assert "`pip " + "wheel`" in audit
    assert "`python -m " + "build`" in audit


def test_runtime_consumer_and_physical_surfaces_remain_forbidden() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for surface in fixture["forbidden_surfaces"]:
        assert surface in combined

    assert "No `lima/`, package metadata, test, fixture, example, public export, consumer repo" in _readiness_review_text()


def test_static_test_lane_allowed_files_are_exact() -> None:
    fixture = _load_fixture()
    readiness = _readiness_review_text()
    audit = _independent_audit_text()
    static_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in readiness
        assert f"`{path}`" in audit
        assert f"`{path}`" in static_audit

    assert "No `lima/`, package metadata, public export, example, consumer repo, approval response, or runtime behavior changes are made." in static_audit


def test_sparkbot_arc_remaining_blockers_stay_documented() -> None:
    fixture = _load_fixture()
    combined = _combined_docs()

    for blocker in fixture["remaining_blockers"]:
        assert blocker in combined

    assert "This approval request does not make LIMA ready for Sparkbot or Arc Bot." in _design_text()
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
        == "audit-lima-build-backend-operator-approval-request-static-tests"
    )
    assert f"`{fixture['recommended_next_branch']}`" in static_audit
