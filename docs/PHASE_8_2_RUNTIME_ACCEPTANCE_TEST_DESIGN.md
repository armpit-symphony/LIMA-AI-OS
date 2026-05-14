# Phase 8.2 Runtime Acceptance Test Design

Phase 8.2 defines the acceptance tests that must exist before any future first runtime slice implementation can be approved. It is docs/tests/fixtures only and does not implement those runtime tests yet.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Test Design Target

The future acceptance tests apply only to a later explicitly approved non-executing kernel intake-to-candidate coordinator.

The future tests must prove that the coordinator accepts only already-typed explicit metadata and returns non-executable candidate metadata. They must also prove that runtime code does not become a HumanInput bridge, IntentCompiler, GuardianDecision, approval engine, execution path, audit persistence path, live adapter, or Sparkbot integration.

## Required Future Test Families

- Import-boundary tests for the exact Phase 8.1 file-touch map.
- Typed-input acceptance tests.
- Missing-field and malformed-input rejection tests.
- Natural-language/raw-chat rejection tests.
- Non-executable candidate output tests.
- Authority-free output tests.
- Approval-bypass wording rejection tests.
- GuardianDecision non-creation tests.
- IntentEnvelope non-creation tests.
- Sparkbot coupling rejection tests.
- Side-effect rejection tests.
- Phase 5 runtime bridge gate preservation tests.
- Rollback and diff-scope review checks.

## Required Negative Cases

Future runtime tests must reject or preserve blocked status for:

- raw natural-language prompts
- shell command requests
- browser or network requests
- file mutation requests
- model-call requests
- tool-call requests
- Sparkbot import or runtime coupling
- real IntentEnvelope creation
- real GuardianDecision creation
- approval enforcement
- execution
- audit persistence
- robotics or physical-world requests
- operator/admin/Phil/trusted bypass wording
- stale or replayed candidate metadata
- malformed provenance

## Limited Positive Cases

Future positive tests may cover only:

- typed synthetic metadata input accepted
- candidate metadata returned
- candidate provenance retained
- candidate risk hints retained as descriptive metadata
- candidate approval hints retained as descriptive metadata
- candidate output marked non-executable
- candidate output marked not approved and not execution-ready
- future Guardian review boundary references retained

## Validation Expectations

A future runtime implementation proposal must include targeted tests for every touched file, all Phase 8 gate tests, full `python -m pytest -q`, `python -m compileall lima`, `git diff --check`, and explicit forbidden-path review.

## Next Step

Phase 8.3 may define rollback and audit proof requirements as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
