# V1 Consumer Harness Usability Matrix

Date: 2026-06-21
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before matrix: `37626bf236bf96c8a57a3ca351668e90eeb0e651`
API status: `CANDIDATE_ONLY`

This matrix defines what "usable by Sparkbot and Arc-Bot-shell harnesses" means at the current V1 candidate boundary.

It is docs/tests/fixtures-only readiness evidence. It does not approve V1-G61 implementation, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add runtime vendor SDK imports in `lima/`, add provider SDK clients, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, wire consumer production runtime behavior, invoke connectors, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Matrix Verdict

Verdict: `HARNESS_USABLE_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER`

Sparkbot and Arc-Bot-shell harnesses remain usable for local candidate smoke validation with fake in-process executors and sanitized fixtures. They are not approved for production runtime integration, direct provider egress, provider SDK client construction, secret access, fallback execution, or physical-world control.

## Harness Usability Criteria

The current V1 candidate is usable by a consumer harness only when all of the following stay true:

- The harness imports only approved candidate public wrapper symbols.
- The harness injects a fake in-process provider SDK/network executor.
- The harness uses sanitized request metadata and does not persist raw prompts, raw model responses, raw customer data, secrets, provider tokens, API keys, raw diffs, full patches, or raw file contents.
- The harness test proves candidate call shape and authority metadata only.
- The harness performs no LIMA-owned DNS/HTTP/socket/network call.
- The harness performs no provider endpoint resolution, credential lookup, provider token access, fallback execution, connector invocation, browser/file/device/robotics/physical-world action, or production runtime wiring.
- The G61 operator decision packet status audit remains current and records `Approve-V1-G61` for bounded local import-proof evidence only.
- The current-gate consistency audit remains current and rejects stale blocker or release-candidate claims.
- The current candidate validation refresh, post-validation readiness-change freshness audit, latest post-G61 request readiness-refresh supplement, and latest quickstart artifact refresh evidence remain current for the harness handoff.
- The release-candidate acceptance checklist and cutover runbook remain blocked until the G61 operator decision is resolved, the final readiness audit passes, and clean Arc-Bot-shell checkpoint proof is recorded.
- Arc-Bot-shell smoke evidence is treated as compatibility evidence only unless unrelated local drift is absent and clean-checkpoint proof is recorded before release-candidate, final-readiness, branch, tag, cutover, or readiness claims.
- The harness stops before V1-G61 implementation unless `Approve-V1-G61` is explicitly recorded with the exact approval wording.

## Consumer Matrix

| Consumer | Local checkpoint | Current usable path | Required local command | Expected result | Boundary |
| --- | --- | --- | --- | --- | --- |
| Public Sparkbot target checkout | `C:\Users\limap\Sparkbot-public` on `v1-g56-runtime-authority-chain-audit` at `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | G56 fake-executor provider SDK/network egress smoke against local LIMA checkout | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` | Candidate smoke only; no production wiring or provider egress. |
| Accessible Sparkbot checkpoint | `C:\Users\limap\Sparkbot` on `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` at `ddaa4ccaacd328ddcc1f00a040c2c140abee428e` | G56 fake-executor provider SDK/network egress smoke against local LIMA checkout | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` | Candidate smoke only; no production wiring or provider egress. |
| Arc-Bot-shell | `C:\Users\limap\Arc-Bot-shell` on `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` at `2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0` | G56 fake-executor provider SDK/network egress smoke against local LIMA checkout | `python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` | Candidate smoke plus separate clean-checkpoint proof; no production wiring, provider egress, release authority, or cutover claim. |

## LIMA-Side Evidence Chain

- V1 candidate harness quickstart: `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`
- V1 candidate harness quickstart execution audit: `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`
- V1 candidate test handoff manifest: `docs/readiness/V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md`
- V1 candidate handoff execution audit: `docs/audits/V1_CANDIDATE_TEST_HANDOFF_MANIFEST_EXECUTION_AUDIT.md`
- V1 final blocker register: `docs/readiness/V1_FINAL_BLOCKER_REGISTER.md`
- V1 current candidate validation refresh audit: `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`
- V1 post-validation readiness-change freshness audit: `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`
- V1 Arc-Bot-shell local drift exclusion audit: `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`
- V1-G61 approval request: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`
- V1-G61 request-gate audit: `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`
- V1-G61 preapproval runtime-tree guard audit: `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`
- V1-G61 operator decision packet status audit: `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`
- V1 post-G61 request readiness refresh: `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`
- V1 current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- V1 release-candidate acceptance checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`
- V1 release-candidate cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`
- V1 final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`

## Current Freshness Evidence

- Current candidate validation refresh: 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests.
- Candidate harness quickstart execution refresh: public Sparkbot 8 tests, accessible Sparkbot 8 tests, Arc-Bot-shell 8 tests, LIMA 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests.
- Latest final blocker/index readiness refresh: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests.
- Latest post-G61 request readiness-refresh: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests.
- Latest quickstart artifact refresh: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- These freshness results keep the local harness handoff current only. They do not approve V1-G61 implementation, release-candidate status, final readiness, cutover, production integration, or Arc-Bot-shell clean-checkpoint proof.

## Required False Boundaries

- V1-G61 implementation approval recorded: false.
- V1-G61 runtime vendor SDK import execution proof implemented: false.
- V1 release-candidate branch or tag authorized by harness usability: false.
- V1 release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim authorized by harness usability: false.
- Arc-Bot-shell clean-checkpoint evidence claimed from local smoke: false.
- Release, cutover, final-readiness, or G61 implementation authority created by freshness evidence: false.
- Consumer production runtime integration approved: false.
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
- V1.0 completion, product-readiness, or production-readiness claimed: false.

## Stop Conditions

Stop and record a blocker before any step that would:

- implement V1-G61 without exact approval
- treat this matrix as G61 implementation approval
- treat this matrix as release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness-claim authority
- treat Arc-Bot-shell compatibility smoke as a substitute for recorded clean-checkpoint proof, or treat clean-checkpoint proof as release, final-readiness, branch, tag, cutover, or readiness authority
- edit Sparkbot, Sparkbot-public, or Arc-Bot-shell from this matrix lane
- add runtime behavior, public API exports, provider SDK clients, runtime vendor SDK imports in `lima/`, lockfile edits, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness

## Next Operator Action

Record exactly one V1-G61 operator choice: `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`.
