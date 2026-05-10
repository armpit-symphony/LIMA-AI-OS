# Phase 1.22 Payload Drift Check Contract

## Purpose

Define the review contract for detecting drift between LIMA-owned Sparkbot payload fixtures and Sparkbot origin/main.

This does not import Sparkbot.
This does not wire routes.
This does not execute code.
This does not make fixtures runtime authority.

## Sparkbot Reference Check

| Repo | Branch | Commit | Local status | Adapter-relevant changes since fixture commit |
| --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `4da833858428e076645cac8fca942205e80bcc6e` | Clean at review time | Sparkbot moved from `f7d5ee2054794ea7156ffb51a009c058cb7757e6` to v1.6.71. Changed files include `backend/app/api/routes/chat/rooms.py`, `backend/app/api/routes/chat/spine.py`, Guardian correction/improvement files, frontend Spine routes, docs, package metadata, and release notes. `StreamMessageRequest`, MCP request, robotics request, and terminal session request shapes were checked through `git show origin/main:path`; no fixture shape update was required in this phase. |

## Drift Check Rule

Before any real Sparkbot adapter work:

- fetch Sparkbot origin/main
- record commit
- ignore dirty local worktree files unless explicitly reviewing them
- compare adapter-relevant surfaces against fixture metadata
- update fixture mirrors if payload shape changed
- keep production adapter blocked until drift review passes

## Adapter-Relevant Surfaces

- chat input
- WebSocket message input
- voice/transcript input
- meeting/roundtable prompt input
- SparkBud/workstation prompt input
- operator/terminal request input
- MCP explain-plan/run approval input
- robotics natural-language request input
- frontend chat input shape
- auth/session/user context only as passive refs

## Fixture Metadata Requirements

Every fixture object must include:

- `fixture_id`
- `source_surface`
- `sparkbot_reference_path`
- `inspected_commit`
- `payload`
- `expected_humaninput_source`
- `privacy_class`
- `redaction_class`
- `notes`

Every fixture object should also include drift metadata:

- `shape_version`
- `reviewed_at`
- `reviewed_against`
- `drift_status`
- `drift_notes`

`drift_status` values:

- `current`
- `needs_review`
- `stale`
- `unknown`

## Dirty Worktree Rule

If Sparkbot local checkout is dirty, do not use local files as source of truth.

Use:

- origin/main
- `git show origin/main:path`
- explicit commit hash
- clean temporary checkout

Dirty local files can be noted but cannot update fixtures unless deliberately reviewed and committed upstream.

## Drift Decision Outcomes

- `no_drift`
- `fixture_update_required`
- `sparkbot_changed_not_adapter_relevant`
- `review_blocked_dirty_source`
- `unknown`

## What Drift Check Does Not Do

- does not import Sparkbot
- does not execute Sparkbot
- does not verify runtime behavior
- does not authorize production adapter
- does not prove identity/session/auth safety
- does not prove model/tool execution safety

## Contract Types

Phase 1.22 adds describe-only drift contracts:

- `DriftStatus`
- `DriftDecision`
- `PayloadFixtureDriftRecord`
- `PayloadDriftReview`
- `PayloadDriftReviewProtocol`

These contracts describe review evidence only. They do not fetch Sparkbot, compare live files, mutate fixtures, execute code, wire routes, or authorize production adapter work.

## Acceptance Criteria

- drift contract doc exists
- fixture metadata requirements include drift fields
- dirty worktree rule exists
- production adapter remains blocked
- tests validate fixture metadata shape
- no Sparkbot imports
- no runtime behavior
