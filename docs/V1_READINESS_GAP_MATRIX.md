# V1 Readiness Gap Matrix

This matrix turns the V1 product target into an implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, GuardianDecision creation, approval enforcement, persistence, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Current branch: `v1-g7-first-shell-integration-proof-request-gate`
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
| `V1-G7` | First-shell integration proof | `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST.md` and audit criteria define required proof packets for `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`; no shell proof packets have been accepted yet | `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` each prove they can consume LIMA contract outputs safely | Request all three shell proof packets, then perform one LIMA intake audit per packet before consolidated closeout | Runtime wiring requires later approval |
| `V1-G8` | Audit/evidence persistence | Static audit/evidence lineage exists; durable audit persistence is not implemented | Consequential actions produce durable, redacted, queryable evidence lineage | Audit persistence design, storage contract, threat model, then runtime gate | Yes |
| `V1-G9` | Product release boundary | Current package remains candidate/proof-stage | V1 release gates, compatibility freeze, shell compatibility evidence, and rollback proof all pass | V1 release readiness audit after blockers close | No implementation by audit alone |

## Recommended Order

1. Treat `V1-G1` as accepted for source-backed local shell `thinking` evidence, while rejecting live runtime parity claims.
2. Treat `V1-G2` as complete for static typed bridge acceptance proof, while rejecting runtime parity claims.
3. Treat `V1-G3` as complete for static destructive edit/delete approval contract evidence, while rejecting runtime enforcement claims.
4. Treat `V1-G4` as complete for static GuardianDecision/live approval path design-gate evidence, while rejecting runtime authority claims.
5. Treat `V1-G5` as complete for static provider/model routing contract and acceptance-test design evidence, while rejecting runtime routing claims.
6. Treat `V1-G6` as complete for static haptic intent metadata contract and shell fixture evidence, while rejecting device haptic behavior claims.
7. Treat `V1-G7` request gate as complete, then require all three shell proof packets before compatibility freeze.
8. Finish `V1-G8` and `V1-G9` before claiming V1 product readiness.

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

`V1-G7` request gate is complete as docs/tests/fixtures-only proof request and audit criteria. V1-G7 itself remains open until `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` proof packets are delivered and audited by LIMA.

The next smallest safe step is `V1-G7D`: request all three first-shell proof packets in parallel, then create one LIMA intake/audit lane per returned packet, still without LIMA runtime behavior, shell wiring, provider/model calls, approval enforcement, persistence, haptic device behavior, robotics, or physical-world behavior until a later explicit implementation approval.
