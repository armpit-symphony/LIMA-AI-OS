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

Phase 21.5 Phase 21 Runtime Slice Audit Archive / Closeout is complete on branch `phase-21-5-phase-21-runtime-slice-audit-archive-closeout` pending merge. It archives Phase 21 as complete, records the exact runtime files touched, and keeps Phase 22 gated.

Phase 22.0 Post-Phase-21 Runtime Slice Audit Charter is complete on branch `phase-22-0-post-phase-21-runtime-slice-audit-charter` pending merge. It opens the docs/tests/fixtures-only no-code decision lane and records the Phase 21 audit baseline.

Phase 22.1 Candidate Provenance Coverage Review is complete on branch `phase-22-1-candidate-provenance-coverage-review` pending merge. It reviews existing provenance coverage and identifies remaining test-only hardening opportunities without runtime changes.

Phase 22.2 Remaining Safety Gap Review is complete on branch `phase-22-2-remaining-safety-gap-review` pending merge. It finds the remaining gaps are test/planning gaps and recommends test-only hardening before runtime expansion.

Phase 22.3 Next-Lane Decision Matrix is complete on branch `phase-22-3-next-lane-decision-matrix` pending merge. It recommends Phase 23 as test-only hardening for provenance and candidate invariants.

Phase 22.4 Phase 22 Decision Gate / Closeout is complete on branch `phase-22-4-phase-22-decision-gate-closeout` pending merge. It closes Phase 22, preserves the exact Phase 23 approval question, and keeps Phase 23 gated.

Phase 23.0 Provenance Invariant Test Hardening Charter is complete on branch `phase-23-0-provenance-invariant-test-hardening-charter` pending merge. It opens the approved test-only hardening lane for provenance and candidate invariants without runtime changes.

Phase 23.1 Candidate Provenance Regression Tests is complete on branch `phase-23-1-candidate-provenance-regression-tests` pending merge. It adds deterministic tests for valid, missing, malformed, stale, and replayed provenance behavior without runtime changes.

Phase 23.2 Suspicious Provenance Fixture Hardening is complete on branch `phase-23-2-suspicious-provenance-fixture-hardening` pending merge. It adds synthetic suspicious provenance fixtures and tests without runtime changes.

Phase 23.3 Bypass-Wording Provenance Tests is complete, merged to `main`, and tagged. It adds deterministic tests proving Phil/operator/admin/trusted/urgent/override/approve/emergency wording does not bypass non-executing candidate safety.

Phase 23.4 Provenance Hardening Readiness Review is complete, merged to `main`, and tagged. It reviews Phase 23.0 through Phase 23.3 as ready for archive/closeout without runtime changes.

Phase 23.5 Phase 23 Test-Only Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 23 as test-only hardening and preserves Phase 24 as a docs/tests/fixtures-only next-lane decision gate.

Phase 24.0 Phase 23 Hardening Audit Charter is complete, merged to `main`, and tagged. It opens the approved docs/tests/fixtures-only audit/archive and next-lane decision phase for the Phase 23 package.

Phase 24.1 Provenance Hardening Coverage Review is complete, merged to `main`, and tagged. It confirms the Phase 23 provenance and candidate-invariant coverage without runtime changes.

Phase 24.2 Remaining Candidate Invariant Gap Review is complete, merged to `main`, and tagged. It identifies remaining gaps as planning inputs only without runtime changes.

Phase 24.3 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It recommends Phase 25 as additional test-only hardening for a cross-API candidate invariant matrix.

Phase 24.4 Phase 24 Hardening Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 24 and preserves Phase 25 as a gated test-only hardening lane.

Phase 25.0 Cross-API Candidate Invariant Matrix Charter is complete, merged to `main`, and tagged. It opens the approved test-only hardening lane without runtime changes.

Phase 25.1 Candidate API Matrix Fixtures is complete, merged to `main`, and tagged. It adds synthetic matrix fixtures without runtime changes.

Phase 25.2 Cross-API Non-Execution Invariant Tests is complete, merged to `main`, and tagged. It adds deterministic tests proving existing candidate-facing APIs preserve non-execution invariants without runtime changes.

Phase 25.3 Cross-API Provenance and Status Invariant Tests is complete, merged to `main`, and tagged. It adds deterministic tests for provenance and status invariants without runtime changes.

Phase 25.4 Cross-API Boundary Readiness Review is complete, merged to `main`, and tagged. It reviews Phase 25.0 through Phase 25.3 as ready for archive/closeout without runtime changes.

