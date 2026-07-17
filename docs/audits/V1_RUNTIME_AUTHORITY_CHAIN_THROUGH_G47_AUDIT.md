# V1 Runtime Authority Chain Through G47 Audit

Date: 2026-06-17
Branch: `audit-v1-runtime-authority-chain-through-g47`
G47 implementation commit: `3b252a4a8c75fbe3278b98a7f260a45e8bdd54a4`
G47 audit commit: `9dab3a2588787579212781fc6d3a10737351fe61`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit reviews the V1 authority chain through V1-G47. It includes V1-G11 through V1-G46 and adds the V1-G47 consumer fake-executor provider/model call smoke evidence for Sparkbot and Arc-Bot-shell.

The audit does not add or approve `lima/` runtime changes, real provider executor invocation, live provider/model calls, built-in provider SDK clients, direct network code, network calls, ambient secret lookup, credential value access, provider readiness checks, fallback execution, Token Guardian live routing, consumer production runtime imports/calls, runtime shell execution, connectors, browser/network/file/device/robotics/physical-world behavior, scheduled tasks, external sends, raw sensitive content persistence, or product readiness.

## Inputs Reviewed

- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_CLOSEOUT.md`
- `docs/audits/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g47_consumer_fake_executor_provider_model_call_smoke.json`
- `tests/test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py`
- Sparkbot `tests/fixtures/sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
- Sparkbot `tests/test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py`
- Arc-Bot-shell `tests/fixtures/arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
- Arc-Bot-shell `tests/test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G46_AUDIT.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md`
- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md`
- `docs/V1_G43_PROVIDER_MODEL_DISPATCH.md`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY.md`

## Chain Findings

- V1-G11 through V1-G46 authority gates remain intact: pass.
- V1-G47 changes no `lima/` runtime files: pass.
- V1-G47 changes only LIMA docs/tests/fixtures plus exact approved Sparkbot and Arc-Bot-shell test/fixture files: pass.
- V1-G47 does not expand `lima.harness.__all__`: pass.
- Prior frozen V1-G22/G45/G46 harness exports remain present: pass.
- V1-G44 authority validation remains intact and is not weakened: pass.
- V1-G46 execution wrapper remains the only bounded LIMA provider/model call execution wrapper: pass.
- V1-G47 consumer tests exercise that wrapper with fake in-process provider executors only: pass.
- V1-G47 consumer tests validate sanitized V1-G44 authority metadata before execution: pass.
- V1-G47 returned evidence remains sanitized and redaction-reference based: pass.
- Sparkbot consumer proof is saved at commit `83918032f52f069d16796865066ea78dfd182d58`: pass.
- Arc-Bot-shell consumer proof is saved at commit `3edf31f2ee3143756db8d9410009cd87e98bba71`: pass.
- Consumer production runtime/source files were not changed: pass.
- Real provider executor invocation was not added: pass.
- Live provider credentials were not used: pass.
- Network calls were not performed: pass.
- Product readiness was not claimed: pass.

## Authority Invariants

- Consumer fake-executor proof cannot become real provider executor authority: pass.
- Consumer fake-executor proof cannot become built-in provider SDK authority: pass.
- Consumer fake-executor proof cannot become provider credential lookup or credential value access authority: pass.
- Consumer fake-executor proof cannot become provider network egress authority: pass.
- Consumer fake-executor proof cannot become fallback execution authority: pass.
- Consumer fake-executor proof cannot become connector/browser/network authority: pass.
- Consumer fake-executor proof cannot become consumer production runtime integration authority: pass.
- Consumer fake-executor proof cannot become runtime shell execution authority: pass.
- Consumer fake-executor proof cannot become file mutation, external send, scheduled task, or physical-world authority: pass.
- Consumer fake-executor proof cannot become product-readiness authority: pass.
- V1-G46 execution authority remains limited to caller-injected provider executor invocation after V1-G44 authority, V1-G46 approval, redaction, audit, and execution-boundary checks: pass.
- Public harness import availability remains candidate-only and does not imply live services, credentials, network, connectors, or production readiness: pass.
- Built-in provider SDK integration, direct provider egress, secret lookup, credential value access, fallback execution, and provider readiness checks remain unapproved: pass.
- Tool, browser/network, connector, device, and physical-world behavior remain blocked unless future exact authority lanes approve them: pass.

## Data Protection Invariants

- Raw prompts are not persisted or emitted in V1-G47 LIMA evidence: pass.
- Raw model responses are not persisted or emitted in V1-G47 LIMA evidence: pass.
- Raw customer data is not persisted or emitted: pass.
- Raw secrets are not persisted or emitted: pass.
- Raw credentials are not persisted or emitted: pass.
- Provider tokens and API keys are not persisted or emitted: pass.
- Raw diff or patch bodies are not persisted in LIMA evidence: pass.
- Raw file contents are not persisted in LIMA evidence: pass.
- Consumer fixtures store redacted refs and expected sanitized evidence only: pass.

## Integration Invariants

- Sparkbot changes are limited to the approved V1-G47 test/fixture pair: pass.
- Arc-Bot-shell changes are limited to the approved V1-G47 test/fixture pair: pass.
- Consumer runtime modules are not imported by the V1-G47 smoke tests: pass.
- Consumer runtime calls are not added: pass.
- Runtime shell wiring execution is not added: pass.
- Adapter symbols are not called by V1-G47: pass.
- Built-in provider SDK clients are not added: pass.
- Direct provider network clients are not added: pass.
- Secret lookup and credential value access are not added: pass.
- Fallback execution is not added: pass.
- Connector/browser/network behavior is not added: pass.
- Product readiness remains unclaimed: pass.

## Full Consumer Suite Self-Audit

Optional full consumer-suite runs were attempted and reproduced an existing suite-order limitation even with `v1_g47` deselected. Older G34 tests import `lima`; older static G38/G39/G41/G42 tests later assert `lima` is absent from `sys.modules`.

The authority chain is not advanced by that optional self-audit. The required V1-G47 focused consumer tests passed, and older consumer tests were not edited because doing so would exceed the approved V1-G47 file scope.

## Residual Gaps

- Real provider executor integration remains unapproved.
- Built-in provider SDK integration remains unapproved.
- Direct provider network egress remains unapproved.
- Secret lookup and credential value access remain unapproved.
- Provider readiness network checks remain unapproved.
- Fallback execution remains unapproved.
- Actual guarded file mutation execution remains unapproved.
- Connector authority remains unapproved.
- Browser/network authority remains unapproved.
- Consumer production runtime call expansion remains approval-gated.
- Physical-world/device/robot/drone/IoT authority remains blocked pending a dedicated safety lane.
- Product readiness remains incomplete.

## Validation Evidence

- Sparkbot `python -B -m pytest -q tests\test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider`: pass, `8 passed`.
- Sparkbot `python -B -m pytest -q tests\test_sparkbot_lima_v1_g42_shell_wiring_implementation.py -p no:cacheprovider`: pass, `9 passed`.
- Arc-Bot-shell `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider`: pass, `8 passed`.
- Arc-Bot-shell `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py -p no:cacheprovider`: pass, `9 passed`.
- LIMA `python -m pytest -q tests\test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py tests\test_v1_g47_consumer_fake_executor_provider_model_call_smoke_approval_request.py tests\test_v1_g46_live_provider_model_call_execution.py tests\test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`: pass, `77 passed`.
- LIMA `python -m compileall lima`: pass.
- LIMA `python -m pytest -q tests -p no:cacheprovider`: pass, `4291 passed`.
- `git diff --check` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell: pass.
- `git diff --cached --check`: pass before chain audit commit.

## Audit Conclusion

The V1 authority chain through G47 preserves the capability-open, authority-gated posture while adding consumer-facing fake-executor proof for Sparkbot and Arc-Bot-shell. V1-G47 proves the public V1-G46 wrapper import/call shape with fake in-process provider executors only and does not approve real provider executors, credentials, network egress, provider SDK clients, fallback, connectors, physical-world behavior, consumer production runtime integration, raw sensitive persistence, or product readiness.

Recommended next safe step: update readiness rollup through G47, then prepare the next exact approval gate. The recommended next lane is provider credential/network hardening as a request-only gate before any real provider SDK, credential, or network work.
