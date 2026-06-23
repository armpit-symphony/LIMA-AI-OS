# V1 Product Readiness Target

This document records the current V1 product target for LIMA-AI-OS.

It is product-direction and readiness evidence only. It does not approve runtime implementation, shell wiring, provider calls, model routing, provider SDK/network egress, GuardianDecision execution authority, approval enforcement expansion, persistence expansion, adapter calls, file mutation, browser/network activity, robotics, or physical-world behavior in the current branch.

## V1 Objective

LIMA-AI-OS V1 should become a usable Guardian-gated runtime for the first shell consumers:

- `Sparkbot_shell`
- public `Sparkbot`
- `Arc-Bot-shell`

Sparkbot remains the R&D reference for how shells should behave. LIMA should use Sparkbot as reference evidence and extract compatible contracts deliberately. LIMA must not copy Sparkbot code, import Sparkbot runtime modules, wire Sparkbot routes, or mutate consumer repositories unless a future implementation approval explicitly names that scope.

## Current Gate

LIMA remains `CANDIDATE_ONLY`.

The current V1 completed implementation evidence is refreshed through `V1-G60`. Request-stage readiness is refreshed through the post-G61 request readiness refresh. The V1-G61 runtime vendor SDK import execution proof approval request is prepared as the next narrow request-only authority gate.

`V1-G60` is complete as approved dependency declaration and vendor provider SDK import-boundary evidence. It adds `openai>=1.0.0,<3.0.0` to `pyproject.toml` only. It remains `CANDIDATE_ONLY`.

Authoritative completed provider SDK/network and dependency evidence files:

- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_APPROVAL_REQUEST.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_WORK_ORDER.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_PREFLIGHT_AUDIT.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_CLOSEOUT.md`
- `docs/audits/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_AUDIT.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G56_AUDIT.md`
- `docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE.md`
- `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md`
- `docs/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT.md`
- `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md`
- `docs/audits/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G60.md`
- `docs/readiness/V1_POST_G60_NEXT_LANE_DECISION_MATRIX.md`
- `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`
- `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`
- `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`
- `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`
- `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`
- `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`
- `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`
- `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`
- `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`

Observed workspace branch for this refresh:

- `docs-v1-post-g60-readiness-and-next-lane-matrix`

The current request-only approval lane label is:

- `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`

Authoritative G61 request files:

- `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md`
- `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_WORK_ORDER.md`
- `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_PREFLIGHT_AUDIT.md`
- `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md`
- `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`
- `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`
- `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`
- `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`

Valid G61 operator choices are `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`.

No V1-G61 implementation is approved by this document.

## Accepted Evidence Through G60 And G61 Request Stage

The V1 evidence chain now includes:

- first-shell proof intake for `Sparkbot_shell`, public `Sparkbot`, and `Arc-Bot-shell`
- typed request and GuardianDecision preflight metadata
- local redacted audit/evidence persistence
- destructive approval enforcement metadata
- guarded file mutation policy and preview evidence
- consumer import, patch preview, repository edit, and import-smoke evidence
- shell wiring and consumer integration evidence
- provider/model dispatch, live-call authority, live-call execution metadata, and fake-executor smoke evidence
- provider credential/network hardening metadata
- real provider executor design, invocation metadata, and executable caller-injected wrapper metadata
- provider SDK/network/credential authority metadata
- fake SDK/fake-egress harness evidence
- bounded caller-injected real provider SDK/network egress wrapper evidence
- V1-G56 consumer fake-executor provider SDK/network egress smoke evidence for Sparkbot and Arc-Bot-shell
- V1-G57 provider execution hardening authorization metadata
- built-in provider SDK client authority contract metadata
- SDK dependency and vendor provider SDK import authority metadata
- approved dependency declaration and vendor provider SDK import-boundary evidence
- runtime authority-chain audit through G56
- readiness rollup through G60
- post-G60 next-lane decision matrix
- V1-G61 request-gate audit
- V1-G61 preapproval runtime-tree guard audit
- V1-G61 operator decision packet status audit proving the packet is still awaiting one exact valid choice
- post-G61 request readiness refresh
- V1 candidate harness quickstart with current verdict `QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER`
- V1 candidate harness quickstart execution audit with current verdict `PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER`
- V1 candidate harness quickstart post-refresh validation with public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 tests, plus LIMA focused quickstart/handoff 17 tests, broader V1 harness/readiness 108 tests, and full LIMA suite 5360 tests
- V1 consumer harness usability matrix for Sparkbot and Arc-Bot-shell local candidate smoke criteria
- V1 release-candidate acceptance checklist with current verdict `NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS`
- V1 release-candidate cutover runbook with current verdict `CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS`
- V1 current gate consistency audit proving the active gate is G61, not stale G56/G57 language
- V1 current candidate validation refresh with 153 focused current-gate/release-readiness tests and 5350 full LIMA suite tests passing
- V1 current candidate validation refresh latest LIMA readiness freshness supplement with 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests passing
- V1 current candidate validation refresh latest handoff freshness supplement with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests passing
- V1 post-validation readiness-change freshness audit proving same-turn readiness edits after the validation refresh are covered by release/cutover freshness checks, a 5359-test full LIMA suite pass, latest quickstart post-refresh 5360-test full LIMA suite evidence, and latest final blocker/index refresh evidence passing 15 focused final blocker/index tests, 89 broader affected readiness tests, and 5361 full-suite tests
- V1 latest post-G61 request readiness-refresh evidence passing 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and the 5362-test full LIMA suite
- V1 latest quickstart artifact refresh evidence passing 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and the 5364-test full LIMA suite
- V1 Arc-Bot-shell local drift exclusion audit proving current Arc local drift, currently 7 tracked modified files and 64 untracked files, is compatibility-only evidence and excluded from V1 release-candidate/final-readiness proof, with same-day recheck evidence that approved G56 smoke proof paths remain clean
- V1 final readiness audit template for the future post-G61 release-candidate audit, not a current release approval
- V1 operator unblock action packet for recording exactly one G61 operator decision, not implementation approval
- V1 final candidate branch index for saved checkpoint and future branch/tag guard traceability
- Arc-Bot-shell clean-checkpoint gate requiring clean checkpoint proof before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim
- V1 consumer target state after Arc readiness integration, including
  Arc-Bot-shell runtime gating readiness integration evidence
- public Sparkbot G56 publication resolution audit evidence

This evidence is still candidate-only. It does not prove V1 product readiness, production readiness, live customer use, consumer production runtime integration, runtime vendor SDK import execution, built-in provider SDK clients, direct provider egress by LIMA, secret access, credential value access, fallback, connector authority, or physical-world authority.

## Operator Approval Rule

Deleting or editing anything must require operator approval in LIMA-AI-OS and in first shell consumers.

This applies at minimum to:

- deleting files, records, memories, messages, tasks, events, customer data, or shell-owned state
- editing or mutating files, records, memories, messages, tasks, events, customer data, or shell-owned state
- overwriting existing content
- destructive admin or connector actions

Read-only inspection, preview, explanation, draft generation, and blocked/deferred states may remain lower risk when they do not mutate state, reveal secrets, execute external actions, or bypass shell/Guardian policy.

## Haptics Ownership

Haptics are acceptable as a V1 shell experience requirement, but ownership remains split:

- shells own haptic rendering, tactile behavior, animation, and device-specific feedback
- LIMA may define future haptic intent metadata for shell contracts
- LIMA does not own device haptic implementation
- no haptic implementation is added by this document

## First-Shell Readiness Requirements

For V1, LIMA must prove compatibility with the first shells before product readiness can be claimed:

- `Sparkbot_shell` UX-state proof, including real source-backed `thinking` / streaming or progress state
- public `Sparkbot` behavior-reference alignment for approvals, Guardian posture, provider/model routing, and shell response states
- `Arc-Bot-shell` task-oriented approval, audit/evidence, connector, and office-work boundary proof
- no raw natural-language-to-tool execution shortcut
- provider/model routing constrained by Guardian and shell tool-pack scope
- destructive edit/delete operations requiring operator approval
- audit/evidence lineage for consequential actions
- local consumer harness usability criteria that keep Sparkbot and Arc-Bot-shell smoke tests bounded to fake in-process executors, sanitized fixtures, no-network behavior, no-secret access, and no production wiring
- consumer import/call smoke evidence remains fake-runtime or bounded by explicit approvals until a later gate authorizes more

## Current Status

Current status remains not V1 product-ready.

The latest completed gate is `V1-G60`. The active next lane is operator decision on the prepared request-only `V1-G61` runtime vendor SDK import execution proof packet. The operator decision packet status audit proves that no V1-G61 choice is recorded yet. No V1-G61 implementation is approved. The V1.0.0 release-candidate acceptance checklist is not satisfied and the release-candidate cutover runbook remains blocked while the G61 operator decision blocker remains active. The operator unblock action packet and final candidate branch index are handoff and traceability evidence only. The current gate consistency audit, current candidate validation refresh including latest LIMA readiness freshness supplement 15/89/5361 evidence and latest handoff freshness supplement 8/117/5362 plus 7/64/133/5364 evidence, post-validation readiness-change freshness audit including latest final blocker/index 15/89/5361 evidence, latest post-G61 request readiness-refresh 8/117/5362 evidence, and latest quickstart artifact refresh 7/64/133/5364 evidence, current quickstart post-refresh evidence, current Arc drift exclusion audit, and clean Arc-Bot-shell checkpoint proof are required inputs to any future final readiness audit, but they do not approve implementation, release, production use, or consumer production integration.

Until `Approve-V1-G61` is explicitly recorded, the following remain blocked:

- V1-G61 runtime vendor SDK import execution proof implementation
- consumer repository edits for V1-G61
- lockfile edits
- runtime vendor SDK imports in `lima/`
- built-in provider SDK clients
- direct provider SDK implementation
- provider endpoint resolution by LIMA
- LIMA-owned DNS, HTTP, socket, network calls, or direct provider egress
- secret lookup, credential value access, provider token access, or API key access
- provider configuration changes
- fallback execution
- consumer production runtime integration
- connector, browser, network, file, device, robotics, or physical-world behavior
- V1 product readiness or production readiness claims

## Remaining Blockers

- V1-G61 operator approval is not recorded
- runtime vendor SDK import execution proof is not implemented
- lockfile edits remain unapproved
- runtime vendor SDK imports in `lima/` remain unapproved
- direct provider SDK/network egress by LIMA is still forbidden
- real provider SDK client ownership remains outside LIMA
- provider secrets and credential values remain inaccessible to LIMA
- fallback execution remains unapproved
- consumer production runtime integration remains unapproved
- live runtime parity across first shells is not proven as product readiness
- clean Arc-Bot-shell checkpoint proof is not recorded for release-candidate, final-readiness, branch, tag, cutover, or readiness claims
- release boundary remains not passed
- V1 product readiness is not approved
- production behavior is not approved

## Recommended Next Step

Record exactly one operator choice for the prepared V1-G61 runtime vendor SDK import execution proof approval request.

The request asks only whether LIMA may later prove the approved vendor SDK module can be imported in a controlled local test context. Stop before implementation unless `Approve-V1-G61` is recorded. Stop before lockfile edits, runtime imports in `lima/`, credentials, built-in SDK clients, client construction, LIMA-owned endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, physical-world behavior, or product-readiness claims.
