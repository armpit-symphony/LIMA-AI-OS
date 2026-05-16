# Phase 32.2 Next-Slice Safety And Scope Comparison

Phase 32.2 compares the Phase 32.1 candidate next lanes against safety, scope, testability, rollback, usefulness, and readiness.

This phase is docs/tests/fixtures-only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, and does not approve Phase 33 runtime implementation.

## Comparison Summary

| Option | Safety | Scope | Testability | Rollback | Usefulness | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| A: `runtime_state` test-only hardening | Highest | docs/tests/fixtures only | High | Simple test/doc revert | Strengthens Phase 30 boundary | Ready |
| B: second read-only runtime inspection slice | Medium | would require new or existing runtime file scope | Needs more design | Runtime rollback required | Potentially useful | Not ready |
| C: non-executing candidate preview helper | Medium-low | could touch candidate/runtime semantics | Needs stricter HumanInput boundary proof | Runtime rollback required | Useful later | Not ready |
| D: candidate status read-only normalization hardening | Medium | could touch existing runtime files | Existing coverage already strong | Runtime rollback required | Limited immediate value | Not ready |
| E: HumanInput bridge boundary planning | High if planning-only | docs/tests/fixtures only | High | Simple test/doc revert | Useful as planning | Separate lane |
| F: Sparkbot integration boundary planning | High if planning-only | docs/tests/fixtures only | High | Simple test/doc revert | Useful as planning | Separate lane |
| G: pause and preserve state | High | docs/tests/fixtures only | High | Simple test/doc revert | Useful only if risk exists | Not required |

## Decision

Option A remains the safest immediate Phase 33 direction because it:

- requires no runtime implementation
- requires no `lima/` changes
- requires no `tests/support/` changes
- directly strengthens the completed Phase 30 `runtime_state` slice
- is deterministic and offline
- can prove nested suspicious metadata remains non-authoritative and non-executing
- can be rolled back by removing only Phase 33 docs/tests/fixtures

## Runtime Implementation Criteria

Phase 32.2 does not recommend immediate Phase 33 runtime implementation.

A future runtime implementation should not be proposed unless it is at least as bounded as Phase 30 and can prove all of the following before implementation:

- exact runtime file scope
- no external calls
- no filesystem/environment/shell/browser/network/database access
- no background worker, queue, daemon, subprocess, or thread
- no approval, execution, dispatch, audit persistence, or mutation
- no HumanInput runtime bridge behavior
- no Sparkbot wiring/imports
- no live adapter
- no robotics or physical-world behavior
- deterministic output from caller-provided data only
- safe defaults for missing, malformed, unknown, suspicious, and bypass-worded input

## Phase 33 Scope If Option A Is Approved

Implementation file scope: none.

Allowed Phase 33 paths under Option A:

- `docs/PHASE_33_*.md`
- `tests/fixtures/runtime_extraction/phase_33_*.json`
- `tests/test_phase_33_*.py`
- README and roadmap/state docs only if required by repository convention

Forbidden Phase 33 paths under Option A:

- all `lima/` files
- all `tests/support/` files
- new runtime modules
- helper behavior changes

## Continue

Continue only to Phase 32.3 Phase 33 eligibility and test plan matrix.