Phase 25.5 Phase 25 Test-Only Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 25 and preserves Phase 26 as a gated docs/tests/fixtures-only audit/archive decision lane.

Phase 26.0 Phase 25 Cross-API Invariant Audit Charter is complete, merged to `main`, and tagged. It opens the approved docs/tests/fixtures-only audit/archive and next-lane decision lane without runtime changes.

Phase 26.1 Cross-API Invariant Coverage Review is complete, merged to `main`, and tagged. It confirms Phase 25 coverage across existing candidate-facing APIs without runtime changes.

Phase 26.2 Remaining Cross-API Gap Review is complete, merged to `main`, and tagged. It records remaining cross-API candidate invariant gaps as planning inputs only without runtime changes.

Phase 26.3 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It recommends Phase 27 as a docs/tests/fixtures-only preservation and roadmap decision lane without runtime changes.

Phase 26.4 Phase 26 Cross-API Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 26 and preserves Phase 27 as a gated docs/tests/fixtures-only preservation and roadmap decision lane.

Phase 27.0 Phase 26 Preservation Audit Charter is complete, merged to `main`, and tagged. It opens the approved docs/tests/fixtures-only preservation and roadmap decision lane without runtime changes.

Phase 27.1 Current Runtime/Test State Preservation Record is complete, merged to `main`, and tagged. It preserves the current known-good runtime/test state without runtime changes.

Phase 27.2 Gated Runtime Boundary Review is complete, merged to `main`, and tagged. It reviews the blocked runtime and integration boundaries without runtime changes.

Phase 27.3 Next-Lane Risk Decision Matrix is complete, merged to `main`, and tagged. It recommends Phase 28 as a docs/tests/fixtures-only preservation status review without runtime changes.

Phase 27.4 Phase 27 Preservation Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 27 and preserves Phase 28 as a gated docs/tests/fixtures-only preservation status review.

Phase 28.0 Phase 27 Preservation Status Audit Charter is complete, merged to `main`, and tagged. It opens the preservation status review and requires a sharper Phase 29 decision gate without runtime changes.

Phase 28.1 Stable Runtime/Test State Review is complete, merged to `main`, and tagged. It confirms the current runtime/test state remains stable and preserved without runtime changes.

Phase 28.2 Preservation Pause Justification Review is complete, merged to `main`, and tagged. It recommends Phase 29 as a docs/tests/fixtures-only no-code design review rather than another automatic preservation pause.

Phase 28.3 Phase 29 Decision Readiness Matrix is complete, merged to `main`, and tagged. It recommends Phase 29 as a docs/tests/fixtures-only no-code design review for the next narrow runtime slice.

Phase 28.4 Phase 28 Preservation Status Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 28 and preserves Phase 29 as a gated docs/tests/fixtures-only no-code design review.

Phase 29.0 Phase 28 No-Code Design Review Audit Charter is complete, merged to `main`, and tagged. It opens the approved no-code design review lane without runtime changes.

Phase 29.1 Narrow Runtime Slice Candidate Inventory is complete, merged to `main`, and tagged. It recommends a future read-only runtime state inspection slice for detailed no-code boundary design.

Phase 29.2 Runtime Slice Safety Boundary Design is complete, merged to `main`, and tagged. It defines the future read-only runtime state inspection boundary without runtime changes.

Phase 29.3 Future Implementation Eligibility Matrix is complete, merged to `main`, and tagged. It defines the future eligibility criteria, acceptance-test expectations, rollback/audit proof, and Phase 30 approval question for read-only runtime state inspection without runtime changes.

Phase 29.4 Phase 29 No-Code Design Review Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 29 as no-code design review only and keeps Phase 30 blocked pending explicit Phil approval.

Phase 30.0 Phase 29 Runtime Implementation Audit Charter is complete, merged to `main`, and tagged. It audits Phase 29 and confirms the approved Phase 30 read-only runtime state inspection scope before runtime files are touched.

Phase 30.1 Read-Only Runtime State Inspection Acceptance Design is complete, merged to `main`, and tagged. It defines acceptance and regression coverage for the approved read-only runtime state inspection slice before implementation.

Phase 30.2 Read-Only Runtime State Inspection Implementation is complete, merged to `main`, and tagged. It adds `lima/kernel/runtime_state.py` plus a safe `lima/kernel/__init__.py` export for deterministic, local-only, read-only, non-authoritative runtime state inspection.

