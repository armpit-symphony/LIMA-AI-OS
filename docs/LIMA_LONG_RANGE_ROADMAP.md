# LIMA Long Range Roadmap

This file captures the long-range direction for LIMA-AI-OS so future Codex threads can keep moving without relying on old conversation memory.

Read `docs/CURRENT_PROJECT_STATE.md` first for the current branch, phase, merge/tag status, and immediate next step. This file explains where the work is going after the current phase.

## North Star

LIMA-AI-OS is SparkPit Labs' trust-governed natural-language operating runtime/kernel.

The goal is a human-controlled OS layer that can harness any AI model and safely coordinate:

- assistant bots
- office-worker bots
- business automation bots
- software tools and computers
- IoT devices
- drones
- robots
- future humanoid robots

LIMA is the kernel/runtime. Product shells and consumers sit on top of it.

## Product Family

Sparkbot is the open-source hobby/R&D shell and public reference model. It may help prove the ecosystem and drive interest in commercial SparkPit Labs products, but it is not the kernel.

LIMA AI Office is the intended commercial office-worker direction. ARC Bot and future office-worker bots are shells or consumers on top of LIMA-AI-OS, not Phase 3 implementation work.

Custom business/private-sector bots are future client-specific shells built on LIMA-AI-OS. They are doctrine only until a future approved product phase.

Robo/automation systems are future deterministic driver-plane consumers. Robot, drone, IoT, and humanoid control remains blocked until explicit future approval.

Guardian services are the trust, policy, approval, audit, and governance layer that make LIMA usable for real automation.

## Architecture Posture

LIMA Runtime is the kernel.

Guardian is the syscall gate.

Every external action, tool execution, privileged operation, model call, file/network/browser action, robot action, physical-world action, approval-requiring action, and future business automation action must pass through Guardian.

Sparkbot is the spec and reference source, but extraction must be deliberate:

- contracts first
- fixtures second
- tests third
- safety gates before runtime
- extract, do not rewrite
- reference Sparkbot before copying behavior
- never preserve unsafe shortcuts as kernel primitives

## Phase 3 Direction

Phase 3 is the non-production kernel pipeline phase.

Phase 3 must continue to keep runtime behavior blocked unless an explicit future task changes scope. The safe path is:

1. Static report/map artifact.
2. Pipeline composition safety gate docs.
3. Readiness review for any test-only composition harness.
4. Only then consider a test-only composition harness.
5. Do not move to production runtime composition from Phase 3 without a separate explicit approval phase.

Current expected sequence:

- Phase 3.6 - Non-production Kernel Pipeline Report/Map Artifact: complete/tagged.
- Phase 3.7 - Pipeline Composition Safety Gate Docs: complete/tagged.
- Phase 3.8 - Pipeline Composition Safety Gate Readiness Review: complete/tagged.
- Phase 3.9 - Final Readiness Review: complete/tagged.
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
- Phase 5.0 - Phase 5 Scope Charter / HumanInput IntentEnvelope Boundary Decision Record: complete/tagged.
- Phase 5.1 - HumanInput to IntentEnvelope Contract Proposal: complete/tagged.
- Phase 5.2 - Test-only Bridge Harness Proposal: complete/tagged.
- Phase 5.3 - Test-only Bridge Harness Readiness Review: in progress.
- Phase 4.16 - HumanInput Boundary Lane Closeout Review: approved next.

The exact numbering may change if a readiness review finds gaps. Do not skip safety gate docs or readiness reviews.

## Phase 4 Direction

Phase 4 is the runtime extraction readiness phase.

The first safe Phase 4 sequence is:

- Phase 4.0 - Runtime Extraction Readiness Planning.
- Phase 4.1 - Sparkbot Runtime Reference Refresh.
- Phase 4.2 - Runtime Boundary Candidate Selection.
- Phase 4.3 - Boundary Extraction Safety Gate.
- Phase 4.4 - Boundary Fixture Contract Extension, if approved.
- Phase 4.5 - Boundary Readiness Review.
- Phase 4.6 - Non-production HumanInput Adapter Proposal, explicitly approved as docs/tests/fixtures only.
- Phase 4.7 - Non-production HumanInput Adapter Proposal Readiness Review.
- Phase 4.8 - HumanInput Adapter Safety Gate Docs, if Phase 4.7 lands cleanly.
- Phase 4.9 - HumanInput Adapter Implementation Readiness Review, explicitly approved as docs/tests/fixtures only.
- Phase 4.10 - Non-production Test-only HumanInput Adapter Harness Proposal.
- Phase 4.11 - Test-only HumanInput Adapter Harness Proposal Readiness Review.
- Phase 4.12 - Test-only HumanInput Adapter Harness Safety Gate Docs.
- Phase 4.13 - Phase 4 HumanInput Boundary Readiness Review.
- Explicitly approved narrow non-production extraction or adapter work only after readiness gates.

