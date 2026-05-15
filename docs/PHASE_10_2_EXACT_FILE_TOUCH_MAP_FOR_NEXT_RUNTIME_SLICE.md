# Phase 10.2 Exact File-Touch Map for Next Runtime Slice

Phase 10.2 maps the exact future file-touch surface for a possible Phase 11 candidate validation and status normalization runtime slice. It does not implement that slice.

This phase does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add live adapters, does not implement HumanInput runtime bridge behavior, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future-Eligible Runtime Files

If Phil later approves Phase 11, the only future-eligible runtime files for the proposed candidate validation and status normalization slice are:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/__init__.py`
- `lima/kernel/candidate_status.py`

`lima/kernel/intake_candidate.py` may be touched only to call or expose pure validation/status metadata helpers for already-created candidate objects. It must not create HumanInput bridge behavior, execute, approve, dispatch, persist, or call external services.

`lima/kernel/__init__.py` may be touched only for safe public exports, if needed. Importing `lima.kernel` must remain side-effect-free.

`lima/kernel/candidate_status.py` may be created only if Phase 11 is explicitly approved. It must remain pure, in-process, non-executing, and authority-free.

## Forbidden Runtime Files

Phase 11 must not touch any other runtime file without a separate explicit approval. Forbidden surfaces include:

- `lima/adapters/**`
- `lima/contracts/**`
- `lima/guardian/**`
- `lima/harness/**`
- `lima/io/**`
- `lima/packs/**`
- `lima/persistence/**`
- `lima/services/**`
- `lima/shells/**`
- `lima/spine/**`
- any Sparkbot repo or file
- any `tests/support/` helper

## Required Future Scope Limits

A future Phase 11 implementation, if approved, must remain limited to candidate validation and status normalization. It must:

- preserve `execution_allowed` as false
- preserve `side_effects_allowed` as false
- preserve `approval_state` as never approved
- preserve provenance
- keep unknown, malformed, stale, replayed, or incomplete candidates blocked or not ready
- keep HumanInput runtime bridge behavior gated
- avoid Sparkbot, live adapters, IntentCompiler, GuardianDecision, approval enforcement, execution, dispatch, audit persistence, shell, browser, network, file mutation, robotics, and physical-world behavior

## Next Step

Phase 10.3 should define acceptance tests and rollback/audit proof for the mapped Phase 11 candidate validation and status normalization slice.
