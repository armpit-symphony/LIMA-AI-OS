# V1-G12 Sparkbot LIMA Consumer Proof Closeout

Date: 2026-06-14
Branch: `v1-g12-sparkbot-lima-consumer-proof-intake`
API status: `CANDIDATE_ONLY`

## Intake Verdict

Recommended verdict: `accept_static_consumer_reference_evidence_only`

Sparkbot delivered a useful LIMA consumer proof packet. LIMA can accept it as static consumer-reference evidence and should reject live runtime parity claims.

## Accepted Evidence

- Proof packet delivered.
- Audit delivered.
- Machine-readable summary JSON delivered.
- Sparkbot validation was reported.
- Sparkbot static/reference surfaces are documented for chat, workstation, meeting, command center, controls, Guardian, approval, audit/spine, memory/history, model-seat, provider/model routing, and tool/action paths.
- Candidate mappings are documented for `ConsumerRequest`, `HumanInput`, `TaskIntent`, `TypedIntentEnvelope`, `CandidatePreview`, `RuntimeStateSnapshot`, `GuardianDecision`, and audit/spine concepts.
- CandidatePreview examples include `embodiment_profile`.
- Candidate statuses are limited to `preview_only`, `explain_plan`, `blocked`, and `deferred`.
- Protected provider/model, connector, browser, file, network, device, robotics, physical-world, secret, memory, and audit categories are explicitly Guardian-gated or blocked until LIMA contracts exist.
- Sparkbot is substantial behavior-reference evidence for LIMA planning.

## Rejected / Non-Accepted Claims

Do not accept this packet as proof of:

- live Sparkbot-on-LIMA runtime parity
- live Sparkbot LIMA runtime consumer status
- live `ConsumerRequest` intake in the shell
- live shared intent adapter behavior
- canonical live `RuntimeStateSnapshot` export
- LIMA-native `GuardianDecision` authority in current Sparkbot paths
- LIMA approval enforcement
- LIMA provider/model runtime routing
- LIMA provider/model calls
- LIMA connector, tool, file, browser, network, device, robotics, or physical-world behavior
- durable LIMA audit/evidence persistence
- runtime export cleanup approval
- final API freeze
- V1 product readiness
- production readiness

## Remaining Blockers

- no live `ConsumerRequest` intake contract in shell
- no shared intent adapter for `TaskIntent` / `TypedIntentEnvelope`
- no canonical shell-to-LIMA snapshot/event contract for `RuntimeStateSnapshot`
- no LIMA-native `GuardianDecision` authority in current paths
- high-risk actions still route through Sparkbot-native runtime paths
- no live approval enforcement by LIMA
- no provider/model/connector runtime owned by LIMA
- no audit persistence owned by LIMA
- no production behavior

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added by this intake: no.
- `lima/` runtime files changed by this intake: no.
- Runtime exports changed by this intake: no.
- Sparkbot changed by this intake: no.
- Sparkbot_shell changed by this intake: no.
- Arc-Bot-shell changed by this intake: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/file/network action behavior added: no.
- External sends added: no.
- Device, robotics, or physical-world behavior added: no.
- Product readiness claimed: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Choices

Option `V1-G12A`: Accept Sparkbot proof as static consumer-reference evidence and keep LIMA `CANDIDATE_ONLY`.

Option `V1-G13`: Open a separate approval gate for a strict, non-execution Sparkbot LIMA Intake Adapter. The gate must define exact file scope, test scope, rollback, audit proof, and stop conditions before any implementation.

Option `V1-G14`: Continue toward a separate runtime export cleanup proposal gate, still without consumer integration.

## Recommendation

Recommended: `V1-G13`.

The Sparkbot packet identifies a concrete next safe lane, but it does not approve implementation. The next smallest safe step is an explicit gate for a strict non-execution intake adapter that accepts only preview-safe `ConsumerRequest` records, normalizes metadata to `TaskIntent` / `TypedIntentEnvelope`, emits `CandidatePreview` in `preview_only`, `explain_plan`, `blocked`, or `deferred`, and returns a LIMA-owned `GuardianDecision` before any dispatch.
