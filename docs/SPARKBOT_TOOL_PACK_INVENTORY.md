# Sparkbot Tool-Pack Inventory

## Purpose

This inventory maps Sparkbot's current broad tool surface into future LIMA tool packs. It prevents extracting a full-catalogue firehose into LIMA Runtime.

This does not migrate code. This does not enforce packs. This does not modify Sparkbot.

Sparkbot remains the spec, but LIMA Runtime must preserve Sparkbot behavior through scoped, auditable, deny-by-default tool packs rather than by preserving broad catalogue exposure.

## Sparkbot Commit Inspected

- Repo: `https://github.com/armpit-symphony/Sparkbot`
- Branch inspected: `origin/main`
- Commit inspected: `fdc65ea33f23adbb39a6c9267b684f1277824c41`
- Inspection date: May 7, 2026
- Local checkout state: local `main` was at `9f68de2d14e59391b9c65b5d7cd6c0da6d8d089f` and behind `origin/main` by 3 commits.
- Freshness: `origin/main` was fetched and inspected read-only through `git grep`, `git show`, and `git ls-tree`; the Sparkbot worktree was not modified or checked out to the newer commit.

## Discovery Method

Commands and patterns used from the Sparkbot repository:

- `git fetch --all --prune`
- `git ls-tree -r --name-only origin/main`
- `git grep -n -i -E "tool|tools|function_call|tool_call|_select_tool_definitions|_CORE_TOOL_PRIORITY|stream_chat_with_tools|execute_tool|run_tool|call_tool|skills|terminal|pty|shell|browser|filesystem|file|network|http|websocket|mcp|robot|robo|guardian|approval|breakglass|vault|calendar|gmail|email|meeting|roundtable|sparkbud|memory|task|spine|audit|deploy|admin|payment|stripe" origin/main -- backend frontend scripts docs pyproject.toml package.json`
- `git show origin/main:backend/app/api/routes/chat/tools.py`
- `git grep` over `backend/skills`, `backend/app/services`, `backend/app/api/routes/chat`, `.github/workflows`, `scripts`, and docs.

The inspected static catalogue in `backend/app/api/routes/chat/tools.py` exposes 71 named tools. The dynamic skill directory under `backend/skills/` exposes 66 named skill tools. The MCP registry contains 11 manifest-level tool surfaces. Some names overlap between the static catalogue and dynamic skills, especially calendar tools. Results are best-effort and must be re-run before actual extraction.

## Catalogue Evidence

These lists are inventory evidence only. They do not create packs, enforce packs, expose tools, execute tools, or modify Sparkbot.

### Static Chat Catalogue: 71 Tool Names

- `remember_fact`, `forget_fact`, `memory_recall`, `memory_retrieval_stats`, `memory_reindex`, `memory_compact`
- `web_search`, `fetch_url`
- `browser_open`, `browser_navigate`, `browser_snapshot`, `browser_fill_field`, `browser_click`, `browser_close`, `browser_save_session`, `browser_restore_session`, `browser_list_sessions`
- `terminal_list_sessions`, `terminal_send`
- `get_datetime`, `calculate`
- `create_task`, `list_tasks`, `complete_task`
- `github_list_prs`, `github_get_pr`, `github_create_issue`, `github_get_ci_status`
- `slack_send_message`, `slack_list_channels`, `slack_get_channel_history`
- `notion_search`, `notion_get_page`, `notion_create_page`
- `confluence_search`, `confluence_get_page`, `confluence_create_page`
- `gmail_fetch_inbox`, `gmail_search`, `gmail_get_message`, `gmail_send`
- `drive_search`, `drive_get_file`, `drive_create_folder`
- `server_read_command`, `server_manage_service`, `ssh_read_command`
- `email_fetch_inbox`, `email_search`, `email_send`
- `set_reminder`, `list_reminders`, `cancel_reminder`
- `guardian_schedule_task`, `guardian_list_tasks`, `guardian_list_runs`, `guardian_propose_improvement`, `guardian_simulate_policy`, `guardian_list_improvements`, `guardian_run_task`, `guardian_pause_task`
- `calendar_list_events`, `calendar_create_event`
- `telegram_test_connection`
- `lima_robot_command`
- `vault_list_secrets`, `vault_use_secret`, `vault_reveal_secret`, `vault_add_secret`, `vault_update_secret`, `vault_delete_secret`

