# Consumer Checkpoint Manifest

## Recovery Status

LIMA recovery v0.1 has produced a governed dry-run runtime seam.
This is not a full AI OS.
This is not production enforcement.
This is not execution.

The recovery checkpoint proves that LIMA, Guardian Suite, Arc Bot, and Sparkbot have a shared non-executing decision path that can classify requests and return governed decisions without granting runtime authority.

## Repos And Commits

| Component | Repository | Branch | Commit | Remote verification |
|---|---|---|---|---|
| LIMA governed kernel alpha | `armpit-symphony/LIMA-AI-OS` | `recovery-v0-1-guardian-backed-kernel` | `702b0554203f83002815362c7fce783e18ddbf03` | verified by `git ls-remote origin recovery-v0-1-guardian-backed-kernel` |
| Guardian Suite policy core | `armpit-symphony/LIMA-Guardian-Suite` | `recovery-policy-core-alpha` | `fd4da09a059b36195d0886bde20d0419a6b3560a` | verified by `git ls-remote git@github-armpit:armpit-symphony/LIMA-Guardian-Suite.git recovery-policy-core-alpha` |
| Arc Bot LIMA preflight | `armpit-symphony/Arc-Bot-shell` | `arc-lima-governed-preflight-alpha` | `3a565a6ea1518519dbe64119c0e3b4431cc06ac8` | verified by `git ls-remote git@github-armpit:armpit-symphony/Arc-Bot-shell.git arc-lima-governed-preflight-alpha` |
| LIMA Guardian Core integration | `armpit-symphony/LIMA-AI-OS` | `lima-guardian-core-policy-integration-alpha` | `17fab7cbf8befa846444437fd1108847c42ff9c0` | verified by `git ls-remote origin lima-guardian-core-policy-integration-alpha` |
| Sparkbot LIMA decision preview | `sparkpit-labs/Sparkbot` | `sparkbot-lima-decision-preview-alpha` | `20df0ca24deacd6b8df480f8b52873050e086cf8` | verified by `git ls-remote git@github-armpit:armpit-symphony/Sparkbot.git sparkbot-lima-decision-preview-alpha` |

## Working Integration Path

Sparkbot preview path:

```text
Sparkbot preview request
-> optional LIMA import
-> run_governed_request
-> guardian_core.policy decision when available
-> GovernedDecision preview
-> no execution
```

Arc private preflight path:

```text
ArcActionRequest
-> normalize_for_lima
-> run_governed_request
-> guardian_core.policy decision when available
-> GovernedDecision
-> no execution
```

## What Is Working

- LIMA exposes `run_governed_request` from `lima.runtime`.
- Guardian Suite exposes `guardian_core.policy` with `decide_tool_use` and `get_tool_policy`.
- LIMA can map Guardian Core decisions into `GovernedDecision`.
- Arc Bot can call LIMA for governed dry-run preflight and fail closed when LIMA is unavailable.
- Sparkbot can expose a public-safe LIMA decision preview and fail closed when LIMA is unavailable.

## What Remains Blocked

- active Guardian enforcement
- production LIMA wiring
- execution
- model/provider calls
- tool calls
- connector calls
- external sends
- file mutation
- credential access/storage
- approval tokens
- PIN/breakglass flow
- scheduler/background jobs
- robotics
- IoT
- drones
- physical-world actions

## Validation Matrix

| Component | Command | Result |
|---|---|---|
| LIMA Week 1 | `python -m compileall lima tests` | passed |
| LIMA Week 1 | `python -m pytest -q` | 5487 passed, 1 warning |
| LIMA Week 1 | `git diff --check` | passed |
| Guardian Suite Week 2A | `python -m compileall .` | passed |
| Guardian Suite Week 2A | `python -m pytest -q` | 28 passed, 7 warnings |
| Guardian Suite Week 2A | `git diff --check` | passed |
| Arc Week 2B | `python -m compileall .` | passed |
| Arc Week 2B | `python -m pytest -q` | 356 passed |
| Arc Week 2B | `git diff --check` | passed |
| LIMA Guardian Core integration | `python -m compileall lima tests` | passed |
| LIMA Guardian Core integration | `python -m pytest -q` | 5509 passed, 1 warning |
| LIMA Guardian Core integration | `git diff --check` | passed |
| Sparkbot preview | `bash scripts/validate-public-shell.sh` | 22 passed, 32 warnings |
| Sparkbot preview | `bash scripts/check-public-safety.sh` | passed |
| Sparkbot preview | `python -m pytest backend/tests/services/test_lima_decision_preview.py backend/tests/api/routes/test_lima_decision_preview.py -q` | 9 passed, 19 warnings |
| Sparkbot preview | `git diff --check` | passed |

Known non-blocking validation issue:

- Earlier Sparkbot full backend suite report: 653 passed, 41 failed, 1 skipped.
- Verification rerun on this checkpoint: 652 passed, 42 failed, 1 skipped.
- The rerun failures do not touch the new LIMA preview service, route, or tests.
- Failure areas are unrelated Windows/path and chmod behavior in setup/security tests plus existing governance and memory fixture assertions.
- These failures must be fixed or formally classified before merging this preview branch into a public mainline.

## Next Recommended Lanes

1. Fix or classify Sparkbot full backend suite failures.
2. Merge/rebase recovery branches in controlled order.
3. Add package/install guidance for local LIMA + Guardian Core use.
4. Add Arc internal operator UI/status surface for LIMA decisions.
5. Add Sparkbot frontend display for LIMA preview only.
6. Later: approval workflow design, still non-executing.