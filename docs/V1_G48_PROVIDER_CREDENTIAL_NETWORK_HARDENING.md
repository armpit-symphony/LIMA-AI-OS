# V1-G48 Provider Credential Network Hardening

Date: 2026-06-17
Branch: `v1-g48-provider-credential-network-hardening`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_provider_credential_network_hardening_metadata_slice`

V1-G48 implements the approved metadata-only provider credential/network hardening slice. It adds LIMA-side docs/tests/fixtures that define reference-only credential metadata, reference-only provider network policy metadata, deny-by-default egress posture, redaction/audit linkage, and blocked future authorities before any real provider executor, provider SDK client, secret lookup, credential value access, endpoint resolution, or network egress is approved.

This slice does not edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, invoke provider executors, execute live provider/model calls, add provider SDK clients, make network calls, read secrets, access credential values, resolve provider endpoints, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G48` approval wording.

Approved implementation branch:

- `v1-g48-provider-credential-network-hardening`

Approved scope:

- `provider_credential_network_hardening_metadata_slice`

## Metadata Result

The V1-G48 hardening result is:

- `provider_credential_network_hardening_metadata_created`

This means LIMA now has deterministic evidence for credential-reference and provider-network-reference boundaries. It does not approve real credentials, real provider executors, built-in provider SDK clients, provider endpoint resolution, network egress, fallback execution, connector/browser/network authority, physical-world behavior, or product readiness.

## Credential Boundary

The credential policy is reference-only:

- stores a credential reference id only
- records vault policy and rotation policy references only
- forbids raw secrets
- forbids credential values
- forbids provider token and API key material
- forbids ambient environment lookup
- forbids runtime credential fetch
- forbids credential storage, rotation, provisioning, or migration

## Network Boundary

The provider network policy is reference-only and deny-by-default:

- stores a provider network policy reference only
- records allowed-provider metadata by reference only
- forbids endpoint resolution
- forbids DNS lookups
- forbids HTTP clients
- forbids socket clients
- forbids readiness probes
- forbids direct provider egress
- records that later egress requires a dedicated approval gate

## Audit And Redaction Boundary

The metadata requires sanitized evidence refs:

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

V1-G48 changed only these LIMA-AI-OS files:

- `docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING.md`
- `docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g48_provider_credential_network_hardening.json`
- `tests/test_v1_g48_provider_credential_network_hardening.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or expanded by this slice.

No Sparkbot file was changed.

No Arc-Bot-shell file was changed.

## Required Distinction

V1-G48 separates:

- credential reference metadata: approved and implemented
- network policy reference metadata: approved and implemented
- real secret lookup: not approved and not implemented
- credential value access: not approved and not implemented
- provider endpoint resolution: not approved and not implemented
- provider network egress: not approved and not implemented
- real provider executor invocation: not approved and not implemented
- built-in provider SDK clients: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Provider credential/network hardening approved: yes.
- Provider credential/network hardening metadata added: yes.
- `lima/` runtime files changed: no.
- LIMA public API expanded: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer runtime/source files changed: no.
- Real provider executor invoked: no.
- Fake provider executor invoked by V1-G48: no.
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

V1-G48 is ready for independent audit.

The next smallest safe step is a separate V1-G48 audit branch. Do not proceed to real provider executor integration, built-in provider SDK clients, provider endpoint resolution, network egress, secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
