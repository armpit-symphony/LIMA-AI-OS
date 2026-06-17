"""Tests for the V1-G22 final public API freeze fixture."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g22_final_public_api_freeze.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _frozen_surfaces() -> dict[str, list[str]]:
    fixture = _load_fixture()
    surfaces: dict[str, list[str]] = {}
    surfaces.update(fixture["public_package_surfaces"])
    surfaces.update(fixture["public_subpackage_export_surfaces"])
    return surfaces


def test_v1_g22_fixture_records_candidate_final_api_freeze_scope() -> None:
    fixture = _load_fixture()

    assert fixture["freeze_packet_id"] == "v1_g22_final_public_api_freeze"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g22-final-public-api-freeze"
    assert fixture["approved_scope"] == "final_public_api_freeze_docs_tests_fixtures_slice"
    assert fixture["final_public_api_freeze_docs_tests_fixtures_added"] is True
    assert fixture["freeze_scope"]["scope_type"] == "docs_tests_fixtures_only"
    assert "sparkbot" in fixture["freeze_scope"]["consumer_targets"]
    assert "arc_bot" in fixture["freeze_scope"]["consumer_targets"]


def test_v1_g22_boundary_flags_remain_non_executing() -> None:
    fixture = _load_fixture()

    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["runtime_export_cleanup_added"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["product_ready"] is False


def test_v1_g22_public_surface_modules_are_frozen() -> None:
    surfaces = _frozen_surfaces()

    assert set(surfaces) == {
        "lima",
        "lima.contracts",
        "lima.kernel",
        "lima.guardian",
        "lima.spine",
        "lima.persistence",
        "lima.shells.contracts",
        "lima.harness",
        "lima.adapters",
    }


def test_v1_g22_frozen_all_exports_match_current_modules() -> None:
    for module_name, expected_exports in _frozen_surfaces().items():
        module = importlib.import_module(module_name)

        assert list(getattr(module, "__all__")) == expected_exports


def test_v1_g22_frozen_subpackage_symbols_are_importable() -> None:
    surfaces = _frozen_surfaces()

    for module_name, expected_exports in surfaces.items():
        module = importlib.import_module(module_name)
        for symbol_name in expected_exports:
            if module_name == "lima":
                importlib.import_module(f"lima.{symbol_name}")
            else:
                assert hasattr(module, symbol_name), f"{module_name}.{symbol_name}"


def test_v1_g22_runtime_symbols_are_exported_by_expected_modules() -> None:
    fixture = _load_fixture()
    surfaces = _frozen_surfaces()

    gates = {entry["gate"] for entry in fixture["v1_runtime_symbol_surfaces"]}
    assert gates == {
        "V1-G11",
        "V1-G12",
        "V1-G14",
        "V1-G15",
        "V1-G16",
        "V1-G17",
        "V1-G18",
        "V1-G19",
        "V1-G20",
        "V1-G21",
    }

    for entry in fixture["v1_runtime_symbol_surfaces"]:
        module_name = entry["module"]
        module = importlib.import_module(module_name)
        for symbol_name in entry["symbols"]:
            assert symbol_name in surfaces[module_name]
            assert hasattr(module, symbol_name)


def test_v1_g22_candidate_export_inventory_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["candidate_export_inventory_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g22_consumer_and_import_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["consumer_compatibility_refs"]:
        assert (REPO_ROOT / relative_path).exists()
    for relative_path in fixture["import_surface_expectation_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g22_future_change_and_cleanup_policies_are_gated() -> None:
    fixture = _load_fixture()

    backward_policy = fixture["backward_compatibility_policy"]
    future_policy = fixture["future_change_gate_policy"]
    cleanup_policy = fixture["runtime_export_cleanup_policy"]

    assert backward_policy["current_exports_frozen"] is True
    assert backward_policy["symbol_removal_requires_future_gate"] is True
    assert backward_policy["symbol_rename_requires_future_gate"] is True
    assert backward_policy["consumer_breakage_requires_stop"] is True
    assert future_policy["future_public_api_change_requires_approval"] is True
    assert future_policy["runtime_export_cleanup_requires_separate_approval"] is True
    assert future_policy["consumer_repo_edits_require_separate_approval"] is True
    assert future_policy["live_import_calls_require_separate_approval"] is True
    assert cleanup_policy["approved"] is False
    assert cleanup_policy["implemented"] is False
    assert cleanup_policy["requires_future_gate"] is True


def test_v1_g22_authority_boundaries_do_not_grant_execution() -> None:
    fixture = _load_fixture()

    guardian = fixture["guardian_boundary_confirmation"]
    approval = fixture["approval_boundary_confirmation"]
    provider_model = fixture["provider_model_route_boundary_confirmation"]

    assert guardian["compatible"] is True
    assert guardian["grants_authority"] is False
    assert guardian["execution_authority_added"] is False
    assert approval["compatible"] is True
    assert approval["approval_token_issued"] is False
    assert approval["raw_factor_verified"] is False
    assert provider_model["compatible"] is True
    assert provider_model["provider_model_calls_added"] is False
    assert provider_model["secret_lookup_added"] is False
    assert provider_model["model_dispatch_added"] is False


def test_v1_g22_required_confirmations_are_present() -> None:
    fixture = _load_fixture()

    assert fixture["no_consumer_repo_mutation_confirmation"] is True
    assert fixture["no_live_import_call_confirmation"] is True
    assert fixture["no_runtime_behavior_change_confirmation"] is True
    assert fixture["no_secret_credential_customer_data_confirmation"] is True
    assert fixture["proof_not_authority_confirmation"] is True


def test_v1_g22_audit_evidence_links_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["audit_evidence_linkage"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g22_docs_contain_required_boundary_language() -> None:
    implementation_text = (REPO_ROOT / "docs" / "V1_G22_FINAL_PUBLIC_API_FREEZE.md").read_text(
        encoding="utf-8"
    )
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G22_FINAL_PUBLIC_API_FREEZE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file was created" in implementation_text
    assert "Runtime export cleanup requires a separate approval gate" in implementation_text
    assert "consumer repo edits: not approved" in implementation_text
    assert "V1-G22 is complete" in closeout_text
    assert "No `lima/` runtime files were changed" in closeout_text
