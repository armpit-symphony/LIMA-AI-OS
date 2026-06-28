# V1 Release Candidate Cutover Runbook

Date: 2026-06-28
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before runbook refresh: `bfa27f37212a24f0ca3e7d21c37e4ff80192db14`
API status: `CANDIDATE_ONLY`

This runbook defines the controlled path from the current V1 candidate evidence set to a future V1.0.0 release-candidate branch or tag for Sparkbot and Arc-Bot-shell harness use.

It is docs/tests/fixtures-only readiness evidence. It records that `Approve-V1-G61` was provided separately and that the bounded G61 proof/closeout exists, but it does not itself approve V1-G61 implementation, complete V1.0, create a release branch, create a tag, modify `lima/`, change public API exports, edit consumer repositories, add runtime vendor SDK imports in `lima/`, add provider SDK clients, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, wire consumer production runtime behavior, invoke connectors, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

This runbook is not itself cutover authority. It remains blocked procedure text until the operator packet, final blocker register, branch index, release-candidate checklist, current validation refresh, post-validation readiness-change freshness audit, final readiness audit, and current consumer checkpoint evidence all prove the cutover is safe.

## Runbook Verdict

Verdict: `CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION`

The V1.0.0 release-candidate cutover is not currently allowed. `Approve-V1-G61` is recorded, the bounded G61 proof/closeout exists, Arc-Bot-shell clean-checkpoint proof is recorded at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`, the release-candidate acceptance checklist is satisfied for first-consumer harness testing, and `docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md` records `PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`. This runbook may be used only as a future branch/tag procedure after explicit operator authorization for branch creation, tag creation, and cutover is recorded.

## 2026-06-24 Arc Clean Checkpoint Supplement

Arc-Bot-shell clean-checkpoint proof is now recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`. This supersedes earlier same-document language that treated Arc-Bot-shell local drift as an active release blocker.

This supplement closes only the Arc clean-checkpoint blocker. LIMA remains `CANDIDATE_ONLY`; final-readiness reconciliation and release-candidate acceptance are now satisfied for first-consumer harness testing, while cutover remains blocked until explicit operator authorization is recorded through the runbook.
## Required Inputs Before Cutover

