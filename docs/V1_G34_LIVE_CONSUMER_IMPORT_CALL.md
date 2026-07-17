# V1-G34 Live Consumer Import/Call

Date: 2026-06-17
Branch: `v1-g34-live-consumer-import-call`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_live_consumer_import_call_test_slice`

V1-G34 implements the approved live consumer import/call test slice. It adds exact focused Sparkbot and Arc-Bot-shell tests that import and call only approved LIMA adapter validators with static sanitized metadata, plus deterministic LIMA-side evidence metadata for those tests.

This implementation does not edit `lima/` runtime files, edit consumer runtime/source files, import consumer runtime modules, wire shells, call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G34` template.

Approved implementation branch:

- `v1-g34-live-consumer-import-call`

Approved scope:

- `live_consumer_import_call_test_slice`

## Live Consumer Import/Call Records

Sparkbot:

- Live call record id: `live-consumer-import-call:v1-g34:sparkbot:001`
- Consumer commit evidence: `cee164655e1603f5e68b6df9773dc5b08dd27ca0`
- Added fixture: `tests/fixtures/sparkbot_lima_v1_g34_live_consumer_import_call.json`
- Added test: `tests/test_sparkbot_lima_v1_g34_live_consumer_import_call.py`
- Focused V1-G34 consumer test result: `9 passed`
- Runtime/source files changed: no
- Consumer runtime modules imported: no
- Provider/model calls added: no

Arc-Bot-shell:

- Live call record id: `live-consumer-import-call:v1-g34:arc-bot-shell:001`
- Consumer commit evidence: `61404a3bf7d95a45138ebd97992bcebe61651d79`
- Added fixture: `tests/fixtures/arc_bot_shell_lima_v1_g34_live_consumer_import_call.json`
- Added test: `tests/test_arc_bot_shell_lima_v1_g34_live_consumer_import_call.py`
- Focused V1-G34 consumer test result: `9 passed`
- Runtime/source files changed: no
- Consumer runtime modules imported: no
- Provider/model calls added: no

## Approved Adapter Validator Calls

The focused consumer tests call only these approved LIMA adapter validators:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

The calls use static sanitized metadata fixtures. The returned records remain candidate-only, non-executing, proof-not-authority metadata.

## LIMA Files Added

V1-G34 changed only these LIMA-AI-OS files:

- `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL.md`
- `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g34_live_consumer_import_call.json`
- `tests/test_v1_g34_live_consumer_import_call.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or executed by the implementation.

## Consumer Files Added

V1-G34 changed only these consumer files:

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g34_live_consumer_import_call.json`
- `tests/test_sparkbot_lima_v1_g34_live_consumer_import_call.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g34_live_consumer_import_call.json`
- `tests/test_arc_bot_shell_lima_v1_g34_live_consumer_import_call.py`

No Sparkbot or Arc-Bot-shell runtime/source file was created, edited, removed, renamed, imported, or executed by the implementation.

## Evidence Links

The fixture links:

- V1-G27 first consumer frozen API import-smoke evidence
- V1-G28 runtime export cleanup evidence
- V1-G29 live consumer import/call planning evidence
- V1-G30 fake-runtime consumer call evidence
- V1-G31 fake-runtime consumer repository test preview evidence
- V1-G32 consumer repository test edit evidence
- V1-G33 consumer fake-runtime import/call smoke evidence
- V1-G33 consumer fake-runtime import/call smoke audit
- V1 runtime authority chain through G33
- V1 readiness rollup through G33

## Required Distinction

V1-G34 separates:

- approved focused test-only adapter validator calls: implemented
- consumer runtime module imports: not approved and not implemented
- consumer runtime/source file edits: not approved and not implemented
- shell runtime wiring: not approved and not implemented
- fake call envelope execution: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- secret lookup or credential access: not approved and not implemented
- raw sensitive content persistence in LIMA evidence: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Live consumer import/call test slice added: yes, approved focused tests only.
- Approved adapter validator calls executed: yes, in approved focused consumer tests only.
- Unapproved adapter symbols called: no.
- `lima/` runtime files changed: no.
- Sparkbot runtime/source files changed: no.
- Arc-Bot-shell runtime/source files changed: no.
- Consumer runtime modules imported: no.
- Fake call envelopes executed: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Fallback execution added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution outside local tests added: no.
- Action execution added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Raw sensitive content persisted in LIMA evidence: no.
- Product readiness approved: no.

## Readiness Result

V1-G34 is ready for independent audit.

The next smallest safe step is a separate V1-G34 audit branch. Do not proceed to consumer integration, provider/model dispatch, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
