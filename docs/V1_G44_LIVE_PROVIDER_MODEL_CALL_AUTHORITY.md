# V1-G44 Live Provider Model Call Authority

Date: 2026-06-17
Branch: `v1-g44-live-provider-model-call-authority`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_non_executing_live_provider_model_call_authority_slice`

V1-G44 implements the approved LIMA-side live provider/model call authority metadata/preflight slice. It adds one deterministic local validator for sanitized authority metadata that proves a future live provider/model call has the required Guardian decision, approval evidence, audit evidence, route evidence, dispatch evidence, credential reference metadata, network policy reference metadata, prompt reference metadata, output policy, budget/cost class, and proof-not-execution confirmations.

This implementation does not execute live provider/model calls, dispatch model requests, make network calls, read secrets, access credential values, run provider readiness checks, execute fallback, activate Token Guardian live routing, execute tools, mutate files, edit Sparkbot, edit Arc-Bot-shell, import consumer runtime modules, call adapter symbols, wire runtime shells, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw prompts, raw model responses, raw customer data, raw secrets, raw credentials, raw patch bodies, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G44` template.

Approved implementation branch:

- `v1-g44-live-provider-model-call-authority`

Approved scope:

- `live_provider_model_call_authority_metadata_preflight_slice`

## Runtime Files

- `lima/harness/v1_live_provider_model_call_authority.py`

## Module-Local Runtime Symbols

- `V1LiveProviderModelCallAuthorityError`
- `validate_v1_live_provider_model_call_authority`

## Public Export Status

V1-G44 leaves frozen `lima.harness.__all__` unchanged. The V1-G22 final public API freeze remains active, and V1-G44 did not approve a refresh of `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`.

The new validator is importable from `lima.harness.v1_live_provider_model_call_authority`. Exporting it through `lima.harness.__all__` requires a future exact runtime export cleanup or public API freeze refresh gate.

## Behavior Added

V1-G44 adds one deterministic local non-executing live provider/model call authority metadata validator:

- requires authority id metadata
- requires request id or GuardianDecision linkage
- requires tenant, shell, actor, and session scope metadata
- requires V1-G20 provider/model route authority evidence linkage
- requires V1-G43 provider/model dispatch evidence linkage
- requires provider id, model id, model role, and provider boundary metadata
- requires credential reference metadata without secret lookup or credential value access
- requires network policy reference metadata without network calls or provider endpoint resolution
- requires redacted prompt reference metadata without raw prompts or raw customer data
- requires output handling policy metadata without raw model responses
- requires data sensitivity, budget, cost, and latency metadata
- requires approval evidence linkage
- requires audit/evidence linkage
- requires proof-not-execution confirmation
- requires no raw prompt/model-response/customer-data confirmation
- requires no secret lookup confirmation
- requires no credential value access confirmation
- requires no network call confirmation
- requires no live provider call execution confirmation
- requires no fallback execution confirmation
- returns a deterministic `record_hash`
- keeps live provider/model call execution, actual model request dispatch execution, network calls, provider readiness checks, Token Guardian live routing, secret lookup, credential value access, fallback execution, tool execution, consumer integration, connector/browser/network/device/robotics/physical-world, and product readiness flags false
- preserves the frozen `lima.harness.__all__` export surface

## Required Distinction

V1-G44 separates:

- live provider/model call authority metadata/preflight validation: approved and implemented
- live provider/model call execution: not approved and not implemented
- actual model request dispatch execution: not approved and not implemented
- network calls: not approved and not implemented
- secret lookup or credential value access: not approved and not implemented
- provider readiness network checks: not approved and not implemented
- fallback execution: not approved and not implemented
- Token Guardian live routing: not approved and not implemented
- tool execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Fail-Closed Cases

The validator rejects:

- missing authority metadata fields
- missing request or GuardianDecision linkage
- linkage metadata that claims execution authority
- missing route authority evidence linkage
- missing dispatch evidence linkage
- unsupported model roles
- unsupported data sensitivity, budget, cost, or latency values
- provider boundary metadata that is not configured for scope
- provider boundary metadata that allows live provider call execution
- provider boundary metadata that allows provider readiness network checks
- provider boundary metadata that allows Token Guardian live routing
- credential metadata without a reference or no-key-local confirmation
- credential metadata that is not reference-only
- secret lookup claims
- credential value access claims
- raw secret, credential value, or provider token presence
- network policy metadata without a reference
- network policy metadata that is not reference-only
- network call claims
- provider endpoint resolution claims
- prompt metadata without redaction
- raw prompt claims
- raw customer data claims
- output policy metadata that would persist raw model responses
- missing approval evidence linkage
- stale approval evidence
- approval evidence metadata that claims execution authority
- missing audit/evidence linkage
- audit/evidence metadata that claims execution authority
- missing proof-not-execution confirmations
- raw prompts, raw model responses, raw customer data, credentials, provider tokens, API keys, and secrets
- live provider/model call execution claims
- actual model request dispatch execution claims
- fallback execution claims
- tool execution claims
- consumer repo mutation, consumer imports/calls, connector/browser/network/device/robotics/physical-world claims
- product-readiness claims

## Boundaries

- Runtime behavior added: yes, only the approved non-executing authority metadata/preflight validator.
- Frozen `lima.harness.__all__` changed: no.
- Live provider/model call execution added: no.
- Actual model request dispatch execution added: no.
- Network calls added: no.
- Provider readiness network checks added: no.
- Token Guardian live routing added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Fallback execution added: no.
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
- Product readiness approved: no.

## Readiness Result

V1-G44 is ready for independent audit.

The next smallest safe step is a separate V1-G44 audit branch. After audit and readiness rollup, the next approval gate may request live provider/model call execution or a narrower dry-run call envelope. Do not proceed to live provider/model call execution, network calls, secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
