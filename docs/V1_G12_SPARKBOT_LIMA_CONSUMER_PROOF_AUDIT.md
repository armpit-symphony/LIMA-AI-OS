# V1-G12 Sparkbot LIMA Consumer Proof Audit

Date: 2026-06-14
Audit target: `Sparkbot`
Packet branch: `proof-sparkbot-shell-lima-consumer-packet`
Packet commit: `842a6757a2fbdc87451042eec465eb76be5bea80`
LIMA API status: `CANDIDATE_ONLY`

## Audit Verdict

Verdict: `accept_static_consumer_reference_evidence_only`

Sparkbot delivered the requested consumer proof packet artifacts and provided useful evidence for future LIMA consumer intake design. The packet is insufficient for live LIMA-runtime consumer parity, API freeze, runtime export cleanup, product readiness, or production readiness.

## Required Audit Questions

| Question | Answer |
| --- | --- |
| Did Sparkbot provide the proof packet? | Yes. |
| Did Sparkbot provide the audit? | Yes. |
| Did Sparkbot provide machine-readable fixture evidence? | Yes. |
| Did Sparkbot report validation commands? | Yes. |
| Did Sparkbot document implemented, mocked, placeholder, incomplete, and missing areas? | Yes. |
| Did Sparkbot identify human-input surfaces for future LIMA mapping? | Yes. |
| Did Sparkbot identify chat, workstation, meeting, and model-seat surfaces? | Yes. |
| Did Sparkbot identify memory, note, audit, event, and history surfaces? | Yes. |
| Did Sparkbot identify Guardian and approval surfaces? | Yes. |
| Did Sparkbot identify provider/model routing and tool/action surfaces as reference evidence? | Yes. |
| Did Sparkbot identify protected categories that must stay Guardian-gated? | Yes. |
| Did Sparkbot propose mappings to `ConsumerRequest`, `HumanInput`, `TaskIntent`, `TypedIntentEnvelope`, `CandidatePreview`, `RuntimeStateSnapshot`, `GuardianDecision`, and audit/spine concepts? | Yes. |
| Did Sparkbot include `embodiment_profile` on CandidatePreview examples? | Yes. |
| Did Sparkbot prove live LIMA runtime consumer wiring? | No. |
| Did Sparkbot prove live `ConsumerRequest` intake in the shell? | No. |
| Did Sparkbot prove a shared intent adapter for `TaskIntent` / `TypedIntentEnvelope`? | No. |
| Did Sparkbot prove canonical `RuntimeStateSnapshot` shell-to-LIMA serialization? | No. |
| Did Sparkbot prove LIMA-native `GuardianDecision` authority in current paths? | No. |
| Did Sparkbot prove high-risk actions route through LIMA instead of Sparkbot-native runtime paths? | No. |
| Did Sparkbot avoid unsafe provider/model/tool/file/network/browser/device/robotics claims as LIMA behavior? | Yes. |
| Is the proof acceptable as static consumer-reference evidence? | Yes. |
| Is the proof insufficient for live Sparkbot-on-LIMA parity? | Yes. |

## What LIMA Should Accept

LIMA should accept:

- Sparkbot proof packet delivery.
- Sparkbot audit delivery.
- Sparkbot machine-readable summary JSON delivery.
- Sparkbot validation report, with the noted environment failures.
- Sparkbot source-backed inventory of chat, workstation, meeting, command center, controls, Guardian, approval, audit/spine, model-seat, provider/model, connector, and tool/action surfaces.
- Static candidate mappings to `ConsumerRequest`, `HumanInput`, `TaskIntent`, `TypedIntentEnvelope`, `CandidatePreview`, `RuntimeStateSnapshot`, `GuardianDecision`, and audit/spine concepts.
- `embodiment_profile` presence on CandidatePreview examples.
- Candidate status evidence for `preview_only`, `explain_plan`, `blocked`, and `deferred`.
- The conclusion that Sparkbot is substantial behavior-reference evidence, not a live LIMA runtime consumer.

## What LIMA Should Reject

LIMA should reject:

- live LIMA runtime consumer parity
- Sparkbot-on-LIMA runtime parity
- live `ConsumerRequest` intake in Sparkbot
- live shared intent adapter behavior
- canonical live shell-to-LIMA `RuntimeStateSnapshot` export
- LIMA-native `GuardianDecision` authority in current Sparkbot paths
- LIMA approval enforcement
- LIMA provider/model runtime routing
- LIMA provider/model calls
- LIMA connector, tool, file, browser, network, device, robotics, or physical-world behavior
- LIMA durable audit/evidence persistence
- runtime export cleanup approval
- final API freeze
- V1 product readiness
- production readiness

## Blocker Audit

The top blockers remain:

1. No live `ConsumerRequest` intake contract in the shell.
2. No shared intent adapter for `TaskIntent` / `TypedIntentEnvelope`.
3. No canonical shell-to-LIMA snapshot/event contract for `RuntimeStateSnapshot`.
4. No LIMA-native `GuardianDecision` authority in current paths.
5. Current high-risk actions still route through Sparkbot-native runtime paths.

## Boundary Audit

Pass:

- no LIMA runtime behavior added by this intake
- no `lima/` runtime files changed by this intake
- no runtime exports changed by this intake
- no Sparkbot wiring added to LIMA
- no Sparkbot import added to LIMA
- no Sparkbot code copied to LIMA
- no Sparkbot_shell changes
- no Arc-Bot-shell changes
- no provider/model routing added to LIMA
- no HumanInput bridge activated
- no connector behavior added
- no browser/file/network action behavior added
- no external sends added
- no device, robotics, or physical-world behavior added
- no haptic device behavior added
- runtime export cleanup remains unapproved
- final API freeze remains unapproved
- product readiness and production readiness remain unapproved

## Follow-Up To Request

Request a separate LIMA-side implementation approval gate for a strict non-execution Sparkbot intake adapter.

The follow-up gate should require exact file scope, rollback proof, validation proof, forbidden-surface scans, and tests proving:

- only preview-safe `ConsumerRequest` inputs are accepted
- normalized intent remains metadata until LIMA review
- `CandidatePreview` status is limited to `preview_only`, `explain_plan`, `blocked`, or `deferred`
- LIMA-owned `GuardianDecision` is returned before dispatch
- blocked and deferred states are non-dispatching
- provider/model/tool/browser/file/network/device/robotics/physical-world claims fail closed

Do not treat this audit as approval to implement that adapter.
