# V1-G12 Sparkbot LIMA Consumer Proof Intake

Date: 2026-06-14
LIMA branch: `v1-g12-sparkbot-lima-consumer-proof-intake`
Source branch: `v1-g11-runtime-request-decision-gate`
Source commit: `50425b41bb64cca8174c6fc21983cf44f8c41e6b`
API status: `CANDIDATE_ONLY`

## Sparkbot Packet Reviewed

- Repository: `https://github.com/sparkpit-labs/Sparkbot`
- Local path reviewed: `C:\Users\limap\Sparkbot`
- Branch: `proof-sparkbot-shell-lima-consumer-packet`
- Commit: `842a6757a2fbdc87451042eec465eb76be5bea80`

The local Sparkbot checkout was present on the reported branch and commit. Two unrelated untracked files were present under `scripts/` and were not used as evidence or modified.

## Files Reviewed

Sparkbot proof files:

- `docs/proof_packets/SPARKBOT_SHELL_LIMA_CONSUMER_PROOF_PACKET.md`
- `docs/audits/SPARKBOT_SHELL_LIMA_CONSUMER_PACKET_AUDIT.md`
- `docs/proof_packets/sparkbot_shell_lima_consumer_packet.json`

LIMA context files:

- `AGENTS.md`
- `docs/CURRENT_PROJECT_STATE.md`
- `docs/LIMA_LONG_RANGE_ROADMAP.md`
- `README.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/EXTRACTION_PLAN.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `docs/V1_G7_SPARKBOT_INTEGRATION_PROOF_INTAKE.md`
- `docs/V1_G7_SPARKBOT_INTEGRATION_PROOF_INTAKE_AUDIT.md`
- `docs/V1_G7_SPARKBOT_INTEGRATION_PROOF_INTAKE_CLOSEOUT.md`

## Validation Reported By Sparkbot

Sparkbot reported:

- `python3 --version`
  - Failed in that environment: Python 3 shim not available.
- `python --version`
  - Passed: Python 3.12.10.
- `git diff --check`
  - Passed: clean.
- `npm run lint`
  - Failed because `bun` is not installed in that environment.
- `python -m pytest -q tests/test_sparkbot_lima_v1_g7_integration_proof_packet.py`
  - Passed: 9 passed in 0.04s.

## What Sparkbot Proved

Sparkbot proved substantial static/reference evidence for future LIMA consumer planning:

- The proof packet, audit, and machine-readable summary JSON are present.
- Sparkbot is a production-oriented fullstack shell with API-backed chat, workstation, meeting, command center, controls, Guardian, approval, audit/spine, model-seat, and connector/tool surfaces.
- Sparkbot can provide route-level, component-level, conversation, dashboard, approval queue, meeting, model-seat, history, and event evidence as preview input.
- Candidate mappings are documented for `ConsumerRequest`, `HumanInput`, `TaskIntent`, `TypedIntentEnvelope`, `CandidatePreview`, `RuntimeStateSnapshot`, `GuardianDecision`, and audit/spine concepts.
- CandidatePreview examples include `embodiment_profile`.
- Allowed mock-safe statuses are represented as `preview_only`, `explain_plan`, `blocked`, and `deferred`.
- Protected categories that must stay Guardian-gated are explicitly listed, including provider calls, connector sends, shell commands, browser writes, secret handling, file mutation, robot/IoT physical execution, memory writeback, and audit integrity persistence.

This is valid static consumer-reference evidence for LIMA planning.

## What Sparkbot Did Not Prove

Sparkbot did not prove:

- live Sparkbot as a LIMA runtime consumer
- a live `ConsumerRequest` intake endpoint in Sparkbot for LIMA
- a shared `HumanInput` intake transform layer
- a shared `TaskIntent` or `TypedIntentEnvelope` adapter
- a stable `CandidatePreview` publication API
- a canonical `RuntimeStateSnapshot` serializer for shell state
- LIMA-owned `GuardianDecision` authority in current Sparkbot paths
- LIMA approval enforcement
- LIMA provider/model runtime routing
- LIMA durable audit/evidence persistence
- LIMA connector, tool, browser, file, network, device, robotics, or physical-world behavior
- LIMA runtime export cleanup readiness
- final API freeze readiness
- V1 product readiness or production readiness

## Consumer Statuses

Source-backed Sparkbot surfaces support these proposed candidate statuses as static/reference mapping evidence:

- `preview_only`
- `explain_plan`
- `blocked`
- `deferred`

These statuses are acceptable as candidate mapping evidence only. They are not live LIMA runtime parity.

## Top Blockers

Sparkbot and LIMA should treat the following as still open before Sparkbot can be accepted as a live LIMA-runtime consumer:

1. No live `ConsumerRequest` intake contract in the shell.
2. No shared intent adapter for `TaskIntent` / `TypedIntentEnvelope`.
3. No canonical shell-to-LIMA snapshot/event contract for `RuntimeStateSnapshot`.
4. No LIMA-native `GuardianDecision` authority in current Sparkbot paths.
5. Current high-risk actions still route through Sparkbot-native runtime paths.

## Intake Verdict

LIMA can accept the Sparkbot packet as static consumer-reference evidence.

LIMA cannot treat the packet as live LIMA runtime consumer parity.

This intake does not change LIMA API status. API status remains `CANDIDATE_ONLY`.

This intake does not approve runtime export cleanup.

This intake does not approve final API freeze.

This intake does not approve product readiness or production readiness.

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added by this intake: no.
- `lima/` runtime files changed by this intake: no.
- Runtime exports changed by this intake: no.
- Sparkbot touched by this intake: no.
- Sparkbot_shell touched by this intake: no.
- Arc-Bot-shell touched by this intake: no.
- Consumer integration added by this intake: no.
- Provider/model routing added by this intake: no.
- HumanInput bridge activated by this intake: no.
- Connector, browser, file, network, device, robotics, or physical-world behavior added by this intake: no.
- Product readiness claimed: no.

## Recommended Next Safe Step

Recommended option: `V1-G13`.

Open a separate approval gate for a strict, non-execution LIMA Intake Adapter on Sparkbot surfaces. That gate should only propose accepting preview-safe `ConsumerRequest` records, normalizing them to `TaskIntent` / `TypedIntentEnvelope`, emitting `CandidatePreview` in `preview_only`, `explain_plan`, `blocked`, or `deferred`, and returning a LIMA-owned `GuardianDecision` before any dispatch.

Do not implement that adapter from this intake packet alone.
