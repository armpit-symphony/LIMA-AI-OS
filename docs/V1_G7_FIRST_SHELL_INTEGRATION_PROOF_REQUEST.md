# V1-G7 First-Shell Integration Proof Request

This document requests first-shell integration proof packets for V1 readiness gap `V1-G7`.

It is a request only. It does not approve LIMA runtime behavior, shell wiring, provider/model calls, runtime `GuardianDecision` creation, approval enforcement, persistence, haptic device behavior, file mutation, browser/network behavior, robotics, physical-world behavior, runtime export cleanup, final API freeze, or production readiness.

## Request Target

- V1 gap: `V1-G7`
- Gap name: first-shell integration proof
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Gap matrix: `docs/V1_READINESS_GAP_MATRIX.md`
- Base completed gap: `V1-G6` haptic intent metadata contract
- Requested consumer repos:
  - `Sparkbot_shell`
  - `Sparkbot`
  - `Arc-Bot-shell`

## Requested Proof Branches

Each first shell should provide its own proof branch:

| Shell repo | Requested branch |
| --- | --- |
| `Sparkbot_shell` | `v1-g7-sparkbot-shell-integration-proof-packet` |
| `Sparkbot` | `v1-g7-sparkbot-integration-proof-packet` |
| `Arc-Bot-shell` | `v1-g7-arc-bot-shell-integration-proof-packet` |

## Existing Local Evidence Snapshot

Local read-only shell evidence exists, but it is not a complete V1-G7 proof set:

- `Sparkbot_shell` has earlier thinking and UX-state proof packet material.
- `Sparkbot` has behavior-reference docs for approvals, Guardian posture, provider/model routing, memory/audit posture, and public capability boundaries.
- `Arc-Bot-shell` has static LIMA/office consumer proof material and readiness/audit docs.

These references can inform V1-G7 packets. They do not replace the requested uniform proof packet for each shell.

## Why This Is Needed

V1 product readiness requires more than LIMA-owned static contracts. The first shells must prove they can safely consume or align with LIMA contract outputs without creating unsafe shortcuts.

V1-G7 should prove shell compatibility posture for:

- shell response states and packet/kernel status mapping
- haptic intent metadata ownership
- operator approval for destructive edit/delete behavior
- `GuardianDecision` authority boundaries
- provider/model routing constraints
- audit/evidence lineage expectations
- tool-pack and connector scope
- file/browser/network/device/robotics/physical-world boundaries
- no raw natural-language-to-tool execution shortcut

## Requested Files Per Shell

Each shell should provide at least:

- `docs/proof_packets/<SHELL>_LIMA_V1_G7_INTEGRATION_PROOF_PACKET.md`
- `docs/audits/<SHELL>_LIMA_V1_G7_INTEGRATION_PROOF_AUDIT.md`
- `tests/fixtures/<shell>_lima_v1_g7_integration_proof_packet.json`
- `tests/test_<shell>_lima_v1_g7_integration_proof_packet.py`

If a shell does not use a `tests/` directory today, it may place static validation in the nearest existing test or validation location, but the packet must state the path and command clearly.

## Required Evidence

Each shell proof packet must show:

- shell repo name, branch, commit, and validation commands
- whether the shell can consume or render LIMA contract outputs as static/local evidence
- whether the shell has any live LIMA runtime wiring
- shell response-state coverage for `received`, `thinking`, `preview_ready`, `blocked`, `needs_approval`, `completed`, `failed_safe`, and `deferred`
- kernel-status to packet-status mapping for `proposed -> preview_only`, `needs_review -> explain_plan`, and `blocked -> blocked`
- haptic intent ownership: LIMA metadata only, shell/device rendering shell-owned
- whether device haptic behavior is implemented, and if so, that it is shell-owned
- operator approval posture for deleting or editing anything
- whether approval is real enforcement, preview-only, docs-only, or missing
- whether real `GuardianDecision` authority exists, is preview-only, or is missing
- whether provider/model routing exists, and whether routes are Guardian/scope/secret/budget/audit constrained
- whether audit/evidence lineage exists, is durable, is static-only, or is missing
- whether connector, file, browser, network, device, robotics, and physical-world behaviors are absent, preview-only, or runtime-enabled
- explicit statement that no LIMA runtime behavior was added by the proof branch
- explicit statement that no Sparkbot/Sparkbot_shell/Arc-Bot-shell code was copied into LIMA

