# V1 Consumer Target State After Arc Readiness Integration

Date: 2026-06-19
Branch: `docs-v1-consumer-target-state-after-arc-readiness-integration`
API status: `CANDIDATE_ONLY`

This refresh records the current first-consumer testing state after the Arc-Bot-shell runtime-authority gating readiness integration audit. It is docs/tests/fixtures-only state evidence. It does not approve V1-G55, add runtime behavior, edit `lima/`, change public API exports, modify consumer repositories, wire shells, call providers, invoke network egress, access credentials, or claim V1/product/production readiness.

## Current Runtime Gate

The active implementation gate remains `V1-G55`.

The only valid operator choices remain:

- `Approve-V1-G55`
- `Revise-V1-G55`
- `Pause`

No valid `Approve-V1-G55` decision is recorded. Until that exact approval is recorded in `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`, G55 runtime implementation, public API export changes, provider SDK/network egress, SDK clients, endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, fallback, consumer production runtime integration, and product-readiness claims remain blocked.

## First Consumer Targets

| Consumer target | Current evidence | State |
| --- | --- | --- |
| `Sparkbot_shell` | Branch `sparkbot-shell-work-settings-runtime-preview`, commit `548b6d6aa6cde98b261e867c0c2db86ddbfa83dc` | Local branch is clean and tracks origin. |
| public `Sparkbot` | Branch `public-work-settings-preview`, commit `81eed8c4067b1a73885bbc79003ea5870b1604a2` | Local branch is clean; remote push to `sparkpit-labs/Sparkbot` is blocked by GitHub 403 for the current `armpit-symphony` credential. |
| `Arc-Bot-shell` | Branch `arc-bot-runtime-ui-scaffold-foundation-phase-chain`, commit `3004367aa7aa96b4b2518c0e3783cf5afba979c0` | Pushed to origin and audited in LIMA. |

## Accepted Arc Consumer Evidence

The latest Arc consumer-side audit evidence is:

- `docs/audits/V1_ARC_PHASE1_READINESS_BUNDLE_AUDIT.md`
- `docs/audits/V1_ARC_PHASE1_RUNTIME_AUTHORITY_GATING_AUDIT.md`
- `docs/audits/V1_ARC_RUNTIME_GATING_READINESS_INTEGRATION_AUDIT.md`

The Arc readiness integration makes the runtime-authority gating projection visible in the default Phase-1 readiness bundle while keeping:

- all required future gates unresolved
- runtime authority blocked
- runtime execution disabled
- connector behavior blocked
- worker dispatch blocked
- customer-system mutation blocked
- product readiness unclaimed

## Public Sparkbot Publication Note

The public Sparkbot preview branch exists locally and is clean, but the current credential cannot push to `sparkpit-labs/Sparkbot`.

Observed push result:

`Permission to sparkpit-labs/Sparkbot.git denied to armpit-symphony` with HTTP 403.

This is an external repository-permission blocker only. It does not change LIMA runtime authority, does not approve G55, and does not imply public Sparkbot product readiness.

## Boundary Results

- Runtime behavior added by this refresh: no.
- `lima/` runtime files changed by this refresh: no.
- Public API exports changed by this refresh: no.
- `tests/support` changed by this refresh: no.
- Consumer repository files changed by this refresh: no.
- V1-G55 operator approval recorded by this refresh: no.
- V1-G55 runtime implementation approved by this refresh: no.
- G55 wrapper added by this refresh: no.
- Provider SDK/network egress invocation added: no.
- Built-in provider SDK clients added: no.
- SDK dependencies added: no.
- Vendor SDK imports added: no.
- Endpoint resolution by LIMA added: no.
- LIMA-owned DNS, HTTP, socket, or network calls added: no.
- Direct provider egress by LIMA added: no.
- Secret lookup or credential value access added: no.
- Provider token or API key access added: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Consumer production runtime integration added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- V1 product readiness claimed: no.
- Production readiness claimed: no.

## Recommended Next Step

Record exactly one valid operator choice in `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`.

If the intended path is implementation, the choice must be `Approve-V1-G55` using the exact required wording from `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_APPROVAL_REQUEST.md`. Otherwise, keep LIMA at `CANDIDATE_ONLY` and continue only docs/tests/fixtures review, guard, audit, request-revision, or decision-recording work.
