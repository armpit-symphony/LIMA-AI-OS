# V1-G35 Consumer Integration Compatibility Review Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g35-consumer-integration-compatibility-review-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer test files, call consumer runtimes, execute adapter validators, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G35 implementation of the consumer integration compatibility review slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G34, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G35 Objective

Implement the smallest LIMA-side consumer integration compatibility review slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that review whether the V1-G27 through V1-G34 evidence is sufficient to propose a future bounded consumer integration lane for Sparkbot and Arc-Bot-shell. It must not edit consumer repositories, call adapter symbols, call consumer runtimes, wire shells, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW.md`
- `docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g35_consumer_integration_compatibility_review.json`
- `tests/test_v1_g35_consumer_integration_compatibility_review.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G35.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G35.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G35 may add only deterministic LIMA-side docs/tests/fixtures that review evidence and record compatibility metadata.

Allowed if approved:

- add one LIMA-side compatibility review fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side compatibility review test
- review V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, V1-G30 fake-runtime evidence, V1-G31 preview evidence, V1-G32 consumer test edit evidence, V1-G33 smoke evidence, and V1-G34 live consumer import/call test evidence
- record gaps and next-lane recommendations
- enforce no runtime file change confirmation
- enforce no consumer repo mutation confirmation
- enforce no adapter symbol execution confirmation
- enforce no consumer runtime module import confirmation
- enforce no shell wiring confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw sensitive content persistence in LIMA evidence
- enforce proof-not-integration-authority and proof-not-product-readiness confirmations

## Explicitly Forbidden

V1-G35 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer test files
- consumer runtime/source file edits
- consumer runtime module imports
- calls to LIMA adapter symbols
- fake call envelope execution
- consumer integration
- shell runtime wiring
- live provider/model calls
- model request dispatch
- fallback execution
- secret lookup
- credential access
- connector behavior
- browser or network behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- HumanInput bridge activation
- scheduled task execution
- external sends
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- raw sensitive content persistence in LIMA evidence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA compatibility review fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved LIMA docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell files are changed
- Sparkbot compatibility review record exists and remains review-only
- Arc-Bot-shell compatibility review record exists and remains review-only
- V1-G27 through V1-G34 evidence is linked
- no adapter symbols are called
- no consumer runtime modules are imported
- no shell wiring, provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-sensitive-content persistence is added to LIMA evidence
- proof-not-integration-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G35 tests
- LIMA focused V1-G34 tests
- LIMA focused V1-G33 tests
- LIMA focused V1-G32 tests
- LIMA focused V1-G31 tests
- LIMA focused V1-G30 tests
- LIMA focused V1-G29 tests
- LIMA focused V1-G28 tests
- LIMA focused V1-G27 tests
- LIMA focused adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G34 live consumer import/call test
- Sparkbot focused V1-G32 consumer test
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G34 live consumer import/call test
- Arc-Bot-shell focused V1-G32 consumer test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run live provider/model calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G35 docs/tests/fixtures:

- `docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW.md`
- `docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g35_consumer_integration_compatibility_review.json`
- `tests/test_v1_g35_consumer_integration_compatibility_review.py`

Rollback must not require `lima/` runtime file changes, consumer repository changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G35 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell file edits are required
- consumer runtime/source file edits are required
- adapter symbols are called
- consumer runtime modules are imported
- consumer integration is added
- shell runtime wiring is added
- provider/model calls are added
- model request dispatch is added
- fallback execution is added
- secret lookup or credential access is added
- raw sensitive content can persist or emit in LIMA evidence
- connector/browser/network/device/robotics/physical-world behavior is added
- action execution is added
- file mutation execution outside the exact approved docs/tests/fixtures files is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Consumer integration compatibility review approved: no.
- Consumer integration compatibility review added: no.
- Consumer integration approved: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer runtime/source files changed by this request: no.
- Adapter symbols called: no.
- Consumer runtime modules imported: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Raw sensitive content persisted in LIMA evidence: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g35-consumer-integration-compatibility-review` in LIMA-AI-OS. Implement only the exact consumer integration compatibility review slice. Do not edit runtime files, edit consumer repos, wire shells, call providers/models, access secrets, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
