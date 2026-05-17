# Phase 35.1 Second Runtime Slice Candidate Inventory

Phase 35.1 inventories possible second narrow runtime slices after the completed read-only `runtime_state` inspection slice.

This is no-code design review only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, and does not approve Phase 36 implementation.

## Candidate Inventory

| Option | Candidate | Inventory Result |
| --- | --- | --- |
| A | Test-only continuation / no second runtime implementation yet | Safe fallback if Phase 35 finds no implementation candidate with enough evidence. |
| B | Second read-only runtime inspection helper over caller-provided snapshot data only | Potentially safe, but lower usefulness because Phase 30 already covers read-only runtime state inspection. |
| C | Non-executing candidate preview helper over caller-provided data only | Strongest future design candidate if tightly bounded: local-only, read-only, non-authoritative, non-executing, inspectable, and safe-by-default. |
| D | Read-only candidate status normalization wrapper | Rejected for Phase 36 unless later evidence proves it can avoid modifying existing `candidate_status` behavior. |
| E | GuardianDecision read-only preview planning only | Planning-only candidate; not eligible for Phase 36 implementation because GuardianDecision behavior remains too authority-adjacent. |
| F | HumanInput bridge boundary planning only | Planning-only candidate; not eligible for implementation because HumanInput runtime bridge behavior remains gated. |
| G | Sparkbot integration boundary planning only | Planning-only candidate; not eligible for implementation because Sparkbot wiring/imports remain forbidden. |
| H | Pause and preserve state | Safe fallback if no candidate meets the Phase 35 eligibility bar. |

## Leading Future Candidate

Option C is the leading future Phase 36 candidate for design review purposes only: a non-executing candidate preview helper that accepts only caller-provided data and emits inspectable, non-authoritative, safe preview output.

It must not:

- bridge HumanInput to runtime behavior
- approve, execute, dispatch, or persist anything
- mutate files or runtime state
- call shell, browser, network, database, external service, robotics, or physical-world systems
- start workers, queues, daemons, subprocesses, or threads
- wire Sparkbot or live adapters
- change `runtime_state`, `intake_candidate`, or `candidate_status`
- change `tests/support`

## Possible Future Phase 36 File Scope

If Phase 35 evidence continues to support Option C, a future Phase 36 approval question may evaluate:

- a new `lima/kernel/candidate_preview.py`
- `lima/kernel/__init__.py` only if a safe public export is required by existing package convention
- Phase 36 docs/tests/fixtures only

This file scope is proposed only. Phase 35 does not touch it.

## Continue

Continue only to Phase 35.2 second-slice safety and scope comparison.
