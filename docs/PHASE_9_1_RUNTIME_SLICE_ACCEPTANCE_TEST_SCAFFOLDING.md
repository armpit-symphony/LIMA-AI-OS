# Phase 9.1 Runtime Slice Acceptance Test Scaffolding

Phase 9.1 converts the Phase 8.2 acceptance-test design into concrete Phase 9 scaffolding for the first runtime slice. It is docs/tests/fixtures only and does not modify `lima/`.

This phase does not implement runtime behavior, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement HumanInput runtime bridge behavior, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Acceptance Target

The Phase 9.2 target remains a pure in-process, non-executing kernel intake-to-candidate coordinator. The coordinator must accept only already-normalized synthetic intake metadata and return non-executable candidate metadata.

## Required Phase 9.2 Acceptance Cases

- Low-risk synthetic intake creates a non-executing candidate.
- Unknown intake becomes blocked or needs review.
- Malformed intake is rejected or blocked safely.
- Stale or replayed intake is rejected or blocked.
- Candidate output is always non-executable.
- `execution_allowed` is always false.
- `side_effects_allowed` is always false.
- `approval_state` is never approved.
- Provenance is preserved.
- Shell, browser, network, file mutation, robotics, and physical-world behavior are not reachable.
- Sparkbot imports or wiring do not exist.
- Phase 5 HumanInput runtime bridge remains gated.
- Only Phase 8.1 eligible runtime files are changed.
- Phase 8.3 rollback and audit proof expectations are satisfied.

## Forbidden Runtime Interpretations

The Phase 9.2 coordinator must not parse raw natural language, create a real `IntentEnvelope`, create a real `GuardianDecision`, enforce approval, dispatch tools, execute, persist audit, call models, call network services, call shell/browser surfaces, mutate files, hand off to drivers, wire Sparkbot, or perform robotics or physical-world action.

## Next Step

Phase 9.2 may implement the narrow coordinator only inside the Phase 8.1 eligible runtime file list and only after these acceptance obligations are represented in tests.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
