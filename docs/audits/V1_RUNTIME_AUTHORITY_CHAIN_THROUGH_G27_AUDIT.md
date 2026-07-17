# V1 Runtime Authority Chain Through G27 Audit

Date: 2026-06-17
Branch: `audit-v1-runtime-authority-chain-through-g27`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit reviews the V1 authority chain through V1-G27:

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

The audit does not add runtime behavior, edit `lima/` runtime files, call imported LIMA symbols, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, verify raw PINs, issue approval tokens, activate HumanInput, invoke connectors, mutate runtime files, execute browser/network/device/physical-world actions, run scheduled tasks, send external messages, or claim product readiness.

## Inputs Reviewed

- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md`
- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_CLOSEOUT.md`
- `docs/audits/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g27_first_consumer_frozen_api_import_smoke.json`
- `tests/test_v1_g27_first_consumer_frozen_api_import_smoke.py`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G26_AUDIT.md`

## Chain Findings

- V1-G11 through V1-G26 authority gates remain intact: pass.
- V1-G27 adds Sparkbot and Arc-Bot-shell consumer import-smoke tests/fixtures only: pass.
- V1-G27 records saved consumer commits for both repositories: pass.
- V1-G27 imports only the approved frozen G22 LIMA API symbols in consumer tests: pass.
- V1-G27 confirms the approved imported symbols are not called: pass.
- V1-G27 links each consumer import-smoke record to V1-G24 import-plan evidence: pass.
- V1-G27 links each consumer import-smoke record to V1-G25 patch-preview evidence: pass.
- V1-G27 links each consumer import-smoke record to V1-G26 static consumer edit evidence: pass.
- Consumer import-smoke records remain static metadata and test evidence only: pass.
- LIMA remains capability-open and authority-gated: pass.
- Import-smoke evidence exists as proof of symbol availability, not as live import authority, runtime export cleanup, provider/model dispatch, connector behavior, or product readiness: pass.

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
- Runtime export cleanup remains unapproved: pass.
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

- `lima/` runtime files were not touched by V1-G27: pass.
- Sparkbot runtime/source files were not touched by V1-G27: pass.
- Arc-Bot-shell runtime/source files were not touched by V1-G27: pass.
- Sparkbot tests/fixtures import-smoke files were added only as approved: pass.
- Arc-Bot-shell tests/fixtures import-smoke files were added only as approved: pass.
- Approved imported symbols are not called: pass.
- Consumer runtime calls were not added: pass.
- Shell runtime wiring was not added: pass.
- Runtime export cleanup was not performed: pass.
- Live provider/model calls were not added: pass.
- Secret lookup and credential access were not added: pass.
- Product readiness remains unclaimed: pass.

## Residual Gaps

- Runtime export cleanup remains unapproved.
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

- `python -m pytest -q tests\test_v1_g27_first_consumer_frozen_api_import_smoke.py -p no:cacheprovider`: pass, `12 passed`.
- `python -m pytest -q tests\test_v1_g27_first_consumer_frozen_api_import_smoke_approval_request.py -p no:cacheprovider`: pass, `9 passed`.
- `python -m pytest -q tests\test_v1_g26_first_consumer_repository_edit.py -p no:cacheprovider`: pass, `11 passed`.
- `python -m pytest -q tests\test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`: pass, `13 passed`.
- `python -m pytest -q tests\test_adapter_boundaries.py -p no:cacheprovider`: pass, `7 passed`.
- `python -m compileall lima`: pass.
- `python -m pytest -q tests -p no:cacheprovider`: pass, `3699 passed`.
- Sparkbot `python -B -m pytest -q tests\test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py -p no:cacheprovider`: pass, `7 passed`.
- Arc-Bot-shell `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py -p no:cacheprovider`: pass, `7 passed`.
- `git diff --check` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell: pass.
- `git diff --cached --check`: pass before audit commit.

## Audit Conclusion

The V1 authority chain through G27 preserves the capability-open, authority-gated posture while allowing the first test-only consumer import-smoke of the frozen LIMA candidate API. V1-G27 advances Sparkbot and Arc-Bot-shell test preparation without approving calls to imported symbols, live consumer imports/calls, runtime export cleanup, provider/model dispatch, connector/browser/network authority, physical-world behavior, or product readiness.

Recommended next safe step: update readiness rollup through G27, then prepare the next exact approval gate. The smallest safe next lane is runtime export cleanup planning before any live consumer import/call work. Do not implement runtime export cleanup, live consumer imports/calls, live provider/model calls, connector/browser/network authority, physical-world behavior, or product-readiness claims without future exact approvals.
