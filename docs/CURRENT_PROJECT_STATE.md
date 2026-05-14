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

Phase 4.10 Non-production Test-only HumanInput Adapter Harness Proposal is complete, merged to `main`, and tagged. It describes a future test-only harness proposal as docs/tests/fixtures only, but does not implement harness code.

Phase 4.11 Test-only HumanInput Adapter Harness Proposal Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 4.10 proposal as docs/tests/fixtures only, but does not implement harness code.

Phase 4.12 Test-only HumanInput Adapter Harness Safety Gate Docs is complete, merged to `main`, and tagged. It defines safety gate docs for a future test-only harness, but does not implement harness code.

Phase 4.13 Phase 4 HumanInput Boundary Readiness Review is complete, merged to `main`, and tagged. It summarizes the HumanInput boundary lane as ready only for a future explicitly approved test-only harness implementation phase or further non-runtime review.

The approved Phase 4.10 through Phase 4.13 docs/tests/fixtures-only queue is exhausted.

Phase 4.14 Test-only HumanInput Adapter Harness Implementation is complete, merged to `main`, and tagged. It adds deterministic test-only helper code under `tests/` and does not modify files under `lima/`.

Phase 4.15 Test-only HumanInput Adapter Harness Implementation Readiness Review is complete, merged to `main`, and tagged. It is docs/tests/fixtures only and did not add harness behavior.

Phase 4.16 HumanInput Boundary Lane Closeout Review is complete, merged to `main`, and tagged. It closes the HumanInput boundary lane as ready to stop and proposes the next explicitly approved lane should be HumanInput to IntentEnvelope boundary planning.

The approved Phase 4.14 through Phase 4.16 queue is exhausted.

Phase 4.17 HumanInput to IntentEnvelope Boundary Planning is complete, merged to `main`, and tagged. It is docs/tests/fixtures only and did not add schema implementation, bridge code, real IntentCompiler behavior, or runtime behavior.

Phase 4.18 HumanInput to IntentEnvelope Boundary Schema / Contract Proposal is complete, merged to `main`, and tagged. It proposed static metadata shape and did not implement a bridge, parser, compiler, adapter, or runtime behavior.

Phase 4.19 HumanInput to IntentEnvelope Boundary Readiness Review is complete, merged to `main`, and tagged. It reviewed the Phase 4.18 schema/contract proposal as docs/tests/fixtures-only readiness metadata before a Phase 5 gate / implementation readiness closeout.

Phase 4.20 Phase 5 Gate / Implementation Readiness Closeout is complete, merged to `main`, and tagged. It confirms Phase 5 gate is reached and identifies operator decisions needed before any Phase 5 runtime, test-only bridge, or implementation work.

Phase 5.0 Phase 5 Scope Charter / HumanInput IntentEnvelope Boundary Decision Record is complete, merged to `main`, and tagged. It opens Phase 5 as non-runtime planning only and keeps implementation, bridge code, runtime wiring, live adapter code, real IntentCompiler behavior, real GuardianDecision behavior, approval enforcement, audit persistence, Sparkbot integration, and physical-world action blocked.

Phase 5.1 HumanInput to IntentEnvelope Contract Proposal is complete, merged to `main`, and tagged. It proposes static contract metadata only and does not create IntentEnvelope records, implement bridge code, run IntentCompiler behavior, enforce approvals, execute actions, persist audit, or add runtime wiring.

Phase 5.2 Test-only Bridge Harness Proposal is complete, merged to `main`, and tagged. It proposes a future test-only bridge harness only and does not implement the harness.

Phase 5.3 Test-only Bridge Harness Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 5.2 proposal as ready only for an explicit operator implementation-scope decision and stops at the implementation gate.

Phase 5.4 Test-only HumanInput to IntentEnvelope Bridge Harness Implementation is complete, merged to `main`, and tagged. It adds deterministic test-only helper code under `tests/support/` and does not modify files under `lima/`.

Phase 5.5 Test-only Bridge Harness Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 5.4 helper without changing helper behavior, adding runtime behavior, modifying `lima/`, or approving live implementation.

Phase 5.6 HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record is complete, merged to `main`, and tagged. It defines next-scope options and keeps live/runtime HumanInput to IntentEnvelope implementation blocked.

Phase 5.7 HumanInput Runtime Bridge Design Proposal is complete, merged to `main`, and tagged. It documents future runtime bridge shape without implementation.

