# V1 Runtime Readiness Rollup Through G28

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g28`
API status: `CANDIDATE_ONLY`

## Required Verdicts

- V1 runtime authority chain: `CANDIDATE_ONLY`
- Consumer proof packet audit intake: `CANDIDATE_ONLY`
- Live approval evidence/capture metadata: `CANDIDATE_ONLY`
- Provider/model routing authority metadata: `CANDIDATE_ONLY`
- Consumer integration compatibility/freeze metadata: `CANDIDATE_ONLY`
- Final public API freeze docs/tests/fixtures: `CANDIDATE_ONLY`
- Consumer integration proof-to-import dry-run metadata: `CANDIDATE_ONLY`
- First consumer import-plan evidence packets: `CANDIDATE_ONLY`
- First consumer repo patch-preview evidence: `CANDIDATE_ONLY`
- First consumer repository edit: `CANDIDATE_ONLY`
- First consumer frozen API import-smoke: `CANDIDATE_ONLY`
- Runtime export cleanup: `CANDIDATE_ONLY`
- Live consumer imports/calls: `NOT_APPROVED`
- Consumer integration: `BLOCKED`
- Live provider/model calls: `NOT_APPROVED`
- Secret lookup and credential access: `NOT_APPROVED`
- Model dispatch and fallback execution: `NOT_APPROVED`
- Actual runtime file edit/delete/mutation execution: `NOT_APPROVED`
- Connector/browser/network authority: `NOT_APPROVED`
- Physical-world readiness: `BLOCKED`
- Product readiness: `NOT_READY`

## Current Accepted Evidence

- V1-G11 through V1-G17: local non-executing runtime request, approval, policy, and preview metadata slices.
- V1-G18: consumer proof packet audit-intake metadata.
- V1-G19: live approval evidence/capture metadata.
- V1-G20: provider/model routing authority metadata.
- V1-G21: consumer integration compatibility/freeze metadata.
- V1-G22: final public API freeze docs/tests/fixtures for current candidate import surfaces.
- V1-G23: consumer integration proof-to-import dry-run metadata validator.
- V1-G24: Sparkbot and Arc-Bot-shell import-plan evidence packets validated through V1-G23.
- V1-G25: Sparkbot and Arc-Bot-shell patch-preview evidence packets linked to V1-G24 import-plan evidence.
- V1-G26: Sparkbot and Arc-Bot-shell static consumer repository proof edits, recorded by LIMA by commit hash.
- V1-G27: Sparkbot and Arc-Bot-shell test-only frozen API import-smoke evidence, recorded by LIMA by commit hash.
- V1-G28: LIMA adapter runtime export cleanup for existing V1-G23 import dry-run symbols.

All accepted evidence remains proof or metadata unless a later exact approval gate grants additional authority.

## V1-G28 Status

V1-G28 implemented the runtime export cleanup slice.

Accepted evidence:

- exact `Approve-V1-G28` decision was recorded
- `lima/adapters/__init__.py` was the only approved runtime file changed
- `V1ConsumerImportDryRunError` is exported through `lima.adapters.__all__`
- `validate_v1_consumer_integration_proof_to_import_dry_run` is exported through `lima.adapters.__all__`
- all prior frozen V1-G22 adapter exports remain present
- the G22 final public API freeze fixture reflects the approved adapter export cleanup
- Sparkbot V1-G27 import-smoke validation still passes
- Arc-Bot-shell V1-G27 import-smoke validation still passes
- no Sparkbot or Arc-Bot-shell files were changed
- no validator behavior, consumer runtime calls, consumer integration, shell runtime wiring, provider/model calls, secret lookup, tool execution, connector/browser/network/device/robotics/physical-world behavior, external sends, or product-readiness claims were added

## Capability-Open / Authority-Gated Posture

LIMA AI OS remains capability-open and authority-gated.

Capability-open means LIMA is intended to govern broad capabilities across bots, shells, workstations, office systems, models, tools, files, browser, network, connectors, devices, robots, drones, IoT, automation, and physical-world systems.

Authority-gated means current candidate lanes allow only the authority they explicitly prove. A blocked capability means "not authorized by the current gate," not "impossible forever."

## Consumer Integration Status

Consumer integration: `BLOCKED`

Sparkbot and Arc-Bot-shell now carry static V1-G26 consumer proof edits and V1-G27 test-only import-smoke checks. LIMA now exposes the V1-G23 import dry-run symbols through `lima.adapters.__all__`. They still must not perform live LIMA calls, shell wiring, provider/model calls, connector calls, browser/network behavior, physical-world behavior, or product-readiness claims until future exact approvals land.

## Live Consumer Import/Call Status

Live consumer imports/calls: `NOT_APPROVED`

The chain is now ready for an approval request that plans live consumer import/call boundaries using fake-runtime, no-network, no-secret, and no-provider/model constraints. That planning request must not add live calls by itself.

## Current Blocked Areas

- Live consumer imports/calls are blocked.
- Consumer integration is blocked.
- Live provider/model calls are blocked.
- Secret lookup and credential access are blocked.
- Model dispatch and fallback execution are blocked.
- Actual runtime file edit/delete/mutation execution is blocked.
- Raw live approval factor verification is blocked.
- Approval-token issuance is blocked.
- Connector behavior is blocked.
- Browser/network behavior is blocked.
- HumanInput bridge activation is blocked.
- Device/robot/drone/IoT/physical-world behavior is blocked.
- Product readiness is not approved.

## Product Readiness Status

Product readiness: `NOT_READY`

The current chain is candidate runtime authority infrastructure. It is not a product release, production readiness claim, live consumer integration approval, live provider/model dispatch approval, or physical-world approval.

## Next Recommended Lane

Next recommended lane: prepare V1-G29 live consumer import/call planning approval request.

Reason: V1-G28 cleaned the candidate adapter export surface after consumer import-smoke evidence. The next useful step toward testing Sparkbot and Arc-Bot-shell is an exact planning gate for fake-runtime live consumer import/call boundaries. That gate should remain docs/tests/fixtures-only and should not implement live consumer runtime calls.

Do not implement live consumer imports/calls, live provider/model calls, credential handling, external sends, runtime file mutation execution, connector/browser/network behavior, physical-world behavior, or product-readiness claims without future exact approvals.
