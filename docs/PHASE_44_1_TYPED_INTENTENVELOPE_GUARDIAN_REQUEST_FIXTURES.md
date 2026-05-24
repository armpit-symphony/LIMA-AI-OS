# Phase 44.1 Typed IntentEnvelope Guardian Request Fixtures

Phase 44.1 adds docs/tests/fixtures-only inert fixture data for the typed IntentEnvelope / Guardian request bridge design lane.

This phase does not implement a bridge, parser, runtime compiler behavior, runtime Guardian request behavior, GuardianDecision creation, approval enforcement, execution, dispatch, persistence, model calls, tool calls, driver calls, adapter calls, external calls, shell/browser/network/file mutation, robotics, physical-world behavior, background work, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Mission

Create inert future-bridge metadata examples:

source request metadata -> typed IntentEnvelope candidate metadata -> Guardian request metadata -> future GuardianDecision absent/pending/blocked -> no execution.

The corpus exists to harden shape and safety expectations before any runtime bridge exists.

## Fixture Coverage

Phase 44.1 fixture cases include:

- safe draft-only natural-language request
- ambiguous request requiring clarification
- external write request requiring Guardian review
- tool-pack scope request
- scheduled/background request without dispatch
- physical-world request blocked before drivers
- emergency stop request with no execution path
- malicious typed intent claiming approval
- malicious Guardian request claiming decision authority
- missing actor, tenant, or lineage metadata

## Invariants

Every case in this phase remains:

- docs/tests/fixtures-only
- non-authoritative
- safe by default
- deterministic
- local only
- no runtime activation

Every case denies:

- approval granted
- GuardianDecision created
- execution allowed
- dispatch allowed
- persistence allowed
- model/tool/driver calls
- adapter activity
- external calls
- shell/browser/network/file mutation
- robotics or physical-world action
- audit storage writes

## Boundary Result

The fixture corpus models future bridge metadata only. It does not create behavior.

No `lima/` file changed.
No `tests/support` file changed.
No Sparkbot wiring, Arc Bot implementation, or live adapter behavior was added.

## Recommended Next Direction

Stop at review for Phase 44.1. If Phil approves, Phase 44.2 may add docs/tests/fixtures-only regression checks over this corpus. No runtime implementation is recommended by Phase 44.1.
