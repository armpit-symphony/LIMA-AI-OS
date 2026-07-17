# V1-G7 First-Shell Integration Proof Audit Criteria

This document defines how LIMA will audit first-shell integration proof packets for V1 readiness gap `V1-G7`.

It is audit criteria only. It does not approve LIMA runtime behavior, shell wiring, provider/model calls, runtime `GuardianDecision` creation, approval enforcement, persistence, haptic device behavior, file mutation, browser/network behavior, robotics, physical-world behavior, runtime export cleanup, final API freeze, or production readiness.

## Audit Scope

The audit will review proof packets from:

- `Sparkbot_shell`
- `Sparkbot`
- `Arc-Bot-shell`

Each shell packet must be audited independently before LIMA makes any consolidated V1-G7 judgment.

## Required Audit Questions

For each shell, answer:

- Did the shell provide the requested proof packet?
- Did the shell provide the requested audit?
- Did the shell provide machine-readable fixture evidence?
- Did the shell run and report validation commands?
- Did the shell evaluate all required response states?
- Did the shell evaluate packet/kernel status mappings?
- Did the shell preserve haptics as shell-owned?
- Did the shell avoid claiming LIMA owns haptic device behavior?
- Did the shell prove destructive edit/delete requires operator approval or is blocked?
- Did the shell classify approval as real enforcement, preview-only, docs-only, or missing?
- Did the shell classify `GuardianDecision` authority as real, preview-only, docs-only, or missing?
- Did the shell classify provider/model routing as real, preview-only, docs-only, or missing?
- Did the shell constrain provider/model routing by Guardian, shell scope, tool-pack scope, secret, budget, privacy, and audit posture where applicable?
- Did the shell classify audit/evidence lineage as durable, static-only, preview-only, or missing?
- Did the shell avoid raw natural-language-to-tool execution shortcuts?
- Did the shell avoid unsafe connector, file, browser, network, device, robotics, and physical-world claims?
- Did the shell avoid LIMA runtime wiring?
- Did the shell avoid requiring unapproved LIMA runtime exports?
- Did the shell avoid importing/copying Sparkbot code into LIMA?
- Is the proof acceptable as static shell integration evidence?
- Is the proof insufficient for live runtime parity?
- What should LIMA accept?
- What should LIMA reject?
- What follow-up should be requested from the shell?

## Required State Coverage

Each shell packet must evaluate:

- `received`
- `thinking`
- `preview_ready`
- `blocked`
- `needs_approval`
- `completed`
- `failed_safe`
- `deferred`

The audit must categorize each as:

- `source_backed`
- `docs_fixture_only`
- `missing`

## Required Status Mapping

Each shell packet must evaluate at least:

- `proposed -> preview_only`
- `needs_review -> explain_plan`
- `blocked -> blocked`

Additional mappings may be accepted if they do not weaken the required mappings.

## Required Ownership Boundaries

The audit must preserve:

- LIMA owns runtime/kernel contracts and future authority boundaries.
- Shells own rendering, UX state presentation, haptic rendering, and device feedback.
- Guardian owns future authority for consequential action decisions.
- Operators own approval for destructive edit/delete behavior.
- Provider/model routing must be constrained by Guardian, shell/tool-pack scope, secret, budget, privacy, and audit posture.
- Audit/evidence lineage must be redacted and reference-based before durable storage is accepted.

## Static Acceptance

LIMA may accept a shell packet as static integration evidence when it proves:

- shell contract compatibility posture
- required state/status mapping review
- shell-owned haptic and rendering boundaries
- destructive edit/delete approval posture
- no raw natural-language-to-tool execution shortcut
- no unsafe runtime claims
- validation evidence is present

Static acceptance is not live runtime parity.

## Rejection / Return Conditions

Return or reject a shell packet if it:

- omits required state/status mapping
- treats LIMA haptic intent as device authority
- claims destructive edits/deletes can proceed without operator approval
- claims live approval enforcement without source-backed proof
- claims live `GuardianDecision` authority without source-backed proof
- claims provider/model routing without required constraints
- claims connector/file/browser/network/device/robotics/physical-world behavior without Guardian/action boundaries
- claims production or V1 product readiness from static evidence
- requires LIMA runtime wiring, runtime export cleanup, or final freeze approval

## Consolidated V1-G7 Closeout Rule

LIMA should not close `V1-G7` as complete until:

- all three shell packets have been delivered
- all three shell packets have LIMA intake audits
- accepted evidence and rejected claims are consolidated
- remaining blockers are explicit
- no runtime wiring or final freeze is implied

If any shell packet is missing or incomplete, V1-G7 remains open.
