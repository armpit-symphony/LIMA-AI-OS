# Phase 45.0 Typed Bridge Acceptance Test Design

Phase 45.0 opens a docs/tests/fixtures-only no-code acceptance-test design lane for a future typed IntentEnvelope / Guardian request bridge runtime slice.

This phase does not implement a bridge, parser, runtime compiler behavior, runtime Guardian request behavior, GuardianDecision creation, approval enforcement, execution, dispatch, persistence, model calls, tool calls, driver calls, adapter calls, external calls, shell/browser/network/file mutation, robotics, physical-world behavior, background work, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Mission

Design the acceptance tests that must exist before any future runtime bridge implementation can be considered:

source request metadata -> typed IntentEnvelope candidate metadata -> Guardian request metadata -> future GuardianDecision metadata -> still no execution.

These are test requirements only. Phase 45.0 does not create bridge behavior, runtime records, policy decisions, persistence, or execution paths.

## Required Future Test Families

Future acceptance tests must cover:

- accepted source request metadata shape from HumanInput, shell request, bot request, and automation request sources
- typed IntentEnvelope candidate fields for intent kind, confidence, risk class, clarification state, requested tool-pack scope, and evidence requirements
- Guardian request metadata for actor, tenant, lineage, requested action class, risk posture, evidence references, policy review need, and approval posture
- GuardianDecision metadata states limited to absent, pending, or blocked until a future approved Guardian policy membrane exists
- fail-closed behavior for malicious approval claims, forged GuardianDecision claims, missing actor/tenant/lineage metadata, background scheduling claims, adapter claims, physical-world claims, model/tool/driver-call claims, and persistence claims

## Required Invariants

Every future acceptance test must prove:

- raw natural language cannot execute directly
- typed intent is metadata, not authority
- Guardian request is not GuardianDecision
- GuardianDecision metadata cannot grant approval, execution, dispatch, persistence, adapter access, model/tool/driver calls, external calls, robotics, or physical-world action
- source request metadata and typed bridge metadata remain deterministic and local-only in test scope
- all denied surfaces fail closed

## Required Validation Gate

Before any future runtime bridge implementation is allowed, a future phase must define concrete tests that prove:

- no `lima/` runtime file changes occur without explicit approval
- no `tests/support` helper behavior is added without explicit approval
- no Sparkbot, Arc Bot, HumanInput bridge, live adapter, IntentCompiler, Guardian request, GuardianDecision, approval, execution, dispatch, persistence, external-call, model/tool/driver-call, robotics, or physical-world behavior is introduced by test design work

## Boundary Result

Phase 45.0 is acceptance-test design only.

No runtime implementation is recommended by Phase 45.0.
No `lima/` file changed.
No `tests/support` file changed.

## Recommended Next Direction

Stop at review for Phase 45.0. If Phil approves, Phase 45.1 may add docs/tests/fixtures-only acceptance-test fixture requirements. Runtime implementation remains blocked.
