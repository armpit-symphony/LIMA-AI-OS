# V1-G20 Provider Model Routing Authority Approval Request

Date: 2026-06-16
Branch: `prepare-v1-g20-provider-model-routing-authority-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, route providers/models, call model providers, read secrets, access credentials, run provider readiness checks, activate Token Guardian live routing, execute tools, mutate files, touch consumer repositories, import consumer code, wire consumers, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G20 implementation of the LIMA-side provider/model routing authority metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G19, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G20 Objective

Implement the smallest LIMA-side provider/model routing authority metadata slice.

The slice should define how LIMA validates sanitized provider/model route intent, fallback posture, tool-pack scope, budget/cost class, credential-reference metadata, GuardianDecision linkage, approval evidence linkage, and audit evidence linkage without making live provider calls, reading secrets, dispatching model requests, or wiring consumer runtimes.

Provider/model routing families covered:

- primary model route
- backup fallback route
- heavy hitter route
- agent override route
- workstation model seat route
- local endpoint route
- Codex subscription route
- provider readiness self-inspection route as metadata only

## Required Artifact Fields

Each provider/model routing authority packet should provide metadata for:

- route id
- route family
- route intent scope
- request id or Guardian decision id linkage
- tenant scope
- shell scope
- actor scope
- session scope
- provider id
- model id
- model role
- provider boundary metadata
- data sensitivity
- prompt context class
- requested tool packs
- allowed tool packs
- credential reference metadata
- budget class
- estimated cost class
- latency tier
- fallback chain metadata
- approval evidence linkage when required by risk policy
- provider configuration reference
- audit evidence linkage
- proof-not-authority confirmation
- no raw prompt/secret/credential/customer-data confirmation
- no secret lookup confirmation
- no live provider call confirmation
- no execution-authority confirmation

## Required Distinction

V1-G20 must clearly separate:

- sanitized provider/model routing authority metadata
- raw prompts, raw customer context, secrets, credentials, and provider tokens
- credential reference metadata versus secret lookup
- route eligibility proof versus a live provider/model call
- route metadata versus model execution
- route metadata versus consumer integration

Provider/model routing authority metadata remains proof for a later Guardian-controlled Harness decision. It is not a live model call, provider dispatch, fallback execution, credential lookup, tool execution, or broad runtime authority by itself.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/harness/v1_provider_model_routing_authority.py` (new)
- `lima/harness/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY.md`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g20_provider_model_routing_authority.json`
- `tests/test_v1_g20_provider_model_routing_authority.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G20 may add only deterministic local non-executing provider/model routing authority metadata validation.

Allowed if approved:

- validate route id, route family, and route intent scope metadata
- validate request id or Guardian decision id linkage
- validate tenant, shell, actor, and session scope metadata
- validate provider id, model id, model role, and provider boundary metadata
- validate data sensitivity and prompt context class metadata without accepting raw prompts
- validate requested and allowed tool-pack scope metadata
- validate credential reference metadata without looking up, reading, or persisting secrets
- validate budget, cost, and latency metadata
- validate fallback chain metadata and require fallback candidates to inherit the same gates
- validate approval evidence linkage when required by risk policy
- validate provider configuration reference metadata without live readiness checks
- validate audit/evidence linkage metadata
- validate proof-not-authority confirmation
- reject raw prompts, raw customer data, credentials, secrets, provider tokens, and API keys
- prove route metadata cannot call providers/models, read secrets, execute tools, mutate files, call consumers, invoke connectors/browser/network/device/robotics/physical-world behavior, or claim final readiness

## Explicitly Forbidden

V1-G20 must not add:

- live provider/model calls
- model request dispatch
- fallback execution
- provider readiness network checks
- Token Guardian live routing
- secret lookup
- credential access
- provider token persistence
- raw prompt persistence
- raw customer context persistence
- tool execution
- action execution
- file mutation execution
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- final API freeze
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- fixture records `CANDIDATE_ONLY`
- required provider/model route metadata fields are enforced
- request or GuardianDecision linkage is required
- tenant/shell/actor/session scope is required
- provider/model identity metadata is required
- route family and route intent scope are required
- tool-pack scope is required and cannot exceed shell/decision scope
- credential metadata is reference-only and cannot read or include raw secrets
- budget/cost/latency metadata is required
- fallback chain candidates inherit the same gates
- approval evidence linkage is required when risk policy requires approval
- audit/evidence linkage is required
- proof-not-authority confirmation is enforced
- raw prompts, raw customer data, credentials, provider tokens, API keys, and secrets fail closed
- live provider/model call claims fail closed
- secret lookup claims fail closed
- Token Guardian live routing claims fail closed
- provider readiness network check claims fail closed
- consumer repo mutation, consumer imports/calls, connector/browser/network/device/robotics/physical-world claims fail closed

## Rollback Plan If Approved

Rollback must remove only:

- `lima/harness/v1_provider_model_routing_authority.py`
- V1-G20 candidate exports added to `lima/harness/__init__.py`
- V1-G20 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G20 files
- live provider/model calls are added
- model request dispatch is added
- fallback execution is added
- provider readiness network checks are added
- Token Guardian live routing is added
- secret lookup is added
- credentials or provider tokens are accessed, persisted, or emitted
- raw prompts or raw customer data can persist or emit
- route metadata can grant execution authority
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
- final API freeze is claimed
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Provider/model routing authority behavior added: no.
- Live provider/model routing added: no.
- Provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Token Guardian live routing added: no.
- Provider readiness checks added: no.
- Execution authority added: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Final API freeze approved: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g20-provider-model-routing-authority` and implement only the LIMA-side provider/model routing authority metadata slice. Do not call model providers, read secrets, route live requests, execute tools, or touch consumer repos.
