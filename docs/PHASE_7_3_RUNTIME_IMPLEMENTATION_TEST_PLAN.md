# Phase 7.3 Runtime Implementation Test Plan

Phase 7.3 defines the test plan required before any future kernel runtime implementation can be approved. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Test Families

A future runtime implementation proposal must define these test families before code:

- Import boundary tests.
- Typed input validation tests.
- Fail-closed missing-field tests.
- Raw natural-language rejection tests.
- Non-executable candidate output tests.
- Approval bypass rejection tests.
- GuardianDecision non-creation tests.
- Sparkbot coupling rejection tests.
- Side-effect rejection tests.
- Rollback and revertability review tests.

## Required Negative Tests

Future runtime tests must prove the implementation rejects or blocks:

- missing typed input
- empty input
- raw chat text without explicit typed metadata
- operator/admin/Phil/trusted approval-bypass wording
- shell command requests
- browser or network requests
- file mutation requests
- model call requests
- Sparkbot import or runtime coupling
- real GuardianDecision creation
- approval enforcement
- audit persistence
- robotics or physical-world requests

## Required Positive Tests

Future runtime tests may only prove:

- typed explicit metadata is accepted
- provenance is preserved
- candidate metadata remains non-executable
- Guardian review boundary references are present
- approval state remains descriptive
- execution and side effects remain disallowed

## Required Validation Commands

Future runtime implementation must run targeted tests for changed files, all Phase 7 gate tests, the full test suite, `python -m compileall lima`, `git diff --check`, and an explicit forbidden-path review.

## Next Gate

Phase 7.4 may close the Phase 7 no-code charter lane with an implementation decision gate as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
