# V1 Through G57 Candidate Test Runbook

Date: 2026-06-20
Branch: `docs-v1-through-g57-candidate-test-runbook`
Source LIMA commit before runbook: `7888182b1ba0d53aa42f6480db574e7c1975562d`
API status: `CANDIDATE_ONLY`

This runbook gives an operator a repeatable local test path for the current LIMA V1 candidate stack through the G57 request gate across LIMA-AI-OS, public Sparkbot, the accessible Sparkbot checkpoint, and Arc-Bot-shell.

This is test/readiness evidence only. It does not approve V1-G57 implementation, complete V1.0, add provider SDK clients, add SDK dependencies, resolve provider endpoints, make LIMA-owned network calls, read credentials, call providers, wire production consumers, or create product-readiness claims.

## Branch Map

| Repo | Local path | Branch | Commit | Publication status |
| --- | --- | --- | --- | --- |
| LIMA-AI-OS | `C:\Users\limap\LIMA-AI-OS` | `audit-v1-g57-provider-execution-hardening-authorization-request` source checkpoint | `7888182b1ba0d53aa42f6480db574e7c1975562d` | pushed |
| Public Sparkbot target checkout | `C:\Users\limap\Sparkbot-public` | `v1-g56-runtime-authority-chain-audit` | `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | local only, push blocked by GitHub 403 |
| Accessible Sparkbot checkpoint | `C:\Users\limap\Sparkbot` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ddaa4cc` | pushed to `armpit-symphony/Sparkbot` |
| Arc-Bot-shell | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ec06e7670f18eeae192fc0f995b6ffd07481d8c9` | pushed |

## Checkout Preflight

Run these before validating. Stop on unexpected dirty worktrees unless the changes are already known, unrelated, and separately recorded.

```powershell
git -C C:\Users\limap\LIMA-AI-OS status --short --branch
git -C C:\Users\limap\Sparkbot-public -c safe.directory='C:/Users/limap/Sparkbot-public' status --short --branch
git -C C:\Users\limap\Sparkbot status --short --branch
git -C C:\Users\limap\Arc-Bot-shell status --short --branch
```

Expected current notes:

- LIMA-AI-OS should be clean on this runbook branch or on the audited G57 source checkpoint.
- Sparkbot-public should be clean on `v1-g56-runtime-authority-chain-audit`; push to `sparkpit-labs/Sparkbot` is still blocked by credentials.
- Accessible Sparkbot should be clean on `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke`.
- Arc-Bot-shell has a pushed G56 commit, but the local worktree may contain unrelated pre-existing dirty files outside the G56 smoke scope. Do not treat those unrelated files as LIMA G57 evidence.

## Validation Order

Run the consumer smoke tests first, then LIMA. This keeps consumer import/call breakage separate from LIMA evidence breakage.

| Step | Path | Command | Expected current result |
| --- | --- | --- | --- |
| 1 | `C:\Users\limap\Sparkbot-public` | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 2 | `C:\Users\limap\Sparkbot-public` | `git diff --check` | pass |
| 3 | `C:\Users\limap\Sparkbot` | `python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 4 | `C:\Users\limap\Sparkbot` | `git diff --check` | pass |
| 5 | `C:\Users\limap\Arc-Bot-shell` | `python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider` | `8 passed` |
| 6 | `C:\Users\limap\Arc-Bot-shell` | `git diff --check` | pass for the G56 scope; unrelated dirty files remain outside this evidence |
| 7 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests/test_v1_g57_provider_execution_hardening_authorization_request_audit.py tests/test_v1_g57_provider_execution_hardening_authorization_approval_request.py tests/test_v1_runtime_authority_chain_through_g56.py tests/test_v1_runtime_readiness_rollup_through_g56.py tests/test_v1_post_g56_next_lane_decision_matrix.py -p no:cacheprovider` | `41 passed` or better after runbook test additions |
| 8 | `C:\Users\limap\LIMA-AI-OS` | `python -m compileall lima` | pass |
| 9 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests -p no:cacheprovider` | pass; source audit baseline was `4978 passed` |
| 10 | `C:\Users\limap\LIMA-AI-OS` | `git diff --check` | pass |

## Candidate Evidence Proven

- Sparkbot-public can import the approved G55 public wrapper symbols from the local LIMA checkout and call the wrapper with fake in-process provider SDK/network executors only.
- Accessible Sparkbot carries the same G56 two-file checkpoint and passes the same fake-executor smoke test.
- Arc-Bot-shell can import the approved G55 public wrapper symbols from the local LIMA checkout and call the wrapper with fake in-process provider SDK/network executors only.
- LIMA-AI-OS records G56 as the latest completed candidate gate and G57 as the next request-only operator decision gate.
- G57 remains unapproved and request-only until an explicit operator decision is recorded.

## Boundary Results To Preserve

- No V1-G57 implementation approval.
- No G57 provider execution hardening authorization evidence implementation.
- No `lima/` runtime change from this runbook.
- No public API export change from this runbook.
- No provider SDK clients.
- No built-in provider SDK clients.
- No SDK dependencies.
- No vendor provider SDK imports.
- No endpoint resolution execution.
- No LIMA-owned DNS, HTTP, socket, or provider network call.
- No direct provider egress by LIMA.
- No credential lookup, credential value access, provider token access, or API key access.
- No provider configuration changes.
- No fallback execution.
- No connector/browser/network/file/device/robotics/physical-world authority from LIMA.
- No consumer production runtime integration.
- No public Sparkbot target push to `sparkpit-labs/Sparkbot` until write credentials are available.
- No product readiness, production readiness, or V1.0 completion claim.

## Stop Conditions

Stop and record a blocker if any of these occur:

- A repo is on an unexpected branch or commit and the drift is not understood.
- A worktree has unreviewed dirty changes that affect the intended evidence scope.
- Any consumer validation command fails.
- Any LIMA focused, compile, full-suite, or diff-check validation fails.
- Any test requires secrets, provider tokens, credential values, SDK clients, endpoint resolution, non-local network, or direct provider egress.
- Any step attempts to modify or push public Sparkbot target repository state without GitHub write permission.
- Any step would implement V1-G57 without exact `Approve-V1-G57` approval.

## Evidence Capture

For each run, record:

- repo path
- branch
- commit
- command
- pass/fail result
- stderr warnings if any
- whether the boundary results above stayed false

Keep evidence sanitized. Do not store raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw file contents, raw diffs, or raw patch bodies in LIMA audit/readiness metadata.

## Known Blockers

Public Sparkbot target publication is still blocked:

- target repo: `sparkpit-labs/Sparkbot`
- local branch: `v1-g56-runtime-authority-chain-audit`
- local commit: `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2`
- blocker: GitHub 403 for the current credential

V1-G57 remains blocked until the operator records exactly one valid choice in `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md`: `Approve-V1-G57`, `Revise-V1-G57`, or `Pause`.

## Next Smallest Safe Step

If G57 remains unapproved, keep work to docs/tests/fixtures-only readiness evidence, branch/test runbooks, audit metadata, or public Sparkbot push/auth unblock work. If `Approve-V1-G57` is explicitly recorded later, implement only the exact metadata-only provider execution hardening authorization scope in `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md`.
