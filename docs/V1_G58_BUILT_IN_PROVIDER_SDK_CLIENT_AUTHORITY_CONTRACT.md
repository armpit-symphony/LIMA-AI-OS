# V1-G58 Built-In Provider SDK Client Authority Contract

Date: 2026-06-20
Branch: `v1-g58-built-in-provider-sdk-client-authority-contract`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_metadata_only_built_in_provider_sdk_client_authority_contract_slice`

This is metadata-only built-in provider SDK client authority contract evidence.

V1-G58 implements the approved LIMA-side built-in provider SDK client authority contract metadata slice. It records the authority conditions that must remain true before any future built-in provider SDK client implementation can be considered after V1-G57.

This slice adds docs/tests/fixtures only. It does not edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, edit consumer production runtime/source files, add built-in provider SDK clients, add SDK dependencies, import vendor provider SDKs, implement direct provider SDK code, resolve provider endpoints, add DNS/HTTP/socket/network clients, make network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, claim product readiness, or approve final public API freeze.

## Operator Decision

The operator decision was recorded in `docs/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT_OPERATOR_DECISION_PACKET.md` using the `Approve-V1-G58` choice and the exact approval wording from the packet template.

Approved implementation branch:

- `v1-g58-built-in-provider-sdk-client-authority-contract`

Approved scope:

- `built_in_provider_sdk_client_authority_contract_metadata_slice`

## Contract Result

The V1-G58 result is:

- `built_in_provider_sdk_client_authority_contract_metadata_recorded`

This means LIMA has metadata evidence requiring Guardian-gated authorization, explicit operator approval linkage, provider capability declaration metadata, SDK dependency declaration metadata, sanitized evidence references, credential-reference metadata, network-policy-reference metadata, endpoint-authority-reference metadata, and denial-by-default posture before any later built-in provider SDK client implementation can proceed.

It does not approve built-in provider SDK clients, SDK dependencies, vendor provider SDK imports, provider credential-value access, LIMA-owned endpoint resolution, LIMA-owned provider network egress, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, product readiness, or final public API freeze.

## Evidence Chain

V1-G58 links the built-in provider SDK client authority contract posture to these prior evidence lanes:

- V1-G48 provider credential/network hardening
- V1-G53 provider SDK/network/credential authority
- V1-G54 fake SDK/fake-egress harness
- V1-G55 caller-injected real provider SDK/network egress wrapper
- V1-G56 consumer fake-executor provider SDK/network egress smoke
- V1-G57 provider execution hardening authorization
- Public Sparkbot G56 publication resolution

These references are evidence links only. They do not become execution authority, SDK authority, credential authority, provider configuration authority, or product-readiness evidence.

## Required Authority Contract Conditions

Before any future built-in provider SDK client implementation can proceed, a later gate must prove:

- Guardian gate linkage is explicit.
- Operator approval linkage is explicit.
- Provider capability declaration metadata is explicit.
- SDK dependency declaration metadata is explicit.
- Built-in provider SDK client behavior remains denied by default unless a later exact approval grants the specific lane.
- Evidence references are sanitized and path/ref based.
- Credential metadata is reference-only.
- Network policy metadata is reference-only.
- Endpoint authority metadata is reference-only.
- Raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, full patches, and raw file contents are not persisted or emitted.
- Consumer production runtime integration remains blocked until a later explicit approval.
- Physical-world/device/robotics behavior remains blocked until a dedicated physical-world authority lane approves it.

## LIMA Files Added

V1-G58 changed only these approved LIMA-AI-OS files:

- `docs/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT.md`
- `docs/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g58_built_in_provider_sdk_client_authority_contract.json`
- `tests/test_v1_g58_built_in_provider_sdk_client_authority_contract.py`

The operator decision packet was updated to record the required exact `Approve-V1-G58` decision before implementation.

No `lima/` runtime file was created, edited, removed, renamed, imported by implementation docs, or expanded by this slice.

## Required Distinction

V1-G58 separates:

- built-in provider SDK client authority contract metadata: approved and implemented
- built-in provider SDK client implementation: not approved and not implemented
- SDK dependency additions: not approved and not implemented
- vendor provider SDK imports: not approved and not implemented
- provider execution expansion: not approved and not implemented
- LIMA runtime behavior: not added
- LIMA public API expansion: not added
- consumer production runtime integration: not added
- real provider credential access: not approved and not implemented
- provider endpoint resolution by LIMA: not approved and not implemented
- direct provider network egress by LIMA: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- raw sensitive content persistence: not approved and not implemented
- product readiness: not approved and not claimed
- final public API freeze: not approved and not claimed

## Boundaries

- Built-in provider SDK client authority contract metadata approved: yes.
- Built-in provider SDK client authority contract metadata added: yes.
- Built-in provider SDK client implementation approved: no.
- Built-in provider SDK client implementation added: no.
- SDK dependency added: no.
- Vendor provider SDK import added: no.
- `lima/` runtime files changed: no.
- LIMA public API expanded by V1-G58: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer production runtime/source files changed: no.
- Provider execution expansion added: no.
- Live provider/model calls added: no.
- Direct provider SDK implementation added: no.
- Provider endpoint resolution added: no.
- DNS lookup added: no.
- HTTP client added: no.
- Socket client added: no.
- Network call performed by LIMA: no.
- Direct provider egress performed by LIMA: no.
- Credential-reference metadata only: yes.
- Network-policy metadata only: yes.
- Endpoint-authority metadata only: yes.
- Provider capability declaration metadata only: yes.
- SDK dependency declaration metadata only: yes.
- Secret lookup added: no.
- Credential-value access added: no.
- Provider token or API key access added: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- Raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, API key, raw diff, full patch, or raw file content persistence added: no.
- Product readiness approved: no.
- Final public API freeze approved: no.

## Readiness Result

V1-G58 is ready for independent audit after the validation commands recorded in the closeout and fixture remain green.

The next smallest safe step is a separate V1-G58 audit branch. Do not proceed to built-in provider SDK client implementation, SDK dependency additions, vendor provider SDK imports, credential-value access, LIMA-owned provider network egress, endpoint resolution, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, product readiness, or final public API freeze from this implementation branch.
