# LIMA AI OS Runtime Readiness Audit

## Branch

`audit-lima-ai-os-runtime-readiness`

## Base commit

`8328bfe99452a32d54e6659f0e099e450699d901`

## Audit verdict

The current LIMA-AI-OS repo is safety-disciplined and contract-rich, with narrow non-executing callable kernel helpers, but it is not yet a plug-and-play AI operating layer.

The repo should not claim plug-and-play readiness today. It has package metadata, a `lima/` package, public contract definitions, non-production/test-only fakes, and narrow in-process kernel helpers. It does not contain a top-level `LimaKernel` or equivalent shell integration point, callable runtime services, a durable event/spine implementation, provider/model routing implementation, Guardian enforcement implementation, persistence backend, adapter wiring, or a working example shell.

The next implementation direction should be a separately approved minimal kernel runtime design/implementation lane, not more broad planning.

## Current import/package status

LIMA is importable from the repository checkout.

Observed package metadata:

- `pyproject.toml` declares project name `lima-runtime`, version `0.0.1`, Python `>=3.11`, and setuptools package discovery for `lima*`.
- The source tree contains a real `lima/` package with contracts, kernel helpers, adapter skeletons, Guardian fakes, and reserved namespaces.

Observed import surfaces:

- `import lima` succeeds from the repo checkout.
- `lima.__all__` is `["contracts"]`.
- `import lima.kernel` succeeds from the repo checkout.
- `lima.kernel.__all__` exposes:
  - `ALLOWED_CANDIDATE_STATUSES`
  - `CandidatePreview`
  - `CandidateStatusError`
  - `IntakeCandidateError`
  - `RuntimeStateSnapshot`
  - `build_intake_candidate`
  - `inspect_runtime_state`
  - `normalize_candidate_status`
  - `preview_candidate`
  - `validate_candidate`

Audit answer:

- Is LIMA importable as a package? Yes, from the checkout, and it is package-configured through `pyproject.toml`.
- What top-level APIs are exposed from `lima` and `lima.kernel`? `lima` only advertises `contracts`; `lima.kernel` advertises narrow non-executing candidate helpers and related dataclasses/errors.
- Is there a `LimaKernel` or equivalent single shell integration point? No.

## Callable runtime APIs found

Callable source surfaces found today are narrow and intentionally non-executing.

Kernel helpers:

- `lima.kernel.build_intake_candidate(intake)` accepts already-normalized synthetic/test-only intake metadata and returns non-executable candidate metadata.
- `lima.kernel.normalize_candidate_status(candidate)` returns a fail-closed status-normalized candidate copy.
- `lima.kernel.validate_candidate(candidate)` validates candidate metadata and forces invalid or risky states to blocked/non-executable outputs.
- `lima.kernel.preview_candidate(candidate_data=None)` returns non-authoritative candidate preview metadata.
- `lima.kernel.inspect_runtime_state(candidate_state=None)` returns a read-only, non-authoritative runtime-state snapshot for caller-provided candidate state.

Non-production adapter skeleton:

- `lima.adapters.SparkbotHumanInputAdapter` converts neutral Sparkbot-style payload dataclasses into `HumanInput` records.
- The adapter is pure conversion only. It does not import Sparkbot, wire routes, perform live lookup, execute actions, approve, persist audit, or call models/tools.

Test-only/in-memory Guardian support:

- `lima.guardian` exports fake in-memory providers, evaluators, recorders, fixture harnesses, and fake pipeline classes for contract validation.
- These are explicitly fake/test-only/non-production and do not constitute real Guardian enforcement, durable audit persistence, approval enforcement, model routing, tool execution, or shell runtime behavior.

Audit answer:

- Which callable runtime APIs exist today? Narrow non-executing candidate helpers and pure conversion/test-only helpers exist. A callable product/runtime kernel API does not exist.

## Contracts/docs-only areas

The following are contracts, docs, tests, fixtures, placeholder namespaces, or fake/test-only support rather than production runtime behavior:

- `lima.contracts.*`: Protocols, dataclasses, enums, and safety contracts for Guardian, Harness, Intent, Driver, ToolPack, Spine, Storage, Privacy, Shell, Approval, Auth/Vault, and related boundaries.
- `lima.harness`, `lima.persistence`, `lima.spine`: reserved implementation namespaces only.
- `lima.io.*`: reserved IO/driver boundary namespaces only, including browser, filesystem, MCP, network, and Robo-OS.
- `lima.packs.*`: reserved tool-pack namespaces only.
- `lima.services.*`: reserved service namespaces only.
- `lima.shells.*`: reserved shell namespaces only.
- `docs/`: architecture, roadmap, phase reviews, safety gates, inventories, boundary maps, and implementation gate records.
- `tests/fixtures/*`: synthetic and inert fixture corpora.
- `tests/support/*`: test-only helper code, not product runtime.

