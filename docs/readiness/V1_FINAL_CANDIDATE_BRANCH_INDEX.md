# V1 Final Candidate Branch Index

Date: 2026-06-21
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before index refresh: `37626bf236bf96c8a57a3ca351668e90eeb0e651`
API status: `CANDIDATE_ONLY`

This index records the current saved branch map for the V1 candidate after the G61 request-stage refresh. It is docs/tests/fixtures-only readiness evidence for operator handoff and self-audit traceability.

This index does not approve V1-G61 implementation, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK clients, add runtime vendor SDK imports in `lima/`, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, invoke connectors, wire consumer production runtime behavior, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

This index is not release-candidate branch or tag authority. It records saved candidate lanes and the future cutover sequence only; it does not authorize a branch, tag, release cutover, final-readiness pass, or Arc-Bot-shell clean-checkpoint claim.

## Index Verdict

Verdict: `CANDIDATE_INDEX_READY_WITH_G61_OPERATOR_BLOCKER`

The V1 candidate evidence is saved across LIMA, public Sparkbot, the accessible Sparkbot checkpoint, and Arc-Bot-shell. Public Sparkbot G56 publication is resolved. V1-G57 through V1-G60 are completed candidate-only evidence. The current gate consistency audit rejects stale public Sparkbot publication and V1-G57 active-blocker language. The candidate is still not a final-readiness pass because V1-G61 has no recorded operator decision, the release-candidate checklist is not passed, cutover is not authorized, and Arc-Bot-shell clean-checkpoint proof is not recorded.

## Current LIMA Branch Checkpoints

| Branch or lane | Commit or label | Purpose |
| --- | --- | --- |
| `docs-v1-post-g60-readiness-and-next-lane-matrix` | `37626bf236bf96c8a57a3ca351668e90eeb0e651` | Current observed workspace branch for the G61 request-stage readiness refresh. |
| `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request` | request-stage lane label | Prepares the G61 runtime vendor SDK import execution proof approval request. |
| `audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request` | audit lane label | Independently audits the G61 request gate. |
| `audit-v1-g61-preapproval-runtime-tree-guard` | guard audit label | Records the preapproval runtime-tree guard that fails if LIMA runtime imports the vendor SDK or constructs provider clients before exact approval. |
| `docs-v1-post-g61-request-readiness-refresh` | readiness lane label | Refreshes status after the G61 request-gate audit. |
| `audit-v1-g61-operator-decision-packet-status` | status audit lane label | Records that the G61 operator decision packet is present, awaiting exactly one valid choice, and not an implementation approval. |
| `docs-v1-candidate-harness-quickstart-execution-audit` | quickstart audit lane label | Records local public Sparkbot, accessible Sparkbot, and Arc-Bot-shell quickstart execution proof while preserving the G61 operator blocker. |
| `audit-v1-current-gate-consistency` | consistency audit lane label | Locks current-facing status, release, and handoff artifacts to the active G61 operator-decision gate. |
| `audit-v1-post-validation-readiness-change-freshness` | freshness audit lane label | Locks same-turn readiness edits after the validation refresh to release/cutover freshness checks and a 5359-test full LIMA suite pass without creating release authority. |
| `audit-v1-arc-bot-shell-local-drift-exclusion` | Arc drift audit lane label | Records current Arc-Bot-shell local drift as compatibility-only evidence, currently 7 tracked modified files and 64 untracked files excluded from V1 release-candidate/final-readiness proof, with approved G56 smoke proof paths rechecked clean. |
| `docs-v1-release-candidate-acceptance-checklist` | checklist lane label | Defines the future V1.0.0 acceptance bar; currently `NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS`. |
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
| Arc-Bot-shell checkpoint | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0` | checkpoint commit tracks origin; unrelated local worktree drift is excluded from V1 proof; same-day approved G56 smoke proof paths rechecked clean |

## Current Validation Evidence

- Consumer quickstart smoke refresh: passed, public Sparkbot 8 tests, accessible Sparkbot 8 tests, and Arc-Bot-shell 8 tests.
- Arc-Bot-shell approved G56 smoke proof-path recheck: passed; approved proof paths remain clean while unrelated local drift remains excluded from V1 release-candidate/final-readiness proof.
- LIMA post-validation readiness freshness full suite: passed, same-turn evidence 5359 tests after release/cutover freshness checks.
- LIMA quickstart post-refresh validation: passed, 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests.
- LIMA latest final blocker/index readiness refresh: passed, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests.
- LIMA latest post-G61 request readiness-refresh: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests.
- LIMA latest quickstart artifact refresh: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- LIMA latest handoff freshness supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests.

## Current Required Unblock

Record exactly one V1-G61 operator choice in `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`.

The current G61 decision packet status audit is `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`. It must remain current and consistent with the recorded decision state before any implementation, final readiness audit, release-candidate branch, or tag action.

The current G61 preapproval runtime-tree guard audit is `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`. It must remain current and passing before any G61 implementation, final readiness audit, release-candidate branch, or tag action.

Valid V1-G61 choices are:

- `Approve-V1-G61`
- `Revise-V1-G61`
- `Pause`

If the recorded choice is `Approve-V1-G61`, implement only the runtime vendor SDK import execution proof scope in `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`.

If the recorded choice is `Revise-V1-G61` or `Pause`, do not implement G61. Refresh the final audit outcome around the recorded decision.

Additional blocked gates:

- Release-candidate checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`, current verdict `NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS`.
- Release cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`, current verdict `CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS`.
- Final readiness audit: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`, future audit scaffolding only; not executed or passed by this index.
- Arc-Bot-shell local drift exclusion audit: `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`, current 7 tracked modified files and 64 untracked files excluded from V1 release-candidate/final-readiness proof.
- Arc-Bot-shell approved G56 smoke proof-path recheck: passed same-day; current Arc evidence remains compatibility-only while unrelated local drift is excluded.
- Arc-Bot-shell clean checkpoint: not recorded; current Arc evidence is compatibility smoke only while unrelated local drift remains excluded from V1 proof.

