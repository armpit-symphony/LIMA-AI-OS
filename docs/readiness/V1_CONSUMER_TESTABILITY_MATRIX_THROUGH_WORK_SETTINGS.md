# V1 Consumer Testability Matrix Through Work/Settings

Date: 2026-06-18
Branch: `docs-v1-consumer-testability-through-work-settings`
Source LIMA commit before matrix: `525648d1d7ef536dc89e793095db89f69728c015`
API status: `CANDIDATE_ONLY`

This matrix records the current testable consumer surface for LIMA V1 after the Work/Settings branches in public Sparkbot, Sparkbot Shell, and Arc-Bot-shell. It is readiness/testability evidence only. It does not approve V1-G55 implementation, modify `lima/`, change public API exports, add provider SDK/network egress, read credentials, call providers, or claim V1.0 readiness.

## Testable Consumer Branches

| Consumer | Repository | Branch | Commit | Testability status |
| --- | --- | --- | --- | --- |
| Public Sparkbot preview | `armpit-symphony/Sparkbot` fork for `sparkpit-labs/Sparkbot` | `public-work-settings-preview` | `81eed8c4067b1a73885bbc79003ea5870b1604a2` | Work/Local AI settings static preview is testable on fork branch; target PR still blocked |
| Sparkbot Shell | `armpit-symphony/Sparkbot_shell` | `sparkbot-shell-work-settings-runtime-preview` | `548b6d6aa6cde98b261e867c0c2db86ddbfa83dc` | Work route and Settings route are testable as bounded local browser preview |
| Arc-Bot-shell | `armpit-symphony/Arc-Bot-shell` | `arc-work-queue-runtime-settings-docs` | `a05faea14ab24341b4b4567967911e33e51ce88a` | Work Queue and Runtime Settings operator-console docs/tests are testable |
| LIMA-AI-OS | `armpit-symphony/LIMA-AI-OS` | `audit-v1-consumer-work-settings-readiness` | `525648d1d7ef536dc89e793095db89f69728c015` | LIMA-side consumer Work/Settings readiness audit is testable |

## Current Validation Commands

Run these from the local checkout paths named in the repository column.

| Repo | Command | Current result |
| --- | --- | --- |
| `C:\Users\limap\Arc-Bot-shell` | `python -B -m pytest -q tests -p no:cacheprovider` | `93 passed in 0.27s` |
| `C:\Users\limap\Sparkbot_shell` | `python -B -m pytest -q tests -p no:cacheprovider` | `13 passed in 0.04s` |
| `C:\Users\limap\Sparkbot_shell` | `npm run build` | passed: `tsc --noEmit && vite build` |
| `C:\Users\limap\Sparkbot-public` | `.\\.venv-public-test\\Scripts\\python.exe -B -m pytest -q backend\\tests\\test_capabilities.py -p no:cacheprovider` | `4 passed, 1 Starlette/httpx deprecation warning` |
| `C:\Users\limap\Sparkbot-public\frontend` | `npm run test -- --run` | `1 test file passed, 4 tests passed` |
| `C:\Users\limap\Sparkbot-public\frontend` | `npm run build` | passed: `vite build` |
| `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests -p no:cacheprovider` | `4698 passed` on the source LIMA audit checkpoint |

## What This Proves

- The first consumer Work/Settings surfaces are testable from named branches.
- Public Sparkbot has a safe static Work/Local AI settings preview branch with backend/frontend checks.
- Sparkbot Shell has a bounded local browser preview branch with tests proving file ingestion, in-memory edits, simulated network-index search, and localhost/loopback-only endpoint checks stay scoped.
- Arc-Bot-shell has operator-console Work Queue and Runtime Settings docs/tests with fail-closed runtime boundaries.
- LIMA has a matching readiness audit that records those consumer branches and their blockers.

## What This Does Not Prove

- No V1-G55 implementation approval.
- No LIMA provider SDK/network egress runtime.
- No built-in provider SDK clients.
- No provider/model generation through LIMA.
- No credential lookup, credential value access, provider token access, or API key access.
- No non-local endpoint checks.
- No connector/browser/network/file/device/robotics/physical-world authority from LIMA.
- No consumer production runtime integration.
- No public Sparkbot target PR into `sparkpit-labs/Sparkbot`.
- No product readiness, production readiness, or V1.0 completion.

## Manual Public Sparkbot PR Path

The public Sparkbot preview branch remains saved on the accessible fork:

`https://github.com/sparkpit-labs/Sparkbot/compare/main...armpit-symphony:public-work-settings-preview?expand=1`

Creating that PR still requires GitHub auth/write permission for `sparkpit-labs/Sparkbot` or a working cross-repo PR creation path.

## Next Decision Point

Keep these branches separate and testable while the V1-G55 decision remains pending. If `Approve-V1-G55` is explicitly recorded, implement only the bounded LIMA-side real provider SDK/network egress authority wrapper named in the G55 approval request. If G55 stays pending, the next safe work is docs/tests/fixtures-only readiness evidence or PR/auth unblock work for the public Sparkbot target.
