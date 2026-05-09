# Phase 1.2 Vault/Auth Provider Boundary Tests

## Purpose

Add boundary tests that protect future Vault/Auth provider work from leaking Sparkbot runtime internals or live secret/auth behavior into LIMA Runtime.

This phase does not implement providers.
This phase does not implement adapters.
This phase does not enforce auth.
This phase does not read/decrypt secrets.

## Reference Commits Inspected

| Repo | Branch | Commit | Inspected paths | Modified? | Notes |
| --- | --- | --- | --- | --- | --- |
| LIMA-Guardian-Suite | `origin/main` | `0559d9a6ce7e3dc401185a6732a6c8fa123db477` | `app/services/guardian/auth.py`, `app/services/guardian/vault.py`, `guardian/`, `docs/`, `tests/` | No | Latest `origin/main` was rechecked read-only. Auth remains coupled to `ChatUser` and Sparkbot env conventions; vault remains SQLite/decryption-backed. |
| Sparkbot | `origin/main` | `b59041d2946e8c121e76ab9af47d1fbea4bd90cb` | `backend/app/services/guardian/`, `backend/app/models.py`, `backend/app/crud.py`, `backend/app/services/`, `docs/` | No | Latest `origin/main` was rechecked read-only. Guardian auth/vault/breakglass behavior remains coupled to Sparkbot app models, DB/session paths, env conventions, and live PIN/vault behavior. |

## Boundary Risks Being Blocked

- Sparkbot `app.crud`/`app.models`/`app.services` imports
- `backend.app` imports
- Sparkbot `ChatUser` dependency
- Sparkbot DB/session access
- Sparkbot env/path coupling
- `vault.db` direct reads/writes
- raw secret fields
- `decrypt`/`encrypt`/`get_secret`/`read_value`/`write_value` methods
- `verify_pin`/`login`/`authenticate_live` methods
- `open_live_session`/`bypass`/breakglass enforcement methods
- side effects at import time
- external service calls from contracts/providers

## Test Strategy

1. Existing guardian import-boundary test remains.
2. New provider-boundary test scans LIMA provider/interface directories.
3. New raw-secret field test prevents unsafe dataclass fields.
4. New forbidden method-name test prevents live behavior from entering protocols.
5. Tests remain repo-local and do not inspect reference repos.
6. Tests do not require external services.

## Protected Paths

The boundary tests scan future local LIMA paths if they exist:

- `lima/guardian`
- `lima/contracts`
- `lima/persistence`
- `lima/services`
- `lima/io`
- `lima/adapters` if later created

Tests are safe when these paths are missing or minimal.

## Forbidden Import Patterns

- `app.crud`
- `app.models`
- `app.services`
- `backend.app`
- `from app`
- `import app`
- `Sparkbot`
- `sparkbot`
- `ChatUser`
- `chat.routes`
- `websocket`
- `app.api.routes.chat`
- direct Sparkbot DB/session strings such as `SPARKBOT_`, `vault.db`, `sqlmodel`, and `SQLModel`

## Forbidden Secret/Auth Method Patterns

- `get_secret`
- `decrypt`
- `encrypt`
- `read_value`
- `write_value`
- `return_secret`
- `verify_pin`
- `check_pin`
- `login`
- `authenticate_live`
- `open_live_session`
- `enforce`
- `execute`
- `bypass`

Important: the test scans code paths and protocol/class method names, not documentation.

## Forbidden Field Names

- `raw_secret`
- `secret_value`
- `plaintext`
- `password`
- `token`
- `api_key`
- `private_key`
- `credential`
- `decrypted_value`
- `cleartext`
- `value`

Important: tests focus on dataclass fields in Vault/Auth contracts, not arbitrary docs wording.

## Future Provider Rules

Future providers must:

- depend on LIMA contracts
- return references/metadata, not raw secrets
- avoid Sparkbot backend imports
- avoid side effects at import time
- be explicit adapters in later phases
- have separate tests proving no forbidden imports/methods/fields

## Acceptance Criteria

- provider boundary test exists
- forbidden import strings are blocked in local LIMA code paths
- forbidden secret/auth methods are blocked from protocols/classes where applicable
- forbidden raw secret field names are blocked from vault/auth dataclasses
- tests are safe with current minimal package layout
- no reference repo inspection occurs inside tests
- no runtime implementation is added
- no Sparkbot code copied
