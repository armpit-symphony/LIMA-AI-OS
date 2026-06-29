# V1 Readiness Gap Matrix

This matrix turns the V1 product target into the current implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, provider SDK/network egress, GuardianDecision execution authority, approval enforcement expansion, persistence expansion, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
- Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Current product status: not V1-ready
- API status: `CANDIDATE_ONLY`
- Latest completed gate: `V1-G60`
- Current release-candidate cutover approval: not recorded
- Current active gate: `V1-RC-CUTOVER`
- Current required next action: record exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`
- Current request-stage audit: `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`
- Current preapproval runtime-tree guard audit: `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`
- Current request-stage readiness refresh: `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`
- Current candidate harness quickstart: `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`
- Current candidate harness quickstart execution audit: `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`
- Current consumer harness usability matrix: `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`
- Current release-candidate acceptance checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`
- Current release-candidate cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`
- Current Arc-Bot-shell clean-checkpoint stance: Arc-Bot-shell clean-checkpoint proof is recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`; it is release-gate input evidence only and does not authorize release-candidate acceptance, branch, tag, cutover, product readiness, or production readiness.
- Current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- Current candidate validation refresh audit: `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`
- Current post-validation readiness-change freshness audit: `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`
- Current final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`
- Current validation evidence: 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing
- Current validation latest LIMA readiness freshness supplement: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and full LIMA suite passing with 5361 tests
- Current post-validation freshness evidence: same-turn release/cutover freshness validation and full LIMA suite passing with 5359 tests
- Latest quickstart post-refresh evidence: public Sparkbot 8 tests, accessible Sparkbot 8 tests, Arc-Bot-shell 8 tests, LIMA focused quickstart/handoff 17 tests, broader V1 harness/readiness 108 tests, and full LIMA suite 5360 tests
- Latest final blocker/index freshness evidence: 15 focused final blocker/index tests, 89 broader affected readiness tests, and full LIMA suite 5361 tests passing
- Latest post-G61 request readiness-refresh evidence: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and full LIMA suite 5362 tests passing
- Latest quickstart artifact refresh evidence: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and full LIMA suite 5364 tests passing
- Latest current-goal evidence refresh: 16 focused status tests, 56 broader V1 readiness/status tests, and full LIMA suite 5435 tests passing
- Latest consumer checkpoint freshness refresh: 16 focused consumer/current-goal tests, 56 broader V1 readiness/status tests, and full LIMA suite 5435 tests passing

## Readiness Matrix

| ID | Gap | Current evidence | V1-ready requirement | Recommended lane | Runtime approval needed |
| --- | --- | --- | --- | --- | --- |
| `V1-G1` through `V1-G10` | Static target, first-shell proof, contract, release-boundary, and implementation-gate evidence | Historical docs/tests/fixtures exist and remain part of the V1 evidence base | Keep target, shell proof, approval, haptic, release-boundary, and implementation-gate constraints explicit | Complete as historical candidate-only evidence | No current implementation approval |
| `V1-G11` through `V1-G17` | Typed request, GuardianDecision preflight, audit/evidence persistence, approval-enforcement, shell guiderail, guarded file mutation, and preview/diff slices | Local non-executing metadata proves the earliest Guardian and audit chain | Preserve fail-closed request/decision/evidence behavior | Complete as candidate-only runtime/evidence slices | Already approved and implemented only inside prior scopes |
| `V1-G18` through `V1-G28` | Consumer proof intake, live approval metadata, provider/model routing authority, compatibility/freeze metadata, dry-run/import-plan/patch-preview evidence, consumer repo edits, import smoke, and runtime export cleanup evidence | Consumer-facing evidence stays bounded and audited | Preserve first consumer import and public API evidence without product readiness claims | Complete as candidate-only evidence | Already approved and implemented only inside prior scopes |
| `V1-G29` through `V1-G42` | Consumer import/call planning, fake runtime call evidence, consumer test preview/edit/smoke, live import/call tests, compatibility review, bounded integration design, integration patch/edit/import smoke, shell wiring design and implementation evidence | Consumer and shell integration evidence remains bounded by approval and fake-runtime constraints where required | Preserve testability with Sparkbot and Arc-Bot-shell without claiming production integration | Complete as candidate-only integration evidence | Already approved and implemented only inside prior scopes |
| `V1-G43` through `V1-G56` | Provider/model dispatch, live provider/model authority/execution metadata, fake-executor consumer smoke, credential/network hardening, real provider executor design/invocation/wrapper metadata, provider SDK/network/credential authority, fake SDK/fake-egress harness evidence, bounded real provider SDK/network egress wrapper evidence, and consumer fake-executor SDK/network egress smoke evidence | Provider/model/provider-SDK authority chain exists with caller-injected/fake executors only, without LIMA-owned SDK clients, secrets, credential values, endpoint resolution, or network egress; `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md` defines current Sparkbot and Arc-Bot-shell harness usability as local candidate smoke only | Preserve caller-injected and fake-harness boundaries before any provider execution, credential, fallback, connector, or production lane | Complete through G56 as candidate-only authority and consumer smoke evidence | Already approved and implemented only inside prior scopes |
| `V1-G57` through `V1-G60` | Provider execution hardening authorization metadata, built-in provider SDK client authority contract metadata, SDK dependency/vendor import authority metadata, and approved SDK dependency declaration/import-boundary evidence | G57 through G60 are complete and audited as candidate-only evidence; G60 adds only `openai>=1.0.0,<3.0.0` to `pyproject.toml` | Preserve the separation between dependency declaration, runtime import execution, client construction, credentials, endpoint resolution, network egress, fallback, consumers, and product readiness | Complete through G60 as candidate-only dependency/import-boundary evidence | Already approved and implemented only inside prior scopes |
| `V1-G61` | `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`; `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`; `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`; `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`; `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`; `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`; `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`; `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`; `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`; `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md` | Request-only runtime vendor SDK import execution proof packet is prepared after G60 dependency declaration and import-boundary evidence; request-gate audit passes; preapproval runtime-tree guard audit passes; operator decision packet status audit proves `Approve-V1-G61` is recorded for bounded local import-proof evidence only; post-G61 request readiness refresh is complete; current gate consistency rejects stale G56/G57 blocker language; current validation refresh records 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing plus latest LIMA readiness freshness supplement evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests plus latest handoff freshness supplement evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests; post-validation readiness-change freshness evidence records same-turn validation requirements for later readiness docs, fixtures, or tests with full LIMA suite passing 5359 tests, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests; candidate harness quickstart execution evidence records consumers 8/8/8 and LIMA 17/108/5360 plus latest quickstart artifact refresh 7/64/133/5364; Arc clean-checkpoint proof records clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3` as release-gate input evidence only | Keep the bounded `Approve-V1-G61` import proof closed; preserve current gate consistency, validation refresh, post-validation freshness evidence, latest quickstart evidence, latest final blocker/index freshness evidence, latest post-G61 request readiness-refresh evidence, latest quickstart artifact refresh evidence, Arc drift exclusion evidence, and clean Arc checkpoint proof as required inputs to any future final readiness audit | Bounded local import proof complete; first-consumer final-readiness reconciliation passes; cutover authority still blocked | Yes, before implementation |