Phase 5.8 HumanInput Runtime Bridge Threat Model is complete, merged to `main`, and tagged. It documents future bridge threats and mitigations without implementation.

Phase 5.9 HumanInput Runtime Bridge Boundary Validation Matrix is complete, merged to `main`, and tagged. It documents future bridge boundary categories without implementation.

Phase 5.10 Runtime Bridge Implementation Gate / Closeout Review is complete, merged to `main`, and tagged. It closes the design lane and keeps live/runtime implementation blocked.

Phase 5.11 Phase 5 HumanInput Bridge Design Lane Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 5.0 through Phase 5.10 as planning/specification work.

Phase 6.0 Post-Phase-5 Roadmap Reorientation is complete, merged to `main`, and tagged. It reorients the roadmap toward kernel lifecycle planning after the Phase 5 archive.

Phase 6.1 LIMA Kernel Lifecycle Planning is complete, merged to `main`, and tagged. It maps the kernel lifecycle without implementation.

Phase 6.2 IntentEnvelope and GuardianDecision Lifecycle Boundary Map is complete, merged to `main`, and tagged. It maps the non-executable IntentEnvelope candidate lifecycle and future GuardianDecision authority boundary without implementation.

Phase 6.3 Approval / Audit / Memory Boundary Planning is complete, merged to `main`, and tagged. It maps descriptive approval, audit/spine lineage, and memory reference boundaries without implementation.

Phase 6.4 Phase 6 Roadmap Gate / Next-Lane Closeout is complete, merged to `main`, and tagged. It closes the current Phase 6 planning lane and requires explicit operator next-scope selection before any next phase.

Phase 6.5 Phase 6 Roadmap Planning Lane Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 6.0 through Phase 6.4 as roadmap/planning only and confirms Phase 5 runtime bridge work remains gated.

Phase 7.0 Kernel Runtime Implementation Charter is complete, merged to `main`, and tagged. It opens Phase 7 as a no-code runtime charter lane and defines the smallest future runtime slice without approving implementation.

Phase 7.1 First Runtime Slice Eligibility Map is complete, merged to `main`, and tagged. It maps future eligible contract files and forbidden runtime surfaces without modifying `lima/` or approving implementation.

Phase 7.2 Kernel Runtime Safety Preconditions is complete, merged to `main`, and tagged. It defines required tests, rollback expectations, audit proof, input/output constraints, and safety gates before any future runtime code can be approved.

Phase 7.3 Runtime Implementation Test Plan is complete, merged to `main`, and tagged. It defines future test families, required negative tests, limited positive tests, and validation commands without implementing runtime behavior.

Phase 7.4 Phase 7 Implementation Decision Gate / Closeout is complete, merged to `main`, and tagged. It closes the no-code Phase 7 charter lane and requires explicit operator decision before any runtime code.

Phase 7.5 Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 7.0 through Phase 7.4 as no-code charter/planning work and requires explicit operator next-scope decision before any Phase 8, runtime implementation, `lima/` change, `tests/support/` change, Sparkbot integration, live adapter, approval enforcement, execution, audit persistence, or physical-world behavior.

Phase 8.0 Implementation Design Review Charter is complete, merged to `main`, and tagged. It opens Phase 8 as no-code implementation design review and identifies the narrowest future runtime slice without approving runtime implementation or modifying `lima/`.

Phase 8.1 Exact Runtime File-Touch Map is complete, merged to `main`, and tagged. It maps future-eligible existing contract files, proposed new kernel files, and forbidden runtime surfaces without modifying `lima/` or approving runtime implementation.

Phase 8.2 Runtime Acceptance Test Design is complete, merged to `main`, and tagged. It defines future required test families, negative cases, limited positive cases, and validation expectations before any runtime implementation can be approved.

Phase 8.3 Rollback / Audit Proof Plan is complete, merged to `main`, and tagged. It defines future revertibility, forbidden-path review, audit-proof evidence, success criteria, and failure criteria before any runtime implementation can be approved.

Phase 8.4 Runtime Implementation Approval Gate / Closeout is complete, merged to `main`, and tagged. It closes the no-code Phase 8 design lane and requires explicit operator approval before any Phase 9 runtime implementation or `lima/` change.

