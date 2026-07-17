# V1 Post-G17 Next Lane Decision Matrix

Date: 2026-06-16
Branch: `docs-v1-post-g17-next-lane-decision-matrix`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G17. The current chain is capability-open and authority-gated, but still candidate-only. V1-G17 proves non-mutating preview/diff metadata; it does not approve actual file mutation execution or consumer integration.

## Recommendation

Recommended next lane: `V1-G18 consumer proof packet audit intake approval request`.

Reason: V1-G17 now proves preview/diff metadata without mutation. Actual guarded file mutation execution is still too risky without stronger approval, rollback, shell policy, and consumer evidence. A LIMA-side consumer proof packet audit intake lane can gather integration evidence without touching consumer repos or wiring runtime paths.

Recommended order:

1. Consumer proof packet audit intake lane
2. Live approval enforcement lane
3. Provider/model routing authority lane
4. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
5. Connector authority lane
6. Browser/network authority lane
7. Final public API freeze lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17, stronger approval enforcement, rollback proof, shell policy proof, workspace/root safety proof. | Dedicated execution-lane approval request. | Likely filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw content persistence, consumer wiring. | Local sandbox execution tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests, no raw secret persistence tests. | Not next. Execution should wait for stronger approval/rollback/shell policy evidence. |
| Consumer proof packet audit intake lane | Lets LIMA receive and audit consumer proof packets without editing consumer repos or wiring runtime paths. | Medium. | V1-G15/G16/G17 candidate contracts, proof packet criteria, current non-integration boundaries. | Dedicated V1-G18 approval request. | LIMA docs/audits/fixtures/tests only; no consumer repo changes. | Stop on consumer repo mutation, runtime imports/calls, final freeze bypass, product readiness claims, live execution claims. | Static packet validation, required artifact fields, status ledger checks, no import/copy tests, blocked/missing packet tests. | Yes. This is the safest product-moving next lane. |
| Live approval enforcement lane | Moves from sanitized approval proof metadata toward live approval capture or verification semantics. | High. | V1-G14, V1-G15, V1-G16, V1-G17, raw PIN/token policy, actor/session scope, audit linkage. | Dedicated live approval enforcement approval request. | Likely `lima/guardian/` approval modules plus docs/tests/fixtures. | Stop on raw PIN persistence, token issuance without policy, approval metadata becoming broad authority, execution authority, consumer wiring. | Forged/stale/replayed/denied/revoked approval tests, no raw PIN/token persistence tests, no execution tests. | Soon, but consumer proof intake should come first to ground shell needs. |
| Provider/model routing authority lane | Enables governed model selection, fallback, and tool-pack scoping under Guardian authority. | High. | Shell/harness capability profiles, model boundary policy, tenant/session scope, audit evidence, credential policy, consumer proof evidence. | Dedicated provider/model routing approval request. | Likely `lima/harness/`, `lima/guardian/`, docs/tests/fixtures. | Stop on live provider calls, credentials, external sends, unscoped model access, product readiness claims. | Route metadata tests, no credential tests, no live call tests, blocked unsafe routing tests. | Later. Should follow consumer proof intake and approval authority maturation. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than consumer proof intake. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Final public API freeze lane | Stabilizes LIMA exports for consumer integration. | High. | Audited core authority lanes, compatibility review, proof packets, unresolved API gaps closed. | Dedicated final API freeze approval gate. | Docs/tests/export review and compatibility fixtures. | Stop on unresolved authority gaps, unreviewed exports, consumer breakage, runtime export cleanup without approval. | API surface diff tests, import tests, compatibility fixtures, release-boundary audit. | Not yet. Candidate exports remain intentionally unfrozen. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-consumer-proof-packet-audit-intake-approval-request`.

Do not start consumer proof packet intake implementation, consumer integration, actual file mutation execution, live approval capture, provider/model routing, connector, browser/network, physical-world, final API freeze, or product-readiness work until their own approval gates exist.