Phase 30.3 Runtime State Inspection Boundary Regression Review is complete, merged to `main`, and tagged. It reviews the Phase 30.2 slice and confirms it remains inside the approved read-only, non-authoritative, non-executing boundary without runtime changes.

Phase 30.4 Phase 30 Runtime Slice Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 30 as the completed read-only runtime state inspection slice and stops at the Phase 31 gate without new runtime changes.

Phase 31.0 Phase 30 Runtime Slice Audit Charter is complete, merged to `main`, and tagged. It opens the docs/tests/fixtures-only Phase 31 audit/archive lane and records the Phase 30 audit result without runtime changes.

Phase 31.1 Read-Only Runtime State Boundary Evidence Review is complete, merged to `main`, and tagged. It records evidence that the Phase 30 slice remains deterministic, local-only, read-only, non-authoritative, non-executing, and side-effect-free without runtime changes.

Phase 31.2 Runtime Slice Regression and Gap Review is complete, merged to `main`, and tagged. It reviews Phase 30 regression coverage, finds no blocking safety regression, and recommends Phase 32 not default to implementation.

Phase 31.3 Phase 32 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It recommends Phase 32 as docs/tests/fixtures-only design review for the next narrow runtime slice, not runtime implementation.

Phase 31.4 Phase 31 Runtime Slice Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 31 as the completed docs/tests/fixtures-only audit/archive for the Phase 30 runtime slice and stops at the Phase 32 gate.

Phase 32.0 Phase 31 Next-Slice Design Audit Charter is complete, merged to `main`, and tagged. It opens the docs/tests/fixtures-only design review for the next narrow runtime slice and records the Phase 31 audit result.

Phase 32.1 Candidate Runtime Slice Inventory is complete, merged to `main`, and tagged. It reviews seven next-lane options and recommends Phase 33 as test-only `runtime_state` hardening with nested suspicious metadata fixtures rather than runtime implementation.

Phase 32.2 Next-Slice Safety And Scope Comparison is complete, merged to `main`, and tagged. It compares safety, scope, testability, rollback, usefulness, and readiness, confirming that no immediate Phase 33 runtime implementation is recommended.

Phase 32.3 Phase 33 Eligibility And Test Plan Matrix is complete, merged to `main`, and tagged. It defines Phase 33 as test-only `runtime_state` hardening, with no implementation file scope and an explicit Phil approval question.

Phase 32.4 Phase 32 Design Review Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 32 as docs/tests/fixtures-only, confirms no runtime or support files changed, and stops at the Phase 33 test-only hardening gate.

Phase 33.0 Phase 32 Test-Only Hardening Audit Charter is complete, merged to `main`, and tagged. It opens the approved test-only hardening lane for the existing read-only `runtime_state` inspection slice and records the Phase 32 audit result.

Phase 33.1 Nested Suspicious Metadata Fixture Design is complete, merged to `main`, and tagged. It adds synthetic caller-provided nested metadata fixtures for `runtime_state` hardening without changing runtime code.

Phase 33.2 Runtime State Nested Metadata Regression Tests is complete, merged to `main`, and tagged. It adds regression tests proving nested suspicious metadata remains safe under the existing `inspect_runtime_state` API without runtime code changes.

Phase 33.3 Phase 34 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It recommends Phase 34 as docs/tests/fixtures-only audit/archive for Phase 33 hardening rather than runtime implementation.

Phase 33.4 Phase 33 Test-Only Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 33 as test-only `runtime_state` hardening, records no runtime gap, and stops at the Phase 34 audit/archive gate.

Phase 34.0 Phase 33 Hardening Audit Charter is complete, merged to `main`, and tagged. It opens the docs/tests/fixtures-only audit/archive lane and records the Phase 33 audit result.

Phase 34.1 Nested Metadata Coverage Evidence Review is complete, merged to `main`, and tagged. It confirms Phase 33 nested metadata coverage and records that the claims remain inert caller-provided data.

Phase 34.2 Runtime State Hardening Gap Review is complete, merged to `main`, and tagged. It finds no concrete `runtime_state` gap, no runtime code change need, and no immediate additional test-only hardening need.

Phase 34.3 Phase 35 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It recommends Phase 35 as docs/tests/fixtures-only no-code design review for a possible second narrow runtime slice, not implementation.

Phase 34.4 Phase 34 Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 34, confirms no remaining gaps, and stops at the Phase 35 no-code design review gate.

