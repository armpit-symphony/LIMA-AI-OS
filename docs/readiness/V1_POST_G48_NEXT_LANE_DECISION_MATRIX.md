# V1 Post-G48 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g48`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G48. The current chain is capability-open and authority-gated, but still candidate-only. V1-G48 defines reference-only credential and provider-network hardening metadata with deny-by-default egress. It does not add real provider executors, provider SDK clients, credential access, endpoint resolution, network egress, fallback execution, connector/browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G49 real provider executor approval request`.

Reason: the metadata boundary now exists. The next safe step is not implementation; it is a request-only gate that asks whether to open a tightly bounded real provider executor lane and defines the exact authority model before any provider executor, SDK, credential, or network code is added.

Recommended order:

1. Real provider executor approval request
2. Real provider executor metadata/design implementation only after exact approval
3. Built-in provider SDK integration request, if still needed
4. Provider network egress execution request, if not covered by the executor gate
5. Fallback execution approval request
6. Connector/browser/network authority lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model
8. Product-readiness lane only after runtime, security, field operations, and rollback evidence exist

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Real provider executor request | Defines whether LIMA should add a bounded real provider executor lane after credential/network hardening metadata. | Critical. | V1-G46 wrapper, V1-G47 consumer fake-executor proof, V1-G48 credential/network hardening metadata and audits. | Dedicated V1-G49 approval request. | LIMA request docs/tests/fixtures only; no runtime, no secrets, no network, no SDK, no consumer edits in the request. | Stop on credential value access, raw secrets, live network calls, provider config edits, SDK code, fallback, connector behavior, product-readiness claims. | Approval-request fixture tests, authority-chain tests, no-secret/no-network assertions. | Yes, as a request-only gate. |
| Real provider executor metadata/design implementation | Adds exact metadata/design/tests for one bounded executor lane without yet invoking live services unless separately approved. | Critical. | Approved V1-G49 request. | Dedicated implementation approval recorded from V1-G49. | Likely LIMA docs/tests/fixtures first; runtime only if explicitly approved. | Stop on real secrets, credential values, live egress, SDK clients unless approved, fallback execution, connectors, production claims. | Static authority tests, fail-closed metadata tests, audit/redaction linkage tests. | Later. It requires explicit approval first. |
| Built-in provider SDK integration | Adds first SDK-backed provider adapter if required by the executor lane. | Critical. | Real provider executor authority, credential/network hardening, provider-specific scope, timeout/cost policy, audit policy. | Dedicated provider SDK approval request. | LIMA harness/provider adapter docs/tests/runtime only after approval. | Stop on ambient secrets, broad SDK access, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite. | Later. Do not add SDK code before an exact SDK gate. |
| Provider network egress execution lane | Opens direct egress under scoped network policy if not covered elsewhere. | Critical. | Credential/network hardening, egress policy, endpoint allowlist, audit/approval evidence, timeout and retry policy. | Dedicated egress approval request. | Contracts/docs/tests first; runtime only after approval. | Stop on unscoped endpoints, DNS bypass, proxy bypass, missing audit, raw data persistence, fallback bypass. | Egress deny/allow tests, endpoint-scope tests, no-secret tests. | Later. It should not precede real executor request design. |
| Fallback execution lane | Opens controlled failover behavior after first real execution path is governed. | High. | Live execution wrapper, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede first real executor design. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider/model execution. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g49-real-provider-executor-approval-request`.

Do not start real provider executor implementation, built-in provider SDK integration, credential handling, secret lookup, direct network calls, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
