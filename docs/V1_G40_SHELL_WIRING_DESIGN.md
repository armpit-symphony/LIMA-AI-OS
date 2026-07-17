# V1-G40 Shell Wiring Design

Date: 2026-06-17
Branch: `v1-g40-shell-wiring-design`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_metadata_only_shell_wiring_design_slice`

V1-G40 implements the approved LIMA-side shell wiring design slice. It creates deterministic docs/tests/fixtures that map future Sparkbot and Arc-Bot-shell shell boundaries without implementing shell runtime wiring.

This implementation does not edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, edit consumer runtime/source files, persist raw patch bodies, call adapter symbols, import consumer runtime modules, implement consumer integration, implement shell runtime wiring, call providers/models, dispatch model requests, execute fallback, read secrets, access credentials, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw sensitive content in LIMA evidence, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G40_SHELL_WIRING_DESIGN_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G40` template.

Approved implementation branch:

- `v1-g40-shell-wiring-design`

Approved scope:

- `shell_wiring_design_slice`

## Design Result

The V1-G40 design result is:

- `metadata_only_shell_boundary_maps_created`

This result means LIMA now has static design evidence describing future shell boundary maps for Sparkbot and Arc-Bot-shell. It does not approve shell runtime wiring implementation, consumer integration implementation, provider/model dispatch, connector/browser/network authority, physical-world behavior, or product readiness.

## Shell Boundary Records

Sparkbot:

- Shell boundary record id: `shell-wiring-design:v1-g40:sparkbot:001`
- Consumer repository: `sparkpit-labs/Sparkbot`
- Source import-smoke record: `consumer-integration-import-smoke:v1-g39:sparkbot:001`
- Boundary role: `sparkbot_product_shell_boundary`
- Design result: `metadata_only_shell_boundary_map_created`
- Shell wiring implementation approved: no
- Consumer integration implementation approved: no

Arc-Bot-shell:

- Shell boundary record id: `shell-wiring-design:v1-g40:arc-bot-shell:001`
- Consumer repository: `armpit-symphony/Arc-Bot-shell`
- Source import-smoke record: `consumer-integration-import-smoke:v1-g39:arc-bot-shell:001`
- Boundary role: `arc_office_shell_boundary`
- Design result: `metadata_only_shell_boundary_map_created`
- Shell wiring implementation approved: no
- Consumer integration implementation approved: no

## Boundary Map Summary

The static boundary maps define future design intent only:

- Shells remain outside the LIMA Runtime trust boundary until a future exact gate approves runtime integration.
- Future shell requests must enter through a Guardian-gated boundary before any model, tool, file, connector, browser/network, or physical-world action.
- Future shell-to-LIMA calls must be bounded to approved public contract surfaces.
- Future shell wiring must produce audit evidence for request intake, Guardian decision, approval state, model/tool routing metadata, and result delivery.
- Future shell wiring must keep secrets, credentials, provider tokens, connector tokens, and approval factors outside static evidence.
- Future shell wiring must not bypass Guardian, Harness, approval policy, model routing authority, tool-pack scoping, or audit persistence.

## Linked Evidence

The fixture links:

- V1-G39 consumer integration import-smoke evidence
- V1-G39 closeout evidence
- V1-G39 audit evidence
- V1 runtime authority chain through G39
- V1 readiness rollup through G39
- V1 post-G39 next-lane decision matrix
- V1-G38 consumer repository edit records
- V1-G37 patch-preview records

## Future Required Gates

The fixture records these future gates as required and blocked:

- `consumer_integration_implementation_approval_request`
- `shell_wiring_implementation_approval_request`
- `provider_model_dispatch_approval_request`
- `connector_browser_network_authority_approval_request`
- `physical_world_authority_approval_request`
- `product_readiness_approval_request`

The next narrow step after audit/readiness is a future consumer integration implementation approval request. V1-G40 does not approve that request or implementation.

## LIMA Files Added

V1-G40 changed only these LIMA-AI-OS files:

- `docs/V1_G40_SHELL_WIRING_DESIGN.md`
- `docs/V1_G40_SHELL_WIRING_DESIGN_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g40_shell_wiring_design.json`
- `tests/test_v1_g40_shell_wiring_design.py`

No `lima/` runtime file was created, edited, removed, renamed, imported, or executed by the implementation.

## Consumer Files Added

No Sparkbot or Arc-Bot-shell file was created, edited, removed, renamed, imported, or executed by V1-G40.

## Remaining Gaps

The shell wiring design records these remaining gates:

- `consumer_integration_implementation_not_approved`
- `shell_wiring_implementation_not_approved`
- `provider_model_dispatch_not_approved`
- `secret_credential_access_not_approved`
- `connector_browser_network_authority_not_approved`
- `physical_world_authority_not_approved`
- `product_readiness_not_approved`

## Required Distinction

V1-G40 separates:

- shell wiring design evidence: approved and implemented
- shell runtime wiring implementation: not approved and not implemented
- consumer integration implementation: not approved and not implemented
- adapter symbol calls: not approved and not executed
- consumer runtime module imports: not approved and not implemented
- provider/model dispatch: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- secret lookup or credential access: not approved and not implemented
- raw sensitive content persistence in LIMA evidence: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Shell wiring design evidence added: yes.
- Metadata-only shell boundary maps added: yes.
- Shell wiring implementation approved: no.
- Shell wiring implementation added: no.
- Consumer integration implementation approved: no.
- Consumer integration implementation added: no.
- `lima/` runtime files changed: no.
- Sparkbot files changed: no.
- Arc-Bot-shell files changed: no.
- Consumer runtime/source files changed: no.
- Raw patch bodies persisted: no.
- Adapter symbols called: no.
- Consumer runtime modules imported: no.
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

V1-G40 is ready for independent audit.

The next smallest safe step is a separate V1-G40 audit branch. After audit and readiness rollup, the next approval gate may request consumer integration implementation authority. Do not proceed to consumer integration implementation, shell wiring implementation, provider/model dispatch, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
