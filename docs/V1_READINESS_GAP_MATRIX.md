# V1 Readiness Gap Matrix

This matrix turns the V1 product target into an implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, GuardianDecision creation, approval enforcement, persistence, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Current branch: `v1-g11-runtime-slice-approval-request`
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Current product status: not V1-ready
- Current implementation approval: not granted

## Readiness Matrix

| ID | Gap | Current evidence | V1-ready requirement | Recommended lane | Runtime approval needed |
| --- | --- | --- | --- | --- | --- |
| `V1-G0` | V1 target clarity | `docs/V1_PRODUCT_READINESS_TARGET.md` exists and is static-tested | Keep first-shell target, operator approval rule, haptics ownership, and future runtime capabilities explicit | Complete in current branch | No |
| `V1-G1` | Sparkbot_shell `thinking` / progress proof | LIMA accepted Sparkbot_shell commit `36d697bf875a44dbafa41fc841ded86437917627` in `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md` as source-backed local shell evidence | Source-backed shell evidence for in-band thinking/progress state | Complete as source-backed local shell evidence; live streaming parity remains out of scope | No LIMA runtime approval |
| `V1-G2` | Typed bridge acceptance proof | `docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md` and static fixtures/tests prove source request metadata, typed IntentEnvelope candidate metadata, Guardian request metadata, GuardianDecision absent/pending/blocked boundaries, status mappings, and fail-closed cases | Executable acceptance tests proving source request metadata, typed IntentEnvelope candidate metadata, and Guardian request metadata fail closed without authority | Complete as static docs/tests/fixtures-only proof; runtime bridge remains out of scope | No runtime approval |
| `V1-G3` | Destructive edit/delete approval contract | `docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md` and static fixtures/tests prove destructive action classes require operator approval metadata and approval-bypass claims fail closed | Contract and tests proving destructive action classes cannot be marked approved without explicit operator approval metadata | Complete as static docs/tests/fixtures-only contract; runtime enforcement remains out of scope | No for static contract; later runtime approval required for enforcement |
| `V1-G4` | Real GuardianDecision and live approval path | `docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md` and static fixtures/tests define future decision outcomes, status mappings, approval-decision dependency, and fail-closed authority cases | Runtime GuardianDecision path that distinguishes allow, confirm, deny, privileged, expired, revoked, and blocked outcomes before consequential action | Complete as static docs/tests/fixtures-only design gate; runtime authority remains out of scope | No for static gate; later runtime approval required for implementation |
| `V1-G5` | Provider/model routing | `docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md` and static fixtures/tests define route families, metadata, Guardian/shell/tool-pack/secret/budget/privacy/audit gates, fallback inheritance, and fail-closed routing cases | Model routing constrained by Guardian, shell tool-pack scope, secret policy, and audit/evidence rules | Complete as static docs/tests/fixtures-only contract and acceptance-test design; runtime routing remains out of scope | No for static contract; later runtime approval required for routing |
| `V1-G6` | Haptic intent metadata | `docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md` and static fixtures/tests define shell state to haptic intent mapping, metadata fields, forbidden device fields, shell ownership, and fail-closed forged device claims | LIMA may emit non-device-specific haptic intent metadata while shells own rendering/device feedback | Complete as static docs/tests/fixtures-only contract; device behavior remains out of scope | No device implementation in LIMA |
| `V1-G7` | First-shell integration proof | `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` proof packets have LIMA intake audits and consolidated closeout in `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md` | `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` each prove they can consume or align with LIMA contract outputs safely as static evidence | Complete as static first-shell integration evidence; runtime parity remains out of scope | No for static closeout; runtime wiring requires later approval |
| `V1-G8` | Audit/evidence persistence | `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CONTRACT.md` and `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_THREAT_MODEL.md` define static record families, lineage fields, query needs, redaction/retention envelopes, threat mitigations, and negative cases; durable audit persistence is not implemented | Consequential actions produce durable, redacted, queryable evidence lineage | Complete as static contract/threat model; runtime persistence remains out of scope | No for static contract; later runtime persistence approval required |
| `V1-G9` | Product release boundary | `docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md` and `docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_CLOSEOUT.md` record that the release boundary audit is complete but not passed | V1 release gates, compatibility freeze, shell compatibility evidence, rollback proof, and runtime blockers all pass | Complete as static release-boundary audit; release boundary remains blocked | No implementation by audit alone |
| `V1-G10` | Minimum runtime implementation gate | `docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_GATE.md` and `docs/V1_G10_MINIMUM_RUNTIME_IMPLEMENTATION_CLOSEOUT.md` define exact file-touch map, rollback plan, acceptance-test obligations, stop conditions, and first runtime-slice scope | Exact file-touch map, rollback plan, stop conditions, and first runtime-slice scope exist before any `lima/` runtime change | Complete as static implementation gate; runtime remains unapproved | No for gate; later runtime approval required |
| `V1-G11` | Typed request GuardianDecision preflight runtime slice | `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md`, `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_PREFLIGHT_AUDIT.md`, and `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md` record the exact approval question, preflight audit, valid choices, required approval wording, and an empty Decision Record section; operator approval is not recorded | Local deterministic runtime slice converts validated candidate metadata into typed request metadata, produces fail-closed GuardianDecision preflight metadata, and emits non-persistent audit/evidence linkage without execution | Record one valid operator choice in the Decision Record section; implement only after explicit approval and only inside the approved file-touch map | Yes |

