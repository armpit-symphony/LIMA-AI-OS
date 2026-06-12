from __future__ import annotations

import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DELIVERY_RECORD = (
    REPO_ROOT
    / "docs"
    / "consumer_proof_packets"
    / "LIMA_CONSUMER_PROOF_PACKET_REQUEST_DELIVERY_RECORD.md"
)
CURRENT_STATE = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"
READINESS_ROLLUP = (
    REPO_ROOT / "docs" / "readiness" / "LIMA_READINESS_ROLLUP_AFTER_PACKAGE_PROOF.md"
)
AUDIT_RECORD = (
    REPO_ROOT
    / "docs"
    / "audits"
    / "LIMA_CONSUMER_PROOF_PACKET_REQUEST_DELIVERY_RECORD_AUDIT.md"
)


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def test_delivery_record_exists_and_records_manual_confirmation_only() -> None:
    record = _read(DELIVERY_RECORD)

    assert "Operator confirmation received: 2026-06-12." in record
    assert "This record is manual delivery confirmation only." in record
    assert "`WAITING_ON_CONSUMER_PROOF_PACKET_RESPONSES`" in record
    assert "It does not mean consumer proof packets have been received" in record


def test_delivery_scope_names_all_requested_consumer_artifacts() -> None:
    record = _read(DELIVERY_RECORD)

    for artifact in (
        "SPARKBOT_LIMA_PROOF_PACKET_REQUEST.md",
        "ARC_BOT_LIMA_PROOF_PACKET_REQUEST.md",
        "LIMA_ROBO_OS_LIMA_PROOF_PACKET_REQUEST.md",
        "LIMA_OFFICE_LIMA_PROOF_PACKET_REQUEST.md",
        "FUTURE_SHELL_LIMA_PROOF_PACKET_TEMPLATE.md",
    ):
        assert artifact in record


def test_all_consumer_packets_remain_not_supplied() -> None:
    combined = "\n".join((_read(DELIVERY_RECORD), _read(AUDIT_RECORD)))

    for line in (
        "Sparkbot proof packet: `not_supplied_yet`",
        "Arc Bot proof packet: `not_supplied_yet`",
        "LIMA Robo OS proof packet: `not_supplied_yet`",
        "LIMA Office proof packet: `not_supplied_yet`",
        "Future shell proof packet: `not_supplied_yet`",
    ):
        assert line in combined

    assert "No proof packet is received, archived, audited, accepted, or passed by this branch." in combined


def test_current_state_and_rollup_move_only_to_waiting_state() -> None:
    current_state = _read(CURRENT_STATE)
    rollup = _read(READINESS_ROLLUP)
    combined = "\n".join((current_state, rollup))

    assert "operator delivery confirmation: recorded as manual-delivery-only" in current_state
    assert "Operator delivery confirmation: RECORDED_MANUAL_DELIVERY_ONLY." in rollup
    assert "`WAITING_ON_CONSUMER_PROOF_PACKET_RESPONSES`" in combined
    assert "Runtime integration: NOT_READY." in rollup
    assert "Product readiness: NOT_READY." in rollup


def test_hard_limits_remain_blocked_after_delivery_record() -> None:
    combined = "\n".join((_read(DELIVERY_RECORD), _read(AUDIT_RECORD)))

    for blocked in (
        "touch consumer repos",
        "wire Sparkbot",
        "wire Arc Bot",
        "wire LIMA Robo OS",
        "wire LIMA Office",
        "create runtime integration",
        "finalize public API freeze",
        "claim product readiness",
        "add live provider/model routing",
        "add Guardian authority expansion",
        "activate HumanInput bridge",
        "add connector/browser/file/network/external-send behavior",
        "add live discovery, scanning, pairing, credential use, device control, robot, drone, IoT, or physical-world behavior",
    ):
        assert blocked in combined


def test_branch_stops_before_proof_packet_audit() -> None:
    record = _read(DELIVERY_RECORD)
    audit = _read(AUDIT_RECORD)

    assert "Do not proceed to proof packet audit from this branch." in record
    assert "Ready only to wait for consumer proof packet responses." in audit
    assert "Not ready for proof packet audit until" in audit
