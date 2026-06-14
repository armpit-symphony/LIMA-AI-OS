# V1-G7 Sparkbot Integration Proof Intake

Date: 2026-06-14
LIMA branch: `intake-v1-g7-sparkbot-integration-proof-packet`
Source branch: `intake-v1-g7-sparkbot-shell-integration-proof-packet`
Source commit: `4153e1c51efa1fe03316913fc83192c87e8ffc33`
V1-G7 request branch: `v1-g7-first-shell-integration-proof-request-gate`
V1-G7 request commit: `fa3ad4af48c7c2b6286c9d3b789f5a7a2e85fda2`
API status: `CANDIDATE_ONLY`

## Sparkbot Packet Reviewed

- Repository: `armpit-symphony/Sparkbot`
- Local path reviewed: `C:\Users\limap\Sparkbot`
- Branch: `v1-g7-sparkbot-integration-proof-packet`
- Commit: `0bb99352a9b62cf1dc35e075c9f3a08054b6bef1`

## Files Reviewed

Sparkbot proof files:

- `docs/proof_packets/SPARKBOT_LIMA_V1_G7_INTEGRATION_PROOF_PACKET.md`
- `docs/audits/SPARKBOT_LIMA_V1_G7_INTEGRATION_PROOF_AUDIT.md`
- `tests/fixtures/sparkbot_lima_v1_g7_integration_proof_packet.json`
- `tests/test_sparkbot_lima_v1_g7_integration_proof_packet.py`

Sparkbot supporting evidence named by the packet:

- `AGENTS.md`
- `docs/capabilities.md`
- `docs/PUBLIC_RELEASE_CAPABILITY_MODEL.md`
- `docs/guardian-spine.md`
- `docs/LIMA_RUNTIME_ALIGNMENT_NOTES.md`
- `backend/app/services/guardian/policy.py`
- `backend/app/services/guardian/pending_approvals.py`
- `backend/app/services/guardian/spine.py`
- `backend/app/services/model_seats.py`
- `backend/app/api/routes/chat/rooms.py`
- `backend/app/api/routes/chat/llm.py`
- `backend/app/api/routes/chat/dashboard.py`
- `backend/app/api/routes/chat/tools.py`
- `backend/app/api/routes/chat/mcp.py`
- `backend/app/services/mcp_registry.py`
- `backend/app/services/mcp_runs.py`
- `frontend/src/pages/SparkbotDmPage.tsx`
- `frontend/src/components/chat/MessageBubble.tsx`
- `frontend/src/components/chat/ChatWindow.tsx`
- `frontend/src/lib/sparkbotControls.ts`
- `frontend/src/lib/mcpRegistry.ts`
- `frontend/src/lib/spine.ts`

LIMA request and prior intake files:

- `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST.md`
- `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_AUDIT_CRITERIA.md`
- `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g7_first_shell_integration_proof_request.json`
- `docs/V1_G7_SPARKBOT_SHELL_INTEGRATION_PROOF_INTAKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g7_sparkbot_shell_integration_proof_intake.json`

## Validation Reported By Sparkbot

Sparkbot reported:

- `cmd /c "python3 --version || python --version"`
  - Passed: Python 3.12.10, with known trailing Windows environment message.
- `cmd /c "python3 -m pytest -q tests/test_sparkbot_lima_v1_g7_integration_proof_packet.py || python -m pytest -q tests/test_sparkbot_lima_v1_g7_integration_proof_packet.py"`
  - Passed: 9 passed in 0.05s, with known trailing Windows environment message.
- `cmd /c "python3 -m json.tool tests/fixtures/sparkbot_lima_v1_g7_integration_proof_packet.json || python -m json.tool tests/fixtures/sparkbot_lima_v1_g7_integration_proof_packet.json"`
  - Passed: JSON parsed and printed, with known trailing Windows environment message.
- `git diff --check`
  - Passed: clean.

## What Sparkbot Proved

Sparkbot proved source-backed behavior-reference evidence for the V1-G7 request:

