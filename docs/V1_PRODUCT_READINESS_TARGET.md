# V1 Product Readiness Target

This document records the current V1 product target for LIMA-AI-OS.

It is product-direction evidence only. It does not approve runtime implementation, shell wiring, provider calls, model routing, GuardianDecision creation, approval enforcement, persistence, adapter calls, file mutation, browser/network activity, robotics, or physical-world behavior in the current branch.

## V1 Objective

LIMA-AI-OS V1 should become a usable Guardian-gated runtime for the first shell consumers:

- `Sparkbot_shell`
- `Sparkbot`
- `Arc-Bot-shell`

Sparkbot remains the R&D reference for how shells should behave. LIMA should use Sparkbot as reference evidence and extract compatible contracts deliberately. LIMA must not copy Sparkbot code, import Sparkbot runtime modules, or wire Sparkbot routes unless a future implementation approval explicitly names that scope.

## Sparkbot Reference Evidence Checked

The local `C:\Users\limap\Sparkbot` checkout is present. Git revision reads were blocked by Git ownership safety for this sandbox user, so no Sparkbot commit is recorded here.

Read-only document references checked:

- `Sparkbot/AGENTS.md`: identifies Sparkbot as the public/R&D assistant app with model/provider switching and Guardian approvals.
- `Sparkbot/docs/capabilities.md`: documents owner-local operation, provider/model setup and routing, persistent approvals, operator controls, and confirmation for dangerous/destructive actions.
- `Sparkbot/docs/PUBLIC_RELEASE_CAPABILITY_MODEL.md`: documents public capability tiers where file edits/deletes, writes, sends, credential access, service control, and critical changes require confirmation or elevated approval.

These references support using Sparkbot as behavior guidance for V1 shell policy. They do not authorize copying Sparkbot implementation into LIMA.

## Accepted Future V1 Runtime Capabilities

The following capabilities are acceptable as future V1 product requirements after separately approved implementation gates:

- live/actual approval flow
- real `GuardianDecision` runtime path
- provider/model routing
- shell haptic intent support
- shell response-state parity for first shell consumers

These are not implemented by this document and are not approved by Phase 48.2.

## Operator Approval Rule

Deleting or editing anything must require operator approval in LIMA-AI-OS and in first shell consumers.

This applies at minimum to:

- deleting files, records, memories, messages, tasks, events, customer data, or shell-owned state
- editing or mutating files, records, memories, messages, tasks, events, customer data, or shell-owned state
- overwriting existing content
- destructive admin or connector actions

Read-only inspection, preview, explanation, draft generation, and blocked/deferred states may remain lower risk when they do not mutate state, reveal secrets, execute external actions, or bypass shell/Guardian policy.

## Haptics Ownership

Haptics are acceptable as a V1 shell experience requirement, but ownership remains split:

- shells own haptic rendering, tactile behavior, animation, and device-specific feedback
- LIMA may define future haptic intent metadata for shell contracts
- LIMA does not own device haptic implementation
- no haptic implementation is added by this document

## First-Shell Readiness Requirements

For V1, LIMA must prove compatibility with the first shells before product readiness can be claimed:

- `Sparkbot_shell` UX-state proof, including real source-backed `thinking` / streaming or progress state
- `Sparkbot` behavior-reference alignment for approvals, Guardian posture, provider/model routing, and shell response states
- `Arc-Bot-shell` task-oriented approval, audit/evidence, connector, and office-work boundary proof
- no raw natural-language-to-tool execution shortcut
- provider/model routing constrained by Guardian and shell tool-pack scope
- destructive edit/delete operations requiring operator approval
- audit/evidence lineage for consequential actions

## Current Status

Current status remains not V1 product-ready.

The current Phase 48.2 branch is a docs/tests/fixtures-only concrete implementation design review. It does not implement runtime behavior and does not approve a runtime implementation lane.

## Remaining Blockers

- real `GuardianDecision` runtime path is not implemented
- live approval enforcement is not implemented
- provider/model routing is not implemented
- typed bridge runtime behavior is not implemented
- shell runtime wiring is not implemented
- Sparkbot_shell real `thinking` proof remains missing as live/source-backed behavior
- haptics proof and implementation remain shell-owned and not implemented here
- audit persistence is not implemented
- destructive edit/delete approval enforcement is not implemented
- production behavior is not approved

## Recommended Next Step

Use Phase 48.3 or the next approved docs/tests/fixtures lane to review whether the Phase 48.2 design still points at the right first implementation target after this V1 product direction.

`docs/V1_READINESS_GAP_MATRIX.md` records the current gap order and recommends closing Sparkbot_shell `thinking` / progress-state proof first. The request packet for that gap is `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md`.

The likely next implementation design question is:

Should the next concrete lane stay limited to typed bridge acceptance-test proof, or should the next design lane expand into a V1 product-readiness implementation sequence that separately scopes live approval, real GuardianDecision, provider/model routing, haptic intent metadata, and destructive-action operator approval?
