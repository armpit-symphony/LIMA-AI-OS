# V1-G7 Sparkbot Integration Proof Intake Audit

Date: 2026-06-14
Audit target: `Sparkbot`
Packet branch: `v1-g7-sparkbot-integration-proof-packet`
Packet commit: `0bb99352a9b62cf1dc35e075c9f3a08054b6bef1`
LIMA API status: `CANDIDATE_ONLY`

## Audit Verdict

Verdict: `accept_static_behavior_reference_evidence_only`

Sparkbot satisfies the V1-G7 request gate for static behavior-reference evidence. It is the strongest current source for first-shell behavior posture, but it does not satisfy live LIMA runtime parity or V1 product readiness.

## Required Audit Questions

| Question | Answer |
| --- | --- |
| Did Sparkbot provide the requested proof packet? | Yes. |
| Did Sparkbot provide the requested audit? | Yes. |
| Did Sparkbot provide machine-readable fixture evidence? | Yes. |
| Did Sparkbot run and report validation commands? | Yes. |
| Did Sparkbot evaluate all required response states? | Yes. |
| Did Sparkbot evaluate packet/kernel status mappings? | Yes. |
| Did Sparkbot preserve haptics as shell-owned? | Yes. |
| Did Sparkbot avoid claiming LIMA owns haptic device behavior? | Yes. |
| Did Sparkbot prove destructive edit/delete requires operator approval or is blocked? | Yes, as Sparkbot source-backed runtime behavior-reference evidence. |
| Did Sparkbot classify approval as real, preview-only, docs-only, or missing? | Yes: real Sparkbot runtime enforcement, not LIMA enforcement. |
| Did Sparkbot classify `GuardianDecision` authority? | Yes: Sparkbot policy decisions are source-backed; LIMA runtime `GuardianDecision` remains missing. |
| Did Sparkbot classify provider/model routing? | Yes: real Sparkbot runtime provider/model routing, not LIMA routing. |
| Did Sparkbot constrain provider/model routing where applicable? | Yes: route context, model seats, provider/auth posture, Token Guardian route evidence, and audit posture are source-backed. |
| Did Sparkbot classify audit/evidence lineage? | Yes: Sparkbot audit, pending approval, dashboard timeline, and Guardian Spine evidence are source-backed; LIMA audit persistence remains missing. |
| Did Sparkbot avoid raw natural-language-to-tool execution shortcuts? | Yes. Tool calls flow through Sparkbot tool catalogue and Guardian policy gates. |
| Did Sparkbot avoid unsafe connector/file/browser/network/device/robotics claims? | Yes. Runtime surfaces are classified as Guardian-gated, preview-only, private-gated, or outside LIMA scope. |
| Did Sparkbot avoid LIMA runtime wiring? | Yes. |
| Did Sparkbot avoid requiring unapproved LIMA runtime exports? | Yes. |
| Did Sparkbot avoid importing/copying Sparkbot code into LIMA? | Yes. |
| Is the proof acceptable as static shell integration evidence? | Yes. |
| Is the proof insufficient for live runtime parity? | Yes. |

## What LIMA Should Accept

LIMA should accept:

- Sparkbot proof packet delivery for V1-G7.
- Sparkbot source-backed response-state evidence for `received`, `thinking`, `preview_ready`, `blocked`, `needs_approval`, `completed`, and `failed_safe`.
- Sparkbot docs/fixture-only classification for `deferred`.
- Sparkbot source-backed approval and policy decision posture as reference behavior.
- Sparkbot source-backed provider/model routing as reference behavior.
- Sparkbot source-backed audit/spine/timeline posture as reference behavior.
- Sparkbot destructive edit/delete approval posture.
- Sparkbot public Robo preview/private bridge classification.
- Sparkbot no-raw-natural-language-to-tool-bypass posture.
- Haptics remain shell-owned and absent from Sparkbot device behavior.

## What LIMA Should Reject

LIMA should reject:

- live LIMA runtime parity
- Sparkbot-on-LIMA runtime parity
- LIMA runtime `GuardianDecision` authority
- LIMA approval enforcement
- LIMA provider/model routing
- LIMA provider/model calls
- LIMA audit persistence
- LIMA haptic device behavior
- LIMA connector/file/browser/network/device/robotics behavior
- runtime export cleanup approval
- final API freeze
- V1 product readiness
- production readiness

## State Coverage Audit

Source-backed:

- `received`
- `thinking`
- `preview_ready`
- `blocked`
- `needs_approval`
- `completed`
- `failed_safe`

Docs/fixture-only:

- `deferred`

Missing:

- none

## Status Mapping Audit

Required mappings are present:

- `proposed -> preview_only`
- `needs_review -> explain_plan`
- `blocked -> blocked`

Additional reference mappings:

- `completed -> completed`
- `deferred -> deferred`

## Haptics Audit

Pass:

- haptics remain shell-owned
- LIMA device haptic ownership remains false
- no haptic device behavior was added
- no device vibration command was added

Sparkbot does not currently prove haptic intent metadata support. That is acceptable for this intake because LIMA must not own shell haptic rendering or device feedback.

## Boundary Audit

Pass:

- no LIMA runtime behavior added
- no `lima/` runtime files changed
- no `tests/support` changes
- no runtime exports changed
- no Sparkbot wiring added to LIMA
- no Sparkbot import added to LIMA
- no Sparkbot code copied to LIMA
- no provider/model calls added to LIMA
- no approval enforcement added to LIMA
- no execution, dispatch, or persistence added
- no browser/file/network/device/robotics behavior added
- no physical-world behavior added
- runtime export cleanup remains unapproved
- final freeze remains unapproved

## Follow-Up To Request From Sparkbot

No further Sparkbot static proof is required for this V1-G7 packet at this time.

Future runtime follow-ups should wait for separate implementation gates and should be narrow: LIMA runtime parity tests for typed bridge, GuardianDecision, approval enforcement, provider/model routing, and audit persistence.

## V1-G7 Status After This Audit

Sparkbot_shell: accepted as static shell integration evidence.

Sparkbot: accepted as static behavior-reference evidence.

Arc-Bot-shell: not yet delivered or audited for V1-G7.

Consolidated V1-G7 closeout: not complete.
