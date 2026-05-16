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

Phase 9.1 Runtime Slice Acceptance Test Scaffolding is complete, merged to `main`, and tagged. It translates the Phase 8.2 acceptance-test design into concrete static scaffolding for Phase 9.2, while adding no runtime behavior and modifying no `lima/` files.

Phase 9.2 Non-executing Kernel Intake-to-Candidate Coordinator Implementation is complete, merged to `main`, and tagged. It adds the first narrow runtime slice under `lima/kernel/`: a pure in-process coordinator that accepts only already-normalized synthetic intake metadata and returns non-executable candidate metadata. It does not implement HumanInput runtime bridge behavior, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, audit persistence, Sparkbot wiring, live adapters, or side effects.

Phase 9.3 Runtime Slice Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 9.2 coordinator as ready only for Phase 9.4 audit/archive closeout or further non-runtime review, not for runtime expansion.

Phase 9.4 Phase 9 Runtime Slice Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 9.0 through Phase 9.3, preserves the narrow Phase 9 runtime slice as non-executing candidate metadata only, and stops before Phase 10 or any runtime expansion.

Phase 9.5 First Runtime Slice Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 9.0 through Phase 9.4 as the completed first narrow runtime slice, preserves the Phase 8.1 test-update warning, confirms only `lima/kernel/__init__.py` and `lima/kernel/intake_candidate.py` were touched as runtime files, and keeps Phase 10 gated.

Phase 10.0 Post-Phase-9 Runtime Slice Review is complete, merged to `main`, and tagged. It opens Phase 10 as a no-code design lane, reviews what Phase 9 proved and did not prove, does not modify `lima/` or `tests/support/`, and keeps Phase 11 runtime implementation unapproved.

Phase 10.1 Next Runtime Slice Design Options is complete, merged to `main`, and tagged. It evaluates candidate validation, status normalization, lifecycle metadata, intake error taxonomy, provenance hardening, and stopping with no further runtime work, then recommends candidate validation plus status normalization as a future Phase 11 approval candidate only.

Phase 10.2 Exact File-Touch Map for Next Runtime Slice is complete, merged to `main`, and tagged. It maps only `lima/kernel/intake_candidate.py`, `lima/kernel/__init__.py`, and a possible future `lima/kernel/candidate_status.py` as future-eligible for a Phase 11 candidate validation/status normalization slice, while keeping implementation unapproved.

Phase 10.3 Acceptance Test and Rollback Plan is complete, merged to `main`, and tagged. It defines required future acceptance tests, rollback steps, and audit proof for the possible Phase 11 candidate validation/status normalization slice, while keeping implementation unapproved.

Phase 10.4 Phase 10 Runtime Expansion Approval Gate / Closeout is complete, merged to `main`, and tagged. It closes the Phase 10 no-code design lane and preserves the exact Phase 11 approval question for Phil before any runtime expansion.

Phase 10.5 Phase 10 Next Runtime Slice Design Lane Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 10.0 through Phase 10.4 as no-code design only, confirms no `lima/` changes and no `lima/kernel/candidate_status.py`, and keeps Phase 11 gated pending explicit Phil approval.

Phase 11.0 Runtime Slice Preflight Audit / Eligible File Confirmation is complete, merged to `main`, and tagged. It confirms Phase 10.2 clearly lists the only Phase 11 eligible runtime files and adds no runtime behavior.

Phase 11.1 Candidate Status Acceptance Test Scaffolding is complete, merged to `main`, and tagged. It translates Phase 10.3 acceptance obligations into Phase 11.2 and Phase 11.3 test families without modifying runtime files.

Phase 11.2 Candidate Status Normalization Runtime Implementation is complete, merged to `main`, and tagged. It adds pure in-process candidate status normalization under `lima/kernel/candidate_status.py` and safe exports in `lima/kernel/__init__.py`, while keeping execution, approval, dispatch, persistence, HumanInput bridge behavior, Sparkbot wiring, live adapters, IntentCompiler behavior, GuardianDecision behavior, and physical-world behavior absent.

