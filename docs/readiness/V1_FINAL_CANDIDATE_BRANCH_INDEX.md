# V1 Final Candidate Branch Index

Date: 2026-06-28
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before index refresh: `a60700a9bd6f31f1d36b8c3619284da63a6ccd60`
API status: `CANDIDATE_ONLY`

This index records the current saved branch map for the V1 candidate after the latest current-goal and consumer-checkpoint freshness refresh. It is docs/tests/fixtures-only readiness evidence for operator handoff and self-audit traceability.

This index does not approve V1-G61 implementation, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK clients, add runtime vendor SDK imports in `lima/`, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, invoke connectors, wire consumer production runtime behavior, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

This index is not release-candidate branch or tag authority. It records saved candidate lanes and the future cutover sequence only; it does not authorize a branch, tag, release cutover, final-readiness pass, or Arc-Bot-shell clean-checkpoint claim.

## Index Verdict

Verdict: `CANDIDATE_INDEX_READY_WITH_G61_OPERATOR_BLOCKER`

The V1 candidate evidence is saved across LIMA, public Sparkbot, accessible Sparkbot, Sparkbot_shell, and Arc-Bot-shell. Public Sparkbot G56 publication is resolved. V1-G57 through V1-G60 are completed candidate-only evidence, `Approve-V1-G61` is recorded, the bounded G61 proof/closeout exists, and Arc-Bot-shell clean-checkpoint proof is recorded. The release-candidate checklist is satisfied for first-consumer harness testing and final-readiness reconciliation passes for that scope. The candidate is still not V1.0.0 complete because cutover authorization is not recorded, the cutover runbook is not executed, and no branch, tag, cutover, or readiness claim is authorized.

## Current LIMA Branch Checkpoints

| Branch or lane | Commit or label | Purpose |
| --- | --- | --- |
| `docs-v1-post-g60-readiness-and-next-lane-matrix` | `a60700a9bd6f31f1d36b8c3619284da63a6ccd60` | Current observed workspace branch for the latest current-goal and consumer-checkpoint freshness refresh. |
| `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request` | request-stage lane label | Prepares the G61 runtime vendor SDK import execution proof approval request. |
| `audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request` | audit lane label | Independently audits the G61 request gate. |
| `audit-v1-g61-preapproval-runtime-tree-guard` | guard audit label | Records the preapproval runtime-tree guard that fails if LIMA runtime imports the vendor SDK or constructs provider clients before exact approval. |
| `docs-v1-post-g61-request-readiness-refresh` | readiness lane label | Refreshes status after the G61 request-gate audit. |
| `audit-v1-g61-operator-decision-packet-status` | status audit lane label | Records that `Approve-V1-G61` is recorded for bounded local import-proof evidence only and not release approval. |
| `docs-v1-candidate-harness-quickstart-execution-audit` | quickstart audit lane label | Records local public Sparkbot, accessible Sparkbot, and Arc-Bot-shell quickstart execution proof while preserving the G61 operator blocker. |
| `audit-v1-current-gate-consistency` | consistency audit lane label | Locks current-facing status, release, and handoff artifacts to the active G61 operator-decision gate. |
| `audit-v1-post-validation-readiness-change-freshness` | freshness audit lane label | Locks same-turn readiness edits after the validation refresh to release/cutover freshness checks and a 5359-test full LIMA suite pass without creating release authority. |
| `audit-v1-arc-bot-shell-local-drift-exclusion` | Arc drift audit lane label | Records historical Arc-Bot-shell local drift as compatibility-only context; superseded for release-gate evaluation by clean-checkpoint proof at `99a4ba4955f13626c2176a2c44592000029a16c3`. |
| `docs-v1-release-candidate-acceptance-checklist` | checklist lane label | Defines the V1.0.0 acceptance bar; currently satisfied for first-consumer harness testing with cutover authorization still required. |
| `docs-v1-release-candidate-cutover-runbook` | runbook lane label | Defines the future branch/tag cutover sequence after the checklist and final audit pass; currently blocked. |
| `docs-v1-final-blocker-index-freshness` | freshness supplement label | Records latest final blocker/register and branch-index readiness freshness with 15 focused tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests. |
| `docs-v1-post-g61-request-readiness-freshness` | latest request freshness supplement label | Records latest post-G61 request readiness freshness with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests. |
| `docs-v1-quickstart-artifact-freshness` | latest quickstart artifact freshness supplement label | Records latest quickstart artifact freshness with 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests. |
| `docs-v1-handoff-freshness` | latest handoff freshness supplement label | Records combined latest handoff freshness with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests. |
| `v1-g61-runtime-vendor-sdk-import-execution-proof` | proposed future implementation branch | May be used only if `Approve-V1-G61` is explicitly recorded. |

