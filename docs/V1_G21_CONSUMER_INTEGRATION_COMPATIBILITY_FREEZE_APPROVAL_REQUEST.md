# V1-G21 Consumer Integration Compatibility Freeze Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g21-consumer-integration-compatibility-freeze-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit consumer repositories, import consumer code, call consumer runtimes, wire Sparkbot, wire Arc-Bot-shell, wire LIMA Robo OS, freeze the final public API, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G21 implementation of the LIMA-side consumer integration compatibility/freeze metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G20, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G21 Objective

Implement the smallest LIMA-side consumer integration compatibility/freeze metadata slice.

The slice should define how LIMA validates sanitized consumer compatibility evidence for Sparkbot, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and future shells without editing consumer repositories, importing consumer code, calling consumer runtimes, or freezing the final public API.

Compatibility/freeze families covered:

- candidate export surface compatibility
- runtime symbol compatibility
- import surface expectation compatibility
- fixture compatibility matrix
- version and commit metadata compatibility
- Guardian/approval/provider-route boundary compatibility
- no-live-consumer-runtime-call confirmation
- no-consumer-repo-mutation confirmation
- final-public-API-freeze-not-claimed confirmation

## Required Artifact Fields

Each consumer compatibility packet should provide metadata for:

- compatibility packet id
- consumer packet family
- consumer name
- consumer repository
- consumer branch/ref
- consumer commit SHA
- candidate export surface refs
- runtime symbol refs
- import surface expectations
- fixture compatibility matrix
- version compatibility metadata
- Guardian boundary compatibility
- approval boundary compatibility
- provider/model route boundary compatibility
- consumer runtime call prohibition
- no consumer repo mutation confirmation
- no live import/call confirmation
- final public API freeze not claimed confirmation
- audit evidence linkage
- proof-not-authority confirmation
- no raw content/secret/credential/customer-data confirmation
- no execution-authority confirmation

## Required Distinction

V1-G21 must clearly separate:

- sanitized consumer compatibility metadata
- consumer repo edits
- live consumer imports/calls
- consumer runtime wiring
- final public API freeze
- product readiness

Compatibility/freeze metadata remains proof for later consumer integration review. It is not consumer integration, live import authority, runtime wiring, final API freeze, or product readiness by itself.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/adapters/v1_consumer_integration_compatibility.py` (new)
- `lima/adapters/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE.md`
- `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g21_consumer_integration_compatibility_freeze.json`
- `tests/test_v1_g21_consumer_integration_compatibility_freeze.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G21 may add only deterministic local non-executing consumer compatibility/freeze metadata validation.

Allowed if approved:

- validate compatibility packet id metadata
- validate consumer packet family, name, repository, branch/ref, and commit SHA metadata
- validate candidate export surface refs
- validate runtime symbol refs
- validate import surface expectation metadata
- validate fixture compatibility matrix metadata
- validate version compatibility metadata
- validate Guardian boundary compatibility metadata
- validate approval boundary compatibility metadata
- validate provider/model route boundary compatibility metadata
- validate consumer runtime call prohibition metadata
- validate no consumer repo mutation confirmation
- validate no live import/call confirmation
- validate final public API freeze not claimed confirmation
- validate audit/evidence linkage metadata
- validate proof-not-authority confirmation
- reject raw file contents, raw prompts, raw customer data, credentials, secrets, provider tokens, and API keys
- prove compatibility metadata cannot mutate consumer repos, import consumer code, call consumer runtimes, freeze the final API, call providers/models, read secrets, execute tools, or invoke connector/browser/network/device/robotics/physical-world behavior

## Explicitly Forbidden

V1-G21 must not add:

- consumer repo edits
- consumer file writes
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- final public API freeze
- runtime export cleanup
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
- required consumer compatibility fields are enforced
- consumer packet family is constrained
- consumer commit SHA metadata is validated
- candidate export surface refs are required
- runtime symbol refs are required
- import surface expectations are metadata-only
- fixture compatibility matrix is required
- version compatibility metadata is required
- Guardian, approval, and provider/model route boundary compatibility metadata is required
- consumer runtime call prohibition is required
- no consumer repo mutation confirmation is enforced
- no live import/call confirmation is enforced
- final public API freeze not claimed confirmation is enforced
- audit/evidence linkage is required
- proof-not-authority confirmation is enforced
- raw contents, prompts, customer data, credentials, provider tokens, API keys, and secrets fail closed
- consumer repo mutation claims fail closed
- live import/call claims fail closed
- final API freeze claims fail closed
- provider/model call, secret lookup, tool execution, connector/browser/network/device/robotics/physical-world claims fail closed

## Rollback Plan If Approved

Rollback must remove only:

- `lima/adapters/v1_consumer_integration_compatibility.py`
- V1-G21 candidate exports added to `lima/adapters/__init__.py`
- V1-G21 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G21 files
- consumer repo edits are required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- shell runtime wiring is added
- final public API freeze is claimed
- runtime export cleanup is performed
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- compatibility metadata can grant execution authority
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
- Consumer compatibility/freeze behavior added: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Consumer code imports added: no.
- Shell runtime wiring added: no.
- Final public API freeze approved: no.
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

If approved, create branch `v1-g21-consumer-integration-compatibility-freeze` and implement only the LIMA-side consumer integration compatibility/freeze metadata slice. Do not edit consumer repos, import consumer code, call consumer runtimes, freeze the final public API, or claim product readiness.
