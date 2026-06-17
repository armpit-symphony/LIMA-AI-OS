# V1-G23 Consumer Integration Proof-To-Import Dry Run

Date: 2026-06-17
Branch: `v1-g23-consumer-integration-proof-to-import-dry-run`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_consumer_integration_proof_to_import_dry_run_slice`

V1-G23 implements the approved LIMA-side consumer integration proof-to-import dry-run metadata slice. It validates sanitized import-plan evidence for Sparkbot, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and future shells so accepted proof packets, compatibility evidence, and frozen public API surfaces can be reviewed before any consumer repository edit or live runtime path is approved.

This implementation does not edit consumer repositories, write consumer files, import consumer code, call consumer runtimes, wire Sparkbot, wire Arc-Bot-shell, wire LIMA Robo OS, clean up runtime exports, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G23_CONSUMER_INTEGRATION_PROOF_TO_IMPORT_DRY_RUN_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G23` template.

Approved implementation branch:

- `v1-g23-consumer-integration-proof-to-import-dry-run`

Approved runtime scope:

- `consumer_integration_proof_to_import_dry_run_metadata_slice`

## Runtime Files

- `lima/adapters/v1_consumer_import_dry_run.py`
- `lima/adapters/__init__.py` (module-level candidate symbol availability; frozen G22 `__all__` unchanged)

## Runtime Symbols

- `V1ConsumerImportDryRunError`
- `validate_v1_consumer_integration_proof_to_import_dry_run`

## Behavior Added

V1-G23 adds one deterministic local consumer import-plan metadata validator:

- requires import plan id metadata
- requires consumer packet family, name, repository, branch/ref, and commit SHA metadata
- supports `sparkbot`, `arc_bot`, `lima_robo_os`, `lima_office`, and `future_shell` packet families
- requires proof packet ref metadata
- requires compatibility packet ref metadata
- requires frozen API packet ref metadata
- requires proposed import metadata and keeps it metadata-only
- requires proposed call-site metadata and keeps it metadata-only
- requires adapter, Guardian, approval, and provider/model boundary mappings
- requires expected test command metadata
- requires rollback metadata
- requires no consumer repo mutation confirmation
- requires no live import/call confirmation
- requires no runtime export cleanup confirmation
- requires no raw content/secret/credential/customer-data confirmation
- requires proof-not-authority confirmation
- requires audit/evidence linkage
- returns a deterministic `record_hash`
- keeps consumer repo mutation, consumer imports, consumer runtime calls, consumer integration, shell wiring, runtime export cleanup, provider/model calls, secret lookup, credential access, tool execution, file mutation, connector/browser/network/device/robotics/physical-world, and product readiness flags false

## Required Distinction

V1-G23 separates:

- sanitized import-plan metadata: implemented as validation
- consumer repo edits: not approved and not implemented
- live consumer imports/calls: not approved and not implemented
- consumer runtime wiring: not approved and not implemented
- runtime export cleanup: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Dry-run import-plan behavior added: yes, only the approved non-executing metadata validator.
- Frozen G22 `lima.adapters.__all__` changed: no.
- Consumer repo mutation added: no.
- Consumer file writes added: no.
- Consumer code imports added: no.
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
- File mutation execution added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Product readiness approved: no.

## Readiness Result

V1-G23 is ready for independent audit.

The next smallest safe step is a separate V1-G23 audit branch. Do not proceed to consumer repo edits, live consumer imports/calls, runtime export cleanup, live provider/model calls, secret lookup, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