Phase 35.0 Phase 34 Second-Slice Design Audit Charter is complete, merged to `main`, and tagged. It opens Phase 35 as docs/tests/fixtures-only no-code design review for a possible second narrow runtime slice, records the Phase 34 audit result as PASS, and keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, and physical-world behavior blocked.

Phase 35.1 Second Runtime Slice Candidate Inventory is complete, merged to `main`, and tagged. It reviews options A through H and identifies a future-only, non-executing candidate preview helper as the leading design candidate, while keeping Phase 36 implementation unapproved and `lima/` untouched.

Phase 35.2 Second-Slice Safety And Scope Comparison is complete, merged to `main`, and tagged. It compares candidate safety, usefulness, file scope, testability, rollback simplicity, and risk, then recommends a future candidate preview helper only for a later explicit Phase 36 approval question.

Phase 35.3 Phase 36 Eligibility And Test Plan Matrix is complete, merged to `main`, and tagged. It defines eligibility criteria, acceptance-test requirements, rollback/audit proof, stop conditions, and the exact future Phase 36 approval question without approving implementation.

Phase 35.4 Phase 35 Design Review Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 35 as completed docs/tests/fixtures-only no-code design review, preserves the exact Phase 36 approval question, and confirms Phase 36 remains gated pending explicit Phil approval.

Phase 36.0 Phase 35 Runtime Implementation Audit Charter is complete, merged to `main`, and tagged. It records the Phase 35 audit as PASS, opens Phase 36 for the explicitly approved candidate preview runtime slice, and adds no runtime implementation yet.

Phase 36.1 Candidate Preview Acceptance Design is complete, merged to `main`, and tagged. It defines the preview output shape, required input coverage, safety outcomes, and static boundary checks before implementation, without modifying runtime files.

Phase 36.2 Candidate Preview Runtime Implementation is complete, merged to `main`, and tagged. It adds `lima/kernel/candidate_preview.py` and safe exports in `lima/kernel/__init__.py` only, preserving non-execution, no approval, no dispatch, no persistence, no HumanInput bridge behavior, no Sparkbot wiring, no live adapters, no external calls, no background work, no robotics, and no physical-world behavior.

Phase 36.3 Candidate Preview Boundary Regression Review is complete, merged to `main`, and tagged. It confirms Phase 36.2 stayed within approved runtime scope and records the narrow stale Phase 35 test adjustment approved for Phase 36.2.

Phase 36.4 Phase 36 Runtime Slice Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 36 as the completed narrow candidate preview runtime slice and stops at the Phase 37 audit/archive approval gate.

Phase 37.0 Phase 36 Candidate Preview Audit Charter is complete, merged to `main`, and tagged. It opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 36 candidate preview runtime slice and records the Phase 36 audit result as PASS.

Phase 37.1 Candidate Preview Boundary Evidence Review is complete, merged to `main`, and tagged. It reviews Phase 36 acceptance evidence and static scan evidence without modifying runtime files.

Phase 37.2 Candidate Preview Regression And Gap Review is complete, merged to `main`, and tagged. It finds no regression, no blocking gap, and no immediate hardening need after the Phase 36 candidate preview slice.

Phase 37.3 Next-Lane Decision Matrix is complete, merged to `main`, and tagged. It recommends pausing and preserving the current runtime/test state after Phase 37.4, with no immediate runtime implementation, no immediate test-only hardening, and no Phil approval question required by this closeout.

Phase 37.4 Phase 37 Candidate Preview Audit Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 37 as a completed docs/tests/fixtures-only audit lane, confirms no runtime files, `tests/support/`, or stale prior-phase tests changed during Phase 37, finds no remaining gap, and recommends pausing and preserving the current runtime/test state.

Phase 38.0 Phase 37 Sparkbot Alignment Audit Charter is complete, merged to `main`, and tagged. It opens Sparkbot v1.6.80 alignment intake as docs/tests/fixtures-only work, records a Phase 37 audit PASS, and treats Sparkbot as read-only reference material without wiring or runtime behavior.

Phase 38.1 Sparkbot v1.6.42-to-v1.6.80 Concept Intake is complete, merged to `main`, and tagged. It records Sparkbot's current operating concepts as LIMA planning metadata only and preserves all non-execution, non-approval, non-dispatch, non-persistence, no-wiring, and no-physical-world invariants.

Phase 38.2 LIMA Consumer Boundary Vocabulary Review is complete, merged to `main`, and tagged. It defines Sparkbot-shaped consumer vocabulary for LIMA planning and fixtures while keeping owner-local, strict-security, explain-plan, approval, MCP, and robotics terms non-authoritative and non-executing.

