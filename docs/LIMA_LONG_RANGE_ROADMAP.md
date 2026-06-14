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
- Phase 5.3 - Test-only Bridge Harness Readiness Review: complete/tagged.
- Phase 5.4 - Test-only HumanInput to IntentEnvelope Bridge Harness Implementation: complete/tagged.
- Phase 5.5 - Test-only Bridge Harness Readiness Review: complete/tagged.
- Phase 5.6 - HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record: complete/tagged.
- Phase 5.7 - HumanInput Runtime Bridge Design Proposal: complete/tagged.
- Phase 5.8 - HumanInput Runtime Bridge Threat Model: complete/tagged.
- Phase 5.9 - HumanInput Runtime Bridge Boundary Validation Matrix: complete/tagged.
- Phase 5.10 - Runtime Bridge Implementation Gate / Closeout Review: complete/tagged.
- Phase 5.11 - Phase 5 HumanInput Bridge Design Lane Audit Archive / Closeout: complete/tagged.
- Phase 6.0 - Post-Phase-5 Roadmap Reorientation: complete/tagged.
- Phase 6.1 - LIMA Kernel Lifecycle Planning: complete/tagged.
- Phase 6.2 - IntentEnvelope and GuardianDecision Lifecycle Boundary Map: complete/tagged.
- Phase 6.3 - Approval / Audit / Memory Boundary Planning: complete/tagged.
- Phase 6.4 - Phase 6 Roadmap Gate / Next-Lane Closeout: complete/tagged.
- Phase 6.5 - Phase 6 Roadmap Planning Lane Audit Archive / Closeout: complete/tagged.
- Phase 7.0 - Kernel Runtime Implementation Charter: complete/tagged.
- Phase 7.1 - First Runtime Slice Eligibility Map: complete/tagged.
- Phase 7.2 - Kernel Runtime Safety Preconditions: complete/tagged.
- Phase 7.3 - Runtime Implementation Test Plan: complete/tagged.
- Phase 7.4 - Phase 7 Implementation Decision Gate / Closeout: complete/tagged.
- Phase 7.5 - Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout: complete/tagged.
- Phase 8.0 - Implementation Design Review Charter: complete/tagged.
- Phase 8.1 - Exact Runtime File-Touch Map: complete/tagged.
- Phase 8.2 - Runtime Acceptance Test Design: complete/tagged.
- Phase 8.3 - Rollback / Audit Proof Plan: complete/tagged.
- Phase 8.4 - Runtime Implementation Approval Gate / Closeout: complete/tagged.
- Phase 8.5 - Phase 8 No-Code Implementation Design Review Audit Archive / Closeout: complete/tagged.
- Next phase: explicit operator runtime implementation decision required.

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

Phase 5.3 is complete and tagged as docs/tests/fixtures-only readiness review work. It stops at the implementation gate.

Phase 5.4 is complete and tagged. It adds deterministic test-only bridge helper code under `tests/support/` only and keeps live runtime implementation blocked.

Phase 5.5 is complete and tagged as docs/tests/fixtures-only readiness review work. It confirms the Phase 5.4 helper remains test-only and must not be reused as runtime classifier logic.

Phase 5.6 is complete and tagged as a docs/tests/fixtures-only safety gate and next-scope decision record. It requires explicit Phil approval and runtime design before any future live/runtime HumanInput to IntentEnvelope bridge work.

Phase 5.7 is complete and tagged as a docs/tests/fixtures-only runtime bridge design proposal. It documents future bridge shape while keeping live/runtime implementation blocked.

Phase 5.8 is complete and tagged as a docs/tests/fixtures-only runtime bridge threat model. It documents future bridge risks and mitigations while keeping live/runtime implementation blocked.

Phase 5.9 is complete and tagged as a docs/tests/fixtures-only runtime bridge boundary validation matrix. It makes future category expectations machine-checkable while keeping live/runtime implementation blocked.

Phase 5.10 is complete and tagged as a docs/tests/fixtures-only implementation gate / closeout review. It closes the current design lane and keeps live/runtime implementation blocked pending explicit operator next-scope approval.

