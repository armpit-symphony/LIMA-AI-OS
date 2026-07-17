# V1-G15 Shell/Harness Guiderail Contract

Date: 2026-06-15
Branch: `v1-g15-shell-harness-guiderail-contract`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_contract_slice`

V1-G15 implements the approved shell/harness guiderail input contract slice. It validates structured metadata that shells and harnesses can provide before future authority lanes expand.

This slice is capability-open and authority-gated. It accepts broad capability metadata as policy input, but it does not wire shells, route providers/models, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, perform external sends, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G15` template.

Approved implementation branch:

- `v1-g15-shell-harness-guiderail-contract`

Approved scope:

- `shell_harness_guiderail_input_contract_slice`

## Runtime Files

- `lima/shells/contracts/v1_guiderail_input.py`
- `lima/shells/contracts/__init__.py`

## Runtime Symbols

- `V1GuiderailInputError`
- `validate_v1_shell_harness_guiderail_input`

## Contract Fields

The V1-G15 contract requires:

- `capability_profile`
- `guardrail_mode`
- `approval_policy`
- `actor_scope`
- `session_scope`
- `tenant_scope`
- `shell_scope`
- `allowed_capability_lanes`
- `destructive_edit_delete_policy`
- `file_mutation_policy`
- `provider_model_policy`
- `connector_policy`
- `browser_network_policy`
- `physical_world_policy`
- `emergency_stop_expectations`
- `rollback_expectations`
- `dry_run_vs_execution_authorized_posture`
- `operator_approval_evidence_expectations`
- `audit_evidence_linkage_expectations`

## Behavior Added

V1-G15 adds deterministic local validation and normalization for shell/harness guiderail input metadata.

The validator proves:

- guardrail mode is explicit
- capability profile is explicit
- approval policy is explicit
- actor/session/tenant/shell scope is explicit
- allowed capability lanes are explicit
- destructive edit/delete and file mutation policies require explicit approval
- provider/model policy is accepted only as policy metadata
- connector policy is accepted only as policy metadata
- browser/network policy is accepted only as policy metadata
- physical-world policy remains blocked until a dedicated authority lane
- emergency stop and rollback expectations are represented for consequential lanes
- dry-run versus execution-authorized posture is explicit
- operator approval evidence expectations are represented
- audit/evidence linkage expectations are represented
- raw sensitive content fails closed

## Boundary Results

- Runtime behavior added: yes, only candidate local contract validation.
- Shell runtime wiring added: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- Connector behavior added: no.
- Browser/network behavior added: no.
- File mutation behavior added: no.
- Device/robotics/physical-world behavior added: no.
- HumanInput bridge activated: no.
- External sends added: no.
- Approval tokens issued: no.
- Raw PIN verification added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- Product readiness claimed: no.

## Readiness Result

V1-G15 is ready for independent audit.

The next safe step is a separate V1-G15 audit branch. Do not proceed to guarded file mutation policy implementation, live approval capture, provider/model routing, consumer integration, final API freeze, or product readiness from this branch.
