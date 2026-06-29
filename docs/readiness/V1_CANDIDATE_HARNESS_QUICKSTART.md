# V1 Candidate Harness Quickstart

Date: 2026-06-21
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before quickstart: `37626bf236bf96c8a57a3ca351668e90eeb0e651`
API status: `CANDIDATE_ONLY`

This quickstart gives operators the shortest safe path to run the current Sparkbot and Arc-Bot-shell V1 candidate smoke checks.

It is docs/tests/fixtures-only readiness evidence. It does not approve V1-G61 implementation, complete V1.0, create a release branch, create a tag, modify `lima/`, change public API exports, edit consumer repositories, add runtime vendor SDK imports in `lima/`, add provider SDK clients, edit lockfiles, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, wire consumer production runtime behavior, invoke connectors, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Quickstart Verdict

Verdict: `QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER`

Use this quickstart only for local candidate smoke validation with fake in-process executors and sanitized fixtures. It is not a production setup guide and not a release-candidate cutover.

## Preconditions

- Use the local checkpoints listed in `docs/readiness/V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md`.
- Keep LIMA at `C:\Users\limap\LIMA-AI-OS`.
- Keep public Sparkbot at `C:\Users\limap\Sparkbot-public`.
- Keep accessible Sparkbot at `C:\Users\limap\Sparkbot`.
- Keep Arc-Bot-shell at `C:\Users\limap\Arc-Bot-shell`.
- Do not edit consumer repositories from this quickstart.
- Do not proceed to G61 implementation unless `Approve-V1-G61` is explicitly recorded.
- Treat `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md` as the current committed proof that `Approve-V1-G61` is recorded for bounded local import-proof evidence only.
- Treat `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md` as the current committed proof that stale blocker or release-candidate claims are rejected.
- Treat `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`, `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`, and `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md` as the current harness-usability and freshness evidence before using this quickstart as handoff proof.
- Treat `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md` as the future final-audit shape only; this quickstart does not execute or pass that audit.
- Treat Arc-Bot-shell smoke as compatibility evidence only unless unrelated local drift is absent and clean-checkpoint proof is recorded before release-candidate, final-readiness, branch, tag, cutover, or readiness claims.

## Run Order

Run from PowerShell. Stop on the first failure.

```powershell
Set-Location C:\Users\limap\Sparkbot-public
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

Expected result: `8 passed`, then diff check passes.

```powershell
Set-Location C:\Users\limap\Sparkbot
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

Expected result: `8 passed`, then diff check passes.

```powershell
Set-Location C:\Users\limap\Arc-Bot-shell
python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

Expected result: `8 passed`, then diff check passes.

```powershell
Set-Location C:\Users\limap\LIMA-AI-OS
python -m compileall lima
python -m pytest -q tests -p no:cacheprovider
git diff --check
git diff --cached --check
```

Expected result: compile passes, full LIMA suite passes, and diff checks pass.

## What A Pass Means

- Public Sparkbot can run the current fake-executor provider SDK/network smoke test against the local LIMA candidate.
- Accessible Sparkbot can run the current fake-executor provider SDK/network smoke test against the local LIMA candidate.
- Arc-Bot-shell can run the current fake-executor provider SDK/network smoke test against the local LIMA candidate.
- LIMA compile, full suite, and diff hygiene still pass.
- The current G61 operator-decision status audit still records the packet as awaiting exactly one valid choice.
- The current gate consistency audit still records G61 as the active gate and rejects release-candidate claims before a final-readiness pass and clean Arc-Bot-shell checkpoint proof.
- The current candidate remains usable for local harness smoke validation only.

## Current Evidence To Preserve

- Consumer smoke freshness: public Sparkbot 8 tests, accessible Sparkbot 8 tests, and Arc-Bot-shell 8 tests.
- LIMA quickstart freshness: 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests.
- Final blocker/index freshness: 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests.
- Latest post-G61 request readiness-refresh: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests.
- Latest quickstart artifact refresh: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.
- These evidence counts keep this quickstart current for local harness handoff only. They do not create G61 implementation, release, cutover, final-readiness, production, or Arc-Bot-shell clean-checkpoint authority.

## What A Pass Does Not Mean

- It does not approve V1-G61.
- It does not prove runtime vendor SDK import execution.
- It does not approve runtime vendor SDK imports in `lima/`.
- It does not execute or pass the future final readiness audit.
- It does not authorize a release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim.
- It does not turn Arc-Bot-shell compatibility smoke into release, final-readiness, branch, tag, cutover, or readiness authority; clean-checkpoint proof is recorded separately as release-gate input evidence.
- It does not approve built-in provider SDK clients, provider client construction, endpoint resolution, network egress, credential access, fallback, connectors, consumer production runtime integration, physical-world behavior, V1.0 completion, product readiness, or production readiness.

## Related Artifacts

- Candidate harness quickstart execution audit: `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`
- Candidate handoff manifest: `docs/readiness/V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md`
- Consumer harness usability matrix: `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`
- Current candidate validation refresh audit: `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`
- Post-validation readiness-change freshness audit: `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`
- Current gate consistency audit: `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`
- G61 operator decision packet status audit: `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`
- Release-candidate acceptance checklist: `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`
- Release-candidate cutover runbook: `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`
- Final readiness audit template: `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`
- Final blocker register: `docs/readiness/V1_FINAL_BLOCKER_REGISTER.md`

## Required False Boundaries

- V1-G61 implementation approval recorded by this quickstart: false.
- V1-G61 runtime vendor SDK import execution proof implemented by this quickstart: false.
- V1.0.0 release-candidate branch or tag created by this quickstart: false.
- V1 release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim authorized by this quickstart: false.
- Future final readiness audit executed by this quickstart: false.
- Arc-Bot-shell clean-checkpoint evidence claimed by this quickstart: false.
- `lima/` runtime files changed by this quickstart: false.
- LIMA public API exports changed by this quickstart: false.
- Consumer repositories changed by this quickstart: false.
- Runtime vendor SDK imports added to `lima/`: false.
- Provider SDK clients added: false.
- Provider client construction added: false.
- Lockfile edits added: false.
- LIMA-owned provider endpoint resolution added: false.
- LIMA-owned DNS/HTTP/socket/network calls added: false.
- Direct provider egress by LIMA added: false.
- Secret lookup or credential value access added: false.
- Provider token or API key access added: false.
- Provider configuration changes added: false.
- Fallback execution added: false.
- Connector/browser/file/device/robotics/physical-world behavior added: false.
- Consumer production runtime integration added: false.
- V1.0 completion, product-readiness, or production-readiness claimed: false.

## Next Action

If every quickstart command passes, the current state-changing step is still explicit `Approve-V1-RC-Cutover` authorization before any branch, tag, cutover, or readiness claim. Do not add more G61 implementation or create release-candidate artifacts from this quickstart.