Phase 5.11 is complete and tagged as a docs/tests/fixtures-only audit archive / closeout. It archives Phase 5.0 through Phase 5.10 as planning/specification work and keeps live/runtime implementation blocked pending explicit operator next-scope approval.

Phase 6.0 is complete and tagged as docs/tests/fixtures-only roadmap reorientation. It selects kernel lifecycle planning as the safest next lane after Phase 5.

Phase 6.1 is complete and tagged as docs/tests/fixtures-only LIMA Kernel Lifecycle Planning. It maps shell intake through blocked driver handoff without implementing runtime behavior.

Phase 6.2 is complete and tagged as docs/tests/fixtures-only IntentEnvelope and GuardianDecision Lifecycle Boundary Mapping. It keeps IntentEnvelope candidates non-executable and separates descriptive candidate metadata from future GuardianDecision authority without implementing runtime behavior.

Phase 6.3 is complete and tagged as docs/tests/fixtures-only Approval / Audit / Memory Boundary Planning. It keeps approval states descriptive, audit/spine metadata as lineage planning, and memory references reference-only without adding enforcement, persistence, memory IO, or runtime behavior.

Phase 6.4 is complete and tagged as docs/tests/fixtures-only roadmap gate / next-lane closeout. It closes the current Phase 6 planning lane and requires explicit operator next-scope selection before any Phase 7, runtime bridge, Sparkbot integration, Robo-OS integration, approval/enforcement/execution/audit, memory IO, or physical-world work.

Phase 6.5 is complete and tagged as docs/tests/fixtures-only Phase 6 Roadmap Planning Lane Audit Archive / Closeout. It archives Phase 6.0 through Phase 6.4 as roadmap/planning only and confirms Phase 5 runtime bridge work remains gated. Future runtime work requires new explicit Phil approval.

Phase 7.0 is complete and tagged as a docs/tests/fixtures-only no-code Kernel Runtime Implementation Charter. It defines a possible future non-executing kernel intake-to-candidate coordinator but does not approve runtime implementation or modify `lima/`.

Phase 7.1 is complete and tagged as a docs/tests/fixtures-only First Runtime Slice Eligibility Map. It names future-eligible contract files and forbidden execution surfaces without modifying `lima/` or approving runtime implementation.

Phase 7.2 is complete and tagged as docs/tests/fixtures-only Kernel Runtime Safety Preconditions. It defines required tests, rollback expectations, audit proof, input/output shape constraints, and safety gates before any future runtime code can be approved.

Phase 7.3 is complete and tagged as docs/tests/fixtures-only Runtime Implementation Test Plan. It defines future test families, required negative cases, limited positive cases, and validation commands without implementing runtime behavior.

Phase 7.4 is complete and tagged as docs/tests/fixtures-only Phase 7 Implementation Decision Gate / Closeout. It closes the no-code charter lane and requires explicit operator decision before any Phase 8, runtime implementation, `lima/` changes, helper behavior changes, Sparkbot wiring, live adapters, execution, approval enforcement, audit persistence, or physical-world behavior.

Phase 7.5 is complete and tagged as docs/tests/fixtures-only Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout. It archives Phase 7.0 through Phase 7.4 as no-code charter/planning work, confirms no runtime implementation was approved, and keeps Phase 5 runtime bridge work gated pending explicit operator next-scope approval.

Phase 8.0 is complete and tagged as docs/tests/fixtures-only Implementation Design Review Charter. It opens Phase 8 as no-code implementation design review and identifies the narrowest future runtime slice as a non-executing kernel intake-to-candidate coordinator without approving code.

Phase 8.1 is complete and tagged as docs/tests/fixtures-only Exact Runtime File-Touch Map. It identifies future-eligible contract files and proposed new kernel files for a later explicitly approved first runtime slice without modifying `lima/`.

Phase 8.2 is complete and tagged as docs/tests/fixtures-only Runtime Acceptance Test Design. It defines future required test families, negative cases, limited positive cases, and validation expectations before any runtime implementation can be approved.

