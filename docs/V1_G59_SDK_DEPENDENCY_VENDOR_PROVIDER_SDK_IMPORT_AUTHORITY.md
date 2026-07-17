# V1-G59 SDK Dependency Vendor Provider SDK Import Authority

Date: 2026-06-20
Branch: `v1-g59-sdk-dependency-vendor-provider-sdk-import-authority`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_metadata_only_sdk_dependency_vendor_provider_sdk_import_authority_slice`

This is metadata-only SDK dependency and vendor provider SDK import authority evidence.

V1-G59 implements the approved LIMA-side SDK dependency and vendor provider SDK import authority metadata slice. It records the authority criteria that must remain true before any future SDK dependency addition or vendor provider SDK import can be considered after V1-G58.

This slice adds docs/tests/fixtures only. It does not edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, edit consumer production runtime/source files, add SDK dependencies, edit dependency manifests, edit lockfiles, import vendor provider SDKs, add built-in provider SDK clients, construct provider clients, implement direct provider SDK code, resolve provider endpoints, add DNS/HTTP/socket/network clients, make network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, claim product readiness, or approve final public API freeze.

## Operator Decision

The operator decision was recorded in `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_OPERATOR_DECISION_PACKET.md` using the `Approve-V1-G59` choice and the exact approval wording from the packet template.

Approved implementation branch:

- `v1-g59-sdk-dependency-vendor-provider-sdk-import-authority`

Approved scope:

- `sdk_dependency_vendor_provider_sdk_import_authority_metadata_slice`

## Contract Result

The V1-G59 result is:

- `sdk_dependency_vendor_provider_sdk_import_authority_metadata_recorded`

This means LIMA has metadata evidence requiring Guardian-gated authorization, explicit operator approval linkage, SDK dependency declaration metadata, vendor provider SDK import declaration metadata, supply-chain review metadata, license/security posture metadata, sanitized evidence references, credential-reference metadata, network-policy-reference metadata, endpoint-authority-reference metadata, and denial-by-default posture before any later SDK dependency addition or vendor provider SDK import can proceed.

It does not approve SDK dependency additions, dependency manifest edits, lockfile edits, vendor provider SDK imports, built-in provider SDK client implementation, provider client construction, provider credential-value access, LIMA-owned endpoint resolution, LIMA-owned provider network egress, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, product readiness, or final public API freeze.

## Evidence Chain

V1-G59 links the SDK dependency and vendor provider SDK import authority posture to these prior evidence lanes:

- V1-G48 provider credential/network hardening
- V1-G53 provider SDK/network/credential authority
- V1-G54 fake SDK/fake-egress harness
- V1-G55 caller-injected real provider SDK/network egress wrapper
- V1-G56 consumer fake-executor provider SDK/network egress smoke
- V1-G57 provider execution hardening authorization
- V1-G58 built-in provider SDK client authority contract
- Public Sparkbot G56 publication resolution

These references are evidence links only. They do not become execution authority, SDK dependency authority, vendor SDK import authority, credential authority, provider configuration authority, or product-readiness evidence.

## Required Authority Conditions

Before any future SDK dependency addition or vendor provider SDK import can proceed, a later gate must prove:

- Guardian gate linkage is explicit.
- Operator approval linkage is explicit.
- SDK dependency declaration metadata is explicit.
- Vendor provider SDK import declaration metadata is explicit.
- Supply-chain review metadata is explicit.
- License/security posture metadata is explicit.
- Dependency manifest and lockfile mutation remains denied by default unless a later exact approval grants the specific lane.
- Vendor provider SDK import behavior remains denied by default unless a later exact approval grants the specific lane.
- Evidence references are sanitized and path/ref based.
- Credential metadata is reference-only.
- Network policy metadata is reference-only.
- Endpoint authority metadata is reference-only.
- Raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, full patches, and raw file contents are not persisted or emitted.
- Consumer production runtime integration remains blocked until a later explicit approval.
- Physical-world/device/robotics behavior remains blocked until a dedicated physical-world authority lane approves it.

## LIMA Files Added

V1-G59 changed only these approved LIMA-AI-OS files:

- `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md`
- `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.json`
- `tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.py`

The operator decision packet was updated to record the required exact `Approve-V1-G59` decision before implementation.

No `lima/` runtime file was created, edited, removed, renamed, imported by implementation docs, or expanded by this slice.

## Required Distinction

V1-G59 separates:

- SDK dependency and vendor provider SDK import authority metadata: approved and implemented
- SDK dependency additions: not approved and not implemented
- dependency manifest edits: not approved and not implemented
- lockfile edits: not approved and not implemented
- vendor provider SDK imports: not approved and not implemented
- built-in provider SDK client implementation: not approved and not implemented
- provider client construction: not approved and not implemented
- direct provider SDK implementation: not approved and not implemented
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

- SDK dependency and vendor provider SDK import authority metadata approved: yes.
- SDK dependency and vendor provider SDK import authority metadata added: yes.
- SDK dependency addition approved: no.
- SDK dependency added: no.
- Dependency manifest edited: no.
- Lockfile edited: no.
- Vendor provider SDK import approved: no.
- Vendor provider SDK import added: no.
- Built-in provider SDK client implementation approved: no.
- Built-in provider SDK client implementation added: no.
- Provider client construction added: no.
- `lima/` runtime files changed: no.
- LIMA public API expanded by V1-G59: no.
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
- SDK dependency declaration metadata only: yes.
- Vendor import declaration metadata only: yes.
- Supply-chain review metadata only: yes.
- License/security posture metadata only: yes.
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

V1-G59 is ready for independent audit after the validation commands recorded in the closeout and fixture remain green.

The next smallest safe step is a separate V1-G59 audit branch. Do not proceed to SDK dependency additions, dependency manifest edits, lockfile edits, vendor provider SDK imports, built-in provider SDK client implementation, provider client construction, credential-value access, LIMA-owned provider network egress, endpoint resolution, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, product readiness, or final public API freeze from this implementation branch.
