# V1 Post-G51 Next Lane Decision Matrix

Date: 2026-06-18
Branch: `docs-v1-readiness-rollup-through-g51`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G51. The current chain is capability-open and authority-gated, but still candidate-only. V1-G51 adds a bounded caller-injected executable provider executor invocation wrapper. It does not add built-in provider SDK clients, credential access, endpoint resolution, direct network egress, fallback execution, connector/browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G52 consumer fake-executor provider invocation smoke approval request`.

Reason: the G51 wrapper now exists and is exported through `lima.harness`. The next safe step is not SDK or network work; it is a request-only gate for focused Sparkbot and Arc-Bot-shell tests proving both consumers can import and call the G51 public wrapper with fake injected executors only.

Recommended order:

1. Consumer fake-executor provider invocation smoke approval request
2. Consumer fake-executor provider invocation smoke implementation only after exact approval
3. Built-in provider SDK integration request, if needed
4. Provider endpoint resolution and network egress request
5. Fallback execution approval request
6. Connector/browser/network authority lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model
8. Product-readiness lane only after runtime, security, field operations, and rollback evidence exist

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer fake-executor provider invocation smoke request | Asks whether Sparkbot and Arc-Bot-shell should prove import/call compatibility with the G51 wrapper. | Medium. | V1-G51 wrapper, public harness exports, V1-G22 fixture refresh, V1-G47 consumer smoke precedent. | Dedicated V1-G52 approval request. | LIMA request docs/tests/fixtures only; no consumer edits in the request. | Stop on live provider calls, SDK code, network calls, secrets, credentials, consumer production runtime calls, product-readiness claims. | Approval-request fixture tests and static no-secret/no-network assertions. | Yes, as a request-only gate. |
| Consumer fake-executor provider invocation smoke implementation | Adds focused Sparkbot and Arc-Bot-shell tests/fixtures that call the G51 wrapper with fake executors only. | Medium. | Approved V1-G52 request. | Dedicated implementation approval recorded from V1-G52. | Exact consumer test/fixture files plus LIMA evidence files named by request. | Stop on consumer production runtime edits, live provider credentials, SDK imports, network calls, endpoint resolution, fallback, connectors, product claims. | Consumer focused tests, LIMA evidence tests, diff checks across repos. | Later. It requires explicit approval first. |
| Built-in provider SDK integration | Adds first SDK-backed provider adapter if required by future live integration. | Critical. | G51 wrapper, credential/network hardening, provider-specific scope, timeout/cost policy, audit policy, consumer smoke proof. | Dedicated provider SDK approval request. | LIMA harness/provider adapter docs/tests/runtime only after approval. | Stop on ambient secrets, broad SDK access, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite. | Later. Do not add SDK code before an exact SDK gate. |
| Provider endpoint and network egress lane | Opens direct egress under scoped network policy. | Critical. | Credential/network hardening, egress policy, endpoint allowlist, audit/approval evidence, timeout and retry policy. | Dedicated egress approval request. | Contracts/docs/tests first; runtime only after approval. | Stop on unscoped endpoints, DNS bypass, proxy bypass, missing audit, raw data persistence, fallback bypass. | Egress deny/allow tests, endpoint-scope tests, no-secret tests. | Later. It should not precede consumer fake-executor proof. |
| Fallback execution lane | Opens controlled failover behavior after first real execution path is governed. | High. | Live execution wrapper, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede first governed consumer smoke proof. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider/model execution. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g52-consumer-fake-executor-provider-invocation-smoke-approval-request`.

Do not start consumer edits, built-in provider SDK integration, credential handling, secret lookup, direct network calls, endpoint resolution, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
