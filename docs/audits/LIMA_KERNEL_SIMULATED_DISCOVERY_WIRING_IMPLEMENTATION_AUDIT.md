# LIMA Kernel Simulated Discovery Wiring Implementation Audit

## Branch

`implement-lima-kernel-simulated-discovery-wiring`

## Base commit

`33394bf4a634d7313e8a1ba9f89e735baea6ac7e`

## Goal

Implement the smallest explicit, non-executing bridge from `LimaKernel.evaluate(...)` to `SimulatedDiscoveryAdapter.simulate(...)` so LIMA can prove a kernel-to-adapter path without live discovery, scanning, connection attempts, pairing, credentials, shell wiring, persistence, or physical-world behavior.

This branch is part of the larger SparkPit Labs goal of getting LIMA AI OS ready for future use by Sparkbot and Arc Bot. It does not touch the public Sparkbot repository and does not wire Sparkbot or Arc Bot.

## Files Changed

- `lima/kernel/kernel.py`
- `tests/test_lima_kernel_simulated_discovery_wiring.py`
- `docs/audits/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING_IMPLEMENTATION_AUDIT.md`

## Public API Status

No new public exports were added.

Existing public API updated:

- `LimaKernel.evaluate(request, *, simulated_discovery_adapter=None)`

The new argument is keyword-only and explicit. Existing callers can continue to call `evaluate(request)` for classification-only behavior.

Top-level `lima` remains unchanged.

## Callable Kernel API Summary

`LimaKernel.evaluate(...)` now supports an explicit simulated adapter path only when a caller supplies `simulated_discovery_adapter=...`.

Adapter invocation requires:

- classification result is `proposed`
- requested capability is a connection/discovery capability
- `discovery_mode="simulated"`
- `dry_run=True`
- `simulated_only=True`
- required capability is enabled
- no credential claims
- no pairing claims
- no connection/session target hint
- no auto-connect wording
- no try-everything wording
- no robot/drone/physical-world markers
- valid simulated adapter manifest

If the adapter is absent and the request only asks for classification, the kernel returns the existing classification-only result.

If the adapter is absent and the request demands simulated surfaces, the kernel blocks with:

- `simulated_discovery_adapter_required`

If an adapter is present but the request is not strictly simulated, the kernel blocks with:

- `strict_simulated_discovery_metadata_required`

## Request/Result Mapping

The kernel maps `KernelRequest` to `DiscoveryAdapterRequest` only after classification passes and strict simulated metadata is present.

Mapped request fields:

- request ID
- actor ID
- shell ID
- session ID
- redacted source surface
- safe target hint only
- connection type
- `discovery_mode="simulated"`
- `dry_run=True`
- `simulated_only=True`
- `credential_ref=None`
- inert metadata flags only

The kernel maps `DiscoveryAdapterResult` back into `ExecutionResult.metadata["simulated_discovery"]` only.

Returned synthetic surface metadata includes:

- `surface_id`
- `connection_type`
- `synthetic: true`
- `inert: true`
- `simulated: true`
- `connectable: false`
- `controllable: false`
- `physical_world: false`

Adapter results do not become execution authority.

## Non-Execution Invariants

Every result still preserves:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `dispatch_allowed: false`
- `persistence_allowed: false`
- `dry_run: true`
- `model_calls_allowed: false`
- `model_calls_executed: false`
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_allowed: false`
- `physical_world_executed: false`
- `guardian_decision_created: false`
- `approval_enforced: false`
- `humaninput_bridge_active: false`
- `sparkbot_wiring_active: false`
- `robo_os_wiring_active: false`
- `adapter_active: false`
- `tool_execution_allowed: false`
- `driver_execution_allowed: false`
- `scheduler_active: false`
- `external_calls_allowed: false`

`adapter_active` remains false because the field means live adapter/runtime activation. The dry-run metadata uses `simulated_adapter_used: true` only to indicate an explicit synthetic adapter preview occurred without execution authority.

## Fail-Closed Behavior

The kernel blocks:

- missing adapter when simulated surfaces are required
- adapter present with non-strict simulated metadata
- disabled capability
- invalid simulated adapter manifest
- adapter exception, with raw error redacted
- adapter blocked result
- unsafe adapter invariants
- unsafe adapter surfaces
- unsafe credential/pairing/session/live/physical markers in adapter output

Adapter results cannot turn a blocked or approval-required classification into `proposed`.

## Event and Redaction Behavior

Kernel events remain redacted and in-memory only.

Adapter event refs are copied only into `ExecutionResult.metadata["simulated_discovery"]["event_refs"]`.

The kernel does not persist adapter events, open a Spine writer, append files, create database records, send telemetry, write queues, or notify shells.

The kernel redacts adapter exceptions and does not echo raw exception text.

## Tests Added

Added `tests/test_lima_kernel_simulated_discovery_wiring.py`.

Coverage includes:

- explicit simulated adapter returns synthetic surfaces in dry-run metadata
- absent adapter returns classification-only when surfaces are not requested
- absent adapter blocks when request demands simulated surfaces
- non-strict simulated metadata blocks
- disabled capability blocks before adapter metadata is added
- invalid manifest blocks without adapter invocation
- adapter exception blocks with redacted reason
- unsafe adapter result blocks
- adapter blocked result becomes kernel blocked result
- non-execution invariants
- forbidden import/call/string checks for kernel wiring

## Forbidden Surfaces Checked

The implementation does not add:

- live adapter registry
- hidden dispatch
- plugin auto-loading
- dynamic import
- environment-based activation
- shell-driven hidden activation
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- credential storage
- sockets/network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS wiring
- Sparkbot wiring
- Arc Bot wiring
- storage/persistence
- provider/model calls
- real Guardian enforcement
- real HumanInput bridge
- approval enforcement
- background workers
- subprocesses
- threads
- scheduler
- device control
- robot/drone control
- physical-world behavior

Focused tests statically check for forbidden imports, calls, and live/shell wiring strings.

## Sparkbot and Arc Bot Notes for Handoff

No Sparkbot or Arc Bot repository was touched.

Team-facing note:

- LIMA now has an explicit dry-run kernel-to-simulated-discovery adapter path in progress.
- Future Sparkbot/Arc integration must pass already-normalized metadata into LIMA.
- Sparkbot/Arc must not send raw natural language directly into LIMA for execution.
- Sparkbot/Arc must not expect model calls, tool execution, persistence, connector access, or live discovery from this slice.
- The next useful consumer contract for Sparkbot/Arc is an install/package/example-shell proof that imports `lima.kernel.LimaKernel`, builds a `KernelRequest`, and receives a dry-run `ExecutionResult`.

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2479 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only intended implementation, test, and audit files before staging.

Focused pre-audit validation already passed:

- `python -m pytest -q tests\test_lima_kernel_simulated_discovery_wiring.py tests\test_lima_minimal_kernel_runtime.py tests\test_lima_simulated_discovery_adapter.py tests\test_lima_connection_intent_classification.py -p no:cacheprovider` passed: 108 tests.

## Remaining Blockers Before Sparkbot/Arc Use

LIMA is closer to being usable as a dependency, but it is not ready for public Sparkbot or Arc Bot integration yet.

Remaining blockers:

- no package install proof from a separate example shell
- no formal shell contract for Sparkbot/Arc request metadata
- no real HumanInput runtime bridge
- no real IntentEnvelope runtime creation
- no real GuardianDecision authority
- no approval enforcement
- no model provider routing
- no durable event/spine implementation
- no shell manifests
- no provider/tool/connector execution
- no storage backend
- no live adapter registry
- no Sparkbot or Arc integration tests from outside this repo

## Recommended Next Branch

`audit-lima-kernel-simulated-discovery-wiring`

After that audit passes, the next safest product-readiness lane should be:

`design-lima-package-example-shell-contract`

That branch should design an install/package/example-shell proof for Sparkbot/Arc readiness without touching the public Sparkbot repo or adding runtime execution.