Audit answer:

- Which areas are contracts/docs/tests/fixtures only? Most of the repo outside the narrow `lima/kernel` helpers and pure adapter skeleton is contracts/docs/tests/fixtures/reserved namespaces. The repo remains dominated by contract-first safety work.

## Storage/event capability

Code capability today:

- `lima.contracts.storage.StorageProtocol` defines a persistence interface for transactions, sanitized event storage, event lookup, and vault reference storage.
- `lima.contracts.spine.SpineProtocol`, `SpineEvent`, and `TaskRecord` define ledger/event/task shapes.
- `lima.contracts.events` defines audit event dataclasses and event/status enums.
- `lima.guardian.FakeSpineAuditRecorder` exists as an in-memory fake for contract validation.

Protocol-only or absent:

- No SQLite, Postgres, memory, file, or hosted storage backend is implemented.
- No durable event ledger exists.
- No audit writer service exists.
- No scheduler, recurring job runner, autonomous loop, task queue, or lineage persistence exists as product runtime.
- No redacted in-memory event bus exists as a top-level kernel service.

Audit answer:

- What storage/event/spine capability exists as code versus protocol only? The repo has protocol/dataclass definitions and fake in-memory test recorders. Real storage, durable Spine, event bus, audit persistence, and scheduler capability are protocol-only or absent.

## Provider/model capability

Code capability today:

- `lima.contracts.harness.HarnessProtocol`, `ModelRequest`, and `ModelResponse` define model harness boundaries.
- `lima.contracts.guardian.GuardianProtocol` includes model-call classification requirements.
- `lima.contracts.toolpack` defines tool-pack exposure/request/decision contracts.
- Docs inventory Sparkbot and Guardian Suite provider/model routing surfaces as future extraction references.

Protocol-only or absent:

- No provider adapter exists.
- No model router exists.
- No model call path exists.
- No prompt assembly, prompt cache, fallback routing, telemetry service, token/cost policy engine, or model tool-call loop exists in LIMA runtime code.
- No working example shell can call a model through LIMA.

Audit answer:

- What provider/model routing capability exists as code versus protocol only? Model/provider capability is contract-only today, with docs pointing to Sparkbot/Guardian Suite as future references. There is no executable model routing implementation.

## Guardian/action boundary capability

Code capability today:

- `lima.contracts.guardian` defines `GuardianProtocol`, `GuardianDecision`, `GuardianDecisionRef`, `ConsequentialActionRequest`, `ConsequentialActionType`, and decision statuses.
- `lima.contracts.approval`, `auth`, `vault`, `policy`, `privacy`, and `toolpack` define related trust-boundary contracts.
- `lima.guardian` contains fake in-memory evaluators, fake providers, fake approval/spine recorders, and a fake pipeline for contract tests.
- Kernel helpers force candidate outputs to non-executable and fail closed when caller-provided metadata implies approval, execution, dispatch, persistence, external calls, Sparkbot wiring, live adapters, or physical-world claims.

Protocol-only or absent:

- No real Guardian enforcement engine exists.
- No production policy engine exists.
- No live approval flow exists.
- No PIN verification, breakglass enforcement, vault access, auth provider, or trust-context lookup exists.
- No syscall gate object exists between shells and tools/models/drivers.
- No action execution path exists.

Audit answer:

- What Guardian/action boundary capability exists as code versus protocol only? Contracts and fake/test-only validation components exist. Real Guardian enforcement and runtime action gating are not implemented.

## HumanInput capability

Code capability today:

- `lima.contracts.intent.HumanInput`, `IntentEnvelope`, `IntentCompilerProtocol`, risk/intent/status enums, clarification, and compilation result contracts exist.
- `lima.adapters.SparkbotHumanInputAdapter` converts neutral chat, voice, meeting, and operator payload dataclasses into `HumanInput`.
- Test-only bridge/harness code exists under tests/support and fake Guardian modules.

Protocol-only or absent:

- No live HumanInput ingestion runtime exists.
- No shell adapter is wired.
- No IntentCompiler implementation exists.
- No HumanInput to `IntentEnvelope` runtime bridge exists.
- No natural-language parser exists.
- No GuardianDecision creation from HumanInput exists.
- No Sparkbot, Arc Bot, or other product shell integration exists.

