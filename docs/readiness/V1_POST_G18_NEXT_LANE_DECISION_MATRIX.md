# V1 Post-G18 Next Lane Decision Matrix

Date: 2026-06-16
Branch: `docs-v1-readiness-rollup-through-g18`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G18. The current chain is capability-open and authority-gated, but still candidate-only. V1-G18 proves LIMA-side consumer proof packet audit intake metadata; it does not approve consumer integration, execution, provider/model routing, final API freeze, or product readiness.

## Recommendation

Recommended next lane: `V1-G19 live approval evidence/capture approval request`.

Reason: V1-G18 now gives LIMA a non-executing proof-packet intake boundary for Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, and future shells. The next product-moving gap is live approval evidence/capture semantics, because guarded file mutation, provider/model routing, connector authority, browser/network authority, and future consumer integration all need stronger approval evidence before they can safely proceed.

Recommended order:

1. Live approval evidence/capture lane
2. Provider/model routing authority lane
3. Consumer integration compatibility/freeze lane
4. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
5. Connector authority lane
6. Browser/network authority lane
7. Final public API freeze lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Live approval evidence/capture lane | Moves from sanitized approval proof metadata toward a concrete, governed approval evidence capture or verification boundary. | High. | V1-G14, V1-G15, V1-G16, V1-G17, V1-G18, raw PIN/token policy, actor/session/tenant/shell scope, audit linkage. | Dedicated V1-G19 approval request. | Likely `lima/guardian/` approval evidence modules plus docs/tests/fixtures. | Stop on raw PIN persistence, approval-token issuance, approval metadata becoming broad authority, execution authority, consumer wiring, provider/model calls. | Forged/stale/replayed/denied/revoked approval tests, no raw PIN/token persistence tests, audit-link tests, no execution tests. | Yes. Approval evidence must mature before execution, routing, connector, or integration lanes. |
| Provider/model routing authority lane | Enables governed model selection, fallback, and tool-pack scoping under Guardian authority. | High. | Shell/harness capability profiles, model boundary policy, tenant/session scope, audit evidence, credential policy, consumer proof evidence, approval evidence lane. | Dedicated provider/model routing approval request. | Likely `lima/harness/`, `lima/guardian/`, docs/tests/fixtures. | Stop on live provider calls, credentials, external sends, unscoped model access, product readiness claims. | Route metadata tests, no credential tests, no live call tests, blocked unsafe routing tests. | Later. Should follow approval authority maturation. |
| Consumer integration compatibility/freeze lane | Starts checking whether Sparkbot and Arc Bot can safely consume candidate outputs without wiring live runtime paths. | High. | V1-G18 proof intake, authority-chain audit, compatibility criteria, export review. | Dedicated compatibility/freeze approval request. | Docs/tests/export compatibility fixtures first; no consumer repo edits. | Stop on consumer repo mutation, live imports/calls, final freeze bypass, product-readiness claims. | Import-surface tests, fixture compatibility tests, no runtime call tests, no consumer mutation tests. | Later. Useful after approval evidence and provider/model boundaries are clearer. |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17, stronger approval enforcement, rollback proof, shell policy proof, workspace/root safety proof, consumer evidence. | Dedicated execution-lane approval request. | Likely filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw content persistence, consumer wiring. | Local sandbox execution tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests, no raw secret persistence tests. | Not next. Execution should wait for stronger approval and rollback evidence. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than approval evidence maturation. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Final public API freeze lane | Stabilizes LIMA exports for consumer integration. | High. | Audited core authority lanes, compatibility review, proof packets, unresolved API gaps closed. | Dedicated final API freeze approval gate. | Docs/tests/export review and compatibility fixtures. | Stop on unresolved authority gaps, unreviewed exports, consumer breakage, runtime export cleanup without approval. | API surface diff tests, import tests, compatibility fixtures, release-boundary audit. | Not yet. Candidate exports remain intentionally unfrozen. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g19-live-approval-evidence-capture-approval-request`.

Do not start live approval evidence/capture implementation, provider/model routing, consumer integration, actual file mutation execution, connector, browser/network, physical-world, final API freeze, or product-readiness work until their own approval gates exist.
