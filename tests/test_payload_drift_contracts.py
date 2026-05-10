"""Tests for describe-only payload drift contracts."""

from __future__ import annotations

from lima.contracts import (
    DriftDecision,
    DriftStatus,
    PayloadDriftReview,
    PayloadDriftReviewProtocol,
    PayloadFixtureDriftRecord,
)


def test_drift_status_values() -> None:
    assert {status.value for status in DriftStatus} == {
        "current",
        "needs_review",
        "stale",
        "unknown",
    }


def test_drift_decision_values() -> None:
    assert {decision.value for decision in DriftDecision} == {
        "no_drift",
        "fixture_update_required",
        "sparkbot_changed_not_adapter_relevant",
        "review_blocked_dirty_source",
        "unknown",
    }


def test_payload_fixture_drift_record_instantiates() -> None:
    record = PayloadFixtureDriftRecord(
        fixture_id="fixture-id",
        source_surface="chat_message_stream",
        sparkbot_reference_path="backend/app/api/routes/chat/rooms.py:StreamMessageRequest",
        inspected_commit="f7d5ee2054794ea7156ffb51a009c058cb7757e6",
        reviewed_against="4da833858428e076645cac8fca942205e80bcc6e",
        drift_status=DriftStatus.CURRENT,
        drift_decision=DriftDecision.NO_DRIFT,
        shape_version="phase-1.21",
        drift_notes="fixture shape reviewed",
        metadata={"fixture_only": True},
    )

    assert record.drift_status is DriftStatus.CURRENT
    assert record.drift_decision is DriftDecision.NO_DRIFT
    assert record.metadata == {"fixture_only": True}


def test_payload_drift_review_instantiates() -> None:
    record = PayloadFixtureDriftRecord(
        fixture_id="fixture-id",
        source_surface="robotics_command",
        sparkbot_reference_path="backend/app/api/routes/chat/robotics.py:RobotCommandRequest",
        inspected_commit="f7d5ee2054794ea7156ffb51a009c058cb7757e6",
        reviewed_against="4da833858428e076645cac8fca942205e80bcc6e",
        drift_status=DriftStatus.CURRENT,
        drift_decision=DriftDecision.NO_DRIFT,
    )
    review = PayloadDriftReview(
        review_id="payload-drift-review-fixture",
        sparkbot_commit="4da833858428e076645cac8fca942205e80bcc6e",
        local_worktree_dirty=False,
        fixture_records=(record,),
        decision=DriftDecision.CHANGED_NOT_ADAPTER_RELEVANT,
        reviewed_at="2026-05-09",
        notes="Describe-only review contract.",
        metadata={"no_runtime_behavior": True},
    )

    assert review.fixture_records == (record,)
    assert review.decision is DriftDecision.CHANGED_NOT_ADAPTER_RELEVANT
    assert review.metadata == {"no_runtime_behavior": True}


def test_payload_drift_review_protocol_is_describe_only() -> None:
    public_callables = {
        name
        for name, value in PayloadDriftReviewProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }
    forbidden_methods = {
        "compare_live",
        "import_sparkbot",
        "execute",
        "fetch",
        "mutate",
        "update_fixtures",
        "wire_route",
        "call_model",
        "call_tool",
    }

    assert public_callables == {"describe_review"}
    assert public_callables.isdisjoint(forbidden_methods)
