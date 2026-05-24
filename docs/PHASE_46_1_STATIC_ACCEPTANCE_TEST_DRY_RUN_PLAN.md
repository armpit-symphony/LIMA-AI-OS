# Phase 46.1 Static Acceptance-Test Dry-Run Plan

Phase 46.1 opens a docs/tests/fixtures-only static dry-run plan lane for future typed bridge acceptance-test implementation planning.

This phase does not implement runtime bridge behavior. This phase does not create a runtime test harness. This phase does not add actual or executable runtime bridge acceptance tests. This phase does not modify `lima/` or `tests/support/` behavior.

## Mission

Use the Phase 46.0 static implementation-plan template to simulate a future typed bridge acceptance-test implementation phase as metadata only and validate the plan shape before any implementation.

## Dry-Run Objective

- simulate a future typed bridge acceptance-test implementation plan
- validate the plan shape before any test implementation
- keep all work metadata-only

## Dry-Run Inputs

- Phase 45.0 acceptance-test families
- Phase 45.1 fixture matrix rows
- Phase 45.2 readiness outcomes
- Phase 45.3 archive closeout
- Phase 46.0 static implementation-plan template

## Dry-Run Case Catalog

Phase 46.1 dry-run cases are metadata-only and describe what would be checked in a future separately approved implementation phase.

- `source_request_metadata_shape_dry_run`
- `typed_intentenvelope_candidate_shape_dry_run`
- `guardian_request_metadata_shape_dry_run`
- `guardian_decision_boundary_dry_run`
- `positive_non_authoritative_shape_dry_run`
- `approval_bypass_fail_closed_dry_run`
- `forged_guardian_decision_fail_closed_dry_run`
- `missing_actor_tenant_lineage_fail_closed_dry_run`
- `background_dispatch_fail_closed_dry_run`
- `adapter_external_call_fail_closed_dry_run`
- `model_tool_driver_call_fail_closed_dry_run`
- `robotics_physical_world_fail_closed_dry_run`
- `runtime_support_boundary_path_dry_run`

Each case records:

- `dry_run_case_id`
- `source_phase_reference`
- `future_test_family`
- `future_candidate_files`
- `forbidden_files`
- `expected_checks`
- `stop_conditions`
- `rollback_requirements`
- `expected_result`
- `boundary_flags`

## Future Candidate Files (Candidate-Only)

These paths are candidate patterns for a future separately approved phase. They are not created in Phase 46.1:

- `tests/test_typed_bridge_acceptance_*.py`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_*.json`
- `docs/PHASE_46_X_TYPED_BRIDGE_ACCEPTANCE_TEST_*.md`
- README/current-state/roadmap/decision/extraction-plan updates

## Forbidden Files and Surfaces

The dry-run keeps these forbidden surfaces blocked:

- `lima/`
- `tests/support/`
- Sparkbot files
- adapter or driver directories
- persistence/runtime/execution paths
- shell/browser/network/file mutation paths
- robotics/hardware/physical-world paths

## Stop Conditions

The dry-run must stop and report if any of the following are detected:

- any `lima/` change
- any `tests/support/` change
- runtime test harness creation
- executable runtime bridge acceptance tests
- actual acceptance-test harness behavior
- GuardianDecision creation
- approval enforcement
- execution, dispatch, or persistence behavior
- external/model/tool/driver calls
- robotics/physical-world behavior
- failed validation
- unclear approval boundary

## Rollback Requirements

- stop immediately on forbidden scope
- revert or isolate unapproved paths before further phase work
- keep merge/tag blocked until independent audit and Phil approval
- report failure mode and updated boundary risk summary

## Boundary Result

Phase 46.1 boundary flags remain fail-closed:

- docs/tests/fixtures-only true
- static dry-run only true
- runtime test harness created false
- actual acceptance tests created false
- executable acceptance tests created false
- acceptance-test harness behavior added false
- runtime implementation recommended false
- next runtime implementation approved false
- execution/dispatch/persistence/call/robotics/physical-world flags false

## Recommended Next Lane

Phase 46.2 should remain docs/tests/fixtures-only and focus on static dry-run readiness review or archive closeout.

Runtime implementation remains blocked unless Phil explicitly approves a separate runtime design/audit gate.
