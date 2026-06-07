# LIMA Kernel Simulated Discovery Wiring Audit

## Branch

`audit-lima-kernel-simulated-discovery-wiring`

## Base Commit

`47f490c9743ec61df1baf52c6d08ee72ae1e3df4`

## Scope

This independent audit reviews the explicit kernel-to-simulated-discovery-adapter wiring implementation before any package/example-shell work, Sparkbot readiness contract, Arc Bot readiness contract, live adapter work, or runtime expansion begins.

This branch does not implement behavior. It does not modify `lima/`, tests, tests/support, adapter implementation files, provider/model files, storage/persistence files, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, runtime behavior, or physical-world behavior.

## Audit Verdict

PASS.

The implementation remains explicit, opt-in, dry-run only, simulated only, synthetic/inert only, local/in-process only, redacted, and non-executing.

It is ready for the next product-readiness design lane:

`design-lima-package-example-shell-contract`

It is not ready for public Sparkbot or Arc Bot integration yet. It is also not ready for live discovery, scanning, connection attempts, pairing, credential use, model calls, provider routing, persistence, HumanInput runtime bridge, Guardian enforcement, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Scope and File Safety

The implementation branch changed only:

- `lima/kernel/kernel.py`
- `tests/test_lima_kernel_simulated_discovery_wiring.py`
- `docs/audits/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING_IMPLEMENTATION_AUDIT.md`

Confirmed untouched:

- top-level `lima/__init__.py`
- `lima/kernel/__init__.py`
- `lima/kernel/discovery.py`
- `lima/adapters/`
- `lima/contracts/`
- provider/model implementation files
- storage/persistence implementation files
- Sparkbot wiring files
- Arc Bot wiring files
- Robo-OS wiring files
- public Sparkbot repository

Audit finding:

- PASS. The branch stayed within the approved implementation/test/audit files.

## 2. Public API Review

The only public API shape change is:

- `LimaKernel.evaluate(request, *, simulated_discovery_adapter=None)`

No new public exports were added.

Top-level `lima` remains unchanged.

The new parameter is keyword-only, explicit, and local to the call site. Existing callers can continue to use classification-only `LimaKernel.evaluate(request)` behavior.

Audit finding:

- PASS. The API change is narrow and does not introduce global state, registry behavior, or implicit activation.

## 3. Explicit Wiring Behavior

The kernel invokes the adapter only when a caller explicitly passes:

- `simulated_discovery_adapter=...`

The implementation does not add:

- constructor-held simulated adapter state
- global adapter registry
- plugin loader
- dynamic import
- package entry-point loading
- environment activation
- shell hidden activation
- background adapter discovery
- live connector lookup

Audit finding:

- PASS. Adapter use is explicit and opt-in.

## 4. Invocation Gates

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

If no adapter is supplied and the request only asks for classification, the kernel returns classification-only results.

If no adapter is supplied and the request demands simulated surfaces, the kernel blocks with:

- `simulated_discovery_adapter_required`

If an adapter is supplied but metadata is not strict simulated dry-run metadata, the kernel blocks with:

- `strict_simulated_discovery_metadata_required`

Audit finding:

- PASS. The adapter path remains gated and fail-closed.

## 5. Request/Result Mapping

The kernel maps `KernelRequest` to `DiscoveryAdapterRequest` only after classification passes.

Mapped adapter request fields are limited to:

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
- inert metadata flags

The adapter result is mapped back only into `ExecutionResult.metadata["simulated_discovery"]`.

Synthetic surface metadata includes:

- `surface_id`
- `connection_type`
- `synthetic: true`
- `inert: true`
- `simulated: true`
- `connectable: false`
- `controllable: false`
- `physical_world: false`

Audit finding:

- PASS. The mapping does not create execution authority, dispatch, persistence, live adapter activation, or shell wiring.

## 6. Non-Execution Invariants

Tests assert that results preserve:

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

Audit finding:

- PASS. `simulated_adapter_used: true` is metadata-only and does not change the live `adapter_active` invariant.

## 7. Fail-Closed and Redaction Behavior

The implementation blocks:

- missing adapter when simulated surfaces are required
- adapter present with non-strict simulated metadata
- disabled capability
- invalid simulated adapter manifest
- adapter exception
- adapter blocked result
- unsafe adapter invariants
- unsafe adapter surfaces
- unsafe credential/pairing/session/live/physical markers in adapter output

Adapter exceptions are redacted:

- raw exception text is not echoed into `ExecutionResult`

Adapter event refs are copied only into result metadata. Events remain in-memory and non-durable.

Audit finding:

- PASS. The implementation treats adapter output as untrusted and fails closed.

## 8. Forbidden Surface Review

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

Focused tests statically check the kernel module for forbidden imports, calls, and live/shell wiring strings.

Audit finding:

- PASS. No forbidden runtime or physical-world surfaces were introduced.

## 9. Test Coverage Review

`tests/test_lima_kernel_simulated_discovery_wiring.py` covers:

- explicit simulated adapter success path
- synthetic surfaces in dry-run metadata
- absent adapter classification-only behavior
- absent adapter block when simulated surfaces are requested
- non-strict metadata blocks
- disabled capability block
- invalid manifest block without invocation
- adapter error redaction
- unsafe adapter result block
- adapter blocked result propagation
- non-execution invariants
- forbidden imports/calls/strings

Existing focused tests continued to pass for:

- minimal kernel runtime invariants
- simulated discovery adapter behavior
- connection intent classification

Audit finding:

- PASS. Coverage is appropriate for this non-executing slice.

## 10. Sparkbot and Arc Bot Readiness Impact

This branch moves LIMA closer to future Sparkbot and Arc Bot use because it proves:

- a shell-facing `LimaKernel` can accept normalized metadata
- connection/discovery metadata can be classified
- an explicit simulated adapter can be invoked without hidden dispatch
- synthetic results can be carried back in dry-run metadata
- non-execution invariants can survive kernel-to-adapter composition

This branch does not make LIMA ready for Sparkbot or Arc Bot integration yet.

Remaining blockers before Sparkbot/Arc can use LIMA safely:

- package install proof from outside this repo
- example shell proof
- formal Sparkbot/Arc request metadata contract
- shell manifest and capability profile contract
- real HumanInput runtime bridge
- real IntentEnvelope runtime creation
- real GuardianDecision authority
- approval UX and enforcement
- model/provider routing
- durable/redacted Spine event path
- storage backend
- connector/tool execution policy
- compatibility test plan that does not touch the public Sparkbot repo

Team note for Sparkbot/Arc handoff:

- Do not integrate yet.
- Prepare to send already-normalized metadata only.
- Do not send raw natural language directly into LIMA for execution.
- Do not expect model calls, tool execution, connector access, persistence, or live discovery from the current LIMA branch.

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2479 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only `docs/audits/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING_AUDIT.md` before staging.

## Readiness Decision

Ready for:

- `design-lima-package-example-shell-contract`

Not ready for:

- public Sparkbot integration
- Arc Bot integration
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- provider/model calls
- tool execution
- storage/persistence
- Guardian enforcement
- HumanInput runtime bridge
- Robo-OS access
- physical-world behavior

## Recommended Next Branch

`design-lima-package-example-shell-contract`

That branch should be design-only and should define the install/package/example-shell proof needed before LIMA can become a credible dependency candidate for Sparkbot and Arc Bot.
