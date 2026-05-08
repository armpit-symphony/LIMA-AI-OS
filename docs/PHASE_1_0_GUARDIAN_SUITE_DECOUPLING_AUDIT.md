# Phase 1.0 Guardian Suite Decoupling Audit

## Purpose

This audit addresses the first Phase 1 blocker: Guardian Suite coupling to Sparkbot internals.

Phase 1.0 does not migrate behavior. Phase 1.0 does not enforce Guardian decisions. Phase 1.0 does not change production Sparkbot. Phase 1.0 identifies seams and import boundaries.

The goal is to make the first extraction step boring and defensible: Guardian must depend on LIMA contracts, not Sparkbot backend internals.

## Reference Commit Inspected

| Repo | Branch | Commit | Inspection date | Modified? |
| --- | --- | --- | --- | --- |
| `https://github.com/armpit-symphony/LIMA-Guardian-Suite` | `origin/main` | `0559d9a6ce7e3dc401185a6732a6c8fa123db477` | May 8, 2026 | No |

Inspection notes:

- The local checkout was not modified by this audit.
- The local checkout had pre-existing untracked cache/data and one local-only commit ahead of `origin/main`; this audit used fetched `origin/main` state for commit identity and read-only source inspection.
- Search focused on `guardian/`, `app/services/guardian/`, `tests/`, `README.md`, `docs/`, `pyproject.toml`, and requirements-style surfaces.

## Coupling Inventory

| Current file/path | Coupled import/reference | Coupling type | Why it blocks extraction | Proposed boundary/interface | Risk | Recommended action | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `app/services/guardian/auth.py` | `from app.models import ChatUser`; `SPARKBOT_OPERATOR_*`, `SPARKBOT_BREAKGLASS_*`, `SPARKBOT_PIN_*` env names | app.models / Sparkbot-specific path/config / runtime side effect | Auth depends on Sparkbot user model and process-local privileged session state. | Identity lookup adapter, `ApprovalMetadata`, auth session interface, explicit operator identity contract | critical | Isolate identity lookup and PIN/breakglass metadata before any Auth extraction. | First Auth seam should be interface-only, not live PIN enforcement. |
| `app/services/guardian/meeting_recorder.py` | `from app.crud import get_chat_messages`, `create_chat_meeting_artifact`; `from app.models import ChatUser`; `litellm.completion` | app.crud / app.models / runtime side effect | Meeting notes combine Sparkbot persistence, model call, and artifact write. | Transcript provider, artifact writer, `DataReference`, `RedactionMetadata`, model-context ref | high | Do not extract as Guardian core; classify as meeting service adapter. | Raw transcripts and prompts need privacy gates before persistence. |
| `app/services/guardian/task_guardian.py` | `from app.crud import create_audit_log, create_chat_message`; `from app.models import ChatRoom, ChatUser, UserType`; `from app.api.routes.chat.tools import execute_tool`; bridge imports | app.crud / app.models / app.services / runtime side effect | Scheduled task execution imports Sparkbot models, chat writes, tool execution, websocket broadcast, and bridge notifications. | Task scheduler contract, tool execution adapter, audit lineage adapter, notification adapter | critical | Keep do-not-extract-yet; split storage, execution, chat notification, and audit seams first. | This is the highest-risk coupling cluster. |
| `app/services/guardian/task_guardian.py` | `sqlite3`, `data/guardian/task_guardian.db`, `SPARKBOT_TASK_GUARDIAN_*` | direct database / Sparkbot-specific path/config | Task storage and runtime config are hardcoded to Sparkbot local data conventions. | `StorageProtocol`, scheduled action record, approval renewal metadata | high | Document persistence boundary before moving task state. | No DB migration in Phase 1.0. |
| `app/services/guardian/policy.py` | `from app.services.skills import _registry as _skill_registry` | app.services | Policy depends on Sparkbot dynamic skill registry and can classify fallback tools from Sparkbot runtime state. | `ToolPackRiskPolicy`, `PolicyEvaluationContext`, skill manifest provider | high | Replace direct registry dependency with manifest/pack interface before extraction. | Dynamic skills remain denied until classified. |
| `app/services/guardian/vault.py` | `sqlite3`, `SPARKBOT_GUARDIAN_DATA_DIR`, `SPARKBOT_DATA_DIR`, `SPARKBOT_VAULT_KEY`, encrypted value reads/writes | direct database / vault/auth persistence / Sparkbot-specific path/config | Vault is live secret persistence and decrypts plaintext values. | Vault interface, secret ref adapter, `StorageProtocol`, `DataReference`, `RedactionMetadata` | critical | Start with interface skeleton only; no live vault behavior or secret migration. | Raw secrets must stay referenced, never copied into audit. |
| `app/services/guardian/pending_approvals.py` | `sqlite3`, `data/guardian/pending_approvals.db` | direct database / vault/auth persistence | Approval state is stored directly in local SQLite with Sparkbot room/user fields. | Approval repository interface, `ApprovalMetadata`, expiry/revocation contract | high | Keep as reference; future adapter must hide storage. | Approval evidence does not replace `GuardianDecision`. |
| `app/services/guardian/executive.py` | JSONL decision path under Sparkbot-style `data/guardian/executive/decisions` | Sparkbot-specific path/config / runtime side effect | Executive journaling writes runtime evidence directly to local files. | Audit writer interface, `AuditLineageRecord`, `SpineEvent` | high | Keep as behavior reference; no audit persistence extraction yet. | Future audit must carry privacy metadata. |
| `app/services/guardian/memory.py` and `app/services/guardian/memory_os/*` | Sparkbot adapter comments, local `data/memory_guardian`, SQLite FTS/embed stores | direct database / Sparkbot-specific path/config | Memory combines local persistence, Sparkbot session naming, and retrieval behavior. | Memory reference interface, `DataReference`, `StorageProtocol`, privacy classes | high | Defer until privacy and storage adapters exist. | Memory content must be referenced or summarized. |
| `app/services/guardian/token_guardian.py` and `tokenguardian/*` | `SPARKBOT_TOKEN_GUARDIAN_*`, `~/.tokenguardian`, `/etc/tokenguardian`, Sparkbot audit metadata | Sparkbot-specific path/config / runtime side effect | Routing policy is useful, but config and telemetry are not kernel-clean yet. | Harness routing policy interface, model telemetry event, policy evidence | medium | Treat as later Harness policy reference after decoupling. | No live model routing in Phase 1.0. |
| `app/services/guardian/suite.py` | Imports all Guardian modules at suite import time | runtime side effect / unknown | Importing the suite can transitively import coupled modules and initialize local assumptions. | Lazy component registry over contract interfaces | high | Avoid importing this as LIMA core until components are split behind interfaces. | This is a useful inventory shape, not a kernel module. |
| `guardian/vault.py` | `sqlite3`, default `data/guardian/vault.db`, direct encrypted secret store | direct database / vault/auth persistence | Simplified standalone vault still persists and reveals secrets through direct storage. | Vault/Auth interface skeleton with secret refs only | high | Use only as reference for interface names. | Do not copy implementation. |
| `guardian/executive.py` / `guardian/adapters/openclaw.py` | Approval decision wrapper and OpenClaw adapter assumptions | runtime side effect / unknown | Contains enforcement-style wrappers and an external agent adapter, not a LIMA contract seam. | `GuardianProtocol`, `ConsequentialActionRequest`, policy evidence | medium | Defer; extract no enforcement behavior. | Good evidence that enforcement must stay behind contracts. |
| `tests/services/test_guardian_suite.py` | `from app.services.guardian import get_guardian_suite` | app.services | Tests prove the current coupled import path, not LIMA independence. | LIMA import-boundary tests and future parity tests | medium | Add LIMA-side forbidden-import test first. | Phase 1.0 adds the LIMA boundary check only. |

