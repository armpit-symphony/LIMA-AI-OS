# V1 Candidate Test Handoff Manifest

Date: 2026-06-20
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before manifest refresh: `37626bf236bf96c8a57a3ca351668e90eeb0e651`
API status: `CANDIDATE_ONLY`

This manifest is the current operator handoff index for local V1 candidate testing across LIMA-AI-OS, public Sparkbot, the accessible Sparkbot checkpoint, and Arc-Bot-shell.

It is docs/tests/fixtures-only readiness evidence. It does not approve V1-G61 implementation, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK clients, add runtime vendor SDK imports in `lima/`, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, invoke connectors, wire consumer production runtime behavior, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Handoff Verdict

Verdict: `READY_FOR_LOCAL_CANDIDATE_TESTING_WITH_G61_OPERATOR_BLOCKER`

The current candidate remains testable locally with fake in-process provider SDK/network executors only. Public Sparkbot G56 publication is resolved, V1-G57 through V1-G60 are completed candidate-only evidence, and V1-G61 remains unapproved until an explicit operator choice is recorded.

## Source Evidence

- V1 through G57 candidate test runbook: `docs/runbooks/V1_THROUGH_G57_CANDIDATE_TEST_RUNBOOK.md`
- V1-G56 consumer fake-executor provider SDK/network egress smoke audit: `docs/audits/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_AUDIT.md`
- V1 runtime authority chain through G56 audit: `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G56_AUDIT.md`
- Public Sparkbot G56 publication resolution audit: `docs/audits/V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md`
- V1-G57 provider execution hardening authorization audit: `docs/audits/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_AUDIT.md`
- V1-G58 built-in provider SDK client authority contract audit: `docs/audits/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT_AUDIT.md`
- V1-G59 SDK dependency and vendor provider SDK import authority audit: `docs/audits/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_AUDIT.md`
- V1-G60 SDK dependency and vendor provider SDK import-boundary audit: `docs/audits/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUDIT.md`
- V1 runtime readiness rollup through G60: `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G60.md`
- V1 post-G60 next-lane decision matrix: `docs/readiness/V1_POST_G60_NEXT_LANE_DECISION_MATRIX.md`
- V1 candidate harness quickstart: `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`
- V1 candidate harness quickstart execution audit: `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`
- V1 consumer harness usability matrix: `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`
- V1 current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- V1 release-candidate acceptance checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`
- V1 release-candidate cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`
- V1 final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`
- V1-G61 approval request: `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`
- V1-G61 request-gate audit: `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`
- V1-G61 operator decision packet status audit: `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`
- V1 post-G61 request readiness refresh: `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`

## Repository Checkpoints

| Repo | Local path | Branch | Commit | Current state |
| --- | --- | --- | --- | --- |
| LIMA-AI-OS | `C:\Users\limap\LIMA-AI-OS` | `docs-v1-post-g60-readiness-and-next-lane-matrix` | `37626bf236bf96c8a57a3ca351668e90eeb0e651` | Working tree contains current V1 readiness/G61 request updates. |
| Public Sparkbot target checkout | `C:\Users\limap\Sparkbot-public` | `v1-g56-runtime-authority-chain-audit` | `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | Local checkpoint clean; public G56 target publication resolved by audit. |
| Accessible Sparkbot checkpoint | `C:\Users\limap\Sparkbot` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ddaa4ccaacd328ddcc1f00a040c2c140abee428e` | Local checkpoint clean and tracks origin. |
| Arc-Bot-shell | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0` | Checkpoint commit matches the expected G56 branch and tracks origin; local worktree has unrelated pre-existing changes, so current evidence is compatibility evidence, not clean-checkpoint evidence. |

## Local Candidate Validation Commands

Run these commands from the listed paths. Stop on any failure.

