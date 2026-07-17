# V1 Post-G19 Next Lane Decision Matrix

Date: 2026-06-16
Branch: `docs-v1-readiness-rollup-through-g19`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G19. The current chain is capability-open and authority-gated, but still candidate-only. V1-G19 proves LIMA-side live approval evidence/capture metadata; it does not approve raw approval-factor verification, approval-token issuance, execution, provider/model routing, final API freeze, consumer integration, or product readiness.

## Recommendation

Recommended next lane: `V1-G20 provider/model routing authority approval request`.

Reason: V1-G19 gives LIMA a non-executing approval evidence/capture boundary. The next product-moving gap is provider/model routing authority metadata, because Sparkbot and Arc-Bot-shell need a governed way to describe model-route intent, fallback posture, provider boundary, tool-pack scope, credential non-exposure, and audit linkage before LIMA can later support real model selection or consumer integration.

Recommended order:

1. Provider/model routing authority metadata lane
2. Consumer integration compatibility/freeze lane
3. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
4. Connector authority lane
5. Browser/network authority lane
6. Final public API freeze lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider/model routing authority metadata lane | Defines governed model-route intent, fallback, tool-pack scope, provider boundary, and audit linkage without live provider calls. | High. | V1-G11, V1-G12, V1-G15, V1-G18, V1-G19, shell/harness capability profiles, approval evidence metadata, credential policy. | Dedicated V1-G20 approval request. | Likely `lima/harness/`, `lima/guardian/`, docs/tests/fixtures. | Stop on live provider calls, credentials, external sends, unscoped model access, consumer wiring, product readiness claims. | Route metadata tests, fallback metadata tests, no credential tests, no live call tests, blocked unsafe-routing tests, audit-link tests. | Yes. It is the next needed non-executing authority boundary for Sparkbot and shell compatibility. |
| Consumer integration compatibility/freeze lane | Starts checking whether Sparkbot and Arc Bot can safely consume candidate outputs without wiring live runtime paths. | High. | V1-G18 proof intake, V1-G19 approval evidence, authority-chain audit, compatibility criteria, export review. | Dedicated compatibility/freeze approval request. | Docs/tests/export compatibility fixtures first; no consumer repo edits. | Stop on consumer repo mutation, live imports/calls, final freeze bypass, product-readiness claims. | Import-surface tests, fixture compatibility tests, no runtime call tests, no consumer mutation tests. | Later. Useful after provider/model boundaries are clearer. |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17, V1-G19, stronger rollback proof, shell policy proof, workspace/root safety proof, consumer evidence. | Dedicated execution-lane approval request. | Likely filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw content persistence, consumer wiring. | Local sandbox execution tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests, no raw secret persistence tests. | Not next. Execution should wait until routing and compatibility boundaries are clearer. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than provider/model metadata. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Final public API freeze lane | Stabilizes LIMA exports for consumer integration. | High. | Audited core authority lanes, provider/model metadata, compatibility review, proof packets, unresolved API gaps closed. | Dedicated final API freeze approval gate. | Docs/tests/export review and compatibility fixtures. | Stop on unresolved authority gaps, unreviewed exports, consumer breakage, runtime export cleanup without approval. | API surface diff tests, import tests, compatibility fixtures, release-boundary audit. | Not yet. Candidate exports remain intentionally unfrozen. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g20-provider-model-routing-authority-approval-request`.

Do not start provider/model routing implementation, live provider calls, credential handling, consumer integration, actual file mutation execution, connector, browser/network, physical-world, final API freeze, or product-readiness work until their own approval gates exist.
