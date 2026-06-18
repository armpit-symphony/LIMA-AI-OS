# V1 Runtime Authority Chain Through G52 Audit

Date: 2026-06-18
Branch: `audit-v1-runtime-authority-chain-through-g52`
API status: `CANDIDATE_ONLY`

Audit verdict: `pass_candidate_only_authority_chain_preserved`

This audit reviews the V1 runtime authority chain after V1-G52. V1-G52 adds consumer fake-executor provider invocation smoke evidence for Sparkbot and Arc-Bot-shell against the public V1-G51 wrapper. It does not add new LIMA runtime behavior, expand the public API, edit consumer production runtime/source files, add built-in provider SDK integration, resolve provider endpoints, open direct provider network egress, look up secrets, access credential values, execute fallback, invoke connectors, open browser/network authority, add physical-world authority, or claim product readiness.

## Chain Position

- V1-G43: deterministic fake-provider/no-secret/no-network provider/model dispatch evidence.
- V1-G44: non-executing live provider/model call authority metadata/preflight validator.
- V1-G45: public API export cleanup for approved authority validator symbols.
- V1-G46: bounded live provider/model call execution wrapper with caller-injected provider executor only.
- V1-G47: consumer fake-executor provider/model call smoke evidence.
- V1-G48: provider credential/network hardening metadata, reference-only and deny-by-default.
- V1-G49: non-executing real provider executor authority design metadata.
- V1-G50: non-executing real provider executor invocation envelope metadata.
- V1-G51: bounded caller-injected executable provider executor invocation wrapper.
- V1-G52: consumer fake-executor provider invocation smoke evidence against the V1-G51 public wrapper.

## Preserved Authority Boundary

- API status remains `CANDIDATE_ONLY`.
- G52 changes no files under `lima/`: pass.
- G52 does not expand `lima.harness` exports or any public API surface: pass.
- G52 adds LIMA-side evidence docs/tests/fixtures only: pass.
- G52 Sparkbot edits are limited to the approved consumer test and fixture files: pass.
- G52 Arc-Bot-shell edits are limited to the approved consumer test and fixture files: pass.
- G52 does not edit consumer production runtime/source files: pass.
- G52 proves consumer import/call compatibility with the existing G51 wrapper only: pass.
- G52 does not create new provider executor invocation runtime in LIMA: pass.
- G52 does not add built-in provider SDK clients: pass.
- G52 does not add direct provider SDK usage: pass.
- G52 does not add provider endpoint resolution: pass.
- G52 does not add direct network code or provider network egress: pass.
- G52 does not add ambient secret lookup: pass.
- G52 does not add credential value access: pass.
- G52 does not add provider token or API key access: pass.
- G52 does not add provider configuration changes: pass.
- G52 does not add fallback execution: pass.
- G52 does not add provider readiness network checks: pass.
- G52 does not add Token Guardian live routing: pass.
- G52 does not add connector, browser/network, file/device/robotics/physical-world behavior: pass.
- G52 does not add scheduled task execution or external sends: pass.
- G52 does not persist raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, API key, raw diff, full patch, or raw file content: pass.
- G52 does not claim product readiness or production readiness: pass.

## G51 Boundary Preservation

The V1-G51 wrapper remains the only runtime call surface exercised by G52 consumer tests. G52 does not modify the wrapper, does not expand the wrapper API, and does not weaken the G51 caller-injected executor boundary.

G52 confirms that consumers can call:

- `V1ExecutableRealProviderExecutorInvocationError`
- `execute_v1_executable_real_provider_executor_invocation`

The consumer tests call the wrapper with fake in-process provider executors only. The wrapper's record fields that say `provider_executor_invoked`, `real_provider_executor_invoked`, and `model_request_dispatched` are G51 candidate runtime evidence from the injected executor boundary. G52 does not convert those records into external provider, SDK, network, credential, connector, or product authority.

## G50 Boundary Preservation

G52 consumer tests build sanitized V1-G50 invocation envelope metadata. The V1-G50 envelope remains metadata-only and non-executing. G52 does not mutate it or use it to approve SDK, network, endpoint, credential, fallback, connector, or product-readiness authority.

## G48 Boundary Preservation

The V1-G48 hardening posture remains intact:

- credential policy is reference-only
- network policy is reference-only
- provider egress remains deny-by-default
- no secret lookup exists
- no credential value access exists
- no provider token/API key access exists
- no endpoint resolution exists
- no direct LIMA network call exists

G52 consumer tests preserve those conditions through fixture assertions and returned-record checks.

## Consumer Evidence Boundary

G52 adds consumer evidence for:

- Sparkbot branch `v1-g52-consumer-fake-executor-provider-invocation-smoke`, commit `77838a00f981bbae1e2f299055df4f4ee7d9663a`
- Arc-Bot-shell branch `v1-g52-consumer-fake-executor-provider-invocation-smoke`, commit `8358b8c3afb0bc18b886b19452e160c3c560e3cf`

This consumer evidence proves:

- public import shape is usable by both consumers
- sanitized V1-G50 envelope metadata can be assembled in consumer tests
- the G51 wrapper can be called by both consumers with fake in-process executors
- returned records preserve forbidden-boundary false claims
- no consumer production runtime modules are imported or edited

This consumer evidence does not prove:

- live provider credentials are available or approved
- built-in provider SDK clients are available or approved
- provider endpoints can be resolved
- direct provider network egress is allowed
- fallback is allowed
- connectors or browser/network authority are allowed
- physical-world behavior is allowed
- product readiness is achieved

## Validation Evidence

- Sparkbot focused V1-G52 test: passed, 8 tests.
- Sparkbot focused V1-G47 test: passed, 8 tests.
- Arc-Bot-shell focused V1-G52 test: passed, 8 tests.
- Arc-Bot-shell focused V1-G47 test: passed, 8 tests.
- LIMA focused V1-G52 tests: passed, 12 tests.
- LIMA focused V1-G52/G51/G50/G22 tests: passed, 144 tests.
- Full LIMA suite: passed, 4536 tests.
- `python -m compileall lima`: passed.
- `git diff --check` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell: passed.

## Residual Blocked Authorities

- Built-in provider SDK integration remains blocked.
- Provider endpoint resolution remains blocked.
- Direct provider network egress remains blocked.
- Secret lookup and credential value access remain blocked.
- Provider token/API key access remains blocked.
- Fallback execution remains blocked.
- Connector/browser/network authority remains blocked.
- HumanInput bridge activation remains blocked.
- Consumer production runtime integration remains blocked.
- Device/robot/drone/IoT/physical-world authority remains blocked.
- Product readiness remains blocked.

## Chain Decision

The V1 runtime authority chain through G52 remains candidate-only and authority-gated.

Recommended next step: update the V1 readiness rollup through G52 and prepare the next-lane decision matrix. Do not proceed to built-in provider SDK clients, provider credential access, provider network egress, endpoint resolution, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, or product-readiness claims from this audit branch.
