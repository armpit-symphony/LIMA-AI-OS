# Phase 6.3 Approval / Audit / Memory Boundary Planning

Phase 6.3 plans how approval, audit, spine, and memory boundaries relate to the LIMA Kernel lifecycle. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not read or write memory.

## Approval Boundary

Approval state remains descriptive metadata until a future explicitly approved runtime phase. A future system may describe states such as proposed, approval_required, denied, blocked, or ready_for_review, but Phase 6.3 does not verify approval, open breakglass, enforce approval, or authorize execution.

HumanInput and IntentEnvelope candidates may request work, but they are not permission. GuardianDecision remains the future authority boundary for approval semantics.

## Audit and Spine Boundary

Audit and spine metadata remains lineage planning only. A future system may require event IDs, provenance links, retention policy, review evidence, and decision IDs, but Phase 6.3 does not create audit events, append a ledger, persist records, or store operational data.

Audit planning must precede runtime persistence so execution paths cannot appear before evidence, review, retention, and redaction requirements are defined.

## Memory Boundary

Memory metadata remains reference-only. A future system may attach memory refs, context refs, recall constraints, privacy markings, and retention intent, but Phase 6.3 does not read memory, write memory, update embeddings, create summaries, or store personal data.

Memory context can inform future review, but it cannot approve, enforce, execute, or bypass Guardian.

## Boundary Rules

- Approval references are not approval enforcement.
- Audit references are not audit persistence.
- Memory references are not memory reads or writes.
- Spine references are not event-ledger writes.
- HumanInput remains intent context, not execution permission.
- IntentEnvelope candidates remain non-executable.
- GuardianDecision remains future authority, not current runtime behavior.
- Operator, admin, Phil, trusted, or owner wording must never bypass approval.
- Shell, browser, network, file, robot, and physical-world actions remain blocked.

## Next Gate

Phase 6.4 may close the Phase 6 planning lane with a roadmap gate / next-lane closeout as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
