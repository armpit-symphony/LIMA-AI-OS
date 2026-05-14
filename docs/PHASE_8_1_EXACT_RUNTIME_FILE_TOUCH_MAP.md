# Phase 8.1 Exact Runtime File-Touch Map

Phase 8.1 maps the exact future file-touch surface for the narrowest possible runtime slice. It is docs/tests/fixtures only and does not modify any runtime file.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Slice Being Mapped

The only future runtime slice in scope is the non-executing kernel intake-to-candidate coordinator described by Phase 8.0.

It may be considered later only if Phil explicitly approves runtime code. It must remain candidate-metadata-only and must not become a HumanInput runtime bridge, live adapter, IntentCompiler, GuardianDecision, approval engine, execution path, or audit persistence path.

## Future Eligible Existing Files

The following existing files are the only future existing runtime files that may be touched by a later explicitly approved first runtime slice:

- `lima/contracts/boundary.py`
- `lima/contracts/intent.py`
- `lima/contracts/guardian.py`
- `lima/contracts/events.py`
- `lima/contracts/privacy.py`
- `lima/__init__.py`, only if a public export is required

Eligibility here is not approval to modify these files now.

## Future Eligible New Files

The following new files may be proposed only in a later explicitly approved runtime implementation phase:

- `lima/kernel/__init__.py`
- `lima/kernel/intake_candidate.py`

These files do not exist in Phase 8.1 and must not be created by this phase.

## Forbidden File Surfaces

The first future runtime slice must not touch:

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

The first future runtime slice must also not add Sparkbot imports, live adapters, model calls, network calls, shell execution, browser execution, file mutation, approval enforcement, audit persistence, robotics behavior, or physical-world behavior.

## Touch Rules For A Later Approved Runtime Slice

- Only files named in the eligible list may be modified or created.
- Every touched file must have a targeted test before merge.
- Any new public export must stay non-executing.
- Future candidate outputs must be explicitly non-executable.
- Future candidate outputs must not contain approval, enforcement, execution, audit persistence, or driver-handoff authority.
- Any need to touch a forbidden surface stops the implementation and requires Phil approval.

## Next Step

Phase 8.2 may design runtime acceptance tests as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