Phase 38.3 Sparkbot-to-LIMA Gap and Risk Matrix is complete, merged to `main`, and tagged. It finds Sparkbot-shaped fixture coverage gaps and recommends Phase 39 as test-only `candidate_preview` hardening, with no runtime implementation, no `lima/` changes, and no Sparkbot wiring.

Phase 38.4 Phase 38 Alignment Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 38 as docs/tests/fixtures-only Sparkbot v1.6.80 alignment intake and recommends Phase 39 as test-only `candidate_preview` hardening with Sparkbot-shaped fixtures.

Phase 39.0 Sparkbot-Shaped Candidate Preview Hardening Charter is complete, merged to `main`, and tagged. It opens a docs/tests/fixtures-only hardening lane for Sparkbot-shaped `candidate_preview` fixtures without approving runtime implementation or `lima/` changes.

Phase 39.1 Sparkbot-Shaped Candidate Preview Fixtures is complete, merged to `main`, and tagged. It adds inert caller-provided JSON fixtures for Sparkbot-shaped owner-local, strict-security, breakglass, MCP, Robo OS, hardware-motion, agent kill-switch, and memory-trust cases.

Phase 39.2 Candidate Preview Sparkbot-Shaped Regression Tests is complete, merged to `main`, and tagged. It proves the existing `candidate_preview` helper keeps every Sparkbot-shaped fixture blocked, non-authoritative, non-executing, approval-free, dispatch-free, persistence-free, bridge-inactive, and side-effect free.

Phase 39.3 Hardening Gap and Next-Lane Decision Review is complete, merged to `main`, and tagged. It finds no runtime gap after Sparkbot-shaped hardening and recommends only Phase 39.4 archive/closeout followed by pause and preserve.

Phase 39.4 Phase 39 Sparkbot-Shaped Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 39 as completed docs/tests/fixtures-only hardening, finds no remaining gap, and recommends pausing and preserving the current runtime/test state.

Phase 40.0 Arc Bot Consumer Boundary Clarification is complete, merged to `main`, and tagged. It clarifies that Sparkbot v1.6.80 is reference evidence only, records Arc Bot / LIMA AI Office as the primary guarded task-oriented office consumer for future boundary planning, and preserves all runtime, Sparkbot, `tests/support/`, execution, approval, dispatch, persistence, external-call, robotics, and physical-world boundaries.

Phase 40.1 Arc Bot Guarded Task Consumer Boundary Review is complete, merged to `main`, and tagged. It defines Arc Bot / LIMA AI Office as a guarded task-oriented office consumer over LIMA AI OS/runtime safety concepts, with stricter defaults than Sparkbot and no runtime implementation.

Phase 40.2 LIMA Office Task Approval Audit Vocabulary Matrix is complete, merged to `main`, and tagged. It records the Arc Bot task, approval, explain-plan, run-state, audit/evidence, connector, memory-trust, scheduled-work, secret-use, admin-action, and physical-world planning vocabulary without adding runtime behavior.

Phase 40.3 Arc Bot Candidate Preview Fixture Plan is complete, merged to `main`, and tagged. It identifies the Arc Bot-shaped synthetic fixture cases for a future docs/tests/fixtures-only `candidate_preview` hardening lane and does not approve runtime implementation.

Phase 40.4 Arc Bot Consumer Boundary Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 40 as a completed docs/tests/fixtures-only Arc Bot / LIMA Office boundary review and recommends Phase 41 as docs/tests/fixtures-only Arc Bot-shaped `candidate_preview` hardening.

Phase 41.0 Arc Bot Candidate Preview Hardening Charter is complete, merged to `main`, and tagged. It opens a docs/tests/fixtures-only test-hardening lane for the existing `candidate_preview` helper without approving runtime implementation or `lima/` changes.

Phase 41.1 Arc Bot Candidate Preview Fixtures is complete, merged to `main`, and tagged. It adds synthetic Arc Bot / LIMA Office fixture data for later `candidate_preview` regression tests without modifying runtime code.

Phase 41.2 Arc Bot Candidate Preview Regression Tests is complete, merged to `main`, and tagged. It exercises the existing `candidate_preview` helper against Arc Bot-shaped fixture data and confirms deterministic, read-only, non-authoritative, non-executing, side-effect-free behavior without runtime changes.