- V1 final blocker register: `docs/readiness/V1_FINAL_BLOCKER_REGISTER.md`
- V1 candidate test handoff manifest: `docs/readiness/V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md`
- V1 consumer harness usability matrix: `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`
- V1 consumer checkpoint manifest: `docs/readiness/V1_CONSUMER_CHECKPOINT_MANIFEST.md`
- V1 release-candidate acceptance checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`
- V1 final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`
- V1 current candidate validation refresh audit: `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`
- V1 post-validation readiness-change freshness audit: `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`
- V1 current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- V1-G61 operator decision packet status audit: `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`
- V1 Arc-Bot-shell local drift exclusion audit: `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`
- V1 Arc-Bot-shell clean checkpoint proof: `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md`
- V1 operator unblock action packet: `docs/readiness/V1_OPERATOR_UNBLOCK_ACTION_PACKET.md`
- V1 release-candidate cutover authorization packet: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`
- V1 release-candidate cutover authorization packet status audit: `docs/audits/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET_STATUS_AUDIT.md`
- V1 final candidate branch index: `docs/readiness/V1_FINAL_CANDIDATE_BRANCH_INDEX.md`
- V1 final readiness audit: `docs/audits/V1_FINAL_READINESS_AUDIT.md`
- V1 final readiness reconciliation audit: `docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md`
- V1-G61 operator decision packet: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`
- V1-G61 approval request: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`
- V1-G61 runtime vendor SDK import execution proof: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md`
- V1-G61 runtime vendor SDK import execution proof closeout: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md`

## Cutover Preconditions

Every precondition must be satisfied before creating any V1.0.0 release-candidate branch or tag:

- Exactly one valid V1-G61 operator decision is recorded.
- If G61 is approved, the approved implementation and closeout are complete.
- If G61 is revised or paused, release-candidate cutover remains stopped.
- `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md` reports `CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`.
- `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md` remains current and records the latest focused current-gate validation, full-suite evidence, latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests.
- `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md` remains current and records same-turn focused, full-suite, and diff-check evidence requirements for readiness docs, fixtures, or tests changed after the current validation refresh, with current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md` remains current and passes before any branch or tag action.
- `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md` remains current and records `Approve-V1-G61`.
- `docs/audits/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET_STATUS_AUDIT.md` remains current and records the cutover authorization packet as blocked with recorded valid cutover operator choice count `0` until a later explicit operator choice is recorded.
- `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md` records exactly one valid cutover operator choice, and that choice is `Approve-V1-RC-Cutover`.
- The final readiness reconciliation audit exists and passes with `PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`.
- Public Sparkbot, accessible Sparkbot, and Arc-Bot-shell candidate smoke validation passes.
- Arc-Bot-shell clean-checkpoint proof is recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3` before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim.
- Historical Arc-Bot-shell local drift exclusion evidence remains compatibility-only context and is superseded by the clean-checkpoint proof for release-gate evaluation.
- LIMA compileall, full suite, and diff hygiene pass.
- Evidence remains sanitized.
- No unapproved runtime, provider, network, credential, connector, browser, file, device, robotics, physical-world, consumer production, or product-readiness behavior appears.

## Current State

| Precondition | Current state |
| --- | --- |
| V1-G61 operator decision recorded | satisfied, `Approve-V1-G61` recorded by operator |
| G61 implementation and closeout complete if approved | satisfied, bounded local import proof and closeout recorded |
| Release-candidate acceptance checklist satisfied | satisfied for first-consumer harness testing |
| Current candidate validation refresh audit current | satisfied, latest current-gate/release-readiness set 153 tests, full suite 5350 tests, latest LIMA readiness freshness supplement 15/89/5361 tests, and latest handoff freshness supplement 8/117/5362 plus 7/64/133/5364 tests |
| Post-validation readiness-change freshness audit current | satisfied, same-turn full-suite freshness evidence 5359 tests; latest final blocker/index refresh evidence 15/89/5361 tests; latest post-G61 request refresh evidence 8/117/5362 tests; latest quickstart artifact refresh evidence 7/64/133/5364 tests |
| Latest quickstart post-refresh validation | satisfied, consumers 8/8/8 and LIMA 17/108/5360 tests |
| Current gate consistency audit current | satisfied |
| V1-G61 operator decision packet status audit current | satisfied, `Approve-V1-G61` recorded |
| Cutover authorization packet status audit | satisfied, blocked with recorded valid cutover operator choice count `0` |
| Final readiness audit exists | satisfied, historical audit remains recorded in `docs/audits/V1_FINAL_READINESS_AUDIT.md` |
| Final readiness reconciliation audit passes | satisfied, `docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md` records `PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED` |
| Public Sparkbot candidate smoke | satisfied as current G56 fake-executor evidence |
| Accessible Sparkbot candidate smoke | satisfied as current G56 fake-executor evidence |
| Arc-Bot-shell candidate smoke | satisfied as current G56 fake-executor evidence |
| Arc-Bot-shell clean-checkpoint proof | satisfied, clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3` recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` |
| Arc-Bot-shell local drift exclusion audit | historical compatibility evidence only; superseded by clean-checkpoint proof for release-gate evaluation |
| LIMA full suite | satisfied at current validation checkpoint; latest validation-refresh supplement full-suite evidence 5361 tests; latest handoff freshness supplement full-suite evidence 5362/5364 tests; latest quickstart post-refresh full-suite evidence 5360 tests; latest final blocker/index refresh full-suite evidence 5361 tests; latest post-G61 request refresh full-suite evidence 5362 tests; latest quickstart artifact refresh full-suite evidence 5364 tests |
| Cutover authorization packet | prepared, `AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION` |
| Cutover authorized by this runbook | blocked pending `Approve-V1-RC-Cutover` |
| Release-candidate branch creation | blocked |
| Release-candidate tag creation | blocked |

## Future Cutover Procedure

Run this procedure only after all cutover preconditions are satisfied:

1. Confirm the final readiness reconciliation audit verdict is `PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`.
2. Confirm the release-candidate acceptance checklist reports `CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`.
3. Confirm the current gate consistency audit still passes and records V1-G61 as the active current gate.
4. Confirm the G61 operator decision packet status audit is current and consistent with the recorded decision state.
5. Confirm the cutover authorization packet status audit is current and still records blocked packet status until a valid operator choice is recorded.
6. Confirm `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md` records `Approve-V1-RC-Cutover`.
7. Confirm public Sparkbot, accessible Sparkbot, and Arc-Bot-shell smoke tests pass from their documented checkpoints.
8. Confirm Arc-Bot-shell clean-checkpoint proof remains recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`.
9. Confirm any historical Arc-Bot-shell local drift exclusion evidence is treated only as superseded compatibility context, not current release-candidate evidence.
10. Confirm Arc-Bot-shell evidence is not treated as release-candidate, final-readiness, branch, tag, cutover, or readiness evidence unless the clean checkpoint proof remains current.
11. Confirm the current candidate validation refresh audit records the latest focused current-gate validation, full-suite evidence, latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests.
12. Confirm the post-validation readiness-change freshness audit covers later readiness docs, fixtures, or tests with same-turn focused, full-suite, and diff-check evidence, including current same-turn full-suite freshness evidence of 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence of 5360 tests, latest final blocker/index refresh evidence of 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request refresh evidence of 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence of 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
13. Confirm LIMA `python -m compileall lima`, `python -m pytest -q tests -p no:cacheprovider`, `git diff --check`, and `git diff --cached --check` pass.
14. Confirm `git status --short --branch` is clean except intentional staged release-candidate metadata.
15. Create a release-candidate branch only after `Approve-V1-RC-Cutover` is recorded.
16. Create a V1.0.0 release-candidate tag only after `Approve-V1-RC-Cutover` is recorded.
17. Record the branch/tag identifiers in a future cutover audit.

