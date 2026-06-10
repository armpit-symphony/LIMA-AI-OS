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
    / "package_proof_ledger"
    / "package_proof_ledger.json"
)


def _fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _ledger_text() -> str:
    return (REPO_ROOT / _fixture()["ledger_path"]).read_text(encoding="utf-8")


def _package_metadata() -> Mapping[str, Any]:
    return tomllib.loads((REPO_ROOT / _fixture()["package_metadata_path"]).read_text(encoding="utf-8"))


def test_package_proof_ledger_fixture_paths_exist() -> None:
    fixture = _fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_package_proof_ledger_only"
    assert (REPO_ROOT / fixture["ledger_path"]).exists()
    assert (REPO_ROOT / fixture["package_metadata_path"]).exists()


def test_package_metadata_matches_ledger_claims() -> None:
    fixture = _fixture()
    metadata = _package_metadata()

    assert metadata["project"]["name"] == fixture["package_name"]
    assert metadata["project"]["version"] == fixture["package_version"]
    assert metadata["build-system"]["build-backend"] == fixture["declared_build_backend"]
    assert fixture["declared_build_requirement"] in metadata["build-system"]["requires"]


def test_ledger_records_build_install_and_import_proofs_without_artifacts() -> None:
    fixture = _fixture()
    ledger = _ledger_text()

    assert "controlled local environment" in ledger
    assert "Wheel and sdist were built successfully" in ledger
    assert "pip " + "install --no-index --find-links <artifact-root> lima-runtime==0.0.1" in ledger

    for proof in fixture["import_proofs"]:
        assert proof in ledger

    for artifact_rule in fixture["artifact_forbidden_patterns"]:
        assert artifact_rule in ledger

    assert "Package artifacts are proof evidence only and must not be committed." in ledger


def test_ledger_tracks_license_warning_without_blocking_current_proof() -> None:
    fixture = _fixture()
    ledger = _ledger_text()

    assert fixture["known_warning"] in ledger
    assert fixture["known_warning_deadline"] in ledger
    assert "This warning is not a current package-proof blocker." in ledger
    assert "before release readiness" in ledger


def test_ledger_does_not_authorize_runtime_or_consumer_wiring() -> None:
    fixture = _fixture()
    ledger = _ledger_text()

    for statement in fixture["required_non_authorization_statements"]:
        assert statement in ledger

    for consumer in fixture["consumer_names"]:
        assert consumer in ledger

    for surface in fixture["forbidden_surfaces"]:
        assert surface in ledger

    assert "NOT_READY for runtime integration." in ledger
    assert "BLOCKED for consumer integration." in ledger
    assert "NOT_READY for product readiness." in ledger


def test_static_ledger_tests_do_not_use_execution_surfaces() -> None:
    source = pathlib.Path(__file__).read_text(encoding="utf-8")

    forbidden = (
        "import " + "subprocess",
        "import " + "socket",
        "import " + "threading",
        "pip " + "install",
        "python -m " + "build",
        "url" + "lib",
        "re" + "quests",
    )
    for item in forbidden:
        assert item not in source


def test_ledger_recommends_public_api_freeze_candidate_next() -> None:
    fixture = _fixture()
    ledger = _ledger_text()

    assert fixture["recommended_next_branch"] == "design-lima-public-api-freeze-candidate"
    assert f"`{fixture['recommended_next_branch']}`" in ledger
