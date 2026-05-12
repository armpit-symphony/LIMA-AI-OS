# Current Project State

This file is the first project-state anchor for Codex and operator workflows. Read it before acting on roadmap, extraction-plan, or older thread context.

For long-range product direction, Phase 3 continuation assumptions, and operator decisions that prevent repeated stops, read `docs/LIMA_LONG_RANGE_ROADMAP.md`.

## Current State

Phase 3.5 is complete and tagged on `main`.

Phase 3.6 is complete, merged to `main`, and tagged.

Phase 3.7 is complete, merged to `main`, and tagged.

Phase 3.8 is complete, merged to `main`, and tagged.

Phase 3.9 final readiness review is complete, merged to `main`, and tagged.

Phase 3 is complete as non-runtime kernel pipeline safety work.

Phase 4.0 is in progress on the implementation branch. It is Runtime Extraction Readiness Planning only and must not start runtime implementation, Sparkbot integration, execution, approval, enforcement, audit persistence, product shell implementation, or physical-world action.

Latest completed phase merge:

`3c922b3`

Latest tag:

`phase-3.9-final-readiness-review`

## Current Next Step

Current operator step:

Complete Phase 4.0 Runtime Extraction Readiness Planning, then merge/tag under standing operator approval if validation and boundary checks pass.

Current implementation branch:

`phase-4-0-runtime-extraction-readiness-planning`

Latest completed merge:

`3c922b3`

Recommended PR target:

`main`

Corrected roadmap note: Phase 3.5 was intentionally inserted before returning to the pipeline report/map artifact path, to capture product-family and adaptive-trust doctrine.

Next intended milestone after Phase 4.0 lands:

Phase 4.1 - Sparkbot Runtime Reference Refresh.

## Active Phase 4 Status

- Phase 4.0 - Runtime Extraction Readiness Planning: in progress.

Phase 4.0 is planning only. Phase 4.1 is expected to be read-only Sparkbot reference refresh. Runtime extraction implementation remains blocked.

## Completed Phase 3 Status

- Phase 3.3 - Non-production Kernel Pipeline Relationship Metadata: complete/tagged.
- Phase 3.4 - Relationship Metadata Readiness Review: complete/tagged.
- Phase 3.5 - LIMA Product Family and Adaptive Trust Doctrine: complete/tagged.
- Phase 3.6 - Non-production Kernel Pipeline Report/Map Artifact: complete/tagged.
- Phase 3.7 - Pipeline Composition Safety Gate Docs: complete/tagged.
- Phase 3.8 - Pipeline Composition Safety Gate Readiness Review: complete/tagged.
- Phase 3.9 - Final Readiness Review: complete/tagged.

## Product Direction

LIMA AI OS is the trust-governed operating runtime/kernel that will eventually let AI models safely control software, workflows, tools, computers, automation systems, devices, and future robots.

The operator goal is a natural-language OS that can harness any AI model and govern assistant bots, office-worker bots, automation bots, IoT devices, drones, robots, and future humanoid robots through explicit trust boundaries.

SparkPit Labs product positioning is tracked at `https://sparkpitlabs.com`: governed AI systems, Guardian services, LIMA AI, LIMA Office Suite, Sparkbot, and the longer LIMA AI OS / Robo OS direction.

Sparkbot is the open-source hobby/R&D shell and reference shell/spec source. It is not the kernel. Do not import or wire Sparkbot unless a future explicit phase allows it.

Sparkbot also serves as the public/open-source model that can help prove the ecosystem and drive interest in commercial SparkPit Labs products. There may be a local Sparkbot prototype on the operator's PC; treat it as useful reference material when explicitly needed, but expect dirty prototype code and do not copy or wire it without an approved phase.

LIMA AI Office is the intended commercial office-worker product direction. ARC Bot is a future office-worker shell under LIMA AI / SparkPit Labs. These are doctrine only right now. Do not implement LIMA AI Office or ARC Bot yet.

Custom business/private-sector bots are future client-specific office-worker and automation shells built on LIMA AI OS. They are doctrine only right now. Do not implement bot generation yet.

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
