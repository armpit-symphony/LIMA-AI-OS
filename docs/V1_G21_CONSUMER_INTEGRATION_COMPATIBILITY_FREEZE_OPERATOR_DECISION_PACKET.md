# V1-G21 Consumer Integration Compatibility Freeze Operator Decision Packet

Date: 2026-06-17
Branch: `prepare-v1-g21-consumer-integration-compatibility-freeze-approval-request`
API status: `CANDIDATE_ONLY`

Decision packet status: `approved_for_v1_g21_implementation`

This packet records the valid operator choices for the exact V1-G21 consumer integration compatibility/freeze approval request. It does not approve implementation, edit consumer repositories, import consumer code, call consumer runtimes, wire consumers, freeze the final public API, or approve product readiness by itself.

## Decision Source

The decision source is:

- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_APPROVAL_REQUEST.md`
- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_WORK_ORDER.md`
- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_PREFLIGHT_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G20.md`
- `docs/readiness/V1_POST_G20_NEXT_LANE_DECISION_MATRIX.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G20_AUDIT.md`

The approval request asks:

> Do you explicitly approve V1-G21 implementation of the LIMA-side consumer integration compatibility/freeze metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

## Current Decision State

- Operator approval recorded: yes.
- Implementation approved: yes.
- Approved next implementation branch: `v1-g21-consumer-integration-compatibility-freeze`.
- Current next action: implement only the approved V1-G21 consumer integration compatibility/freeze metadata slice.

## Decision Record

The operator recorded exactly one valid choice for implementation.

- Recorded choice: `Approve-V1-G21`
- Recorded approval wording: `I explicitly approve V1-G21 implementation of the LIMA-side consumer integration compatibility/freeze metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_APPROVAL_REQUEST.md.`
- Recorded revision request: `none`
- Recorded pause reason: `none`
- Approved implementation branch: `v1-g21-consumer-integration-compatibility-freeze`
- Implementation approved: yes

## Decision Record Templates

Use one template only.

Template for no recorded choice:

```text
Recorded choice: none
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: none
Implementation approved: no
```

Template for `Approve-V1-G21`:

```text
Recorded choice: Approve-V1-G21
Recorded approval wording: I explicitly approve V1-G21 implementation of the LIMA-side consumer integration compatibility/freeze metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_APPROVAL_REQUEST.md.
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: v1-g21-consumer-integration-compatibility-freeze
Implementation approved: yes
```

Template for `Revise-V1-G21`:

```text
Recorded choice: Revise-V1-G21
Recorded approval wording: none
Recorded revision request: <required revision request>
Recorded pause reason: none
Approved implementation branch: none
Implementation approved: no
```

Template for `Pause`:

```text
Recorded choice: Pause
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: <required pause reason>
Approved implementation branch: none
Implementation approved: no
```

## Valid Operator Choices

Only these choices are valid:

- `Approve-V1-G21`
- `Revise-V1-G21`
- `Pause`

Runtime implementation may start only from the valid `Approve-V1-G21` state.

## If `Approve-V1-G21` Is Recorded

Implementation must stay inside the named V1-G21 scope:

- `lima/adapters/v1_consumer_integration_compatibility.py`
- `lima/adapters/__init__.py`
- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE.md`
- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g21_consumer_integration_compatibility_freeze.json`
- `tests/test_v1_g21_consumer_integration_compatibility_freeze.py`

Any different file requires a new gate update before implementation.

## Recommended Next Step

Record exactly one operator choice in this packet.

If `Approve-V1-G21` is recorded, implement only the LIMA-side consumer integration compatibility/freeze metadata slice. Do not edit consumer repos, import consumer code, call consumer runtimes, freeze the final public API, or claim product readiness.
