# Phase 15.1 Future Static Test Implementation Plan

Phase 15.1 proposes the future static forbidden-pattern test implementation package without implementing it.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not implement actual future static acceptance tests, does not add scanner utilities, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Proposed Future Test File

Future test-only implementation may create:

- `tests/test_acceptance_static_forbidden_patterns.py`

This file is proposed for a later explicitly approved phase only.

## Proposed Future Static Tests

- `test_runtime_files_have_no_sparkbot_imports`: assert runtime files do not import Sparkbot modules.
- `test_runtime_files_have_no_live_adapter_imports`: assert runtime files do not import live adapter modules.
- `test_runtime_files_have_no_humaninput_bridge_imports`: assert runtime files do not create or import HumanInput runtime bridge behavior.
- `test_runtime_files_have_no_execution_or_dispatch_calls`: assert runtime files do not call execution, dispatch, subprocess, shell, browser, network, file mutation, robotics, or physical-world APIs.
- `test_runtime_files_have_no_approval_or_audit_persistence_calls`: assert runtime files do not enforce approval or persist audit.
- `test_runtime_files_have_no_authority_claims`: assert runtime files do not claim approval, authorization, enforcement, execution, dispatch, persistence, or physical-world authority.

## Fixture And Scanner Requirements

The later implementation may use stdlib-only static text inspection against an explicitly listed file set. It must not introduce a reusable production scanner, runtime imports, dynamic import execution, subprocess use, network access, filesystem mutation outside normal test reads, or broad repository crawling that hides the intended scope.

## Readiness Decision

The Phase 14.1 static designs are ready to be proposed for a later test-only implementation lane, but they are not implemented in Phase 15.1.
