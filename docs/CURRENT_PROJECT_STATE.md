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

Phase 4.0 is complete, merged to `main`, and tagged.

Phase 4.1 Sparkbot Runtime Reference Refresh is complete, merged to `main`, and tagged. It inspected Sparkbot as read-only reference/spec material without importing, wiring, copying, or moving behavior.

Phase 4.2 Runtime Boundary Candidate Selection is complete, merged to `main`, and tagged. It selects the non-executing HumanInput intake boundary for chat and voice as the first candidate to carry into a safety gate.

Phase 4.3 Boundary Extraction Safety Gate is complete, merged to `main`, and tagged. It defines the safety gate for the selected HumanInput intake boundary.

Phase 4.4 Boundary Fixture Contract Extension is complete, merged to `main`, tagged, and hardened. It adds synthetic HumanInput intake fixture/contract metadata for text and voice while keeping adapters, runtime behavior, live lookup, authority, approval, execution, and production integration blocked.

Phase 4.5 Boundary Readiness Review is complete, merged to `main`, and tagged. It reviews the HumanInput intake boundary as ready only for a future explicitly approved narrow non-production proposal, while keeping runtime extraction and blocked behavior closed.

Phase 4.6 Non-production HumanInput Adapter Proposal is complete, merged to `main`, and tagged. It adds docs/tests/fixtures-only proposal metadata describing how a future shell intake adapter could convert selected shell input context into the Phase 4.4 HumanInput fixture/contract shape.

Phase 4.6 is not a HumanInput adapter. It is not executable, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

Phase 4.7 Non-production HumanInput Adapter Proposal Readiness Review is complete, merged to `main`, and tagged. It adds docs/tests/fixtures-only readiness metadata reviewing whether Phase 4.6 is clear, safe, constrained, and explicitly non-runtime enough before future adapter safety gate docs.

Phase 4.8 HumanInput Adapter Safety Gate Docs is complete, merged to `main`, and tagged. It defines safety gate documentation for any future HumanInput adapter, but does not implement adapter code.

Phase 4.9 HumanInput Adapter Implementation Readiness Review is complete, merged to `main`, and tagged. It reviews readiness for a future explicitly approved test-only adapter harness proposal, but does not implement an adapter or harness.

The next phase is not automatically approved. Any next narrow non-production phase requires explicit operator approval.

Latest completed phase merge:

`a9d18fa8788fb70a0ed0cf131a972e6eb37206a1`

Latest tag:

`phase-4.9-humaninput-adapter-implementation-readiness-review`

## Current Next Step

Current operator step:

Request explicit operator approval for any next narrow non-production phase.

Recommended next branch:

`pending-explicit-approval`

Latest completed merge:

`ad72435909ee09b19ca83a10900cd628b88b6a1d`

Recommended PR target:

`main`

Corrected roadmap note: Phase 3.5 was intentionally inserted before returning to the pipeline report/map artifact path, to capture product-family and adaptive-trust doctrine.

Next intended milestone:

Explicit operator approval for the next narrow non-production phase.

## Active Phase 4 Status

- Phase 4.0 - Runtime Extraction Readiness Planning: complete/tagged.
- Phase 4.1 - Sparkbot Runtime Reference Refresh: complete/tagged.
- Phase 4.2 - Runtime Boundary Candidate Selection: complete/tagged.
- Phase 4.3 - Boundary Extraction Safety Gate: complete/tagged.
- Phase 4.4 - Boundary Fixture Contract Extension: complete/tagged/hardened.
- Phase 4.5 - Boundary Readiness Review: complete/tagged.
- Phase 4.6 - Non-production HumanInput Adapter Proposal: complete/tagged.
- Phase 4.7 - Non-production HumanInput Adapter Proposal Readiness Review: complete/tagged.
- Phase 4.8 - HumanInput Adapter Safety Gate Docs: complete/tagged.
- Phase 4.9 - HumanInput Adapter Implementation Readiness Review: complete/tagged.

Phase 4.5 reviews the non-executing HumanInput intake boundary as conditionally ready only for a future explicitly approved narrow non-production proposal. Runtime extraction implementation remains blocked.

Phase 4.6 was the approved narrow proposal. It remained docs/tests/fixtures only and did not add adapter code, Sparkbot wiring, runtime behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.7 was an approved readiness review only. It remained docs/tests/fixtures only and recommended Phase 4.8 HumanInput Adapter Safety Gate Docs, not live adapter code.

Phase 4.8 defined adapter safety gate docs only. It did not add live adapter code, Sparkbot imports or wiring, runtime behavior, model/tool/terminal/robot behavior, live auth/session/trust lookup, real IntentCompiler, real GuardianDecision, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.9 was a readiness review only. Readiness to discuss a future test-only adapter harness is not readiness for runtime adapter implementation.

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
