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
    / "local_package_build_preflight"
    / "local_package_build_preflight.json"
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


def test_local_package_build_preflight_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_local_package_build_preflight_only"
    assert fixture["audit_status"] == "PASS"
    assert fixture["base_commit"] == "3965fc2105290d490adbe8ac77086be134b4fb76"


def test_local_package_build_preflight_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "design_path",
        "readiness_review_path",
        "independent_audit_path",
        "static_tests_audit_path",
        "package_metadata_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_package_metadata_still_declares_expected_build_backend_without_changes() -> None:
    fixture = _load_fixture()
    metadata = _package_metadata()

    assert metadata["build-system"]["build-backend"] == fixture["declared_build_backend"]
    assert fixture["declared_build_requirement"] in metadata["build-system"]["requires"]
    assert metadata["project"]["name"] == fixture["project_name"]
    assert metadata["project"]["version"] == fixture["project_version"]
    assert metadata["project"]["requires-python"] == fixture["requires_python"]
    assert fixture["package_include"] in metadata["tool"]["setuptools"]["packages"]["find"]["include"]


def test_preflight_design_preserves_failed_build_evidence() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _independent_audit_text()
    combined = "\n".join((design, audit))

    for evidence in fixture["failed_build_evidence"]:
        assert evidence in combined

    assert "This is a packaging-environment blocker, not a LIMA runtime safety blocker." in design
    assert "packaging-environment blocker, not a runtime defect" in audit


def test_preflight_design_keeps_proof_modes_separate() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _independent_audit_text()
    combined = "\n".join((design, audit))

    assert set(fixture["proof_modes"]) == {"mode_a", "mode_b", "mode_c", "mode_d"}
    for description in fixture["proof_modes"].values():
        assert description in combined

    assert "already passing but insufficient for wheel readiness" in audit
    assert "the next safest lane because it inspects environment readiness without installing or building" in audit
    assert "blocked behind explicit operator approval" in audit
    assert "blocked until the backend is available or an approved environment exists" in audit


def test_preflight_docs_forbid_install_build_publish_commands() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _readiness_review_text()
    audit = _independent_audit_text()
    combined = "\n".join((design, review, audit))

    for command in fixture["forbidden_commands"]:
        assert command in combined

    expected_command_boundary = (
        "must not run `pip " + "install`, `pip " + "wheel`, `python -m " + "build`"
    )
    assert expected_command_boundary in design
    assert "explicit operator approval" in combined


def test_preflight_docs_preserve_forbidden_runtime_and_consumer_surfaces() -> None:
    fixture = _load_fixture()
    design = _design_text()
    review = _readiness_review_text()
    audit = _independent_audit_text()
    combined = "\n".join((design, review, audit))
    normalized_combined = combined.replace("`", "")

    for surface in fixture["forbidden_surfaces"]:
        assert surface in normalized_combined

    assert "This preflight does not make LIMA ready for Sparkbot or Arc Bot." in design
    assert "This branch does not make LIMA ready for Sparkbot or Arc Bot." in audit


def test_future_package_build_acceptance_remains_evidence_based() -> None:
    fixture = _load_fixture()
    design = _design_text()
    audit = _independent_audit_text()
    combined = "\n".join((design, audit))

    for criterion in fixture["future_acceptance_criteria"]:
        assert criterion in combined

    assert "The exact filename must be verified from the produced artifact, not assumed" in design
    assert "do not overclaim package readiness" in audit


def test_static_test_lane_allowed_files_are_exact() -> None:
    fixture = _load_fixture()
    audit = _independent_audit_text()
    static_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in audit
        assert f"`{path}`" in static_audit

    assert "No `lima/`, package metadata, public export, example, consumer repo, or runtime behavior changes are made." in static_audit


def test_static_tests_do_not_use_subprocess_or_package_build_tools() -> None:
    test_source = pathlib.Path(__file__).read_text(encoding="utf-8")

    forbidden_imports = ("import " + "subprocess", "import " + "socket", "import " + "threading")
    forbidden_calls = (
        "pip " + "wheel",
        "pip " + "install",
        "python -m " + "build",
        "vir" + "tualenv",
    )

    for forbidden in forbidden_imports + forbidden_calls:
        assert forbidden not in test_source


def test_static_tests_recommend_independent_audit_next() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    assert fixture["recommended_next_branch"] == "audit-lima-local-package-build-preflight-static-tests"
    assert f"`{fixture['recommended_next_branch']}`" in static_audit