Phase 41.3 Arc Bot Hardening Gap And Next-Lane Review is complete, merged to `main`, and tagged. It records that Phase 41 found no concrete runtime gap and recommends Phase 41.4 as docs/tests/fixtures-only archive closeout.

Phase 41.4 Arc Bot Candidate Preview Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 41 as a completed docs/tests/fixtures-only hardening lane, confirms no runtime gap, and recommends a future no-code Arc Bot / LIMA Office consumer contract design review rather than runtime implementation.

Phase 42.0 LIMA Universal Runtime Contract Reframing Audit is complete, merged to `main`, and tagged. It corrects Phase 42 away from Arc-centered framing and records LIMA AI OS as the universal model-, consumer-, and embodiment-agnostic runtime contract target while preserving Arc Bot as one example guarded office-agent profile.

Phase 42.1 Model-Agnostic Task Intent Contract Design is complete, merged to `main`, and tagged. It records universal planning contracts for input, task/intent, candidate preview, approval posture, telemetry/evidence, and embodiment/profile metadata without adding runtime schemas or authority.

Phase 42.2 Consumer And Embodiment Profile Taxonomy is complete, merged to `main`, and tagged. It records universal LIMA AI OS consumer profiles, embodiment/action profiles, action classes, and adapter-boundary vocabulary while keeping Arc Bot as one profile and robotics/IoT as blocked/deferred planning vocabulary.

Phase 42.3 Universal Safety Invariants And Guardian Boundary Matrix is complete, merged to `main`, and tagged. It records that Guardian or a future policy membrane owns real approval state, while LIMA Phase 42 only describes posture and cannot grant approval, execute, dispatch, persist, call adapters, or touch physical-world systems.

Phase 42.4 Universal Runtime Contract Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 42 as a completed docs/tests/fixtures-only universal LIMA AI OS contract design lane and recommends Phase 43 as Universal Contract Fixture Hardening, not implementation.

Phase 43.0 Universal Contract Fixture Hardening Charter is prepared on branch `phase-43-0-universal-contract-fixture-hardening-charter` as docs/tests/fixtures-only charter work. It opens the Phase 43 fixture-hardening lane without approving runtime implementation, `lima/` changes, `tests/support` changes, Sparkbot wiring, Arc Bot implementation, live adapters, real approval enforcement, execution, dispatch, persistence, external calls, robotics, physical-world behavior, background work, or hidden side effects.

Phase 43.1 Universal Contract Profile Fixtures is prepared on branch `phase-43-1-universal-contract-profile-fixtures` as docs/tests/fixtures-only fixture metadata. It adds inert universal consumer, embodiment/action, and adversarial profile fixtures while preserving preview-only, non-authoritative, non-executing, approval-free, dispatch-free, persistence-free, adapter-inactive, robotics-inactive, physical-world-inactive, and side-effect-free boundaries.

Phase 43.2 Universal Contract Profile Regression Tests is prepared on branch `phase-43-2-universal-contract-profile-regression-tests` as docs/tests/fixtures-only regression coverage over the existing `candidate_preview` helper. It proves risky, embodied, physical-world, and adversarial profile metadata stays blocked and that all preview outputs remain deterministic, read-only, local-only, non-authoritative, non-executing, approval-free, dispatch-free, persistence-free, adapter-inactive, robotics-inactive, and physical-world inactive without runtime changes.

Phase 43.3 Universal Contract Hardening Gap Review is prepared on branch `phase-43-3-universal-contract-hardening-gap-review` as docs/tests/fixtures-only review work. It finds no concrete runtime gap after Phase 43.0 through Phase 43.2, accepts conservative blocking as safe, and recommends Phase 43.4 archive closeout rather than runtime implementation.

Phase 43.4 Universal Contract Hardening Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 43, finds no concrete runtime gap, and stopped at the merge/tag approval gate before Phil approved the merge/tag.

Phase 44.0 Typed IntentEnvelope Guardian Request Bridge Design Charter is complete, merged to `main`, and tagged. It defines the no-code design bridge from HumanInput, shell request, bot request, or automation request metadata to typed IntentEnvelope candidate metadata and Guardian request metadata while keeping GuardianDecision creation, approval enforcement, execution, dispatch, persistence, model/tool/driver calls, adapters, robotics, physical-world behavior, and hidden side effects blocked.

Phase 44.1 Typed IntentEnvelope Guardian Request Fixtures is complete, merged to `main`, and tagged. It adds inert source request, typed intent candidate, and Guardian request metadata examples with future GuardianDecision absent/pending/blocked states and malicious bypass cases while keeping runtime behavior blocked.