Phase 11.3 Candidate Validation Runtime Implementation is complete, merged to `main`, and tagged. It adds fail-closed candidate validation in `lima/kernel/candidate_status.py` with safe exports in `lima/kernel/__init__.py`, while preserving non-executing behavior and all Phase 11 forbidden boundaries.

Phase 11.4 Runtime Slice Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 11.2 and Phase 11.3 runtime slice as ready only for Phase 11.5 audit/archive closeout, with no `lima/` or `tests/support/` changes and no runtime expansion.

Phase 11.5 Phase 11 Runtime Slice Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 11 as a completed narrow, non-executing runtime slice, confirms the only Phase 11 runtime files touched were `lima/kernel/candidate_status.py` and `lima/kernel/__init__.py`, and keeps Phase 12 gated pending explicit Phil approval.

Phase 12.0 Post-Phase-11 Runtime Slice Review is complete, merged to `main`, and tagged. It opens Phase 12 as a docs/tests/fixtures-only planning lane, reviews the completed Phase 11 candidate status slice, and keeps runtime expansion unapproved.

Phase 12.1 Next Direction Options: Runtime / Sparkbot / Robo-OS / Pause is complete, merged to `main`, and tagged. It compares pause, future runtime design, Sparkbot boundary planning, Robo-OS boundary planning, and threat-model strengthening, then recommends threat-model and safety-gap review before any next lane is selected.

Phase 12.2 Threat Model and Safety Gap Review is complete, merged to `main`, and tagged. It reviews candidate-status, HumanInput bridge, Sparkbot, Robo-OS, operator-bypass, side-effect escalation, audit, and static-test risks, then recommends a next-lane recommendation matrix.

Phase 12.3 Next Lane Recommendation Matrix is complete, merged to `main`, and tagged. It recommends a docs/tests/fixtures-only threat-model-derived test planning lane as the safest next step and defers runtime expansion, Sparkbot wiring, Robo-OS driver behavior, HumanInput runtime bridge behavior, live adapters, execution, dispatch, and persistence.

Phase 12.4 Phase 12 Decision Gate / Closeout is complete, merged to `main`, and tagged. It closes Phase 12 as planning-only, preserves the Phase 13 approval question for a docs/tests/fixtures-only threat-model-derived test planning lane, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, and physical-world behavior blocked.

Phase 13.0 Threat-Derived Test Planning Charter is complete, merged to `main`, and tagged. It opens Phase 13 as a docs/tests/fixtures-only lane to convert Phase 12.2 threats into static, contract, fixture, and future acceptance-test requirements without runtime changes.

Phase 13.1 Static Forbidden-Pattern Test Requirements is complete, merged to `main`, and tagged. It defines future static requirements for forbidden imports, calls, boundary names, and behavior claims, while adding no scanner implementation and no runtime changes.

Phase 13.2 Runtime Contract Test Requirements is complete, merged to `main`, and tagged. It defines future contract-test requirements for non-executing candidate invariants, provenance preservation, malformed/unknown/stale/replayed safety, operator-bypass resistance, and Phase 5 runtime bridge gating.

Phase 13.3 Threat Fixture Matrix is complete, merged to `main`, and tagged. It defines future synthetic fixture families for malformed candidates, unknown statuses, stale/replayed candidates, approval-bypass wording, shell/network/browser/file/robotics attempts, Sparkbot integration attempts, and HumanInput bridge attempts.

Phase 13.4 Future Acceptance Gate / Closeout is complete, merged to `main`, and tagged. It closes Phase 13 as docs/tests/fixtures-only planning, preserves the future acceptance gate requirements, recommends Phase 14 as docs/tests/fixtures-only acceptance-gate test design, and keeps runtime implementation and integration work blocked.

Phase 14.0 Acceptance-Gate Test Design Charter is complete, merged to `main`, and tagged. It opens Phase 14 as docs/tests/fixtures-only acceptance-gate test design and converts Phase 13 requirements into concrete future test-name planning without implementation.

Phase 14.1 Static Forbidden-Pattern Test Design is complete, merged to `main`, and tagged. It designs future static tests for forbidden imports, calls, side-effect patterns, boundary names, and authority claims while adding no scanner implementation and no runtime changes.

