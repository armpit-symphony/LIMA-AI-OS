# Current Project State

This file is the first project-state anchor for Codex and operator workflows. Read it before acting on roadmap, extraction-plan, or older thread context.

## Current State

Phase 3.5 is complete and tagged.

Latest main commit:

`5b0c8586267f6f7bab544634422b4a04d2221d2a`

Latest tag:

`phase-3.5-lima-product-family-adaptive-trust-doctrine`

## Current Next Step

Next intended phase:

Phase 3.6 - Non-production Kernel Pipeline Report/Map Artifact

Next intended branch:

`phase-3-6-nonproduction-kernel-pipeline-report-map-artifact`

Corrected roadmap note: Phase 3.5 was intentionally inserted before returning to the pipeline report/map artifact path, to capture product-family and adaptive-trust doctrine.

After Phase 3.6, the likely next phase is Phase 3.7 - Pipeline Composition Safety Gate Docs.

## Completed Phase 3 Status

- Phase 3.3 - Non-production Kernel Pipeline Relationship Metadata: complete/tagged.
- Phase 3.4 - Relationship Metadata Readiness Review: complete/tagged.
- Phase 3.5 - LIMA Product Family and Adaptive Trust Doctrine: complete/tagged.

## Product Direction

LIMA AI OS is the trust-governed operating runtime/kernel that will eventually let AI models safely control software, workflows, tools, computers, automation systems, devices, and future robots.

Sparkbot is the open-source hobby/R&D shell and reference shell/spec source. It is not the kernel. Do not import or wire Sparkbot unless a future explicit phase allows it.

ARC Bot is a future commercial office-worker shell under LIMA AI / SparkPit Labs. It is doctrine only right now. Do not implement ARC Bot yet.

Custom business/private-sector bots are future client-specific shells built on LIMA AI OS. They are doctrine only right now. Do not implement bot generation yet.

Robo/automation surfaces are future deterministic driver-plane consumers. They are doctrine only right now. Do not implement robot control yet.

Adaptive trust is future UX doctrine. Breakglass becomes a rare emergency/privileged override. Do not implement adaptive trust enforcement yet.

## Standing Blocked Items

The following remain blocked unless explicitly approved in a future task:

- Runtime behavior.
- Executable pipeline.
- Test-only composition harness.
- Production Sparkbot integration.
- Sparkbot imports or wiring.
- ARC implementation.
- Custom bot implementation.
- Robot control.
- Real `IntentCompiler`.
- Real `GuardianDecision`.
- Adaptive trust enforcement.
- Approval.
- Execution.
- Audit persistence.
- Physical-world action.

## Validation Command Policy

Use `python3` if available. If `python3` or `python3.exe` is unavailable but `python` resolves to Python 3.x, use `python` and report the exact version.

Expected validation set for ordinary docs/config guidance changes:

- `python3 --version || python --version`
- `python3 -m compileall lima || python -m compileall lima`
- `python3 -m pytest -q || python -m pytest -q`
- `git diff --check`

## Workflow Policy

Use this sequence unless the operator explicitly directs otherwise:

1. Implement branch.
2. Review branch.
3. Merge/tag only after explicit approval.

Do not merge or tag from a routine implementation thread.
