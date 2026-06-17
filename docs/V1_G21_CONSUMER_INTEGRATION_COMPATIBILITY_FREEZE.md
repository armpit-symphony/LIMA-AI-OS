# V1-G21 Consumer Integration Compatibility Freeze

Date: 2026-06-17
Branch: `v1-g21-consumer-integration-compatibility-freeze`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_consumer_integration_compatibility_freeze_slice`

V1-G21 implements the approved LIMA-side consumer integration compatibility/freeze metadata slice. It validates sanitized compatibility evidence for Sparkbot, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and future shells so candidate export surfaces, runtime symbol refs, import expectations, fixtures, versions, Guardian boundaries, approval boundaries, and provider/model route boundaries can be reviewed later.

This implementation does not edit consumer repositories, write consumer files, import consumer code, call consumer runtimes, wire Sparkbot, wire Arc-Bot-shell, wire LIMA Robo OS, freeze the final public API, clean up runtime exports, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G21` template.

Approved implementation branch:

- `v1-g21-consumer-integration-compatibility-freeze`

Approved runtime scope:

- `consumer_integration_compatibility_freeze_metadata_slice`

## Runtime Files

- `lima/adapters/v1_consumer_integration_compatibility.py`
- `lima/adapters/__init__.py`

## Runtime Symbols

- `V1ConsumerIntegrationCompatibilityError`
- `validate_v1_consumer_integration_compatibility_freeze`

## Behavior Added

V1-G21 adds one deterministic local consumer compatibility/freeze metadata validator:

- requires compatibility packet id metadata
- requires consumer packet family, name, repository, branch/ref, and commit SHA metadata
- supports `sparkbot`, `arc_bot`, `lima_robo_os`, `lima_office`, and `future_shell` packet families
- requires candidate export surface refs
- requires runtime symbol refs
- requires import surface expectation metadata
- requires fixture compatibility matrix metadata
- requires version compatibility metadata
- requires Guardian boundary compatibility metadata
- requires approval boundary compatibility metadata
- requires provider/model route boundary compatibility metadata
- requires consumer runtime call prohibition metadata
- requires no consumer repo mutation confirmation
- requires no live import/call confirmation
- requires final public API freeze not claimed confirmation
- requires audit/evidence linkage metadata
- requires proof-not-authority confirmation
- requires no raw content/secret/credential/customer-data confirmation
- requires no execution-authority confirmation
- returns a deterministic `record_hash`
- keeps consumer repo mutation, consumer imports, consumer runtime calls, consumer integration, shell wiring, final freeze, export cleanup, provider/model calls, secret lookup, credential access, tool execution, file mutation, connector/browser/network/device/robotics/physical-world, and product readiness flags false

## Required Distinction

V1-G21 separates:

- sanitized consumer compatibility metadata: implemented as validation
- consumer repo edits: not approved and not implemented
- live consumer imports/calls: not approved and not implemented
- consumer runtime wiring: not approved and not implemented
- final public API freeze: not approved and not implemented
- runtime export cleanup: not approved and not implemented
- product readiness: not approved and not claimed

## Fail-Closed Cases

The validator rejects:

- missing consumer compatibility metadata fields
- unsupported consumer packet families
- invalid consumer commit SHA metadata
- missing candidate export surface refs
- missing runtime symbol refs
- import surface expectations that are not metadata-only
- live consumer import claims
- consumer runtime call claims
- consumer code import claims
- import surface expectations that claim runtime authority
- missing fixture compatibility matrix metadata
- fixture matrix raw content claims
- fixture matrix consumer runtime invocation claims
- invalid compatibility statuses
- version metadata that claims final public API freeze
- Guardian boundary metadata that is not compatible
- approval boundary metadata that is not compatible
- provider/model route boundary metadata that is not compatible
- boundary metadata that claims authority
- boundary metadata that grants execution
- missing future-integration approval requirement
- consumer runtime call prohibition metadata that does not confirm non-execution
- consumer runtime call prohibition metadata that claims live import/call behavior
- missing no consumer repo mutation confirmation
- missing no live import/call confirmation
- missing final public API freeze not claimed confirmation
- missing audit/evidence linkage
- audit/evidence metadata that claims authority
- missing proof-not-authority confirmation
- missing no raw content/secret/credential/customer-data confirmation
- missing no execution-authority confirmation
- raw file contents, prompts, customer data, credentials, provider tokens, API keys, and secrets
- consumer repo mutation claims
- consumer code import claims
- consumer runtime call claims
- final API freeze claims
- runtime export cleanup claims
- provider/model call, secret lookup, credential access, tool execution, connector/browser/network/device/robotics/physical-world claims

## Boundaries

- Runtime behavior added: yes, only the approved non-executing consumer compatibility/freeze metadata validator.
- Consumer repo mutation added: no.
- Consumer file writes added: no.
- Consumer code imports added: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- Final public API freeze approved: no.
- Runtime export cleanup approved: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Product readiness approved: no.

## Readiness Result

V1-G21 is ready for independent audit.

The next smallest safe step is a separate V1-G21 audit branch. Do not proceed to consumer repo edits, live consumer imports/calls, final public API freeze, runtime export cleanup, live provider/model calls, secret lookup, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
