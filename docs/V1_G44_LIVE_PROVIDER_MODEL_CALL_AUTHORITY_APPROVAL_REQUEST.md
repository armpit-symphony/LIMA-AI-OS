# V1-G44 Live Provider Model Call Authority Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g44-live-provider-model-call-authority-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, call providers/models, execute live model requests, make network calls, read secrets, access credential values, run provider readiness checks, execute fallback, activate Token Guardian live routing, edit Sparkbot, edit Arc-Bot-shell, import consumer runtime modules, wire runtime shells, call adapter symbols, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw prompts, raw model responses, raw customer data, raw secrets, raw credentials, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G44 implementation of the live provider/model call authority metadata/preflight slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G43, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G44 Objective

Implement the smallest LIMA-side live provider/model call authority metadata/preflight slice.

The requested future implementation should add a deterministic local validator for live provider/model call authority packets. The validator may prove that a future live provider/model call has the required Guardian decision, approval evidence, audit evidence, provider/model route reference, credential reference metadata, network policy reference metadata, redacted prompt reference, output handling policy, budget/cost class, and proof-not-execution confirmations.

The slice must not execute a live provider/model call, dispatch a model request, make a network call, read or emit secrets, access credential values, run provider readiness network checks, execute fallback, activate Token Guardian live routing, execute tools, mutate files, invoke connectors, use browser/network/device/robotics/physical-world behavior, or claim product readiness.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/harness/v1_live_provider_model_call_authority.py` (new)
- `lima/harness/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md`
- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g44_live_provider_model_call_authority.json`
- `tests/test_v1_g44_live_provider_model_call_authority.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Required Artifact Fields If Approved

Each live provider/model call authority packet should provide metadata for:

- authority id
- request id or Guardian decision id linkage
- tenant scope
- shell scope
- actor scope
- session scope
- source provider/model route authority reference
- source provider/model dispatch evidence reference
- provider id
- model id
- model role
- provider boundary metadata
- credential reference metadata
- network policy reference metadata
- prompt reference metadata without raw prompts
- output handling policy without raw model responses
- data sensitivity
- budget class
- estimated cost class
- latency tier
- approval evidence linkage
- audit/evidence linkage
- proof-not-execution confirmation
- no raw prompt/model-response/customer-data confirmation
- no secret lookup confirmation
- no credential value access confirmation
- no network call confirmation
- no live provider call execution confirmation
- no fallback execution confirmation

## Allowed Behavior If Approved

V1-G44 may add only deterministic local non-executing live provider/model call authority metadata validation.

Allowed if approved:

- add a candidate runtime validator for live provider/model call authority metadata
- add candidate exports in `lima/harness/__init__.py`
- validate request id or GuardianDecision linkage
- validate tenant, shell, actor, and session scope metadata
- validate provider/model route authority evidence linkage
- validate provider/model dispatch evidence linkage
- validate provider id, model id, model role, and provider boundary metadata
- validate credential reference metadata without looking up, reading, emitting, or persisting secret values
- validate network policy reference metadata without performing network calls
- validate redacted prompt reference metadata without accepting raw prompts
- validate output handling policy metadata without accepting raw model responses
- validate budget, cost, latency, approval evidence, and audit evidence metadata
- validate proof-not-execution confirmations
- reject raw prompts, raw model responses, raw customer data, credentials, secrets, provider tokens, and API keys
- reject live provider/model call execution claims
- reject network call claims
- reject secret lookup and credential value access claims
- reject fallback execution claims
- reject connector/browser/network/device/robotics/physical-world claims

## Explicitly Forbidden

V1-G44 must not add:

- live provider/model call execution
- actual model request dispatch execution
- network calls
- provider readiness network checks
- Token Guardian live routing
- secret lookup
- credential value access
- raw credential persistence
- provider token persistence
- raw prompt persistence
- raw model response persistence
- raw customer data persistence
- fallback execution
- tool execution
- action execution
- file mutation execution
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- runtime shell wiring execution
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
- required live provider/model call authority metadata fields are enforced
- request or GuardianDecision linkage is required
- tenant/shell/actor/session scope is required
- V1-G20 provider/model routing authority evidence is linked
- V1-G43 provider/model dispatch evidence is linked
- provider/model identity metadata is required
- credential metadata is reference-only and cannot read or include raw secrets
- network policy metadata is reference-only and cannot make network calls
- prompt metadata is reference-only and cannot include raw prompts
- output policy metadata is required and cannot include raw model responses
- approval evidence linkage is required
- audit/evidence linkage is required
- proof-not-execution confirmation is enforced
- raw prompts, raw model responses, raw customer data, credentials, provider tokens, API keys, and secrets fail closed
- live provider/model call execution claims fail closed
- network call claims fail closed
- secret lookup and credential value access claims fail closed
- fallback execution claims fail closed
- connector/browser/network/device/robotics/physical-world claims fail closed

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G44 live provider/model call authority tests
- LIMA focused V1-G43 provider/model dispatch tests
- LIMA focused V1-G20 provider/model routing authority tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run live provider/model calls, network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only:

- `lima/harness/v1_live_provider_model_call_authority.py`
- V1-G44 candidate exports added to `lima/harness/__init__.py`
- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md`
- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g44_live_provider_model_call_authority.json`
- `tests/test_v1_g44_live_provider_model_call_authority.py`

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, Arc-Bot-shell changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G44 files
- live provider/model call execution is added
- actual model request dispatch execution is added
- network calls are added
- provider readiness network checks are added
- Token Guardian live routing is added
- secret lookup is added
- credential values or provider tokens are accessed, persisted, or emitted
- raw prompts, raw model responses, or raw customer data can persist or emit
- authority metadata can grant execution authority
- fallback execution is added
- tool execution is added
- action execution is added
- file mutation execution is added
- consumer repo work is required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Live provider/model call authority behavior added: no.
- Live provider/model call execution added: no.
- Actual model request dispatch execution added: no.
- Network call added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Provider readiness checks added: no.
- Fallback execution added: no.
- Token Guardian live routing added: no.
- Tool execution added: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g44-live-provider-model-call-authority` and implement only the LIMA-side non-executing live provider/model call authority metadata/preflight slice. Do not call model providers, make network calls, read secrets, access credential values, dispatch model requests, execute fallback, execute tools, touch consumer repos, or claim product readiness.