Coupling findings count: 14 inventory rows.

## Forbidden Imports

Future `lima.guardian` code must not import:

- `app.crud`
- `app.models`
- `app.services`
- `backend.app`
- Sparkbot runtime modules
- frontend modules
- production-specific config
- local deployment paths
- direct Sparkbot DB sessions

The import boundary also rejects route-level Sparkbot modules such as `app.api.routes.chat.tools`, `app.api.routes.chat.llm`, and `app.api.routes.chat.websocket` inside Guardian core. Those belong behind adapters, not in the kernel.

## Allowed Boundary Concepts

Future Guardian code may depend only on contracts/interfaces such as:

- `GuardianDecision`
- `ConsequentialActionRequest`
- `ApprovalMetadata`
- `ToolPackRiskPolicy`
- `AuditLineageRecord`
- `DataReference` / `RedactionMetadata`
- `StorageProtocol`
- Vault/Auth interfaces
- explicit persistence adapters

Guardian policy evidence can narrow or deny work. It must not expand tool scope, execute tools, call models, persist raw secrets, or write production state.

## First Extraction Seam

The first safe seam is a non-executing Vault/Auth interface boundary or GuardianDecision request/decision dataclass boundary, not live policy enforcement.

Preferred next seam:

1. Define a Vault/Auth interface skeleton that returns secret references and approval/auth metadata only.
2. Prove it imports without `app.crud`, `app.models`, `app.services`, Sparkbot routes, or direct Sparkbot DB sessions.
3. Keep Sparkbot's existing vault/auth behavior untouched behind a future adapter.

This keeps Guardian as the trust boundary while avoiding accidental secret persistence, breakglass enforcement, or production behavior changes.

## Do-Not-Extract-Yet

- Any module that imports `app.crud` directly.
- Any module that imports `app.models` directly.
- Any module that imports `app.services` directly.
- Any module that imports Sparkbot route modules such as `app.api.routes.chat.tools`, `app.api.routes.chat.llm`, or `app.api.routes.chat.websocket`.
- Any module that opens Sparkbot DB directly.
- Any module that reads/writes live vault secrets.
- Any module that performs live auth/breakglass enforcement.
- Any module that performs tool execution.
- Any module that calls live models.
- Any module with side effects at import time.
- Any module that writes audit/approval/task/vault persistence directly instead of using LIMA contracts.

## Phase 1.1 Recommendation

Recommended next branch: `phase-1-1-vault-auth-interface-skeleton`.

Proceed only if Phase 1.0 is reviewed and confirms the import-boundary seam stays clean.

Phase 1.1 should remain skeleton/interface work unless explicitly reviewed otherwise. It should not migrate live vault storage, live PIN verification, breakglass sessions, task scheduling, tool execution, model routing, or audit persistence.
