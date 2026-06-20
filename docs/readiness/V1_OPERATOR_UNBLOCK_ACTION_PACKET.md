# V1 Operator Unblock Action Packet

Date: 2026-06-20
Branch: `docs-v1-operator-unblock-action-packet`
Source LIMA commit before packet: `d1b3d5ae02d6d363876eaf6369dbdba6f1cb7f48`
API status: `CANDIDATE_ONLY`

This packet lists the exact operator actions needed to unblock the current V1 candidate toward a final readiness audit.

It is docs/tests/fixtures-only readiness evidence. It does not approve V1-G57 implementation, grant repository credentials, push public Sparkbot, complete V1.0, modify `lima/`, change public API exports, edit consumer repositories, add provider SDK clients, add SDK dependencies, resolve provider endpoints, make LIMA-owned DNS/HTTP/socket/network calls, read secrets, access credential values, call providers, execute fallback, invoke connectors, wire consumer production runtime behavior, execute browser/file/device/robotics/physical-world behavior, or claim product/production readiness.

## Packet Verdict

Verdict: `AWAITING_OPERATOR_UNBLOCK_ACTIONS`

The current candidate is locally testable and self-audited. The remaining unblock actions are external to this packet:

1. Publish or authorize publication of the public Sparkbot G56 branch.
2. Record exactly one V1-G57 operator decision.

## Action 1: Public Sparkbot Publication

Required operator action: provide or switch to a credential with write permission for `sparkpit-labs/Sparkbot`, then retry publication of the saved branch.

Current local public Sparkbot state:

- Local path: `C:\Users\limap\Sparkbot-public`
- Target repository: `sparkpit-labs/Sparkbot`
- Branch: `v1-g56-runtime-authority-chain-audit`
- Commit: `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2`
- Current blocker: GitHub HTTP 403 for current credential
- Current branch pushed to target: no

Validation before retry:

```powershell
python -m pytest -q tests\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
```

Publication command after credentials are available:

```powershell
git -C C:\Users\limap\Sparkbot-public -c safe.directory='C:/Users/limap/Sparkbot-public' push origin v1-g56-runtime-authority-chain-audit
```

Evidence required to close this action:

- branch pushed to `sparkpit-labs/Sparkbot` or authorized PR/compare evidence recorded
- public Sparkbot G56 smoke still passes
- no new secrets, credential values, tokens, raw diffs, or raw file contents persisted in LIMA evidence

## Action 2: V1-G57 Operator Decision

Required operator action: record exactly one V1-G57 operator choice.

Valid choices:

- `Approve-V1-G57`
- `Revise-V1-G57`
- `Pause`

Exact approval text if approving:

```text
Approve-V1-G57

I explicitly approve V1-G57 implementation of the LIMA-side provider execution hardening authorization metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md.
```

Decision packet:

- `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md`

Approval request:

- `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md`

If approved later, the implementation branch must add only:

- `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md`
- `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g57_provider_execution_hardening_authorization.json`
- `tests/test_v1_g57_provider_execution_hardening_authorization.py`

Evidence required to close this action:

- exactly one valid operator choice is recorded
- if `Approve-V1-G57` is recorded, implementation stays inside the approved metadata-only scope
- if `Revise-V1-G57` or `Pause` is recorded, implementation does not begin

## Current Evidence To Preserve

- V1 final blocker register after Arc drift audit: `docs/readiness/V1_FINAL_BLOCKER_REGISTER.md`
- Arc-Bot-shell local drift exclusion audit: `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`
- V1 candidate handoff manifest execution audit: `docs/audits/V1_CANDIDATE_TEST_HANDOFF_MANIFEST_EXECUTION_AUDIT.md`
- V1-G57 request audit: `docs/audits/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_REQUEST_AUDIT.md`
- V1-G57 approval request: `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md`

## Boundaries Preserved

- Public Sparkbot branch pushed by this packet: no.
- Public Sparkbot write credential provided by this packet: no.
- V1-G57 operator decision recorded by this packet: no.
- V1-G57 implementation approval inferred by this packet: no.
- V1-G57 provider execution hardening authorization implemented by this packet: no.
- `lima/` runtime files changed by this packet: no.
- LIMA public API exports changed by this packet: no.
- Consumer repositories changed by this packet: no.
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
- treat this packet as G57 approval
- edit consumer repositories from this packet lane
- add runtime behavior, public API exports, provider SDK clients, SDK dependencies, endpoint resolution, network calls, secret access, credential value access, fallback, connectors, or physical-world behavior
- persist raw prompts, raw model responses, raw customer data, secrets, credential values, provider tokens, API keys, raw diffs, full patches, or raw file contents
- claim V1.0 completion, product readiness, or production readiness

## Next Step After Both Actions

After public Sparkbot publication is proven and the V1-G57 decision is resolved, run the final V1 readiness audit. Until then, keep LIMA in `CANDIDATE_ONLY`.
