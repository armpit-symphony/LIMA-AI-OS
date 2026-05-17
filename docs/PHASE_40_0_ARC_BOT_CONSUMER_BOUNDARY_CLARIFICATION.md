# Phase 40.0 Arc Bot Consumer Boundary Clarification

Phase 40.0 clarifies the Phase 38 Sparkbot alignment intake without rewriting the completed Phase 38 or Phase 39 history.

Sparkbot v1.6.80 remains reference evidence for current product/control vocabulary. It is not the primary future consumer to wire next.

The intended guarded chat/task consumer for this planning thread is Arc Bot / LIMA AI Office: a guarded, task-oriented office agent built on LIMA AI OS / runtime safety concepts, not the full personal Sparkbot workstation/R&D bot.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, Sparkbot, `tests/support/`, stale prior-phase tests, runtime behavior, helper behavior, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, audit persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Product Distinction

Sparkbot:

- open R&D / self-hosted workstation assistant
- more personal-owner-friendly
- broader computer-control surface
- Command Center, Workstation, Robo OS, Guardian controls, model stack, memory, meetings, scheduled jobs
- useful as evidence for vocabulary and product/control lessons
- not the next direct integration target by default

Arc Bot / LIMA AI Office:

- guarded task-oriented office agent
- tighter default boundaries
- stronger task, approval, and audit posture
- intended to use LIMA AI OS / runtime concepts as its safety substrate
- should not inherit Sparkbot's broad owner-local execution posture by default
- primary guarded-task consumer for this planning line

LIMA AI OS / runtime remains the main target.

## Correct Phase 38 Framing

Use this framing:

> Sparkbot v1.6.80 concept intake for future Arc Bot / LIMA Office consumer boundary planning.

Do not use this framing:

> Prepare direct Sparkbot integration.

## Concept Classification

| Sparkbot concept | Phase 40 classification | Reason |
| --- | --- | --- |
| Command Center as operator hub | Adopt into LIMA AI OS planning vocabulary | LIMA needs an operator/control-surface concept, independent of Sparkbot UI. |
| Guardian controls and policy simulation | Adopt into LIMA AI OS planning vocabulary | Core safety vocabulary for all future consumers. |
| Run states: planned, awaiting approval, ready, blocked, completed, failed | Adopt into LIMA AI OS planning vocabulary | Needed for task-oriented office workflows. |
| Durable audit/evidence model | Adopt into LIMA AI OS planning vocabulary | Arc Bot needs evidence-first office actions. |
| Agent identity, scopes, expiration, risk tier, kill switch | Adopt into LIMA AI OS planning vocabulary | Useful cross-consumer safety metadata. |
| Memory trust, verification, redaction, pending approval | Adopt into LIMA AI OS planning vocabulary | Useful for guarded office memory. |
| Connector health/setup posture | Adopt into LIMA AI OS planning vocabulary | Useful before any office connector action. |
| Owner-local friendly routine-read posture | Adapt for Arc Bot / LIMA Office with stricter defaults | Arc Bot should not inherit broad owner-local computer-control defaults. |
| Strict Security posture | Adapt for Arc Bot / LIMA Office with stricter defaults | Arc Bot should default tighter than personal Sparkbot. |
| Persistent approvals / approval inbox | Adapt for Arc Bot / LIMA Office with stricter defaults | Useful, but office approval semantics must be stricter and role-aware. |
| Guarded scheduled work | Adapt for Arc Bot / LIMA Office with stricter defaults | Office scheduling needs explicit scope, evidence, and audit posture. |
| Round Table / meetings manager / task rooms | Adapt for Arc Bot / LIMA Office with stricter defaults | Useful task collaboration pattern, but bounded to office workflows. |
| Broad shell/browser/live terminal/code execution | Keep as Sparkbot-only product behavior | Too broad for Arc Bot defaults and not part of current LIMA runtime. |
| Personal workstation Command Center affordances | Keep as Sparkbot-only product behavior | Product-specific UX, not core LIMA substrate. |
| MCP/Robo OS manifests and robotics posture | Defer until future integration planning | Valuable, but not needed for Arc Bot office boundary review. |
| Direct Sparkbot integration | Defer until future integration planning | Sparkbot remains reference evidence, not next wiring target. |
| Inheriting Sparkbot owner-local execution behavior in LIMA runtime | Reject from LIMA runtime safety model | LIMA must stay Guardian-gated and non-authoritative until explicitly approved. |
| Runtime approval/execution/dispatch/persistence from planning labels | Reject from LIMA runtime safety model | Vocabulary must not grant authority. |

## Arc Bot Needs To Preserve

Future Arc Bot / LIMA Office planning should emphasize:

- task-oriented office workflow
- operator approval boundaries
- policy simulation / explain-plan before action
- run states: planned, awaiting approval, ready, blocked, completed, failed
- durable audit/evidence model
- agent identity and kill switch
- memory trust, verification, and redaction
- guarded scheduled work
- connector health and setup posture
- strict defaults for external writes, secrets, admin actions, and physical-world actions

## Revised Next Direction

Phase 39 is already complete and remains valid as test-only hardening of `candidate_preview` with Sparkbot-shaped evidence fixtures.

The next recommended direction after this clarification is docs/tests/fixtures-only Arc Bot / LIMA Office consumer boundary review, or test-only hardening of `candidate_preview` with Arc Bot-shaped task fixtures.

Do not recommend direct Sparkbot integration by default.

Do not recommend Arc Bot implementation yet.

Do not recommend HumanInput bridge implementation yet.