Phase 8.3 is complete and tagged as docs/tests/fixtures-only Rollback / Audit Proof Plan. It defines revertibility, forbidden-path review, audit-proof evidence, success criteria, and failure criteria before any runtime code can be approved.

Phase 8.4 is complete and tagged as docs/tests/fixtures-only Runtime Implementation Approval Gate / Closeout. It closes the no-code design lane and asks whether Phil approves a narrow Phase 9 non-executing kernel intake-to-candidate coordinator implementation limited to the Phase 8.1 eligible files and Phase 8.2/8.3 proof obligations.

Phase 8.5 is complete and tagged as docs/tests/fixtures-only Phase 8 No-Code Implementation Design Review Audit Archive / Closeout. It archives Phase 8.0 through Phase 8.4 as no-code design review work, preserves the exact Phase 9 approval question, and keeps runtime implementation blocked pending explicit operator approval.

Phase 9 is complete and archived as the first narrow runtime slice. It added only the approved non-executing kernel intake-to-candidate coordinator runtime files and kept HumanInput bridge behavior, Sparkbot wiring, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 10 is complete and archived as no-code design for the next runtime slice. It did not modify `lima/` or approve implementation.

Phase 11 is complete and archived as a narrow non-executing candidate status normalization and validation runtime slice. It kept the Phase 5 runtime bridge gated and added no execution, approval enforcement, dispatch, persistence, Sparkbot wiring, live adapter, or physical-world behavior.

Phase 12 is complete and tagged as docs/tests/fixtures-only next-direction planning after Phase 11.

Phase 13 is complete and tagged as docs/tests/fixtures-only threat-model-derived test planning.

Phase 14 is complete and tagged as docs/tests/fixtures-only acceptance-gate test design. It converts Phase 13 requirements into future test names and expected assertions, but it does not implement acceptance-gate tests or approve runtime expansion. Phase 15 requires explicit operator approval.

Phase 15 is complete and tagged as docs/tests/fixtures-only acceptance-gate implementation proposal/readiness work. It proposes the future test-only acceptance-gate package but does not implement the actual future tests, add future fixtures, change `lima/`, change `tests/support/`, or approve runtime expansion. Phase 16 requires explicit operator approval.

Phase 16 is complete and tagged as a test-only acceptance-gate implementation lane. It added docs, fixtures, static acceptance tests, runtime contract acceptance tests against existing non-executing APIs, and synthetic threat fixture acceptance tests under `tests/` and `tests/fixtures/runtime_extraction/` only. It did not change `lima/`, did not change `tests/support/`, did not change runtime behavior, did not wire Sparkbot, did not add a HumanInput runtime bridge, did not add a live adapter, and did not add approval enforcement, execution, dispatch, audit persistence, or physical-world behavior. Phase 17 requires explicit operator approval.

Phase 17 is open as a docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision phase. It may review and archive Phase 16 acceptance tests, evaluate remaining safety gaps, and recommend a Phase 18 direction without changing runtime behavior or approving runtime expansion.

Phase 17 is complete and tagged as a docs/tests/fixtures-only acceptance-gate audit/archive lane. It archived Phase 16 acceptance tests as complete and test-only, recorded remaining safety gaps, recommended Phase 18 as test-only regression hardening, and did not change `lima/`, `tests/support/`, runtime behavior, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior.

Phase 18 is open as a test-only regression hardening lane for existing non-executing candidate APIs and acceptance-gate boundaries. It may add tests, docs, and synthetic fixtures only; it must not change `lima/`, `tests/support/`, runtime behavior, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior.

Phase 18 is complete and tagged as a test-only regression hardening lane. It added candidate API regression tests, synthetic acceptance-boundary regression fixtures, forbidden integration regression tests, readiness review metadata, and archive metadata without changing `lima/`, `tests/support/`, runtime behavior, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior.

Phase 19 is open as a docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision phase for the Phase 18 regression hardening package. It may review coverage, identify remaining gaps, and recommend a Phase 20 direction without changing runtime behavior or approving runtime expansion.