Phase 8.5 Phase 8 No-Code Implementation Design Review Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 8.0 through Phase 8.4 as no-code design review work and preserves the exact Phase 9 approval question while keeping runtime implementation blocked.

Phase 9.0 Runtime Slice Preflight Audit / Eligible File Confirmation is complete, merged to `main`, and tagged. It confirms the Phase 8.1 eligible runtime file-touch map is explicit enough for Phase 9.1 acceptance test scaffolding, while adding no runtime behavior and modifying no `lima/` files.

Latest completed phase merge:

`8dd81595ab9ffd503a36556551110fec6605066c`

Latest tag:

`phase-9.0-runtime-slice-preflight-audit-eligible-file-confirmation`

## Current Next Step

Current operator step:

Continue only to Phase 9.1 Runtime Slice Acceptance Test Scaffolding under the approved narrow Phase 9 lane.

Recommended next branch:

`phase-9-1-runtime-slice-acceptance-test-scaffolding`

Latest completed merge:

`8dd81595ab9ffd503a36556551110fec6605066c`

Recommended PR target:

`main`

Corrected roadmap note: Phase 3.5 was intentionally inserted before returning to the pipeline report/map artifact path, to capture product-family and adaptive-trust doctrine.

Next intended milestone:

Explicit operator runtime implementation decision.

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
- Phase 4.10 - Non-production Test-only HumanInput Adapter Harness Proposal: complete/tagged.
- Phase 4.11 - Test-only HumanInput Adapter Harness Proposal Readiness Review: complete/tagged.
- Phase 4.12 - Test-only HumanInput Adapter Harness Safety Gate Docs: complete/tagged.
- Phase 4.13 - Phase 4 HumanInput Boundary Readiness Review: complete/tagged.
- Phase 4.14 - Test-only HumanInput Adapter Harness Implementation: complete/tagged.
- Phase 4.15 - Test-only HumanInput Adapter Harness Implementation Readiness Review: complete/tagged.
- Phase 4.16 - HumanInput Boundary Lane Closeout Review: complete/tagged.
- Phase 4.17 - HumanInput to IntentEnvelope Boundary Planning: complete/tagged.
- Phase 4.18 - HumanInput to IntentEnvelope Boundary Schema / Contract Proposal: complete/tagged.
- Phase 4.19 - HumanInput to IntentEnvelope Boundary Readiness Review: complete/tagged.
- Phase 4.20 - Phase 5 Gate / Implementation Readiness Closeout: complete/tagged.

Phase 4.5 reviews the non-executing HumanInput intake boundary as conditionally ready only for a future explicitly approved narrow non-production proposal. Runtime extraction implementation remains blocked.

Phase 4.6 was the approved narrow proposal. It remained docs/tests/fixtures only and did not add adapter code, Sparkbot wiring, runtime behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.7 was an approved readiness review only. It remained docs/tests/fixtures only and recommended Phase 4.8 HumanInput Adapter Safety Gate Docs, not live adapter code.

Phase 4.8 defined adapter safety gate docs only. It did not add live adapter code, Sparkbot imports or wiring, runtime behavior, model/tool/terminal/robot behavior, live auth/session/trust lookup, real IntentCompiler, real GuardianDecision, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.9 was a readiness review only. Readiness to discuss a future test-only adapter harness is not readiness for runtime adapter implementation.

Phase 4.10 was proposal metadata only. It did not add harness code, adapter code, files under `lima/`, Sparkbot wiring, runtime behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.11 was readiness-review metadata only. It recommended Phase 4.12 safety gate docs, not harness implementation.

Phase 4.12 was safety gate documentation only. It did not add harness code, adapter code, files under `lima/`, Sparkbot wiring, runtime behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.13 was the final approved Phase 4 HumanInput boundary readiness review in the current queue. It summarized known gaps and readiness for a future explicitly approved test-only harness implementation phase or further non-runtime review, but did not implement harness code, adapter code, files under `lima/`, Sparkbot wiring, runtime behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.14 was the approved narrow implementation of a deterministic test-only harness under `tests/`. It validates synthetic fixture shapes and produces HumanInput-shaped test dictionaries only. It did not add runtime code, live adapter code, Sparkbot imports/wiring, real IntentEnvelope or GuardianDecision behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.15 was the approved docs/tests/fixtures-only readiness review of Phase 4.14. It did not add new harness behavior.