### Dynamic Skill Catalogue: 66 Tool Names

- `backend/skills/apple_integrations.py`: `apple_contacts_search`, `apple_reminders_list`, `apple_reminders_create`, `apple_notes_search`, `apple_notes_create`
- `backend/skills/audio_transcribe.py`: `transcribe_audio`
- `backend/skills/calendar_create_event.py`: `calendar_create_event`
- `backend/skills/calendar_list_events.py`: `calendar_list_events`
- `backend/skills/contacts.py`: `contacts_search`, `contacts_add`, `contacts_update`, `contacts_delete`, `contacts_sync_google`
- `backend/skills/crypto_price.py`: `crypto_price`
- `backend/skills/currency_convert.py`: `currency_convert`
- `backend/skills/example_weather.py`: `get_weather`
- `backend/skills/knowledge_base.py`: `ingest_document`, `search_knowledge`, `list_knowledge`, `delete_knowledge`
- `backend/skills/linear_jira.py`: `linear_list_issues`, `linear_create_issue`, `linear_update_issue`, `jira_list_issues`, `jira_create_issue`, `jira_add_comment`
- `backend/skills/microsoft_graph.py`: `outlook_read_mail`, `outlook_send_mail`, `outlook_calendar_list`, `outlook_calendar_create`, `onedrive_list`, `onedrive_read`
- `backend/skills/morning_briefing.py`: `morning_briefing`
- `backend/skills/news_headlines.py`: `news_headlines`
- `backend/skills/nl_sql.py`: `execute_sql`, `list_databases`, `describe_table`
- `backend/skills/proactive_alerts.py`: `send_alert`
- `backend/skills/relationship_memory.py`: `remember_person`, `recall_person`, `list_people`, `log_interaction`, `forget_person_fact`, `forget_person`
- `backend/skills/run_code.py`: `run_code`
- `backend/skills/shell_run.py`: `shell_run`
- `backend/skills/spotify.py`: `spotify_play`, `spotify_pause`, `spotify_next`, `spotify_previous`, `spotify_now_playing`, `spotify_search`, `spotify_volume`
- `backend/skills/stocks.py`: `stock_quote`, `stock_history`, `portfolio_add`, `portfolio_view`, `portfolio_remove`
- `backend/skills/system_diagnostics.py`: `system_diagnostics`
- `backend/skills/time_tracking.py`: `time_start`, `time_stop`, `time_log`, `time_report`, `time_status`
- `backend/skills/youtube_summarize.py`: `youtube_transcript`, `youtube_summarize`

Dynamic skill names are loaded through `SPARKBOT_SKILLS_DIR` and `_register_extra()`. A future LIMA extraction must not treat this list as stable or self-authorizing; any newly loaded or unclassified skill remains `unknown` and denied by default until it has an explicit pack and risk classification.

### MCP Manifest Surfaces: 11 Manifest IDs

- `sparkbot.shell_run` -> `terminal`
- `sparkbot.terminal_send` -> `terminal`
- `sparkbot.browser_control` -> `browser`
- `sparkbot.google_calendar` -> `calendar`
- `sparkbot.task_guardian` -> `meeting` / workflow scheduling, with target-tool pack inheritance required before execution
- `sparkbot.guardian_vault` -> `admin`
- `sparkbot.memory_recall` -> `memory`
- `lima.navigate` -> `robo`
- `lima.inspect` -> `sensors`
- `lima.stop` -> `robo`
- `lima.replay_simulation` -> `robo` / `sensors` depending on whether the request is simulation control or read-only replay inspection