## Consumer Checkpoints

| Repo | Local path | Branch | Commit | Status |
| --- | --- | --- | --- | --- |
| Public Sparkbot target checkout | `C:\Users\limap\Sparkbot-public` | `v1-g56-runtime-authority-chain-audit` | `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | clean local branch; public G56 target publication resolved by audit |
| Accessible Sparkbot checkpoint | `C:\Users\limap\Sparkbot` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ddaa4ccaacd328ddcc1f00a040c2c140abee428e` | clean local branch tracking origin |
| Sparkbot_shell checkpoint | `C:\Users\limap\Sparkbot_shell` | `sparkbot-shell-work-settings-runtime-preview` | `548b6d6aa6cde98b261e867c0c2db86ddbfa83dc` | clean local branch tracking origin; shell checkpoint only |
| Arc-Bot-shell checkpoint | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `40fc474b0e09580a82f90518ebe341e2c98cd644` | clean local branch tracking origin; descends from clean checkpoint proof `99a4ba4955f13626c2176a2c44592000029a16c3`; release authority remains blocked |

## Current Validation Evidence

- Consumer quickstart smoke refresh: passed, public Sparkbot 8 tests, accessible Sparkbot 8 tests, and Arc-Bot-shell 8 tests.
- Arc-Bot-shell clean-checkpoint proof: recorded at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`; release-candidate/final-readiness authority remains blocked.
- LIMA post-validation readiness freshness full suite: passed, same-turn evidence 5359 tests after release/cutover freshness checks.
- LIMA quickstart post-refresh validation: passed, 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests.
- LIMA latest final blocker/index readiness refresh: passed, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests.
- LIMA latest post-G61 request readiness-refresh: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests.
- LIMA latest quickstart artifact refresh: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- LIMA latest handoff freshness supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests.
- LIMA latest current-goal evidence refresh: passed, 16 focused status tests, 56 broader V1 readiness/status tests, and 5435 full-suite tests.
- LIMA latest consumer checkpoint freshness refresh: passed, 16 focused consumer/current-goal tests, 56 broader V1 readiness/status tests, and 5435 full-suite tests.

Traceability artifacts: `V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`, `V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`, `V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`, `V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`, `V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md`, `V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`, `V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`, `V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`, and `V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`.

## Current Required Unblock

Record exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`. If the recorded choice is `Approve-V1-RC-Cutover`, revalidate current checklist, reconciliation, consumer checkpoint freshness, and LIMA test evidence before executing the cutover runbook.

The current cutover authorization packet status audit is `docs/audits/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET_STATUS_AUDIT.md`. It records valid cutover operator choice count `0`; it must show exactly one valid cutover choice before any release-candidate branch, tag, cutover, or readiness claim.

The current goal status audit is `docs/audits/V1_CURRENT_GOAL_STATUS_AUDIT.md`. It records `GOAL_NOT_COMPLETE_CUTOVER_OPERATOR_DECISION_REQUIRED` and must remain aligned with the branch index before any release-candidate branch, tag, cutover, or readiness claim.

