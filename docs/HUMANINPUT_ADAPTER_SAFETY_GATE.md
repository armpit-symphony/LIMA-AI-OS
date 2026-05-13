# HumanInput Adapter Safety Gate

This safety gate applies to any future HumanInput adapter work.

The gate is documentation only in Phase 4.8. It is not adapter code, not executable, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

## Gate Purpose

A future HumanInput adapter may be proposed only after this gate is satisfied in a later explicitly approved phase.

The adapter boundary must remain narrow:

- accept selected shell intake context
- produce HumanInput only
- preserve source, actor, session, trust, privacy, lineage, and handoff references
- stop before IntentEnvelope
- stop before GuardianDecision
- stop before model, tool, terminal, robot, or driver behavior

## Required Adapter Contract

Any future adapter design must prove:

- adapter output is HumanInput only
- source metadata is reference-only
- shell, channel, room, actor, and session values are passive metadata
- passive trust and autonomy values do not grant authority
- transcript confidence is descriptive metadata only
- privacy, redaction, retention, and visibility fields are metadata only
- lineage seeds are references only
- handoff requirements point toward future IntentEnvelope and GuardianDecision boundaries without creating them
- all capability flags remain non-authorizing
- blocked capabilities remain explicit

## Required Blockers

Any future adapter proposal is blocked if it requires:

- files under `lima/` before explicit implementation approval
- live adapter code
- Sparkbot import or wiring
- Sparkbot route import or code copy
- runtime behavior
- natural-language parsing into action
- model calls
- tool execution
- terminal or PTY behavior
- robotics behavior
- robot or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- execution
- audit persistence
- production shell implementation

## Review Checklist

Before any future adapter code phase, reviewers must confirm:

- the adapter returns HumanInput only
- no IntentEnvelope is created
- no GuardianDecision is created
- no approval, enforcement, execution, or audit persistence is created
- no model, tool, terminal, robot, or physical-world behavior is introduced
- no live auth, session, or trust lookup is introduced
- no Sparkbot code is copied, imported, or wired
- no production integration identifiers are introduced
- no secrets, credentials, tokens, hostnames, deployment details, or private operational data are introduced
- the phase is explicitly approved for any code beyond docs/tests/fixtures

## Exit Criteria

This gate is not passed by documentation alone.

A later explicitly approved phase must provide a specific adapter design or implementation scope, validation plan, and safety review before any adapter code can be considered.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
