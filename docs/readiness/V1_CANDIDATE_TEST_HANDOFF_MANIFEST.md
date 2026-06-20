# V1 Candidate Test Handoff Manifest

Date: 2026-06-20
Branch: `docs-v1-candidate-test-handoff-manifest`
Source LIMA commit before manifest: `992c17107830f2e0ea464301d864b24a855b5d6d`
API status: `CANDIDATE_ONLY`

This manifest is the current operator handoff index for local V1 candidate testing across LIMA-AI-OS, public Sparkbot, the accessible Sparkbot checkpoint, and Arc-Bot-shell.

It is docs/tests/fixtures-only readiness evidence. It does not approve V1-G57 implementation, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK clients, add SDK dependencies, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, invoke connectors, wire consumer production runtime behavior, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Handoff Verdict

Verdict: `READY_FOR_LOCAL_CANDIDATE_TESTING_WITH_BLOCKERS`

The current candidate is testable locally with fake in-process provider SDK/network executors only. Public Sparkbot remote publication remains blocked by missing write credentials for `sparkpit-labs/Sparkbot`, and V1-G57 remains unapproved until an explicit operator choice is recorded.

## Source Evidence

- V1 through G57 candidate test runbook: `docs/runbooks/V1_THROUGH_G57_CANDIDATE_TEST_RUNBOOK.md`
- V1-G56 public Sparkbot target publication audit: `docs/audits/V1_G56_PUBLIC_SPARKBOT_TARGET_PUBLICATION_AUDIT.md`
- V1-G56 consumer fake-executor provider SDK/network egress smoke audit: `docs/audits/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_AUDIT.md`
- V1 runtime authority chain through G56 audit: `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G56_AUDIT.md`
- V1 runtime readiness rollup through G56: `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G56.md`
- V1 post-G56 next-lane decision matrix: `docs/readiness/V1_POST_G56_NEXT_LANE_DECISION_MATRIX.md`
- V1-G57 request audit: `docs/audits/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_REQUEST_AUDIT.md`
- V1-G57 approval request: `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md`

## Repository Checkpoints

| Repo | Local path | Branch | Commit | Remote state |
| --- | --- | --- | --- | --- |
| LIMA-AI-OS | `C:\Users\limap\LIMA-AI-OS` | `audit-v1-g56-public-sparkbot-target-publication` | `992c17107830f2e0ea464301d864b24a855b5d6d` | pushed |
| Public Sparkbot target checkout | `C:\Users\limap\Sparkbot-public` | `v1-g56-runtime-authority-chain-audit` | `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | local only; target branch absent on `sparkpit-labs/Sparkbot` |
| Accessible Sparkbot checkpoint | `C:\Users\limap\Sparkbot` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ddaa4ccaacd328ddcc1f00a040c2c140abee428e` | pushed to `armpit-symphony/Sparkbot` |
| Arc-Bot-shell | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ec06e7670f18eeae192fc0f995b6ffd07481d8c9` | pushed; local worktree has unrelated dirty files outside G56 evidence |

## Local Candidate Validation Commands

Run these commands from the listed paths. Stop on any failure.

| Step | Path | Command | Expected result |
| --- | --- | --- | --- |
| 1 | `C:\Users\limap\Sparkbot-public` | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 2 | `C:\Users\limap\Sparkbot-public` | `git diff --check` | pass |
| 3 | `C:\Users\limap\Sparkbot` | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 4 | `C:\Users\limap\Sparkbot` | `git diff --check` | pass |
| 5 | `C:\Users\limap\Arc-Bot-shell` | `python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 6 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests/test_v1_g56_public_sparkbot_target_publication_audit.py tests/test_v1_through_g57_candidate_test_runbook.py tests/test_v1_g57_provider_execution_hardening_authorization_request_audit.py tests/test_v1_runtime_authority_chain_through_g56.py tests/test_v1_runtime_readiness_rollup_through_g56.py -p no:cacheprovider` | pass |
| 7 | `C:\Users\limap\LIMA-AI-OS` | `python -m compileall lima` | pass |
| 8 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests -p no:cacheprovider` | pass |
| 9 | `C:\Users\limap\LIMA-AI-OS` | `git diff --check` | pass |

## Candidate Scope Proven

- Public Sparkbot can import the approved G55 public wrapper symbols and call them with a fake in-process provider SDK/network executor in local tests.
- Accessible Sparkbot carries the pushed G56 fake-executor smoke checkpoint.
- Arc-Bot-shell carries the pushed G56 fake-executor smoke checkpoint.
- LIMA-AI-OS records the runtime authority chain through G56 and G57 as a request-only operator gate.
- The local candidate remains bounded to fake/caller-injected execution evidence and sanitized fixtures.

## Required Boundaries

The following must remain false while this manifest is the current handoff:

- V1-G57 implementation approval recorded
- V1-G57 provider execution hardening authorization implemented
- public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot`
- `lima/` runtime files changed by this manifest
- LIMA public API exports changed by this manifest
- Sparkbot or Arc-Bot-shell files changed by this manifest
- provider SDK clients added
- SDK dependencies added
- vendor provider SDK imports added
- LIMA-owned provider endpoint resolution added
- LIMA-owned DNS/HTTP/socket/network calls added
- direct provider egress by LIMA added
- secret lookup or credential value access added
- provider token or API key access added
- provider configuration changes added
- fallback execution added
- connector, browser, file, device, robotics, or physical-world behavior added
- consumer production runtime integration added
- V1.0 completion, product-readiness, or production-readiness claimed

## Current Blockers

- Public Sparkbot publication: blocked until a credential with write access to `sparkpit-labs/Sparkbot` is available.
- V1-G57 implementation: blocked until exactly one valid operator choice is recorded, and implementation may proceed only if that choice is `Approve-V1-G57`.
- Arc-Bot-shell local worktree: dirty with unrelated files outside the pushed G56 evidence; do not use those files as LIMA V1 proof until separately audited.

## Stop Conditions

Stop and record a blocker before any step that would:

- push public Sparkbot without write credentials
- implement V1-G57 without exact approval
- edit consumer repositories from this manifest lane
- add runtime behavior, public API exports, provider SDK clients, SDK dependencies, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness

## Next Operator Actions

1. Provide or switch to public Sparkbot write credentials, then publish the saved `v1-g56-runtime-authority-chain-audit` branch to `sparkpit-labs/Sparkbot`.
2. Record exactly one V1-G57 operator choice: `Approve-V1-G57`, `Revise-V1-G57`, or `Pause`.
3. If G57 is approved later, implement only the metadata-only file scope in `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md`.
