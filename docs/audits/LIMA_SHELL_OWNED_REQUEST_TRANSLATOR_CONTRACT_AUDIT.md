# LIMA Shell-Owned Request Translator Contract Audit

## Branch

`audit-lima-shell-owned-request-translator-contract`

## Base Commit

`fd3941dd2724e9093e555900a5c2bba252a5c71d`

## Audit Scope

This independent audit reviews the design-only shell-owned request translator contract before any translator fixture implementation begins.

This audit branch does not implement behavior. It does not modify `lima/`, tests, fixtures, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Audit Verdict

PASS.

The contract is safe to proceed to a synthetic fixture-only implementation lane:

`implement-lima-shell-owned-translator-fixtures`

It is not ready for production translator code, public Sparkbot integration, Arc Bot integration, live HumanInput, raw text parsing in LIMA, runtime `IntentEnvelope` creation, real `GuardianDecision` authority, approval enforcement, model/provider calls, tool execution, persistence, connector access, live discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Scope and File Safety

The design branch added only:

- `docs/design/LIMA_SHELL_OWNED_REQUEST_TRANSLATOR_CONTRACT.md`
- `docs/audits/LIMA_SHELL_OWNED_REQUEST_TRANSLATOR_CONTRACT_READINESS_REVIEW.md`

Confirmed untouched by the design branch:

- `lima/`
- `tests/`
- `fixtures/`
- `examples/`
- `pyproject.toml`
- public Sparkbot repository
- Arc Bot repository surfaces
- provider/model implementation
- storage/persistence implementation
- live adapter implementation
- shell wiring
- connector behavior
- browser/network/file mutation surfaces
- scheduler/background worker surfaces
- Robo-OS/device/robot/drone/physical-world surfaces

Audit finding:

- PASS. The branch stayed docs-only and did not alter runtime behavior.

## 2. Shell Ownership Review

The contract states:

- Sparkbot owns Sparkbot UI/session/task context parsing.
- Arc owns Arc office workflow/session/task context parsing.
- LIMA receives already-normalized metadata.
- LIMA does not parse raw user text.
- LIMA does not import Sparkbot or Arc internals.

Audit finding:

- PASS. Translation ownership is correctly held by consuming shells.

## 3. Raw Input Boundary Review

The design blocks forwarding to LIMA:

- raw chat text
- raw prompt text
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- unsafe command bodies
- live device/network scan dumps
- robot/drone command payloads

Audit finding:

- PASS. LIMA remains a normalized metadata consumer, not a raw input parser.

## 4. Translator Input and Output Review

The proposed input shape captures shell-owned context and raw input state as metadata only.

The proposed output shape includes:

- `translation_state`
- `blocked_reason`
- redaction summary flags
- `normalized_request`

Only `normalized_request` is eligible to map into `KernelRequest`, and only when `translation_state == "translated"`.

Audit finding:

- PASS. The contract separates shell translation from LIMA evaluation.

## 5. Translation State Review

Allowed future states:

- `translated`
- `blocked`
- `needs_clarification`

The contract states none of these states authorize execution.

Audit finding:

- PASS. Translation states are non-executing.

## 6. Fail-Closed Rule Review

The translator must block on:

- raw forwarding requirements
- credentials
- unsafe payloads
- live connector access
- live network/device scans
- connection, pairing, or credential use
- model calls
- tool execution
- external sends
- file writes
- browser control
- process execution
- scheduler/background work
- device control
- robot/drone/physical-world behavior
- missing tenant/session/actor metadata
- missing or non-default-deny capability profiles
- missing source surface identity

Audit finding:

- PASS. The contract preserves fail-closed behavior.

## 7. Redaction Contract Review

Translator output must not contain:

- raw user text
- raw prompts
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- passwords
- tokens
- API keys
- headers
- cookies
- credential refs unless separately approved later
- pairing codes
- unsafe command payloads
- raw scan dumps
- raw IP/MAC/Bluetooth addresses
- device serial numbers
- precise physical location
- robot/drone command payloads

Audit finding:

- PASS. Redaction expectations are explicit enough for fixture tests.

## 8. Capability Profile Review

The translator output must default consequential capabilities to false:

- `model_calls`
- `memory_write`
- `task_state_write`
- `connector_read`
- `connector_write`
- `external_send`
- `file_write`
- `process_execute`
- `browser_control`
- `device_control`
- `robotics_actuation`
- `drone_actuation`
- `scheduler_run`
- `connection_attempt`
- `device_pairing`
- `credential_use`
- `iot_control`
- `physical_world_actuation`

Audit finding:

- PASS. Capability profiles remain default-deny.

## 9. Mapping Review

The design maps `normalized_request` into current `KernelRequest` fields:

- `request_id`
- `shell_id`
- `actor_id`
- `session_id`
- `normalized_intent`
- `capability_profile`
- `actor_context`
- `shell_context`
- `session_context`
- `memory_refs`
- `source_surface`
- `metadata`

The mapping is explicitly test-only in the first implementation lane.

Audit finding:

- PASS. The future fixture branch can validate mapping without adding runtime translator behavior.

## 10. Sparkbot and Arc Boundary Review

The design does not authorize touching public Sparkbot or Arc repositories.

It explicitly says future Sparkbot/Arc translator work must happen in repo-owned branches after LIMA contract audit and handoff.

Audit finding:

- PASS. Repo ownership remains clear.

## 11. Fixture Implementation Readiness

The next implementation-shaped branch may be:

`implement-lima-shell-owned-translator-fixtures`

That branch should be limited to:

- synthetic `ShellTranslatorInput` fixtures
- synthetic `ShellTranslatorOutput` fixtures
- tests validating translated outputs can map into `KernelRequest`
- tests proving blocked/needs-clarification outputs do not call `LimaKernel`
- tests that redaction flags remain safe
- an implementation audit report

Audit finding:

- PASS. The next lane is narrow and non-executing.

## 12. Forbidden Later Surfaces

The fixture branch must not add:

- production translator code
- public Sparkbot repo changes
- Arc Bot repo changes
- production shell wiring
- `lima/` runtime behavior
- provider/model calls
- storage/persistence
- real Guardian enforcement
- real approval enforcement
- live HumanInput bridge
- IntentEnvelope runtime creation
- live adapters
- tool execution
- connector access
- browser control
- file mutation
- network calls
- socket APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- scheduler/background workers
- subprocesses/threads
- device control
- robot/drone control
- physical-world behavior
- credentials or secret storage

Audit finding:

- PASS. Forbidden surfaces remain explicit.

## Handoff Notes for Sparkbot and Arc Teams

Archive-ready message:

- LIMA is preserving the shell-owned translator boundary.
- Sparkbot and Arc must own raw input handling, local classification, and redaction.
- LIMA receives already-normalized metadata only.
- The next LIMA-side branch should add synthetic translator fixtures and tests, not production translator code.
- Do not wire public Sparkbot or Arc production paths yet.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2493 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except this audit report before commit

## Recommended Next Branch

`implement-lima-shell-owned-translator-fixtures`

That branch must remain synthetic fixture-only and non-executing.
