# Extraction Readiness Review

## Purpose

This is the final Phase 0 readiness review before Phase 1 extraction.

It does not authorize implementation by itself. It does not migrate code. It identifies the safest Phase 1 extraction order.

Phase 1 should reduce coupling before moving behavior. LIMA Runtime is ready for narrow, non-executing boundary work. It is not ready for Harness/tool execution extraction, terminal/PTY extraction, Robo-OS physical action integration, audit persistence, redaction runtime, policy enforcement, approval enforcement, or production runtime migration.

## Reference Commits Rechecked

| Repo | Branch | Commit | Freshness notes | Modified? | Boundary impact since Phase 0.14 |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `origin/main` | `129eab05b37b5d3fb6b078b4218b0dca7f6d993b` | Rechecked after fetch. Local checkout remains behind `origin/main` by 9 commits, so review used fetched `origin/main` read-only. | No | No movement since Phase 0.14. No new boundary impact beyond already documented chat/model/tool, voice, tools, dynamic skills, MCP, Guardian, terminal, file/browser/network, Spine/audit/task, and robotics bridge risks. |
| LIMA-Guardian-Suite | `origin/main` | `0559d9a6ce7e3dc401185a6732a6c8fa123db477` | Rechecked after fetch. Local checkout has one local-only commit and pre-existing untracked cache/data; review used `origin/main` and ignored local dirty state. | No | No movement since Phase 0.14. Coupling remains the first extraction risk: `app.crud`, `app.models`, `app.services`, SQLite persistence, and Sparkbot route assumptions still appear in Guardian-style modules. |
| LIMA-Robo-OS | `origin/main` | `d6f8edc7423e72343d0e4778fb7555b96beed288` | Rechecked after fetch. Local worktree still reports a pre-existing Git LFS clean/filter issue for `data/.lfs/unitree_go2_bigoffice.tar.gz`; review used `origin/main` and did not rely on large data files. | No | No movement since Phase 0.14. Robo-OS remains a Guardian-gated driver/runtime integration candidate, with direct CLI/MCP/skill and physical-world action paths blocked until GuardianDecision, ApprovalMetadata, dry-run/simulation, lineage, and sensor privacy gates exist. |

## Phase 0 Contract Inventory

| Phase | Contract/doc | Status | What it gates | Ready for Phase 1? | Notes |
| --- | --- | --- | --- | --- | --- |
| Phase 0 | LIMA Runtime architecture/contracts | Landed | Kernel shape, Guardian invariant, layer model, MCP boundary, package skeleton | Yes | Ready as architecture baseline only. No runtime behavior exists. |
| Phase 0.5 | Intent Compiler Boundary | Landed | Raw human input, voice, console, gesture, future BCI, typed intent, clarification | Partial | Ready for adapter design. Not ready for execution because compiler implementation is absent by design. |
| Phase 0.6 | Sparkbot Entrypoint Inventory | Landed | Sparkbot chat, voice, model, tool, Guardian, terminal, browser, network, meeting, robotics entrypoints | Partial | Good enough to block unsafe paths and guide first audit. Recheck Sparkbot before any code movement. |
| Phase 0.7 | GuardianDecision ID Contract | Landed | `decision_id` requirement before consequential execution | Partial | Contract is ready. Runtime decision issuance/enforcement is intentionally absent. |
| Phase 0.8 | Tool-Pack Scoping Contract | Landed | Deny-by-default pack exposure and Harness selected-tools shortlist | Partial | Ready for classification fixtures. Not ready for live Harness/tool extraction. |
| Phase 0.9 | Sparkbot Tool-Pack Inventory | Landed | Sparkbot tools grouped into proposed packs and unknown denied by default | Partial | Inventory is useful but must be refreshed if Sparkbot tools move. |
| Phase 0.10 | Tool-Pack Risk Policy | Landed | Default pack risk, mixed read/write rules, dynamic skills, scheduled inheritance | Partial | Policy shape is ready. Enforcement is not implemented and must not be assumed. |
| Phase 0.11 | Approval Metadata Contract | Landed | Human/operator approval evidence for high/critical actions | Partial | Contract is ready. Approval enforcement and token issuance remain future work. |
| Phase 0.12 | Spine/Audit Lineage Contract | Landed | Input-to-result lineage, event IDs, critical action traceability | Partial | Event shapes are ready. Storage/audit persistence is blocked. |
| Phase 0.13 | Redaction/Privacy Contract | Landed | Sensitive data references, retention, visibility, no raw secrets in audit | Partial | Contract is ready. Redaction implementation and storage are absent by design. |
| Phase 0.14 | Runtime Boundary Map | Landed | Sparkbot, Guardian Suite, and Robo-OS boundary classification | Yes | Ready to guide Phase 1 order. Unsafe shortcuts are explicitly do-not-extract-yet. |