## Required Machine-Readable Fields

Each shell fixture should include:

- `proof_gap_id`: `V1-G7`
- `shell_repo`
- `proof_branch`
- `proof_commit`
- `proof_packet_files`
- `validation_commands`
- `validation_results`
- `can_consume_lima_contract_outputs_as_static_evidence`
- `can_consume_lima_runtime_outputs_live`
- `lima_runtime_wiring_added`
- `lima_runtime_behavior_added`
- `runtime_exports_required_from_lima`
- `runtime_exports_changed_in_lima`
- `shell_response_states_evaluated`
- `source_backed_shell_response_states`
- `docs_fixture_only_shell_response_states`
- `missing_shell_response_states`
- `kernel_status_mappings`
- `packet_statuses`
- `haptic_intent_metadata_supported`
- `shell_owns_haptics`
- `lima_owns_haptic_device_behavior`: false
- `haptic_device_behavior_added`
- `destructive_edit_delete_requires_operator_approval`
- `approval_enforcement_status`
- `guardian_decision_status`
- `provider_model_routing_status`
- `audit_evidence_status`
- `tool_pack_scope_status`
- `connector_file_browser_network_device_robotics_status`
- `raw_natural_language_to_tool_execution_allowed`: false
- `sparkbot_code_copied_to_lima`: false
- `sparkbot_imported_by_lima`: false
- `lima_imported_by_shell_runtime`
- `production_readiness_claimed`: false
- `v1_product_readiness_claimed`: false
- `accepted_as_static_shell_evidence`
- `accepted_as_live_runtime_parity`: false
- `blockers`
- `recommended_next_step`

## Required Validation Commands

Each shell should run its normal static validation plus the proof packet test. At minimum:

- Python projects: `python3 --version || python --version`
- Python proof tests: `python3 -m pytest -q || python -m pytest -q`
- Node/frontend projects: existing build/test command, such as `npm run build`, `npm test`, or the repo's documented equivalent
- Whitespace: `git diff --check`

The proof packet must record exact command output summaries, including failures and known environment warnings.

## Acceptance Criteria

LIMA can accept a shell packet as static integration evidence only if:

- the packet names concrete shell source or contract files
- the packet evaluates every required shell response state
- the packet evaluates packet/kernel status mappings
- haptics remain shell-owned and LIMA device-haptic ownership is false
- destructive edit/delete behavior requires operator approval or is explicitly blocked
- any approval, GuardianDecision, provider/model routing, connector, file, browser, network, device, robotics, or physical-world behavior is truthfully classified as runtime, preview-only, docs-only, or missing
- the shell does not claim LIMA runtime parity without runtime evidence
- the proof branch does not add LIMA runtime behavior
- the proof branch does not require unapproved LIMA runtime export cleanup or final API freeze
- validation commands pass or failures are documented for LIMA audit

## Rejection Criteria

LIMA should reject or return a shell packet for clarification if:

- a required shell response state is omitted
- packet/kernel status mappings are missing
- haptics are claimed as LIMA-owned device behavior
- destructive edit/delete can bypass operator approval
- the shell claims real approval enforcement without source-backed proof
- the shell claims real `GuardianDecision` authority without source-backed proof
- provider/model routing claims omit Guardian, shell scope, secret, budget, privacy, or audit constraints
- raw natural language can execute tools directly
- connector/file/browser/network/device/robotics/physical-world behavior is claimed without Guardian/action boundaries
- the packet claims V1 product readiness or production readiness from static evidence alone
- the packet requires unapproved LIMA runtime wiring, export cleanup, or final freeze

## LIMA Boundary

This request keeps LIMA in docs/tests/fixtures-only status for `V1-G7`.

LIMA will intake future shell packets as evidence only. It will not wire shell repos, import shell runtime code, copy Sparkbot code, change runtime exports, approve runtime implementation, approve final API freeze, or claim V1 readiness from this request.

## Recommended Next Step

Ask `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell` to create the requested proof branches and deliver proof packets. After delivery, LIMA should create separate intake/audit lanes for each shell packet, then a consolidated V1-G7 closeout.
