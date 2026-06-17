# V1-G22 Final Public API Freeze Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g22-final-public-api-freeze-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, freeze the final public API, clean up runtime exports, edit consumer repositories, import consumer code, call consumer runtimes, wire Sparkbot, wire Arc-Bot-shell, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G22 implementation of the LIMA-side final public API freeze docs/tests/fixtures slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G21, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G22 Objective

Implement the smallest LIMA-side final public API freeze slice.

The slice should lock the current candidate public import surfaces as metadata and tests so Sparkbot, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and future shells can test against a stable V1 import contract. It must not edit consumer repositories, import consumer code, call consumer runtimes, wire shells, clean up exports, change runtime behavior, or claim product readiness.

Public API freeze families covered:

- package-level public import surface inventory
- subpackage `__all__` export inventory
- V1 candidate runtime symbol inventory
- consumer compatibility reference linkage
- import surface expectation linkage
- future public API change gate
- runtime export cleanup not approved confirmation
- no-live-consumer-import-call confirmation
- no-consumer-repo-mutation confirmation
- no-runtime-behavior-change confirmation
- proof-not-authority confirmation

## Required Artifact Fields

Each final API freeze packet should provide metadata for:

- final API freeze packet id
- API status
- freeze scope
- public package surfaces
- public subpackage export surfaces
- V1 runtime symbol surfaces
- candidate export inventory refs
- consumer compatibility refs
- import surface expectation refs
- backward compatibility policy
- future change gate policy
- runtime export cleanup policy
- Guardian boundary confirmation
- approval boundary confirmation
- provider/model route boundary confirmation
- no consumer repo mutation confirmation
- no live import/call confirmation
- no runtime behavior change confirmation
- no secret/credential/customer-data confirmation
- proof-not-authority confirmation
- audit evidence linkage

## Required Distinction

V1-G22 must clearly separate:

- final public API freeze evidence
- runtime export cleanup
- consumer repo edits
- live consumer imports/calls
- consumer runtime wiring
- runtime behavior changes
- product readiness

The final public API freeze is a compatibility contract for later consumer testing. It is not consumer integration, export cleanup, live import authority, runtime wiring, provider/model dispatch, connector authority, physical-world authority, or product readiness by itself.

## Approved Files If Operator Says Yes

Docs/tests/fixtures only:

- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md`
- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- `tests/test_v1_g22_final_public_api_freeze.py`

No `lima/` runtime files may be created or edited in V1-G22. Runtime export cleanup requires a separate gate unless a future operator decision explicitly expands this request before implementation.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G22 may add only deterministic local docs/tests/fixtures that freeze current public import surfaces.

Allowed if approved:

- record final API freeze packet id metadata
- record API status as `CANDIDATE_ONLY`
- record freeze scope metadata
- record current public package surface refs
- record current public subpackage `__all__` export refs
- record current V1 runtime symbol refs
- record candidate export inventory refs
- record consumer compatibility refs
- record import surface expectation refs
- record backward compatibility policy
- record future public API change gate policy
- record runtime export cleanup as not approved
- record Guardian boundary confirmation
- record approval boundary confirmation
- record provider/model route boundary confirmation
- record no consumer repo mutation confirmation
- record no live import/call confirmation
- record no runtime behavior change confirmation
- record no secret/credential/customer-data confirmation
- record proof-not-authority confirmation
- add tests that compare the frozen export inventory to current local imports
- prove the freeze packet cannot mutate consumer repos, import consumer code, call consumer runtimes, clean up exports, call providers/models, read secrets, execute tools, or invoke connector/browser/network/device/robotics/physical-world behavior

## Explicitly Forbidden

V1-G22 must not add:

- `lima/` runtime file changes
- runtime export cleanup
- symbol removal from current exports
- symbol rename from current exports
- unreviewed public exports
- consumer repo edits
- consumer file writes
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
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
- final API freeze packet fields are present
- public package surfaces are listed
- public subpackage export surfaces are listed
- V1 runtime symbol surfaces are listed
- candidate export inventory refs are listed
- consumer compatibility refs are listed
- import surface expectation refs are listed
- backward compatibility policy is recorded
- future public API change gate policy is recorded
- runtime export cleanup remains not approved
- current local `__all__` exports match the frozen fixture
- current frozen symbols are importable locally
- no `lima/` runtime file changes are required
- no consumer repo mutation is approved
- no live import/call behavior is approved
- no runtime behavior change is approved
- no provider/model call, secret lookup, tool execution, connector/browser/network/device/robotics/physical-world behavior is approved

## Rollback Plan If Approved

Rollback must remove only:

- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md`
- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- `tests/test_v1_g22_final_public_api_freeze.py`

Rollback must not require `lima/` runtime file changes, consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G22 files
- `lima/` runtime file changes are required
- runtime export cleanup is required
- current export symbols must be removed or renamed
- unreviewed public exports are introduced
- consumer repo edits are required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- final API freeze evidence can grant execution authority
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
- Final public API freeze implemented: no.
- Runtime export cleanup approved: no.
- `lima/` runtime files changed: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Consumer code imports added: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g22-final-public-api-freeze` and implement only the LIMA-side final public API freeze docs/tests/fixtures slice. Do not edit `lima/` runtime files, clean up exports, edit consumer repos, import consumer code, call consumer runtimes, or claim product readiness.
