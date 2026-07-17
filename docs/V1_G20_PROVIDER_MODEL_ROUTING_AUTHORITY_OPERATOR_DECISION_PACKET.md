# V1-G20 Provider Model Routing Authority Operator Decision Packet

Date: 2026-06-16
Branch: `prepare-v1-g20-provider-model-routing-authority-approval-request`
API status: `CANDIDATE_ONLY`

Decision packet status: `approved_for_v1_g20_implementation`

This packet records the valid operator choices for the exact V1-G20 provider/model routing authority approval request. It does not approve implementation, route providers/models, call model providers, read secrets, execute tools, touch consumer repos, import consumer code, wire consumers, or approve product readiness by itself.

## Decision Source

The decision source is:

- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_APPROVAL_REQUEST.md`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_WORK_ORDER.md`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_PREFLIGHT_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G19.md`
- `docs/readiness/V1_POST_G19_NEXT_LANE_DECISION_MATRIX.md`
- `docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md`
- `docs/V1_G5_PROVIDER_MODEL_ROUTING_AUDIT.md`

The approval request asks:

> Do you explicitly approve V1-G20 implementation of the LIMA-side provider/model routing authority metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

## Current Decision State

- Operator approval recorded: yes.
- Implementation approved: yes.
- Approved next implementation branch: `v1-g20-provider-model-routing-authority`.
- Current next action: implement only the approved V1-G20 provider/model routing authority metadata slice.

## Decision Record

The operator recorded exactly one valid choice for implementation.

- Recorded choice: `Approve-V1-G20`
- Recorded approval wording: `I explicitly approve V1-G20 implementation of the LIMA-side provider/model routing authority metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_APPROVAL_REQUEST.md.`
- Recorded revision request: `none`
- Recorded pause reason: `none`
- Approved implementation branch: `v1-g20-provider-model-routing-authority`
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

Template for `Approve-V1-G20`:

```text
Recorded choice: Approve-V1-G20
Recorded approval wording: I explicitly approve V1-G20 implementation of the LIMA-side provider/model routing authority metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_APPROVAL_REQUEST.md.
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: v1-g20-provider-model-routing-authority
Implementation approved: yes
```

Template for `Revise-V1-G20`:

```text
Recorded choice: Revise-V1-G20
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

- `Approve-V1-G20`
- `Revise-V1-G20`
- `Pause`

Runtime implementation may start only from the valid `Approve-V1-G20` state.

## If `Approve-V1-G20` Is Recorded

Implementation must stay inside the named V1-G20 scope:

- `lima/harness/v1_provider_model_routing_authority.py`
- `lima/harness/__init__.py`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY.md`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g20_provider_model_routing_authority.json`
- `tests/test_v1_g20_provider_model_routing_authority.py`

Any different file requires a new gate update before implementation.

## Recommended Next Step

Record exactly one operator choice in this packet.

If `Approve-V1-G20` is recorded, implement only the LIMA-side provider/model routing authority metadata slice. Do not call providers/models, read secrets, dispatch live requests, execute tools, touch consumer repos, or implement consumer integration.
