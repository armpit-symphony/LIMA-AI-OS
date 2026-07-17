# V1 Consumer Work/Settings Test Runbook

Date: 2026-06-19
Branch: `docs-v1-consumer-work-settings-test-runbook`
Source LIMA commit before runbook: `dbdcca147c44539e9c4cdd302b3eb05c1af067ed`
API status: `CANDIDATE_ONLY`

This runbook gives an operator a repeatable local test path for the current LIMA V1 consumer Work/Settings preview stack across LIMA-AI-OS, public Sparkbot, Sparkbot Shell, and Arc-Bot-shell.

This is test/readiness evidence only. It does not approve V1-G55 implementation, complete V1.0, add provider SDK/network egress, read credentials, call providers, wire production consumers, or create product-readiness claims.

## Branch Map

| Repo | Local path | Branch | Commit |
| --- | --- | --- | --- |
| LIMA-AI-OS | `C:\Users\limap\LIMA-AI-OS` | `docs-v1-consumer-testability-through-work-settings` source checkpoint | `dbdcca147c44539e9c4cdd302b3eb05c1af067ed` |
| Public Sparkbot preview | `C:\Users\limap\Sparkbot-public` | `public-work-settings-preview` | `81eed8c4067b1a73885bbc79003ea5870b1604a2` |
| Sparkbot Shell | `C:\Users\limap\Sparkbot_shell` | `sparkbot-shell-work-settings-runtime-preview` | `548b6d6aa6cde98b261e867c0c2db86ddbfa83dc` |
| Arc-Bot-shell | `C:\Users\limap\Arc-Bot-shell` | `arc-work-queue-runtime-settings-docs` | `a05faea14ab24341b4b4567967911e33e51ce88a` |

## Checkout Preflight

Run these commands before validating the stack. Stop on dirty worktrees unless the changes are expected and separately recorded.

```powershell
git -C C:\Users\limap\LIMA-AI-OS status --short --branch
git -C C:\Users\limap\Sparkbot-public status --short --branch
git -C C:\Users\limap\Sparkbot_shell status --short --branch
git -C C:\Users\limap\Arc-Bot-shell status --short --branch
```

If a repo is not on the expected branch, switch to the named branch and re-run status:

```powershell
git -C C:\Users\limap\Sparkbot-public switch public-work-settings-preview
git -C C:\Users\limap\Sparkbot_shell switch sparkbot-shell-work-settings-runtime-preview
git -C C:\Users\limap\Arc-Bot-shell switch arc-work-queue-runtime-settings-docs
```

## Validation Order

Run the consumer repos first, then LIMA. This keeps consumer breakage separate from LIMA evidence breakage.

| Step | Path | Command | Expected current result |
| --- | --- | --- | --- |
| 1 | `C:\Users\limap\Arc-Bot-shell` | `python -B -m pytest -q tests -p no:cacheprovider` | `93 passed in 0.27s` |
| 2 | `C:\Users\limap\Arc-Bot-shell` | `git diff --check` | pass |
| 3 | `C:\Users\limap\Sparkbot_shell` | `python -B -m pytest -q tests -p no:cacheprovider` | `13 passed in 0.04s` |
| 4 | `C:\Users\limap\Sparkbot_shell` | `npm run build` | passed: `tsc --noEmit && vite build` |
| 5 | `C:\Users\limap\Sparkbot_shell` | `git diff --check` | pass |
| 6 | `C:\Users\limap\Sparkbot-public` | `.\\.venv-public-test\\Scripts\\python.exe -B -m pytest -q backend\\tests\\test_capabilities.py -p no:cacheprovider` | `4 passed, 1 Starlette/httpx deprecation warning` |
| 7 | `C:\Users\limap\Sparkbot-public\frontend` | `npm run test -- --run` | `1 test file passed, 4 tests passed` |
| 8 | `C:\Users\limap\Sparkbot-public\frontend` | `npm run build` | passed: `vite build` |
| 9 | `C:\Users\limap\Sparkbot-public` | `git diff --check` | pass |
| 10 | `C:\Users\limap\LIMA-AI-OS` | `python -m compileall lima` | pass |
| 11 | `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests -p no:cacheprovider` | pass; source matrix baseline was `4703 passed` before this runbook |
| 12 | `C:\Users\limap\LIMA-AI-OS` | `git diff --check` | pass |

## User-Visible Smoke Targets

Public Sparkbot preview:

- Work/Local AI settings preview renders from the `public-work-settings-preview` branch.
- The backend capabilities test remains limited to capability metadata.
- No public Sparkbot target PR is created by this runbook.

Sparkbot Shell:

- Work route is testable as a local browser preview.
- Settings route is testable as a local browser preview.
- Local file ingestion and in-memory edit preview remain local browser behavior.
- Endpoint reachability checks remain limited to localhost and loopback targets.

Arc-Bot-shell:

- Work Queue operator-console docs/tests remain testable.
- Runtime Settings operator-console docs/tests remain testable.
- Runtime boundaries remain documented and fail-closed.

LIMA-AI-OS:

- G54 fake SDK/fake-egress harness evidence remains candidate-only.
- G55 remains request-only unless exact `Approve-V1-G55` wording is recorded later.
- Consumer Work/Settings readiness evidence remains separate from product readiness.

## Boundary Results To Preserve

- No V1-G55 implementation approval.
- No G55 runtime wrapper.
- No `lima/` runtime change from this runbook.
- No public API export change from this runbook.
- No provider SDK/network egress runtime.
- No built-in provider SDK clients.
- No SDK dependencies.
- No endpoint resolution execution.
- No LIMA-owned DNS, HTTP, socket, or provider network call.
- No credential lookup, credential value access, provider token access, or API key access.
- No non-local endpoint checks.
- No connector/browser/network/file/device/robotics/physical-world authority from LIMA.
- No consumer production runtime integration.
- No public Sparkbot target PR into `sparkpit-labs/Sparkbot`.
- No product readiness, production readiness, or V1.0 completion claim.

## Stop Conditions

Stop and record a blocker if any of these occur:

- A repo is on an unexpected branch or commit and the drift is not understood.
- A worktree has unreviewed dirty changes.
- Any consumer validation command fails.
- Any LIMA focused, coupled, compile, full-suite, or diff-check validation fails.
- Any test or preview requires secrets, provider tokens, credential values, SDK clients, endpoint resolution, non-local network, or direct provider egress.
- Any step attempts to modify public Sparkbot target repository state without GitHub auth/write permission.
- Any step would implement V1-G55 without exact `Approve-V1-G55` approval.

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

The public Sparkbot preview branch is saved on the accessible fork, but the target PR still needs GitHub auth/write permission or a working cross-repo PR creation path:

`https://github.com/sparkpit-labs/Sparkbot/compare/main...armpit-symphony:public-work-settings-preview?expand=1`

V1-G55 remains blocked until the operator records exactly one valid choice in `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`: `Approve-V1-G55`, `Revise-V1-G55`, or `Pause`.

## Next Smallest Safe Step

If G55 remains unapproved, keep work to docs/tests/fixtures-only readiness evidence, branch/test runbooks, audit metadata, or public Sparkbot PR/auth unblock work. If `Approve-V1-G55` is explicitly recorded later, implement only the exact bounded LIMA-side real provider SDK/network egress authority wrapper scope in `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_APPROVAL_REQUEST.md`.
