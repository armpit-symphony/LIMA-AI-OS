# V1-G15 Shell/Harness Guiderail Contract Work Order

Date: 2026-06-15
Branch: `prepare-v1-shell-harness-guiderail-contract-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_contract_slice`

This is a conditional work order only. It does not record operator approval, does not approve implementation, and does not change runtime behavior.

## Approval Dependency

V1-G15 implementation may start only after the operator explicitly approves:

`docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Existing Evidence To Reuse

The implementation must remain compatible with:

- V1-G11 typed request and GuardianDecision preflight metadata
- V1-G12 redacted audit/evidence metadata
- V1-G14 destructive approval-enforcement metadata
- `docs/architecture/LIMA_CAPABILITY_OPEN_AUTHORITY_GATED_MODEL.md`
- `docs/readiness/V1_NEXT_AUTHORITY_LANE_DECISION_MATRIX.md`

Do not create execution authority. The guiderail contract supplies structured input for future authority gates.

## Implementation Sequence If Approved

1. Add `lima/shells/contracts/v1_guiderail_input.py`.
2. Define candidate dataclasses or typed validators for shell/harness guiderail input metadata.
3. Require capability profile, guardrail mode, approval policy, actor/session/tenant/shell scope, allowed capability lanes, and dry-run versus execution-authorized posture.
4. Require policy metadata for destructive edit/delete, file mutation, provider/model, connector, browser/network, and physical-world capabilities.
5. Require emergency stop and rollback expectations when capability profiles include consequential or physical-world lanes.
6. Require operator approval evidence expectations and audit/evidence linkage expectations.
7. Reject raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, and customer data.
8. Keep physical-world behavior blocked until a dedicated physical-world authority lane.
9. Add candidate exports only in `lima/shells/contracts/__init__.py`.
10. Add `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT.md`.
11. Add `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_CLOSEOUT.md`.
12. Add `tests/fixtures/runtime_extraction/v1_g15_shell_harness_guiderail_contract.json`.
13. Add `tests/test_v1_g15_shell_harness_guiderail_contract.py`.

## Expected Candidate Symbols If Approved

The implementation should expose only candidate V1 symbols such as:

- `V1GuiderailInputError`
- `validate_v1_shell_harness_guiderail_input`

Exact names may change only if the V1-G15 implementation doc records the reason and tests lock the exported surface.

## Required Output Boundaries If Approved

The slice may output:

- normalized guiderail input dictionaries
- redacted capability profile metadata
- policy metadata references
- audit/evidence linkage references
- fail-closed error messages without raw sensitive values

The slice must not output:

- raw secrets
- raw prompts
- raw file contents
- raw customer records
- approval PINs
- approval tokens
- provider credentials
- executable commands
- connector dispatch payloads
- shell dispatch payloads

## Required Validation If Approved

Run at minimum:

- focused V1-G15 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G15 file map
- consumer repo changes
- shell runtime wiring
- provider/model calls or routing
- live HumanInput bridge behavior
- connector behavior
- browser/network behavior
- file mutation behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external sends
- raw sensitive content persistence
- approval-token issuance
- approval metadata as broad execution authority
- final API freeze
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G15 operator decision packet.

If approved, implement only the approved candidate guiderail input contract slice on branch `v1-g15-shell-harness-guiderail-contract`.
