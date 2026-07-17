# V1-G60 SDK Dependency Vendor Provider SDK Import

Date: 2026-06-20
Branch: `v1-g60-sdk-dependency-vendor-provider-sdk-import`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_sdk_dependency_addition_vendor_provider_sdk_import_approval_slice`

V1-G60 implements the approved LIMA-side SDK dependency addition and vendor provider SDK import approval slice.

This slice declares the OpenAI Python SDK dependency in `pyproject.toml` and records a bounded importability proof posture for the vendor module name `openai`. It does not add `lima/` runtime files, public API exports, built-in provider SDK clients, provider client construction, direct provider SDK call behavior, provider endpoint resolution, DNS/HTTP/socket/network clients, network calls, direct provider egress, secret lookup, credential-value access, provider token or API key access, provider configuration changes, fallback execution, consumer production runtime integration, connector behavior, browser/network/file/device/robotics/physical-world behavior, external sends, product-readiness claims, or final public API freeze.

No `lima/` runtime file was created, edited, removed, renamed, or given a vendor SDK import by this slice.

## Operator Decision

The operator decision was recorded in `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_OPERATOR_DECISION_PACKET.md` using the `Approve-V1-G60` choice and the exact approval wording from the packet template.

Approved implementation branch:

- `v1-g60-sdk-dependency-vendor-provider-sdk-import`

Approved scope:

- `sdk_dependency_addition_vendor_provider_sdk_import_approval_slice`

## Dependency Declaration

V1-G60 adds this dependency declaration to `pyproject.toml`:

- package: `openai`
- version constraint: `>=1.0.0,<3.0.0`
- import module: `openai`
- provider family: `openai`
- manifest: `pyproject.toml`
- lockfile changed: no

The dependency declaration is intentionally separated from provider client construction, credential access, endpoint resolution, provider network egress, fallback, and runtime invocation.

## Importability Proof Boundary

V1-G60 proves the vendor provider SDK import boundary as static/local evidence:

- the approved vendor import module is `openai`
- the module name is declared in the fixture and tests
- no `lima/` runtime file imports `openai`
- no provider client is constructed
- no credential lookup is performed
- no endpoint resolution is performed
- no provider/model call is performed
- no LIMA-owned network call is performed

The current local environment did not have the `openai` package installed before this slice. V1-G60 therefore does not claim a successful runtime import execution in this environment. It claims the dependency declaration and import boundary are approved and represented; a later install/runtime lane must prove installed import execution if needed.

## Evidence Chain

V1-G60 links to these prior evidence lanes:

- V1-G48 provider credential/network hardening
- V1-G53 provider SDK/network/credential authority
- V1-G54 fake SDK/fake-egress harness
- V1-G55 caller-injected real provider SDK/network egress wrapper
- V1-G56 consumer fake-executor provider SDK/network egress smoke
- V1-G57 provider execution hardening authorization
- V1-G58 built-in provider SDK client authority contract
- V1-G59 SDK dependency and vendor provider SDK import authority
- Public Sparkbot G56 publication resolution

These links are evidence references only. They do not become execution authority, credential authority, endpoint authority, network authority, fallback authority, consumer integration authority, product readiness, or final public API freeze.

## Required Distinction

V1-G60 separates:

- SDK dependency declaration in `pyproject.toml`: approved and implemented
- vendor import module boundary metadata: approved and recorded
- lockfile edit: not approved and not implemented
- `lima/` runtime import of the vendor SDK: not added
- built-in provider SDK client implementation: not approved and not implemented
- provider client construction: not approved and not implemented
- direct provider SDK call behavior: not approved and not implemented
- credential-value access: not approved and not implemented
- provider token or API key access: not approved and not implemented
- endpoint resolution by LIMA: not approved and not implemented
- direct provider network egress by LIMA: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- consumer production runtime integration: not approved and not implemented
- product readiness: not approved and not claimed
- final public API freeze: not approved and not claimed

## Boundaries

- SDK dependency addition approved: yes.
- SDK dependency added to `pyproject.toml`: yes.
- Dependency manifest edited: yes, limited to the approved dependency declaration.
- Lockfile edited: no.
- Vendor provider SDK import boundary approved: yes.
- Vendor provider SDK import module recorded: yes.
- Runtime vendor SDK import added to `lima/`: no.
- Built-in provider SDK client implementation approved: no.
- Built-in provider SDK client implementation added: no.
- Provider client construction added: no.
- `lima/` runtime files changed: no.
- LIMA public API expanded by V1-G60: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer production runtime/source files changed: no.
- Provider execution expansion added: no.
- Live provider/model calls added: no.
- Direct provider SDK call implementation added: no.
- Provider endpoint resolution added: no.
- DNS lookup added: no.
- HTTP client added: no.
- Socket client added: no.
- Network call performed by LIMA: no.
- Direct provider egress performed by LIMA: no.
- Credential-reference metadata only: yes.
- Network-policy metadata only: yes.
- Endpoint-authority metadata only: yes.
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

V1-G60 is ready for independent audit after the validation commands recorded in the closeout and fixture remain green.

The next smallest safe step is a separate V1-G60 audit branch. Do not proceed to built-in provider SDK client implementation, provider client construction, credential-value access, provider token or API key access, LIMA-owned provider endpoint resolution, LIMA-owned provider network egress, fallback execution, connector/browser/network authority, consumer production runtime integration, physical-world authority, product readiness, or final public API freeze from this implementation branch.
