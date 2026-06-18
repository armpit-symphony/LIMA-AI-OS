# V1-G40 Shell Wiring Design Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g40-shell-wiring-design-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create shell wiring design files, implement shell wiring, implement consumer integration, call adapter symbols, import consumer runtime modules, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G40 implementation of the shell wiring design slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G39, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G40 Objective

Implement the smallest approved LIMA-side shell wiring design slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that map future Sparkbot and Arc-Bot-shell shell wiring boundaries without implementing shell runtime wiring, editing consumer repositories, importing consumer runtimes, calling adapter symbols, calling providers/models, accessing credentials, invoking connectors, using network/browser/device/robotics/physical-world behavior, or claiming product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G40_SHELL_WIRING_DESIGN.md`
- `docs/V1_G40_SHELL_WIRING_DESIGN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g40_shell_wiring_design.json`
- `tests/test_v1_g40_shell_wiring_design.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G40.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G40.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G40 may add only deterministic LIMA-side docs/tests/fixtures.

Allowed if approved:

- add one LIMA-side shell wiring design evidence fixture
- add one focused LIMA-side shell wiring design evidence test
- add shell boundary map metadata for Sparkbot and Arc-Bot-shell
- link V1-G39 import-smoke evidence, audit, authority-chain audit, readiness rollup, and next-lane matrix
- enforce no `lima/` runtime file change confirmation
- enforce no consumer repository edit confirmation
- enforce no consumer runtime/source file change confirmation
- enforce no adapter symbol execution confirmation unless a future gate approves it
- enforce no consumer runtime module import confirmation
- enforce no consumer integration implementation confirmation
- enforce no shell wiring implementation confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw sensitive content persistence in LIMA evidence
- enforce proof-not-shell-wiring-implementation, proof-not-integration-authority, and proof-not-product-readiness confirmations

## Explicitly Forbidden

V1-G40 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer runtime/source file edits
- raw patch body persistence in LIMA evidence
- unapproved patch application
- consumer runtime module imports
- calls to LIMA adapter symbols
- fake call envelope execution
- consumer integration implementation
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

- LIMA shell wiring design fixture records `CANDIDATE_ONLY`
- LIMA files are limited to approved docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot files are changed
- no Arc-Bot-shell files are changed
- no consumer runtime/source files are changed
- shell boundary map records exist for Sparkbot and Arc-Bot-shell
- V1-G39 import-smoke evidence is linked
- no raw patch bodies are persisted in LIMA evidence
- consumer integration, shell wiring implementation, provider/model, connector/browser/network, physical-world, and product-readiness gates remain blocked
- no adapter symbols are called
- no consumer runtime modules are imported
- no shell wiring implementation, provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-sensitive-content persistence is added to LIMA evidence
- proof-not-shell-wiring-implementation and proof-not-integration-authority confirmations are enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G40 tests
- LIMA focused V1-G39 tests
- LIMA focused V1-G38 tests
- LIMA focused V1-G37 tests
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
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run live provider/model calls, connector calls, browser/network calls, migrations, services, workers, production deploys, consumer repository edits, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G40 docs/tests/fixtures:

LIMA-AI-OS:

- `docs/V1_G40_SHELL_WIRING_DESIGN.md`
- `docs/V1_G40_SHELL_WIRING_DESIGN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g40_shell_wiring_design.json`
- `tests/test_v1_g40_shell_wiring_design.py`

Rollback must not require `lima/` runtime file changes, consumer repository repair, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G40 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell file edits are required
- consumer runtime/source file edits are required
- raw patch bodies are persisted in LIMA evidence
- unapproved patches are applied
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
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Shell wiring design approved: no.
- Shell wiring design added: no.
- Shell wiring implementation approved: no.
- Consumer integration approved: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer runtime/source files changed by this request: no.
- Raw patch bodies persisted: no.
- Patches applied: no.
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

If approved, create branch `v1-g40-shell-wiring-design` in LIMA-AI-OS as needed. Implement only the exact shell wiring design slice. Do not edit runtime files, edit consumer repositories, implement consumer integration, implement shell wiring, call providers/models, access secrets, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