Phase 4.16 was the approved docs/tests/fixtures-only closeout review for the HumanInput boundary lane. It did not add new harness behavior or runtime behavior. It recommends the next explicitly approved lane be HumanInput to IntentEnvelope boundary planning.

Phase 4.17 opened that lane as planning only. It aligned the lane with the standing IntentEnvelope safety gate and did not approve bridge code, schema implementation, real IntentCompiler behavior, GuardianDecision behavior, runtime wiring, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.18 HumanInput to IntentEnvelope Boundary Schema / Contract Proposal is complete, merged to `main`, and tagged. It proposed static metadata shape and did not implement a bridge, parser, compiler, adapter, or runtime behavior.

Phase 4.19 HumanInput to IntentEnvelope Boundary Readiness Review is complete, merged to `main`, and tagged. It reviewed the Phase 4.18 schema/contract proposal as docs/tests/fixtures-only readiness metadata before a Phase 5 gate / implementation readiness closeout.

Phase 4.20 Phase 5 Gate / Implementation Readiness Closeout is complete, merged to `main`, and tagged. It confirms Phase 5 gate is reached and identifies operator decisions needed before any Phase 5 runtime, test-only bridge, or implementation work.

Phase 5 is not pre-approved. Before Phase 5 starts, the operator must decide whether Phase 5 begins as further non-runtime planning or as a narrow explicitly approved test-only HumanInput to IntentEnvelope bridge implementation, plus the human UX flow, approval semantics, trust/autonomy handling, safety boundary, and code scope.

Phase 5.0 Phase 5 Scope Charter / HumanInput IntentEnvelope Boundary Decision Record is complete, merged to `main`, and tagged. It opens Phase 5 as non-runtime planning only and records the approved HumanInput to IntentEnvelope boundary scope.

Phase 5.1 HumanInput to IntentEnvelope Contract Proposal is complete, merged to `main`, and tagged. It proposes static contract metadata only.

Phase 5.2 Test-only Bridge Harness Proposal is complete, merged to `main`, and tagged. It proposes a future test-only bridge harness only and does not implement the harness.

Phase 5.3 Test-only Bridge Harness Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 5.2 proposal and stops at an implementation gate.

Phase 5.4 Test-only HumanInput to IntentEnvelope Bridge Harness Implementation is complete, merged to `main`, and tagged. It adds a test-only helper under `tests/support/` that converts synthetic HumanInput-shaped dictionaries into non-executable IntentEnvelope-candidate-shaped test dictionaries only.

Phase 5.5 Test-only Bridge Harness Readiness Review is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 5.6 HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 5.7 HumanInput Runtime Bridge Design Proposal is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 5.8 HumanInput Runtime Bridge Threat Model is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 5.9 HumanInput Runtime Bridge Boundary Validation Matrix is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 5.10 Runtime Bridge Implementation Gate / Closeout Review is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

No next phase is approved. Live/runtime HumanInput to IntentEnvelope implementation remains blocked pending explicit operator next-scope approval.

Phase 5.11 Phase 5 HumanInput Bridge Design Lane Audit Archive / Closeout is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

No next phase is approved. Future runtime work requires new explicit Phil approval.

Phase 6.0 Post-Phase-5 Roadmap Reorientation is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 6.1 LIMA Kernel Lifecycle Planning is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 6.2 IntentEnvelope and GuardianDecision Lifecycle Boundary Map is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 6.3 Approval / Audit / Memory Boundary Planning is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, read or write memory, append a spine ledger, or perform physical-world action.

Phase 6.4 Phase 6 Roadmap Gate / Next-Lane Closeout is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, read or write memory, append a spine ledger, or perform physical-world action.

Phase 6.5 Phase 6 Roadmap Planning Lane Audit Archive / Closeout is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 7.0 Kernel Runtime Implementation Charter is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 7.1 First Runtime Slice Eligibility Map is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 7.2 Kernel Runtime Safety Preconditions is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 7.3 Runtime Implementation Test Plan is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 7.4 Phase 7 Implementation Decision Gate / Closeout is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

Phase 7.5 Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout is complete, merged to `main`, and tagged. It did not change helper behavior, modify `tests/support/`, modify `lima/`, add a live bridge, add a live adapter, wire Sparkbot, implement real IntentCompiler behavior, implement real GuardianDecision behavior, enforce approval, execute, persist audit, or perform physical-world action.

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
