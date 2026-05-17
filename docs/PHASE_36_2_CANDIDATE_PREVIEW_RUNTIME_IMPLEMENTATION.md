# Phase 36.2 Candidate Preview Runtime Implementation

Phase 36.2 adds the approved narrow candidate preview runtime helper.

Runtime scope changed only in:

- `lima/kernel/candidate_preview.py`
- `lima/kernel/__init__.py` for safe public exports of `CandidatePreview` and `preview_candidate`

The helper is deterministic, local-only, read-only, non-authoritative, non-executing, side-effect free, and based only on caller-provided data. It does not approve, execute, dispatch, persist, mutate, read files, write files, read environment variables, call shell/browser/network/database/external systems, start background work, bridge HumanInput, wire Sparkbot, activate live adapters, or connect to robotics or physical-world systems.

## Behavior

`preview_candidate` returns inspectable preview metadata. Benign caller-provided data may produce a `proposed` preview, but every output remains non-authoritative and non-executing.

Missing, malformed, unknown, suspicious, nested, or bypass-worded input produces a blocked, invalid, or needs-review safe preview. Suspicious caller-provided claims are recorded as `blocked_claims` and never become authority.

## Safe Export

`lima/kernel/__init__.py` changed only to export the approved helper and immutable preview structure by existing package convention.

## Continue

Continue only to Phase 36.3 candidate preview boundary regression review.