| Step | Path | Command | Expected result |
| --- | --- | --- | --- |
| 1 | `C:\Users\limap\Sparkbot-public` | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 2 | `C:\Users\limap\Sparkbot-public` | `git diff --check` | pass |
| 3 | `C:\Users\limap\Sparkbot` | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 4 | `C:\Users\limap\Sparkbot` | `git diff --check` | pass |
| 5 | `C:\Users\limap\Arc-Bot-shell` | `python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 6 | `C:\Users\limap\Arc-Bot-shell` | `git diff --check` | pass |
| 7 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests/test_v1_candidate_harness_quickstart.py tests/test_v1_candidate_test_handoff_manifest.py tests/test_v1_consumer_harness_usability_matrix.py tests/test_v1_current_gate_consistency_audit.py tests/test_v1_final_blocker_register.py tests/test_v1_g61_operator_decision_packet_status_audit.py tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request.py tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request_audit.py tests/test_v1_post_g61_request_readiness_refresh.py -p no:cacheprovider` | pass |
| 8 | `C:\Users\limap\LIMA-AI-OS` | `python -m compileall lima` | pass |
| 9 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests -p no:cacheprovider` | pass |
| 10 | `C:\Users\limap\LIMA-AI-OS` | `git diff --check` | pass |

## Candidate Scope Proven

- Public Sparkbot can import the approved G55 public wrapper symbols and call them with a fake in-process provider SDK/network executor in local tests.
- Accessible Sparkbot carries the pushed G56 fake-executor smoke checkpoint.
- Arc-Bot-shell carries the pushed G56 fake-executor smoke checkpoint, with unrelated local worktree drift excluded from current V1 proof.
- The V1 consumer harness usability matrix defines local candidate smoke usability as fake in-process executor, sanitized fixture, no-network, no-secret, no-production-wiring evidence only.
- The V1 candidate harness quickstart defines the shortest safe local smoke command path for public Sparkbot, accessible Sparkbot, Arc-Bot-shell, and LIMA-AI-OS.
- The V1 candidate harness quickstart execution audit records current public Sparkbot, accessible Sparkbot, and Arc-Bot-shell G56 smoke reruns as 8 passed each; LIMA focused handoff/current-gate pytest rerun as 73 passed; and full LIMA suite validation as 5359 passed.
- The post-G61 request readiness-refresh supplement records later handoff freshness with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests.
- The latest quickstart artifact refresh records current quickstart evidence-to-preserve assertions with 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- The V1 current gate consistency audit locks current-facing handoff, readiness, and release artifacts to the active G61 operator-decision gate.
- The V1 release-candidate checklist and cutover runbook remain blocked until the G61 decision is resolved, the final readiness audit passes, and clean Arc-Bot-shell checkpoint proof is recorded.
- The V1 final readiness audit template has not been executed by this manifest.
- The V1-G61 operator decision packet status audit proves the packet is still awaiting exactly one valid choice and does not approve implementation.
- LIMA-AI-OS records the runtime authority chain through G56, completed G57 through G60 candidate-only evidence, and the request-only G61 operator gate.
- The local candidate remains bounded to fake/caller-injected execution evidence and sanitized fixtures.

## Required Boundaries

The following must remain false while this manifest is the current handoff:

- V1-G61 implementation approval recorded
- V1-G61 runtime vendor SDK import execution proof implemented
- V1.0.0 release-candidate branch or tag authorized by this manifest
- release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim authorized by this manifest
- future final readiness audit executed by this manifest
- Arc-Bot-shell clean-checkpoint evidence claimed by this manifest
- `lima/` runtime files changed by this manifest
- LIMA public API exports changed by this manifest
- Sparkbot or Arc-Bot-shell files changed by this manifest
- runtime vendor SDK imports added to `lima/`
- provider SDK clients added
- lockfile edits added
- LIMA-owned provider endpoint resolution added
- LIMA-owned DNS/HTTP/socket/network calls added
- direct provider egress by LIMA added
- secret lookup or credential value access added
- provider token or API key access added
- provider configuration changes added
- fallback execution added
- connector/browser/file/device/robotics/physical-world behavior added
- consumer production runtime integration added
- V1.0 completion, product-readiness, or production-readiness claimed

## Current Blockers

- V1-G61 implementation: blocked until exactly one valid operator choice is recorded, and implementation may proceed only if that choice is `Approve-V1-G61` with the exact approval wording.
- Runtime import execution proof: blocked until V1-G61 is approved.
- Release-candidate branch/tag authority: blocked until the release-candidate checklist, final readiness audit, and clean Arc-Bot-shell checkpoint proof pass under separate approval.
- Arc-Bot-shell clean-checkpoint proof: blocked while unrelated local drift remains excluded from current V1 proof.
- Latest handoff freshness supplements: evidence only; they do not approve V1-G61 implementation, release-candidate acceptance, final readiness, cutover, consumer production integration, Arc-Bot-shell clean-checkpoint proof, product readiness, or production readiness.
- Lockfile edits, runtime imports in `lima/`, provider client construction, credentials, endpoint resolution, network egress, fallback, consumer production runtime integration, and product readiness remain separate blocked gates.

## Stop Conditions

Stop and record a blocker before any step that would:

- implement V1-G61 without exact approval
- treat this handoff manifest as release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness-claim authority
- treat Arc-Bot-shell compatibility evidence as clean-checkpoint proof for release, final-readiness, branch, tag, cutover, or readiness claims while unrelated local drift remains excluded
- edit consumer repositories from this manifest lane
- add runtime behavior, public API exports, provider SDK clients, runtime vendor SDK imports in `lima/`, lockfile edits, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness

## Next Operator Actions

1. Record exactly one V1-G61 operator choice: `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`.
2. If G61 is approved later, implement only the exact runtime vendor SDK import execution proof scope in `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`.