Phase 44.2 Typed Bridge Fixture Validation Gap Review is complete, merged to `main`, and tagged. It validates that the Phase 44.1 fixture corpus adequately covers source request metadata -> typed IntentEnvelope candidate metadata -> Guardian request metadata with future GuardianDecision absent/pending/blocked metadata only, confirms no execution path exists, and records no concrete runtime gap.

Phase 44.3 Typed Bridge Archive / Closeout is complete, merged to `main`, and tagged. It archives Phase 44.0 through Phase 44.2 as a completed no-code typed bridge design/fixture/review lane and confirms no runtime implementation is recommended.

Phase 45.0 Typed Bridge Acceptance Test Design is complete, merged to `main`, and tagged. It defines required future acceptance test families before any runtime typed bridge implementation could be considered, while keeping runtime implementation blocked.

Phase 45.1 Typed Bridge Acceptance Test Fixture Matrix / Scaffolding Design is complete, merged to `main`, and tagged. It maps Phase 45.0 required test families into inert acceptance-test fixture matrix/scaffolding metadata and keeps runtime implementation and test harness behavior blocked.

Phase 45.2 Typed Bridge Acceptance Test Matrix Readiness Review is prepared on branch `phase-45-2-typed-bridge-acceptance-test-matrix-readiness-review` as docs/tests/fixtures-only readiness-review work. It reviews whether the Phase 45.1 matrix/scaffolding corpus adequately covers required test families, fail-closed rows, and boundary assertions before any future acceptance-test implementation design.

Latest completed phase merge:

`1806a6ecddcb66106eb76da03e75664c8f17c27e`

Latest tag:

`phase-45.1-typed-bridge-acceptance-test-fixture-matrix`

## Current Next Step

Current operator step:

Complete Phase 45.2 as a docs/tests/fixtures-only acceptance-test matrix readiness review lane for a future typed bridge runtime slice and push the branch for review. Runtime implementation, `lima/` changes, `tests/support` changes, runtime test harness creation, live adapters, approval enforcement, GuardianDecision creation, execution, dispatch, persistence, robotics, physical-world behavior, and hidden side effects remain blocked.

Recommended next branch:

No next branch is approved beyond Phase 45.2. Phase 45.3 requires Phil approval after Phase 45.2 review.

Latest completed merge:

`1806a6ecddcb66106eb76da03e75664c8f17c27e`

Recommended PR target:

`main`

Canonical state anchor:

Phase 45.1 is the canonical completed state before Phase 45.2. The prior stale Phase 23/28/29 state-anchor text is superseded and must not be used to infer approval for runtime work.

Phase 44 boundary:

Docs/tests/fixtures-only. Runtime implementation, `lima/` changes, `tests/support` changes, Sparkbot wiring, Arc Bot implementation, live adapters, real IntentCompiler behavior, real Guardian request behavior, real GuardianDecision creation, real approval enforcement, execution, dispatch, persistence, external calls, shell/browser/network/file mutation, model/tool/driver calls, robotics, hardware control, physical-world behavior, background workers, queues, daemons, subprocesses, threads, database writes, and hidden side effects remain blocked unless Phil explicitly approves a future implementation scope.

No live/customer connector or production deployment is approved by this cleanup.

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
## Phase 45.3 - Typed Bridge Acceptance Test Archive Closeout

- branch: `phase-45-3-typed-bridge-acceptance-test-archive-closeout`
- status: complete, merged to `main`, and tagged as `phase-45.3-typed-bridge-acceptance-test-archive-closeout`
- runtime implementation: blocked
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 46 docs/tests/fixtures-only static acceptance-test implementation-plan template or dry-run plan

## Phase 46.0 - Static Acceptance-Test Implementation-Plan Template

- branch: `phase-46-0-static-acceptance-test-implementation-plan-template`
- status: complete, merged to `main`, and tagged as `phase-46.0-static-acceptance-test-implementation-plan-template`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 46.1 docs/tests/fixtures-only static dry-run plan or readiness review

## Phase 46.1 - Static Acceptance-Test Dry-Run Plan

- branch: `phase-46-1-static-acceptance-test-dry-run-plan`
- status: complete, merged to `main`, and tagged as `phase-46.1-static-acceptance-test-dry-run-plan`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 46.2 docs/tests/fixtures-only static dry-run readiness review or archive closeout