Recorded V1-G61 choice: `Approve-V1-G61`. The bounded runtime vendor SDK import execution proof is closed as local test-scoped evidence only. Valid cutover choices are `Approve-V1-RC-Cutover`, `Revise-V1-RC-Cutover`, or `Pause`; none is recorded yet.

Additional blocked gates:

- Release-candidate checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`, current verdict `CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED` for first-consumer harness testing only.
- Release cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`, current verdict `CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION`.
- Final readiness reconciliation audit: `docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md`, current verdict `PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`; it does not authorize branch, tag, cutover, or V1.0.0 completion.
- Final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`, future audit scaffolding only; not executed or passed by this index.
- Arc-Bot-shell clean-checkpoint proof: `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md`, clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`.
- Arc-Bot-shell historical drift exclusion evidence remains compatibility-only context; clean-checkpoint proof is the current release-gate input.
- Arc-Bot-shell clean checkpoint: clean checkpoint proof recorded at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`; current Arc smoke remains compatibility evidence and release authority remains blocked.

## Post-Unblock Sequence

After exactly one cutover operator choice is recorded:

1. If the choice is `Pause`, stop branch/tag/cutover work and preserve candidate-only evidence.
2. If the choice is `Revise-V1-RC-Cutover`, update the cutover packet and rerun affected readiness evidence before reconsidering.
3. If the choice is `Approve-V1-RC-Cutover`, rerun public Sparkbot, accessible Sparkbot, Sparkbot_shell, and Arc-Bot-shell checkpoint checks.
4. Re-run LIMA `python -m compileall lima`, the focused V1 readiness/status tests, the full `python -m pytest -q tests -p no:cacheprovider` suite, and `git diff --check`.
5. Confirm `docs/audits/V1_CURRENT_GOAL_STATUS_AUDIT.md` and `docs/audits/V1_CONSUMER_CHECKPOINT_FRESHNESS_AUDIT.md` remain current for the exact LIMA and consumer commits under audit.
6. Execute `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md` only after approval and validation freshness are confirmed.
7. Record release-candidate branch and tag identifiers in a future cutover audit before any V1.0.0 readiness claim.
8. Do not treat Arc smoke or clean-checkpoint proof as release authority without the recorded cutover approval and completed runbook.

## Boundaries Preserved

- Additional V1-G61 implementation approval recorded by this index: no.
- V1-G61 runtime vendor SDK import execution proof implemented by this index: no; bounded proof is recorded separately.
- Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot`: yes.
- Public Sparkbot branch merge to main claimed by this index: no.
- Release-candidate branch or tag authority created by this index: no.
- Release-candidate acceptance checklist passed by this index: no.
- Release-candidate cutover authorized by this index: no.
- Final readiness audit executed or passed by this index: no.
- Arc-Bot-shell clean-checkpoint proof claimed by this index: no.
- `lima/` runtime files changed by this index: no.
- LIMA public API exports changed by this index: no.
- Consumer repositories changed by this index: no.
- Runtime vendor SDK imports added to `lima/`: no.
- Provider SDK clients added: no.
- Lockfile edits added: no.
- LIMA-owned provider endpoint resolution added: no.
- LIMA-owned DNS/HTTP/socket/network calls added: no.
- Direct provider egress by LIMA added: no.
- Secret lookup or credential value access added: no.
- Provider token or API key access added: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Connector, browser, file, device, robotics, or physical-world behavior added: no.
- Consumer production runtime integration added: no.
- V1.0 completion, product readiness, or production readiness claimed: no.

## Stop Conditions

Stop before any next step that would:

- add more V1-G61 implementation without exact approval
- treat this index as additional G61 implementation approval
- treat this index as release-candidate branch or tag authority
- treat this index as a passed release-candidate checklist, release cutover, or final readiness audit
- treat Arc-Bot-shell local candidate smoke evidence as a substitute for the recorded clean-checkpoint proof
- edit consumer repositories from this index lane
- add runtime behavior, public API exports, provider SDK clients, runtime vendor SDK imports in `lima/`, lockfile edits, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness
