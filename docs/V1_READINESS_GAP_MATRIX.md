# V1 Readiness Gap Matrix

This matrix turns the V1 product target into the current implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, provider SDK/network egress, GuardianDecision execution authority, approval enforcement expansion, persistence expansion, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Current branch: `audit-v1-g55-real-provider-sdk-network-egress`
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Current product status: not V1-ready
- API status: `CANDIDATE_ONLY`
- Latest completed gate: `V1-G55`
- Current implementation approval: not granted for G56
- Current active gate: `V1-G56`
- Current required next artifact: V1-G56 consumer fake-executor provider SDK/network egress smoke approval request

## Readiness Matrix

| ID | Gap | Current evidence | V1-ready requirement | Recommended lane | Runtime approval needed |
| --- | --- | --- | --- | --- | --- |
| `V1-G1` through `V1-G10` | Static target, first-shell proof, contract, release-boundary, and implementation-gate evidence | Historical docs/tests/fixtures exist and remain part of the V1 evidence base | Keep target, shell proof, approval, haptic, release-boundary, and implementation-gate constraints explicit | Complete as historical candidate-only evidence | No current implementation approval |
| `V1-G11` through `V1-G17` | Typed request, GuardianDecision preflight, audit/evidence persistence, approval-enforcement, shell guiderail, guarded file mutation, and preview/diff slices | Local non-executing metadata proves the earliest Guardian and audit chain | Preserve fail-closed request/decision/evidence behavior | Complete as candidate-only runtime/evidence slices | Already approved and implemented only inside prior scopes |
| `V1-G18` through `V1-G28` | Consumer proof intake, live approval metadata, provider/model routing authority, compatibility/freeze metadata, dry-run/import-plan/patch-preview evidence, consumer repo edits, import smoke, and runtime export cleanup evidence | Consumer-facing evidence stays bounded and audited | Preserve first consumer import and public API evidence without product readiness claims | Complete as candidate-only evidence | Already approved and implemented only inside prior scopes |
| `V1-G29` through `V1-G42` | Consumer import/call planning, fake runtime call evidence, consumer test preview/edit/smoke, live import/call tests, compatibility review, bounded integration design, integration patch/edit/import smoke, shell wiring design and implementation evidence | Consumer and shell integration evidence remains bounded by approval and fake-runtime constraints where required | Preserve testability with Sparkbot and Arc-Bot-shell without claiming production integration | Complete as candidate-only integration evidence | Already approved and implemented only inside prior scopes |
| `V1-G43` through `V1-G55` | Provider/model dispatch, live provider/model authority/execution metadata, fake-executor consumer smoke, credential/network hardening, real provider executor design/invocation/wrapper metadata, provider SDK/network/credential authority, fake SDK/fake-egress harness evidence, and bounded real provider SDK/network egress wrapper evidence | Provider/model/provider-SDK authority chain exists with caller-injected executors only, without LIMA-owned SDK clients, secrets, credential values, endpoint resolution, or network egress | Preserve caller-injected and fake-harness boundaries before any consumer fake-executor smoke, credential, fallback, connector, or production lane | Complete through G55 as candidate-only authority evidence | Already approved and implemented only inside prior scopes |
| `V1-G56` | `docs/readiness/V1_POST_G55_NEXT_LANE_DECISION_MATRIX.md` | Next safe lane is request-only consumer fake-executor provider SDK/network egress smoke evidence against the G55 public wrapper | Prepare an approval request only; do not implement smoke tests or edit consumer repositories until a future exact approval exists | Request preparation pending | Yes, before implementation |

## Recommended Order

1. Treat V1-G1 through V1-G55 as accepted candidate-only evidence inside their original approved scopes.
2. Treat the G55 caller-injected provider SDK/network egress wrapper and runtime authority-chain audit as the latest completed provider SDK/network safety evidence.
3. Treat the V1 consumer target state after Arc readiness integration as consumer-side testing evidence only, not runtime authority.
4. Treat V1-G56 as request preparation only until an exact approval request and operator decision exist.
5. Reject any claim that the broad V1 goal, the G55 audit, the readiness rollup, the consumer target refresh, this matrix, or successful tests approve G56 implementation, credential value access, fallback, connector/browser/network authority, consumer production runtime integration, or product readiness.

## Stop Conditions

Stop and request a new approval gate before any work that adds:

- V1-G56 consumer fake-executor smoke implementation without exact approval
- file scope outside a future approved V1-G56 request
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell modifications for V1-G56 without exact approval
- credential handling or real provider SDK/network egress in a consumer smoke lane
- built-in provider SDK clients
- SDK dependencies
- vendor SDK imports
- direct provider SDK implementation
- provider endpoint resolution by LIMA
- LIMA-owned DNS, HTTP, socket, network calls, or direct provider egress
- secret lookup, credential value access, provider token access, or API key access
- provider configuration changes
- fallback execution
- consumer production runtime integration
- connector/browser/network/file/device/robotics/physical-world behavior
- V1 product readiness, production readiness, final release, or live customer claims

## Current Verdict

LIMA-AI-OS has a clearer and deeper V1 evidence chain through G55, but it is not V1 product-ready.

`V1-G55` is complete as the latest approved bounded caller-injected provider SDK/network egress wrapper slice. The runtime authority chain audit and readiness rollup through G55 are complete.

`V1-G56` is not prepared or approved yet. It should be request-only if opened. It must not add consumer smoke implementation, consumer repository edits, SDK clients, SDK dependencies, endpoint resolution, network calls by LIMA, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, or product-readiness claims without a future exact approval.

The next smallest safe step is to prepare a V1-G56 consumer fake-executor provider SDK/network egress smoke approval request. It should ask only whether first-shell consumers may prove import/call compatibility with the G55 wrapper using fake in-process caller-injected provider SDK/network executors. Stop before implementation, built-in SDK clients, SDK dependencies, LIMA-owned endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, physical-world behavior, or product-readiness claims.
