# LIMA Package and Example Shell Contract

## Purpose

This document designs the next product-readiness proof needed before LIMA AI OS can become a credible dependency candidate for Sparkbot and Arc Bot.

The next proof is not live integration. The proof is:

- LIMA can be packaged from this repository.
- A separate example shell can install or import LIMA as a dependency.
- The example shell can instantiate `LimaKernel`.
- The example shell can pass already-normalized metadata into `LimaKernel.evaluate(...)`.
- The example shell can optionally pass an explicit `SimulatedDiscoveryAdapter`.
- The example shell receives a dry-run `ExecutionResult`.
- No model call, tool call, shell wiring, persistence, network access, connector access, or physical-world behavior occurs.

This branch is design-only. It does not implement packaging changes, example shell code, tests, Sparkbot wiring, Arc Bot wiring, provider/model calls, storage/persistence, live adapters, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Product Context

SparkPit Labs needs LIMA AI OS to become the governed runtime/kernel below:

- public Sparkbot release
- Arc Bot / LIMA AI Office
- future custom office bots
- Guardian Services
- LIMA-Robo-OS and other physical-world consumers later

The first dependency-readiness milestone is deliberately small:

- prove a shell can depend on LIMA
- prove a shell can call the kernel
- prove LIMA stays dry-run and fail-closed
- prove no public Sparkbot repository changes are needed for the proof

This is a package/interface proof, not a product integration.

## Current Package Baseline

Current `pyproject.toml` already declares:

- project name: `lima-runtime`
- version: `0.0.1`
- Python: `>=3.11`
- build backend: `setuptools.build_meta`
- package discovery: `include = ["lima*"]`

The later implementation branch should verify the current package metadata rather than widening scope first. Packaging changes should be made only if the proof fails for a specific reason.

## Future Example Shell Shape

The example shell must be local to this repository until a later audit approves external consumer work.

Preferred future location:

- `examples/minimal_shell/`

The example shell must be inert and deterministic. It may include:

- a README explaining scope and non-execution guarantees
- a small Python module or script that imports `lima.kernel`
- a fixture-like normalized request builder
- a dry-run evaluation example
- an optional explicit simulated discovery adapter example
- assertions or printed summaries proving non-execution fields remain false

The example shell must not:

- parse raw natural language
- import Sparkbot
- import Arc Bot
- call models
- call providers
- execute tools
- mutate files
- open browser sessions
- call networks
- connect to devices
- scan
- pair
- use credentials
- persist data
- start schedulers/workers/threads/subprocesses
- wire Robo-OS
- touch physical-world systems

## Example Shell Input Contract

The example shell must construct already-normalized metadata only.

Allowed request shape:

```python
# PSEUDO-CODE ONLY. Not implemented in this branch.
request = KernelRequest(
    request_id="example-req-001",
    shell_id="example-shell",
    actor_id="example-actor",
    session_id="example-session",
    normalized_intent={
        "action_category": "planning",
        "summary": "prepare a dry-run task plan",
        "risk_class": "low",
    },
    capability_profile=CapabilityProfile(),
    source_surface={
        "surface": "example_shell",
        "privacy_class": "synthetic",
    },
)
```

Allowed simulated discovery request shape:

```python
# PSEUDO-CODE ONLY. Not implemented in this branch.
request = KernelRequest(
    request_id="example-sim-001",
    shell_id="example-shell",
    actor_id="example-actor",
    session_id="example-session",
    normalized_intent={
        "action_category": "ble_discovery",
        "requested_capability": "ble_discovery",
        "connection_type": "ble",
        "discovery_mode": "simulated",
        "dry_run": True,
        "simulated_only": True,
        "include_simulated_surfaces": True,
        "risk_class": "low",
        "target_hint": "synthetic_ble_fixture",
    },
    capability_profile=CapabilityProfile(ble_discovery=True),
    source_surface={
        "surface": "example_shell",
        "privacy_class": "synthetic",
    },
)

result = LimaKernel().evaluate(
    request,
    simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
)
```

Raw user text is not an accepted input for this proof.

## Example Shell Output Contract

The example shell may display or assert only redacted dry-run result metadata.

Required invariant checks:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

Simulated discovery output may include synthetic surfaces only:

- `surface_id`
- `connection_type`
- `synthetic: true`
- `inert: true`
- `simulated: true`
- `connectable: false`
- `controllable: false`
- `physical_world: false`

