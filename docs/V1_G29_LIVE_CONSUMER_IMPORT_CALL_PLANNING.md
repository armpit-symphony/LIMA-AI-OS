# V1-G29 Live Consumer Import/Call Planning

Date: 2026-06-17
Branch: `v1-g29-live-consumer-import-call-planning`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_live_consumer_import_call_planning_metadata_slice`

V1-G29 implements the approved live consumer import/call planning slice. It records deterministic LIMA-side metadata for Sparkbot and Arc-Bot-shell fake-runtime/no-network import/call boundaries after the V1-G28 adapter export cleanup.

This implementation does not edit `lima/` runtime files, edit consumer repositories, call planned adapter symbols, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G29` template.

Approved implementation branch:

- `v1-g29-live-consumer-import-call-planning`

Approved scope:

- `live_consumer_import_call_planning_metadata_slice`

## Planning Surfaces

The planned future call surfaces are metadata-only references to existing candidate LIMA adapter symbols:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

V1-G29 does not call these symbols and does not wire them into Sparkbot or Arc-Bot-shell runtime code.

## Consumer Planning Records

Sparkbot:

- Planning record id: `live-consumer-import-call-plan:v1-g29:sparkbot:001`
- Consumer branch evidence: `v1-g27-first-consumer-frozen-api-import-smoke`
- Consumer commit evidence: `e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f`
- Planned mode: fake-runtime/no-network metadata only

Arc-Bot-shell:

- Planning record id: `live-consumer-import-call-plan:v1-g29:arc-bot-shell:001`
- Consumer branch evidence: `v1-g27-first-consumer-frozen-api-import-smoke`
- Consumer commit evidence: `e619e51d2dca81b272173dffcbc60bf9c3f0d659`
- Planned mode: fake-runtime/no-network metadata only

## LIMA Files Added

V1-G29 changed only these LIMA-AI-OS files:

- `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING.md`
- `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g29_live_consumer_import_call_planning.json`
- `tests/test_v1_g29_live_consumer_import_call_planning.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or executed by the implementation.

No Sparkbot or Arc-Bot-shell file was created, edited, removed, renamed, imported, or executed by the implementation.

## Evidence Links

The planning fixture links:

- V1-G27 first consumer frozen API import-smoke evidence
- V1-G28 runtime export cleanup evidence
- V1-G28 runtime export cleanup audit
- V1 runtime authority chain through G28
- V1 readiness rollup through G28

## Required Distinction

V1-G29 separates:

- fake-runtime/no-network planning metadata: implemented
- live consumer imports/calls: not approved and not implemented
- calls to planned adapter symbols: not approved and not implemented
- `lima/` runtime file changes: not approved and not implemented
- Sparkbot file edits: not approved and not implemented
- Arc-Bot-shell file edits: not approved and not implemented
- consumer integration: not approved and not implemented
- shell runtime wiring: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Live consumer import/call planning added: yes, metadata only.
- `lima/` runtime files changed: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Planned adapter symbols called: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution outside approved docs/tests/fixtures added: no.
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

V1-G29 is ready for independent audit.

The next smallest safe step is a separate V1-G29 audit branch. Do not proceed to fake-runtime calls, live consumer imports/calls, provider/model dispatch, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
