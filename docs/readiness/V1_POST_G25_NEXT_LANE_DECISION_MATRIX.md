# V1 Post-G25 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g25`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G25. The current chain is capability-open and authority-gated, but still candidate-only. V1-G25 creates Sparkbot and Arc-Bot-shell patch-preview evidence; it does not approve consumer repository edits, live consumer imports/calls, shell wiring, runtime export cleanup, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G26 first consumer repository edit approval request`.

Reason: the patch-preview evidence exists. The next safe step is a read-only local path audit and exact approval packet for applying minimal consumer repository edits. The approval packet must not itself edit consumer repositories.

Recommended order:

1. First consumer repository edit approval request grounded in local path audit
2. Consumer repository edit implementation only after exact approval
3. Consumer repository edit audit
4. Runtime export cleanup only after a separate cleanup gate
5. Live consumer import/call lane only after consumer repo edit evidence is audited
6. Live provider/model call dispatch lane only after credential policy proof
7. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
8. Connector authority lane
9. Browser/network authority lane
10. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| First consumer repository edit approval request | Converts patch-preview evidence into an exact, operator-reviewable edit gate for Sparkbot and Arc-Bot-shell. | High. | V1-G18, V1-G21, V1-G22, V1-G23, V1-G24, V1-G25, authority-chain audit, read-only local path audit. | Dedicated V1-G26 approval request. | LIMA docs/tests/fixtures request files only; no consumer repo edits in the request branch. | Stop on consumer repo mutation, writing files, importing consumer code, live runtime calls, shell wiring, runtime export cleanup, product-readiness claims. | Approval-request fixture tests, local path audit metadata tests, no write tests, rollback-plan tests. | Yes. It is the next approval gate before any consumer edit. |
| Consumer repository edit implementation | Applies the first approved static consumer-side import review changes. | Critical. | Approved V1-G26 request, clean consumer repo status, exact file scope, rollback plan, CI plan. | Dedicated implementation approval recorded from V1-G26. | Only exact Sparkbot and Arc-Bot-shell files named by V1-G26. | Stop on unapproved files, raw secrets, live runtime calls, provider/model calls, external sends, product-readiness claims. | Repo-specific focused tests, no live call tests, rollback checks, proof linkage. | Later. It requires V1-G26 approval first. |
| Runtime export cleanup lane | Removes or reshapes candidate exports after consumer edit evidence is stable. | High. | V1-G22, V1-G25, consumer edit audit, export diff, rollback plan, consumer notice plan. | Dedicated cleanup approval. | Export files, docs/tests/fixtures, compatibility tests. | Stop on unapproved symbol removal, consumer breakage, hidden runtime behavior, live imports/calls, product-readiness claims. | Export-diff tests, import tests, compatibility fixtures, rollback tests. | Later. Cleanup should wait until consumer edit evidence is audited. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Consumer repo edit audit, final API freeze, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests. | Later. Live calls are higher risk than static repo edits. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer repo edit proof should land first. |
| Actual guarded file mutation execution lane | Enables approved real edits/deletes after policy, preview, approval, rollback, and audit are proven. | Critical. | V1-G16, V1-G17, V1-G19, rollback proof, shell policy proof, workspace/root safety proof. | Dedicated execution-lane approval request. | Filesystem adapter boundary, Guardian execution gate, audit/evidence hooks, docs/tests/fixtures. | Stop on missing approval evidence, missing preview, missing rollback, path traversal, out-of-scope paths, raw content persistence, consumer wiring. | Local sandbox execution tests, rollback tests, denied/revoked/stale approval tests, path boundary tests, audit tests. | Later. Execution should wait until consumer posture is clearer. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than repo edit approval. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g26-first-consumer-repository-edit-approval-request` after a read-only local path audit of Sparkbot and Arc-Bot-shell.

Do not start consumer repository edit implementation, runtime export cleanup, live consumer imports/calls, live provider/model calls, credential handling, actual file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
