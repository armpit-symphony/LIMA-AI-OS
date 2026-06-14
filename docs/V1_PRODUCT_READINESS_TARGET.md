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

The current V1 lane remains docs/tests/fixtures-only. It does not implement runtime behavior and does not approve a runtime implementation lane.

`V1-G1` source-backed Sparkbot_shell `thinking` evidence has now been accepted in `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md` from Sparkbot_shell commit `36d697bf875a44dbafa41fc841ded86437917627`. This proves local shell-owned `received -> thinking -> completed` behavior only. It does not prove live model streaming parity, provider/model response pacing, LIMA runtime integration, approval enforcement, GuardianDecision authority, haptics, persistence, or production behavior.

`V1-G2` static typed bridge acceptance proof has been accepted in `docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md`. It proves metadata shape, status mapping, and fail-closed case coverage only.

`V1-G3` static destructive edit/delete operator-approval contract proof has been accepted in `docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md`. It proves destructive action classes require operator approval metadata and static approval-bypass claims fail closed. It does not prove live approval enforcement or runtime mutation blocking.

`V1-G4` static real `GuardianDecision` and live approval path design-gate proof has been accepted in `docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md`. It proves future decision outcome families, status mappings, decision-scope requirements, and fail-closed authority cases only. It does not prove runtime `GuardianDecision` authority or live approval enforcement.

`V1-G5` static provider/model routing contract proof has been accepted in `docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md`. It proves route families, metadata, Guardian/shell/tool-pack/secret/budget/privacy/audit gates, fallback inheritance, and fail-closed routing cases only. It does not prove runtime provider/model routing or model calls.

`V1-G6` static haptic intent metadata contract proof has been accepted in `docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md`. It proves shell response state to haptic intent family mapping, required non-device metadata, forbidden device fields, shell-owned haptic boundaries, accessibility/fallback metadata, and fail-closed forged device haptic claims only. It does not prove device haptic behavior, shell rendering, LIMA runtime integration, or live UX parity.

`V1-G7` first-shell integration proof is now closed as static evidence in `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md`. `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` proof packets have been delivered and intaken by LIMA. This proves static first-shell compatibility evidence only. It does not prove live runtime parity, shell wiring, or V1 product readiness.

`V1-G8` audit/evidence persistence request gate is now recorded in `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_GATE.md`. It defines required durable record families, lineage fields, query capabilities, shell evidence needs, and fail-closed negative cases only. It does not implement durable audit persistence, storage adapters, query APIs, export/delete review behavior, live approval, real `GuardianDecision`, provider/model routing, shell wiring, or V1 product readiness.

`V1-G8` static audit/evidence persistence contract and threat model are now recorded in `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CONTRACT.md` and `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_THREAT_MODEL.md`. They define static record families, query rules, redaction/retention envelopes, destructive edit/delete approval evidence requirements, provider/model route evidence requirements, export/delete review refs, and threat mitigations only. They do not implement durable runtime persistence.

`V1-G9` product release boundary audit is now recorded in `docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md`. The audit is complete, but the release boundary is not passed. LIMA remains `CANDIDATE_ONLY`; runtime export cleanup, final API freeze, V1 product readiness, and production readiness remain unapproved.

`V1-G10` minimum runtime implementation gate is now recorded in `docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_GATE.md`. It defines the future V1-G11 file-touch map, rollback plan, acceptance-test expectations, stop conditions, and runtime-slice boundaries. It does not approve runtime implementation or change runtime behavior.

## Remaining Blockers

- V1-G11 implementation approval is still required
- runtime implementation scope gate is defined, but runtime implementation is not approved
- real `GuardianDecision` runtime path is not implemented
- live approval enforcement is not implemented
- provider/model routing is not implemented
- typed bridge runtime behavior is not implemented
- shell runtime wiring is not implemented
- first-shell integration proof is static-only and does not prove live runtime parity
- live model streaming parity remains unproven
- haptic device rendering proof remains shell-owned and not implemented here
- audit persistence request gate exists, but durable audit persistence is not implemented
- destructive edit/delete approval enforcement is not implemented
- product release boundary audit is complete, but release boundary is not passed
- runtime export cleanup remains unapproved
- final API freeze remains unapproved
- production behavior is not approved

## Recommended Next Step

Use `V1-G11`, after explicit approval, to implement the typed request and GuardianDecision preflight runtime slice exactly inside the V1-G10 file-touch map.

`docs/V1_READINESS_GAP_MATRIX.md` records the current gap order. Sparkbot_shell `thinking` / progress-state proof is accepted as source-backed local shell evidence by `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md`.

`docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md` records the V1-G2 static typed bridge acceptance proof. It proves metadata shape, status mapping, and fail-closed case coverage only. It does not prove runtime bridge behavior.

`docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md` records the V1-G3 static destructive edit/delete approval contract proof. It proves destructive approval metadata requirements and approval-bypass fail-closed behavior only. It does not prove runtime approval enforcement.

`docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md` records the V1-G4 static real `GuardianDecision` and live approval path design gate. It proves decision outcome families, GuardianDecision status mapping, decision-scope requirements, and fail-closed authority cases only. It does not prove runtime authority.

`docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md` records the V1-G5 static provider/model routing contract and acceptance-test design. It proves route constraints and fail-closed model-routing cases only. It does not prove runtime routing.

`docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md` records the V1-G6 static haptic intent metadata contract and shell fixture proof. It proves non-device haptic intent metadata shape and fail-closed device haptic claim handling only. It does not prove device behavior or shell rendering.

`docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md` records the V1-G7 first-shell integration proof closeout. It accepts `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` as static first-shell evidence only. It does not approve shell runtime wiring or live parity.

`docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_GATE.md` records the V1-G8 audit/evidence persistence request gate. `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_AUDIT_CRITERIA.md` records the audit criteria. `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_CLOSEOUT.md` records the request closeout. These do not complete durable persistence.

`docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md` records the V1-G9 product release boundary audit. It confirms that static evidence is not enough for V1 readiness, runtime export cleanup, final freeze, or production claims.

`docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_GATE.md` records the V1-G10 minimum runtime implementation gate. It confirms that the first future runtime slice should be typed request plus GuardianDecision preflight behavior only, with no execution, no provider/model calls, no durable persistence, no shell wiring, no runtime export cleanup, and no final freeze.

The next implementation design question is:

Should V1-G11 be explicitly approved as the smallest runtime implementation slice that moves LIMA from static V1 evidence toward usable V1 behavior without bypassing Guardian, approval, audit/evidence, shell, or rollback boundaries?
