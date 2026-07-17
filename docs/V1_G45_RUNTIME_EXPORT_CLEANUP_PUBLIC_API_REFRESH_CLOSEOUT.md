# V1-G45 Runtime Export Cleanup Public API Refresh Closeout

Date: 2026-06-17
Branch: `v1-g45-runtime-export-cleanup-public-api-refresh`
API status: `CANDIDATE_ONLY`

Closeout verdict: `complete_pending_independent_audit`

V1-G45 is complete as an approved runtime export cleanup/public API refresh slice. It exposes the existing V1-G44 live provider/model call authority symbols through `lima.harness.__all__` and refreshes the V1-G22 final public API freeze fixture to match the candidate public harness export surface.

## Completed Scope

Runtime file changed:

- `lima/harness/__init__.py`

Docs/tests/fixtures changed:

- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g45_runtime_export_cleanup_public_api_refresh.json`
- `tests/test_v1_g45_runtime_export_cleanup_public_api_refresh.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

No Sparkbot file changed.

No Arc-Bot-shell file changed.

## Public Harness Export Refresh

The refreshed `lima.harness.__all__` candidate export list is:

- `V1ProviderModelRoutingAuthorityError`
- `validate_v1_provider_model_routing_authority`
- `V1LiveProviderModelCallAuthorityError`
- `validate_v1_live_provider_model_call_authority`

The existing V1-G20 harness exports remain present and importable. The existing V1-G44 symbols are now explicit public harness exports. No existing frozen harness export was removed or renamed.

## Validation Evidence

Required validation for this implementation:

- `python -m pytest -q tests\test_v1_g45_runtime_export_cleanup_public_api_refresh.py -p no:cacheprovider`
- `python -m pytest -q tests\test_v1_g45_runtime_export_cleanup_public_api_refresh.py tests\test_v1_g45_runtime_export_cleanup_public_api_refresh_approval_request.py tests\test_v1_g44_live_provider_model_call_authority.py tests\test_v1_g22_final_public_api_freeze.py tests\test_v1_g20_provider_model_routing_authority.py -p no:cacheprovider`
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`

## Boundary Results

- Runtime export cleanup/public API refresh: complete.
- V1-G22 final public API freeze fixture refreshed: yes.
- Validator behavior changed: no.
- New validator added: no.
- Live provider/model call execution added: no.
- Actual model request dispatch execution added: no.
- Network calls added: no.
- Provider readiness network checks added: no.
- Token Guardian live routing added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Fallback execution added: no.
- Tool execution added: no.
- Action execution added: no.
- Consumer repository edits added: no.
- Consumer runtime calls added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Raw content, secret, credential, customer data, raw diff, or full patch body persistence added: no.
- No product-readiness or production-readiness claim.

## Rollback

Rollback is local and reversible:

- remove `V1LiveProviderModelCallAuthorityError` from `lima.harness.__all__`
- remove `validate_v1_live_provider_model_call_authority` from `lima.harness.__all__`
- restore `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json` to the pre-G45 harness export list
- remove the V1-G45 implementation docs/tests/fixture

Rollback does not require consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Next Step

Create an independent V1-G45 audit branch. Do not proceed to live provider/model execution, provider network egress, secret or credential value access, fallback execution, connector/browser/network authority, physical-world authority, consumer repository edits, or product-readiness claims without a later explicit approval gate.
