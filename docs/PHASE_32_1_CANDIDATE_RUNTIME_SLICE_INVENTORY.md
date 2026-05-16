# Phase 32.1 Candidate Runtime Slice Inventory

Phase 32.1 inventories candidate next lanes after the completed Phase 30 read-only `runtime_state` inspection slice.

This phase is docs/tests/fixtures-only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, and does not approve Phase 33 implementation.

## Inventory Result

Phase 32.1 reviewed seven candidate next lanes:

- Option A: runtime_state test-only hardening with nested suspicious metadata fixtures, no runtime implementation.
- Option B: second read-only runtime inspection slice that consumes caller-provided snapshot data only.
- Option C: non-executing candidate preview helper, local-only and non-authoritative, with no HumanInput bridge behavior.
- Option D: candidate status read-only normalization hardening only, if existing runtime files already support it safely.
- Option E: HumanInput bridge boundary planning only, no implementation.
- Option F: Sparkbot integration boundary planning only, no implementation.
- Option G: pause and preserve state if no next runtime slice is safe enough.

## Recommendation

Option A is the safest immediate Phase 33 direction.

Phase 33 should be a test-only hardening lane for the existing read-only `runtime_state` slice, focused on nested suspicious metadata fixtures and regression tests. It should not implement runtime code, change `lima/`, change `tests/support/`, add Sparkbot wiring, add HumanInput runtime bridge behavior, add live adapters, approve, execute, dispatch, persist, mutate files, call external services, start background work, or create physical-world behavior.

## Deferred Runtime Options

Options B, C, and D remain deferred until a later no-code design can prove exact runtime file scope, acceptance tests, rollback proof, and safety boundaries at least as small as Phase 30.

Options E and F are planning lanes only and should not be mixed with runtime implementation.

Option G is not required immediately because Phase 31 found no blocking safety regression, but pause remains available if later evidence introduces unresolved risk.

## Phase 33 Boundary Draft

If Phil approves Phase 33 under this recommendation, it should be limited to:

- `docs/PHASE_33_*.md`
- `tests/fixtures/runtime_extraction/phase_33_*.json`
- `tests/test_phase_33_*.py`
- README and roadmap/state docs only if required by repository convention

Forbidden for Phase 33 under this recommendation:

- no `lima/` changes
- no `tests/support/` changes
- no runtime implementation
- no Sparkbot wiring/imports
- no HumanInput runtime bridge behavior
- no live adapter
- no IntentCompiler or GuardianDecision runtime behavior changes
- no approval enforcement
- no execution
- no dispatch
- no audit persistence
- no shell/browser/network/file mutation/robotics/physical-world behavior
- no external service calls
- no background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects

## Continue

Continue only to Phase 32.2 next-slice safety and scope comparison.
