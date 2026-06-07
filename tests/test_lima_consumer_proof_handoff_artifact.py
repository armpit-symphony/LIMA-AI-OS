from __future__ import annotations

import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
ARTIFACT_PATH = REPO_ROOT / "docs" / "handoffs" / "LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md"
EXPECTED_INVARIANTS = {
    "`executable is False`",
    "`execution_allowed is False`",
    "`side_effects_allowed is False`",
    "`dispatch_allowed is False`",
    "`persistence_allowed is False`",
    "`dry_run is True`",
    "`model_calls_allowed is False`",
    "`model_calls_executed is False`",
    "`live_discovery_executed is False`",
    "`connection_attempted is False`",
    "`pairing_attempted is False`",
    "`credentials_used is False`",
    "`session_opened is False`",
    "`device_control_executed is False`",
    "`physical_world_allowed is False`",
    "`physical_world_executed is False`",
    "`guardian_decision_created is False`",
    "`approval_enforced is False`",
    "`humaninput_bridge_active is False`",
    "`sparkbot_wiring_active is False`",
    "`robo_os_wiring_active is False`",
    "`adapter_active is False`",
    "`tool_execution_allowed is False`",
    "`driver_execution_allowed is False`",
    "`scheduler_active is False`",
    "`external_calls_allowed is False`",
}
EXPECTED_FORBIDDEN_SURFACES = {
    "production Sparkbot integration",
    "production Arc Bot integration",
    "Sparkbot route wiring",
    "Arc route wiring",
    "raw natural-language parsing in LIMA",
    "runtime `IntentEnvelope` creation",
    "live HumanInput bridge",
    "real Guardian decisions",
    "approval enforcement",
    "provider routing",
    "model calls",
    "tool execution",
    "connector reads or writes",
    "storage or persistence",
    "scheduler or background workers",
    "external sends",
    "browser actions",
    "file mutation",
    "process execution",
    "network actions",
    "live discovery",
    "scanning",
    "WiFi connection attempts",
    "Bluetooth or BLE connection attempts",
    "USB or serial connection attempts",
    "MQTT, Matter, or mDNS calls",
    "pairing",
    "credential use or storage",
    "device control",
    "Robo-OS access",
    "robotics",
    "drones",
    "physical-world behavior",
}


def _artifact_text() -> str:
    return ARTIFACT_PATH.read_text(encoding="utf-8")


def test_consumer_proof_handoff_artifact_exists() -> None:
    assert ARTIFACT_PATH.exists()


def test_handoff_artifact_is_lima_local_and_not_production_ready() -> None:
    text = _artifact_text()

    assert "LIMA-local, archive-ready handoff note" in text
    assert "LIMA is ready for consumer-owned dry-run proof planning only." in text
    assert "LIMA is not production-ready for Sparkbot or Arc Bot." in text
    assert "This LIMA branch must not modify either repository." in text


def test_handoff_artifact_names_consumer_owned_branches() -> None:
    text = _artifact_text()

    assert "`sparkbot-lima-dry-run-boundary-proof`" in text
    assert "`arc-lima-dry-run-boundary-proof`" in text
    assert "Each branch must be created and owned in its consumer repository" in text


def test_handoff_artifact_includes_required_shared_proof_steps() -> None:
    text = _artifact_text()

    required_steps = {
        "Record the exact LIMA commit, package version, or import method.",
        "Build redacted already-normalized intent or task metadata locally.",
        "Build a default-deny `CapabilityProfile`.",
        "Call `LimaKernel.evaluate(...)` in dry-run mode.",
        "Optionally pass an explicit `SimulatedDiscoveryAdapter` only for synthetic preview metadata.",
        "Archive the dry-run `ExecutionResult` sample.",
        "Archive the non-execution invariant checklist.",
        "Archive evidence that no production route was wired.",
        "Archive a rollback or disable plan.",
        "Stop at the proof report.",
    }

    for step in required_steps:
        assert step in text


def test_handoff_artifact_has_distinct_sparkbot_and_arc_evidence() -> None:
    text = _artifact_text()

    assert "proof no raw chat text was sent to LIMA" in text
    assert "proof no public Sparkbot production route was wired" in text
    assert "proof no Sparkbot task was created or mutated" in text
    assert "proof no raw office-task text was sent to LIMA" in text
    assert "proof no customer record payload was sent to LIMA" in text
    assert "proof no Arc scheduler or background worker was triggered" in text


def test_handoff_artifact_blocks_raw_and_sensitive_inputs() -> None:
    text = _artifact_text()

    forbidden_inputs = {
        "raw prompts",
        "raw chat text",
        "raw office-task text",
        "raw customer records",
        "raw connector records",
        "raw provider payloads",
        "raw tool arguments",
        "credentials",
        "tokens",
        "passwords",
        "pairing codes",
        "live scan dumps",
        "private SSIDs",
        "raw Bluetooth MAC addresses",
        "raw IP or MAC addresses",
        "device serial numbers",
        "precise physical location",
        "robot or drone command payloads",
    }

    for forbidden_input in forbidden_inputs:
        assert forbidden_input in text


def test_handoff_artifact_requires_all_non_execution_invariants() -> None:
    text = _artifact_text()

    for invariant in EXPECTED_INVARIANTS:
        assert invariant in text


def test_handoff_artifact_explicitly_forbids_runtime_surfaces() -> None:
    text = _artifact_text()

    assert "The proof branches must not implement or trigger:" in text
    for surface in EXPECTED_FORBIDDEN_SURFACES:
        assert surface in text


def test_handoff_artifact_pseudo_flow_stops_at_proof_report() -> None:
    text = _artifact_text()

    assert "Consumer imports the LIMA dependency candidate." in text
    assert "Consumer builds redacted normalized metadata locally." in text
    assert "Consumer calls LimaKernel.evaluate(...)." in text
    assert "Consumer archives proof no forbidden surface was reached." in text
    assert "Consumer branch stops at proof report." in text


def test_handoff_artifact_lists_remaining_product_use_blockers() -> None:
    text = _artifact_text()

    blockers = {
        "real Guardian request and decision lifecycle",
        "approval enforcement implementation",
        "HumanInput bridge contract and implementation",
        "runtime `IntentEnvelope` creation contract and implementation",
        "provider/model boundary design and implementation",
        "tool execution boundary design and implementation",
        "connector boundary design and implementation",
        "scheduler/background-work boundary design and implementation",
        "event/spine persistence design",
        "storage interface implementation",
        "consumer-owned proof branch design and audit in each repo",
        "rollback and disable strategy",
    }

    for blocker in blockers:
        assert blocker in text


def test_handoff_artifact_recommends_independent_audit_next() -> None:
    text = _artifact_text()

    assert "`audit-lima-consumer-proof-handoff-artifact`" in text
    assert "independently audit this handoff artifact" in text
