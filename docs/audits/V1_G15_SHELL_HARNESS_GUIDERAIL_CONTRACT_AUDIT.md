# V1-G15 Shell/Harness Guiderail Contract Audit

Date: 2026-06-15
Branch: `audit-v1-g15-shell-harness-guiderail-contract`
Audited implementation branch: `v1-g15-shell-harness-guiderail-contract`
Audited implementation commit: `5bf557e18f655b6e0dff13916ee02278a65309ba`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit independently reviews the V1-G15 shell/harness guiderail input contract implementation. It does not add runtime behavior, wire consumers, route providers/models, activate HumanInput, invoke connectors, execute actions, mutate files, or claim product readiness.

## Scope Reviewed

- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT.md`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_CLOSEOUT.md`
- `lima/shells/contracts/v1_guiderail_input.py`
- `lima/shells/contracts/__init__.py`
- `tests/fixtures/runtime_extraction/v1_g15_shell_harness_guiderail_contract.json`
- `tests/test_v1_g15_shell_harness_guiderail_contract.py`

## Decision And File-Map Findings

- Exact `Approve-V1-G15` decision was recorded: pass.
- Approved branch recorded as `v1-g15-shell-harness-guiderail-contract`: pass.
- Implementation stayed inside the approved V1-G15 file map: pass.
- Candidate exports were limited to `lima/shells/contracts/__init__.py`: pass.
- Runtime export cleanup was not performed: pass.
- Final API freeze was not claimed: pass.

## Contract Findings

- Contract is shell/harness-facing: pass.
- Contract is capability-open and authority-gated: pass.
- Guardrail mode is explicit: pass.
- Capability profile is explicit: pass.
- Approval policy is explicit: pass.
- Actor scope is explicit: pass.
- Session scope is explicit: pass.
- Tenant scope is explicit: pass.
- Shell scope is explicit: pass.
- Allowed capability lanes are explicit: pass.
- Destructive edit/delete/file mutation policy is explicit: pass.
- Provider/model policy is explicit and accepted only as policy metadata: pass.
- Connector policy is explicit and accepted only as policy metadata: pass.
- Browser/network policy is explicit and accepted only as policy metadata: pass.
- Physical-world policy is explicit and remains blocked until a dedicated authority lane: pass.
- Emergency stop expectations are represented where consequential lanes are present: pass.
- Rollback expectations are represented where consequential lanes are present: pass.
- Dry-run versus execution-authorized posture is explicit: pass.
- Operator approval evidence expectations are represented: pass.
- Audit/evidence linkage expectations are represented: pass.

## Fail-Closed Findings

- Missing capability profile fails closed: pass.
- Missing guardrail mode fails closed: pass.
- Missing approval policy fails closed: pass.
- Missing actor/session/tenant/shell scope fails closed: pass.
- Missing allowed capability lanes fails closed: pass.
- Missing destructive edit/delete policy fails closed: pass.
- Missing file mutation policy fails closed: pass.
- Missing provider/model, connector, browser/network, or physical-world policy fails closed: pass.
- Raw secrets are rejected: pass.
- Raw prompts are rejected: pass.
- Raw file contents are rejected: pass.
- Raw approval PINs are rejected: pass.
- Raw approval tokens are rejected: pass.
- Raw customer data is rejected: pass.
- Runtime authority claims fail closed: pass.

## Boundary Findings

- No runtime execution was added: pass.
- No real file mutation was added: pass.
- No provider/model routing was added: pass.
- No connector behavior was added: pass.
- No browser/network behavior was added: pass.
- No device/robotics/physical-world behavior was added: pass.
- No HumanInput bridge activation was added: pass.
- No consumer repo was touched: pass.
- Sparkbot was not touched: pass.
- Sparkbot_shell was not touched: pass.
- Arc-Bot-shell was not touched: pass.
- LIMA Robo OS was not touched: pass.
- LIMA Office was not touched: pass.
- Product readiness was not claimed: pass.
- Final API freeze was not claimed: pass.

## Audit Conclusion

V1-G15 passes audit as a candidate shell/harness guiderail input contract. It gives future authority lanes structured context without authorizing live execution.

Recommended next safe step: audit the V1 runtime authority chain through V1-G15 before preparing the guarded file mutation policy approval request.
