from __future__ import annotations

import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
GAP_AUDIT = REPO_ROOT / "docs" / "readiness" / "LIMA_RELEASE_READINESS_GAP_AUDIT.md"
CHECKLIST = REPO_ROOT / "docs" / "readiness" / "LIMA_PACKAGE_RELEASE_CHECKLIST.md"
PYPROJECT = REPO_ROOT / "pyproject.toml"


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def test_release_readiness_gap_audit_exists_and_stays_not_ready() -> None:
    audit = _read(GAP_AUDIT)

    assert "Release readiness: `NOT_READY`." in audit
    assert "Package publish readiness: `NOT_READY`." in audit
    assert "Product readiness: `NOT_READY`." in audit
    assert "Runtime integration readiness: `NOT_READY`." in audit
    assert "`WAITING_ON_CONSUMER_PROOF_PACKET_RESPONSES`" in audit


def test_gap_audit_reviews_current_authoritative_sources() -> None:
    audit = _read(GAP_AUDIT)

    for source in (
        "docs/CURRENT_PROJECT_STATE.md",
        "docs/readiness/LIMA_READINESS_ROLLUP_AFTER_PACKAGE_PROOF.md",
        "docs/readiness/LIMA_PACKAGE_PROOF_LEDGER.md",
        "docs/readiness/LIMA_PUBLIC_API_FREEZE_CANDIDATE.md",
        "docs/public_api/LIMA_PUBLIC_API_MANIFEST.md",
        "docs/consumer_proof_packets/LIMA_CONSUMER_PROOF_PACKET_REQUEST_DELIVERY_RECORD.md",
        "pyproject.toml",
    ):
        assert f"`{source}`" in audit


def test_completed_inputs_are_proof_only_not_release_ready() -> None:
    audit = _read(GAP_AUDIT)

    for completed in (
        "controlled local build-backend verification passed",
        "wheel and sdist proof completed outside the repository",
        "isolated install/import proof completed with `--no-index`",
        "`from lima.kernel import LimaKernel` proof passed",
        "public API freeze candidate exists",
        "operator delivery confirmation is recorded as manual-delivery-only",
    ):
        assert completed in audit

    assert "They do not prove release readiness, consumer integration readiness, or product readiness." in audit


def test_blocking_gaps_cover_packets_api_freeze_metadata_artifacts_and_docs() -> None:
    audit = _read(GAP_AUDIT)

    for gap in (
        "Consumer proof packets",
        "Consumer proof audits",
        "Final public API freeze",
        "Package metadata warning",
        "Release version decision",
        "Artifact policy",
        "CI/release validation policy",
        "Consumer compatibility policy",
        "Install/onboarding docs",
        "Security/readiness attestation",
        "Product/site claims",
    ):
        assert gap in audit


def test_release_non_negotiables_keep_runtime_and_consumer_boundaries_closed() -> None:
    combined = "\n".join((_read(GAP_AUDIT), _read(CHECKLIST)))

    for boundary in (
        "Guardian remains mandatory.",
        "Sparkbot remains the reference shell/spec source.",
        "No consumer repo is touched by LIMA release work.",
        "No Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, or future shell wiring is added.",
        "No provider/model calls, tool execution, connectors, browser/file/network actions",
        "No top-level runtime exports are added without public API freeze approval.",
    ):
        assert boundary in combined


def test_package_release_checklist_records_current_package_identity() -> None:
    checklist = _read(CHECKLIST)
    pyproject = _read(PYPROJECT)

    assert 'name = "lima-runtime"' in pyproject
    assert 'version = "0.0.1"' in pyproject
    assert 'requires-python = ">=3.11"' in pyproject
    assert 'build-backend = "setuptools.build_meta"' in pyproject

    for expected in (
        "package name: `lima-runtime`",
        "current version: `0.0.1`",
        "Python requirement: `>=3.11`",
        "build backend: `setuptools.build_meta`",
        "license metadata warning: `unresolved_before_release_readiness`",
    ):
        assert expected in checklist


def test_checklist_keeps_public_api_candidate_only() -> None:
    checklist = _read(CHECKLIST)

    assert "public API status is `CANDIDATE_ONLY`" in checklist
    assert "top-level runtime exports are not approved" in checklist
    assert "consumer proof branches must use `from lima.kernel import <exported-name>`" in checklist


def test_checklist_keeps_consumer_packets_not_supplied() -> None:
    checklist = _read(CHECKLIST)

    for packet_state in (
        "Sparkbot proof packet: `not_supplied_yet`",
        "Arc Bot proof packet: `not_supplied_yet`",
        "LIMA Robo OS proof packet: `not_supplied_yet`",
        "LIMA Office proof packet: `not_supplied_yet`",
        "Future shell proof packet: `not_supplied_yet`",
    ):
        assert packet_state in checklist


def test_validation_and_release_decision_gates_are_explicit() -> None:
    checklist = _read(CHECKLIST)

    for command in (
        "focused package/release static tests",
        "`python -m compileall lima`",
        "`python -m pytest -q tests -p no:cacheprovider`",
        "`git diff --check`",
        "`git status --short --branch`",
        "independent release-readiness audit",
    ):
        assert command in checklist

    for forbidden in (
        "`publish_package_now`",
        "`claim_product_ready`",
        "`finalize_public_api_freeze_without_packet_audits`",
        "`wire_consumers`",
        "`enable_runtime_integration`",
        "`enable_physical_world_behavior`",
    ):
        assert forbidden in checklist


def test_release_work_stop_conditions_are_strict() -> None:
    audit = _read(GAP_AUDIT)

    for stop in (
        "publish a package",
        "tag a release",
        "finalize public API freeze",
        "touch consumer repositories",
        "change runtime behavior",
        "add provider/model routing",
        "expand Guardian authority",
        "activate HumanInput bridge",
        "add connectors, browser/file/network actions, external sends, live discovery, device control, robotics, drones, IoT",
    ):
        assert stop in audit
