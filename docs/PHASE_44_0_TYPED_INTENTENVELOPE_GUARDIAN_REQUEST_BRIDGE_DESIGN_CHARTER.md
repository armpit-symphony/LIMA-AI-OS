# Phase 44.0 Typed IntentEnvelope Guardian Request Bridge Design Charter

Phase 44.0 opens a no-code design lane for the typed IntentEnvelope / Guardian Request Bridge.

This phase is docs/tests/fixtures-only. It does not implement a bridge, parser, IntentCompiler runtime behavior, Guardian request runtime behavior, GuardianDecision creation, approval enforcement, dispatch, persistence, execution, model calls, tool calls, driver calls, adapters, shell/browser/network/file mutation, robotics, hardware control, physical-world behavior, background work, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Mission

Define the next architectural bridge for LIMA AI OS:

HumanInput / shell request / bot request / automation request -> typed IntentEnvelope candidate -> Guardian request -> future Guardian decision -> no execution yet.

The bridge supports the long-term natural-language OS direction while preserving the core safety rule: natural language never directly executes. A typed intent is structured metadata, not authority. A Guardian request is a request for review, not a decision. A future Guardian or policy membrane owns approval state.

## Charter Scope

Phase 44.0 may define:

- bridge vocabulary
- boundary invariants
- future fixture categories
- future test obligations
- roadmap, decision, extraction-plan, and current-state updates

Phase 44.0 may not define behavior that creates live records, routes requests, dispatches work, stores audit events, calls adapters, invokes models or tools, or touches physical-world systems.

## Bridge Boundary

Allowed bridge concepts:

- source request metadata from HumanInput, shell request, bot request, or automation request
- typed IntentEnvelope candidate fields such as intent kind, confidence, risk class, evidence requirements, clarification state, and requested tool-pack scope
- Guardian request metadata such as actor, tenant, lineage reference, requested action class, risk posture, evidence references, and policy-review needs
- future GuardianDecision reference as absent, pending, or blocked

Forbidden bridge claims:

- approval granted
- execution allowed
- dispatch allowed
- persistence allowed
- external calls allowed
- adapter active
- shell/browser/network/file mutation allowed
- robotics or physical-world action allowed
- GuardianDecision created
- audit storage written

## Future Fixture Targets

If Phil approves a later docs/tests/fixtures-only slice, Phase 44.1 should add inert fixture data for:

- safe draft-only natural-language request
- ambiguous request requiring clarification
- external write request requiring Guardian review
- tool-pack scope request
- scheduled/background request without dispatch
- physical-world request blocked before drivers
- emergency stop request with no execution path
- malicious typed intent trying to claim approval
- malicious Guardian request trying to claim decision authority
- missing actor, tenant, or lineage metadata

## Safety Invariants

- Raw natural language cannot execute directly.
- Typed intent is metadata, not authority.
- Guardian request is not GuardianDecision.
- Approval state is owned by a future Guardian or policy membrane.
- No model, tool, driver, shell, browser, network, file, adapter, or physical-world dispatch is allowed.
- No audit persistence, database write, background worker, queue, daemon, subprocess, or thread is allowed.
- No Sparkbot wiring, Arc Bot implementation, live adapter, or `tests/support` helper behavior is added.
- No `lima/` runtime behavior changes are made.

## Recommended Next Direction

Stop after Phase 44.0 for review. If Phil approves, the next safe lane is Phase 44.1 docs/tests/fixtures-only typed IntentEnvelope / Guardian request bridge fixture contract data. No runtime implementation is recommended by this charter.
