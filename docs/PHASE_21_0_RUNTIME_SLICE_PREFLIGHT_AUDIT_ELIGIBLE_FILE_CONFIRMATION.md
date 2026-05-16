# Phase 21.0 Runtime Slice Preflight Audit / Eligible File Confirmation

Phase 21.0 opens the approved Phase 21 runtime slice with a preflight audit and eligible-file confirmation.

This phase does not implement runtime behavior. It confirms the Phase 20.2 file-touch map before any runtime code is changed.

## Eligible Runtime Files

The only runtime files eligible for Phase 21 candidate provenance hardening are:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`

## Forbidden Runtime Files

Phase 21 must not touch:

- `lima/kernel/__init__.py`
- any new runtime module
- any other `lima/` file
- any `tests/support/` file

## Runtime Boundary

Phase 21 is limited to pure in-process candidate provenance hardening for existing non-executing candidates. It must not create a HumanInput runtime bridge, wire Sparkbot, add live adapters, change IntentCompiler or GuardianDecision runtime behavior, enforce approval, execute, dispatch, persist audit, call shell/browser/network/filesystem mutation/robotics/external services, start background workers, queues, daemons, subprocesses, threads, write databases, or create hidden side effects.

## Gate

Phase 21.0 confirms that Phase 20.2 is unambiguous. Implementation may proceed only inside the two eligible runtime files and only after Phase 21.1 acceptance tests are scaffolded.
