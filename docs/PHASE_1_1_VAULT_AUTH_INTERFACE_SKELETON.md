# Phase 1.1 Vault/Auth Interface Skeleton

## Purpose

Create non-executing Vault/Auth interfaces for LIMA Runtime.

This phase does not implement live vault storage, decryption, PIN verification, breakglass enforcement, DB migration, or secret migration.

The purpose is to define the seam that future Guardian code can depend on instead of Sparkbot-specific internals.

## Reference Commits Inspected

| Repo | Branch | Commit | Inspected paths | Modified? | Notes |
| --- | --- | --- | --- | --- | --- |
| LIMA-Guardian-Suite | `origin/main` | `0559d9a6ce7e3dc401185a6732a6c8fa123db477` | `app/services/guardian/auth.py`, `app/services/guardian/vault.py`, `guardian/`, `docs/`, `tests/` | No | Local checkout has pre-existing untracked cache/data and one local commit ahead of `origin/main`; inspection used fetched `origin/main` read-only. |
| Sparkbot | `origin/main` | `b59041d2946e8c121e76ab9af47d1fbea4bd90cb` | `backend/app/services/guardian/`, `backend/app/models.py`, `backend/app/crud.py`, `backend/app/services/`, `docs/` | No | Inspection confirmed current Sparkbot vault/auth behavior remains coupled to Sparkbot app models, env names, local data paths, and live vault/PIN behavior. |

## Current Coupling Summary

Phase 1.0 identified Vault/Auth as the first safe seam because the live behavior is security-critical and still tied to Sparkbot internals:

- `auth.py` depends on Sparkbot `ChatUser` and operator/breakglass env conventions.
- `vault.py` uses live SQLite-backed vault persistence/decryption and Sparkbot env/data paths.
- direct secret material, decryption behavior, and live DB storage are not safe to extract in this phase.
- future LIMA Guardian must depend on contracts/interfaces instead.

## Interface Goals

- represent actors/operators without Sparkbot `ChatUser` dependency
- represent auth context without Sparkbot DB/session dependency
- represent vault secret references without exposing raw secrets
- represent breakglass session metadata without enforcing it yet
- represent PIN/operator approval requirements without validating PINs yet
- keep all interfaces non-executing

## Non-Goals

- live authentication
- PIN hashing/verification
- operator login
- breakglass enforcement
- vault encryption/decryption
- vault DB/storage
- secret migration
- Sparkbot production integration
- Guardian policy enforcement
- real approval enforcement
- DB migrations
- CLI/API routes

## Proposed Contracts

### AuthActor

Fields:

- `actor_id`
- `actor_type`
- `display_name`
- `roles`
- `shell_id`
- `metadata`

### AuthContext

Fields:

- `actor`
- `session_id`
- `shell_id`
- `auth_level`
- `authenticated_at`
- `expires_at`
- `metadata`

### AuthRequirement

Fields:

- `requirement_id`
- `required_level`
- `reason`
- `risk_class`
- `action_type`
- `metadata`

### AuthDecision

Fields:

- `auth_decision_id`
- `requirement_id`
- `actor_id`
- `allowed`
- `auth_level`
- `reason`
- `created_at`
- `expires_at`
- `metadata`

### VaultSecretRef

Fields:

- `secret_ref`
- `secret_name`
- `namespace`
- `privacy_class`
- `redaction_class`
- `created_at`
- `expires_at`
- `metadata`

Important: `VaultSecretRef` never contains a raw secret value.

### VaultAccessRequest

Fields:

- `request_id`
- `actor_id`
- `shell_id`
- `decision_id`
- `approval_id`
- `secret_ref`
- `purpose`
- `risk_class`
- `metadata`

### VaultAccessDecision

Fields:

- `vault_decision_id`
- `request_id`
- `allowed`
- `reason`
- `constraints`
- `created_at`
- `expires_at`
- `metadata`

### BreakglassSessionRef

Fields:

- `breakglass_id`
- `actor_id`
- `shell_id`
- `decision_id`
- `approval_id`
- `reason`
- `scope`
- `created_at`
- `expires_at`
- `revoked_at`
- `metadata`

## Protocol Rules

### AuthProviderProtocol

- `describe_actor(actor_id) -> AuthActor | None`
- `describe_context(session_id) -> AuthContext | None`
- `evaluate_requirement(requirement, context) -> AuthDecision`

### VaultProviderProtocol

- `describe_secret(secret_ref) -> VaultSecretRef | None`
- `request_access(request) -> VaultAccessDecision`

### BreakglassProviderProtocol

- `describe_session(breakglass_id) -> BreakglassSessionRef | None`
- `record_session(session) -> None`

Important:

- Protocols do not enforce real auth.
- Protocols do not verify PINs.
- Protocols do not decrypt secrets.
- Protocols do not return raw secret values.
- Protocols do not execute privileged actions.

## Forbidden Patterns

- returning raw secret values
- storing raw secrets in events
- importing `app.crud` / `app.models` / `app.services`
- importing Sparkbot `ChatUser`
- opening Sparkbot DB sessions
- reading Sparkbot `vault.db` directly
- using Sparkbot deployment paths directly
- validating live operator PINs
- creating breakglass runtime sessions
- decrypting vault values
- executing tools after auth decision

## Future Extraction Path

Phase 1.1:

- contracts/interfaces only

Phase 1.2:

- add import-boundary tests for vault/auth provider skeletons
- strengthen the boundary with provider tests before any adapter skeletons

Phase 1.3:

- create adapter stubs that can wrap Sparkbot behavior later, still no live secrets

Phase 1.4+:

- implement test-only fake providers

Later:

- real persistence adapters
- real vault provider
- real auth provider
- real breakglass provider
- secret migration plan only after safety review

## Acceptance Criteria

- Auth contracts exist.
- Vault contracts exist.
- Breakglass reference contract exists.
- Protocols are non-executing.
- No raw secret value field exists.
- No Sparkbot imports are added.
- `tests/test_guardian_import_boundaries.py` still passes.
- No reference repo is modified.
- No runtime implementation is added.
