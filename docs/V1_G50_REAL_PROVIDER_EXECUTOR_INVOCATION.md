# V1-G50 Real Provider Executor Invocation

Date: 2026-06-18
Branch: `v1-g50-real-provider-executor-invocation`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_real_provider_executor_invocation_metadata_slice`

V1-G50 implements the approved metadata-only real provider executor invocation slice. It adds LIMA-side docs/tests/fixtures that define non-executing invocation request and response envelope metadata for a future real provider executor lane, including provider/model scope references, V1-G49 executor authority linkage, V1-G48 credential and network hardening linkages, timeout/cost/failure metadata, redaction/audit evidence, and blocked future authorities.

This slice does not edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, invoke real or fake provider executors, execute live provider/model calls, add provider SDK clients, make network calls, read secrets, access credential values, resolve provider endpoints, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G50` approval wording.

Approved implementation branch:

- `v1-g50-real-provider-executor-invocation`

Approved scope:

- `real_provider_executor_invocation_metadata_slice`

## Metadata Result

The V1-G50 result is:

- `real_provider_executor_invocation_metadata_created`

This means LIMA now has deterministic evidence for future real provider executor invocation envelope shape. It does not approve executable provider invocation, built-in provider SDK clients, provider endpoint resolution, provider network egress, secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world behavior, or product readiness.

## Invocation Envelope Boundary

The invocation envelope design is non-executing:

- records an invocation request envelope id
- records an invocation response envelope id
- records provider and model scope references inherited from V1-G49
- links to V1-G49 real provider executor authority design metadata by reference
- links to V1-G48 credential hardening metadata by reference
- links to V1-G48 provider network hardening metadata by reference
- records timeout, retry, cost, and failure-policy metadata without execution
- records that real and fake executor invocation remain blocked in V1-G50
- records that executable provider invocation remains blocked in V1-G50

## Credential And Network Linkage

The credential and network controls inherit the V1-G48 hardening posture:

- credential policy remains reference-only
- secret lookup remains blocked
- credential value access remains blocked
- provider token and API key access remain blocked
- network policy remains reference-only
- provider endpoint resolution remains blocked
- provider egress remains deny-by-default
- DNS, HTTP, socket, and readiness checks remain blocked

## Execution Boundary Metadata

V1-G50 records execution-boundary metadata only:

- timeout policy reference
- retry policy reference
- cost policy reference
- failure policy reference
- sanitized error evidence reference
- no retry execution
- no billing call
- no readiness network probe
- no fallback execution

These records are proof of the future envelope contract, not permission to call a provider.

## Audit And Redaction Boundary

The metadata requires sanitized evidence refs:

- invocation request evidence ref
- invocation response evidence ref
- executor authority evidence ref
- credential policy evidence ref
- network policy evidence ref
- redaction policy evidence ref
- audit record ref
- no raw prompt persistence
- no raw model response persistence
- no raw customer data persistence
- no raw secret or credential persistence
- no raw diff, patch, or file content persistence

## LIMA Files Added

V1-G50 changed only these LIMA-AI-OS files:

- `docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION.md`
- `docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g50_real_provider_executor_invocation.json`
- `tests/test_v1_g50_real_provider_executor_invocation.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or expanded by this slice.

No public API export file was changed.

No Sparkbot file was changed.

No Arc-Bot-shell file was changed.

## Required Distinction

V1-G50 separates:

- real provider executor invocation metadata: approved and implemented
- executable real provider executor invocation: not approved and not implemented
- fake provider executor invocation by V1-G50: not approved and not implemented
- built-in provider SDK clients: not approved and not implemented
- secret lookup: not approved and not implemented
- credential value access: not approved and not implemented
- provider endpoint resolution: not approved and not implemented
- provider network egress: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Real provider executor invocation metadata approved: yes.
- Real provider executor invocation metadata added: yes.
- Executable provider invocation approved: no.
- Executable provider invocation added: no.
- `lima/` runtime files changed: no.
- LIMA public API expanded: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer runtime/source files changed: no.
- Real provider executor invoked: no.
- Fake provider executor invoked by V1-G50: no.
- Live provider/model calls added: no.
- Built-in provider SDK added: no.
- Direct network code added: no.
- Provider endpoint resolution added: no.
- Network call performed: no.
- Ambient secret lookup added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Provider token or API key access added: no.
- Credential storage, rotation, migration, or provisioning added: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Provider readiness network check added: no.
- Token Guardian live routing added: no.
- Tool execution outside local tests added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- Raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, API key, raw diff, full patch, or raw file content persistence added: no.
- Product readiness approved: no.

## Readiness Result

V1-G50 is ready for independent audit.

The next smallest safe step is a separate V1-G50 audit branch. Do not proceed to executable real provider invocation, built-in provider SDK clients, provider endpoint resolution, network egress, secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