## Phase 46.2 - Static Acceptance-Test Dry-Run Readiness Review

- branch: `phase-46-2-static-acceptance-test-dry-run-readiness-review`
- status: complete, merged to `main`, and tagged as `phase-46.2-static-acceptance-test-dry-run-readiness-review`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 46.3 docs/tests/fixtures-only archive closeout or static dry-run plan archive

## Phase 46.3 - Static Acceptance-Test Dry-Run Archive Closeout

- branch: `phase-46-3-static-acceptance-test-dry-run-archive-closeout`
- status: complete, merged to `main`, and tagged as `phase-46.3-static-acceptance-test-dry-run-archive-closeout`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 47 docs/tests/fixtures-only static acceptance-test planning archive or preflight review

## Phase 47.0 - Static Acceptance-Test Implementation Preflight Review

- branch: `phase-47-0-static-acceptance-test-implementation-preflight-review-clean`
- status: complete, merged to `main`, and tagged as `phase-47.0-static-acceptance-test-implementation-preflight-review`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 47.1 docs/tests/fixtures-only static acceptance-test implementation checklist

## Phase 47.1 - Static Acceptance-Test Implementation Checklist

- branch: `phase-47-1-static-acceptance-test-implementation-checklist`
- status: complete, merged to `main`, and tagged as `phase-47.1-static-acceptance-test-implementation-checklist`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 47.2 docs/tests/fixtures-only static acceptance-test checklist readiness review

## Phase 47.2 - Static Acceptance-Test Checklist Readiness Review

- branch: `phase-47-2-static-acceptance-test-checklist-readiness-review`
- status: complete, merged to `main`, and tagged as `phase-47.2-static-acceptance-test-checklist-readiness-review`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): Phase 47.3 docs/tests/fixtures-only static acceptance-test checklist archive closeout

## Phase 47.3 - Static Acceptance-Test Checklist Archive Closeout

- branch: `phase-47-3-static-acceptance-test-checklist-archive-closeout`
- status: complete, merged to `main`, and tagged as `phase-47.3-static-acceptance-test-checklist-archive-closeout`
- runtime implementation: blocked
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): merge/tag approval gate for the Phase 47 static acceptance-test lane; any future implementation lane requires separate explicit Phil approval

## Phase 48.0 - Implementation Gate Decision Charter

- branch: `phase-48-0-implementation-gate-decision-charter`
- status: complete, merged to `main`, and tagged as `phase-48.0-implementation-gate-decision-charter`
- runtime implementation: blocked
- implementation approval: not granted
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- recommended next lane (post-approval): pause/preserve or Phase 48.1 docs/tests/fixtures-only implementation gate readiness review; no implementation lane without separate explicit Phil approval

## Phase 48.1 - Implementation Gate Readiness Review

- branch: `phase-48-1-implementation-gate-readiness-review`
- status: complete, merged to `main`, and tagged as `phase-48.1-implementation-gate-readiness-review`
- runtime implementation: blocked
- implementation approval: not granted
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- Sparkbot Shell modifications in phase lane: not allowed
- recommended next lane (post-approval): pause/preserve or docs/tests/fixtures-only concrete implementation design review; implementation still requires separate explicit Phil approval

## Phase 48.2 - Concrete Implementation Design Review

- branch: `phase-48-2-concrete-implementation-design-review`
- status: docs/tests/fixtures-only concrete implementation design review in progress
- V1 product target captured: `docs/V1_PRODUCT_READINESS_TARGET.md`
- V1 readiness gap matrix captured: `docs/V1_READINESS_GAP_MATRIX.md`
- V1 target first shells: `Sparkbot_shell`, `Sparkbot`, `Arc-Bot-shell`
- V1 future capability direction: live approval, real `GuardianDecision`, provider/model routing, shell-owned haptic intent support, first-shell response-state parity
- destructive edit/delete policy: operator approval required in LIMA-AI-OS and shells
- next smallest safe V1 gap: Sparkbot_shell source-backed `thinking` / progress-state proof
- runtime implementation: blocked
- implementation approval: not granted
- runtime test harness: not created
- executable acceptance tests: not added
- `lima/` changes in phase lane: not allowed
- `tests/support/` changes in phase lane: not allowed
- Sparkbot Shell modifications in phase lane: not allowed
- recommended next lane (post-approval): pause/preserve or Phase 48.3 docs/tests/fixtures-only design readiness review; no implementation lane without separate explicit Phil approval
