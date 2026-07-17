# V1-G11 Runtime Request Decision Gate Audit

Date: 2026-06-14
Audit branch: `audit-v1-g11-runtime-request-decision-gate`
Audited implementation branch: `v1-g11-runtime-request-decision-gate`
Audited implementation commit: `50425b41bb64cca8174c6fc21983cf44f8c41e6b`
API status: `CANDIDATE_ONLY`

## Verdict

Verdict: `PASS`

The V1-G11 runtime request decision gate implementation stayed within the approved file map and matches the recorded `Approve-V1-G11` operator decision. The slice is deterministic, local, typed, non-executing, non-persistent, and fail-closed.

This audit adds no runtime behavior and does not approve any next runtime lane by itself.

## Files Audited

- `lima/kernel/v1_runtime_request.py`
- `lima/kernel/__init__.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/guardian/__init__.py`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

## Scope Audit

Implementation diff from `305a3733eeab7ad9b9fefcfbb3c0146a5558137c` to `50425b41bb64cca8174c6fc21983cf44f8c41e6b` changed only the approved V1-G11 file map:

- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `lima/guardian/__init__.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/kernel/__init__.py`
- `lima/kernel/v1_runtime_request.py`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

Result: pass.

## Operator Decision Audit

`docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md` records:

- Recorded choice: `Approve-V1-G11`
- Approved implementation branch: `v1-g11-runtime-request-decision-gate`
- Runtime implementation approved: yes
- Required approval wording present exactly for the typed request and GuardianDecision preflight runtime slice

Result: pass.

## Runtime Request Builder Audit

`build_v1_runtime_request(candidate)` in `lima/kernel/v1_runtime_request.py`:

- accepts a mapping and rejects non-mapping inputs
- rejects raw natural-language payload keys before validation
- rejects caller-supplied approval, approval token, PIN, decision, or GuardianDecision authority metadata
- delegates candidate validation to `validate_candidate`
- requires candidate id, intake id, actor id, shell id, action category, requested action, and provenance
- derives deterministic ids from candidate metadata
- returns typed `ConsequentialActionRequest` metadata
- emits audit/evidence linkage with `persistent: False`
- sets `execution_allowed: False`, `side_effects_allowed: False`, `approval_token_issued: False`, `provider_model_routing_allowed: False`, `shell_wiring_allowed: False`, and `persistent_storage_allowed: False`

Result: pass.

## GuardianDecision Preflight Gate Audit

`review_v1_runtime_request(request)` in `lima/guardian/v1_decision_gate.py`:

- accepts only `ConsequentialActionRequest`
- rejects caller-supplied authority metadata in request metadata
- returns deterministic `GuardianDecision` preflight metadata
- leaves `allowed_tool_packs` empty
- sets non-executing constraints
- sets `approval_token_issued: False`
- sets `provider_model_routed: False`
- sets `shell_wired: False`
- sets `persistent: False`
- emits non-persistent audit/evidence linkage
- does not call providers, tools, connectors, browsers, files, networks, devices, robots, drones, IoT, or external systems

Result: pass.

## Behavior Audit

| Required behavior | Audit result |
| --- | --- |
| Safe informational, planning, and drafting candidates remain review-only | Pass. They produce non-executing reviewed metadata with empty tool packs. |
| Destructive edit/delete/file mutation shaped requests require operator approval metadata | Pass. `file_mutation`, `admin`, and `shell` categories map to `NEEDS_OPERATOR_PIN`; destructive edit/delete stays non-executing. |
| Provider/model shaped claims are blocked | Pass. `model_call` is denied without routing or execution. |
| Tool shaped claims are blocked | Pass. `tool_call` is denied without tool-pack exposure or execution. |
| Browser/network shaped claims are blocked | Pass. `browser_network` is denied without browser/network behavior. |
| Robotics/physical-world shaped claims are blocked | Pass. `robotics_physical_world` is denied without device, robotics, or physical-world behavior. |
| Stale candidates fail closed | Pass. Candidate validation rejects stale candidates before request review. |
| Replayed candidates fail closed | Pass. Candidate validation rejects replayed candidates before request review. |
| Missing provenance fails closed | Pass. Missing provenance raises `V1RuntimeRequestError`. |
| Raw payload candidates fail closed | Pass. Raw input keys are rejected recursively. |
| Forged approval/decision metadata fails closed | Pass. Builder and gate reject forged authority metadata. |
| Audit/evidence metadata is non-persistent | Pass. Request and decision linkage explicitly set `persistent: False`; no durable writer is added. |
| No approval tokens emitted | Pass. Metadata and constraints keep `approval_token_issued: False`. |
| No raw secrets emitted | Pass. Tests assert raw secret-shaped values are absent from serialized output. |
| No raw prompts emitted | Pass. Raw prompt keys are rejected; output tests cover raw prompt text absence. |
| No raw file contents emitted | Pass. Raw file content keys are rejected; output tests cover raw file content absence. |
| No approval PINs emitted | Pass. Caller-supplied PIN keys are rejected; output tests cover PIN absence. |

## Boundary Audit

| Boundary | Audit result |
| --- | --- |
| Consumer repos touched | No. |
| Sparkbot touched | No. |
| Sparkbot_shell touched | No. |
| Arc-Bot-shell touched | No. |
| LIMA Robo OS touched | No. |
| LIMA Office touched | No. |
| Provider/model routing added | No. |
| HumanInput bridge activated | No. |
| Connector behavior added | No. |
| Browser/file/network action behavior added | No. |
| Live discovery/scanning/pairing/credential/device/robot/drone/IoT/physical-world behavior added | No. |
| Product readiness claimed | No. |
| Final API freeze claimed | No. |

## Test Evidence Reviewed

`tests/test_v1_g11_runtime_request_decision_gate.py` covers:

- approved-scope fixture metadata
- safe informational/planning/drafting decisions
- destructive edit/delete operator approval metadata
- caller-supplied approval rejection
- caller-supplied GuardianDecision authority rejection
- stale candidate rejection
- replayed candidate rejection
- missing provenance rejection
- raw natural-language payload rejection
- unknown action denial
- model/tool/browser-network/robotics future-policy denial
- non-persistent audit/evidence linkage
- sensitive output absence
- forged request authority metadata rejection

The fixture records the same blocked boundaries under `forbidden_behavior`.

## Warnings

No blocking warnings.

Residual notes:

- Safe requests use `GuardianDecisionStatus.APPROVED` as a reviewed preflight status, but constraints keep them non-executing, non-persistent, tool-pack-empty, and token-free. This is acceptable for V1-G11 but must not be interpreted as execution authority.
- Durable audit/evidence persistence remains unimplemented.

## Recommended Next Lane

If this audit is accepted, prepare a separate operator approval request for V1-G12 durable audit/evidence persistence.

Do not start V1-G12 implementation from this audit branch.