Phase 4 must not move behavior until a readiness review approves the specific boundary and scope.

Phase 4.1 reference refresh recommends HumanInput intake for chat and voice as the first candidate to evaluate in Phase 4.2, because it can stay non-executing while preserving Sparkbot text/voice convergence as reference material. Terminal/PTY, robotics, broad tool dispatcher, real Guardian enforcement, dashboard approval execution, and product shell work remain deferred.

Phase 4.2 selects HumanInput intake for chat and voice as the first boundary candidate, but only for a Phase 4.3 safety gate. It does not approve adapter implementation or runtime extraction.

Phase 4.3 defines that safety gate and allows only a future Phase 4.4 fixture/contract extension if explicitly approved. Runtime extraction, Sparkbot wiring, live auth/session lookup, model calls, tool execution, terminal/PTY, robotics, and product shells remain blocked.

Phase 4.4 adds synthetic HumanInput intake fixture/contract metadata for text and voice only. It does not approve adapters or runtime extraction. Phase 4.5 should review whether the boundary is ready for a later narrow non-production extraction or adapter proposal, and should keep behavior blocked unless a future explicit phase approves it.

Phase 4.5 reviews the HumanInput intake boundary as conditionally ready only for a future explicitly approved narrow non-production proposal. It does not approve runtime extraction, live Sparkbot integration, live adapter code, model/tool/terminal/robotics behavior, approval/enforcement/execution/audit persistence, product shells, or physical-world action.

Phase 4.6 is that narrow proposal only. It describes how a future shell intake adapter could convert selected shell input context into the Phase 4.4 HumanInput fixture/contract shape, but it is not an adapter, not executable, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

Phase 4.7 reviews the proposal as ready only for future HumanInput Adapter Safety Gate Docs. It does not approve live adapter code, Sparkbot wiring, runtime behavior, real IntentCompiler, real GuardianDecision, approval, enforcement, execution, audit persistence, product shells, or physical-world action.

Phase 4.8 defined the HumanInput adapter safety gate as docs/tests/fixtures only. It requires any future adapter to return HumanInput only and keeps live adapter code, Sparkbot imports/wiring, runtime behavior, live trust/session/auth lookup, real IntentCompiler, real GuardianDecision, approval, enforcement, execution, audit persistence, model/tool/terminal/robot behavior, and physical-world action blocked.

After Phase 4.8, stop for explicit operator approval before any next narrow non-production phase.

Phase 4.9 reviewed whether the boundary is ready for a future explicitly approved test-only HumanInput adapter harness proposal. That readiness is not readiness for runtime adapter implementation, live Sparkbot integration, production wiring, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.10 through Phase 4.13 are approved as docs/tests/fixtures-only queue work. They may propose, review, gate, and summarize a future test-only harness lane, but must not implement harness code, adapter code, runtime behavior, Sparkbot wiring, model/tool/terminal/robot behavior, live lookup, approval, enforcement, execution, audit persistence, or physical-world action.

Phase 4.11 reviews the Phase 4.10 proposal as ready only for Phase 4.12 safety gate docs.

Phase 4.12 defines the safety gate for any future test-only HumanInput adapter harness and preserves that test-only harness work cannot imply production adapter readiness.

Phase 4.13 is complete and tagged. It is the final approved HumanInput boundary readiness review for this Phase 4 queue. It decides readiness only for a future explicitly approved test-only harness implementation phase or further non-runtime review, not runtime adapter implementation.

Phase 4.14 is complete and tagged. It is the first explicitly approved test-only harness implementation phase and stays under `tests/`, remains deterministic and synthetic-only, and does not move runtime behavior into `lima/`.

Phase 4.15 is complete and tagged. It reviews the harness implementation as ready only for Phase 4.16 lane closeout review or further non-runtime review, not runtime adapter work.

Phase 4.16 is complete and tagged. It closes the HumanInput boundary lane and recommends a future explicitly approved HumanInput to IntentEnvelope boundary planning lane. It does not approve next-lane implementation.

