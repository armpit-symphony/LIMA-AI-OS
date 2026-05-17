# Phase 38.3 Sparkbot-to-LIMA Gap and Risk Matrix

Phase 38.3 compares Sparkbot v1.6.80 concepts with current LIMA runtime slices and identifies the safest next lane.

This phase is docs/tests/fixtures-only. It does not modify LIMA runtime files, Sparkbot files, `tests/support/`, helper behavior, or any execution/approval/dispatch/persistence/integration path.

## Current LIMA Support

Current LIMA runtime slices already support two bounded concepts:

- `runtime_state` can inspect caller-provided state in a read-only, deterministic, non-authoritative way.
- `candidate_preview` can preview caller-provided candidate-shaped data while keeping execution, side effects, approval, dispatch, persistence, bridge behavior, Sparkbot wiring, live adapters, external calls, robotics, and physical-world behavior disallowed.

These are enough to accept Sparkbot-shaped fixture inputs in tests. They are not enough to implement Sparkbot integration.

## Gap And Risk Matrix

| Sparkbot concept | Current LIMA status | Gap | Risk | Phase 39 recommendation |
| --- | --- | --- | --- | --- |
| Owner-local routine read posture | Vocabulary only | Need Sparkbot-shaped candidate fixtures proving owner-local does not authorize LIMA runtime reads. | Medium if confused with permission. | Test-only hardening. |
| Strict Security risky write posture | Vocabulary only | Need fixture coverage for risky write requests mapping to blocked/approval-needed preview output. | Medium. | Test-only hardening. |
| Breakglass/Vault posture | Vocabulary only | Need fixture coverage proving breakglass wording and Vault claims do not grant approval. | High. | Test-only hardening. |
| Policy simulation / explain-plan | Vocabulary only | Need fixture coverage for explain-plan requests remaining preview-only. | Medium. | Test-only hardening. |
| Persistent approvals / approval inbox | Vocabulary only | Need fixture coverage proving persistent approval claims do not create persistence or approval. | High. | Test-only hardening. |
| Agent identity / kill switch | Vocabulary only | Need fixture coverage proving disabled/kill-switch agents remain non-routable preview metadata. | Medium. | Test-only hardening. |
| Memory trust metadata | Vocabulary only | Need fixture coverage proving low-confidence memory writes remain pending/blocked preview metadata. | Medium. | Test-only hardening. |
| MCP/Robo OS manifests | Vocabulary only | Need fixture coverage proving manifest-shaped data does not connect to MCP. | High. | Test-only hardening. |
| Robotics simulation and real hardware | Vocabulary only | Need fixture coverage proving simulation stays preview-only and real hardware stays blocked. | Critical. | Test-only hardening. |
| Run timeline / audit hash | Vocabulary only | Need fixture coverage proving audit claims do not persist audit. | Medium. | Test-only hardening. |

## Not Recommended

No runtime implementation is recommended from Phase 38.

Not recommended now:

- Sparkbot wiring/imports.
- HumanInput runtime bridge behavior.
- Live adapters.
- Approval enforcement.
- Execution.
- Dispatch.
- Audit persistence.
- MCP connection.
- Robotics or physical-world behavior.
- External service calls.
- Background work, subprocesses, threads, queues, daemons, or database writes.

## Recommended Phase 39

Recommend Phase 39 as test-only hardening of `candidate_preview` with Sparkbot-shaped fixtures.

The hardening should use caller-provided JSON fixtures only and prove these examples remain non-executing, non-authoritative, and side-effect free:

- owner-local routine read request
- strict-security risky write request
- breakglass-required Vault request
- MCP explain-plan request
- Robo OS simulation request
- real-hardware robot-motion request
- agent identity with `kill_switch=true`
- low-confidence memory write requiring pending approval

Phase 39 must not modify `lima/`, `tests/support/`, Sparkbot, or stale prior-phase tests.

## Continue

Continue only to Phase 38.4 alignment archive and closeout.
