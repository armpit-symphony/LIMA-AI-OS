# V1 Next Authority Lane Decision Matrix

Date: 2026-06-15
Branch: `docs-v1-next-authority-lane-decision-matrix`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G11, V1-G12, and V1-G14.

The model is capability-open and authority-gated. A blocked capability is not impossible forever; it is not authorized by the current gate. Every future capability lane still needs explicit contracts, tests, audit evidence, approval packets, and operator approval before runtime authority expands.

## Recommendation

Recommended next lane: `V1-G15 shell/harness guiderail input contract approval request`.

Reason: V1-G11, V1-G12, and V1-G14 prove local request, evidence, and destructive approval enforcement boundaries. The next product-moving gap is structured guiderail input from shells/harnesses: capability profile, guardrail mode, approval policy, actor/session/tenant scope, allowed capability lanes, and dry-run versus execution-authorized posture. Without that contract, later file mutation, provider/model routing, connector, browser/network, and physical-world authority lanes would be underspecified.

Recommended order:

1. shell/harness guiderail input contract lane
2. guarded file mutation policy lane
3. live approval enforcement lane
4. provider/model routing authority lane
5. connector authority lane
6. browser/network authority lane
7. physical-world/device/robot/drone/IoT authority lane
8. final public API freeze lane
9. consumer proof packet audit lane

Consumer integration should happen only after proof packet audits, final API freeze, and explicit integration approval.

## Matrix

| Lane | Purpose | Product Value | Risk Level | Required Prerequisites | Required Approval Packet | Likely File Scope | Stop Conditions | Validation Expectations | Should It Happen Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Guarded file mutation policy lane | Define when approved file edit/delete/mutation can move beyond proof into guarded policy. | Opens path toward real office/file workflows. | High. | V1-G11, V1-G12, V1-G14, shell/harness guiderail contract, rollback expectations. | Yes, dedicated file mutation policy approval request. | Likely `lima/guardian/`, `lima/io/filesystem/` contracts, docs/tests/fixtures only until implementation approval. | Stop on real file mutation, raw file contents, missing rollback, missing approval evidence, consumer wiring. | Fail-closed tests for destructive/non-destructive operations, approval scope, rollback metadata, no raw contents. | Not first. Needs shell/harness guiderail contract to define capability profile and execution posture. |
| Shell/harness guiderail input contract lane | Define structured shell/harness input: capability profile, guardrail mode, approval policy, actor/session/tenant scope, allowed lanes, emergency stop, rollback, dry-run/execution posture. | Establishes the control-plane vocabulary needed for all later authority lanes. | Medium. | V1-G11/G12/G14 evidence, capability-open authority-gated posture doc. | Yes, V1-G15 approval request. | Docs/tests/fixtures first; likely future contract module only after approval. | Stop on runtime wiring, consumer changes, provider/model/tool/browser/network/device behavior. | Static tests for required contract fields and no runtime implementation. | Yes. Safest product-moving next step. |
| Live approval enforcement lane | Move from sanitized approval proof records toward live approval capture or verification semantics. | Enables real operator approval flow design. | High. | Shell/harness guiderail contract, approval actor policy, audit/evidence contract, raw PIN/token policy. | Yes, dedicated live approval enforcement approval request. | Likely `lima/guardian/` approval modules plus docs/tests/fixtures. | Stop on raw PIN persistence, token issuance without contract, execution authority, consumer wiring. | Negative tests for forged approvals, stale/replayed approvals, raw PIN/token handling, no execution. | Not yet. Needs guiderail contract and guarded file mutation policy context. |
| Provider/model routing authority lane | Define authority boundary for model routing/fallback/tool-pack scoping. | Enables governed model use across shells and harnesses. | High. | Shell/harness capability profile, approval/risk policy, audit evidence, model boundary policy. | Yes, dedicated provider/model routing approval request. | Likely `lima/harness/`, `lima/guardian/`, docs/tests/fixtures. | Stop on live provider calls, credentials, external sends, unscoped model access. | Tests for no credentials, no live calls, route metadata only until implementation approval. | Later. Should follow guiderail and approval policy lanes. |
| Connector authority lane | Define authority boundary for external systems and office connectors. | Opens path toward real business workflows. | High. | Shell/harness contract, connector capability profiles, tenant scope, approval policy, audit retention. | Yes, dedicated connector authority approval request. | Likely contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation. | Static and negative tests for connector claims, tenant scope, no live calls. | Later. Needs guiderail and provider/model authority context. |
| Browser/network authority lane | Define browser and network action authorization. | Enables controlled research, web workflows, and network automation. | High. | Shell/harness contract, URL/network policy, audit evidence, approval policy. | Yes, dedicated browser/network approval request. | Likely `lima/io/browser/`, `lima/io/network/`, Guardian contracts, docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Tests for blocked live calls, scoped metadata, approval requirements, audit links. | Later. Needs guiderail contract and connector/network threat model. |
| Physical-world/device/robot/drone/IoT authority lane | Define safety and authority boundary for physical-world systems. | Enables robotics and device governance long term. | Critical. | Dedicated safety lane, hazard model, emergency stop, simulation/dry-run, field validation, operator approval. | Yes, dedicated physical-world authority/safety approval request. | Likely contracts/docs/threat model first; no drivers until later approval. | Stop on live device commands, pairing, discovery, credentials, physical movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware. | Not soon. Must wait for safer software authority lanes. |
| Final public API freeze lane | Freeze public candidate API after enough authority boundaries are audited. | Stabilizes consumers and integration contracts. | High. | Audited core authority lanes, docs, tests, compatibility review, integration proof packets. | Yes, dedicated final API freeze approval gate. | Docs/tests and export review. | Stop on unresolved authority gaps, unreviewed exports, consumer breakage. | API surface diff, import tests, compatibility fixtures, release-boundary audit. | Not next. Too early. |
| Consumer proof packet audit lane | Audit shell/consumer proof packets before integration. | Moves toward real consumer integration safely. | High. | Finalized or near-final contract, proof packet criteria, shell evidence, no unapproved runtime wiring. | Yes, per-consumer proof/audit request. | Docs/audits/fixtures; no consumer repo changes from LIMA branch. | Stop on consumer code changes, runtime wiring, final freeze bypass, product readiness claim. | Static packet validation, evidence review, no runtime import/copy. | Later. Consumer integration waits for proof packet audits and final API freeze. |

## Decision

Proceed next to `prepare-v1-shell-harness-guiderail-contract-approval-request`.

Do not start guarded file mutation, live approval capture, provider/model routing, connector, browser/network, physical-world, final API freeze, or consumer integration work until their own approval gates exist.