The MCP registry is a manifest catalogue, not an execution boundary by itself. Manifest IDs still require shell allowance, intent classification, `GuardianDecision.allowed_tool_packs`, selected-tool narrowing, and audit evidence before any future execution path exists.

## Proposed Pack Map

| Proposed pack | Current Sparkbot path/file | Tool/function/surface name | Current role | Default risk | Approval expectation | Requires decision_id | Shells likely allowed | Extraction notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| core | `backend/app/api/routes/chat/tools.py` | `get_datetime`, `calculate` | Basic local utility tools. | low | Usually policy auto-allow later. | Yes for model/tool execution lineage. | Sparkbot, Arc, SparkPit web, Robo-OS | Safe default candidates, but still audited when exposed to a model. |
| model | `backend/app/api/routes/chat/llm.py`, `backend/app/api/routes/chat/model.py`, `backend/app/services/guardian/token_guardian/*` | `stream_chat_with_tools()`, `_select_tool_definitions()`, model controls, Token Guardian routing | Model routing, tool-aware streaming, provider fallback, cost/token policy. | high | Guardian review for consequential model calls with project/user context. | Yes | Sparkbot, Arc, SparkPit web | Must split raw chat, model planning, pack shortlist, and execution. |
| memory | `backend/app/api/routes/chat/tools.py`, `backend/app/api/routes/chat/memory.py`, `backend/app/services/guardian/memory*`, `backend/skills/relationship_memory.py`, `backend/skills/knowledge_base.py` | `remember_fact`, `forget_fact`, `memory_recall`, `memory_retrieval_stats`, `memory_reindex`, `memory_compact`, `remember_person`, `recall_person`, `list_people`, `log_interaction`, `forget_person_fact`, `forget_person`, `ingest_document`, `search_knowledge`, `list_knowledge`, `delete_knowledge` | Guardian memory, relationship memory, knowledge ingestion/search, memo hygiene. | medium | Reads may be low/medium; writes/deletes require confirmation or Guardian policy. | Yes | Sparkbot, Arc, optional SparkPit web | Memory writes/deletes need privacy class and audit lineage. |
| files | `backend/app/api/routes/chat/tools.py`, `backend/app/api/routes/chat/uploads.py`, `backend/skills/microsoft_graph.py`, `backend/skills/knowledge_base.py` | `drive_search`, `drive_get_file`, `drive_create_folder`, `onedrive_list`, `onedrive_read`, uploads, knowledge document ingestion/deletion | Drive/OneDrive/document operations and upload handling. | high | Reads may be medium; writes/deletes require approval policy. | Yes | Sparkbot, Arc | Separate read-only file inspection from mutation/destructive operations. |
| browser | `backend/app/api/routes/chat/tools.py` | `browser_open`, `browser_navigate`, `browser_snapshot`, `browser_fill_field`, `browser_click`, `browser_close`, `browser_save_session`, `browser_restore_session`, `browser_list_sessions` | Browser sessions, page inspection, form fill, click, session persistence. | high | Snapshot/read may be medium; clicks/forms/session writes require confirmation. | Yes | Sparkbot, Arc optional, research shells | Browser pack must distinguish page read from state-changing UI actions. |
| network | `backend/app/api/routes/chat/tools.py`, `backend/skills/*` | `web_search`, `fetch_url`, `crypto_price`, `currency_convert`, `get_weather`, `stock_quote`, `stock_history`, `news_headlines`, `youtube_transcript`, `youtube_summarize`, `spotify_search`, `spotify_play`, `spotify_pause`, `spotify_next`, `spotify_previous`, `spotify_now_playing`, `spotify_volume`, external API-backed skills | External requests and web/API lookups. | medium/high | Read-only lookups may be policy-allowed; external API calls and playback mutation need risk policy. | Yes | Sparkbot, Arc, SparkPit web, research shells | Network tools should carry destination/target refs and prevent fallback to broad outbound access. |
| comms | `backend/app/api/routes/chat/tools.py`, `backend/app/services/*_bridge.py`, `backend/skills/microsoft_graph.py`, `backend/skills/proactive_alerts.py`, `backend/skills/contacts.py` | `slack_send_message`, `slack_list_channels`, `slack_get_channel_history`, `gmail_fetch_inbox`, `gmail_search`, `gmail_get_message`, `gmail_send`, `email_fetch_inbox`, `email_search`, `email_send`, `outlook_read_mail`, `outlook_send_mail`, `telegram_test_connection`, `send_alert`, `contacts_search`, `contacts_add`, `contacts_update`, `contacts_delete`, `contacts_sync_google` | External messaging, mail, contact, notification, and bridge surfaces. | high | External sends and contact mutation require explicit confirmation or Guardian approval. | Yes | Sparkbot, Arc, optional SparkPit web | Sending or mutating contacts must not execute from model-generated tool calls alone. |
| calendar | `backend/app/api/routes/chat/tools.py`, `backend/skills/calendar_*.py`, `backend/skills/microsoft_graph.py` | `calendar_list_events`, `calendar_create_event`, `outlook_calendar_list`, `outlook_calendar_create` | Calendar read/write and scheduling. | medium/high | Reads may be medium; event creation requires confirmation. | Yes | Sparkbot, Arc | Calendar writes should be separate from general comms and carry attendee/time evidence. |
| meeting | `backend/app/api/routes/chat/rooms.py`, `backend/app/services/guardian/meeting_*`, `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/lib/workstationMeeting.ts`, `docs/architecture/roundtable_meeting_flow_v1.6.60.md`, `backend/skills/time_tracking.py` | meeting manager, roundtable flow, meeting artifacts, meeting heartbeat/recorder, `morning_briefing`, `create_task`, `list_tasks`, `complete_task`, `set_reminder`, `list_reminders`, `cancel_reminder`, `guardian_schedule_task`, `guardian_list_tasks`, `guardian_list_runs`, `guardian_propose_improvement`, `guardian_list_improvements`, `guardian_run_task`, `guardian_pause_task`, `time_start`, `time_stop`, `time_log`, `time_report`, `time_status` | Meeting room workflow, summaries, artifacts, scheduled reminders, briefings, task/workflow scheduling, and time records. | medium/high | Artifact/status updates may require shell policy; scheduled execution inherits the target tool pack; external sends still use comms/calendar packs. | Yes for consequential tool-backed actions | Sparkbot, Arc | Meeting instructions may be `HumanInput` or system-service requests depending on source. |
| terminal | `backend/app/api/routes/chat/tools.py`, `backend/app/api/routes/terminal.py`, `backend/app/services/terminal_service.py`, `backend/skills/shell_run.py`, `backend/skills/run_code.py` | `terminal_list_sessions`, `terminal_send`, raw terminal HTTP/WebSocket routes, PTY session management, `shell_run`, `run_code` | Terminal/PTY/shell/code execution. | critical | Explicit human approval, operator PIN, or breakglass depending on policy. | Yes | Sparkbot private/operator shells only | Cannot be extracted until critical-risk GuardianDecision and selected_tools enforcement exist. |
| system | `backend/app/api/routes/chat/tools.py`, `backend/skills/system_diagnostics.py`, `backend/skills/apple_integrations.py`, scripts | `server_read_command`, `server_manage_service`, `ssh_read_command`, `system_diagnostics`, `apple_contacts_search`, `apple_reminders_list`, `apple_reminders_create`, `apple_notes_search`, `apple_notes_create`, setup/start scripts | Local/remote system diagnostics, service control, macOS local app control. | high/critical | Reads may be medium/high; service control and local writes require approval. | Yes | Sparkbot desktop/operator shell | Local-machine control must be shell-specific and denied by default elsewhere. |
| admin | `backend/app/api/routes/chat/guardian.py`, `backend/app/api/routes/chat/users.py`, `backend/app/api/routes/login.py`, `backend/app/services/guardian/*`, `backend/app/api/routes/chat/tools.py` | `vault_list_secrets`, `vault_use_secret`, `vault_reveal_secret`, `vault_add_secret`, `vault_update_secret`, `vault_delete_secret`, Guardian breakglass, auth/operator controls, `guardian_simulate_policy`, user/admin routes | Vault, breakglass, operator auth, privileged policy/admin surfaces. | critical | Operator approval, PIN, or breakglass. | Yes | Sparkbot operator/admin only | Must not be ordinary tools; secret material must stay referenced/redacted. |
| deploy | `.github/workflows/*`, `scripts/build-desktop.sh`, `scripts/package-public-download.sh`, `package.json`, docs | `deploy-production.yml`, `deploy-staging.yml`, `desktop-release.yml`, `build-installer.yml`, `desktop:backend:build`, public download packaging | Build, release, deploy, package, installer, production/staging workflows. | critical | Breakglass/operator approval for production-affecting actions. | Yes before any future runtime toolization | Usually denied to shells by default | Current surfaces are CI/scripts, not chat tools; future runtime must not gain deploy pack by accident. |
| payments | repository-wide search | No direct Stripe/payment tool found; only generic references to payment readiness/status text. | Future billing/payment surface. | critical | Explicit approval, operator policy, and strong audit if added. | Yes | Denied by default | Keep empty pack denied by default until real billing/payment contracts exist. |
| robo | `backend/app/api/routes/chat/tools.py`, `backend/app/api/routes/chat/robotics.py`, `backend/app/services/lima_robotics_bridge.py`, `backend/app/services/mcp_registry.py` | `lima_robot_command`, robotics status/tools/command/emergency stop, MCP `server_status`, `observe`, `stop_navigation`, `relative_move`, `agent_send`, `lima.navigate`, `lima.stop`, `lima.replay_simulation` | Robo-OS bridge, robot MCP planning/calls, simulated or physical robot commands. | critical | Dry-run/simulation first; physical-world actions require explicit Guardian approval. | Yes | Robo-OS shell, Sparkbot only when explicitly enabled | Natural language must not parse directly into robot MCP execution after extraction. |
| sensors | `backend/app/services/lima_robotics_bridge.py`, `backend/app/api/routes/chat/robotics.py`, `backend/skills/audio_transcribe.py` | `observe`, `detect_object`-style MCP tools when available, robot status/telemetry, `transcribe_audio` | Sensor/status/telemetry/audio input surfaces. | medium/high | Read-only telemetry may be medium; microphones/cameras need privacy policy. | Yes | Robo-OS, Sparkbot voice | Sensor data needs privacy class and source confidence. |
| research | `backend/app/api/routes/chat/tools.py`, `backend/skills/news_headlines.py`, `backend/skills/youtube_summarize.py`, `backend/skills/linear_jira.py`, `backend/skills/stocks.py`, `backend/skills/nl_sql.py` | `web_search`, `fetch_url`, `notion_search`, `notion_get_page`, `notion_create_page`, `confluence_search`, `confluence_get_page`, `confluence_create_page`, `github_list_prs`, `github_get_pr`, `github_create_issue`, `github_get_ci_status`, `linear_list_issues`, `linear_create_issue`, `linear_update_issue`, `jira_list_issues`, `jira_create_issue`, `jira_add_comment`, `execute_sql`, `list_databases`, `describe_table`, `portfolio_add`, `portfolio_view`, `portfolio_remove`, market/news/youtube tools | Research, analysis, internal workspace reads, SQL read helpers, workspace issue/page mutation, and lightweight portfolio records. | medium/high | Private data/API access requires policy; external writes go to comms/files/admin as appropriate. | Yes | Sparkbot, Arc, SparkPit research | SQL/private workspace reads and workspace writes need clear target refs, data-class handling, and separate read/write risk. |
| moderation | `frontend`, `docs`, future SparkPit surfaces | No direct dedicated moderation tool found in inspected tool files. | Future SparkPit/community moderation. | high | Role-based Guardian approval. | Yes if added | SparkPit web only by role | Keep future-facing and denied by default until implemented. |
| unknown | `backend/app/services/skills.py`, `backend/app/api/routes/chat/tools.py`, `scripts/*`, `.github/workflows/*` | Dynamic `SPARKBOT_SKILLS_DIR`, `_register_extra()`, `execute_tool()` unknown fallback, scripts requiring individual review | Dynamic or unclassified capability surfaces. | unknown/critical by default | Denied until classified. | Yes if ever exposed | None by default | Unknown tools must be classified before extraction. |

