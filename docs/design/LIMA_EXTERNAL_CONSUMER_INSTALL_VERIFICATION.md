# LIMA External Consumer Install Verification

## Purpose

This document designs the next dependency-readiness proof for LIMA Runtime: a local external-consumer install verification.

The goal is to prove that a shell-shaped consumer outside the `lima/` package can install or import LIMA and call the current non-executing public APIs without touching public Sparkbot, Arc Bot, live connectors, models, tools, storage, networks, devices, or physical-world systems.

This branch is design-only. It does not implement an install verifier, modify packaging metadata, create an external repo, touch public Sparkbot, touch Arc Bot repositories, modify `lima/`, call networks, download dependencies, publish packages, build release artifacts, run Docker, create installers, wire shells, call models/providers, execute tools, access connectors, persist data, use browser/file/network APIs, start background work, wire Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

## Product Context

LIMA now has:

- minimal non-executing `LimaKernel`
- explicit simulated discovery adapter path
- local minimal example shell proof
- Sparkbot/Arc normalized request fixtures
- shell-owned translator fixtures
- installable package metadata in `pyproject.toml`

The next readiness gap is proving dependency behavior from an external-consumer shape. This is a local verification lane, not public Sparkbot or Arc integration.

## Current Package Baseline

Current `pyproject.toml` declares:

- project name: `lima-runtime`
- version: `0.0.1`
- Python: `>=3.11`
- build backend: `setuptools.build_meta`
- package discovery: `include = ["lima*"]`

The later implementation branch should verify this metadata first. Packaging changes are allowed only if verification fails for a specific minimal reason and the change is separately reviewed in that branch.

## Verification Principle

The verification must prove:

```text
external consumer can import LIMA
external consumer can instantiate LimaKernel
external consumer can build normalized KernelRequest metadata
external consumer can optionally pass SimulatedDiscoveryAdapter explicitly
external consumer receives dry-run ExecutionResult
all non-execution invariants remain false
no live integration occurs
```

The verification must not prove or claim:

- public Sparkbot readiness
- Arc Bot readiness
- production shell wiring
- raw chat ingestion
- live HumanInput bridge
- IntentEnvelope runtime creation
- real GuardianDecision authority
- approval enforcement
- model calls
- provider routing
- tool execution
- connector access
- persistence
- live discovery
- network/device access
- Robo-OS access
- physical-world behavior

## Allowed Verification Modes

The later implementation branch may choose one of these local-only modes.

### Mode A: Subprocess-Free Import Verification

Tests import LIMA from the repo checkout and verify:

- `import lima`
- `from lima.kernel import LimaKernel`
- package metadata declares `lima-runtime`
- external-consumer fixture code imports only `lima`
- dry-run result invariants hold

This is the safest fallback mode and requires no package install.

### Mode B: Local Editable Install Verification

If safe in the current environment, tests or scripts may verify:

- `python -m pip install -e .`
- no network dependency download is required
- LIMA imports from the editable install
- dry-run example executes

This mode should be optional and must not mutate global environments in CI-style validation unless explicitly approved.

### Mode C: Local Wheel/Sdist Verification

Only if build tooling is already available locally or separately approved, the branch may verify:

- local package build
- install into a local temporary virtual environment
- import and dry-run execution

This mode must not publish to PyPI or any registry.

## Preferred First Implementation

The first implementation should use Mode A.

Reason:

- no dependency downloads
- no environment mutation
- no publishing
- no external service calls
- no virtualenv management burden
- enough to prove public import and external-consumer call shape

Optional Mode B or C can be designed later after Mode A is audited.

## Proposed External Consumer Fixture

The later implementation may add a local fixture under:

- `tests/fixtures/external_consumer_install/`

The fixture may include synthetic consumer metadata:

```json
{
  "consumer_id": "synthetic-external-consumer",
  "consumer_type": "sparkbot_like_shell",
  "imports_allowed": ["lima", "lima.kernel"],
  "expected_package_name": "lima-runtime",
  "expected_kernel_import": "LimaKernel",
  "expected_result": {
    "dry_run": true,
    "executable": false,
    "execution_allowed": false
  }
}
```