## Package Proof Contract

The later implementation branch may prove packaging in one of two ways.

Preferred proof:

- `python -m build` only if build dependencies are already available locally, or if separate approval allows dependency installation.

Fallback proof:

- `python -m pip install -e .` into the current environment only if already safe and no external downloads are needed.
- Or a subprocess-free test that imports `lima` and `lima.kernel` from the repo checkout and validates public APIs.

The package proof must not require:

- publishing to PyPI
- touching public Sparkbot
- touching Arc Bot
- network dependency downloads without approval
- secrets or credentials
- external service calls
- Docker images
- deployment scripts
- installers
- release tags

## Future Acceptance Tests

The later implementation branch should add focused tests proving:

- `import lima` works
- `from lima.kernel import LimaKernel` works
- package metadata still declares `lima-runtime`
- example shell imports only from `lima`
- example shell creates already-normalized `KernelRequest`
- example shell receives dry-run `ExecutionResult`
- simulated example shell path returns synthetic surfaces only
- non-execution invariants remain false
- example shell does not import Sparkbot
- example shell does not import Arc Bot
- example shell does not import Robo-OS
- example shell does not use sockets, network APIs, subprocesses, threads, schedulers, storage, providers, model APIs, browser APIs, USB/serial/Bluetooth/MQTT/Matter/mDNS APIs, or device/robot/drone control

## Sparkbot and Arc Bot Consumer Contract

Future Sparkbot/Arc teams should treat this proof as a dependency contract only.

Allowed future consumer behavior after the proof passes:

- add LIMA as a dependency candidate in a branch owned by that repo team
- pass already-normalized metadata into `LimaKernel`
- inspect dry-run results
- verify non-execution invariants
- compare shell expectations against LIMA result shapes

Forbidden consumer behavior until later phases:

- raw chat-to-LIMA execution
- live HumanInput bridge
- model routing through LIMA
- tool calls through LIMA
- connector reads/writes through LIMA
- persistence through LIMA
- approval enforcement through LIMA
- real GuardianDecision creation through LIMA
- Sparkbot production route wiring
- Arc Bot production workflow wiring
- live discovery or device connection

## Files Allowed in Later Implementation Branch

The later implementation branch may touch only:

- `examples/minimal_shell/README.md`
- `examples/minimal_shell/example_shell.py`
- `tests/test_lima_package_example_shell_contract.py`
- `docs/audits/LIMA_PACKAGE_EXAMPLE_SHELL_IMPLEMENTATION_AUDIT.md`
- `pyproject.toml` only if a packaging proof fails and the minimal metadata fix is required
- existing README/docs only if needed to link the example shell without claiming product readiness

Any `lima/` changes require separate approval before implementation starts.

## Surfaces Forbidden in Later Implementation Branch

The later implementation branch must not add:

- Sparkbot repo changes
- Arc Bot repo changes
- production shell wiring
- `lima/` runtime behavior
- provider/model calls
- storage/persistence
- real Guardian enforcement
- real approval enforcement
- real HumanInput bridge
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

## Handoff Notes for Sparkbot and Arc Bot Teams

No Sparkbot or Arc Bot repository should be touched by this LIMA lane.

Message to archive for those teams:

- LIMA is moving toward dependency-readiness, not integration-readiness.
- The first expected consumer shape is normalized metadata in, dry-run result out.
- Do not send raw chat text into LIMA for execution.
- Do not expect LIMA to call models, tools, connectors, storage, or devices yet.
- The first useful cross-team review should compare Sparkbot/Arc normalized intent metadata needs against `KernelRequest`, `CapabilityProfile`, and `ExecutionResult`.

## Recommended Later Sequence

1. `audit-lima-package-example-shell-contract`
2. `implement-lima-package-example-shell-proof`
3. `audit-lima-package-example-shell-proof`
4. `design-lima-sparkbot-arc-request-metadata-contract`
5. `audit-lima-sparkbot-arc-request-metadata-contract`

No Sparkbot or Arc Bot repo work should begin until the package/example-shell proof is implemented and audited.

## Design Verdict

This design is ready for independent audit.

It does not approve implementation yet. It does not approve Sparkbot integration, Arc Bot integration, live HumanInput, IntentEnvelope runtime creation, Guardian enforcement, model calls, tool execution, persistence, live discovery, connector behavior, Robo-OS access, or physical-world behavior.