- It provided the requested proof packet, audit, fixture, and static test.
- It evaluated all required response states.
- It evaluated required packet statuses.
- It preserved required kernel-status mapping guidance.
- It kept haptics shell-owned and did not claim LIMA owns haptic device behavior.
- It proved Sparkbot-owned streaming/typing/received/done/error behavior as source-backed reference evidence.
- It proved Sparkbot-owned approval and policy-decision behavior as source-backed reference evidence.
- It proved Sparkbot-owned provider/model routing behavior as source-backed reference evidence.
- It proved Sparkbot-owned audit/spine/timeline evidence paths as source-backed reference evidence.
- It proved destructive edit/delete behavior requires confirmation, privileged approval, or blocking in Sparkbot's own runtime.
- It classified public Robo behavior as preview-only by default and private bridge behavior as separately gated.
- It avoided raw natural-language-to-tool execution bypass claims.
- It avoided LIMA runtime wiring and did not require runtime export cleanup or final freeze.

## What Sparkbot Did Not Prove

Sparkbot did not prove:

- live LIMA runtime output consumption
- live Sparkbot-on-LIMA runtime parity
- LIMA runtime `GuardianDecision` authority
- LIMA approval enforcement
- LIMA provider/model runtime routing
- LIMA durable audit persistence
- LIMA haptic device implementation
- LIMA shell rendering
- LIMA connector, file, browser, network, device, robotics, or physical-world behavior
- runtime export cleanup readiness
- final API freeze readiness
- V1 product readiness
- production readiness

Sparkbot has real runtime behavior in its own repo. LIMA can use that as reference evidence, but this intake does not migrate or wire that behavior into LIMA.

## Required Shell Response States

Source-backed Sparkbot states:

- `received`
- `thinking`
- `preview_ready`
- `blocked`
- `needs_approval`
- `completed`
- `failed_safe`

Docs/fixture-only states:

- `deferred`

Missing required states:

- none

Notes:

- `thinking` is source-backed by Sparkbot token streaming and frontend typing/progress UI.
- `needs_approval` is source-backed by Sparkbot `confirm_required`, `privileged_required`, persistent approvals, and dashboard approval paths.
- `deferred` is represented by planned/deferred concepts and MCP planned status, but not by a dedicated Sparkbot shell response-state label.

## Packet Statuses And Kernel Mapping

Accepted packet status coverage:

- `preview_only`
- `explain_plan`
- `blocked`
- `completed`
- `deferred`

Accepted mapping coverage:

- `proposed -> preview_only`
- `needs_review -> explain_plan`
- `blocked -> blocked`
- `completed -> completed`
- `deferred -> deferred`

The added `completed` and `deferred` mappings are accepted as reference mappings only and do not change LIMA's required mapping minimums.

## Haptics Result

- Shell owns haptics: yes.
- LIMA owns haptic device behavior: no.
- Sparkbot haptic device behavior added: no.
- Device haptic command added: no.
- Sparkbot haptic intent metadata support: not present in source evidence.

This is acceptable for static intake because LIMA V1-G6 keeps haptic rendering and device feedback shell-owned. LIMA must not claim device-haptic authority from this packet.

## Intake Verdict

LIMA can accept this Sparkbot packet as static V1-G7 behavior-reference evidence.

LIMA cannot treat it as live LIMA runtime parity.

This intake does not change LIMA API status. API status remains `CANDIDATE_ONLY`.

This intake does not approve runtime export cleanup.

This intake does not approve final API freeze.

This intake does not complete V1-G7 because `Arc-Bot-shell` still needs a V1-G7 packet and LIMA intake audit.

## Recommended Next Safe Step

Continue V1-G7 by requesting or normalizing the `Arc-Bot-shell` V1-G7 proof packet, then create a separate LIMA intake audit for it. Do not proceed to consolidated V1-G7 closeout, runtime export cleanup, final freeze, or runtime wiring until all three first-shell packets have been delivered and audited.