## Pack Definitions

### core

Read-only/basic runtime tools such as date/time and local calculation. These are likely low-risk but still should be part of an audited shortlist when exposed to a model.

### model

Model selection, completion, planning, fallback, prompt-cache, model telemetry, Token Guardian routing, and tool-aware stream assembly. The model pack cannot be allowed to execute tools directly.

### memory

Memory read/write/retrieval, notes, project memory, relationship memory, knowledge ingestion, memo storage, reindexing, compaction, and deletion. Reads and writes must be separated by risk class.

### files

Filesystem-like read/write/upload/download, Google Drive, OneDrive, document operations, uploads, and file mutation. Destructive operations are critical even when the pack default is high.

### browser

Browser automation, page retrieval, web UI actions, form filling, clicking, session save/restore, and browser session listing. Browser reads and UI mutation need separate policy.

### network

HTTP/API calls, webhooks, external requests, web search, URL fetches, and network-bound operations. Destination and data class should be audit-visible.

### comms

Email, chat, messaging, contacts, notifications, Telegram, Slack, Gmail, Outlook, and external communication. Sending or mutating external data requires explicit confirmation or Guardian approval.

### calendar

Calendar reads/writes, event creation, scheduling, and attendee/time changes. Calendar writes require evidence such as title, start/end, timezone, attendees, and actor confirmation.

