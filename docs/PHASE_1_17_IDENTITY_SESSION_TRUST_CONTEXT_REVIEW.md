# Phase 1.17 Identity / Session / Trust Context Mapping Review

## Purpose

Review how LIMA should map identity, session, trust context, and owner-autonomy metadata before any real Sparkbot adapter implementation.

This review does not implement auth.
This review does not verify sessions.
This review does not enforce trusted devices.
This review does not enforce autonomy.
This review does not modify Sparkbot.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked paths/surfaces | Modified? yes/no | Identity/session/trust relevant changes |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `da9506151f7c45910ddf4788ed50dd989b668c4c` | User/session/auth models and routes; `ChatUser` / `user_id` / `room_id` usage; chat REST/WebSocket/voice/meeting/workstation surfaces; Guardian auth, breakglass, operator, vault, memory, pending approval, policy, and token-guardian surfaces; frontend login/session/hooks/chat/workstation/meeting/command-center/spine context; docs/capabilities and roundtable meeting docs. Representative paths include `backend/app/models.py`, `backend/app/api/deps.py`, `backend/app/api/routes/login.py`, `backend/app/api/routes/users.py`, `backend/app/api/routes/chat/users.py`, `backend/app/api/routes/chat/messages.py`, `backend/app/api/routes/chat/websocket.py`, `backend/app/api/routes/chat/voice.py`, `backend/app/api/routes/chat/rooms.py`, `backend/app/api/routes/chat/workstation.py`, `backend/app/api/routes/chat/guardian.py`, `backend/app/services/guardian/auth.py`, `backend/app/services/guardian/pending_approvals.py`, `backend/app/services/guardian/memory.py`, `frontend/src/hooks/useAuth.ts`, `frontend/src/lib/localSession.ts`, `frontend/src/lib/chat/websocket.ts`, `frontend/src/pages/ChatPage.tsx`, `frontend/src/pages/WorkstationPage.tsx`, `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/routes/login.tsx`, `frontend/src/routes/_layout/spine.tsx`, `docs/capabilities.md`, and `docs/architecture/roundtable_meeting_flow_v1.6.60.md`. | No | No movement since the Phase 1.16 check. `origin/main` remains at `da9506151f7c45910ddf4788ed50dd989b668c4c`; `git diff da9506151f7c45910ddf4788ed50dd989b668c4c..origin/main` is empty. Existing identity/session/auth and adapter-relevant surfaces remain active reference material, not implementation material. |

Sparkbot was fetched read-only. The local Sparkbot checkout remained on `main`, tracking `origin/main`, with no modified files reported.

## Current Metadata Status

`actor_ref`:

- passive reference only
- not verified identity

`session_ref`:

- passive reference only
- not verified session

`trusted_context_ref`:

- passive reference only
- not trusted device proof

`autonomy_notes`:

- passive notes only
- not autonomy enforcement
- not approval
- not risk reduction

privacy metadata:

- classification hint only
- not redaction enforcement

## Future Mapping Targets

`AuthActor`:

- verified or described actor identity

`AuthContext`:

- actor plus session plus shell plus auth level

`TrustedDeviceContext`:

- future trusted device/session context

`IdentityConfidence`:

- confidence score and evidence for identity/session/trust

`OwnerAutonomyProfile`:

- owner-defined autonomy rules

`CapabilityRule`:

- what actions are allowed, confirmed, PIN, breakglass, or never allowed

`ApprovalMetadata`:

- explicit approval evidence when required

`GuardianDecision`:

- final decision gate

## Proposed Identity Mapping

Sparkbot source:

- user id / actor id / `ChatUser` / current user equivalent

LIMA:

- `actor_ref` in payload
- later `AuthActor.actor_id`
- later `AuthContext.actor`

Rules:

- adapter skeleton may carry `actor_ref`
- real adapter must not treat `actor_ref` as verified auth without `AuthContext`
- `actor_ref` alone cannot approve anything
- unknown actor escalates or denies depending policy

## Proposed Session Mapping

Design:

- `session_ref` from request, WebSocket, meeting, or Workstation context
- later maps to `AuthContext.session_id`
- session must have expiry and scope
- session alone cannot approve high/critical actions
- unknown or expired session escalates

## Proposed Trusted Device Mapping

Future `TrustedDeviceContext` fields:

- `trusted_context_id`
- `device_ref`
- `session_ref`
- `actor_ref`
- `trust_level`
- `confidence`
- `last_verified_at`
- `expires_at`
- `signals`
- `anomaly_flags`
- `metadata`

Rules:

- trusted devices reduce friction only inside owner policy
- trusted devices never bypass law/human safety
- unknown devices cannot approve critical actions
- suspicious context escalates
- `trusted_context_ref` is only a pointer until verified

## Proposed Identity Confidence Mapping

Future `IdentityConfidence` fields:

- `confidence_id`
- `actor_ref`
- `session_ref`
- `trusted_context_ref`
- `confidence_score`
- `factors`
- `required_threshold`
- `passed`
- `expires_at`
- `metadata`

Factors may include:

- known device
- login session
- voice match
- face match
- operator PIN
- hardware key
- location/context
- behavior pattern
- future biometric/BCI signal

BCI/thought-adjacent:

- biometric
- confirm-only
- cannot directly approve execution
- cannot control tools/drivers/robots
- cannot bypass Guardian

## Owner Autonomy Mapping

- `autonomy_notes` remain passive metadata in the adapter skeleton
- future `OwnerAutonomyProfile` must be explicit and reviewed
- autonomy does not replace `GuardianDecision`
- autonomy cannot reduce risk alone
- autonomy cannot override law/human safety
- autonomy cannot grant critical physical, destructive, or secret action without policy

## Risk and Escalation Rules

- `actor_ref` without `AuthContext`: not trusted
- `session_ref` without validation: not trusted
- `trusted_context_ref` without verification: not trusted
- `autonomy_notes` without `OwnerAutonomyProfile`: no authority
- missing identity/session: escalate or deny for high/critical
- low-risk actions may proceed only when policy allows
- critical actions require stronger verification later

## Phase 1.18 Recommendation

Recommended next branch:

`phase-1-18-authcontext-trust-contract-extension`

Goal:
Add contract-level types for `TrustedDeviceContext` and `IdentityConfidence`, and possibly extend adapter metadata contracts to reference them.

Still no runtime auth.

## Still Blocked

- production Sparkbot adapter
- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- PIN verification
- face/voice recognition implementation
- real `OwnerAutonomyProfile` enforcement
- model/tool execution
- terminal/PTY
- Robo-OS physical action
- audit persistence
- redaction runtime
- `stream_chat_with_tools`
- raw chat-to-tool shortcut

## Acceptance Criteria

- identity/session/trust mapping review exists
- Sparkbot origin/main rechecked
- `actor_ref`/`session_ref`/`trusted_context_ref`/`autonomy_notes` remain passive
- future `AuthContext` mapping is proposed
- future `TrustedDeviceContext` mapping is proposed
- future `IdentityConfidence` mapping is proposed
- next contract extension phase identified
- no runtime implementation added
