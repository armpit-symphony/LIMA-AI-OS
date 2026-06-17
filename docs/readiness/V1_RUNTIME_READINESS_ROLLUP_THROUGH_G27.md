# V1 Runtime Readiness Rollup Through G27

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g27`
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
- Runtime export cleanup: `NOT_APPROVED`
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

All accepted evidence remains proof or metadata unless a later exact approval gate grants additional authority.

## V1-G27 Status

V1-G27 implemented the first consumer frozen API import-smoke slice as tests/fixtures and LIMA-side evidence only.

Accepted evidence:

- exact `Approve-V1-G27` decision was recorded
- Sparkbot import-smoke test imports the approved frozen G22 LIMA API symbols and passed focused validation
- Arc-Bot-shell import-smoke test imports the approved frozen G22 LIMA API symbols and passed focused validation
- LIMA intake fixture records Sparkbot commit `e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f`
- LIMA intake fixture records Arc-Bot-shell commit `e619e51d2dca81b272173dffcbc60bf9c3f0d659`
- approved imported symbols were not called by consumer tests
- each consumer import-smoke record links V1-G22, V1-G24, V1-G25, and V1-G26 evidence
- consumer repository edits are limited to approved tests/fixtures
- no `lima/` runtime file changes, Sparkbot runtime/source edits, Arc-Bot-shell runtime/source edits, live consumer runtime calls, runtime export cleanup, provider/model calls, secret lookup, tool execution, connector/browser/network/device/robotics/physical-world behavior, external sends, or product-readiness claims were added

## Capability-Open / Authority-Gated Posture

LIMA AI OS remains capability-open and authority-gated.

Capability-open means LIMA is intended to govern broad capabilities across bots, shells, workstations, office systems, models, tools, files, browser, network, connectors, devices, robots, drones, IoT, automation, and physical-world systems.

Authority-gated means current candidate lanes allow only the authority they explicitly prove. A blocked capability means "not authorized by the current gate," not "impossible forever."

## Consumer Integration Status

Consumer integration: `BLOCKED`

Sparkbot and Arc-Bot-shell now carry static V1-G26 consumer proof edits and V1-G27 test-only import-smoke checks for the frozen LIMA candidate public API surface. They still must not perform live LIMA calls, shell wiring, runtime export cleanup, provider/model calls, connector calls, browser/network behavior, physical-world behavior, or product-readiness claims until future exact approvals land.

## Runtime Export Cleanup Status

Runtime export cleanup: `NOT_APPROVED`

The V1-G27 smoke tests prove the current frozen symbols can be imported from the local LIMA checkout. They do not approve adding, removing, renaming, reshaping, or deprecating runtime exports. Any cleanup must start with a separate approval request that defines exact files, compatibility expectations, rollback, validation, and stop conditions.

## Current Blocked Areas

- Runtime export cleanup is blocked.
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

The current chain is candidate runtime authority infrastructure. It is not a product release, production readiness claim, live consumer integration approval, runtime export cleanup approval, live provider/model dispatch approval, or physical-world approval.

## Next Recommended Lane

Next recommended lane: prepare V1-G28 runtime export cleanup approval request.

Reason: V1-G27 proves Sparkbot and Arc-Bot-shell can import the frozen candidate LIMA public API symbols from focused tests. Before live consumer calls, the public export surface should be cleaned up only under a dedicated approval gate that preserves compatibility, records rollback, and blocks hidden runtime behavior.

Do not implement runtime export cleanup, live consumer imports/calls, live provider/model calls, credential handling, external sends, runtime file mutation execution, connector/browser/network behavior, physical-world behavior, or product-readiness claims without future exact approvals.
