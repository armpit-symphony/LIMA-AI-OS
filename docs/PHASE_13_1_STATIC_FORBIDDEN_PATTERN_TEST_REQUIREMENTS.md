# Phase 13.1 Static Forbidden-Pattern Test Requirements

Phase 13.1 defines future static forbidden-pattern test requirements derived from the Phase 12.2 threat model.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add static-test implementation code, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Static Check Requirements

Future static tests should scan approved runtime slices for:

- forbidden imports: `subprocess`, `socket`, `requests`, `urllib`, `httpx`, `webbrowser`, `threading`, `multiprocessing`, Sparkbot modules, live adapter modules
- forbidden calls: `system`, `popen`, `run`, `call`, `Popen`, `open`, `write`, `unlink`, `remove`, `rename`, `replace`, `dispatch`, `execute`, `approve`, `persist`
- forbidden boundary names: `HumanInputBridge`, `IntentCompiler`, `GuardianDecision`, `Sparkbot`, `RoboOSDriver`, `ApprovalEnforcer`, `AuditWriter`
- forbidden behavior claims: approval granted, execution allowed, side effects allowed, dispatched, persisted, live adapter connected

## Static-Test Scope

Static checks are necessary but not sufficient. They must be paired with contract tests, fixtures, and future acceptance gates before runtime work expands.

## Next Step

Phase 13.2 should define runtime contract test requirements for candidate invariants.
