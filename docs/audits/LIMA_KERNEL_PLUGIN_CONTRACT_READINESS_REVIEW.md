# LIMA Kernel Plugin Contract Readiness Review

## Branch

`design-lima-kernel-plugin-contract`

## Scope

This review evaluates `docs/design/LIMA_KERNEL_PLUGIN_CONTRACT.md` as a docs-only design for the first shell-facing LIMA Kernel plugin contract.

No runtime behavior is implemented by this branch. No `lima/` files are changed.

## Verdict

The contract is narrow enough for a later minimal implementation, provided that implementation is separately approved and remains non-executing.

The design defines a shell-facing `LimaKernel` shape, normalized metadata request contract, dry-run `ExecutionResult`, explicit capability profile, fail-closed Guardian stub, redacted in-memory event shape, and future plug-in points for providers, HumanInput, and Robo-OS without implementing any of those systems.

## Is the contract narrow enough for a later minimal implementation?

Yes.

The later implementation can be limited to:

- request/result/capability/event dataclasses
- top-level `LimaKernel.evaluate(...)`
- fail-closed Guardian stub
- redacted in-memory event sink
- deterministic tests for `proposed`, `approval_required`, and `blocked`

The contract excludes providers, storage, persistence, adapters, shell wiring, tool execution, driver execution, schedulers, background work, model calls, and physical-world behavior.

## Does it preserve fail-closed behavior?

Yes.

The design requires:

- unknown or missing risk/capability data to fail closed
- text-only preview metadata to return `proposed`
- consequential capabilities to return `approval_required`
- dangerous or physical-world capabilities to return `blocked`
- no execution authorization from caller-provided approval hints
- no real GuardianDecision creation in the first implementation

## Does it avoid runtime execution?

Yes.

The design explicitly forbids:

- model calls
- tool calls
- file writes
- browser/network actions
- process execution
- connector reads/writes
- external sends
- storage/persistence
- scheduler/background work
- driver execution
- robotics, drone, device, or physical-world behavior

The proposed `ExecutionResult` must always report `dry_run=True`, `executed=False`, and empty execution claims in the first implementation.

## Does it avoid Sparkbot coupling?

Yes.

The design references Sparkbot only as a future shell consumer in pseudo-code.

It does not import Sparkbot, call Sparkbot, wire Sparkbot routes, depend on Sparkbot data models, depend on Sparkbot auth/session state, or preserve Sparkbot chat-to-tool shortcuts.

## Does it avoid Robo-OS unsafe coupling?

Yes.

The design treats LIMA-Robo-OS as a future Guardian-gated driver/runtime integration. It requires dry-run or simulation, approval, emergency-stop semantics, telemetry evidence, and audit lineage before any future physical-world behavior.

The first implementation must block `robotics_actuation`, `drone_actuation`, and `device_control`.

## Exact files allowed in a later implementation branch

Only these new files should be eligible in a later separately approved minimal implementation branch:

- `lima/kernel/plugin_contract.py`
- `lima/kernel/kernel.py`
- `lima/kernel/events.py`
- `lima/kernel/guardian_stub.py`
- `tests/test_lima_kernel_plugin_contract.py`
- `tests/test_lima_kernel_fail_closed.py`
- `tests/test_lima_kernel_redacted_events.py`
- `docs/audits/LIMA_MINIMAL_KERNEL_RUNTIME_IMPLEMENTATION_AUDIT.md`

Existing file allowed for export-only changes:

- `lima/kernel/__init__.py`

Any later implementation should keep changes limited to the files above unless Phil explicitly approves a narrower or amended file map before work begins.

## Exact files/surfaces that remain forbidden

Forbidden source areas:

- `lima/adapters/**`
- `lima/guardian/**` except no changes unless explicitly approved for contract-only import checks
- `lima/harness/**`
- `lima/io/**`
- `lima/packs/**`
- `lima/persistence/**`
- `lima/services/**`
- `lima/shells/**`
- `lima/spine/**`

Forbidden runtime surfaces:

- provider/model calls
- provider registry implementation
- prompt assembly
- tool catalog exposure
- tool execution
- driver execution
- storage/persistence
- durable event log
- Guardian enforcement
- real GuardianDecision creation
- approval enforcement
- PIN verification
- breakglass enforcement
- auth/vault/trust lookup
- HumanInput live bridge
- IntentCompiler runtime
- Sparkbot wiring
- Arc Bot wiring
- Robo-OS wiring
- adapters
- connector reads/writes
- external sends
- shell/browser/network/file mutation
- process execution
- terminal/PTY
- scheduler/background workers
- robotics actuation
- drone actuation
- device control
- physical-world behavior

Forbidden content in events/results:

- raw prompts
- raw provider payloads
- secrets
- headers
- tokens
- credentials
- unsafe command payloads
- raw tool args/results
- raw terminal output
- raw browser/network payloads
- raw sensor data
- robot/device command payloads

## Readiness conditions for implementation

Before implementation begins, the operator should approve:

- exact branch name
- exact file touch map
- no-execution acceptance tests
- rollback expectations
- allowed exports from `lima.kernel`
- whether the object is named `LimaKernel` or another equivalent app object

## Recommended next branch

Recommended next branch if Phil approves implementation scope:

`implement-lima-minimal-kernel-runtime`

If implementation is not approved, the safest next branch is:

`design-lima-kernel-plugin-contract-acceptance-tests`

That branch should remain docs/tests/fixtures-only and define acceptance tests before runtime code.
