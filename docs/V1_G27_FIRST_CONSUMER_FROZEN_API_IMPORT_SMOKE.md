# V1-G27 First Consumer Frozen API Import-Smoke

Date: 2026-06-17
Branch: `v1-g27-first-consumer-frozen-api-import-smoke`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_test_only_consumer_frozen_api_import_smoke_slice`

V1-G27 implements the approved first consumer frozen API import-smoke slice. It adds test-only import-smoke records to Sparkbot and Arc-Bot-shell, then records their LIMA-side intake evidence as docs/tests/fixtures.

This implementation does not edit `lima/` runtime files, call imported LIMA symbols from consumer tests, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G27` template.

Approved implementation branch:

- `v1-g27-first-consumer-frozen-api-import-smoke`

Approved scope:

- first consumer frozen API import-smoke tests/fixtures slice

## Frozen API Import-Smoke Surface

The approved import-smoke symbols are:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.V1ConsumerIntegrationCompatibilityError`

Consumer tests import these symbols through the local LIMA-AI-OS checkout only. They do not call the validator, invoke LIMA runtime behavior, or import consumer runtime modules.

## Consumer Repository Commits

Sparkbot:

- Branch: `v1-g27-first-consumer-frozen-api-import-smoke`
- Commit: `e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f`
- Files added:
  - `tests/fixtures/sparkbot_lima_v1_g27_frozen_api_import_smoke.json`
  - `tests/test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py`

Arc-Bot-shell:

- Branch: `v1-g27-first-consumer-frozen-api-import-smoke`
- Commit: `e619e51d2dca81b272173dffcbc60bf9c3f0d659`
- Files added:
  - `tests/fixtures/arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.json`
  - `tests/test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py`

## LIMA Files Added

V1-G27 changed only these LIMA-AI-OS files:

- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md`
- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g27_first_consumer_frozen_api_import_smoke.json`
- `tests/test_v1_g27_first_consumer_frozen_api_import_smoke.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or executed.

## Evidence Added

The LIMA fixture records two import-smoke evidence records:

- Sparkbot V1-G27 frozen API import-smoke record
- Arc-Bot-shell V1-G27 frozen API import-smoke record

Each record links:

- V1-G22 frozen API metadata
- V1-G24 import-plan evidence packet
- V1-G25 patch-preview evidence packet
- V1-G26 static consumer edit evidence

## Required Distinction

V1-G27 separates:

- test-only import-smoke of frozen LIMA API symbols: implemented
- calls to imported symbols: not approved and not implemented
- `lima/` runtime changes: not approved and not implemented
- consumer runtime/source edits: not approved and not implemented
- live consumer imports/calls: not approved and not implemented
- consumer integration: not approved and not implemented
- runtime export cleanup: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Consumer frozen API import-smoke implementation added: yes, tests/fixtures only.
- `lima/` runtime files changed: no.
- Sparkbot runtime/source files changed: no.
- Arc-Bot-shell runtime/source files changed: no.
- Imported LIMA symbols called: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- Runtime export cleanup approved: no.
- Runtime export cleanup added: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution outside approved tests/fixtures added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Raw diff or full patch body persisted: no.
- Raw file contents persisted: no.
- Product readiness approved: no.

## Readiness Result

V1-G27 is ready for independent audit.

The next smallest safe step is a separate V1-G27 audit branch. Do not proceed to runtime export cleanup, live consumer imports/calls, provider/model dispatch, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
