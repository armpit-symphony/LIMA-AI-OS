# V1-G60 SDK Dependency Vendor Provider SDK Import Operator Decision Packet

Date: 2026-06-20
Branch: `prepare-v1-g60-sdk-dependency-vendor-provider-sdk-import-approval-request`
API status: `CANDIDATE_ONLY`

Decision packet status: `approved`

## Decision Needed

Request-stage status before approval: Decision packet status: `awaiting_operator_decision`

Original decision options:

- Recorded choice: none
- Recorded choice: Approve-V1-G60
- Recorded choice: Revise-V1-G60
- Recorded choice: Pause

## Template for `Approve-V1-G60`

Approve-V1-G60

I explicitly approve V1-G60 implementation of the LIMA-side SDK dependency addition and vendor provider SDK import approval slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md.

## Template for `Revise-V1-G60`

Revise-V1-G60

Requested revision:

- `<specific requested change>`

## Template for `Pause`

Pause

Reason:

- `<reason>`

## Current State

- Implementation approved: yes.
- SDK dependency addition and vendor provider SDK import approved: yes.
- SDK dependency added: pending implementation on `v1-g60-sdk-dependency-vendor-provider-sdk-import`.
- Dependency manifest edited: pending implementation on `v1-g60-sdk-dependency-vendor-provider-sdk-import`.
- Lockfile edited: no.
- Vendor provider SDK import added: pending implementation on `v1-g60-sdk-dependency-vendor-provider-sdk-import`.
- Built-in provider SDK client implementation approved: no.
- Built-in provider SDK client implementation added: no.
- Provider client construction added: no.
- LIMA runtime files changed: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Endpoint resolution by LIMA added: no.
- Network calls by LIMA added: no.
- Direct provider egress by LIMA added: no.
- Secret lookup added: no.
- Credential-value access added: no.
- Provider token or API key access added: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Consumer production runtime integration added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- Final public API freeze claimed: no.

## Recorded Operator Decision

Recorded choice: Approve-V1-G60

Recorded approval wording: I explicitly approve V1-G60 implementation of the LIMA-side SDK dependency addition and vendor provider SDK import approval slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md.

Recorded revision request: none

Recorded pause reason: none

Approved implementation branch: `v1-g60-sdk-dependency-vendor-provider-sdk-import`

Implementation approved: yes.

## Decision Rule

Implementation may proceed only on `v1-g60-sdk-dependency-vendor-provider-sdk-import` and only within the approved file map in `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md`.
