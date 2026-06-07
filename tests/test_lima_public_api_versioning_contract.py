from __future__ import annotations

import importlib
import json
import pathlib
import tomllib
from typing import Any, Mapping

import lima
import lima.kernel as lima_kernel


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "public_api" / "lima_public_api_manifest.json"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _manifest_text() -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture["paths"]["manifest"]).read_text(encoding="utf-8")


def test_public_api_manifest_fixture_is_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["manifest_scope"] == "public_api_versioning_metadata_only"
    assert fixture["lima_runtime_behavior_changed"] is False
    assert fixture["pyproject_modified"] is False
    assert fixture["top_level_runtime_exports_added"] is False
    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["consumer_integration_implemented"] is False
    assert fixture["production_readiness_claimed"] is False


def test_public_api_manifest_paths_exist() -> None:
    fixture = _load_fixture()

    for path in fixture["paths"].values():
        assert (REPO_ROOT / path).exists(), path


def test_public_api_manifest_matches_package_metadata() -> None:
    fixture = _load_fixture()
    pyproject = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == fixture["package"]["name"]
    assert pyproject["project"]["version"] == fixture["package"]["current_version"]
    assert pyproject["project"]["version"] == "0.0.1"
    assert pyproject["project"]["requires-python"] == fixture["package"]["python_requires"]
    assert (
        pyproject["tool"]["setuptools"]["packages"]["find"]["include"]
        == fixture["package"]["package_discovery"]
    )


def test_top_level_lima_exports_remain_narrow() -> None:
    fixture = _load_fixture()

    assert list(lima.__all__) == fixture["top_level"]["expected_all"]
    assert fixture["top_level"]["runtime_exports_allowed"] is False
    for symbol in fixture["top_level"]["forbidden_runtime_exports"]:
        assert not hasattr(lima, symbol)


def test_public_import_classifications_are_valid_and_documented() -> None:
    fixture = _load_fixture()
    text = _manifest_text()
    allowed_classifications = set(fixture["classification_values"])

    for entry in fixture["public_imports"]:
        assert entry["classification"] in allowed_classifications
        assert entry["execution_authority"] is False
        assert f"`{entry['import']}`" in text
        assert f"`{entry['classification']}`" in text


def test_manifest_covers_every_current_kernel_export() -> None:
    fixture = _load_fixture()
    manifest_symbols = {
        entry["symbol"]
        for entry in fixture["public_imports"]
        if entry["module"] == "lima.kernel" and entry["symbol"]
    }

    assert set(lima_kernel.__all__) == manifest_symbols


def test_public_imports_resolve_without_private_modules() -> None:
    fixture = _load_fixture()

    assert importlib.import_module("lima") is lima
    assert importlib.import_module("lima.kernel") is lima_kernel

    for entry in fixture["public_imports"]:
        if entry["symbol"] is None:
            continue
        module = importlib.import_module(entry["module"])
        assert hasattr(module, entry["symbol"]), entry["import"]


def test_proof_public_imports_are_limited_to_approved_symbols() -> None:
    fixture = _load_fixture()
    proof_public_symbols = {
        entry["symbol"]
        for entry in fixture["public_imports"]
        if entry["classification"] == "proof_public" and entry["symbol"]
    }

    assert proof_public_symbols == {
        "LimaKernel",
        "CapabilityProfile",
        "KernelRequest",
        "ExecutionResult",
        "KernelEvent",
        "GuardianStubDecision",
        "SimulatedDiscoveryAdapter",
    }


def test_forbidden_and_internal_consumer_imports_are_documented() -> None:
    fixture = _load_fixture()
    text = _manifest_text()

    for import_path in fixture["forbidden_consumer_imports"]:
        assert f"`{import_path}`" in text
    for import_path in fixture["experimental_internal_modules"]:
        assert f"`{import_path}`" in text


def test_consumer_pin_fields_and_branches_are_documented() -> None:
    fixture = _load_fixture()
    text = _manifest_text()

    for field in fixture["consumer_pin_fields"]:
        assert field in text
    for branch in fixture["consumer_branches"]:
        assert f"`{branch}`" in text


def test_non_execution_invariants_are_preserved_in_manifest() -> None:
    fixture = _load_fixture()
    text = _manifest_text()
    invariants = fixture["required_non_execution_invariants"]

    assert invariants["dry_run"] is True
    assert all(value is False for key, value in invariants.items() if key != "dry_run")

    for invariant_name, value in invariants.items():
        expected = "True" if value is True else "False"
        assert f"`{invariant_name} is {expected}`" in text


def test_forbidden_version_claims_and_surfaces_are_documented() -> None:
    fixture = _load_fixture()
    text = _manifest_text()

    for claim in fixture["forbidden_version_claims"]:
        assert claim in text
    for surface in fixture["forbidden_surfaces"]:
        assert surface in text


def test_manifest_points_to_next_audit_gate() -> None:
    fixture = _load_fixture()
    text = _manifest_text()

    assert fixture["next_review_gate"] == "audit-lima-public-api-versioning-metadata"
    assert f"`{fixture['next_review_gate']}`" in text
