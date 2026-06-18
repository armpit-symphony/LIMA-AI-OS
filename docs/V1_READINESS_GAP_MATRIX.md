# V1 Readiness Gap Matrix

This matrix turns the V1 product target into the current implementation-readiness sequence.

It is docs/tests/fixtures-only. It does not approve runtime behavior, shell wiring, provider/model calls, provider SDK/network egress, GuardianDecision execution authority, approval enforcement expansion, persistence expansion, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Current Anchor

- Current branch: `docs-v1-product-readiness-through-g55`
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Current product status: not V1-ready
- API status: `CANDIDATE_ONLY`
- Current implementation approval: not granted for G55
- Current active gate: `V1-G55`
- Current required operator choice: `Approve-V1-G55`, `Revise-V1-G55`, or `Pause`

## Readiness Matrix

| ID | Gap | Current evidence | V1-ready requirement | Recommended lane | Runtime approval needed |
| --- | --- | --- | --- | --- | --- |
| `V1-G1` through `V1-G10` | Static target, first-shell proof, contract, release-boundary, and implementation-gate evidence | Historical docs/tests/fixtures exist and remain part of the V1 evidence base | Keep target, shell proof, approval, haptic, release-boundary, and implementation-gate constraints explicit | Complete as historical candidate-only evidence | No current implementation approval |
| `V1-G11` through `V1-G17` | Typed request, GuardianDecision preflight, audit/evidence persistence, approval-enforcement, shell guiderail, guarded file mutation, and preview/diff slices | Local non-executing metadata proves the earliest Guardian and audit chain | Preserve fail-closed request/decision/evidence behavior | Complete as candidate-only runtime/evidence slices | Already approved and implemented only inside prior scopes |
| `V1-G18` through `V1-G28` | Consumer proof intake, live approval metadata, provider/model routing authority, compatibility/freeze metadata, dry-run/import-plan/patch-preview evidence, consumer repo edits, import smoke, and runtime export cleanup evidence | Consumer-facing evidence stays bounded and audited | Preserve first consumer import and public API evidence without product readiness claims | Complete as candidate-only evidence | Already approved and implemented only inside prior scopes |
| `V1-G29` through `V1-G42` | Consumer import/call planning, fake runtime call evidence, consumer test preview/edit/smoke, live import/call tests, compatibility review, bounded integration design, integration patch/edit/import smoke, shell wiring design and implementation evidence | Consumer and shell integration evidence remains bounded by approval and fake-runtime constraints where required | Preserve testability with Sparkbot and Arc-Bot-shell without claiming production integration | Complete as candidate-only integration evidence | Already approved and implemented only inside prior scopes |
| `V1-G43` through `V1-G54` | Provider/model dispatch, live provider/model authority/execution metadata, fake-executor consumer smoke, credential/network hardening, real provider executor design/invocation/wrapper metadata, provider SDK/network/credential authority, and fake SDK/fake-egress harness evidence | Provider/model/provider-SDK authority chain exists without LIMA-owned SDK clients, secrets, or network egress | Preserve caller-injected, evidence-only, fake-harness boundaries before any real SDK/network egress wrapper | Complete through G54 as candidate-only authority evidence | Already approved and implemented only inside prior scopes |
| `V1-G55` | `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_APPROVAL_REQUEST.md`, `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_PREFLIGHT_AUDIT.md`, `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_OPERATOR_DECISION_PACKET.md`, and `docs/audits/V1_G55_IMPLEMENTATION_BLOCKER_AUDIT.md` | Bounded real provider SDK/network egress authority wrapper may be considered only after explicit operator approval | Record exactly one valid G55 operator choice; implement only after `Approve-V1-G55` and only inside the approved file map | Pending operator decision | Yes |

## Recommended Order

1. Treat V1-G1 through V1-G54 as accepted candidate-only evidence inside their original approved scopes.
2. Treat the G54 fake SDK/fake-egress harness and runtime authority-chain audit as the latest completed provider SDK/network safety evidence.
3. Treat V1-G55 as the active approval gate.
4. Reject any claim that the broad V1 goal, the G54 audit, the readiness rollup, this matrix, or successful tests approve G55 implementation.

## Stop Conditions

Stop and request a new approval gate before any work that adds:

- G55 implementation without `Approve-V1-G55`
- file scope outside the approved G55 request
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell modifications for G55
- provider SDK/network egress invocation
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

LIMA-AI-OS has a clearer and deeper V1 evidence chain through G54, but it is not V1 product-ready.

`V1-G54` is complete as the latest approved fake SDK/fake-egress harness evidence slice. The runtime authority chain audit and readiness rollup through G54 are complete.

`V1-G55` is prepared as an approval request and implementation blocker audit. It is not approved. It does not add the bounded real provider SDK/network egress wrapper, public API exports, SDK clients, SDK dependencies, endpoint resolution, network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, or product-readiness claims.

The next smallest safe step is to record one valid operator choice in the V1-G55 operator decision packet. If explicitly approved with the required wording, implement only the bounded real provider SDK/network egress authority wrapper exactly inside the approved G55 file-touch map, still without built-in SDK clients, SDK dependencies, LIMA-owned endpoint resolution, LIMA-owned network calls, secret lookup, credential value access, provider configuration changes, fallback, consumer production runtime integration, physical-world behavior, or product-readiness claims.
