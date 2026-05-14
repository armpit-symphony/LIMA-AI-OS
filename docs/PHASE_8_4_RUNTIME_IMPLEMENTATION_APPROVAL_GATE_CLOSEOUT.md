# Phase 8.4 Runtime Implementation Approval Gate / Closeout

Phase 8.4 closes the no-code Phase 8 implementation design review lane at a clean runtime implementation approval gate. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Completed Phase 8 Scope

- Phase 8.0 completed the Implementation Design Review Charter.
- Phase 8.1 completed the Exact Runtime File-Touch Map.
- Phase 8.2 completed the Runtime Acceptance Test Design.
- Phase 8.3 completed the Rollback / Audit Proof Plan.

## Designed Future Runtime Slice

The only future runtime implementation slice that Phase 8 designed is a non-executing kernel intake-to-candidate coordinator.

The future slice would be limited to typed explicit input metadata and non-executable candidate metadata output. It would not parse natural language, create real IntentEnvelope behavior, create real GuardianDecision behavior, enforce approval, execute, persist audit, call models, call tools, mutate files, access network/browser/shell surfaces, wire Sparkbot, or touch robotics/physical-world behavior.

## Future Eligible File Scope

If Phil later approves runtime implementation, the first slice must stay limited to the Phase 8.1 file-touch map:

- `lima/contracts/boundary.py`
- `lima/contracts/intent.py`
- `lima/contracts/guardian.py`
- `lima/contracts/events.py`
- `lima/contracts/privacy.py`
- `lima/__init__.py`, only if a public export is required
- `lima/kernel/__init__.py`, only as a new approved file
- `lima/kernel/intake_candidate.py`, only as a new approved file

Any need to touch `lima/adapters/**`, `lima/guardian/**`, `lima/harness/**`, `lima/io/**`, `lima/packs/**`, `lima/persistence/**`, `lima/services/**`, `lima/shells/**`, `lima/spine/**`, `tests/support/**`, Sparkbot files, or product/driver surfaces is outside the designed slice.

## Runtime Implementation Preconditions

Before future runtime code can be approved, the implementation charter must require:

- targeted tests for every touched file
- all Phase 8 gate tests
- full `python -m pytest -q`
- `python -m compileall lima`
- `git diff --check`
- explicit forbidden-path review
- rollback path documentation
- audit proof as test evidence only
- non-executable output markers
- no approval, execution, audit persistence, or driver handoff authority

## Still Out Of Scope

- Phase 5 HumanInput runtime bridge.
- Runtime HumanInput to IntentEnvelope bridge.
- Live adapter code.
- Sparkbot imports or wiring.
- Real IntentCompiler behavior.
- Real GuardianDecision behavior.
- Approval enforcement.
- Execution.
- Audit persistence.
- Shell, browser, network, file mutation, robotics, or physical-world side effects.
- Product shell implementation.
- Robo-OS integration.

## Approval Gate

Exact future runtime implementation approval question for Phil:

Do you approve a narrow Phase 9 runtime implementation slice limited to a non-executing kernel intake-to-candidate coordinator, touching only the Phase 8.1 eligible files, requiring the Phase 8.2 acceptance tests and Phase 8.3 rollback/audit proof, and still forbidding HumanInput runtime bridge behavior, Sparkbot wiring, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, audit persistence, shell/browser/network/file mutation, robotics, and physical-world action?

Until Phil explicitly answers yes to that narrow question, runtime implementation remains blocked.

## Recommended Next Options

- Option A: approve Phase 9 narrow runtime implementation slice exactly as scoped above.
- Option B: request another no-code review of the Phase 8 design package.
- Option C: return to Sparkbot integration boundary planning.
- Option D: return to Robo-OS / physical-world boundary planning.
- Option E: pause and preserve current state.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