Audit answer:

- What HumanInput capability exists as code versus protocol only? HumanInput has contract definitions and one non-production pure conversion adapter skeleton. Live ingestion, intent compilation, runtime bridge behavior, and shell wiring are absent.

## LIMA-Robo-OS integration readiness

Code capability today:

- `lima.contracts.driver` defines `DriverCapability`, `DriverCommand`, `DriverResult`, and `DriverProtocol`, including dry-run and GuardianDecision-gated execution signatures.
- `lima.io.robo` and `lima.packs.robo` namespaces exist as placeholders.
- Architecture and boundary docs classify Robo-OS as a future Guardian-gated driver/runtime integration, not a competing brain.

Protocol-only or absent:

- No Robo-OS adapter exists.
- No robot driver implementation exists.
- No hardware, simulator, MCP robot bridge, sensor, telemetry, emergency-stop, safety mode, or physical-world command path exists in this repo.
- No robot shell manifest exists.
- No physical-world action can be planned or executed through LIMA today.

Audit answer:

- What Robo-OS / robotics / physical-world readiness exists as code versus protocol only? The repo has driver contracts and placeholder namespaces only. Robotics and physical-world readiness are protocol/design-only.

## Biggest blockers to plug-and-play status

The current repo is blocked from plug-and-play use by Sparkbot, Arc Bot, LIMA-Robo-OS, and future bot/robot/drone shells because it lacks:

1. A top-level `LimaKernel` or equivalent app object that shells can instantiate.
2. A single shell integration contract that accepts normalized task/intent metadata and returns a safe result object.
3. A minimal runtime service graph for Guardian, capability profile, event emission, and dry-run results.
4. A real fail-closed Guardian policy stub behind a kernel boundary.
5. A redacted in-memory event stream or durable Spine implementation.
6. Provider/model adapter interfaces with at least one non-executing, dry-run-safe example path.
7. A working example shell proving dependency use from outside the package.
8. A persistence backend or explicit in-memory runtime store.
9. A HumanInput to IntentEnvelope bridge runtime.
10. Shell manifests and capability profiles for Sparkbot, Arc Bot, Robo-OS, or any generic shell.
11. Real action boundary enforcement beyond contracts and fakes.
12. Packaging/demo evidence that an external repo can install and call LIMA as a dependency.

Audit answer:

- What blocks shells from using LIMA as a plug-and-play dependency? There is no callable kernel/app integration object, no runtime service composition, no durable or in-memory runtime event service, no real Guardian policy stub exposed through a shell API, no example shell, no provider/driver/storage implementation, and no shell-facing execution result API.

## Recommended next branch

Recommended next branch:

`design-lima-kernel-plugin-contract`

Reason:

- The audit finds a specific runtime-shaped gap: LIMA needs a small, explicit, Guardian-first kernel/plugin contract before implementation expands.
- This branch can define the shell-facing `LimaKernel` or app object contract, capability profile inputs, fail-closed Guardian policy stub contract, redacted in-memory event contract, and dry-run `ExecutionResult` shape without adding behavior.

Implementation branch only if Phil explicitly approves implementation scope:

`implement-lima-minimal-kernel-runtime`

If approved, the first minimal runtime branch must stay non-executing and should only introduce a top-level `LimaKernel` or app object that can:

- accept already-normalized intent/task metadata
- apply capability-profile checks
- call a Guardian policy stub/fail-closed decision path
- emit redacted in-memory events
- return a dry-run `ExecutionResult`
- avoid model calls, external calls, tool execution, persistence, adapters, Sparkbot wiring, and physical-world behavior unless separately approved

Audit answer:

- What is the safest recommended next branch? `design-lima-kernel-plugin-contract`. Use `implement-lima-minimal-kernel-runtime` only after explicit Phil approval.

## Validation run

Validation performed on this branch:

- `python3 --version` failed because `python3` is not available on this Windows checkout.
- `python --version` passed: Python 3.12.10.
- `python -m compileall lima` passed.
- `python -m pytest -q` failed during collection because `.pytest_cache` is not accessible in this checkout: `PermissionError: [WinError 5] Access is denied`.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2371 tests.
- `git diff --check` passed.

## Commit

This audit is intended as a docs-only branch commit. The final local commit hash is reported outside this file to avoid self-referential hash churn.

## Pushed yes/no

No.