## Post-Unblock Sequence

After the required G61 decision is resolved:

1. Re-run the public Sparkbot G56 fake-executor provider SDK/network egress smoke and `git diff --check`.
2. Re-run the accessible Sparkbot G56 fake-executor smoke and `git diff --check`.
3. Re-run the Arc-Bot-shell G56 fake-executor smoke and `git diff --check`.
4. Refresh `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md` with the rerun evidence.
5. Re-run or refresh `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md` so current-facing docs still reject stale G56/G57 blocker language.
6. Re-run or refresh `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md` if any readiness doc, fixture, or static test changes after the current validation refresh.
7. Refresh `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md` so it matches the recorded decision state.
8. Re-run or refresh `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md` before any implementation, final readiness audit, release-candidate branch, or tag action.
9. Re-run LIMA `python -m compileall lima`, the full `python -m pytest -q tests -p no:cacheprovider` suite, and `git diff --check`.
10. Refresh `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md` with the latest focused/full validation evidence.
11. Refresh final blocker/register and branch-index freshness evidence after any later readiness edits so the latest supplement remains at least as current as the release/cutover handoff docs.
12. If G61 is approved, include the focused G61 implementation test and closeout evidence.
13. Refresh `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md` if Arc-Bot-shell local drift changes before final-readiness evaluation.
14. Record Arc-Bot-shell clean-checkpoint proof after local drift is absent or resolved and revalidated before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim.
15. Run the final readiness audit on a separate branch using `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`.
16. If the release-candidate acceptance checklist, final readiness audit, and clean Arc-Bot-shell checkpoint proof pass, use `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md` before any branch, tag, cutover, or readiness action.

## Boundaries Preserved

- V1-G61 implementation approval recorded by this index: no.
- V1-G61 runtime vendor SDK import execution proof implemented by this index: no.
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

- implement V1-G61 without exact approval
- treat this index as G61 approval
- treat this index as release-candidate branch or tag authority
- treat this index as a passed release-candidate checklist, release cutover, or final readiness audit
- treat Arc-Bot-shell local candidate smoke evidence as clean-checkpoint proof while local drift remains excluded
- edit consumer repositories from this index lane
- add runtime behavior, public API exports, provider SDK clients, runtime vendor SDK imports in `lima/`, lockfile edits, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness
