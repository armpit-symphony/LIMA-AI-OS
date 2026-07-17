# V1 Post-G21 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g21`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G21. The current chain is capability-open and authority-gated, but still candidate-only. V1-G21 proves LIMA-side consumer integration compatibility/freeze metadata; it does not approve final public API freeze, runtime export cleanup, consumer repository edits, live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G22 final public API freeze approval request`.

Reason: V1-G21 gives LIMA a sanitized compatibility/freeze metadata validator for candidate export surfaces and consumer import expectations. The next useful step for testing Sparkbot and Arc-Bot-shell safely is a final public API freeze approval gate that can review exports, import surfaces, compatibility fixtures, and unresolved authority gaps before any consumer repo edits or live imports are approved.

Recommended order:

1. Final public API freeze approval request
2. Final public API freeze implementation only if explicitly approved
3. Consumer integration proof-to-import dry-run lane
4. Live provider/model call dispatch lane only after final API freeze and credential policy proof
5. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
6. Connector authority lane
7. Browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Final public API freeze lane | Stabilizes candidate LIMA exports so Sparkbot, Arc-Bot-shell, and future shells can test against a stable import surface. | High. | V1-G18 proof intake, V1-G19 approval evidence, V1-G20 provider/model metadata, V1-G21 compatibility/freeze metadata, authority-chain audit, export review, unresolved API gap review. | Dedicated V1-G22 approval request. | Docs/tests/fixtures plus a LIMA-side final API freeze metadata validator or export-surface audit helper; runtime export cleanup only if explicitly approved. | Stop on unreviewed exports, unresolved authority gaps, consumer repo mutation, live imports/calls, runtime cleanup outside approved file map, product-readiness claims. | API surface diff tests, candidate export tests, import-string/static compatibility tests, no consumer mutation tests, no runtime call tests, rollback tests. | Yes. It is the next needed bridge before consumer repo edits or live imports. |
| Consumer integration proof-to-import dry-run lane | Converts accepted proof and compatibility packets into non-executing import-plan evidence for Sparkbot and Arc-Bot-shell. | High. | Final API freeze gate, V1-G18, V1-G21, proof packets from target consumers, import-plan criteria. | Dedicated consumer dry-run integration approval request. | Docs/tests/fixtures plus metadata-only import plan validator; no consumer repo edits. | Stop on consumer repo mutation, importing consumer code, live runtime calls, shell wiring, final freeze bypass, product-readiness claims. | Import-plan fixture tests, no runtime import tests, no consumer mutation tests, proof linkage tests. | Later. It should wait for a final public API freeze gate. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, final API freeze, credential policy, Vault boundary, audit persistence, consumer compatibility, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Not next. Freeze the public surface first. |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17, V1-G19, final API posture, stronger rollback proof, shell policy proof, workspace/root safety proof, consumer evidence. | Dedicated execution-lane approval request. | Likely filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw content persistence, consumer wiring. | Local sandbox execution tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests, no raw secret persistence tests. | Later. Execution should wait until consumer and public API posture are clearer. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, final API freeze, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than final API metadata. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, final API posture, consumer proof. | Dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Runtime export cleanup lane | Removes or reshapes candidate exports after the final API freeze review decides what is public. | High. | Final API freeze approval, export diff, compatibility proof, rollback plan, consumer notice plan. | Dedicated cleanup approval or explicit inclusion in V1-G22 approval. | `__init__.py` export files, docs/tests/fixtures, compatibility tests. | Stop on unapproved symbol removal, consumer breakage, hidden runtime behavior, live imports/calls, product-readiness claims. | Export-diff tests, import tests, compatibility fixtures, rollback tests. | Only if explicitly included with final freeze. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g22-final-public-api-freeze-approval-request`.

Do not start final public API freeze implementation, runtime export cleanup, consumer repository edits, live consumer imports/calls, live provider/model calls, credential handling, actual file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