The fixture must not contain:

- Sparkbot source code
- Arc Bot source code
- raw chat text
- provider/model payloads
- connector payloads
- credentials
- network targets
- device targets
- robot/drone command payloads

## Proposed Verification Test Shape

Future tests may:

- read package metadata from `pyproject.toml`
- import `lima`
- import public kernel APIs from `lima.kernel`
- dynamically load a local synthetic consumer module from `tests/fixtures/external_consumer_install/`
- assert the consumer module imports only `lima`
- build a normalized `KernelRequest`
- call `LimaKernel.evaluate(...)`
- optionally call explicit `SimulatedDiscoveryAdapter`
- assert all non-execution invariants

The tests must not:

- use public Sparkbot code
- use Arc Bot code
- call shell routes
- call models/providers
- execute tools
- write files outside normal pytest/cache behavior
- open sockets
- call networks
- start subprocesses unless a later install-mode branch explicitly approves it
- create virtual environments unless separately approved
- install dependencies from the network
- access devices

## Required Non-Execution Invariants

Any verification result must preserve:

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

## External Consumer Boundary

The external consumer proof must be local and synthetic.

Allowed:

- local fixture consumer module
- local fixture metadata
- package metadata assertions
- public import assertions
- dry-run kernel calls
- synthetic simulated discovery path

Forbidden:

- public Sparkbot repository changes
- Arc Bot repository changes
- production shell wiring
- shell routes
- raw HumanInput bridge
- raw chat parsing in LIMA
- model/provider calls
- tool execution
- connector access
- persistence
- network calls
- sockets
- live discovery
- device control
- robotics/drones/physical-world behavior

## Acceptance Criteria for Later Implementation

The later implementation branch should prove:

- package metadata remains `lima-runtime`
- `import lima` works
- `from lima.kernel import LimaKernel` works
- synthetic external consumer imports only `lima`
- synthetic external consumer builds already-normalized metadata
- dry-run planning evaluation returns `proposed`
- optional explicit simulated discovery returns synthetic surfaces only
- non-execution invariants hold
- blocked/unsafe consumer metadata does not execute
- no forbidden imports or surfaces are introduced

## Future Implementation Branch

The next implementation-shaped branch may be:

`implement-lima-external-consumer-import-proof`

That branch may only add:

- `tests/fixtures/external_consumer_install/`
- `tests/test_lima_external_consumer_install_verification.py`
- `docs/audits/LIMA_EXTERNAL_CONSUMER_INSTALL_VERIFICATION_IMPLEMENTATION_AUDIT.md`
- optional docs note if needed

That branch must not:

- touch public Sparkbot
- touch Arc Bot repositories
- modify `lima/` runtime behavior
- modify package metadata unless a specific verification failure requires a minimal fix
- publish packages
- download dependencies without approval
- create Docker images
- create installers
- call external services
- call models/providers
- execute tools
- access connectors
- persist data
- use browser/network APIs
- start subprocesses unless the branch explicitly stays in approved local install verification scope
- wire Robo-OS
- control devices, robots, drones, or physical-world systems

## Handoff Notes for Sparkbot and Arc Teams

Archive-ready message:

- LIMA is preparing an external-consumer import proof.
- This proof is local and synthetic.
- It does not touch public Sparkbot or Arc repositories.
- It should prove dependency shape only: import LIMA, create normalized metadata, call dry-run kernel, verify non-execution.
- Sparkbot and Arc production integration remains blocked until later repo-owned branches.

## Design Verdict

This design is ready for independent audit.

It does not approve install implementation yet. It does not approve public Sparkbot integration, Arc Bot integration, live HumanInput, raw text parsing in LIMA, IntentEnvelope runtime creation, Guardian enforcement, provider/model calls, tool execution, persistence, connector behavior, live discovery, Robo-OS access, external sends, or physical-world behavior.
