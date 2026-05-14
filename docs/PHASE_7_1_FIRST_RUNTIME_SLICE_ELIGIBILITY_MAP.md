# Phase 7.1 First Runtime Slice Eligibility Map

Phase 7.1 maps which runtime files could be eligible for a later explicitly approved first runtime slice and which files remain forbidden. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Eligible Files

The following files may be considered eligible only in a later explicitly approved runtime implementation phase:

- `lima/contracts/boundary.py`
- `lima/contracts/intent.py`
- `lima/contracts/guardian.py`
- `lima/contracts/events.py`
- `lima/contracts/privacy.py`
- `lima/__init__.py`, only if a public export is required

The following new files may be considered eligible only if a later implementation charter explicitly approves new kernel modules:

- `lima/kernel/__init__.py`
- `lima/kernel/intake_candidate.py`

Eligibility here is not approval to modify these files now.

## Forbidden For The First Slice

The first runtime slice must not modify:

- `lima/adapters/**`
- `lima/guardian/**`
- `lima/harness/**`
- `lima/io/**`
- `lima/packs/**`
- `lima/persistence/**`
- `lima/services/**`
- `lima/shells/**`
- `lima/spine/**`
- `tests/support/**`

The first runtime slice must also not add Sparkbot imports, live adapters, model calls, network calls, shell execution, browser execution, file mutation, approval enforcement, audit persistence, or physical-world behavior.

## Eligibility Rules

- Eligible files are future candidates only.
- Future code must be non-executing and candidate-metadata-only.
- Future code must fail closed on missing typed input.
- Future code must not parse raw natural language.
- Future code must not create a real GuardianDecision.
- Future code must not approve, enforce, execute, persist audit, or hand off to drivers.
- Future code must be covered by targeted tests before approval.

## Next Gate

Phase 7.2 may define kernel runtime safety preconditions as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