## Required Future Cutover Audit

If a release-candidate cutover is approved later, create a separate audit artifact before any final release claim:

- `docs/audits/V1_RELEASE_CANDIDATE_CUTOVER_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_release_candidate_cutover_audit.json`
- `tests/test_v1_release_candidate_cutover_audit.py`

The future cutover audit must record the exact branch, tag, validation commands, validation results, consumer checkpoint commits, LIMA commit, operator approval for branch/tag creation, and all preserved boundaries.

## Required False Boundaries

- V1-G61 implementation approval recorded by this runbook: false.
- V1-G61 runtime vendor SDK import execution proof implemented by this runbook: false.
- V1 release-candidate checklist passed by this runbook: false.
- V1 release-candidate cutover authorized by this runbook: false.
- V1 final readiness audit executed by this runbook: false.
- V1 final readiness audit passed by this runbook: false.
- Arc-Bot-shell clean-checkpoint proof created by this runbook: false.
- V1.0.0 release-candidate branch created by this runbook: false.
- V1.0.0 release-candidate tag created by this runbook: false.
- `lima/` runtime files changed by this runbook: false.
- LIMA public API exports changed by this runbook: false.
- Consumer repositories changed by this runbook: false.
- Runtime vendor SDK imports added to `lima/`: false.
- Provider SDK clients added: false.
- Provider client construction added: false.
- Lockfile edits added: false.
- LIMA-owned provider endpoint resolution added: false.
- LIMA-owned DNS/HTTP/socket/network calls added: false.
- Direct provider egress by LIMA added: false.
- Secret lookup or credential value access added: false.
- Provider token or API key access added: false.
- Provider configuration changes added: false.
- Fallback execution added: false.
- Connector/browser/file/device/robotics/physical-world behavior added: false.
- Consumer production runtime integration added: false.
- V1.0 completion, product-readiness, or production-readiness claimed: false.

## Stop Conditions

Stop before any step that would:

- implement V1-G61 without exact approval
- treat this runbook as G61 approval
- treat this runbook as release cutover authorization or final readiness audit authority
- treat Arc-Bot-shell local candidate smoke evidence as a substitute for the recorded clean-checkpoint proof
- create a release-candidate branch or tag before explicit branch/tag authorization is recorded
- edit consumer repositories from this runbook lane
- add runtime behavior, public API exports, provider SDK clients, runtime vendor SDK imports in `lima/`, lockfile edits, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness

## Next Action

Keep cutover blocked. The checklist/final-readiness loop is reconciled for first-consumer harness testing; the next required action is recording exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`.