### meeting

Roundtable, meeting manager, meeting notes, room flow, meeting heartbeat/recorder, SparkBud-style meeting actions, reminders, and briefings. Meeting-origin instructions must be classified as human input or system-service requests.

### terminal

Terminal, PTY, shell, subprocess, and command execution. This pack is critical-risk and denied by default outside private/operator shells.

### system

Local runtime/system controls, service controls, workstation controls, SSH reads, system diagnostics, macOS app integrations, and setup/start scripts. System writes or service management are critical.

### admin

Privileged admin routes, operator controls, user/account management, Guardian policy surfaces, vault, auth, breakglass, and security-sensitive state changes.

### deploy

Build, release, deploy, package, update, public download packaging, desktop release, staging deploy, production deploy, and production-affecting commands.

### payments

Stripe, billing, checkout, payment actions, and future payment controls. No direct payment tool was observed in the inspected Sparkbot tool files; this pack remains denied by default.

### robo

Robo-OS bridge, robot commands, movement/manipulation, emergency stop, and MCP robot command planning. Physical-world action is critical risk.

### sensors

Robot/device sensors, camera/microphone/telemetry inputs, audio transcription, robot status, and observe/detect/report status operations.

### research

Research workspace, web research, project/workspace reads, GitHub/Notion/Confluence reads, issue tracking reads, SQL read helpers, market/news/video lookups, and bounty/research flows.

