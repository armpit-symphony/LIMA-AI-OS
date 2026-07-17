# V1-G51 Executable Real Provider Executor Invocation

Date: 2026-06-18
Branch: `v1-g51-executable-real-provider-executor-invocation`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_executable_real_provider_executor_invocation_wrapper_slice`

V1-G51 implements the approved bounded executable real provider executor invocation wrapper slice. It adds a LIMA harness wrapper that validates V1-G50 invocation envelope metadata, V1-G49 executor authority linkage, V1-G48 credential/network hardening linkages, redaction/audit policy, timeout/cost/failure metadata, and then calls only a caller-injected provider executor.

This slice does not add built-in provider SDK clients, direct network client code, provider endpoint resolution, ambient secret lookup, credential value access, provider token/API key access, fallback execution, connectors, consumer repository edits, browser/network/file/device/robotics/physical-world behavior, scheduled tasks, external sends, raw sensitive persistence, or product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G51` approval wording.

Approved implementation branch:

- `v1-g51-executable-real-provider-executor-invocation`

Approved scope:

- `executable_real_provider_executor_invocation_wrapper_slice`

Approved scope amendment:

- `Approve-V1-G51-Scope-Amendment`
- `tests/test_v1_g46_live_provider_model_call_execution.py` may be updated so prior G46 public API export assertions allow later approved harness exports while preserving the original G46 export-preservation checks.

## Runtime Execution Target

Approved package:

- `lima.harness`

Approved runtime files:

- `lima/harness/v1_executable_real_provider_executor_invocation.py`
- `lima/harness/__init__.py`

Public harness symbols added to `lima.harness.__all__`:

- `V1ExecutableRealProviderExecutorInvocationError`
- `execute_v1_executable_real_provider_executor_invocation`

No other runtime file was created, edited, removed, renamed, or cleaned up.

## Execution Boundary

The approved wrapper:

- requires V1-G50 invocation request envelope metadata
- requires V1-G50 invocation response envelope metadata
- requires V1-G49 executor authority linkage
- requires V1-G48 credential hardening linkage
- requires V1-G48 network hardening linkage
- requires deny-by-default network metadata
- requires sanitized audit evidence linkage
- requires redaction policy that forbids raw prompt, raw model response, raw customer data, secret, credential, provider token, and API key persistence
- requires V1-G51 execution approval linkage
- requires a caller-injected provider executor
- calls only the caller-injected provider executor
- returns sanitized evidence only

No built-in provider SDK client was added.

No direct network client code was added.

No provider endpoint resolver was added.

No ambient secret lookup was added.

No credential value access was added.

No fallback execution was added.

## Files Changed

V1-G51 changed only these LIMA-AI-OS files:

- `lima/harness/v1_executable_real_provider_executor_invocation.py`
- `lima/harness/__init__.py`
- `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION.md`
- `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g51_executable_real_provider_executor_invocation.json`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- `tests/test_v1_g51_executable_real_provider_executor_invocation.py`

V1-G51 scope amendment changed:

- `tests/test_v1_g46_live_provider_model_call_execution.py`

No Sparkbot file was changed.

No Arc-Bot-shell file was changed.

## Preserved Harness Exports

The prior frozen `lima.harness.__all__` exports remain present:

- `V1ProviderModelRoutingAuthorityError`
- `validate_v1_provider_model_routing_authority`
- `V1LiveProviderModelCallAuthorityError`
- `validate_v1_live_provider_model_call_authority`
- `V1LiveProviderModelCallExecutionError`
- `execute_v1_live_provider_model_call`

No prior harness export was removed or renamed.

## Required Distinction

V1-G51 separates:

- bounded executable wrapper: implemented
- caller-injected provider executor invocation: implemented
- built-in provider SDK clients: not approved and not implemented
- direct network client code: not approved and not implemented
- provider endpoint resolution: not approved and not implemented
- ambient secret lookup: not approved and not implemented
- credential value access: not approved and not implemented
- provider token/API key access: not approved and not implemented
- fallback execution: not approved and not implemented
- consumer repository edits: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Executable real provider executor invocation wrapper approved: yes.
- Executable real provider executor invocation wrapper added: yes.
- Caller-injected provider executor invocation added: yes.
- Actual model request dispatch execution added: yes, through the injected executor boundary.
- Approved runtime files changed: yes, only the approved V1-G51 runtime files.
- Existing frozen harness exports preserved: yes.
- Existing frozen harness exports removed or renamed: no.
- V1-G50 envelope metadata weakened: no.
- V1-G49 executor authority metadata weakened: no.
- V1-G48 hardening metadata weakened: no.
- Built-in provider SDK added: no.
- Direct network code added: no.
- Provider endpoint resolution added: no.
- Network call performed by LIMA harness: no.
- Ambient secret lookup added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Provider token/API key access added: no.
- Fallback execution added: no.
- Provider readiness network check added: no.
- Token Guardian live routing added: no.
- Tool execution added: no.
- Action execution added outside the caller-injected executor boundary: no.
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

V1-G51 is ready for independent audit.

The next smallest safe step is a separate V1-G51 audit branch. Do not proceed to built-in provider SDK clients, provider endpoint resolution, direct provider network egress, secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world authority, consumer repository edits, or product-readiness claims from this implementation branch.
