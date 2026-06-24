# V1 Consumer Checkpoint Manifest

Date: 2026-06-22
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Source LIMA commit before manifest: `37626bf236bf96c8a57a3ca351668e90eeb0e651`
LIMA commit under audit: `c0a758a6aae802669f2d023f83206d7f1efd236c`
API status: `CANDIDATE_ONLY`

This manifest records the consumer repository checkpoints that can feed a future V1 final readiness audit for Sparkbot and Arc-Bot-shell harness use.

It is docs/tests/fixtures-only readiness evidence. It does not execute the final readiness audit, pass the release-candidate checklist, authorize cutover, authorize branch or tag actions, modify consumer repositories, modify `lima/`, add runtime vendor SDK imports in `lima/`, add provider SDK clients, edit dependency manifests or lockfiles, make LIMA-owned DNS/HTTP/socket/network calls, access secrets, call providers, execute fallback, wire consumer production runtime behavior, invoke connectors, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Manifest Verdict

Verdict: `CONSUMER_CHECKPOINTS_PARTIAL_ARC_DIRTY`

Public Sparkbot, accessible Sparkbot, and Sparkbot_shell are currently clean local checkpoints. Arc-Bot-shell is not clean locally and is therefore not clean-checkpoint proof. The Arc-Bot-shell checkpoint can remain compatibility-only evidence until its local worktree is committed to an intentional readiness branch or cleaned and revalidated.

## Consumer Checkpoints

| Consumer | Repository | Local path | Branch | Commit | Local status | Release proof use |
| --- | --- | --- | --- | --- | --- | --- |
| Public Sparkbot | `sparkpit-labs/Sparkbot` | `C:\Users\limap\Sparkbot-public` | `v1-g56-runtime-authority-chain-audit` | `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | clean | candidate smoke checkpoint only |
| Accessible Sparkbot | `armpit-symphony/Sparkbot` | `C:\Users\limap\Sparkbot` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ddaa4ccaacd328ddcc1f00a040c2c140abee428e` | clean | candidate smoke checkpoint only |
| Sparkbot shell | `armpit-symphony/Sparkbot_shell` | `C:\Users\limap\Sparkbot_shell` | `sparkbot-shell-work-settings-runtime-preview` | `548b6d6aa6cde98b261e867c0c2db86ddbfa83dc` | clean | shell checkpoint only |
| Arc-Bot-shell | `armpit-symphony/Arc-Bot-shell` | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0` | dirty: 7 tracked modified files and 64 untracked files | compatibility-only; not clean-checkpoint proof |

## Required Consumer Smoke Commands

Public Sparkbot:

```powershell
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

Accessible Sparkbot:

```powershell
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

Arc-Bot-shell:

```powershell
python -m pytest -q tests\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
git status --porcelain --untracked-files=all
```

Sparkbot_shell:

```powershell
git status --short --branch
git diff --check
```

## Final Readiness Inputs

A future final readiness audit may cite this manifest only if it also records:

- exact LIMA-AI-OS commit under audit
- exact consumer repository commits under audit
- consumer smoke command outputs
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- Arc-Bot-shell clean-checkpoint proof, if Arc evidence is used for release-candidate, final-readiness, branch, tag, cutover, or readiness claims

## Boundaries Preserved

- Final readiness audit executed by this manifest: false.
- V1 release-candidate checklist passed by this manifest: false.
- V1 release-candidate cutover authorized by this manifest: false.
- V1.0.0 branch or tag authorized by this manifest: false.
- Arc-Bot-shell clean-checkpoint proof claimed by this manifest: false.
- Consumer repositories changed by this manifest: false.
- `lima/` runtime files changed by this manifest: false.
- Runtime vendor SDK imports added to `lima/`: false.
- Provider SDK clients added: false.
- Lockfile edits added: false.
- LIMA-owned provider endpoint resolution added: false.
- LIMA-owned DNS/HTTP/socket/network calls added: false.
- Secret lookup or credential value access added: false.
- Provider token or API key access added: false.
- Fallback execution added: false.
- Connector/browser/file/device/robotics/physical-world behavior added: false.
- Consumer production runtime integration approved: false.
- V1.0 completion, product readiness, or production readiness claimed: false.

## Next Action

Commit the LIMA readiness evidence, then record the resulting LIMA commit SHA in the future final readiness audit. Do not create a V1.0.0 release-candidate branch, tag, cutover, or readiness claim until Arc-Bot-shell clean-checkpoint proof and the final readiness audit both pass.
