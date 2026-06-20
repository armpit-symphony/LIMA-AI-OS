# V1 Final Candidate Branch Index

Date: 2026-06-20
Branch: `docs-v1-final-candidate-branch-index`
Source LIMA commit before index: `a10a81fb0ff0096911ab3e62d69463b590520055`
API status: `CANDIDATE_ONLY`

This index records the current saved branch map for the V1 candidate after the final readiness audit template checkpoint. It is docs/tests/fixtures-only readiness evidence for operator handoff and self-audit traceability.

This index does not approve V1-G57 implementation, grant repository credentials, push public Sparkbot, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK clients, add SDK dependencies, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, invoke connectors, wire consumer production runtime behavior, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Index Verdict

Verdict: `CANDIDATE_INDEX_READY_WITH_EXTERNAL_UNBLOCKS`

The V1 candidate evidence is saved across LIMA, the accessible Sparkbot checkpoint, and Arc-Bot-shell. The candidate is still not a final readiness pass because the public Sparkbot target branch is not published and V1-G57 has no recorded operator decision.

## Current LIMA Branch Checkpoints

| Branch | Commit | Purpose |
| --- | --- | --- |
| `docs-v1-final-readiness-audit-template` | `a10a81fb0ff0096911ab3e62d69463b590520055` | Defines the future final readiness audit shape after unblocks. |
| `docs-v1-operator-unblock-action-packet` | `8270cb1b01be3798d2b974b85ca14d851e4aedeb` | Records exact operator actions for public Sparkbot publication and G57 decision. |
| `docs-v1-final-blocker-register-after-arc-drift-audit` | `d1b3d5a87739cfbc0a1e54a57951ab8cc975c502` | Records the current real blockers after Arc drift exclusion. |
| `audit-v1-arc-bot-shell-local-drift-exclusion` | `687637829ed652a341f94f0696cf8ba1afb7993c` | Excludes unrelated Arc-Bot-shell local drift from pushed G56 proof. |
| `audit-v1-g56-public-sparkbot-target-publication` | `992c1714eab6d74a0a67de322942e4c9d1adb55e` | Records the public Sparkbot target publication blocker. |

## Consumer Checkpoints

| Repo | Local path | Branch | Commit | Status |
| --- | --- | --- | --- | --- |
| Public Sparkbot target checkout | `C:\Users\limap\Sparkbot-public` | `v1-g56-runtime-authority-chain-audit` | `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2` | clean local branch; push to `sparkpit-labs/Sparkbot` still blocked by write credentials |
| Accessible Sparkbot checkpoint | `C:\Users\limap\Sparkbot` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ddaa4ccaacd328ddcc1f00a040c2c140abee428e` | clean pushed branch |
| Arc-Bot-shell checkpoint | `C:\Users\limap\Arc-Bot-shell` | `v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke` | `ec06e7670f18eeae192fc0f995b6ffd07481d8c9` | pushed G56 branch; unrelated local drift excluded from proof |

## Required External Unblocks

1. Provide or switch to a credential with write permission for `sparkpit-labs/Sparkbot`, then publish `v1-g56-runtime-authority-chain-audit` from `C:\Users\limap\Sparkbot-public`.
2. Record exactly one V1-G57 operator choice in `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md`.
3. If the recorded choice is `Approve-V1-G57`, implement only the metadata-only scope in `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md`.

Valid V1-G57 choices remain:

- `Approve-V1-G57`
- `Revise-V1-G57`
- `Pause`

## Post-Unblock Sequence

After the required external unblocks are complete:

1. Re-run the public Sparkbot G56 fake-executor provider SDK/network egress smoke and `git diff --check`.
2. Re-run the accessible Sparkbot G56 fake-executor smoke and `git diff --check`.
3. Re-run the Arc-Bot-shell G56 fake-executor smoke and ensure local drift is either resolved or still explicitly excluded.
4. Re-run LIMA `python -m compileall lima`, the full `python -m pytest -q tests -p no:cacheprovider` suite, and `git diff --check`.
5. If G57 is approved, include the focused G57 implementation test and closeout evidence.
6. Run the final readiness audit on a separate branch using `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`.

## Boundaries Preserved

- V1-G57 implementation approval recorded by this index: no.
- V1-G57 provider execution hardening authorization implemented by this index: no.
- Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot` by this index: no.
- Public Sparkbot write credential provided by this index: no.
- `lima/` runtime files changed by this index: no.
- LIMA public API exports changed by this index: no.
- Consumer repositories changed by this index: no.
- Arc-Bot-shell dirty files accepted as V1 proof by this index: no.
- Provider SDK clients added: no.
- SDK dependencies added: no.
- Vendor provider SDK imports added: no.
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

- push public Sparkbot without write credentials
- implement V1-G57 without exact approval
- treat this index as G57 approval
- edit consumer repositories from this index lane
- add runtime behavior, public API exports, provider SDK clients, SDK dependencies, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness
