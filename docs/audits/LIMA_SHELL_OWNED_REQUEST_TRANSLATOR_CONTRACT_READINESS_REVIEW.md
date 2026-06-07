# LIMA Shell-Owned Request Translator Contract Readiness Review

## Branch

`design-lima-shell-owned-request-translator-contract`

## Base Commit

`54e28b95bf197b558af3d9f47e97f01b2d1feddd`

## Scope

This readiness review evaluates the design-only shell-owned request translator contract.

This branch does not implement behavior. It does not modify `lima/`, tests, fixtures, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Readiness Verdict

PASS.

The design is narrow enough for independent audit and a later synthetic fixture-only implementation lane. It keeps raw input ownership in Sparkbot/Arc and preserves LIMA as a normalized-metadata kernel boundary.

Recommended next branch:

`audit-lima-shell-owned-request-translator-contract`

## Does the Design Keep Translation Shell-Owned?

Yes.

The design states that Sparkbot owns Sparkbot UI/session/task context parsing and Arc owns Arc office workflow/session/task context parsing. LIMA does not import shell internals and does not parse raw user text.

Verdict:

- PASS.

## Does It Preserve the Normalized Metadata Boundary?

Yes.

The design requires shells to produce already-normalized metadata and only then map into `KernelRequest`.

Verdict:

- PASS.

## Does It Avoid Runtime Translator Implementation?

Yes.

The branch is design-only and does not add translator code, tests, fixtures, runtime services, shell adapters, or `lima/` changes.

Verdict:

- PASS.

## Does It Preserve Fail-Closed Behavior?

Yes.

The design requires blocking on raw forwarding, credentials, unsafe payloads, live connector access, model calls, tool execution, external sends, file/browser/process/scheduler behavior, connection/pairing, device control, robot/drone/physical-world behavior, missing identity metadata, and missing default-deny capability profiles.

Verdict:

- PASS.

## Does It Preserve Guardian Boundaries?

Yes.

The design does not create real `GuardianDecision` authority, approval enforcement, execution authority, or bypass behavior. Guardian remains the future syscall gate.

Verdict:

- PASS.

## Does It Avoid Sparkbot and Arc Coupling?

Yes.

The design does not touch the public Sparkbot repo or Arc Bot repositories. It defines handoff notes only.

Verdict:

- PASS.

## Is the Later Fixture Lane Narrow Enough?

Yes.

The proposed later branch may only add:

- synthetic `ShellTranslatorInput` fixtures
- synthetic `ShellTranslatorOutput` fixtures
- tests validating safe mapping to `KernelRequest`
- tests proving blocked/needs-clarification outputs do not call `LimaKernel`
- redaction flag checks
- an implementation audit report

Verdict:

- PASS.

## Files Allowed in the Later Implementation Branch

Allowed later files:

- `tests/fixtures/shell_owned_translator/`
- `tests/test_lima_shell_owned_translator_fixtures.py`
- `docs/audits/LIMA_SHELL_OWNED_TRANSLATOR_FIXTURES_IMPLEMENTATION_AUDIT.md`
- optional docs notes under `docs/design/` only if they clarify fixture scope

Any `lima/` runtime change requires separate approval.

## Surfaces That Remain Forbidden

The later fixture branch must not add:

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

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2493 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except intended design docs before commit

## Recommended Next Branch

`audit-lima-shell-owned-request-translator-contract`

After that audit passes, the next implementation-shaped branch should be:

`implement-lima-shell-owned-translator-fixtures`
