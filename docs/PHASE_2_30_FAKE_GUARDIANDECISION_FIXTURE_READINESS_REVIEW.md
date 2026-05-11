# Phase 2.30 Fake GuardianDecision Fixture Readiness Review

## Purpose

Review whether the Phase 2.29 fake GuardianDecision fixtures are ready for a future test-only fake GuardianDecision fixture harness.

This review does not create real GuardianDecision.
This review does not enforce policy.
This review does not approve actions.
This review does not execute tools.
This review does not persist audit data.

## Tag / Milestone Check

Actual Phase 2.29 tag found:

- `phase-2.29-fake-guardiandecision-test-fixtures`

Expected:

`phase-2.29-fake-guardiandecision-test-fixtures`

No malformed duplicate Phase 2.29 tag was found by `git tag --list "phase-2.29*"`.

## Current Fixture Inventory

| Fixture file | Fixture purpose | Expected status | Safety notes | Non-authorizing posture |
| --- | --- | --- | --- | --- |
| `allow_test_only_decision_fixtures.json` | Represents low-risk informational, draft-only, and planning-only fake decision shapes. | `allow_test_only` | Low-risk examples still carry no execution and no approval metadata. | `allow_test_only` is fake/test-only and not production authorization. |
| `deny_test_only_decision_fixtures.json` | Represents malformed, missing context, disallowed pack, and unknown action shapes. | `deny_test_only` | Denied shapes remain non-executable and do not persist audit. | Deny fixtures are fake decision shapes only. |
| `needs_approval_test_only_decision_fixtures.json` | Represents email send, payment, deploy, admin, and secret access shapes that require later approval. | `needs_approval_test_only` | `approval_ref` is reference-only and does not create ApprovalMetadata. | `requires_approval` is not approval granted. |
| `blocked_test_only_decision_fixtures.json` | Represents unsafe robot, destructive filesystem, terminal, and human safety/law block shapes. | `blocked_test_only` | Safety flags are present and owner autonomy cannot override safety/law. | Blocked fixtures do not execute and do not authorize production action. |
| `safety_critical_decision_fixtures.json` | Represents robot, terminal/PTY, secret, and destructive admin safety-critical shapes. | `needs_approval_test_only` or `blocked_test_only` | Safety-critical fixtures do not auto-approve and require later Guardian/policy/approval review. | Safety-critical fake decisions are not approval. |
| `expired_revoked_superseded_decision_fixtures.json` | Represents expired, revoked, and superseded fake decision lifecycle shapes. | `expired_test_only`, `revoked_test_only`, `superseded_test_only` | Lifecycle fixtures are not executable; supersedes references are reference-only. | Expired/revoked/superseded fixtures are not production authorization. |

## What The Fixtures Prove

- fake decision shapes can be represented
- statuses are clearly test-only
- `allow_test_only` is not production authorization
- deny/blocked/expired/revoked/superseded cases are represented
- needs_approval cases are represented
- `approval_ref` remains reference-only
- no ApprovalMetadata is created
- safety-critical cases do not auto-approve
- fake decisions do not execute
- fake decisions do not persist audit

## What The Fixtures Do Not Prove

- real GuardianDecision behavior
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution safety
- model call safety
- audit persistence
- redaction runtime
- production Guardian behavior
- production Sparkbot behavior

## Fixture Coverage Assessment

| Category | Covered? | Risk class | Gap | Recommendation |
| --- | --- | --- | --- | --- |
| `allow_test_only` | yes | low | No runtime interpretation exists. | Keep fake-only and validate status/metadata in Phase 2.31. |
| `deny_test_only` | yes | blocked | No harness summary exists yet. | Add test-only harness reporting in Phase 2.31. |
| `needs_approval_test_only` | yes | high/critical | No approval recording exists, by design. | Preserve `approval_ref` as reference-only. |
| `blocked_test_only` | yes | critical/safety_critical | No production block enforcement exists, by design. | Validate blocked posture without enforcement. |
| `needs_review_test_only` | no | mixed | Status is reserved in tests but no fixture currently exercises it. | Consider adding explicit needs-review fixture before or during harness work if needed. |
| `expired_test_only` | yes | low | No audit persistence exists, by design. | Report lifecycle status only. |
| `revoked_test_only` | yes | medium | No audit persistence exists, by design. | Report lifecycle status only. |
| `superseded_test_only` | yes | medium | Supersedes ref is reference-only. | Validate reference-only semantics. |
| safety-critical robot/terminal/secret/payment/deploy/admin/destructive | yes | critical/safety_critical | Coverage is split across needs-approval, blocked, and safety-critical files. | Harness should aggregate safety-critical coverage. |
| `approval_ref` reference-only | yes | high/critical | No ApprovalMetadata is created. | Harness must reject ApprovalMetadata payloads. |
| owner autonomy not override | yes | critical/safety_critical | Owner autonomy is represented as no-override metadata only. | Harness must keep autonomy passive. |
| tool packs not granted | yes | low/high/critical | Tool packs are refs only. | Harness must reject granted/allowed executable tool-pack semantics. |

## Readiness Decision

GO for Phase 2.31 Fake GuardianDecision Fixture Harness.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.

## Recommended Next Branch

Recommend:

`phase-2-31-fake-guardiandecision-fixture-harness`

Purpose:

Create a test-only harness that validates fake GuardianDecision fixtures against expected fake decision shapes.

Allowed:

- test-only helper
- fixtures only
- fake/test-only decision shape validation
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- no policy evaluation
- no approval recording

## Future Harness Rules

The Phase 2.31 harness may:

- load fake GuardianDecision fixture files
- validate required fake decision fields
- validate `decision_status` is test-only
- report allow/deny/needs_approval/blocked/safety_critical/expired/revoked/superseded statuses

The Phase 2.31 harness must not:

- create real GuardianDecision
- enforce policy
- record ApprovalMetadata
- approve actions
- execute tools
- persist audit data
- call models
- call Sparkbot

## Still Blocked

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- redaction runtime

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| fake GuardianDecision mistaken for production authorization | High | Fixtures use fake IDs, fake-only metadata, and test-only statuses. | Harness must validate fake-only posture and remain under test paths. |
| `allow_test_only` mistaken for production allow | High | Fixtures and docs say `allow_test_only` is not production authorization. | Harness must report `allow_test_only` separately from production allow. |
| `approval_ref` mistaken for ApprovalMetadata | High | Fixtures mark `approval_ref` as reference-only and tests reject ApprovalMetadata keys. | Harness must reject approval metadata payloads. |
| `requires_approval` mistaken for approval granted | High | Fixtures keep `allow` false for approval-required cases and do not include `approval_granted`. | Harness must distinguish required approval from granted approval. |
| safety-critical fake decision auto-approved | Critical | Safety-critical fixtures set `allow` false and `no_auto_approval` true. | Harness must require safety-critical non-allow posture. |
| fake harness mistaken for real Guardian | High | This review limits Phase 2.31 to test-only validation. | Harness docs and helper path must remain test-only. |
| audit persistence added too early | High | Fixtures only include `no_audit_persistence` metadata. | Harness must not write audit records or persistence artifacts. |
| production enforcement added too early | Critical | Real GuardianDecision, enforcement, approval, execution, and persistence remain blocked. | Keep Phase 2.31 validation-only. |

## Final Decision

GO for Phase 2.31 Fake GuardianDecision Fixture Harness.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.