## Recommended Order

1. Treat V1-G1 through V1-G60 as accepted candidate-only evidence inside their original approved scopes.
2. Treat the G56 consumer fake-executor provider SDK/network egress smoke audit as the latest completed provider SDK/network consumer compatibility evidence.
3. Treat the G60 dependency declaration as dependency/import-boundary evidence only, not runtime import execution authority.
4. Treat the V1 consumer target state after Arc readiness integration as consumer-side testing evidence only, not runtime authority.
5. Treat the V1 candidate harness quickstart as the shortest safe local Sparkbot and Arc-Bot-shell smoke command path only, not production integration authority.
6. Treat the V1 candidate harness quickstart execution audit as current local public Sparkbot, accessible Sparkbot, and Arc-Bot-shell smoke pass evidence only, including latest consumers 8/8/8 and LIMA 17/108/5360 post-refresh validation, not production integration authority or clean-checkpoint proof for Arc-Bot-shell.
7. Treat the V1 consumer harness usability matrix as current local Sparkbot and Arc-Bot-shell candidate smoke criteria only, not production integration authority.
8. Treat the V1 release-candidate acceptance checklist as satisfied for first-consumer harness testing only, with current verdict `CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`.
9. Treat the V1 release-candidate cutover runbook as the future branch/tag procedure only, with current verdict `CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION`; Arc-Bot-shell clean-checkpoint proof is recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md`, and any branch, tag, cutover, V1.0.0 completion, product-readiness, or production-readiness claim still requires exactly one valid cutover operator choice and completed runbook evidence.
10. Treat the V1 current gate consistency audit as the active-gate guardrail that rejects stale G56/G57 blocker language and keeps G61 as the only active implementation blocker.
11. Treat the V1 current candidate validation refresh as current validation evidence only: 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing, plus latest LIMA readiness freshness supplement evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests.
12. Treat the V1 post-validation readiness-change freshness audit as same-turn freshness evidence for later readiness docs, fixtures, or tests, including 5359 release/cutover freshness proof, latest quickstart 5360 full-suite proof, latest final blocker/index 15/89/5361 proof, latest post-G61 request readiness-refresh 8/117/5362 proof, and latest quickstart artifact refresh 7/64/133/5364 proof, not a release approval.
13. Treat the V1 final readiness audit template as a future post-G61 release-candidate audit input, not a release approval.
14. Treat the V1-G61 request-gate audit, preapproval runtime-tree guard audit, operator decision packet status audit, and post-G61 request readiness refresh as evidence that the request is ready for operator decision only.
15. Treat V1-G61 as bounded local import-proof evidence only after `Approve-V1-G61`; do not treat it as release, cutover, product-readiness, or production-readiness authority.
16. Reject any claim that the broad V1 goal, the G60 audit, the readiness rollup, the consumer target refresh, the candidate harness quickstart, the candidate harness quickstart execution audit, the consumer harness usability matrix, the release-candidate acceptance checklist, the release-candidate cutover runbook, the current gate consistency audit, the current candidate validation refresh, the post-validation readiness-change freshness audit, the final readiness audit template, the G61 request-gate audit, the G61 preapproval runtime-tree guard audit, the G61 operator decision packet status audit, the post-G61 request readiness refresh, this matrix, or successful tests approve G61 implementation, lockfile edits, runtime vendor SDK imports in `lima/`, credential value access, fallback, connector/browser/network authority, consumer production runtime integration, or product readiness.

## Stop Conditions

Stop and request a new approval gate before any work that adds:

- V1-G61 runtime vendor SDK import execution proof implementation without exact approval
- file scope outside a future approved V1-G61 request
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell modifications for V1-G61 without exact approval
- release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim that treats Arc smoke or clean-checkpoint proof as sufficient without checklist, final audit, and cutover authorization
- dependency manifest or lockfile edits without exact approval
- runtime vendor SDK imports in `lima/`
- built-in provider SDK clients
- provider client construction
- credential handling or real provider SDK/network egress in an import execution proof lane
- direct provider SDK implementation
- provider endpoint resolution by LIMA
- LIMA-owned DNS, HTTP, socket, network calls, or direct provider egress
- secret lookup, credential value access, provider token access, or API key access
- provider configuration changes
- fallback execution
- consumer production runtime integration
- connector/browser/network/file/device/robotics/physical-world behavior
- V1 product readiness, production readiness, final release, or live customer claims

## Current Verdict

LIMA-AI-OS has a clearer and deeper V1 completed implementation evidence chain through G60, request-stage readiness through the post-G61 refresh, current consumer harness usability criteria and quickstart execution evidence for Sparkbot and Arc-Bot-shell local candidate smoke tests, a release-candidate acceptance checklist, a cutover runbook, a current gate consistency audit, a current candidate validation refresh with 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing plus latest LIMA readiness freshness supplement evidence with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests plus latest handoff freshness supplement evidence with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests, a post-validation readiness-change freshness audit with same-turn full LIMA suite evidence passing 5359 tests, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests, recorded Arc clean-checkpoint proof, and a final readiness audit template for future release-candidate review, but it is not V1 product-ready.

`V1-G56` is complete as consumer fake-executor provider SDK/network egress smoke evidence. The runtime authority chain audit through G56 is complete.

`V1-G57` through `V1-G60` are complete as candidate-only provider hardening, SDK authority, dependency authority, and dependency declaration/import-boundary evidence. `V1-G60` does not approve runtime vendor SDK imports in `lima/`, lockfile edits, client construction, endpoint resolution, network egress, credentials, fallback, consumer production integration, or product readiness.

`V1-G61` is approved only for the bounded local import execution proof, independently audited, protected by the preapproval runtime-tree guard audit, checked by the operator decision packet status audit, and refreshed through post-request readiness evidence. It must not add additional runtime vendor SDK import implementation, consumer repository edits, lockfile edits, runtime imports in `lima/`, SDK clients, endpoint resolution, network calls by LIMA, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, or product-readiness claims.

The next smallest safe step is recording exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`; only `Approve-V1-RC-Cutover` authorizes revalidation and cutover runbook execution before any branch, tag, cutover, or readiness claim. The approved G61 proof only proves the approved vendor SDK module can be imported in a controlled local test context. Stop before additional implementation, lockfile edits, runtime imports in `lima/`, built-in SDK clients, client construction, LIMA-owned endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, physical-world behavior, or product-readiness claims.
