# V1-G28 Runtime Export Cleanup

Date: 2026-06-17
Branch: `v1-g28-runtime-export-cleanup`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_runtime_export_cleanup_slice`

V1-G28 implements the approved runtime export cleanup slice. It promotes the existing V1-G23 consumer import dry-run adapter symbols into the explicit `lima.adapters.__all__` candidate public export surface and records evidence that all prior frozen adapter exports remain present.

This implementation does not add new validator behavior, edit consumer repositories, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G28_RUNTIME_EXPORT_CLEANUP_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G28` template.

Approved implementation branch:

- `v1-g28-runtime-export-cleanup`

Approved runtime scope:

- `runtime_export_cleanup_slice`

## Runtime Export Cleanup Target

Approved package:

- `lima.adapters`

Approved runtime file:

- `lima/adapters/__init__.py`

Existing V1-G23 symbols added to `lima.adapters.__all__`:

- `V1ConsumerImportDryRunError`
- `validate_v1_consumer_integration_proof_to_import_dry_run`

No other runtime file was created, edited, removed, renamed, or cleaned up.

## Files Changed

V1-G28 changed only these LIMA-AI-OS files:

- `lima/adapters/__init__.py`
- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md`
- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g28_runtime_export_cleanup.json`
- `tests/test_v1_g28_runtime_export_cleanup.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

No Sparkbot or Arc-Bot-shell file was created, edited, removed, renamed, imported, or executed by the implementation.

## Preserved Adapter Exports

The prior frozen V1-G22 `lima.adapters.__all__` exports remain present:

- `SparkbotChatInputPayload`
- `SparkbotHumanInputAdapter`
- `SparkbotMeetingInputPayload`
- `SparkbotOperatorInputPayload`
- `SparkbotVoiceInputPayload`
- `V1ConsumerIntegrationCompatibilityError`
- `validate_v1_consumer_integration_compatibility_freeze`

## Required Distinction

V1-G28 separates:

- public adapter export cleanup: implemented
- new validator behavior: not approved and not implemented
- consumer repository edits: not approved and not implemented
- consumer runtime calls: not approved and not implemented
- consumer integration: not approved and not implemented
- shell runtime wiring: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Runtime export cleanup approved: yes.
- Runtime export cleanup added: yes.
- Approved runtime file changed: yes, only `lima/adapters/__init__.py`.
- Existing frozen adapter exports preserved: yes.
- Existing frozen adapter exports removed or renamed: no.
- Validator behavior changed: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution outside approved files added: no.
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

V1-G28 is ready for independent audit.

The next smallest safe step is a separate V1-G28 audit branch. Do not proceed to live consumer imports/calls, consumer integration, live provider/model calls, secret lookup, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
