# V1 Readiness Gap Matrix

This matrix turns the V1 product target into an implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, GuardianDecision creation, approval enforcement, persistence, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Current branch: `phase-48-2-concrete-implementation-design-review`
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Current product status: not V1-ready
- Current implementation approval: not granted

## Readiness Matrix

| ID | Gap | Current evidence | V1-ready requirement | Recommended lane | Runtime approval needed |
| --- | --- | --- | --- | --- | --- |
| `V1-G0` | V1 target clarity | `docs/V1_PRODUCT_READINESS_TARGET.md` exists and is static-tested | Keep first-shell target, operator approval rule, haptics ownership, and future runtime capabilities explicit | Complete in current branch | No |
| `V1-G1` | Sparkbot_shell `thinking` / progress proof | LIMA accepted Sparkbot_shell commit `36d697bf875a44dbafa41fc841ded86437917627` in `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md` as source-backed local shell evidence | Source-backed shell evidence for in-band thinking/progress state | Complete as source-backed local shell evidence; live streaming parity remains out of scope | No LIMA runtime approval |
| `V1-G2` | Typed bridge acceptance proof | Phase 44-48 design artifacts exist; Phase 48.2 names candidate future tests but does not create them | Executable acceptance tests proving source request metadata, typed IntentEnvelope candidate metadata, and Guardian request metadata fail closed without authority | Separately approved typed bridge acceptance-test implementation lane | No runtime approval if kept tests/fixtures-only |
| `V1-G3` | Destructive edit/delete approval contract | V1 target records that edits/deletes/overwrites require operator approval | Contract and tests proving destructive action classes cannot be marked approved without explicit operator approval metadata | Destructive-action approval contract design and static acceptance tests | Later runtime approval required for enforcement |
| `V1-G4` | Real GuardianDecision and live approval path | Existing fake/test-only GuardianDecision artifacts are not production authority | Runtime GuardianDecision path that distinguishes allow, confirm, deny, privileged, expired, revoked, and blocked outcomes before consequential action | GuardianDecision runtime design gate, then separately approved narrow runtime slice | Yes |
| `V1-G5` | Provider/model routing | Sparkbot docs prove reference behavior; LIMA has no provider/model runtime routing | Model routing constrained by Guardian, shell tool-pack scope, secret policy, and audit/evidence rules | Provider/model routing contract and acceptance-test design before implementation | Yes for runtime routing |
| `V1-G6` | Haptic intent metadata | Haptics are accepted as shell-owned future UX requirement; no LIMA haptic intent contract exists | LIMA may emit non-device-specific haptic intent metadata while shells own rendering/device feedback | Haptic intent contract design and shell fixture proof | No device implementation in LIMA |
| `V1-G7` | First-shell integration proof | No shell runtime wiring is approved; Sparkbot is reference only | `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` each prove they can consume LIMA contract outputs safely | Per-shell proof packets and LIMA intake audits | Runtime wiring requires later approval |
| `V1-G8` | Audit/evidence persistence | Static audit/evidence lineage exists; durable audit persistence is not implemented | Consequential actions produce durable, redacted, queryable evidence lineage | Audit persistence design, storage contract, threat model, then runtime gate | Yes |
| `V1-G9` | Product release boundary | Current package remains candidate/proof-stage | V1 release gates, compatibility freeze, shell compatibility evidence, and rollback proof all pass | V1 release readiness audit after blockers close | No implementation by audit alone |

## Recommended Order

1. Treat `V1-G1` as accepted for source-backed local shell `thinking` evidence, while rejecting live runtime parity claims.
2. Complete `V1-G2` as the smallest LIMA-side executable proof step, if separately approved.
3. Design and test `V1-G3` before any runtime approval path so destructive edits/deletes cannot be normalized as ordinary writes.
4. Move into `V1-G4` and `V1-G5` only after file scope, rollback proof, and acceptance tests are explicit.
5. Add `V1-G6` haptic intent metadata as a shell-contract lane, not device implementation.
6. Require `V1-G7` shell proof packets before compatibility freeze.
7. Finish `V1-G8` and `V1-G9` before claiming V1 product readiness.

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

The next smallest safe step is `V1-G2`: typed bridge acceptance proof, still without LIMA runtime behavior, shell wiring, provider/model calls, GuardianDecision authority, approval enforcement, persistence, haptic device behavior, robotics, or physical-world behavior.