Phase 19.4 archives Phase 19 as complete and recommends Phase 20 as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice. Phase 20 remains unapproved until Phil explicitly approves it.

Phase 20 is open as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice. It may compare candidate slice options and define future gates, but it may not modify runtime code or approve implementation.

Phase 20.4 archives Phase 20 as completed no-code design work and recommends Phase 21 as a narrow candidate provenance hardening runtime slice only if Phil explicitly approves it.

Phase 20.5 archives the Phase 20 design lane as no-code work only. Phase 21 remains gated and requires explicit Phil approval before any runtime implementation.

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

## V1 Product Readiness Target

The V1 target is now recorded in `docs/V1_PRODUCT_READINESS_TARGET.md`.

V1 aims to make LIMA-AI-OS usable first by `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`.

The V1 direction allows future scoped implementation of live/actual approval, real `GuardianDecision`, provider/model routing, and shell haptic intent support. Destructive edit/delete behavior must require operator approval in LIMA-AI-OS and shells.

`docs/V1_READINESS_GAP_MATRIX.md` records the current V1 gap order. `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md` accepts Sparkbot_shell commit `36d697bf875a44dbafa41fc841ded86437917627` as source-backed local `thinking` / progress-state evidence only.

`docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md` records the V1-G2 static typed bridge acceptance proof. It proves metadata shape, status mappings, and fail-closed fixture cases only.

`docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md` records the V1-G3 static destructive edit/delete operator-approval contract proof. It proves destructive action classes require operator approval metadata and static approval-bypass claims fail closed.

`docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md` records the V1-G4 static real `GuardianDecision` and live approval path design gate. It proves future decision outcome families, GuardianDecision status mappings, decision-scope requirements, approval-decision dependency, and fail-closed authority cases.

`docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md` records the V1-G5 static provider/model routing contract and acceptance-test design. It proves route families, route metadata, Guardian/shell/tool-pack/secret/budget/privacy/audit gates, fallback inheritance, and fail-closed routing cases.

`docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md` records the V1-G6 static haptic intent metadata contract and shell fixture proof. It proves response-state to haptic-intent mapping, required metadata, forbidden device fields, shell ownership, and fail-closed forged device claims.

`docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md` records the V1-G7 first-shell integration proof closeout. `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` are accepted as static first-shell evidence only; live runtime parity remains unproven.

`docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CONTRACT.md` and `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_THREAT_MODEL.md` record the V1-G8 audit/evidence persistence static contract and threat model. They define durable record family, lineage, query, redaction, shell evidence, and negative-case requirements without implementing persistence.

`docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md` records the V1-G9 product release boundary audit. The audit is complete, but the release boundary is not passed. LIMA remains `CANDIDATE_ONLY`; runtime export cleanup, final API freeze, V1 product readiness, and production readiness remain unapproved.

`docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_GATE.md` records the V1-G10 minimum runtime implementation gate. The gate is complete as docs/tests/fixtures-only evidence. It defines the V1-G11 file-touch map, rollback plan, acceptance-test expectations, and stop conditions, but it does not approve runtime implementation.

`docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md` records the exact V1-G11 operator approval question. `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md` records the valid operator decision choices and required approval wording. The request and decision packet are complete as docs/tests/fixtures-only evidence and are ready for operator decision, but neither approves implementation.

The next smallest safe V1 action is to record one valid operator choice in the V1-G11 operator decision packet. If approved with the exact required wording, the next implementation branch may add only the typed request and GuardianDecision preflight runtime slice limited to the V1-G10/V1-G11 file-touch map. It must remain local, deterministic, non-executing, non-persistent, and fail-closed. It must not add provider/model calls, shell wiring, haptic device behavior, runtime export cleanup, final freeze, browser/file/network/device/robotics behavior, or physical-world behavior.

This roadmap update is product-direction evidence only. It does not approve runtime implementation, shell wiring, provider/model calls, GuardianDecision creation, approval enforcement, persistence, haptic device implementation, file mutation, browser/network behavior, robotics, or physical-world behavior.