### moderation

SparkPit/community moderation/admin surfaces if present or future-facing. No dedicated moderation tool was observed in the current Sparkbot tool catalogue.

### unknown

Anything that could not yet be confidently classified, including dynamic skill modules from `SPARKBOT_SKILLS_DIR`, script surfaces that may become tools later, and fallback names accepted by a dispatcher.

## Default Risk Posture

LOW:

- core read-only
- read-only memory retrieval
- status/health checks

MEDIUM:

- drafts
- non-public planning
- local note creation
- safe read-only browser research

HIGH:

- file modification
- external comms
- calendar modification
- network/API calls
- private data access
- memory writes
- admin reads
- costly model usage

CRITICAL:

- terminal/PTY/shell
- deploys
- payments
- secret/vault access
- admin writes
- destructive file operations
- credential/security changes
- robot movement/manipulation
- physical-world actions

## Shell Allowance Draft

| Shell | Default packs | Optional packs | Critical packs | Explicitly denied by default | Notes |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | core, model, memory, meeting | files, browser, network, comms, calendar, research, system read-only | terminal, admin, deploy, payments, robo, destructive files, vault | payments, deploy, robo unless explicitly enabled | Sparkbot is the parity shell but must not receive the full catalogue after extraction. |
| Arc / LIMA AI Office | core, model, memory, comms, calendar, files | browser, network, research, meeting | admin, payments, destructive files | terminal, deploy, robo | Office shell should prioritize work/comms/calendar/files without raw local execution by default. |
| SparkPit web | core, model, research, moderation depending on role | comms, network | admin, payments, deploy | terminal, local files, deploy, robo | Community and web admin surfaces must be role-scoped. |
| Robo-OS | core, sensors | robo, network | robo movement/manipulation, terminal, admin | payments, deploy unless explicitly enabled | Robot shell must separate sensor/read-only state from motion/manipulation. |
| Future humanoid / worker robot | core, sensors, task context | robo, comms | movement, manipulation, tools, doors, vehicles, hazardous workplace actions | payments, deploy, broad admin, unrestricted network | Physical safety policy must be explicit before action. |

