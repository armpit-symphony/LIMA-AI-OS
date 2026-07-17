# V1-G42 Shell Wiring Implementation Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g42-shell-wiring-implementation-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create shell wiring implementation test files, call adapter symbols, import consumer runtime modules, wire runtime shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G42 implementation of the shell wiring implementation slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G41, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G42 Objective

Implement the smallest approved bounded shell wiring implementation evidence slice.

The slice should add exact static shell wiring implementation test/fixture files to Sparkbot and Arc-Bot-shell, plus deterministic LIMA-side docs/tests/fixtures evidence. It must not edit consumer runtime/source files beyond the exact approved test/fixture paths, wire runtime shells, call adapter symbols from LIMA implementation code, import consumer runtimes, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G42_SHELL_WIRING_IMPLEMENTATION.md`
- `docs/V1_G42_SHELL_WIRING_IMPLEMENTATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g42_shell_wiring_implementation.json`
- `tests/test_v1_g42_shell_wiring_implementation.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g42_shell_wiring_implementation.json`
- `tests/test_sparkbot_lima_v1_g42_shell_wiring_implementation.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g42_shell_wiring_implementation.json`
- `tests/test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G42.

No Sparkbot or Arc-Bot-shell files outside the exact approved test/fixture paths above may be created, edited, removed, or renamed in V1-G42.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G42 may add only deterministic LIMA-side docs/tests/fixtures plus the exact approved Sparkbot and Arc-Bot-shell static test/fixture files.

Allowed if approved:

- add one LIMA-side shell wiring implementation evidence fixture
- add one focused LIMA-side shell wiring implementation evidence test
- add one Sparkbot static shell wiring implementation fixture
- add one Sparkbot static shell wiring implementation test
- add one Arc-Bot-shell static shell wiring implementation fixture
- add one Arc-Bot-shell static shell wiring implementation test
- run the approved local static consumer tests
- reference the V1-G41 consumer integration implementation records
- reference the V1-G40 shell boundary design records
- link V1-G41 implementation evidence, audit, authority-chain audit, readiness rollup, and next-lane matrix
- record saved Sparkbot and Arc-Bot-shell commit evidence after edits
- enforce no `lima/` runtime file change confirmation
- enforce no consumer runtime/source file change confirmation outside exact approved paths
- enforce no adapter symbol execution confirmation unless a future gate approves it
- enforce no consumer runtime module import confirmation
- enforce no runtime shell wiring execution confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw sensitive content persistence in LIMA evidence
- enforce proof-not-live-dispatch-authority and proof-not-product-readiness confirmations

## Explicitly Forbidden

V1-G42 must not add:

- `lima/` runtime file changes
- Sparkbot file edits outside the exact approved paths
- Arc-Bot-shell file edits outside the exact approved paths
- consumer runtime/source file edits outside the exact approved paths
- raw patch body persistence in LIMA evidence
- unapproved patch application
- consumer runtime module imports
- calls to LIMA adapter symbols
- fake call envelope execution
- runtime shell wiring execution
- live provider/model calls
- model request dispatch
- fallback execution
- secret lookup
- credential access
- connector behavior
- browser or network behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures and consumer test/fixture files
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

- LIMA shell wiring implementation fixture records `CANDIDATE_ONLY`
- LIMA files are limited to approved docs/tests/fixtures
- Sparkbot files are limited to the exact approved test/fixture files
- Arc-Bot-shell files are limited to the exact approved test/fixture files
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell runtime/source files are changed
- Sparkbot shell wiring implementation evidence record exists and remains static-test-only
- Arc-Bot-shell shell wiring implementation evidence record exists and remains static-test-only
- V1-G41 consumer integration implementation evidence is linked
- V1-G40 shell boundary design evidence is linked
- no raw patch bodies are persisted in LIMA evidence
- provider/model, connector/browser/network, physical-world, and product-readiness gates remain blocked
- no adapter symbols are called
- no consumer runtime modules are imported
- no runtime shell wiring execution, provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-sensitive-content persistence is added to LIMA evidence
- proof-not-live-dispatch-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G42 tests
- LIMA focused V1-G41 tests
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
- Sparkbot focused V1-G42 shell wiring implementation test
- Sparkbot focused V1-G41 consumer integration implementation test
- Sparkbot focused V1-G39 consumer integration import-smoke test
- Sparkbot focused V1-G38 consumer integration candidate test
- Sparkbot focused V1-G34 live consumer import/call test
- Sparkbot focused V1-G31 fake-runtime consumer call preview test
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G42 shell wiring implementation test
- Arc-Bot-shell focused V1-G41 consumer integration implementation test
- Arc-Bot-shell focused V1-G39 consumer integration import-smoke test
- Arc-Bot-shell focused V1-G38 consumer integration candidate test
- Arc-Bot-shell focused V1-G34 live consumer import/call test
- Arc-Bot-shell focused V1-G31 fake-runtime consumer call preview test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run live provider/model calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G42 docs/tests/fixtures and consumer test/fixture files:

LIMA-AI-OS:

- `docs/V1_G42_SHELL_WIRING_IMPLEMENTATION.md`
- `docs/V1_G42_SHELL_WIRING_IMPLEMENTATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g42_shell_wiring_implementation.json`
- `tests/test_v1_g42_shell_wiring_implementation.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g42_shell_wiring_implementation.json`
- `tests/test_sparkbot_lima_v1_g42_shell_wiring_implementation.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g42_shell_wiring_implementation.json`
- `tests/test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py`

Rollback must not require `lima/` runtime file changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G42 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell file edits outside exact approved paths are required
- consumer runtime/source file edits outside exact approved paths are required
- raw patch bodies are persisted in LIMA evidence
- unapproved patches are applied
- adapter symbols are called
- consumer runtime modules are imported
- runtime shell wiring execution is added
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
- Shell wiring implementation approved: no.
- Shell wiring implementation added: no.
- Shell wiring design evidence exists: yes.
- Consumer integration implementation evidence exists: yes.
- Runtime shell wiring execution approved: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer runtime/source files changed by this request: no.
- Raw patch bodies persisted: no.
- Patches applied: no.
- Adapter symbols called: no.
- Consumer runtime modules imported: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Raw sensitive content persisted in LIMA evidence: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g42-shell-wiring-implementation` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell as needed. Implement only the exact shell wiring implementation evidence slice. Do not edit runtime files, edit unapproved consumer files, call providers/models, access secrets, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