## Readiness Score

Architecture readiness: 9/10

- The LIMA Kernel layer model, Guardian syscall gate, MCP boundary rule, shell/service/spine/harness/driver/persistence split, and Sparkbot parity rule are coherent enough to guide Phase 1.

Contract readiness: 8/10

- Core Phase 0 contracts exist and import cleanly. Remaining gap is not contract shape; it is proving import seams and keeping moving Sparkbot behavior rechecked during extraction.

Extraction safety: 6/10

- The blocked list is clear, and the first safe target is narrow. Safety drops quickly if Phase 1 jumps into Harness/tool execution, terminal/PTY, audit persistence, or Robo-OS actions.

Implementation readiness: 4/10

- Implementation is intentionally absent. LIMA is ready for decoupling audit, import-boundary tests, and interface scaffolding, not runtime migration or live enforcement.

Overall Phase 1 readiness: ready with constraints.

LIMA-AI-OS is ready for Phase 1 planning and the first narrow Phase 1 target only. It is not ready for Harness/tool execution extraction, stream-chat refactor-as-runtime, Robo-OS physical action wiring, terminal/PTY runtime extraction, real audit persistence, redaction runtime, or production migration.

## Ready Areas

- Guardian/Vault/Auth decoupling review against Sparkbot and LIMA-Guardian-Suite references.
- Contract-compatible Guardian Suite cleanup planning.
- Read-only adapter and interface design.
- Package/import boundary tests.
- Docs-backed extraction scaffolding.
- Shell adapter design for Sparkbot `HumanInput` only.
- Non-executing import boundary checks for `lima.guardian`.
- Tool-pack classification fixtures for Sparkbot tool names, with no execution.
- Sparkbot MCP explain-plan and run approval surfaces as adapter references.
- Sparkbot Spine views as audit/read-model references, with no persistence implementation.

## Blocked Areas

- `stream_chat_with_tools` direct extraction.
- Full-catalogue tool exposure.
- Terminal/PTY execution.
- Raw natural language to robot MCP command path.
- Dynamic skills without pack classification.
- `execute_tool` fallback names without classification.
- Model prompt logging without privacy/redaction.
- Tool args/results logging without privacy/redaction.
- Terminal output logging without privacy/redaction.
- Robot sensor logging without privacy/redaction.
- Real Spine storage/audit persistence.
- Robo-OS physical execution.
- Guardian enforcement runtime.
- Approval enforcement runtime.
- Policy enforcement runtime.
- Harness/tool execution extraction.
- Redaction runtime.
- Production deploy/update integration.

## First Safe Extraction Target

Phase 1.0 / PR #1 should be Guardian Suite decoupling audit and import-boundary work, not runtime migration.

Recommended first branch: `phase-1-0-guardian-suite-decoupling-audit`.

Goal: identify and remove or isolate Sparkbot `app.crud` / `app.models` / `app.services` coupling from LIMA-Guardian-Suite-style Guardian modules, without changing runtime behavior.

If actual code movement is too risky, Phase 1.0 should remain a decoupling audit and test harness first.

Acceptance criteria for Phase 1 PR #1:

- no Sparkbot runtime behavior changed
- no production wiring
- no tool execution
- no model execution
- no secrets
- Guardian modules import without Sparkbot `app.crud` / `app.models`
- import-boundary tests prove `lima.guardian` does not depend on Sparkbot backend app modules
- Vault/Auth contracts remain compatible
- docs updated with remaining coupling
- compile/tests pass

## Recommended Phase 1 Extraction Order

Phase 1.0: Guardian Suite decoupling audit and import-boundary tests.

Phase 1.1: Vault/Auth contract-compatible skeleton extraction.

Phase 1.2: GuardianDecision non-executing evaluator interface skeleton.

Phase 1.3: ApprovalMetadata and breakglass metadata skeleton, no enforcement.

Phase 1.4: Policy/risk interface skeleton, no enforcement.

Phase 1.5: Spine/Audit event adapter design, no persistence.

