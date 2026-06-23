# V1 Release Candidate Acceptance Checklist

Date: 2026-06-22
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before checklist: `37626bf236bf96c8a57a3ca351668e90eeb0e651`
API status: `CANDIDATE_ONLY`

This checklist defines the minimum evidence required before LIMA-AI-OS can be called a V1.0.0 release candidate for Sparkbot and Arc-Bot-shell harness use.

It is docs/tests/fixtures-only readiness evidence. It records that `Approve-V1-G61` was provided separately and that the bounded G61 proof/closeout exists, but it does not itself approve V1-G61 implementation, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add runtime vendor SDK imports in `lima/`, add provider SDK clients, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, wire consumer production runtime behavior, invoke connectors, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

This checklist is not branch, tag, cutover, final readiness, or Arc-Bot-shell clean-checkpoint authority. It is currently a failing release-candidate bar. Passing this checklist later requires separate evidence that the final readiness audit is executed and passed, cutover is authorized through the runbook, and Arc-Bot-shell clean-checkpoint proof is recorded after local drift is absent or resolved and revalidated.

## Checklist Verdict

Verdict: `NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS`

LIMA-AI-OS is not a V1.0.0 release candidate yet. The current candidate is locally testable by Sparkbot and Arc-Bot-shell harnesses only as fake-executor, sanitized-fixture, no-network smoke evidence. The V1-G61 operator blocker is resolved by `Approve-V1-G61` and bounded proof closeout, but the release-candidate gate remains blocked until the final readiness audit passes, release-candidate cutover is authorized through the runbook, and Arc-Bot-shell clean-checkpoint proof is recorded after local drift is absent or resolved and revalidated.

## Required Release-Candidate Inputs

- V1 final blocker register: `docs/readiness/V1_FINAL_BLOCKER_REGISTER.md`
- V1 candidate test handoff manifest: `docs/readiness/V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md`
- V1 candidate harness quickstart: `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`
- V1 candidate harness quickstart execution audit: `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`
- V1 consumer harness usability matrix: `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`
- V1 consumer checkpoint manifest: `docs/readiness/V1_CONSUMER_CHECKPOINT_MANIFEST.md`
- V1 release-candidate cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`
- V1 final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`
- V1 current candidate validation refresh audit: `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`
- V1 post-validation readiness-change freshness audit: `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`
- V1 current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- V1-G61 operator decision packet status audit: `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`
- V1 Arc-Bot-shell local drift exclusion audit: `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`
- V1 post-G61 request readiness refresh: `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`
- V1-G61 operator decision packet: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`
- V1-G61 approval request: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`
- V1-G61 request-gate audit: `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`
- V1-G61 preapproval runtime-tree guard audit: `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`
- V1-G61 runtime vendor SDK import execution proof: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md`
- V1-G61 runtime vendor SDK import execution proof closeout: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md`
- V1-G61 runtime vendor SDK import execution proof fixture: `tests/fixtures/runtime_extraction/v1_g61_runtime_vendor_sdk_import_execution_proof.json`
- V1-G61 runtime vendor SDK import execution proof test: `tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof.py`
- V1 operator unblock action packet: `docs/readiness/V1_OPERATOR_UNBLOCK_ACTION_PACKET.md`
- V1 final candidate branch index: `docs/readiness/V1_FINAL_CANDIDATE_BRANCH_INDEX.md`

## Entry Criteria

All entry criteria must pass before creating a V1.0.0 release-candidate branch or tag:

- Exactly one valid V1-G61 operator decision is recorded.
- If the decision is `Approve-V1-G61`, the approved G61 implementation, closeout, and focused tests pass.
- If the decision is `Revise-V1-G61` or `Pause`, V1.0.0 release-candidate work remains stopped.
- V1 final blocker register has no active blocker that prevents release-candidate testing.
- V1 final readiness audit is executed and passed.
- V1 release-candidate cutover runbook remains blocked until this checklist and the final readiness audit both pass.
- V1 consumer harness usability matrix remains current for public Sparkbot, accessible Sparkbot, and Arc-Bot-shell local candidate smoke tests.
- V1 candidate harness quickstart remains current as the shortest safe local smoke command path.
- V1 candidate harness quickstart execution audit remains current and records public Sparkbot, accessible Sparkbot, and Arc-Bot-shell local smoke passes.
- V1 candidate harness quickstart execution audit records the latest same-turn consumer smoke refresh with public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 tests, and post-refresh LIMA validation passing 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests.
- V1 current candidate validation refresh audit remains current and records the latest focused current-gate validation, full LIMA suite evidence, latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests.
- V1 post-validation readiness-change freshness audit remains current and records same-turn focused, full-suite, and diff-check evidence requirements for later readiness docs, fixtures, or tests, with current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- V1 current gate consistency audit remains current and rejects stale public Sparkbot publication or V1-G57 active-blocker language.
- V1-G61 operator decision packet status audit remains current and records `Approve-V1-G61`.
- Public Sparkbot target publication remains proven.
- Public Sparkbot G56 fake-executor smoke test passes.
- Accessible Sparkbot G56 fake-executor smoke test passes.
- Arc-Bot-shell G56 fake-executor smoke test passes.
- Arc-Bot-shell local worktree drift is either absent or explicitly excluded by `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md` from V1 proof as compatibility evidence, not clean-checkpoint evidence; the current audit records 7 tracked modified files and 64 untracked files as excluded from release proof.
- Arc-Bot-shell clean-checkpoint proof is recorded after local drift is absent or resolved and revalidated before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim.
- `python -m compileall lima` passes.
- `python -m pytest -q tests -p no:cacheprovider` passes.
- `git diff --check` and `git diff --cached --check` pass in LIMA-AI-OS.
- Consumer diff hygiene passes for public Sparkbot, accessible Sparkbot, and Arc-Bot-shell.
- Evidence remains sanitized and contains no raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents.
- No forbidden runtime, provider, network, credential, connector, browser, file, device, robotics, physical-world, or consumer production behavior is added without separate explicit approval.