Phase 14.2 Runtime Contract Test Design is complete, merged to `main`, and tagged. It designs future runtime contract tests for non-executing candidate invariants, provenance preservation, malformed/unknown/stale/replayed safety, operator-bypass resistance, and Phase 5 runtime bridge gating.

Phase 14.3 Threat Fixture Acceptance Test Design is complete, merged to `main`, and tagged. It designs future fixture-based acceptance tests for malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge attempts.

Phase 14.4 Future Runtime Acceptance Gate / Closeout is complete, merged to `main`, and tagged. It closes Phase 14 as docs/tests/fixtures-only acceptance-gate test design and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 15.0 Acceptance-Gate Implementation Proposal Charter is complete, merged to `main`, and tagged. It opens Phase 15 as docs/tests/fixtures-only proposal/readiness work and does not implement acceptance tests.

Phase 15.1 Future Static Test Implementation Plan is complete, merged to `main`, and tagged. It proposes future static forbidden-pattern test files, names, assertions, and scanner constraints without adding scanners or future acceptance tests.

Phase 15.2 Future Runtime Contract Test Implementation Plan is complete, merged to `main`, and tagged. It proposes future runtime contract acceptance-test files, names, and assertions without adding future acceptance tests or changing runtime behavior.

Phase 15.3 Future Threat Fixture Test Implementation Plan is complete, merged to `main`, and tagged. It proposes future threat fixture acceptance-test files, fixture names, and fixture content requirements without adding those future fixtures or tests.

Phase 15.4 Test-Only Implementation Readiness Gate / Closeout is complete, merged to `main`, and tagged. It closes Phase 15 as docs/tests/fixtures-only proposal/readiness work, marks the Phase 14 designed tests ready only for a later explicitly approved test-only implementation lane, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 16.0 Test-Only Acceptance Implementation Charter is complete, merged to `main`, and tagged. It opens Phase 16 as a test-only acceptance-gate implementation lane and keeps runtime, `lima/`, and `tests/support` changes blocked.

Phase 16.1 Static Forbidden-Pattern Acceptance Tests is complete, merged to `main`, and tagged. It adds static acceptance checks against explicit existing runtime files without adding scanner helpers, changing runtime behavior, or touching `lima/`.

Phase 16.2 Runtime Contract Acceptance Tests is complete, merged to `main`, and tagged. It adds test-only contract acceptance coverage for existing non-executing candidate APIs without modifying runtime code.

Phase 16.3 Threat Fixture Acceptance Tests is complete, merged to `main`, and tagged. It adds synthetic Phase 16 threat fixture cases and fixture-based acceptance tests without live commands, live targets, credentials, private infrastructure, robot instructions, or runtime behavior.

Phase 16.4 Test-Only Acceptance Implementation Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 16.1 through Phase 16.3 acceptance implementation as test-only and ready for archive/closeout.

Phase 16.5 Phase 16 Test-Only Acceptance Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 16 as completed test-only acceptance-gate implementation and keeps Phase 17, runtime expansion, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 17.0 Phase 16 Acceptance Test Audit Charter is complete, merged to `main`, and tagged. It opens Phase 17 as docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision work, audits Phase 16.0 through Phase 16.5, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 17.1 Acceptance Test Coverage Review is complete, merged to `main`, and tagged. It maps the Phase 16 static, contract, and threat fixture acceptance tests to covered gates, records their static/test-only limitations, and confirms they do not approve runtime expansion.

Phase 17.2 Remaining Safety Gap Review is complete, merged to `main`, and tagged. It records remaining blockers before runtime expansion, including exact future file scope, next-slice acceptance tests, rollback/audit proof, approval semantics decisions, and continued Phase 5 HumanInput runtime bridge gating.

Phase 17.3 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It compares Phase 18 options and recommends a test-only regression hardening lane as the safest active next step, while keeping runtime expansion and integration work unapproved.

