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
- Phase 4.3 - Boundary Extraction Safety Gate: next.

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
- Explicitly approved narrow non-production extraction or adapter work only after readiness gates.

Phase 4 must not move behavior until a readiness review approves the specific boundary and scope.

Phase 4.1 reference refresh recommends HumanInput intake for chat and voice as the first candidate to evaluate in Phase 4.2, because it can stay non-executing while preserving Sparkbot text/voice convergence as reference material. Terminal/PTY, robotics, broad tool dispatcher, real Guardian enforcement, dashboard approval execution, and product shell work remain deferred.

Phase 4.2 selects HumanInput intake for chat and voice as the first boundary candidate, but only for a Phase 4.3 safety gate. It does not approve adapter implementation or runtime extraction.

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
