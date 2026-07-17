# V1 Post-G16 Next Lane Decision Matrix

Date: 2026-06-16
Branch: `docs-v1-post-g16-next-lane-decision-matrix`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G16. The current chain is capability-open and authority-gated, but still candidate-only. V1-G16 proves guarded file mutation policy metadata; it does not approve dry-run preview/diff behavior or actual file mutation execution.

## Recommendation

Recommended next lane: `V1-G17 file mutation preview/diff approval request`.

Reason: V1-G16 now defines the guarded file mutation policy contract. The next safest product-moving step is to prove dry-run preview and redacted diff/patch metadata before any execution lane. Actual guarded file mutation execution should wait until preview/diff/rollback behavior is separately approved, implemented, tested, and audited.

Recommended order:

1. File mutation dry-run preview/diff lane
2. Consumer proof packet audit intake
3. Live approval enforcement
4. Provider/model routing authority
5. Actual guarded file mutation execution only after preview/diff/rollback policies are proven
6. Connector authority
7. Browser/network authority
8. Final public API freeze
9. Physical-world/device/robot/drone/IoT authority

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| File mutation dry-run preview/diff lane | Gives users inspectable, non-mutating file change previews before approval or execution. | High. | V1-G11, V1-G12, V1-G14, V1-G15, V1-G16, redaction policy, workspace/root scope policy. | Dedicated V1-G17 preview/diff approval request. | Likely `lima/guardian/` and possibly `lima/io/filesystem/` preview metadata contracts, docs/tests/fixtures; no writes. | Stop on actual file reads beyond approved fixtures, raw file content persistence, writes, deletes, patch apply, consumer wiring, provider/model calls. | Positive preview metadata tests, redaction tests, path scope tests, no-write/no-delete regression tests, raw content fail-closed tests. | Yes. This is the next safest product-moving lane. |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17 preview/diff, rollback plan, durable audit, live approval policy, exact execution approval. | Dedicated execution-lane approval request after preview/diff audit. | Likely filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw secret persistence, consumer wiring. | Integration-style local sandbox tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests. | No. Execution should wait until preview/diff/rollback behavior is proven. |
| Live approval enforcement lane | Moves from sanitized approval proof metadata toward live approval capture/verification semantics. | High. | V1-G14, V1-G15, V1-G16, raw PIN/token policy, audit linkage, actor/session scope. | Dedicated live approval enforcement approval request. | Likely `lima/guardian/` approval modules plus docs/tests/fixtures. | Stop on raw PIN persistence, token issuance without policy, approval metadata becoming broad authority, execution authority, consumer wiring. | Forged/stale/replayed/denied/revoked approval tests, no raw PIN/token persistence tests, no execution tests. | Not first. Useful soon, but preview/diff should come first for file workflows. |
| Provider/model routing authority lane | Enables governed model selection, fallback, and tool-pack scoping under Guardian authority. | High. | Shell/harness capability profile, model boundary policy, tenant/session scope, audit evidence, credentials handling policy. | Dedicated provider/model routing approval request. | Likely `lima/harness/`, `lima/guardian/`, docs/tests/fixtures. | Stop on live provider calls, credentials, external sends, unscoped model access, product readiness claims. | Route metadata tests, no credential tests, no live call tests, blocked unsafe routing tests. | Later. Needs preview/diff and approval authority maturity first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Shell/harness contract, connector capability profiles, tenant scope, approval policy, audit retention, consumer proof. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than local preview/diff. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy. | Dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Consumer proof packet audit lane | Allows LIMA to assess whether consumers are ready to integrate against candidate contracts. | Medium to high. | Current candidate contracts, proof packet criteria, consumer evidence, no runtime import/copy. | Per-consumer proof/audit request; integration approval remains separate. | LIMA docs/audits/fixtures/tests only. | Stop on consumer repo changes, runtime wiring, final freeze bypass, product readiness claims. | Static packet validation, evidence review, no import/copy tests. | Soon after preview/diff request preparation. It can run safely without integration. |
| Final public API freeze lane | Stabilizes LIMA exports for consumer integration. | High. | Audited core authority lanes, compatibility review, proof packets, unresolved API gaps closed. | Dedicated final API freeze approval gate. | Docs/tests/export review and compatibility fixtures. | Stop on unresolved authority gaps, unreviewed exports, consumer breakage, runtime export cleanup without approval. | API surface diff tests, import tests, compatibility fixtures, release-boundary audit. | Not yet. Candidate exports remain intentionally unfrozen. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety lane. |

## Decision

Proceed next to `prepare-v1-file-mutation-preview-diff-approval-request`.

Do not start file mutation preview/diff implementation, actual file mutation execution, live approval capture, provider/model routing, connector, browser/network, physical-world, final API freeze, or consumer integration work until their own approval gates exist.
