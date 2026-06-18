# V1-G36 Bounded Consumer Integration Design Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g36-bounded-consumer-integration-design-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer test files, call adapter symbols, import consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G36 implementation of the bounded consumer integration design slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G35, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G36 Objective

Implement the smallest LIMA-side bounded consumer integration design slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that define a candidate future integration design boundary for Sparkbot and Arc-Bot-shell. It may describe future allowed file families, handoff contracts, validation gates, rollback checkpoints, and stop conditions. It must remain design metadata only and must not edit consumer repositories, wire shells, call adapter symbols, import consumer runtimes, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN.md`
- `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g36_bounded_consumer_integration_design.json`
- `tests/test_v1_g36_bounded_consumer_integration_design.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G36.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G36.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G36 may add only deterministic LIMA-side docs/tests/fixtures that define candidate bounded integration design metadata.

Allowed if approved:

- add one LIMA-side bounded integration design fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side bounded integration design test
- define future integration boundary categories without implementing them
- define future candidate file-map categories without editing files in those categories
- define required future gates for patch preview, consumer repo edits, shell wiring, provider/model dispatch, connector/browser/network authority, and physical-world authority
- link V1-G35 compatibility review evidence, audit, authority-chain audit, readiness rollup, and next-lane matrix
- enforce no runtime file change confirmation
- enforce no consumer repo mutation confirmation
- enforce no adapter symbol execution confirmation
- enforce no consumer runtime module import confirmation
- enforce no shell wiring implementation confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw sensitive content persistence in LIMA evidence
- enforce proof-not-integration-authority and proof-not-product-readiness confirmations

## Explicitly Forbidden

V1-G36 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer test files
- consumer runtime/source file edits
- consumer runtime module imports
- calls to LIMA adapter symbols
- fake call envelope execution
- consumer integration
- shell runtime wiring implementation
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

- LIMA bounded integration design fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved LIMA docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell files are changed
- Sparkbot bounded design record exists and remains design-only
- Arc-Bot-shell bounded design record exists and remains design-only
- V1-G35 compatibility review evidence is linked
- future patch-preview, consumer-edit, shell-wiring, provider/model, connector/browser/network, physical-world, and product-readiness gates remain blocked
- no adapter symbols are called
- no consumer runtime modules are imported
- no shell wiring, provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-sensitive-content persistence is added to LIMA evidence
- proof-not-integration-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G36 tests
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
- Sparkbot focused V1-G31 fake-runtime consumer call preview test
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G34 live consumer import/call test
- Arc-Bot-shell focused V1-G31 fake-runtime consumer call preview test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run live provider/model calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G36 docs/tests/fixtures:

- `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN.md`
- `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g36_bounded_consumer_integration_design.json`
- `tests/test_v1_g36_bounded_consumer_integration_design.py`

Rollback must not require `lima/` runtime file changes, consumer repository changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G36 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell file edits are required
- consumer runtime/source file edits are required
- adapter symbols are called
- consumer runtime modules are imported
- consumer integration is added
- shell runtime wiring implementation is added
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
- Bounded consumer integration design approved: no.
- Bounded consumer integration design added: no.
- Consumer integration approved: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer runtime/source files changed by this request: no.
- Adapter symbols called: no.
- Consumer runtime modules imported: no.
- Shell runtime wiring implementation added: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Raw sensitive content persisted in LIMA evidence: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g36-bounded-consumer-integration-design` in LIMA-AI-OS. Implement only the exact bounded consumer integration design slice. Do not edit runtime files, edit consumer repos, wire shells, call providers/models, access secrets, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