Phase 4.17 is complete and tagged. It opened the HumanInput to IntentEnvelope lane as planning only and stayed aligned with the standing IntentEnvelope safety gate.

Phase 4.18 is complete and tagged. It proposes static boundary metadata only and does not create IntentEnvelope records, implement bridge code, or start real IntentCompiler behavior.

Phase 4.19 is complete and tagged. It reviewed the Phase 4.18 schema/contract proposal as non-runtime readiness metadata before a Phase 5 gate / implementation readiness closeout.

Phase 4.20 is complete and tagged. It confirms the Phase 5 gate is reached and stops at operator decisions for any Phase 5 runtime, test-only bridge, or implementation scope.

Phase 5 is not pre-approved. The next step is an explicit operator scope decision.

Phase 5.0 is complete and tagged. It records the approved Phase 5 scope and keeps implementation, bridge code, runtime wiring, live adapter code, real IntentCompiler, real GuardianDecision, approval enforcement, execution, audit persistence, and physical-world action blocked.

Phase 5.1 is complete and tagged as a static HumanInput to IntentEnvelope contract proposal only.

Phase 5.2 is complete and tagged. It proposes a future test-only bridge harness only and does not add bridge code.

Phase 5.3 is the expected readiness review before any implementation gate. It must not add bridge code.

Phase 5.3 is in progress as docs/tests/fixtures-only readiness review work. It should stop at the implementation gate.

After Phase 4.16, stop for explicit operator approval before any next lane, runtime extraction, live adapter, Sparkbot integration, product shell, approval/enforcement/execution/audit, model/tool/terminal/robot, live lookup, or physical-world phase.

## Standing Phase 3 Boundaries

Unless explicitly approved, Phase 3 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- production Sparkbot integration
- Sparkbot imports or wiring
- live routes
- model calls
- tool execution
- terminal or PTY execution
- real IntentCompiler
- real GuardianDecision
- adaptive trust enforcement
- approval enforcement
- policy enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

## Operator Decisions Needed To Avoid Stops

Future Codex threads can proceed through docs/tests/fixtures-only Phase 3 work without stopping if these standing decisions are accepted:

1. Branches may be created and pushed for the next documented Phase 3 micro-step.
2. `docs/CURRENT_PROJECT_STATE.md` must be updated on every phase branch.
3. `docs/LIMA_LONG_RANGE_ROADMAP.md` may be updated when product direction or phase sequencing changes.
4. Validation must run before every push.
5. Full test validation is expected unless the operator explicitly narrows scope.
6. Merge and tag still require explicit operator approval.
7. Any runtime behavior requires explicit operator approval.
8. Any Sparkbot import, wiring, or code copy requires explicit operator approval.
9. Any LIMA AI Office, ARC Bot, custom bot, robot, drone, IoT, approval, execution, or audit persistence implementation requires explicit operator approval.
10. Local Sparkbot may be inspected for reference only when useful, but it must be treated as dirty prototype code unless a future task says otherwise.

## Validation Policy

Use `python3` if available. If `python3` or `python3.exe` is unavailable but `python` resolves to Python 3.x, use `python` and report the exact version.

Default validation:

- `python3 --version || python --version`
- `python3 -m compileall lima || python -m compileall lima`
- `python3 -m pytest -q || python -m pytest -q`
- `git diff --check`
- `git diff --cached --check` before commit when files are staged

For JSON fixtures, also run:

- `python3 -m json.tool <fixture> || python -m json.tool <fixture>`

## Merge And Tag Policy

Do not merge or tag without explicit operator approval.

Routine implementation threads may:

- create branches
- update docs/tests/fixtures inside approved boundaries
- validate
- commit
- push
- provide PR links

They must stop before:

- merging to `main`
- tagging milestones
- crossing into runtime behavior
- wiring Sparkbot
- implementing product shells
- enabling physical-world action

## Long Range Product Path

The long-range product path is:

1. Finish non-production kernel pipeline safety work.
2. Prove test-only composition safely, if approved.
3. Define Phase 4 runtime extraction readiness before moving behavior.
4. Put Sparkbot on LIMA Runtime only after parity and Guardian boundaries are ready.
5. Build LIMA AI Office / ARC Bot as commercial shells after runtime safety foundations exist.
6. Add custom business/private-sector bot generation only after shell boundaries, tenant boundaries, approval policies, and audit surfaces are defined.
7. Add robot, drone, IoT, and humanoid consumers only after deterministic driver-plane contracts, simulation/dry-run policy, physical safety gates, and emergency-stop doctrine are complete.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
