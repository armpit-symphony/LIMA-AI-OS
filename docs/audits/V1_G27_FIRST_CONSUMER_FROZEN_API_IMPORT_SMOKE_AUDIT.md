# V1-G27 First Consumer Frozen API Import-Smoke Audit

Date: 2026-06-17
Branch: `audit-v1-g27-first-consumer-frozen-api-import-smoke`
Audited LIMA implementation branch: `v1-g27-first-consumer-frozen-api-import-smoke`
Audited LIMA implementation commit: `ed53fc969155b38cfaa0efd4e0bdd8c2a69dfaf2`
Audited Sparkbot implementation branch: `v1-g27-first-consumer-frozen-api-import-smoke`
Audited Sparkbot implementation commit: `e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f`
Audited Arc-Bot-shell implementation branch: `v1-g27-first-consumer-frozen-api-import-smoke`
Audited Arc-Bot-shell implementation commit: `e619e51d2dca81b272173dffcbc60bf9c3f0d659`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit independently reviews the V1-G27 first consumer frozen API import-smoke implementation. It does not add runtime behavior, edit `lima/` runtime files, call imported LIMA symbols, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Scope Reviewed

LIMA-AI-OS:

- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md`
- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g27_first_consumer_frozen_api_import_smoke.json`
- `tests/test_v1_g27_first_consumer_frozen_api_import_smoke.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g27_frozen_api_import_smoke.json`
- `tests/test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.json`
- `tests/test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py`

## Decision And File-Map Findings

- Exact `Approve-V1-G27` decision was recorded: pass.
- Exact approval wording was recorded: pass.
- Approved LIMA branch recorded as `v1-g27-first-consumer-frozen-api-import-smoke`: pass.
- LIMA implementation stayed inside the approved V1-G27 docs/tests/fixtures file map: pass.
- Sparkbot implementation stayed inside the approved V1-G27 tests/fixtures file map: pass.
- Arc-Bot-shell implementation stayed inside the approved V1-G27 tests/fixtures file map: pass.
- No `lima/` runtime files were changed: pass.
- No Sparkbot runtime/source files were changed outside the focused tests/fixtures: pass.
- No Arc-Bot-shell runtime/source files were changed outside the focused tests/fixtures: pass.
- Runtime export cleanup was not performed: pass.
- Product readiness was not claimed: pass.

## Import-Smoke Findings

- Sparkbot V1-G27 import-smoke fixture exists: pass.
- Sparkbot V1-G27 import-smoke test exists and passed: pass.
- Arc-Bot-shell V1-G27 import-smoke fixture exists: pass.
- Arc-Bot-shell V1-G27 import-smoke test exists and passed: pass.
- LIMA intake fixture records the saved Sparkbot import-smoke commit: pass.
- LIMA intake fixture records the saved Arc-Bot-shell import-smoke commit: pass.
- Each consumer test imports only the approved frozen G22 LIMA API symbols: pass.
- Approved frozen API symbols are not called by the consumer tests: pass.
- Each consumer proof record links V1-G22 frozen API metadata: pass.
- Each consumer proof record links V1-G24 import-plan evidence: pass.
- Each consumer proof record links V1-G25 patch-preview evidence: pass.
- Each consumer proof record links V1-G26 static consumer edit evidence: pass.
- Each consumer proof record remains proof metadata, not authority: pass.

## Boundary Findings

- Consumer runtime calls were not added: pass.
- LIMA runtime behavior was not invoked: pass.
- Consumer integration was not added: pass.
- Shell runtime wiring was not added: pass.
- Runtime export cleanup was not approved: pass.
- Runtime export cleanup was not added: pass.
- Live provider/model calls were not added: pass.
- Model request dispatch was not added: pass.
- Secret lookup was not added: pass.
- Credential access was not added: pass.
- Tool execution was not added: pass.
- Action execution was not added: pass.
- File mutation execution outside approved docs/tests/fixtures was not added: pass.
- HumanInput bridge was not activated: pass.
- Connector behavior was not added: pass.
- Browser/network/file/device/robotics/physical-world behavior was not added: pass.
- Scheduled task execution was not added: pass.
- External sends were not added: pass.
- External database writes were not added: pass.
- Raw diffs or full patch bodies were not persisted: pass.
- Raw file contents were not persisted: pass.
- Product readiness was not claimed: pass.

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
- `git diff --cached --check` before each implementation commit: pass.

## Audit Conclusion

V1-G27 passes audit as a candidate first consumer frozen API import-smoke slice. It proves that Sparkbot and Arc-Bot-shell can import the approved frozen G22 LIMA candidate public API symbols from local tests without calling those symbols, invoking LIMA runtime behavior, calling consumer runtimes, wiring shells, cleaning up runtime exports, calling providers/models, invoking connectors, using browser/network/device/physical-world authority, or claiming product readiness.

Recommended next safe step: audit the V1 runtime authority chain through V1-G27, then update readiness and decide the next approval-gated lane. Do not implement runtime export cleanup, live consumer imports/calls, live provider/model calls, connector/browser/network authority, physical-world behavior, or product-readiness claims without future exact approvals.
