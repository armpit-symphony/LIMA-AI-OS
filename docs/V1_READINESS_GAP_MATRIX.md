# V1 Readiness Gap Matrix

This matrix turns the V1 product target into the current implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, provider SDK/network egress, GuardianDecision execution authority, approval enforcement expansion, persistence expansion, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Current branch: `prepare-v1-g57-provider-execution-hardening-authorization-approval-request`
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Current product status: not V1-ready
- API status: `CANDIDATE_ONLY`
- Latest completed gate: `V1-G56`
- Current implementation approval: not granted for G57
- Current active gate: `V1-G57`
- Current required next action: operator decision on the V1-G57 provider execution hardening authorization approval request

## Readiness Matrix

| ID | Gap | Current evidence | V1-ready requirement | Recommended lane | Runtime approval needed |
| --- | --- | --- | --- | --- | --- |
| `V1-G1` through `V1-G10` | Static target, first-shell proof, contract, release-boundary, and implementation-gate evidence | Historical docs/tests/fixtures exist and remain part of the V1 evidence base | Keep target, shell proof, approval, haptic, release-boundary, and implementation-gate constraints explicit | Complete as historical candidate-only evidence | No current implementation approval |
| `V1-G11` through `V1-G17` | Typed request, GuardianDecision preflight, audit/evidence persistence, approval-enforcement, shell guiderail, guarded file mutation, and preview/diff slices | Local non-executing metadata proves the earliest Guardian and audit chain | Preserve fail-closed request/decision/evidence behavior | Complete as candidate-only runtime/evidence slices | Already approved and implemented only inside prior scopes |
| `V1-G18` through `V1-G28` | Consumer proof intake, live approval metadata, provider/model routing authority, compatibility/freeze metadata, dry-run/import-plan/patch-preview evidence, consumer repo edits, import smoke, and runtime export cleanup evidence | Consumer-facing evidence stays bounded and audited | Preserve first consumer import and public API evidence without product readiness claims | Complete as candidate-only evidence | Already approved and implemented only inside prior scopes |
| `V1-G29` through `V1-G42` | Consumer import/call planning, fake runtime call evidence, consumer test preview/edit/smoke, live import/call tests, compatibility review, bounded integration design, integration patch/edit/import smoke, shell wiring design and implementation evidence | Consumer and shell integration evidence remains bounded by approval and fake-runtime constraints where required | Preserve testability with Sparkbot and Arc-Bot-shell without claiming production integration | Complete as candidate-only integration evidence | Already approved and implemented only inside prior scopes |
| `V1-G43` through `V1-G56` | Provider/model dispatch, live provider/model authority/execution metadata, fake-executor consumer smoke, credential/network hardening, real provider executor design/invocation/wrapper metadata, provider SDK/network/credential authority, fake SDK/fake-egress harness evidence, bounded real provider SDK/network egress wrapper evidence, and consumer fake-executor SDK/network egress smoke evidence | Provider/model/provider-SDK authority chain exists with caller-injected/fake executors only, without LIMA-owned SDK clients, secrets, credential values, endpoint resolution, or network egress | Preserve caller-injected and fake-harness boundaries before any provider execution hardening, credential, fallback, connector, or production lane | Complete through G56 as candidate-only authority and consumer smoke evidence | Already approved and implemented only inside prior scopes |
| `V1-G57` | `docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md` | Request-only provider execution hardening authorization packet is prepared after the G56 consumer smoke proof | Record exactly one valid operator choice; do not implement authorization evidence until `Approve-V1-G57` is recorded | Awaiting operator decision; implementation not approved | Yes, before implementation |

## Recommended Order

1. Treat V1-G1 through V1-G56 as accepted candidate-only evidence inside their original approved scopes.
2. Treat the G56 consumer fake-executor provider SDK/network egress smoke audit as the latest completed provider SDK/network consumer compatibility evidence.
3. Treat the V1 consumer target state after Arc readiness integration as consumer-side testing evidence only, not runtime authority.
4. Treat V1-G57 as request-only and awaiting exactly one operator decision until `Approve-V1-G57`, `Revise-V1-G57`, or `Pause` is recorded.
5. Reject any claim that the broad V1 goal, the G56 audit, the readiness rollup, the consumer target refresh, this matrix, or successful tests approve G57 implementation, credential value access, fallback, connector/browser/network authority, consumer production runtime integration, or product readiness.

## Stop Conditions

Stop and request a new approval gate before any work that adds:

- V1-G57 provider execution hardening authorization implementation without exact approval
- file scope outside a future approved V1-G57 request
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell modifications for V1-G57 without exact approval
- credential handling or real provider SDK/network egress in a hardening authorization lane
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

LIMA-AI-OS has a clearer and deeper V1 evidence chain through G56, but it is not V1 product-ready.

`V1-G56` is complete as the latest approved consumer fake-executor provider SDK/network egress smoke slice. The runtime authority chain audit and readiness rollup through G56 are complete.

`V1-G57` is prepared as an approval request but not approved. It must not add provider execution hardening authorization implementation, consumer repository edits, SDK clients, SDK dependencies, endpoint resolution, network calls by LIMA, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, or product-readiness claims unless `Approve-V1-G57` is explicitly recorded.

The next smallest safe step is to record exactly one operator choice in the V1-G57 provider execution hardening authorization operator decision packet. The request asks only whether LIMA may record metadata-only provider execution hardening authorization evidence after the G56 consumer smoke proof. Stop before implementation unless `Approve-V1-G57` is recorded. Stop before built-in SDK clients, SDK dependencies, LIMA-owned endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, physical-world behavior, or product-readiness claims.
