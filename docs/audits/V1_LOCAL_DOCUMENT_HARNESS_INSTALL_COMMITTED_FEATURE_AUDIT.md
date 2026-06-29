# V1 Local Document Harness Install Committed Feature Audit

Date: 2026-06-28
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Observed LIMA commit: `bc63ed3b00055976b1728d80124137d7ce15d871`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS_COMMITTED_LOCAL_DOCUMENT_HARNESS_INSTALL_CANDIDATE_ONLY_CUTOVER_STILL_BLOCKED`

This audit records the current posture of the committed local install and read-only document harness lane added by `bc63ed3b00055976b1728d80124137d7ce15d871`. It is candidate-only evidence for local PC testing. It does not create a release-candidate branch, create a tag, perform cutover, approve production use, approve customer-data processing, invoke providers, invoke connectors, wire consumer production runtime behavior, or claim V1.0.0 completion.

## Committed Artifacts

| Path | Git state | Role | Release-proof treatment |
| --- | --- | --- | --- |
| `docs/readiness/V1_LOCAL_INSTALL_AND_DOCUMENT_HARNESS_QUICKSTART.md` | tracked | local install/document-harness quickstart | candidate-only operator guidance |
| `lima/harness/v1_local_document_harness.py` | tracked | Guardian-gated read-only local document harness and CLI | candidate-only local file intake evidence |
| `scripts/download_lima_ai_os_candidate.ps1` | tracked | GitHub source archive downloader with optional installer execution | explicit operator-run utility; dry-run first |
| `scripts/install_lima_ai_os_candidate.ps1` | tracked | local venv/package installer with optional focused test run | explicit operator-run utility; dry-run first |
| `tests/test_v1_local_document_harness.py` | tracked | harness boundary and CLI tests | committed candidate-only test evidence |

## Guardian And Runtime Boundary Findings

- The harness builds a `ConsequentialActionRequest` with `action_type=FILE_OPERATION`, `risk_class=read_only`, `requested_tool_pack=files`, and explicit metadata setting `execution_allowed`, `side_effects_allowed`, and `approval_token_issued` to `False`.
- The harness calls `review_v1_runtime_request` and accepts only a `GuardianDecision` with status `APPROVED`, `v1_preflight_only=True`, `execution_allowed=False`, `side_effects_allowed=False`, `approval_token_issued=False`, and no `allowed_tool_packs`.
- The harness reads one operator-supplied local file after path resolution, optional `allowed_root` enforcement, extension allow-list checking, and `max_bytes` checking.
- The harness returns bounded metadata and preview text, including `file_read=True`, while keeping file write, delete, mutation, provider routing, provider calls, network action, connector invocation, audit persistence, product readiness, and production readiness false.
- Supported local test formats are `.txt`, `.md`, `.csv`, `.json`, `.log`, `.xml`, `.html`, `.htm`, `.docx`, and PDF metadata-only inspection.

## Installer And Downloader Findings

- `scripts/download_lima_ai_os_candidate.ps1` is network/file-write capable when run without `-DryRun`; it uses `Invoke-WebRequest`, expands the archive, and may invoke the installer when `-Install` is set.
- `scripts/install_lima_ai_os_candidate.ps1` creates a local virtual environment and runs `pip install -e`; it avoids dependency downloads by default with `--no-deps` unless `-InstallDependencies` is set.
- Both scripts are explicit operator-run utilities. This audit does not execute them and does not treat their existence as validation authority.

## Risk Findings

- Local document preview can expose file content in command output. Use synthetic or non-sensitive local test documents only unless a future privacy/data-handling gate explicitly approves broader handling.
- The downloader can make a GitHub network call and write/expand files if run without `-DryRun`; this remains operator intent, not automated validation.
- The installer can write under the install root and optionally install dependencies; this remains operator intent, not release authority.
- The committed lane is a local harness support lane only. It does not change the Sparkbot, Sparkbot_shell, or Arc-Bot-shell consumer checkpoint commits.

## Validation Evidence

| Command | Result |
| --- | --- |
| `python -m pytest -q tests\test_v1_local_document_harness.py tests\test_v1_local_runtime_drift_exclusion_audit.py tests\test_v1_local_document_harness_install_committed_feature_audit.py -p no:cacheprovider` | passed, 20 tests |
| `python -m pytest -q tests\test_v1_current_goal_status_audit.py tests\test_v1_consumer_checkpoint_freshness_audit.py tests\test_v1_readme_status_alignment.py tests\test_v1_current_gate_consistency_audit.py tests\test_v1_final_candidate_branch_index.py tests\test_v1_product_readiness_target.py tests\test_v1_readiness_gap_matrix.py tests\test_v1_local_document_harness.py tests\test_v1_local_runtime_drift_exclusion_audit.py tests\test_v1_local_document_harness_install_committed_feature_audit.py -p no:cacheprovider` | passed, 78 tests |
| `python -m compileall lima` | passed |
| `python -m pytest -q tests -p no:cacheprovider` | passed, 5457 tests |
| `git diff --check` | passed |

This validation confirms the committed harness boundary, the superseded drift-closure audit, and the current goal posture after the post-bc63 local harness/install correction. It does not create cutover authority or product readiness.

## Boundary Confirmation

- Cutover operator choice recorded by this audit: no.
- Release-candidate branch created by this audit: no.
- Release-candidate tag created by this audit: no.
- Release cutover performed by this audit: no.
- V1.0.0 completion claimed by this audit: no.
- Product readiness claimed by this audit: no.
- Production readiness claimed by this audit: no.
- Consumer production integration authorized by this audit: no.
- Provider/model execution added by this audit: no.
- LIMA-owned network egress approved by this audit: no.
- Downloader execution approved by this audit: no.
- Installer execution approved by this audit: no.
- Secret or credential access added by this audit: no.
- Connector, browser, device, robotics, or physical-world behavior added by this audit: no.

## Current Release Impact

The local install/document harness artifacts are now tracked, tested, and documented as candidate-only local PC testing support. The V1.0.0 blocker remains unchanged: record exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`, then rerun current readiness, consumer checkpoint freshness, compile, full-suite, and diff hygiene validation before executing `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`.