## Current Criteria State

| Criterion | Current state |
| --- | --- |
| V1-G61 operator decision recorded | satisfied, `Approve-V1-G61` recorded by operator |
| V1-G61 implementation and closeout complete if approved | satisfied, bounded local import proof and closeout recorded with focused G61 test and full-suite evidence |
| Final blocker register clear | not satisfied |
| Final readiness audit executed and passed | not satisfied |
| Release-candidate cutover authorized | not satisfied |
| Candidate harness quickstart execution audit current | satisfied |
| Candidate harness quickstart post-refresh proof | satisfied, consumers 8/8/8 and LIMA 17/108/5360 tests |
| Current candidate validation refresh audit current | satisfied, latest current-gate/release-readiness set 153 tests, full suite 5350 tests, latest LIMA readiness freshness supplement 15/89/5361 tests, and latest handoff freshness supplement 8/117/5362 plus 7/64/133/5364 tests |
| Post-validation readiness-change freshness audit current | satisfied, same-turn full-suite freshness evidence 5359 tests; latest final blocker/index refresh evidence 15/89/5361 tests; latest post-G61 request refresh evidence 8/117/5362 tests; latest quickstart artifact refresh evidence 7/64/133/5364 tests |
| Current gate consistency audit current | satisfied |
| V1-G61 operator decision packet status audit current | satisfied, `Approve-V1-G61` recorded |
| Consumer harness usability matrix current | satisfied |
| Public Sparkbot publication proven | satisfied |
| Public Sparkbot G56 fake-executor smoke | satisfied |
| Accessible Sparkbot G56 fake-executor smoke | satisfied |
| Arc-Bot-shell G56 fake-executor smoke | satisfied |
| Arc-Bot-shell local drift exclusion audit | satisfied as compatibility evidence only; current audit records 7 tracked modified files and 64 untracked files excluded from release proof; not clean-checkpoint evidence |
| Arc-Bot-shell clean-checkpoint proof | not satisfied |
| LIMA compileall | satisfied |
| LIMA focused current-gate/release-readiness validation | satisfied, 153 tests |
| LIMA full suite | satisfied, 5350 tests |
| LIMA current validation latest readiness freshness supplement | satisfied, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests |
| LIMA current validation latest handoff freshness supplement | satisfied, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests |
| LIMA quickstart post-refresh full suite | satisfied, 5360 tests |
| LIMA latest final blocker/index refresh full suite | satisfied, 5361 tests |
| LIMA latest post-G61 request refresh full suite | satisfied, 5362 tests |
| LIMA latest quickstart artifact refresh full suite | satisfied, 5364 tests |
| LIMA diff hygiene | satisfied |
| Consumer diff hygiene | satisfied |
| Evidence sanitized | satisfied |
| Product or production readiness approved | not satisfied |

## Required Validation Commands

Run these commands before any future release-candidate claim:

```powershell
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

in `C:\Users\limap\Sparkbot-public`.

```powershell
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

in `C:\Users\limap\Sparkbot`.

```powershell
python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

in `C:\Users\limap\Arc-Bot-shell`.

```powershell
python -m compileall lima
python -m pytest -q tests -p no:cacheprovider
git diff --check
git diff --cached --check
```

in `C:\Users\limap\LIMA-AI-OS`.

## Required False Boundaries

- V1-G61 implementation approval recorded by this checklist: false.
- V1-G61 runtime vendor SDK import execution proof implemented by this checklist: false.
- V1.0.0 release-candidate branch or tag created by this checklist: false.
- V1 release-candidate checklist passed by this checklist: false.
- V1 release-candidate cutover authorized by this checklist: false.
- V1 final readiness audit executed or passed by this checklist: false.
- Arc-Bot-shell clean-checkpoint proof claimed by this checklist: false.
- `lima/` runtime files changed by this checklist: false.
- LIMA public API exports changed by this checklist: false.
- Consumer repositories changed by this checklist: false.
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

## Next Action

Keep this checklist as the release-candidate bar. The next state-changing step is clean Arc-Bot-shell checkpoint proof followed by a future final readiness audit. Do not create a V1.0.0 release-candidate branch, release tag, cutover, final-readiness pass, or product-readiness claim until this checklist, the future final readiness audit, and clean Arc-Bot-shell checkpoint proof all pass.

After this checklist is satisfied, use `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md` as the controlled branch/tag procedure. That runbook is currently blocked and does not approve cutover.
