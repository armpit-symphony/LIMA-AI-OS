# Phase 6.2 IntentEnvelope and GuardianDecision Lifecycle Boundary Map

Phase 6.2 maps the boundary between IntentEnvelope candidate metadata and future GuardianDecision authority. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, and does not persist audit.

## IntentEnvelope Candidate Lifecycle

1. HumanInput context is referenced as operator-originated intent context.
2. Candidate metadata is drafted from explicit typed fields.
3. Provenance and lineage references are attached.
4. Risk tier and confidence metadata are proposed.
5. Approval state is proposed as descriptive metadata only.
6. Guardian review readiness is recorded.
7. Compilation, dispatch, execution, and persistence remain blocked until a future explicitly approved runtime phase.

IntentEnvelope candidate metadata is not a command, not authorization, not approval, not execution, not audit persistence, and not driver readiness.

## GuardianDecision Lifecycle

1. Review request metadata is prepared for a future Guardian boundary.
2. Policy context, risk context, trust context, and evidence requirements are referenced.
3. Decision states may be described as approve, deny, block, or request more review.
4. Approval semantics remain future authority semantics only.
5. Enforcement, execution, driver handoff, and audit persistence remain blocked.

GuardianDecision is the future authority boundary, but Phase 6.2 does not create, evaluate, enforce, persist, or execute GuardianDecision behavior.

## Boundary Rules

- HumanInput remains intent context, not execution permission.
- IntentEnvelope candidates remain non-executable.
- IntentEnvelope candidates cannot approve themselves.
- GuardianDecision remains future authority, not current runtime behavior.
- Approval state metadata is descriptive until a future explicit runtime phase.
- Audit, spine, and memory references remain lineage planning only.
- Driver/tool handoff remains blocked until GuardianDecision and audit boundaries are explicitly approved.
- Operator, admin, Phil, trusted, or owner wording must never bypass approval.

## Next Gate

Phase 6.3 may plan Approval / Audit / Memory boundaries as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
