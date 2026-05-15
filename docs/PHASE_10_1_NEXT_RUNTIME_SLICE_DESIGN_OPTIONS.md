# Phase 10.1 Next Runtime Slice Design Options

Phase 10.1 evaluates the safest possible next runtime slice after the Phase 9 non-executing intake-to-candidate coordinator. It is a no-code design phase only.

This phase does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add live adapters, does not implement HumanInput runtime bridge behavior, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Evaluated Options

### Option A: Candidate Validation

Candidate validation would check that a candidate produced by the Phase 9 coordinator carries required safety fields, provenance, blocked/not-ready state, and denial of execution/side effects.

Status: preferred future runtime slice when paired with status normalization, pending explicit Phase 11 approval.

### Option B: Candidate Status Normalization

Candidate status normalization would constrain candidate lifecycle labels to non-authoritative states such as `proposed`, `needs_review`, and `blocked`. It must never produce `approved`.

Status: preferred future runtime slice when paired with candidate validation, pending explicit Phase 11 approval.

### Option C: Candidate Lifecycle Metadata

Candidate lifecycle metadata would add descriptive state-transition context around candidate creation, review, and rejection.

Status: useful later, but broader than the next safest slice.

### Option D: Intake Error Taxonomy

An intake error taxonomy would describe why malformed, stale, replayed, unknown, or unsupported intake failed closed.

Status: useful as supporting metadata for validation and status normalization.

### Option E: Provenance Hardening

Provenance hardening would add stricter requirements for source, source_channel, lineage refs, and input identity preservation.

Status: important but should remain a requirement of validation rather than a standalone Phase 11 slice.

### Option F: No Further Runtime Work Yet

The repo may stop after Phase 10 and preserve the Phase 9 runtime slice without further runtime implementation.

Status: always safe, but Phase 10 may still prepare a narrow Phase 11 approval question.

## Recommended Future Slice

The recommended Phase 11 approval candidate is a narrow, non-executing candidate validation and status normalization slice. It should:

- validate existing intake-candidate output shape
- normalize candidate status into non-authoritative states only
- preserve provenance
- preserve blocked and not-ready semantics
- keep `execution_allowed` false
- keep `side_effects_allowed` false
- keep `approval_state` never approved
- keep HumanInput runtime bridge behavior gated
- avoid Sparkbot, live adapters, IntentCompiler, GuardianDecision, approval enforcement, execution, dispatch, audit persistence, shell, browser, network, file mutation, robotics, and physical-world behavior

This recommendation is design-only. No Phase 11 runtime implementation is approved.

## Next Step

Phase 10.2 should map the exact future file-touch surface for the recommended validation and status normalization slice without modifying those files.
