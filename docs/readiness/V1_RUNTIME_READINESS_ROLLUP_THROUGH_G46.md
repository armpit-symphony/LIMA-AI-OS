# V1 Runtime Readiness Rollup Through G46

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g46`
API status: `CANDIDATE_ONLY`

## Required Verdicts

- V1 runtime authority chain: `CANDIDATE_ONLY`
- Provider/model routing authority metadata: `CANDIDATE_ONLY`
- Provider/model dispatch evidence: `CANDIDATE_ONLY`
- Live provider/model call authority metadata/preflight: `CANDIDATE_ONLY`
- Frozen public API export surface for G46 wrapper: `CANDIDATE_ONLY`
- Bounded live provider/model call execution wrapper: `CANDIDATE_ONLY`
- Caller-injected provider executor invocation: `CANDIDATE_ONLY`
- Built-in provider SDK integration: `NOT_APPROVED`
- Direct provider network egress: `NOT_APPROVED`
- Secret lookup and credential value access: `NOT_APPROVED`
- Fallback execution: `NOT_APPROVED`
- Connector/browser/network authority: `NOT_APPROVED`
- Physical-world readiness: `BLOCKED`
- Product readiness: `NOT_READY`

## Current Accepted Evidence

- V1-G11 through V1-G17: local non-executing runtime request, approval, policy, and preview metadata slices.
- V1-G18 through V1-G25: consumer intake, live approval metadata, routing metadata, compatibility/freeze metadata, API freeze, dry-run, import-plan, and patch-preview metadata.
- V1-G26 through V1-G34: static consumer proof/test edits, fake-runtime call evidence, and focused adapter-validator call tests.
- V1-G35 through V1-G37: LIMA-side compatibility review, bounded design, and patch-preview evidence.
- V1-G38: Sparkbot and Arc-Bot-shell static consumer integration candidate test/fixture edits, recorded by LIMA by commit hash.
- V1-G39: Sparkbot and Arc-Bot-shell static consumer integration import-smoke test/fixture edits, recorded by LIMA by commit hash.
- V1-G40: LIMA-side metadata-only Sparkbot and Arc-Bot-shell shell boundary design records.
- V1-G41: Sparkbot and Arc-Bot-shell static consumer integration implementation test/fixture edits, recorded by LIMA by commit hash.
- V1-G42: Sparkbot and Arc-Bot-shell static shell wiring implementation test/fixture edits, recorded by LIMA by commit hash.
- V1-G43: LIMA-side deterministic fake-provider/no-secret/no-network provider/model dispatch evidence.
- V1-G44: LIMA-side non-executing live provider/model call authority metadata/preflight validator.
- V1-G45: LIMA-side runtime export cleanup/public API refresh for the existing V1-G44 validator symbols.
- V1-G46: LIMA-side bounded live provider/model call execution wrapper with caller-injected provider executor only.

All accepted evidence remains proof or candidate runtime authority unless a later exact approval gate grants additional authority.

## V1-G46 Status

V1-G46 implemented the approved bounded live provider/model call execution slice.

Accepted evidence:

- exact `Approve-V1-G46` decision was recorded
- exact `Approve-V1-G46-Scope-Amendment` was recorded in the operator conversation for the G45 test amendment
- LIMA implementation stayed inside the approved V1-G46 file and behavior scope plus the approved G45 test amendment
- runtime files changed: `lima/harness/v1_live_provider_model_call_execution.py` and `lima/harness/__init__.py`
- `V1LiveProviderModelCallExecutionError` is now exported through `lima.harness.__all__`
- `execute_v1_live_provider_model_call` is now exported through `lima.harness.__all__`
- prior frozen V1-G22/G45 harness exports remain present
- no prior harness export was removed or renamed
- V1-G22 final public API freeze fixture was refreshed for the approved harness export change
- the G45 export test now preserves G45 exports while allowing later approved appended harness exports
- the execution wrapper requires a prevalidated V1-G44 authority record
- the execution wrapper requires V1-G46 approval linkage, audit linkage, redaction policy, and execution-boundary metadata
- the execution wrapper invokes only a caller-injected provider executor
- fake-executor tests prove execution behavior without provider credentials or real network calls
- no Sparkbot files were changed
- no Arc-Bot-shell files were changed
- no consumer runtime/source files were changed
- no built-in provider SDK client, direct network client, ambient secret lookup, credential value access, fallback execution, tool execution, connector/browser/network/device/robotics/physical-world behavior, external send, raw sensitive persistence, or product-readiness claim was added

Saved checkpoints:

- V1-G46 implementation commit: `3ed5b2d207ba28b136535b5836106516feab6349`
- V1-G46 audit commit: `e631e9c7e80f328c40bd5cec211e18a24d30e56f`
- V1 runtime authority chain through G46 audit commit: `f68529fcb91dca07f4cd675c38a86382b393a123`

## Capability-Open / Authority-Gated Posture

LIMA AI OS remains capability-open and authority-gated.

Capability-open means LIMA is intended to govern broad capabilities across bots, shells, workstations, office systems, models, tools, files, browser, network, connectors, devices, robots, drones, IoT, automation, and physical-world systems.

Authority-gated means current candidate lanes allow only the authority they explicitly prove. A blocked capability means "not authorized by the current gate," not "impossible forever."

## Provider Model Status

Provider/model routing authority metadata: `CANDIDATE_ONLY`

Provider/model dispatch evidence: `CANDIDATE_ONLY`

Live provider/model call authority metadata/preflight: `CANDIDATE_ONLY`

Frozen public API export surface for G46 wrapper: `CANDIDATE_ONLY`

Bounded live provider/model call execution wrapper: `CANDIDATE_ONLY`

Caller-injected provider executor invocation: `CANDIDATE_ONLY`

Built-in provider SDK integration: `NOT_APPROVED`

Direct provider network egress: `NOT_APPROVED`

Secret lookup and credential value access: `NOT_APPROVED`

Fallback execution: `NOT_APPROVED`

V1-G46 provides a bounded execution wrapper and sanitized evidence path only. It does not provide built-in model service connectivity, provider credential value access, direct provider egress, fallback execution, provider readiness checks, connector authority, or production readiness.

## Current Blocked Areas

- Built-in provider SDK integration is not approved.
- Direct provider network egress is blocked outside a caller-injected executor boundary.
- Secret lookup and credential value access are blocked.
- Fallback execution is blocked.
- Provider readiness network checks are blocked.
- Token Guardian live routing is blocked.
- Actual runtime file edit/delete/mutation execution is blocked.
- Raw live approval factor verification is blocked.
- Approval-token issuance is blocked.
- Connector behavior is blocked.
- Browser/network behavior is blocked.
- HumanInput bridge activation is blocked.
- Device/robot/drone/IoT/physical-world behavior is blocked.
- Product readiness is not approved.

## Product Readiness Status

Product readiness: `NOT_READY`

The current chain is candidate runtime authority infrastructure. It is not a product release, production readiness claim, built-in provider SDK approval, direct network egress approval, credential value access approval, connector approval, browser/network approval, or physical-world approval.

## Next Recommended Lane

Next recommended lane: prepare V1-G47 consumer fake-executor provider/model call smoke approval request.

Reason: V1-G46 makes the bounded execution wrapper importable through the candidate public `lima.harness` surface. The next smallest testable step for Sparkbot and Arc-Bot-shell is a request-only gate for consumer-side fake-executor import/call smoke tests. That gate should verify that both consumers can import the G46 public API and call it with a fake executor, without live provider credentials, real network calls, connector behavior, consumer production runtime calls, or product-readiness claims.

Do not implement consumer repository edits, built-in provider SDK integration, credential handling, network calls, external sends, fallback execution, runtime file mutation execution, connector/browser behavior, physical-world behavior, or product-readiness claims without future exact approvals.
