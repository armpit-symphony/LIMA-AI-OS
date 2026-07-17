# V1-G36 Bounded Consumer Integration Design

Date: 2026-06-17
Branch: `v1-g36-bounded-consumer-integration-design`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_metadata_only_bounded_design_slice`

V1-G36 implements the approved LIMA-side metadata-only bounded consumer integration design slice. It defines candidate design boundaries for a future Sparkbot and Arc-Bot-shell integration lane without implementing consumer integration.

This implementation does not edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer test files, call adapter symbols, import consumer runtime modules, wire shells, call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G36` template.

Approved implementation branch:

- `v1-g36-bounded-consumer-integration-design`

Approved scope:

- `bounded_consumer_integration_design_slice`

## Bounded Design Result

The V1-G36 design result is:

- `candidate_bounded_design_defined_for_future_patch_preview_gate`

This result means a candidate design boundary exists for a future patch-preview gate. It does not approve consumer repository edits, consumer integration, shell wiring implementation, provider/model dispatch, connector/browser/network authority, physical-world behavior, or product readiness.

## Reviewed Evidence

The fixture links:

- V1-G35 consumer integration compatibility review evidence
- V1-G35 closeout evidence
- V1-G35 audit evidence
- V1 runtime authority chain through G35
- V1 readiness rollup through G35
- V1 post-G35 next lane decision matrix

## Bounded Design Records

Sparkbot:

- Bounded design record id: `bounded-consumer-integration-design:v1-g36:sparkbot:001`
- Consumer repository: `sparkpit-labs/Sparkbot`
- Reviewed consumer branch: `v1-g34-live-consumer-import-call`
- Reviewed consumer commit evidence: `cee164655e1603f5e68b6df9773dc5b08dd27ca0`
- Source compatibility review record: `consumer-integration-compatibility-review:v1-g35:sparkbot:001`
- Design result: `candidate_bounded_design_defined_for_future_patch_preview_gate`
- Consumer integration approved: no
- Consumer repo mutation added: no
- Consumer runtime modules imported: no
- Provider/model calls added: no

Arc-Bot-shell:

- Bounded design record id: `bounded-consumer-integration-design:v1-g36:arc-bot-shell:001`
- Consumer repository: `armpit-symphony/Arc-Bot-shell`
- Reviewed consumer branch: `v1-g34-live-consumer-import-call`
- Reviewed consumer commit evidence: `61404a3bf7d95a45138ebd97992bcebe61651d79`
- Source compatibility review record: `consumer-integration-compatibility-review:v1-g35:arc-bot-shell:001`
- Design result: `candidate_bounded_design_defined_for_future_patch_preview_gate`
- Consumer integration approved: no
- Consumer repo mutation added: no
- Consumer runtime modules imported: no
- Provider/model calls added: no

## Candidate File-Map Categories

V1-G36 defines only candidate future file-map categories. It does not edit files in those categories.

- `lima_evidence_docs_tests_fixtures`
- `consumer_static_test_fixtures_after_future_edit_gate`
- `consumer_static_tests_after_future_edit_gate`
- `consumer_shell_adapter_boundary_after_future_shell_wiring_gate`
- `lima_runtime_boundary_after_future_runtime_gate`

Every category beyond LIMA evidence docs/tests/fixtures requires a future exact approval gate before any file is created, edited, removed, or renamed.

## Handoff Contracts

The design records these handoff contracts as design-only:

- `candidate_import_surface_contract`
- `consumer_fixture_contract`
- `consumer_smoke_test_contract`
- `lima_evidence_packet_contract`
- `rollback_checkpoint_contract`
- `guardian_authority_boundary_contract`

Each handoff contract requires a future exact gate before implementation. None of these contracts creates runtime authority, consumer repo edit authority, shell wiring authority, provider/model authority, connector/browser/network authority, physical-world authority, or product-readiness authority.

## Future Required Gates

The fixture records these future gates as required and blocked:

- `consumer_integration_patch_preview_approval_request`
- `consumer_repository_edit_approval_request`
- `consumer_integration_import_smoke_approval_request`
- `shell_wiring_design_approval_request`
- `provider_model_dispatch_approval_request`
- `connector_browser_network_authority_approval_request`
- `physical_world_authority_approval_request`
- `product_readiness_approval_request`

The next narrow step after audit/readiness is a future patch-preview gate request. V1-G36 does not approve that request or its implementation.

## LIMA Files Added

V1-G36 changed only these LIMA-AI-OS files:

- `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN.md`
- `docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g36_bounded_consumer_integration_design.json`
- `tests/test_v1_g36_bounded_consumer_integration_design.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or executed by the implementation.

## Consumer Files Added

No Sparkbot or Arc-Bot-shell file was created, edited, removed, renamed, imported, or executed by V1-G36.

## Remaining Gaps

The bounded design records these remaining gates:

- `patch_preview_not_approved`
- `consumer_repository_edit_not_approved`
- `consumer_integration_not_approved`
- `shell_wiring_implementation_not_approved`
- `provider_model_dispatch_not_approved`
- `secret_credential_access_not_approved`
- `connector_browser_network_authority_not_approved`
- `physical_world_authority_not_approved`
- `product_readiness_not_approved`

## Required Distinction

V1-G36 separates:

- metadata-only bounded consumer integration design: implemented
- future patch-preview gate request: proposed but not approved
- consumer repository edits: not approved and not implemented
- consumer integration: not approved and not implemented
- adapter symbol calls: not approved and not executed
- consumer runtime module imports: not approved and not implemented
- shell runtime wiring implementation: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- secret lookup or credential access: not approved and not implemented
- raw sensitive content persistence in LIMA evidence: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Bounded consumer integration design added: yes.
- Metadata design only: yes.
- Future patch-preview gate proposed: yes.
- Consumer integration approved: no.
- Consumer integration added: no.
- `lima/` runtime files changed: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Adapter symbols called: no.
- Consumer runtime modules imported: no.
- Shell runtime wiring implementation added: no.
- Live provider/model calls added: no.
- Model request dispatch added: no.
- Fallback execution added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution outside local tests added: no.
- Action execution added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Raw sensitive content persisted in LIMA evidence: no.
- Product readiness approved: no.

## Readiness Result

V1-G36 is ready for independent audit.

The next smallest safe step is a separate V1-G36 audit branch. After audit and readiness rollup, the next approval gate may request consumer integration patch-preview evidence. Do not proceed to consumer repository edits, consumer integration, shell wiring implementation, provider/model dispatch, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
