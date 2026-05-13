# Test-only HumanInput Adapter Harness Safety Gate

This safety gate applies to any future test-only HumanInput adapter harness work.

The gate is documentation only in Phase 4.12. It is not harness implementation, not adapter implementation, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

## Gate Purpose

A future test-only harness may be proposed only after this gate is satisfied in a later explicitly approved phase.

The harness boundary must remain narrow:

- test synthetic fixtures only
- validate HumanInput fixture shape only
- avoid live shell, auth, session, trust, Sparkbot, model, tool, terminal, robot, and production sources
- stop before IntentEnvelope
- stop before GuardianDecision
- stop before approval, enforcement, execution, and audit persistence

## Required Harness Rules

Any future test-only harness design must prove:

- harness input is synthetic only
- harness output is validation result metadata only
- harness validates HumanInput shape only
- harness does not create HumanInput from live sources
- harness does not create IntentEnvelope
- harness does not create GuardianDecision
- harness does not call models
- harness does not call tools
- harness does not write terminal or PTY input
- harness does not call robots or physical-world drivers
- harness does not perform live trust, auth, or session lookup
- harness does not approve, enforce, execute, or persist audit data
- harness does not imply production adapter readiness

## Required Blockers

Any future test-only harness proposal is blocked if it requires:

- files under `lima/` before explicit implementation approval
- live adapter implementation
- production adapter implementation
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

## Production Readiness Warning

Passing this gate does not mean production adapter readiness.

A test-only harness can only prove static shape, blocker enforcement, and non-runtime fixture discipline. It cannot prove live adapter safety, Sparkbot integration safety, runtime wiring safety, Guardian enforcement safety, or physical-world safety.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
