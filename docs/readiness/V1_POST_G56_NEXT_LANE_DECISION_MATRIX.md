# V1 Post-G56 Next Lane Decision Matrix

Date: 2026-06-19
Branch: `docs-v1-post-g56-next-lane-decision-matrix`
API status: `CANDIDATE_ONLY`

This matrix compares the next candidate lanes after V1-G56. G56 proves consumer fake-executor compatibility against the public V1-G55 wrapper with fake in-process executors only.

## Recommendation

Recommended next direction: prepare the next exact operator request for the provider execution hardening/authorization lane first, then proceed only after explicit approval and a bounded preflight audit.

Provider execution must still remain non-production, fake-boundary, and evidence-first until a dedicated approval gate is passed.

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Why It Should or Should Not Come Next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider SDK/network egress execution request | Defines whether LIMA and first consumers move from fake-executor smoke to the next bounded provider execution proof lane. | High. | G55 wrapper proof, G54 fake harness, G53 authority metadata, G56 fake-executor smoke evidence. | Dedicated next provider-execution request packet for the intended execution lane. | LIMA request docs/tests/fixtures only (no runtime behavior) initially. | Stop on credentials, built-in SDK clients, endpoint resolution, LIMA-owned network calls, raw secret handling, connector/browser/network authority, or product-readiness claims. | Request packet static tests, prior evidence checks, fake-executor boundary checks. | Yes, only if no additional capability is being opened at once. |
| Provider credential/network hardening extension | Tightens who can authorize provider credentials and network egress before live execution. | Critical. | G48/G53/G56 evidence; explicit scope for credential policy. | Dedicated approval packet for hardening extension. | Request docs/tests/fixtures and possibly policy references. | Stop on ambient secret lookup, credential values in outputs, endpoint broadening. | Redaction/no-secret tests, policy reference checks, denial tests. | Later; should follow any next proof lane decision. |
| Fallback execution lane | Adds controlled fallback/retry policy if primary provider path fails. | High. | Stable provider egress contract and approved credential/network policy. | Dedicated fallback approval request. | Contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, safety bypass, cost/policy bypass, missing audit linkage. | Fallback deny/allow tests, policy tests. | Not before provider execution proof and hardening are approved. |
| Connector/browser/network authority lane | Adds governed connector and browser/network behavior beyond provider egress. | Critical. | Provider execution and hardening are not yet production-ready; dedicated threat model required. | Dedicated connector/browser authority request. | LIMA contracts/docs/tests only initially. | Stop on live connector calls, external sends, customer data handling without approval, consumer integration bypass. | No-live-call static tests, tenant-scope tests, audit-link tests. | Too early; broader blast radius than provider execution progression. |
| Consumer production runtime integration lane | Wires consumer production runtime paths to LIMA after authority and evidence readiness. | Critical. | Complete prior authority lanes and approved consumer gating docs. | Dedicated consumer integration request packet. | Consumer runtime/source files only after approval. | Stop on bypass imports, route wiring without Guardian, raw prompt persistence, live provider path before approval. | Consumer integration tests and rollback/audit tests. | Later; requires earlier proof lanes and explicit operator approval. |
| Physical-world/device/robot/drones/IoT lane | Introduces physical-world and device actions if ever needed. | Critical. | Dedicated safety model, emergency stop, rollback, and operator policy. | Dedicated physical-world authority request. | Threat model, contracts, proofs, and tests only initially. | Stop on live device discovery, pairing, movement/actuation, credential operations. | Threat/risk/static tests; simulator validation first. | Not now. Needs dedicated safety model. |
| Product-readiness lane | Final release readiness after all capability and operational lanes are approved. | Critical. | All prerequisite runtime, security, consumer, and operational evidence. | Dedicated product-readiness request packet. | Readiness checklists and evidence bundles only until approval. | Stop on unresolved security or rollback gaps. | Readiness audits and runbook evidence. | Not now. Current state is proof-only and candidate-only. |

## Decision

Proceed first to the next exact operator approval request for the provider execution lane after this matrix is captured. No provider runtime behavior may be added until that gate is explicitly approved.