## Full-Catalogue Exposure Risks

- `stream_chat_with_tools()` must not receive the full catalogue after extraction.
- Tool selection must be narrowed before model calls.
- Model-generated tool calls must not execute without `GuardianDecision`.
- Terminal/admin/robot/payment/deploy tools must never be exposed by default.
- Tool fallback must never expand to full catalogue.
- Pack expansion must require a new `GuardianDecision` or constrained approval.
- Dynamic skill registration must not silently add tools to an existing model context.
- Static tools and dynamic skills overlap in names, so extraction must deduplicate by pack and risk policy, not by list order alone.

## GuardianDecision Pack Constraints

`GuardianDecision.allowed_tool_packs` must constrain:

- `ToolExposureRequest.requested_packs`
- `ToolExposureDecision.allowed_packs`
- Harness `ModelRequest.selected_tools`
- actual tool execution

If `GuardianDecision` denies a pack, no downstream component may re-add it.

Pack expansion is a new authorization question. A decision that allows `core` and `memory` cannot be reused to expose `terminal`, `admin`, `browser`, `network`, `payments`, `deploy`, or `robo`.

## Audit Requirements

Future audit events must record:

- `shell_id`
- `actor_id`
- `input_id` if available
- `intent_id`
- `decision_id`
- requested packs
- allowed packs
- denied packs
- selected tools
- executed tool
- risk class
- policy version
- result
- timestamp

## Extraction Blockers

- `backend/app/api/routes/chat/tools.py` centralizes 71 static tool names in a broad catalogue.
- `backend/skills/` dynamically loads 66 skill tool names, including extra names from `_register_extra()`.
- `stream_chat_with_tools()` still couples raw chat, model routing, tool selection, Guardian policy, and execution closely.
- Static tools and skill tools overlap in names, especially calendar tools.
- Terminal actions sit close to chat and Workstation paths.
- Browser/file/network/comms tools have mixed read/write risk in the same catalogue.
- Current tools do not carry LIMA `decision_id` through a common contract.
- No `selected_tools` audit record exists yet.
- Broad catalogue fallback and unknown dynamic skills remain extraction risks.
- Payment tools were not found, but payment references exist in readiness/docs; future payment surfaces must remain denied by default until classified.

## Recommended Next Step

Recommended next branch: `phase-0-10-tool-pack-risk-policy`.

Goal: define default approval/risk policy for each pack before any runtime enforcement.

## Phase 0.10 Follow-Up

This inventory is not enforcement. Pack classifications must be paired with risk/approval policy before extraction.