Phase 17.4 Phase 17 Acceptance-Gate Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 17 as completed docs/tests/fixtures-only acceptance-gate audit/archive work, preserves the Phase 18 approval question, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 18.0 Regression Hardening Charter is complete, merged to `main`, and tagged. It opens Phase 18 as a test-only regression hardening lane for existing non-executing candidate APIs and acceptance-gate boundaries, while keeping runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 18.1 Candidate API Regression Tests is complete, merged to `main`, and tagged. It adds test-only regression coverage for existing non-executing candidate APIs, including non-executable invariants, authority-bearing field invalidation, unknown status blocking, provenance preservation, stale/replayed handling, dangerous wording no-bypass behavior, and raw HumanInput-like payload rejection.

Phase 18.2 Acceptance Boundary Regression Fixtures is complete, merged to `main`, and tagged. It adds synthetic inert acceptance-boundary regression fixtures and fixture tests for approval-bypass wording, shell/browser/network/file/robotics attempts, Sparkbot integration attempts, HumanInput runtime bridge attempts, stale/replayed candidates, malformed candidates, and unknown statuses.

Phase 18.3 Forbidden Integration Regression Tests is complete, merged to `main`, and tagged. It adds test-only static regression checks that existing candidate runtime files do not import or call Sparkbot, HumanInput runtime bridge behavior, live adapters, IntentCompiler, GuardianDecision, subprocess, shell, browser, network, file mutation, persistence, queues, workers, dispatch, approval enforcement, robotics, or physical-world behavior.

Phase 18.4 Regression Hardening Readiness Review is complete, merged to `main`, and tagged. It reviews the Phase 18 regression hardening package as ready for archive/closeout while keeping runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 18.5 Phase 18 Regression Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 18 as completed test-only regression hardening work, preserves the Phase 19 approval question, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 19.0 Phase 18 Regression Hardening Audit Charter is complete, merged to `main`, and tagged. It opens Phase 19 as docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision work, audits Phase 18.0 through Phase 18.5, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 19.1 Regression Coverage Review is complete, merged to `main`, and tagged. It reviews the Phase 18 candidate API, acceptance-boundary fixture, forbidden integration, readiness, and archive coverage as meaningful test-only regression protection while preserving the Phase 20 gate and all runtime boundaries.

Phase 19.2 Remaining Regression Gap Review is complete, merged to `main`, and tagged. It records that Phase 18 coverage is useful but still not runtime monitoring or enforcement, keeps Sparkbot/Robo-OS/HumanInput bridge work separate, and blocks direct runtime expansion before a separately approved next lane.

Phase 19.3 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It evaluates Phase 20 options and recommends a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice while preserving explicit Phil approval and blocking runtime implementation.

Phase 19.4 Phase 19 Regression Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 19 as completed docs/tests/fixtures-only audit/archive work, preserves the exact Phase 20 approval question, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 20.0 Post-Regression Runtime Slice Design Charter is complete, merged to `main`, and tagged. It opens Phase 20 as docs/tests/fixtures-only no-code design for the next narrow runtime slice, lists candidate slice options, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 20.1 Next Runtime Slice Options Review is complete, merged to `main`, and tagged. It compares candidate provenance hardening, lifecycle metadata, replay/staleness marker normalization, error taxonomy, pause/preserve, and Sparkbot boundary planning, and recommends candidate provenance hardening as the single future slice to carry forward without approving implementation.

Phase 20.2 Exact File-Touch Map For Candidate Slice is complete, merged to `main`, and tagged. It maps a future Phase 21 candidate provenance hardening slice to only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`, while keeping `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, `tests/support/`, Sparkbot, live adapter, HumanInput bridge, approval, execution, dispatch, audit persistence, and physical-world surfaces forbidden.

Phase 20.3 Acceptance Test And Rollback Plan is complete, merged to `main`, and tagged. It defines future acceptance tests and rollback/audit proof for candidate provenance hardening while preserving that Phase 21 remains unapproved and no runtime code or future acceptance tests are implemented in Phase 20.

Phase 20.4 Phase 20 Runtime Slice Approval Gate / Closeout is complete, merged to `main`, and tagged. It archives Phase 20 as completed no-code design work and preserves the exact Phase 21 approval question for candidate provenance hardening while keeping Phase 21 unapproved and all runtime expansion blocked.

