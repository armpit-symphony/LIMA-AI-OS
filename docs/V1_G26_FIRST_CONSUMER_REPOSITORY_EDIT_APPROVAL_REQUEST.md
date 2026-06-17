# V1-G26 First Consumer Repository Edit Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g26-first-consumer-repository-edit-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit LIMA runtime files, edit Sparkbot, edit Arc-Bot-shell, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G26 implementation of the first consumer repository edit slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G25, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G26 Objective

Implement the smallest first consumer repository edit slice.

The slice should add static, non-executing consumer-side proof packets and focused tests in Sparkbot and Arc-Bot-shell, plus LIMA-side docs/tests/fixtures that intake those static proof records. It must not add live LIMA imports, live consumer runtime calls, runtime wiring, provider/model calls, connector behavior, raw secrets, raw diffs, or product-readiness claims.

## Read-Only Local Path Audit

Read-only inspection found existing consumer proof/test patterns:

- Sparkbot local repo: `C:\Users\limap\Sparkbot`
- Sparkbot current branch during audit: `proof-sparkbot-shell-lima-consumer-packet`
- Sparkbot existing proof patterns:
  - `docs/proof_packets/SPARKBOT_SHELL_LIMA_CONSUMER_PROOF_PACKET.md`
  - `docs/proof_packets/sparkbot_shell_lima_consumer_packet.json`
  - `tests/test_sparkbot_lima_v1_g7_integration_proof_packet.py`
- Arc-Bot-shell local repo: `C:\Users\limap\Arc-Bot-shell`
- Arc-Bot-shell current branch during audit: `v1-g7-arc-bot-shell-integration-proof-packet`
- Arc-Bot-shell existing proof patterns:
  - `docs/proof_packets/ARC_BOT_SHELL_LIMA_V1_G7_INTEGRATION_PROOF_PACKET.md`
  - `tests/fixtures/arc_bot_shell_lima_v1_g7_integration_proof_packet.json`
  - `tests/test_arc_bot_shell_lima_v1_g7_integration_proof_packet.py`
- Arc-Bot-shell status scan warning: `.pytest_cache/` could not be opened due to permission denial; V1-G26 must not read, write, remove, or rely on `.pytest_cache/`.

The proposed implementation uses static docs/tests/fixtures paths, not runtime shim paths.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT.md`
- `docs/V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g26_first_consumer_repository_edit.json`
- `tests/test_v1_g26_first_consumer_repository_edit.py`

Sparkbot docs/tests/fixtures:

- `docs/proof_packets/SPARKBOT_LIMA_V1_G26_STATIC_CONSUMER_EDIT_PACKET.md`
- `tests/fixtures/sparkbot_lima_v1_g26_static_consumer_edit_packet.json`
- `tests/test_sparkbot_lima_v1_g26_static_consumer_edit_packet.py`

Arc-Bot-shell docs/tests/fixtures:

- `docs/proof_packets/ARC_BOT_SHELL_LIMA_V1_G26_STATIC_CONSUMER_EDIT_PACKET.md`
- `tests/fixtures/arc_bot_shell_lima_v1_g26_static_consumer_edit_packet.json`
- `tests/test_arc_bot_shell_lima_v1_g26_static_consumer_edit_packet.py`

No `lima/` runtime files may be created or edited in V1-G26.

No Sparkbot or Arc-Bot-shell runtime/source files may be created or edited in V1-G26. Consumer repository edits are limited to the exact static docs/tests/fixtures files above.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G26 may add only deterministic local docs/tests/fixtures that describe and validate static consumer-side proof records.

Allowed if approved:

- add one Sparkbot static consumer edit proof packet
- add one Sparkbot focused static proof test
- add one Sparkbot proof fixture
- add one Arc-Bot-shell static consumer edit proof packet
- add one Arc-Bot-shell focused static proof test
- add one Arc-Bot-shell proof fixture
- add one LIMA-side intake evidence fixture for the two consumer proof records
- add one LIMA-side focused intake test
- link consumer proof records to V1-G18, V1-G21, V1-G22, V1-G23, V1-G24, and V1-G25 evidence
- record consumer repository edit metadata as docs/tests/fixtures-only
- enforce no live import/call confirmation
- enforce no runtime wiring confirmation
- enforce no runtime export cleanup confirmation
- enforce no raw file content, prompt, customer data, credential, provider token, API key, secret, raw diff, raw patch, or full patch content confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G26 must not add:

- `lima/` runtime file changes
- Sparkbot runtime/source edits
- Arc-Bot-shell runtime/source edits
- consumer code imports
- consumer runtime calls
- live LIMA imports from consumer repos
- consumer integration
- shell runtime wiring
- runtime export cleanup
- live provider/model calls
- model request dispatch
- secret lookup
- credential access
- tool execution
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- raw diff persistence
- full patch content persistence
- raw file content persistence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA fixture records `CANDIDATE_ONLY`
- Sparkbot proof packet exists and remains static-only
- Arc-Bot-shell proof packet exists and remains static-only
- each consumer proof record links to V1-G24 import-plan evidence and V1-G25 patch-preview evidence
- consumer repository edits are limited to approved docs/tests/fixtures
- no `lima/` runtime files are required
- no Sparkbot or Arc-Bot-shell runtime/source files are required
- no consumer code imports are added
- no live consumer runtime calls are added
- no runtime export cleanup is approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G26 tests
- LIMA focused V1-G25 tests
- LIMA focused adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G26 static proof test
- Arc-Bot-shell focused V1-G26 static proof test
- `git diff --check` in each edited repo
- `git diff --cached --check` in each edited repo before each commit
- `git status --short --branch` in each edited repo

Do not require or run live provider/model calls, live consumer runtime imports, connector calls, browser/network calls, migrations, services, workers, or production deploys.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G26 files:

- LIMA-AI-OS V1-G26 implementation docs/tests/fixtures listed above
- Sparkbot V1-G26 static proof docs/tests/fixtures listed above
- Arc-Bot-shell V1-G26 static proof docs/tests/fixtures listed above

Rollback must not require `lima/` runtime file changes, consumer runtime/source changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G26 files
- `lima/` runtime file changes are required
- Sparkbot runtime/source edits are required
- Arc-Bot-shell runtime/source edits are required
- consumer code is imported
- consumer runtime calls are added
- live LIMA imports are added from consumer repositories
- consumer integration is added
- shell runtime wiring is added
- runtime export cleanup is required
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- proof metadata can grant edit, import, execution, or integration authority
- tool execution is added
- action execution is added
- file mutation execution outside the exact approved docs/tests/fixtures files is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Consumer repository edit implementation added: no.
- `lima/` runtime files changed: no.
- Sparkbot runtime/source mutation added: no.
- Arc-Bot-shell runtime/source mutation added: no.
- Consumer docs/tests/fixtures mutation approved by this request alone: no.
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

If approved, create branch `v1-g26-first-consumer-repository-edit` in LIMA-AI-OS and matching implementation branches in Sparkbot and Arc-Bot-shell. Implement only the exact static docs/tests/fixtures consumer edit slice. Do not add runtime imports, runtime calls, shell wiring, export cleanup, provider/model calls, connector behavior, browser/network behavior, physical-world behavior, or product-readiness claims.
