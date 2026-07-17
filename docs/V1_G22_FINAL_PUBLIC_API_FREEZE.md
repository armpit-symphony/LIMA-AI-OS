# V1-G22 Final Public API Freeze

Date: 2026-06-17
Branch: `v1-g22-final-public-api-freeze`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_final_public_api_freeze_docs_tests_fixtures_slice`

V1-G22 implements the approved LIMA-side final public API freeze docs/tests/fixtures slice. It freezes the current candidate public import surfaces as metadata and tests so Sparkbot, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and future shells can test against a stable V1 import contract.

This implementation does not edit `lima/` runtime files, clean up runtime exports, edit consumer repositories, import consumer code, call consumer runtimes, wire Sparkbot, wire Arc-Bot-shell, wire LIMA Robo OS, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G22_FINAL_PUBLIC_API_FREEZE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G22` template.

Approved implementation branch:

- `v1-g22-final-public-api-freeze`

Approved runtime scope:

- `final_public_api_freeze_docs_tests_fixtures_slice`

## Approved Files

V1-G22 changed only:

- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md`
- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- `tests/test_v1_g22_final_public_api_freeze.py`

No `lima/` runtime file was created, edited, removed, renamed, or cleaned up.

## Frozen Public Surfaces

The freeze fixture records the current `__all__` surfaces for:

- `lima`
- `lima.contracts`
- `lima.kernel`
- `lima.guardian`
- `lima.spine`
- `lima.persistence`
- `lima.shells.contracts`
- `lima.harness`
- `lima.adapters`

The tests compare those frozen exports to the current local package and verify the frozen symbols are importable locally.

## V1 Runtime Symbols Frozen

The fixture records V1 candidate runtime symbols across:

- V1-G11 runtime request metadata
- V1-G11 Guardian decision gate metadata
- V1-G12 audit/evidence metadata
- V1-G12 local audit store metadata
- V1-G14 destructive approval enforcement metadata
- V1-G15 shell/harness guiderail metadata
- V1-G16 guarded file mutation policy metadata
- V1-G17 file mutation preview/diff metadata
- V1-G18 consumer proof packet audit-intake metadata
- V1-G19 live approval evidence/capture metadata
- V1-G20 provider/model routing authority metadata
- V1-G21 consumer integration compatibility/freeze metadata

This freeze records compatibility expectations only. It is not runtime export cleanup, consumer integration, live import authority, provider/model dispatch, connector authority, physical-world authority, or product readiness.

## Required Distinction

V1-G22 separates:

- final public API freeze evidence: implemented as docs/tests/fixtures
- runtime export cleanup: not approved and not implemented
- `lima/` runtime file changes: not approved and not implemented
- consumer repo edits: not approved and not implemented
- live consumer imports/calls: not approved and not implemented
- consumer runtime wiring: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- product readiness: not approved and not claimed

## Freeze Policy

- Current public exports are frozen as `CANDIDATE_ONLY` V1 import surfaces.
- Future public API changes require a new explicit gate.
- Runtime export cleanup requires a separate approval gate.
- Consumer repository edits require a separate approval gate.
- Live consumer imports/calls require a separate approval gate.
- Provider/model dispatch requires a separate approval gate.
- Connector/browser/network/device/physical-world authority requires separate approval gates.

## Boundaries

- Final public API freeze docs/tests/fixtures added: yes.
- `lima/` runtime files changed: no.
- Runtime export cleanup approved: no.
- Runtime export cleanup added: no.
- Consumer repo mutation added: no.
- Consumer file writes added: no.
- Consumer code imports added: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Action execution added: no.
- File mutation execution added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Product readiness approved: no.

## Readiness Result

V1-G22 is ready for independent audit.

The next smallest safe step is a separate V1-G22 audit branch. Do not proceed to runtime export cleanup, consumer repo edits, live consumer imports/calls, consumer integration, live provider/model calls, secret lookup, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
