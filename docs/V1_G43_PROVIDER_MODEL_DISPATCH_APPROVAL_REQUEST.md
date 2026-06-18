# V1-G43 Provider Model Dispatch Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g43-provider-model-dispatch-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create provider/model dispatch evidence files, call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, run provider readiness checks, activate Token Guardian live routing, call adapter symbols, import consumer runtime modules, wire runtime shells, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw prompts, raw model responses, raw customer data, raw secrets, or raw credentials in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G43 implementation of the provider/model dispatch slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G42, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G43 Objective

Implement the smallest bounded provider/model dispatch evidence slice after V1-G42 shell wiring implementation evidence.

The requested future implementation should add deterministic fake-provider/no-secret provider/model dispatch evidence as LIMA-side docs/tests/fixtures only. It must prove that provider/model dispatch remains candidate-only and does not perform live provider calls, real model request dispatch, fallback execution, secret lookup, credential access, provider readiness network checks, Token Guardian live routing, tool execution, connector/browser/network behavior, consumer repo edits, runtime shell wiring execution, physical-world behavior, or product-readiness claims.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G43_PROVIDER_MODEL_DISPATCH.md`
- `docs/V1_G43_PROVIDER_MODEL_DISPATCH_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g43_provider_model_dispatch.json`
- `tests/test_v1_g43_provider_model_dispatch.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G43.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G43.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G43 may add only deterministic LIMA-side docs/tests/fixtures for fake-provider/no-secret provider/model dispatch evidence.

Allowed if approved:

- add one LIMA-side provider/model dispatch evidence fixture
- add one focused LIMA-side provider/model dispatch evidence test
- add one provider/model dispatch evidence doc
- add one provider/model dispatch closeout doc
- reference the V1-G20 provider/model routing authority metadata records
- reference the V1-G42 shell wiring implementation records
- link V1-G42 implementation evidence, audit, authority-chain audit, readiness rollup, and next-lane matrix
- record fake-provider/no-secret dispatch evidence as candidate-only
- enforce no live provider/model call confirmation
- enforce no model request dispatch execution confirmation
- enforce no fallback execution confirmation
- enforce no secret lookup or credential access confirmation
- enforce no provider readiness network check confirmation
- enforce no Token Guardian live routing confirmation
- enforce no consumer repo edit confirmation
- enforce no consumer runtime import or call confirmation
- enforce no runtime shell wiring execution confirmation
- enforce no connector/browser/network/file/device/robotics/physical-world behavior confirmation
- enforce no raw prompt, raw model response, raw customer data, raw secret, or raw credential persistence in LIMA evidence
- enforce proof-not-live-provider-authority, proof-not-secret-authority, and proof-not-product-readiness confirmations

## Explicitly Forbidden

V1-G43 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer runtime/source file edits
- raw prompt persistence
- raw model response persistence
- raw customer data persistence
- raw secret or raw credential persistence
- raw patch body persistence
- unapproved patch application
- provider/model live calls
- actual model request dispatch execution
- fallback execution
- provider readiness network checks
- Token Guardian live routing
- secret lookup
- credential access
- tool execution
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures
- adapter symbol calls
- consumer runtime module imports
- runtime shell wiring execution
- connector behavior
- browser or network behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- HumanInput bridge activation
- scheduled task execution
- external sends
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA provider/model dispatch fixture records `CANDIDATE_ONLY`
- LIMA files are limited to approved docs/tests/fixtures
- no consumer repository files are changed
- no `lima/` runtime files are changed
- V1-G20 provider/model routing authority metadata evidence is linked
- V1-G42 shell wiring implementation evidence is linked
- fake-provider/no-secret dispatch evidence is deterministic and candidate-only
- live provider/model calls remain blocked
- actual model request dispatch execution remains blocked
- fallback execution remains blocked
- provider readiness network checks remain blocked
- Token Guardian live routing remains blocked
- secret lookup and credential access remain blocked
- no raw prompt, raw model response, raw customer data, raw secret, raw credential, or raw patch body is persisted in LIMA evidence
- no adapter symbols are called
- no consumer runtime modules are imported
- no runtime shell wiring execution, connector/browser/network/device/robotics/physical-world behavior, external sends, or product-readiness claims are approved
- proof-not-live-provider-authority and proof-not-product-readiness confirmations are enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G43 provider/model dispatch tests
- LIMA focused V1-G42 shell wiring implementation tests
- LIMA focused V1-G41 consumer integration implementation tests
- LIMA focused V1-G40 shell wiring design tests
- LIMA focused V1-G20 provider/model routing authority tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run live provider/model calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G43 docs/tests/fixtures:

LIMA-AI-OS:

- `docs/V1_G43_PROVIDER_MODEL_DISPATCH.md`
- `docs/V1_G43_PROVIDER_MODEL_DISPATCH_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g43_provider_model_dispatch.json`
- `tests/test_v1_g43_provider_model_dispatch.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Rollback must not require `lima/` runtime file changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G43 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell edits are required
- consumer runtime/source edits are required
- raw prompts, raw model responses, raw customer data, raw secrets, or raw credentials are persisted in LIMA evidence
- raw patch bodies are persisted in LIMA evidence
- unapproved patches are applied
- live provider/model calls are added
- actual model request dispatch execution is added
- fallback execution is added
- provider readiness network checks are added
- Token Guardian live routing is added
- secret lookup or credential access is added
- tool execution is added
- adapter symbols are called
- consumer runtime modules are imported
- runtime shell wiring execution is added
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
- Provider/model dispatch approved: no.
- Provider/model dispatch evidence added: no.
- Live provider/model calls approved: no.
- Actual model request dispatch execution approved: no.
- Fallback execution approved: no.
- Secret lookup approved: no.
- Credential access approved: no.
- Provider/model routing authority metadata evidence exists: yes.
- Shell wiring implementation evidence exists: yes.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer runtime/source files changed by this request: no.
- Raw prompt or raw model response persisted: no.
- Raw secret or raw credential persisted: no.
- Raw patch bodies persisted: no.
- Patches applied: no.
- Adapter symbols called: no.
- Consumer runtime modules imported: no.
- Runtime shell wiring execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g43-provider-model-dispatch` in LIMA-AI-OS only. Implement only the exact fake-provider/no-secret provider/model dispatch evidence slice. Do not edit runtime files, edit consumer repos, call providers/models, access secrets, execute real dispatch or fallback, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
