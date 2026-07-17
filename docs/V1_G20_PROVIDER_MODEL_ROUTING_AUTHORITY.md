# V1-G20 Provider Model Routing Authority

Date: 2026-06-17
Branch: `v1-g20-provider-model-routing-authority`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_provider_model_routing_authority_slice`

V1-G20 implements the approved LIMA-side provider/model routing authority metadata slice. It validates sanitized provider/model route intent, fallback posture, tool-pack scope, budget/cost class, credential-reference metadata, GuardianDecision linkage, approval evidence linkage, and audit evidence linkage for later Guardian/Harness review.

This implementation does not call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, run provider readiness checks, activate Token Guardian live routing, execute tools, mutate files, touch consumer repositories, import consumer code, call consumer runtimes, wire consumers, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G20` template.

Approved implementation branch:

- `v1-g20-provider-model-routing-authority`

Approved runtime scope:

- `provider_model_routing_authority_metadata_slice`

## Runtime Files

- `lima/harness/v1_provider_model_routing_authority.py`
- `lima/harness/__init__.py`

## Runtime Symbols

- `V1ProviderModelRoutingAuthorityError`
- `validate_v1_provider_model_routing_authority`

## Behavior Added

V1-G20 adds one deterministic local provider/model routing authority metadata validator:

- requires route id, route family, and route intent scope metadata
- requires request id or Guardian decision id linkage
- requires tenant, shell, actor, and session scope metadata
- requires provider id, model id, model role, and provider boundary metadata
- requires data sensitivity and prompt context class metadata without raw prompts
- requires requested and allowed tool-pack scope metadata
- rejects requested tool packs that exceed allowed tool packs
- requires credential reference metadata without secret lookup or raw credential values
- requires budget, cost, and latency metadata
- requires fallback chain metadata
- requires fallback candidates to inherit the same gates
- requires approval evidence linkage when risk policy requires approval
- requires provider configuration reference metadata
- requires audit/evidence linkage metadata
- requires proof-not-authority confirmation
- requires no raw prompt/secret/credential/customer-data confirmation
- requires no secret lookup confirmation
- requires no live provider call confirmation
- requires no execution-authority confirmation
- returns a deterministic `record_hash`
- keeps live routing, provider/model calls, model dispatch, fallback execution, provider readiness checks, Token Guardian live routing, secret lookup, credential access, tool execution, file mutation, consumer integration, connector/browser/network/device/robotics/physical-world, final freeze, and product readiness flags false

## Required Distinction

V1-G20 separates:

- sanitized provider/model routing authority metadata: implemented as validation
- raw prompts, customer context, secrets, credentials, provider tokens, and API keys: not accepted
- credential reference metadata: accepted only as reference metadata
- secret lookup: not approved and not implemented
- live provider/model calls: not approved and not implemented
- fallback execution: not approved and not implemented
- model execution or dispatch authority: not approved and not implemented
- consumer integration: not approved and not implemented

## Fail-Closed Cases

The validator rejects:

- missing route metadata fields
- missing request or GuardianDecision linkage
- linkage metadata that claims authority
- unbound route intent scope
- route intent metadata that grants execution
- unsupported route families
- unsupported model roles
- unsupported data sensitivity values
- unsupported prompt context classes
- unsupported budget, cost, or latency values
- provider boundary metadata that is not configured for scope
- live provider call claims
- provider readiness network check claims
- credential lookup claims
- provider boundary metadata that claims authority
- requested tool packs outside allowed tool-pack scope
- credential metadata without a reference or no-key-local confirmation
- credential metadata that is not reference-only
- secret lookup claims
- raw secret or credential value claims
- fallback chains that do not inherit the same gates
- fallback candidates that perform secret lookup, allow live provider calls, or allow fallback execution
- missing approval evidence when risk policy requires approval
- stale approval evidence when risk policy requires current approval
- approval evidence metadata that claims authority
- missing audit/evidence linkage
- audit/evidence metadata that claims authority
- missing proof-not-authority confirmation
- missing no raw prompt/secret/credential/customer-data confirmation
- missing no secret lookup confirmation
- missing no live provider call confirmation
- missing no execution-authority confirmation
- raw prompts, raw customer data, credentials, provider tokens, API keys, secrets, and raw model responses
- live provider/model call claims
- model request dispatch claims
- Token Guardian live routing claims
- tool execution claims
- consumer repo mutation, consumer imports/calls, connector/browser/network/device/robotics/physical-world claims

## Boundaries

- Runtime behavior added: yes, only the approved non-executing provider/model routing authority metadata validator.
- Live provider/model routing added: no.
- Provider/model calls added: no.
- Model request dispatch added: no.
- Fallback execution added: no.
- Provider readiness checks added: no.
- Token Guardian live routing added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution added: no.
- Consumer repo mutation added: no.
- Consumer code import added: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- Product readiness approved: no.

## Readiness Result

V1-G20 is ready for independent audit.

The next smallest safe step is a separate V1-G20 audit branch. Do not proceed to live provider/model calls, secret lookup, model dispatch, fallback execution, consumer integration, shell wiring, connector/browser/network authority, final API freeze, physical-world authority, or product-readiness claims from this implementation branch.
