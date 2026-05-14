# Phase 8.3 Rollback / Audit Proof Plan

Phase 8.3 defines rollback and audit proof requirements that must be satisfied before any future first runtime slice implementation can be approved. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Rollback Requirements For Future Runtime Code

A future runtime implementation must be independently revertible. It must use a narrow branch, touch only the Phase 8.1 eligible files, include no generated churn, and preserve a clean docs/tests-only fallback state.

Rollback proof must include:

- exact file list before merge
- targeted test list
- forbidden-path diff review
- no broad refactor
- no unrelated formatting churn
- no dependency additions
- no migration or data change
- revert command note for the merge commit
- post-revert validation expectation

## Audit Proof Requirements For Future Runtime Code

Audit proof remains test evidence only until audit persistence is separately approved. A future runtime implementation must prove:

- candidate output includes provenance metadata
- candidate output includes non-executable markers
- candidate output includes source boundary metadata
- candidate output includes future Guardian review boundary references
- candidate output includes no approval authority
- candidate output includes no execution authority
- candidate output includes no audit persistence authority
- candidate output includes no driver handoff authority
- negative tests cover all Phase 8.2 blocked cases

## Success Criteria For A Future Runtime Slice

Future implementation success means:

- only Phase 8.1 eligible files were touched
- typed input produces candidate metadata
- candidate metadata is non-executable
- candidate metadata is not approved
- candidate metadata is not execution-ready
- provenance is retained
- future Guardian review boundary is explicit
- all required targeted and full validation passes
- rollback path is documented

## Failure Criteria For A Future Runtime Slice

Future implementation fails and must stop if:

- any forbidden file surface is needed
- raw natural language is parsed
- HumanInput runtime bridge behavior appears
- real IntentEnvelope behavior appears
- real GuardianDecision behavior appears
- approval enforcement appears
- execution or side effects appear
- audit persistence appears
- Sparkbot coupling appears
- shell/browser/network/file mutation/robotics/physical-world behavior appears
- tests fail and the fix requires scope expansion

## Next Step

Phase 8.4 may close the design lane with a runtime implementation approval gate as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
