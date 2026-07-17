# V1 Post-G20 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g20`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G20. The current chain is capability-open and authority-gated, but still candidate-only. V1-G20 proves LIMA-side provider/model routing authority metadata; it does not approve live provider calls, model dispatch, fallback execution, secret lookup, final API freeze, consumer integration, or product readiness.

## Recommendation

Recommended next lane: `V1-G21 consumer integration compatibility/freeze approval request`.

Reason: V1-G18 provides proof-packet intake, V1-G19 provides approval evidence metadata, and V1-G20 provides provider/model route authority metadata. The next useful step for Sparkbot and Arc-Bot-shell testing is a consumer compatibility/freeze lane that can validate candidate import surfaces and fixture compatibility without mutating consumer repositories or wiring live runtime paths.

Recommended order:

1. Consumer integration compatibility/freeze metadata lane
2. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
3. Live provider/model call dispatch lane only after compatibility/freeze and credential policy proof
4. Connector authority lane
5. Browser/network authority lane
6. Final public API freeze lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer integration compatibility/freeze metadata lane | Validates whether Sparkbot, Arc-Bot-shell, and future shells can consume candidate LIMA outputs without wiring live runtime paths. | High. | V1-G18 proof intake, V1-G19 approval evidence, V1-G20 provider/model metadata, authority-chain audit, compatibility criteria, export review. | Dedicated V1-G21 approval request. | Docs/tests/fixtures plus a LIMA-side compatibility metadata validator; no consumer repo edits. | Stop on consumer repo mutation, live imports/calls, final freeze bypass, product-readiness claims. | Candidate export-surface tests, fixture compatibility tests, no runtime call tests, no consumer mutation tests, rollback tests. | Yes. It is the next needed bridge before testing Sparkbot and Arc-Bot-shell consumers. |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17, V1-G19, stronger rollback proof, shell policy proof, workspace/root safety proof, consumer evidence. | Dedicated execution-lane approval request. | Likely filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw content persistence, consumer wiring. | Local sandbox execution tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests, no raw secret persistence tests. | Later. Execution should wait until consumer compatibility and final export posture are clearer. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, consumer compatibility/freeze, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Not next. Metadata and compatibility should settle before live dispatch. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than compatibility metadata. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Final public API freeze lane | Stabilizes LIMA exports for consumer integration. | High. | Audited core authority lanes, provider/model metadata, compatibility review, proof packets, unresolved API gaps closed. | Dedicated final API freeze approval gate. | Docs/tests/export review and compatibility fixtures. | Stop on unresolved authority gaps, unreviewed exports, consumer breakage, runtime export cleanup without approval. | API surface diff tests, import tests, compatibility fixtures, release-boundary audit. | Not yet. Candidate exports remain intentionally unfrozen. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g21-consumer-integration-compatibility-freeze-approval-request`.

Do not start consumer integration compatibility implementation, consumer repo edits, live consumer imports/calls, final API freeze, live provider/model calls, credential handling, actual file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