## Recommended Order

1. Treat `V1-G1` as accepted for source-backed local shell `thinking` evidence, while rejecting live runtime parity claims.
2. Treat `V1-G2` as complete for static typed bridge acceptance proof, while rejecting runtime parity claims.
3. Treat `V1-G3` as complete for static destructive edit/delete approval contract evidence, while rejecting runtime enforcement claims.
4. Treat `V1-G4` as complete for static GuardianDecision/live approval path design-gate evidence, while rejecting runtime authority claims.
5. Treat `V1-G5` as complete for static provider/model routing contract and acceptance-test design evidence, while rejecting runtime routing claims.
6. Treat `V1-G6` as complete for static haptic intent metadata contract and shell fixture evidence, while rejecting device haptic behavior claims.
7. Treat `V1-G7` as complete for static first-shell integration evidence, while rejecting runtime parity claims.
8. Treat `V1-G8` as complete for static audit/evidence persistence contract and threat-model evidence, while rejecting durable runtime persistence claims.
9. Treat `V1-G9` as complete for static product release-boundary audit evidence, while rejecting V1 readiness, final freeze, and runtime export cleanup claims.
10. Treat `V1-G10` as complete for static implementation-gate evidence, while rejecting runtime implementation approval claims.
11. Treat the V1-G11 approval request and operator decision packet as ready for one valid operator choice in the packet's Decision Record section, while rejecting runtime implementation approval until explicitly recorded.

## Stop Conditions

Stop and request a new approval gate before any work that adds:

- `lima/` runtime changes
- `tests/support` runtime or harness helpers
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell modifications
- provider/model calls
- GuardianDecision runtime creation
- approval enforcement
- execution, dispatch, persistence, external calls, shell/browser/network/file mutation, robotics, haptic device behavior, or physical-world behavior

## Current Verdict

LIMA-AI-OS has a clearer V1 target, but it is not V1 product-ready.

`V1-G1` is accepted as source-backed local shell evidence.

`V1-G2` is complete as static docs/tests/fixtures-only typed bridge acceptance proof.

`V1-G3` is complete as static docs/tests/fixtures-only destructive edit/delete operator-approval contract proof.

`V1-G4` is complete as static docs/tests/fixtures-only real `GuardianDecision` and live approval path design-gate proof.

`V1-G5` is complete as static docs/tests/fixtures-only provider/model routing contract and acceptance-test design proof.

`V1-G6` is complete as static docs/tests/fixtures-only haptic intent metadata contract and shell fixture proof.

`V1-G7` is complete as static docs/tests/fixtures-only first-shell integration evidence. `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` proof packets have been delivered, audited, intaken by LIMA, and consolidated in `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md`.

`V1-G8` is complete as static docs/tests/fixtures-only audit/evidence persistence contract and threat-model evidence. Durable runtime audit persistence remains unimplemented and unapproved.

`V1-G9` is complete as static docs/tests/fixtures-only product release-boundary audit evidence. The release boundary is not passed. Runtime export cleanup, final API freeze, V1 product readiness, and production readiness remain unapproved.

`V1-G10` is complete as static docs/tests/fixtures-only minimum runtime implementation gate evidence. It defines the V1-G11 eligible files, rollback plan, acceptance-test obligations, and stop conditions. Runtime implementation remains unapproved.

The V1-G11 approval request and operator decision packet are ready for operator decision. They record the exact implementation scope for the typed request GuardianDecision preflight runtime slice, valid operator choices, required approval wording, and an empty Decision Record section, but approval is not recorded and runtime implementation remains unapproved.

The next smallest safe step is to record one valid operator choice in the V1-G11 operator decision packet's Decision Record section. If explicitly approved with the required wording, implement only the typed request GuardianDecision preflight runtime slice exactly inside the approved file-touch map, still without shell wiring, provider/model calls, durable persistence, haptic device behavior, robotics, runtime export cleanup, final freeze, or physical-world behavior.
