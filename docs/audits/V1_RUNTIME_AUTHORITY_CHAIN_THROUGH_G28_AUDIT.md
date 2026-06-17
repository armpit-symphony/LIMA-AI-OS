# V1 Runtime Authority Chain Through G28 Audit

Date: 2026-06-17
Branch: `audit-v1-runtime-authority-chain-through-g28`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit reviews the V1 authority chain through V1-G28:

- V1-G11 runtime request decision/preflight
- V1-G12 durable audit/evidence persistence
- V1-G14 destructive approval enforcement
- V1-G15 shell/harness guiderail input contract
- V1-G16 guarded file mutation policy contract
- V1-G17 file mutation preview/diff runtime behavior
- V1-G18 consumer proof packet audit intake
- V1-G19 live approval evidence/capture metadata
- V1-G20 provider/model routing authority metadata
- V1-G21 consumer integration compatibility/freeze metadata
- V1-G22 final public API freeze docs/tests/fixtures
- V1-G23 consumer integration proof-to-import dry-run metadata
- V1-G24 first consumer import-plan evidence packets
- V1-G25 first consumer repo patch-preview evidence
- V1-G26 first consumer repository edit
- V1-G27 first consumer frozen API import-smoke
- V1-G28 runtime export cleanup

The audit does not add new validator behavior, call consumer runtimes, wire shells, call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, verify raw PINs, issue approval tokens, activate HumanInput, invoke connectors, mutate runtime files beyond the already approved export cleanup evidence, execute browser/network/device/physical-world actions, run scheduled tasks, send external messages, or claim product readiness.

## Inputs Reviewed

- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md`
- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP_CLOSEOUT.md`
- `docs/audits/V1_G28_RUNTIME_EXPORT_CLEANUP_AUDIT.md`
- `lima/adapters/__init__.py`
- `tests/fixtures/runtime_extraction/v1_g28_runtime_export_cleanup.json`
- `tests/test_v1_g28_runtime_export_cleanup.py`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G27_AUDIT.md`

## Chain Findings

- V1-G11 through V1-G27 authority gates remain intact: pass.
- V1-G28 adds only the approved `lima.adapters.__all__` export cleanup: pass.
- V1-G28 preserves all prior frozen V1-G22 adapter exports: pass.
- V1-G28 exposes the existing V1-G23 import dry-run symbols through `lima.adapters.__all__`: pass.
- V1-G28 does not add new validator behavior: pass.
- V1-G28 does not edit Sparkbot or Arc-Bot-shell repositories: pass.
- Sparkbot and Arc-Bot-shell V1-G27 import-smoke tests still pass: pass.
- LIMA remains capability-open and authority-gated: pass.
- Runtime export cleanup exists as public API surface metadata cleanup, not as live import/call authority, consumer integration, provider/model dispatch, connector behavior, or product readiness: pass.

## Authority Invariants

- Approval evidence cannot be forged into broad authority: pass.
- Audit/evidence metadata cannot become execution authority: pass.
- Consumer proof packet metadata cannot become runtime authority: pass.
- Consumer compatibility/freeze metadata cannot become runtime authority: pass.
- Final public API freeze docs/tests/fixtures cannot become runtime authority: pass.
- Consumer import dry-run metadata cannot become runtime authority: pass.
- Consumer import-plan evidence packets cannot become runtime authority: pass.
- Consumer repo patch-preview evidence cannot become edit, import, integration, or runtime authority: pass.
- Static consumer repository proof edits cannot become live import, integration, execution, provider/model, connector, browser/network, or physical-world authority: pass.
- Frozen API import-smoke tests cannot become live consumer imports/calls, integration, runtime execution, or shell wiring authority: pass.
- Runtime export cleanup cannot become live consumer imports/calls, provider/model, connector, browser/network, or physical-world authority: pass.
- Live consumer imports/calls and shell wiring remain unapproved: pass.
- Live provider/model calls, secret lookup, model dispatch, and fallback execution remain unapproved: pass.
- Tool, browser/network, connector, device, and physical-world behavior remain blocked unless future exact authority lanes approve them: pass.

## Data Protection Invariants

- Raw secrets are not persisted or emitted: pass.
- Raw prompts are not persisted or emitted: pass.
- Raw file contents are not persisted or emitted: pass.
- Raw diff or patch bodies are not persisted or emitted: pass.
- Raw approval PINs are not verified, persisted, or emitted: pass.
- Raw approval tokens are not persisted or emitted: pass.
- Raw credentials are not persisted or emitted: pass.
- Provider tokens and API keys are not persisted or emitted: pass.
- Raw customer data is not persisted or emitted: pass.

## Integration Invariants

- Only `lima/adapters/__init__.py` was touched as a runtime file in V1-G28: pass.
- Sparkbot files were not touched by V1-G28: pass.
- Arc-Bot-shell files were not touched by V1-G28: pass.
- Existing V1-G27 consumer import-smoke tests still pass: pass.
- Consumer runtime calls were not added: pass.
- Shell runtime wiring was not added: pass.
- Live provider/model calls were not added: pass.
- Secret lookup and credential access were not added: pass.
- Product readiness remains unclaimed: pass.

## Residual Gaps

- Live consumer imports/calls remain unapproved.
- Consumer integration remains unapproved.
- Live provider/model calls remain unapproved.
- Secret lookup and credential access remain unapproved.
- Model dispatch and fallback execution remain unapproved.
- Actual guarded file mutation execution remains unapproved.
- Connector authority remains unapproved.
- Browser/network authority remains unapproved.
- Physical-world/device/robot/drone/IoT authority remains blocked pending a dedicated safety lane.
- Product readiness remains incomplete.

## Validation Evidence

- `python -m pytest -q tests\test_v1_g28_runtime_export_cleanup.py -p no:cacheprovider`: pass, `13 passed`.
- `python -m pytest -q tests\test_v1_g28_runtime_export_cleanup_approval_request.py -p no:cacheprovider`: pass, `9 passed`.
- `python -m pytest -q tests\test_v1_g27_first_consumer_frozen_api_import_smoke.py -p no:cacheprovider`: pass, `12 passed`.
- `python -m pytest -q tests\test_v1_g23_consumer_integration_proof_to_import_dry_run.py -p no:cacheprovider`: pass, `134 passed`.
- `python -m pytest -q tests\test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`: pass, `13 passed`.
- `python -m pytest -q tests\test_adapter_boundaries.py -p no:cacheprovider`: pass, `7 passed`.
- `python -m compileall lima`: pass.
- `python -m pytest -q tests -p no:cacheprovider`: pass, `3721 passed`.
- Sparkbot `python -B -m pytest -q tests\test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py -p no:cacheprovider`: pass, `7 passed`.
- Arc-Bot-shell `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py -p no:cacheprovider`: pass, `7 passed`.
- `git diff --check` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell: pass.
- `git diff --cached --check`: pass before audit commit.

## Audit Conclusion

The V1 authority chain through G28 preserves the capability-open, authority-gated posture while completing the approved adapter export cleanup. V1-G28 improves the candidate public API surface without approving live consumer imports/calls, shell wiring, provider/model dispatch, connector/browser/network authority, physical-world behavior, or product readiness.

Recommended next safe step: update readiness rollup through G28, then prepare the next exact approval gate. The smallest safe next lane is live consumer import/call planning with fake-runtime and no-network boundaries. Do not implement live consumer imports/calls, live provider/model calls, connector/browser/network authority, physical-world behavior, or product-readiness claims without future exact approvals.
