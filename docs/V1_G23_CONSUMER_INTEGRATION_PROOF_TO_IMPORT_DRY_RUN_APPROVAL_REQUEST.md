# V1-G23 Consumer Integration Proof-To-Import Dry Run Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g23-consumer-integration-proof-to-import-dry-run-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit consumer repositories, import consumer code, call consumer runtimes, wire Sparkbot, wire Arc-Bot-shell, clean up runtime exports, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G23 implementation of the LIMA-side consumer integration proof-to-import dry-run metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G22, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G23 Objective

Implement the smallest LIMA-side consumer integration proof-to-import dry-run metadata slice.

The slice should validate sanitized import-plan metadata for Sparkbot, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and future shells. It converts accepted proof packet, compatibility, and frozen API evidence into an auditable import plan without editing consumer repositories, importing consumer code, calling consumer runtimes, wiring shells, cleaning up exports, or claiming product readiness.

Dry-run import-plan families covered:

- consumer proof packet linkage
- consumer compatibility packet linkage
- frozen public API surface linkage
- proposed import statements as metadata only
- proposed call sites as metadata only
- expected adapter boundary mapping
- Guardian boundary mapping
- approval boundary mapping
- provider/model route boundary mapping
- no-live-import-call confirmation
- no-consumer-repo-mutation confirmation
- no-runtime-export-cleanup confirmation
- proof-not-authority confirmation

## Required Artifact Fields

Each dry-run import plan should provide metadata for:

- import plan id
- consumer packet family
- consumer name
- consumer repository
- consumer branch/ref
- consumer commit SHA
- proof packet ref
- compatibility packet ref
- frozen API packet ref
- proposed import metadata
- proposed call-site metadata
- adapter boundary mapping
- Guardian boundary mapping
- approval boundary mapping
- provider/model route boundary mapping
- expected test command metadata
- rollback metadata
- no consumer repo mutation confirmation
- no live import/call confirmation
- no runtime export cleanup confirmation
- no raw content/secret/credential/customer-data confirmation
- proof-not-authority confirmation
- audit evidence linkage

## Required Distinction

V1-G23 must clearly separate:

- sanitized import-plan metadata
- consumer repo edits
- live consumer imports/calls
- consumer runtime wiring
- runtime export cleanup
- provider/model dispatch
- product readiness

The import plan remains proof for later consumer integration review. It is not consumer integration, live import authority, runtime wiring, export cleanup, provider/model dispatch, connector authority, physical-world authority, or product readiness by itself.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/adapters/v1_consumer_import_dry_run.py` (new)
- `lima/adapters/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G23_CONSUMER_INTEGRATION_PROOF_TO_IMPORT_DRY_RUN.md`
- `docs/V1_G23_CONSUMER_INTEGRATION_PROOF_TO_IMPORT_DRY_RUN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g23_consumer_integration_proof_to_import_dry_run.json`
- `tests/test_v1_g23_consumer_integration_proof_to_import_dry_run.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G23 may add only deterministic local non-executing dry-run import-plan metadata validation.

Allowed if approved:

- validate import plan id metadata
- validate consumer packet family, name, repository, branch/ref, and commit SHA metadata
- validate proof packet ref metadata
- validate compatibility packet ref metadata
- validate frozen API packet ref metadata
- validate proposed import metadata without importing consumer code
- validate proposed call-site metadata without calling consumer runtimes
- validate adapter boundary mapping metadata
- validate Guardian boundary mapping metadata
- validate approval boundary mapping metadata
- validate provider/model route boundary mapping metadata
- validate expected test command metadata
- validate rollback metadata
- validate no consumer repo mutation confirmation
- validate no live import/call confirmation
- validate no runtime export cleanup confirmation
- validate no raw content/secret/credential/customer-data confirmation
- validate proof-not-authority confirmation
- reject raw file contents, raw prompts, raw customer data, credentials, secrets, provider tokens, and API keys
- prove import-plan metadata cannot mutate consumer repos, import consumer code, call consumer runtimes, clean up exports, call providers/models, read secrets, execute tools, or invoke connector/browser/network/device/robotics/physical-world behavior

## Explicitly Forbidden

V1-G23 must not add:

- consumer repo edits
- consumer file writes
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- runtime export cleanup
- `lima/` export cleanup
- live provider/model calls
- model request dispatch
- secret lookup
- credential access
- tool execution
- action execution
- file mutation execution
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- fixture records `CANDIDATE_ONLY`
- required dry-run import-plan fields are enforced
- consumer packet family is constrained
- consumer commit SHA metadata is validated
- proof packet ref is required
- compatibility packet ref is required
- frozen API packet ref is required
- proposed import metadata is metadata-only
- proposed call-site metadata is metadata-only
- adapter, Guardian, approval, and provider/model boundary mappings are required
- expected test command metadata is required
- rollback metadata is required
- no consumer repo mutation confirmation is enforced
- no live import/call confirmation is enforced
- no runtime export cleanup confirmation is enforced
- proof-not-authority confirmation is enforced
- raw contents, prompts, customer data, credentials, provider tokens, API keys, and secrets fail closed
- consumer repo mutation claims fail closed
- live import/call claims fail closed
- runtime export cleanup claims fail closed
- provider/model call, secret lookup, tool execution, connector/browser/network/device/robotics/physical-world claims fail closed

## Rollback Plan If Approved

Rollback must remove only:

- `lima/adapters/v1_consumer_import_dry_run.py`
- V1-G23 candidate exports added to `lima/adapters/__init__.py`
- V1-G23 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G23 files
- consumer repo edits are required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- shell runtime wiring is added
- runtime export cleanup is required
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- import-plan metadata can grant execution authority
- tool execution is added
- action execution is added
- file mutation execution is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Dry-run import-plan behavior added: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Consumer code imports added: no.
- Shell runtime wiring added: no.
- Runtime export cleanup approved: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g23-consumer-integration-proof-to-import-dry-run` and implement only the LIMA-side consumer integration proof-to-import dry-run metadata slice. Do not edit consumer repos, import consumer code, call consumer runtimes, clean up exports, or claim product readiness.
