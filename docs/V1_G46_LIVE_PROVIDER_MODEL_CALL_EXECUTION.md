# V1-G46 Live Provider Model Call Execution

Date: 2026-06-17
Branch: `v1-g46-live-provider-model-call-execution`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_live_provider_model_call_execution_slice`

V1-G46 implements the approved bounded live provider/model call execution slice. It adds a LIMA harness wrapper that requires prevalidated V1-G44 authority metadata, V1-G46 execution approval linkage, sanitized audit/redaction metadata, and a caller-injected provider executor before a provider/model call can be invoked.

The implementation does not add built-in provider SDK clients, direct network client code, ambient environment secret lookup, credential value access, fallback execution, tools, connectors, consumer repository edits, browser/network/file/device/robotics/physical-world behavior, scheduled tasks, external sends, or product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G46` approval wording.

Approved implementation branch:

- `v1-g46-live-provider-model-call-execution`

Approved runtime scope:

- `live_provider_model_call_execution_slice`

## Runtime Execution Target

Approved package:

- `lima.harness`

Approved runtime files:

- `lima/harness/v1_live_provider_model_call_execution.py`
- `lima/harness/__init__.py`

Public harness symbols added to `lima.harness.__all__`:

- `V1LiveProviderModelCallExecutionError`
- `execute_v1_live_provider_model_call`

No other runtime file was created, edited, removed, renamed, or cleaned up.

## Execution Boundary

The approved wrapper:

- requires a prevalidated V1-G44 authority record
- requires V1-G46 execution approval linkage
- requires sanitized audit evidence linkage
- requires a redaction policy that forbids raw prompt, raw model response, raw customer data, secret, credential, provider token, and API key persistence
- requires a caller-injected provider executor
- calls only the caller-injected provider executor
- returns sanitized evidence only

No built-in provider SDK client was added.

No direct network client code was added.

No ambient secret lookup was added.

No credential value access was added.

No fallback execution was added.

## Files Changed

V1-G46 changed only these LIMA-AI-OS files:

- `lima/harness/v1_live_provider_model_call_execution.py`
- `lima/harness/__init__.py`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g46_live_provider_model_call_execution.json`
- `tests/test_v1_g46_live_provider_model_call_execution.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

No Sparkbot or Arc-Bot-shell file was created, edited, removed, renamed, imported, or executed by the implementation.

## Preserved Harness Exports

The prior frozen V1-G22/G45 `lima.harness.__all__` exports remain present:

- `V1ProviderModelRoutingAuthorityError`
- `validate_v1_provider_model_routing_authority`
- `V1LiveProviderModelCallAuthorityError`
- `validate_v1_live_provider_model_call_authority`

No prior harness export was removed or renamed.

## Required Distinction

V1-G46 separates:

- bounded harness execution wrapper: implemented
- caller-injected provider executor invocation: implemented
- built-in provider SDK clients: not approved and not implemented
- direct network client code: not approved and not implemented
- ambient secret lookup: not approved and not implemented
- credential value access: not approved and not implemented
- fallback execution: not approved and not implemented
- consumer repository edits: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Live provider/model call execution approved: yes.
- Live provider/model call execution added: yes, through the bounded harness wrapper.
- Provider executor invocation added: yes, caller-injected executor only.
- Actual model request dispatch execution added: yes, through the injected executor boundary.
- Approved runtime files changed: yes, only the approved V1-G46 runtime files.
- Existing frozen harness exports preserved: yes.
- Existing frozen harness exports removed or renamed: no.
- V1-G44 authority validator weakened: no.
- Direct provider SDK added: no.
- Direct network code added: no.
- Ambient secret lookup added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Fallback execution added: no.
- Provider readiness network check added: no.
- Token Guardian live routing added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution outside approved files added: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- Raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, API key, raw diff, full patch, or raw file content persistence added: no.
- Product readiness approved: no.

## Readiness Result

V1-G46 is ready for independent audit.

The next smallest safe step is a separate V1-G46 audit branch. Do not proceed to built-in provider SDK integration, provider credential value access, direct provider egress, fallback execution, connector/browser/network authority, physical-world authority, consumer repository edits, or product-readiness claims from this implementation branch.
