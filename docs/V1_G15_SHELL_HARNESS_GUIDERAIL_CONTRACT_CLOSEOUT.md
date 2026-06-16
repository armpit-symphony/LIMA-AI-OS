# V1-G15 Shell/Harness Guiderail Contract Closeout

Date: 2026-06-15
Branch: `v1-g15-shell-harness-guiderail-contract`
API status: `CANDIDATE_ONLY`

## Closeout Verdict

V1-G15 is complete as the approved candidate shell/harness guiderail input contract slice.

The slice validates structured guiderail input metadata and keeps LIMA capability-open and authority-gated. It does not implement shell wiring, consumer integration, provider/model routing, connector behavior, browser/network behavior, file mutation, device/robotics/physical-world behavior, external sends, final API freeze, or product readiness.

## Accepted Evidence

- `Approve-V1-G15` was recorded in the V1-G15 operator decision packet.
- `lima/shells/contracts/v1_guiderail_input.py` implements deterministic local contract validation.
- `lima/shells/contracts/__init__.py` exports only the V1-G15 candidate symbols.
- `tests/test_v1_g15_shell_harness_guiderail_contract.py` covers required contract fields, policy-only lanes, physical-world blocking, raw sensitive rejection, and no live execution flags.
- `tests/fixtures/runtime_extraction/v1_g15_shell_harness_guiderail_contract.json` records scope and boundary evidence.

## Rejected Or Non-Accepted Claims

- Product readiness is not approved.
- Final API freeze is not approved.
- Consumer integration is not approved.
- Shell runtime wiring is not implemented.
- Provider/model routing is not implemented.
- Connector behavior is not implemented.
- Browser/network behavior is not implemented.
- File mutation behavior is not implemented.
- Physical-world/device/robot/drone/IoT behavior is not implemented.
- Approval-token issuance is not implemented.
- Raw PIN verification is not implemented.

## Remaining Blockers

- Independent V1-G15 audit is not complete.
- Guarded file mutation policy is not approved or implemented.
- Live approval capture is not approved or implemented.
- Provider/model routing authority is not approved or implemented.
- Connector authority is not approved or implemented.
- Browser/network authority is not approved or implemented.
- Physical-world authority/safety lane is not approved or implemented.
- Consumer integration remains blocked.
- Final API freeze remains unapproved.

## Recommended Next Step

Prepare a separate V1-G15 audit branch.

After the audit, prepare a guarded file mutation policy approval request. Do not implement actual file mutation without a later exact operator decision.
