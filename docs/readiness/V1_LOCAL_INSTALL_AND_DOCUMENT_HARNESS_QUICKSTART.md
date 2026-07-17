# V1 Local Install And Document Harness Quickstart

Status: `CANDIDATE_ONLY`

This quickstart is for local PC testing of the LIMA candidate package and the
read-only document harness. It does not create a release-candidate branch, tag,
cutover, product readiness, production readiness, provider runtime, connector
runtime, or consumer production integration.

## Local Install

From PowerShell:

```powershell
Set-Location C:\Users\limap\LIMA-AI-OS
.\scripts\install_lima_ai_os_candidate.ps1
```

Default behavior installs the local package into:

```text
%USERPROFILE%\.lima-ai-os\candidate\.venv
```

The default install uses `pip install -e . --no-deps` so the local document
harness can run without downloading provider SDK dependencies. Add
`-InstallDependencies` only when dependency download is intended.

## Downloader

For a fresh source download from GitHub:

```powershell
Set-Location C:\Users\limap
.\LIMA-AI-OS\scripts\download_lima_ai_os_candidate.ps1 -Install
```

Use `-DryRun` first to inspect the planned URL and destination without network
or filesystem writes.

## Document Harness Test

After install, run:

```powershell
%USERPROFILE%\.lima-ai-os\candidate\.venv\Scripts\python.exe -m lima.harness.v1_local_document_harness --path C:\path\to\sample.txt
```

Supported local test formats:

- `.txt`
- `.md`
- `.csv`
- `.json`
- `.log`
- `.xml`
- `.html`
- `.docx`
- `.pdf` metadata only

The harness requires a V1 GuardianDecision preflight internally, reads only the
operator-supplied local file, returns bounded metadata and a short preview, and
keeps writes, deletes, mutation, provider calls, network calls, connector calls,
audit persistence, product readiness, and production readiness false.

Use synthetic or non-sensitive local documents only. The preview is returned to
stdout/JSON for operator inspection and must not be treated as approved handling
for customer, HR, finance, legal, medical, regulated, or production data.

## Validation

Focused validation:

```powershell
Set-Location C:\Users\limap\LIMA-AI-OS
python -m pytest -q tests\test_v1_local_document_harness.py -p no:cacheprovider
python -m compileall lima
git diff --check
```

## Boundaries

- Runtime file mutation: not added.
- Provider/model execution: not added.
- Network/provider SDK call: not added.
- Connector/browser/device/robotics behavior: not added.
- External message send: not added.
- Production install claim: not added.
- V1.0.0 cutover claim: not added.