Phase 20.5 Phase 20 Next Runtime Slice Design Lane Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 20.0 through Phase 20.4 as completed no-code design work, preserves the exact Phase 21 approval question, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior blocked.

Phase 21.0 Runtime Slice Preflight Audit / Eligible File Confirmation is complete, merged to `main`, and tagged. It confirms Phase 20.2 is unambiguous and that only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py` are eligible runtime files for candidate provenance hardening.

Phase 21.1 Candidate Provenance Acceptance Test Scaffolding is complete on branch `phase-21-1-candidate-provenance-acceptance-test-scaffolding` pending merge. It adds deterministic acceptance scaffolding and synthetic fixtures for candidate provenance hardening without modifying runtime files.

Phase 21.2 Candidate Provenance Hardening Runtime Implementation is complete on branch `phase-21-2-candidate-provenance-hardening-runtime-implementation` pending merge. It hardens candidate provenance construction, status normalization, and validation while touching only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`.

Phase 21.3 Candidate Provenance Regression Review is complete on branch `phase-21-3-candidate-provenance-regression-review` pending merge. It reviews the Phase 21.2 runtime slice using docs, fixtures, and tests only, with no runtime changes.

Phase 21.4 Runtime Slice Readiness Review is complete on branch `phase-21-4-runtime-slice-readiness-review` pending merge. It finds the Phase 21 candidate provenance hardening slice ready for archive closeout and keeps Phase 22 gated.

Latest completed phase merge:

`PENDING_PHASE_21_4_MERGE`

Latest tag:

`phase-21.4-runtime-slice-readiness-review`

## Current Next Step

Current operator step:

Continue only inside the approved Phase 21 candidate provenance hardening runtime slice. Phase 21.5 must archive the Phase 21 runtime slice and stop before Phase 22. `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, `tests/support/`, HumanInput runtime bridge behavior, Sparkbot integration, live adapter, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior remain blocked.

Recommended next branch:

phase-21-5-phase-21-runtime-slice-audit-archive-closeout

Latest completed merge:

`PENDING_PHASE_21_4_MERGE`

Recommended PR target:

`main`

Corrected roadmap note: Phase 3.5 was intentionally inserted before returning to the pipeline report/map artifact path, to capture product-family and adaptive-trust doctrine.

Next intended milestone:

Phase 21.5 - Phase 21 Runtime Slice Audit Archive / Closeout.

Phase 21 approval question:

Do you approve Phase 21 as a narrow runtime implementation slice limited to candidate provenance hardening for existing non-executing candidates, touching only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`, requiring the Phase 20.3 acceptance tests and rollback/audit proof, and still forbidding `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world action, external service calls, background workers, queues, daemons, subprocesses, threads, database writes, and hidden side effects?

Phase 20 approval question:

Do you approve Phase 20 as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice, using Phase 18 regression coverage and Phase 19 audit findings as inputs, while still forbidding runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, and physical-world action?

Phase 19 approval question:

Do you approve Phase 19 as a docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision phase that reviews the Phase 18 regression hardening tests before any future runtime expansion, while still forbidding runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, and physical-world action?

Phase 18 approval question:

Do you approve Phase 18 as a test-only regression hardening lane for existing non-executing candidate APIs and acceptance-gate boundaries, limited to tests/docs/fixtures only, while still forbidding runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, and physical-world action?

Phase 17 approval question:

Do you approve Phase 17 as a docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision phase that reviews the Phase 16 acceptance tests before any future runtime expansion, while still forbidding runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, and physical-world action?

Phase 13 approval question:

Do you approve Phase 13 as a docs/tests/fixtures-only threat-model-derived test planning lane that converts the Phase 12.2 threats into static, contract, fixture, and future acceptance-test requirements, while still forbidding runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, and physical-world action?

Phase 12 approval question:

Do you approve a new Phase 12 scope, and if so should it be docs/tests/fixtures-only planning, another narrow non-executing runtime slice, Sparkbot integration boundary planning, Robo-OS / physical-world boundary planning, or a pause to preserve the current state?

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
