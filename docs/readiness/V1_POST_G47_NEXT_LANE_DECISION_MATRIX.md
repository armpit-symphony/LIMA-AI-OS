# V1 Post-G47 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g47`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G47. The current chain is capability-open and authority-gated, but still candidate-only. V1-G47 proves that Sparkbot and Arc-Bot-shell can import the public V1-G46 harness wrapper and call it with fake in-process provider executors only. It does not add real provider executors, provider SDK clients, credential access, network egress, fallback execution, connector/browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G48 provider credential/network hardening approval request`.

Reason: the next risk boundary is not another fake executor. It is the authority model for secrets, credential references, provider egress, redaction, audit retention, failure handling, and deny-by-default behavior before any real provider execution or SDK integration exists.

Recommended order:

1. Provider credential/network hardening approval request
2. Provider credential/network hardening docs/tests/fixtures only after exact approval
3. Real provider executor request after credential/network hardening exists
4. Built-in provider SDK integration request, if still needed
5. Fallback execution approval request
6. Connector/browser/network authority lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model
8. Product-readiness lane only after runtime, security, field operations, and rollback evidence exist

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider credential/network hardening request | Defines how real provider secrets, credential refs, and egress boundaries would be governed later. | Critical. | V1-G46 wrapper, V1-G47 consumer fake-executor proof, existing secret/audit/redaction policy docs. | Dedicated V1-G48 approval request. | LIMA request docs/tests/fixtures only; no runtime, no secrets, no network, no consumer edits in the request. | Stop on credential value access, raw secrets, real network calls, provider config edits, SDK code, fallback, connector behavior, product-readiness claims. | Approval-request fixture tests, no-secret-value tests, denied-network tests, audit/redaction linkage tests. | Yes. It defines the next risk boundary before real provider work. |
| Provider credential/network hardening implementation | Adds metadata contracts/tests for credential references, provider egress policy, redaction, and audit evidence. | Critical. | Approved V1-G48 request. | Dedicated implementation approval recorded from V1-G48. | LIMA docs/tests/fixtures, possibly contracts if explicitly approved. | Stop on real secrets, credential values, live egress, SDK clients, fallback execution, connectors, production claims. | Static contract tests, fail-closed metadata tests, no-value/no-network assertions. | Later. It requires explicit approval first. |
| Real provider executor request | Opens the first gate toward a real executor after credential/network hardening. | Critical. | Credential/network hardening complete and audited. | Dedicated real-provider-executor approval request. | Request docs/tests/fixtures first; no implementation before approval. | Stop on ambiguous provider scope, missing egress/credential/audit policy, raw prompt/output persistence, fallback bypass. | Approval packet tests, authority-chain tests. | Later. It should not precede hardening. |
| Built-in provider SDK integration | Adds first SDK-backed provider adapter if the injected executor boundary is insufficient. | Critical. | Credential/network hardening, real executor gate, provider-specific scope, timeout/cost policy, audit policy. | Dedicated provider SDK approval request. | LIMA harness/provider adapter docs/tests/runtime only after approval. | Stop on ambient secrets, broad SDK access, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite. | Later. Do not add SDK code before credential/network hardening. |
| Fallback execution lane | Opens controlled failover behavior after first real execution path is governed. | High. | Live execution wrapper, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede hardening or first real executor design. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider/model hardening. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g48-provider-credential-network-hardening-approval-request`.

Do not start real provider executor integration, built-in provider SDK integration, credential handling, secret lookup, direct network calls, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
