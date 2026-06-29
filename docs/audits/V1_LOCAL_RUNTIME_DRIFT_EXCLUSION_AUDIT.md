# V1 Local Runtime Drift Exclusion Audit

Date: 2026-06-28
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Observed LIMA commit: `f554a2f048c6231a2b321390e1a309101bee02c9`
API status: `CANDIDATE_ONLY`

Audit verdict: `LOCAL_RUNTIME_DRIFT_EXCLUDED_FROM_V1_RELEASE_PROOF`

This audit records untracked local LIMA-AI-OS workspace artifacts discovered after the current-goal and consumer checkpoint freshness refresh. It is docs/tests/fixtures-only evidence. It does not approve, stage, commit, run, install, download, package, publish, or release those local artifacts.

The observed artifacts are excluded from V1 release-candidate proof because they are untracked local runtime/install behavior under the current workspace and are not covered by a recorded operator approval, committed tests, release checklist acceptance, or cutover authorization.

## Observed Local Drift

| Path | Git state | Observed role | Release-proof treatment |
| --- | --- | --- | --- |
| `docs/readiness/V1_LOCAL_INSTALL_AND_DOCUMENT_HARNESS_QUICKSTART.md` | untracked | local install/document-harness quickstart | excluded |
| `lima/harness/v1_local_document_harness.py` | untracked | candidate local document inspection runtime/CLI | excluded |
| `scripts/download_lima_ai_os_candidate.ps1` | untracked | GitHub source archive downloader with optional installer execution | excluded |
| `scripts/install_lima_ai_os_candidate.ps1` | untracked | local venv/package installer with optional dependency install and focused test run | excluded |
| `tests/test_v1_local_document_harness.py` | untracked | local document harness tests | excluded |

`git ls-files --others --exclude-standard lima/harness/v1_local_document_harness.py` reported `lima/harness/v1_local_document_harness.py`, and `git ls-files lima/harness/v1_local_document_harness.py` returned no tracked path. The local harness file size was observed as 11,113 bytes. `python -m py_compile lima/harness/v1_local_document_harness.py` passed, but syntax validity is not release authority.

## Risk Findings

- The local document harness reads operator-supplied local files and returns bounded preview metadata. Even though it declares Guardian-gated and read-only behavior, it is runtime behavior under `lima/` and is not part of the committed V1 evidence chain.
- The downloader script can perform a network call using `Invoke-WebRequest` and write/expand an archive unless `-DryRun` is used.
- The installer script can create a virtual environment, run `pip install -e`, import the local document harness, and run a focused test command.
- The quickstart references `tests/test_v1_local_document_harness.py`; that test file is present locally but is also untracked and excluded from release proof.
- These artifacts make the local worktree dirty and must not be treated as clean-checkpoint or release-candidate evidence.

## Boundary Decision

The artifacts are not approved for V1 release-candidate proof. They may be considered only in a future explicitly approved lane that defines file scope, behavior scope, tests, rollback plan, stop conditions, and Guardian/read-only constraints.

Until such approval exists, do not:

- stage or commit the untracked runtime/install artifacts as part of the current cutover-readiness lane
- treat them as V1.0.0 readiness evidence
- run the downloader or installer as release validation
- claim local document harness support in V1 release-candidate readiness
- use their presence to satisfy Sparkbot, Sparkbot_shell, or Arc-Bot-shell harness readiness
- create a release-candidate branch, tag, cutover, product-readiness claim, or production-readiness claim from them

## Current Release Impact

The pushed branch remains synced at `f554a2f048c6231a2b321390e1a309101bee02c9`, but the local worktree is not clean because of untracked runtime/install artifacts. The V1 release-candidate blocker remains unchanged: exactly one valid cutover operator choice must be recorded in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`, and local untracked runtime drift must be resolved or explicitly excluded before any clean local checkpoint claim.

## Boundaries Preserved By This Audit

- Runtime/install artifacts staged by this audit: no.
- Runtime/install artifacts committed by this audit: no.
- Runtime behavior approved by this audit: no.
- Local document harness support claimed by this audit: no.
- Downloader or installer execution approved by this audit: no.
- Network behavior approved by this audit: no.
- File read behavior approved by this audit: no.
- Dependency installation approved by this audit: no.
- Consumer production integration approved by this audit: no.
- Release-candidate branch or tag created by this audit: no.
- Cutover operator choice recorded by this audit: no.
- Product or production readiness claimed by this audit: no.

## Next Required Action

Keep these artifacts out of V1 release proof unless the operator explicitly opens a separate local document harness/install lane. For the current V1 cutover lane, either remove the untracked local artifacts from the workspace or keep them documented as excluded local drift before any clean local checkpoint claim.
