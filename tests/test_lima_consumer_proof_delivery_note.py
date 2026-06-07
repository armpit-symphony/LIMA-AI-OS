from __future__ import annotations

import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTE_PATH = REPO_ROOT / "docs" / "handoffs" / "LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md"
REQUIRED_LINKS = {
    "docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md",
    "docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md",
    "tests/fixtures/consumer_proof_archive_template/consumer_proof_archive_template.json",
    "docs/audits/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT_AUDIT.md",
    "docs/audits/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE_IMPLEMENTATION_FINAL_AUDIT.md",
}
REQUIRED_INVARIANTS = {
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


def _note_text() -> str:
    return NOTE_PATH.read_text(encoding="utf-8")


def test_delivery_note_exists_and_is_proof_only() -> None:
    text = _note_text()

    assert NOTE_PATH.exists()
    assert "LIMA has reached consumer-owned dry-run proof handoff readiness only." in text
    assert "This is not production integration approval." in text
    assert "LIMA is not production-ready for Sparkbot or Arc Bot integration." in text
    assert "Ready to deliver as proof-only guidance." in text
    assert "Not ready for production integration." in text


def test_delivery_note_points_to_approved_package_artifacts() -> None:
    text = _note_text()

    for link in REQUIRED_LINKS:
        assert f"`{link}`" in text
        assert (REPO_ROOT / link).exists(), link


def test_delivery_note_recommends_consumer_owned_branches() -> None:
    text = _note_text()

    assert "`sparkbot-lima-dry-run-boundary-proof`" in text
    assert "`arc-lima-dry-run-boundary-proof`" in text
    assert "These branches must be created and owned by their repo teams." in text
    assert "They are not owned by the LIMA repo lane." in text


def test_delivery_note_preserves_allowed_proof_shape() -> None:
    text = _note_text()

    required_phrases = {
        "already-normalized redacted metadata in",
        "default-deny capability profile",
        "LimaKernel.evaluate(...) dry-run call",
        "optional explicit SimulatedDiscoveryAdapter for synthetic preview only",
        "dry-run ExecutionResult out",
        "archive proof packet",
        "stop at repo-team audit",
    }
    for phrase in required_phrases:
        assert phrase in text


def test_delivery_note_includes_required_warning_language() -> None:
    text = _note_text()

    assert "This is a proof-only handoff." in text
    assert "Do not wire production routes." in text
    assert "Do not send raw prompts, raw chat, raw office-task text, customer records" in text
    assert "Do not expect LIMA to call models, tools, connectors, storage, schedulers" in text
    assert "The first proof is normalized metadata in and dry-run ExecutionResult out." in text


def test_delivery_note_carries_all_non_execution_invariants() -> None:
    text = _note_text()

    for invariant in REQUIRED_INVARIANTS:
        assert invariant in text


def test_delivery_note_blocks_forbidden_claims() -> None:
    text = _note_text()

    forbidden_claims = {
        "LIMA is production-ready",
        "Sparkbot is integrated with LIMA",
        "Arc Bot is integrated with LIMA",
        "LIMA can process raw chat or raw office-task text",
        "LIMA can create runtime `IntentEnvelope` records",
        "LIMA can create real Guardian decisions",
        "LIMA can enforce approval",
        "LIMA can route model/provider calls",
        "LIMA can execute tools",
        "LIMA can access connectors",
        "LIMA can persist events",
        "LIMA can schedule work",
        "LIMA can discover or connect to networks/devices",
        "LIMA can pair devices",
        "LIMA can use credentials",
        "LIMA can control devices, robots, drones, or physical-world systems",
    }

    assert "This delivery note does not claim:" in text
    for claim in forbidden_claims:
        assert claim in text


def test_delivery_note_blocks_forbidden_actions() -> None:
    text = _note_text()

    forbidden_actions = {
        "touch public Sparkbot repository files from this LIMA lane",
        "touch Arc Bot repository files from this LIMA lane",
        "modify `lima/`",
        "modify `tests/support/`",
        "implement consumer integration",
        "add route wiring",
        "add model/provider calls",
        "add tool execution",
        "add connector access",
        "add storage/persistence",
        "add event spine persistence",
        "add scheduler/background work",
        "add browser/file/process/network actions",
        "add live discovery",
        "add scanning",
        "add connection attempts",
        "add pairing",
        "add credential use or storage",
        "add sockets",
        "add Bluetooth/BLE APIs",
        "add USB/serial APIs",
        "add MQTT/Matter/mDNS APIs",
        "add Robo-OS access",
        "add device/robot/drone/physical-world behavior",
    }

    assert "This delivery note does not authorize LIMA or consumer teams to:" in text
    for action in forbidden_actions:
        assert action in text


def test_delivery_note_carries_remaining_blockers() -> None:
    text = _note_text()

    blockers = {
        "stable public API versioning policy",
        "stronger install/package verification if needed",
        "real Guardian request and decision lifecycle",
        "approval-required flow design",
        "approval enforcement implementation",
        "HumanInput bridge contract and implementation",
        "runtime `IntentEnvelope` creation contract and implementation",
        "provider/model boundary design and implementation",
        "tool execution boundary design and implementation",
        "connector boundary design and implementation",
        "scheduler/background-work boundary design and implementation",
        "event/spine persistence design",
        "storage interface implementation",
        "consumer-owned proof branch audit in each repo",
    }

    for blocker in blockers:
        assert blocker in text