Phase 1.6: Sparkbot HumanInput adapter design, no tool execution.

Phase 1.7: Tool-pack classification fixtures for Sparkbot tools, no execution.

Defer:

- Harness extraction
- `stream_chat_with_tools` refactor
- terminal/PTY
- Robo-OS physical actions
- real audit persistence
- redaction runtime
- policy enforcement
- approval enforcement
- production deploy/update integration

## Phase 1 PR #1 Work Order

Title: Phase 1.0 - Guardian Suite Decoupling Audit

Scope:

- inspect LIMA-Guardian-Suite and Sparkbot Guardian references
- identify `app.crud` / `app.models` / `app.services` imports
- create import boundary report
- add tests/checks in LIMA-AI-OS or docs that define forbidden imports
- optionally create no-op interface placeholders if needed
- no runtime behavior changes

Out of scope:

- real Guardian enforcement
- runtime migration
- Sparkbot production changes
- tool/model execution
- vault secret migration
- DB migrations
- Robo-OS integration

Acceptance criteria:

- coupling report exists
- forbidden imports listed
- first extraction seam identified
- tests/commands validate LIMA package imports
- no implementation copied unless explicitly safe and stub-only
- Phase 1.1 target is clear

## Final Go / No-Go Decision

GO for Phase 1.0 decoupling audit and import-boundary work.

NO-GO for runtime extraction, Harness extraction, tool execution extraction, `stream_chat_with_tools` extraction, terminal/PTY extraction, Robo-OS physical integration, audit persistence, redaction runtime, policy enforcement, approval enforcement, or production runtime migration.

## Risk Register

| Risk | Severity | Current mitigation | Next action | Phase target |
| --- | --- | --- | --- | --- |
| Guardian Suite Sparkbot coupling | high | Runtime Boundary Map identifies app/model/CRUD coupling | Build coupling report and import-boundary tests | Phase 1.0 |
| Sparkbot `stream_chat_with_tools` coupling | critical | Marked do-not-extract-yet | Leave blocked until intent, decision, pack, approval, lineage, and privacy adapters are proven | Deferred |
| Dynamic skills changing | high | Unknown/dynamic tools denied by default in contracts | Add classification fixtures and refresh inventory before tool work | Phase 1.7 |
| Full-catalogue tool exposure | critical | Tool-pack scoping and risk policy require selected-tools only | Do not extract Harness/tool catalogue until pack tests exist | Deferred |
| Missing enforcement | high | Contracts distinguish policy evidence from execution | Keep Phase 1.0 non-executing | Phase 1.0-1.4 |
| Missing redaction implementation | high | Privacy contract blocks raw sensitive persistence | Defer audit persistence and logging of raw prompts/results/output/sensors | Deferred |
| Terminal/PTY risk | critical | Terminal pack is critical and do-not-extract-yet | Do not move raw PTY into kernel until approval, redaction, and lineage gates exist | Deferred |
| Robo-OS physical-world risk | critical | Robo-OS classified as Guardian-gated driver/runtime integration | Keep physical actions blocked; require dry-run/simulation and approval metadata later | Deferred |
| Audit persistence not implemented | high | Spine/Audit lineage is contract-only | Design adapter events before storage | Phase 1.5 |
| Approvals/breakglass not enforced | critical | ApprovalMetadata contract records evidence but not enforcement | Build metadata skeleton before enforcement | Phase 1.3 |
| Sparkbot `origin/main` moving during Phase 1 | medium | Phase 0.15 records latest reference commit | Recheck Sparkbot before every extraction PR | Phase 1.0+ |

## Final Checklist Before Phase 1

- [x] Phase 0 docs landed on main
- [x] Phase 0 tags exist through Phase 0.14
- [x] contracts import cleanly
- [x] tests pass before Phase 0.15 changes
- [x] reference commits recorded
- [x] blocked items documented
- [x] first Phase 1 branch defined
- [x] do-not-extract-yet list confirmed
- [x] no unsafe shortcut selected as first target

## Recommended Next Step

Recommended next branch: `phase-1-0-guardian-suite-decoupling-audit`.

Recommended first PR title: `Phase 1.0 - Guardian Suite Decoupling Audit`.

The first micro-step is to create a Guardian coupling report that lists forbidden Sparkbot imports, classifies which modules can become contracts, and adds import-boundary tests proving `lima.guardian` remains independent from Sparkbot backend application modules.
