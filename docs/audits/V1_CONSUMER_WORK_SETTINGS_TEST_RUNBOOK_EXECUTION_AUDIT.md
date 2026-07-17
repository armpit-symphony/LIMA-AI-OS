# V1 Consumer Work/Settings Test Runbook Execution Audit

Date: 2026-06-19
Audit branch: `audit-v1-consumer-work-settings-test-runbook-execution`
Source LIMA commit before audit: `7f90c83946d7974e5f60294b1a602a1de3be4e51`
API status: `CANDIDATE_ONLY`

This audit records a sanitized execution of `docs/runbooks/V1_CONSUMER_WORK_SETTINGS_TEST_RUNBOOK.md` against the current local consumer branches for public Sparkbot, Sparkbot Shell, Arc-Bot-shell, and LIMA-AI-OS.

The audit is LIMA-side evidence only. It does not approve V1-G55 implementation, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK/network egress, read credentials, call providers, create the public Sparkbot target PR, or claim V1.0/product readiness.

## Audit Verdict

Runbook execution status: `pass_current_consumer_work_settings_stack`.

The current Work/Settings consumer test stack is repeatable from local branch checkouts:

- Arc-Bot-shell Work Queue / Runtime Settings tests passed.
- Sparkbot Shell Work/Settings local browser preview tests and build passed.
- Public Sparkbot Work/Local AI settings preview backend and frontend checks passed.
- LIMA-AI-OS compile and full test suite passed.
- Diff checks passed for Arc-Bot-shell, Sparkbot Shell, public Sparkbot, and LIMA-AI-OS.

This proves the current preview branches are locally testable. It does not prove production integration, live provider/model generation through LIMA, provider SDK/network egress, public Sparkbot target PR creation, or V1.0 readiness.

## Branch And Commit Evidence

| Repo | Branch | Commit | Status |
| --- | --- | --- | --- |
| LIMA-AI-OS | `docs-v1-consumer-work-settings-test-runbook` source checkpoint | `7f90c83946d7974e5f60294b1a602a1de3be4e51` | clean before audit branch |
| Public Sparkbot preview | `public-work-settings-preview` | `81eed8c4067b1a73885bbc79003ea5870b1604a2` | clean |
| Sparkbot Shell | `sparkbot-shell-work-settings-runtime-preview` | `548b6d6aa6cde98b261e867c0c2db86ddbfa83dc` | clean |
| Arc-Bot-shell | `arc-work-queue-runtime-settings-docs` | `a05faea14ab24341b4b4567967911e33e51ce88a` | clean during initial branch/commit check; final post-validation status later showed local uncommitted Arc changes outside this LIMA audit branch |

## Executed Validation

| Repo | Command | Result |
| --- | --- | --- |
| `C:\Users\limap\Arc-Bot-shell` | `python -B -m pytest -q tests -p no:cacheprovider` | `93 passed in 0.24s` |
| `C:\Users\limap\Arc-Bot-shell` | `git diff --check` | passed |
| `C:\Users\limap\Sparkbot_shell` | `python -B -m pytest -q tests -p no:cacheprovider` | `13 passed in 0.04s` |
| `C:\Users\limap\Sparkbot_shell` | `npm run build` | passed: `tsc --noEmit && vite build`; Vite built 61 modules |
| `C:\Users\limap\Sparkbot_shell` | `git diff --check` | passed |
| `C:\Users\limap\Sparkbot-public` | `.\\.venv-public-test\\Scripts\\python.exe -B -m pytest -q backend\\tests\\test_capabilities.py -p no:cacheprovider` | `4 passed, 1 StarletteDeprecationWarning in 0.27s` |
| `C:\Users\limap\Sparkbot-public\frontend` | `npm run test -- --run` | `1 test file passed, 4 tests passed` |
| `C:\Users\limap\Sparkbot-public\frontend` | `npm run build` | passed: `vite build`; Vite built 32 modules |
| `C:\Users\limap\Sparkbot-public` | `git diff --check` | passed |
| `C:\Users\limap\LIMA-AI-OS` | `python --version` | `Python 3.12.10` |
| `C:\Users\limap\LIMA-AI-OS` | `python -m compileall lima` | passed |
| `C:\Users\limap\LIMA-AI-OS` | `python -m pytest -q tests -p no:cacheprovider` | `4709 passed in 4.04s` |
| `C:\Users\limap\LIMA-AI-OS` | `git diff --check` | passed |

## Scope Audit

- File scope of this audit branch: docs/tests/fixtures only.
- `lima/` runtime files changed by this audit: no.
- LIMA public API exports changed by this audit: no.
- Consumer repository files changed by this audit: no.
- Public Sparkbot target repository state changed by this audit: no.
- Public Sparkbot target PR created by this audit: no.
- V1-G55 implementation approved or started by this audit: no.

## Post-validation Consumer Status Note

After the LIMA audit branch was pushed, a final status check showed local Arc-Bot-shell changes in:

- `README.md`
- `docs/OPERATOR_CONSOLE_FOUNDATION.md`
- `docs/ROADMAP.md`
- `tests/test_arc_bot_phase0_scope_lock_runtime_ui.py`

Those Arc-Bot-shell files are not part of this LIMA audit branch, were not staged or committed by this audit, and are not used as proof of LIMA V1 readiness. The recorded Arc validation result remains the executed `pytest` result and the `git diff --check` result from this runbook execution. Treat the later Arc working-tree drift as a separate consumer-repo status item before any future Arc checkpoint.

## Boundary Results

- G55 runtime wrapper added: no.
- Provider SDK/network egress runtime added: no.
- Built-in provider SDK clients added: no.
- SDK dependencies or vendor SDK imports added: no.
- Endpoint resolution execution added: no.
- LIMA-owned DNS, HTTP, socket, network calls, or direct provider egress added: no.
- Secret lookup, credential value access, provider token access, or API key access added: no.
- Provider configuration change or fallback execution added: no.
- Non-local endpoint checks allowed: no.
- LIMA connector/browser/network/file/device/robotics/physical-world authority added: no.
- Consumer production runtime integration added: no.
- Product readiness, production readiness, or V1.0 completion claim added: no.

## Sanitization Audit

The evidence recorded here is command/status metadata only. It does not store raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw file contents, raw diffs, or raw patch bodies.

The public Sparkbot backend warning is recorded as a dependency deprecation warning only: `StarletteDeprecationWarning`. It does not expose credentials or customer data.

## Known Blockers

- Public Sparkbot target PR into `sparkpit-labs/Sparkbot` still needs GitHub auth/write permission or a working cross-repo PR creation path.
- V1-G55 remains blocked until exactly one valid operator choice is recorded in `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`: `Approve-V1-G55`, `Revise-V1-G55`, or `Pause`.
- V1 remains `CANDIDATE_ONLY`; this audit does not establish product readiness.

## Audit Decision

The V1 consumer Work/Settings test runbook passes against the current local branch stack.

Recommended next step: keep the consumer preview branches separate and testable, unblock public Sparkbot PR creation when GitHub permissions are available, and keep V1-G55 runtime implementation blocked until exact `Approve-V1-G55` approval is recorded.
