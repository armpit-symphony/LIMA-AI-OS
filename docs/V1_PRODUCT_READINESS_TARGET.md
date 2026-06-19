# V1 Product Readiness Target

This document records the current V1 product target for LIMA-AI-OS.

It is product-direction and readiness evidence only. It does not approve runtime implementation, shell wiring, provider calls, model routing, provider SDK/network egress, GuardianDecision execution authority, approval enforcement expansion, persistence expansion, adapter calls, file mutation, browser/network activity, robotics, or physical-world behavior in the current branch.

## V1 Objective

LIMA-AI-OS V1 should become a usable Guardian-gated runtime for the first shell consumers:

- `Sparkbot_shell`
- public `Sparkbot`
- `Arc-Bot-shell`

Sparkbot remains the R&D reference for how shells should behave. LIMA should use Sparkbot as reference evidence and extract compatible contracts deliberately. LIMA must not copy Sparkbot code, import Sparkbot runtime modules, wire Sparkbot routes, or mutate consumer repositories unless a future implementation approval explicitly names that scope.

## Current Gate

LIMA remains `CANDIDATE_ONLY`.

The current V1 authority chain is audited through `V1-G54`. The post-G54 readiness rollup selects `V1-G55` as the next narrow authority gate.

`V1-G55` is an approval request for a bounded real provider SDK/network egress authority wrapper. The request is prepared, but implementation is not approved.

Authoritative G55 files:

- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_APPROVAL_REQUEST.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_WORK_ORDER.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_PREFLIGHT_AUDIT.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`
- `docs/audits/V1_G55_IMPLEMENTATION_BLOCKER_AUDIT.md`

The current operator choices are exactly:

- `Approve-V1-G55`
- `Revise-V1-G55`
- `Pause`

Runtime implementation may start only after the exact `Approve-V1-G55` state is recorded in the G55 operator decision packet.

## Accepted Evidence Through G54

The V1 evidence chain now includes:

- first-shell proof intake for `Sparkbot_shell`, public `Sparkbot`, and `Arc-Bot-shell`
- typed request and GuardianDecision preflight metadata
- local redacted audit/evidence persistence
- destructive approval enforcement metadata
- guarded file mutation policy and preview evidence
- consumer import, patch preview, repository edit, and import-smoke evidence
- shell wiring and consumer integration evidence
- provider/model dispatch, live-call authority, live-call execution metadata, and fake-executor smoke evidence
- provider credential/network hardening metadata
- real provider executor design, invocation metadata, and executable caller-injected wrapper metadata
- provider SDK/network/credential authority metadata
- fake SDK/fake-egress harness evidence
- runtime authority-chain audit through G54
- readiness rollup through G54
- V1 consumer target state after Arc readiness integration, including
  Arc-Bot-shell runtime gating readiness integration evidence and the public
  Sparkbot GitHub 403 publication blocker

This evidence is still candidate-only. It does not prove V1 product readiness, production readiness, live customer use, consumer production runtime integration, direct provider egress, secret access, or real SDK/network execution by LIMA.

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
- public `Sparkbot` behavior-reference alignment for approvals, Guardian posture, provider/model routing, and shell response states
- `Arc-Bot-shell` task-oriented approval, audit/evidence, connector, and office-work boundary proof
- no raw natural-language-to-tool execution shortcut
- provider/model routing constrained by Guardian and shell tool-pack scope
- destructive edit/delete operations requiring operator approval
- audit/evidence lineage for consequential actions
- consumer import/call smoke evidence remains fake-runtime or bounded by explicit approvals until a later gate authorizes more

## Current Status

Current status remains not V1 product-ready.

The active gate is `V1-G55`. The approval request, work order, preflight audit, operator decision packet, and implementation blocker audit are ready. Operator approval is not recorded. Runtime implementation is not approved.

Until `Approve-V1-G55` is explicitly recorded, the following remain blocked:

- G55 runtime implementation
- G55 public API export changes
- provider SDK/network egress invocation
- built-in provider SDK clients
- SDK dependencies
- vendor SDK imports
- direct provider SDK implementation
- provider endpoint resolution by LIMA
- LIMA-owned DNS, HTTP, socket, network calls, or direct provider egress
- secret lookup, credential value access, provider token access, or API key access
- provider configuration changes
- fallback execution
- Sparkbot or Arc-Bot-shell edits for G55
- consumer production runtime integration
- connector, browser, network, file, device, robotics, or physical-world behavior
- V1 product readiness or production readiness claims

## Remaining Blockers

- `Approve-V1-G55` is not recorded
- bounded real provider SDK/network egress wrapper is not implemented
- direct provider SDK/network egress by LIMA is still forbidden
- real provider SDK client ownership remains outside LIMA
- provider secrets and credential values remain inaccessible to LIMA
- consumer production runtime integration remains unapproved
- live runtime parity across first shells is not proven as product readiness
- release boundary remains not passed
- V1 product readiness is not approved
- production behavior is not approved

## Recommended Next Step

Use `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md` to record exactly one valid operator choice: `Approve-V1-G55`, `Revise-V1-G55`, or `Pause`.

If `Approve-V1-G55` is explicitly recorded with the exact required wording, implement only the bounded LIMA-side real provider SDK/network egress authority wrapper named in the G55 request. Stop before SDK dependencies, built-in provider SDK clients, LIMA-owned endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, physical-world behavior, or product-readiness claims.
