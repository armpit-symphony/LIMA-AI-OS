# Phase 1.3 Vault/Auth Fake Providers

## Purpose

Define test-only fake providers for Auth, Vault, and Breakglass contracts.

These providers let LIMA validate contract shape without touching real Sparkbot auth/vault behavior.

## Non-Goals

- no live auth
- no PIN verification
- no raw secrets
- no encryption/decryption
- no vault DB/storage
- no breakglass enforcement
- no Sparkbot imports
- no Guardian Suite implementation copied
- no production use

## Fake Provider Rules

- in-memory only
- metadata only
- no external services
- no environment reads
- no file reads/writes
- no DB
- no real secret values
- no execution/enforcement behavior

## Provider Summary

### FakeAuthProvider

`FakeAuthProvider` stores `AuthActor` and `AuthContext` objects in memory. It can describe actors, describe contexts, and evaluate `AuthRequirement` records using a simple fake auth-level ordering for tests.

It does not log in users, verify PINs, call external auth, open sessions, or read deployment state.

### FakeVaultProvider

`FakeVaultProvider` stores only `VaultSecretRef` metadata in memory. It can describe a secret reference and return a `VaultAccessDecision` for a `VaultAccessRequest`.

It does not store, read, decrypt, encrypt, or return secret values.

### FakeBreakglassProvider

`FakeBreakglassProvider` stores `BreakglassSessionRef` metadata in memory. It can record and describe session references.

It does not authorize, enforce, bypass, or create runtime privileges.

## Safety Notes

`FakeVaultProvider` stores only `VaultSecretRef` metadata. It cannot return secret values because no secret value field exists.

`FakeBreakglassProvider` records session metadata only. It does not authorize, enforce, or bypass anything.

`FakeAuthProvider` evaluates fake `AuthRequirement` records only for tests. It does not log in users or verify PINs.

## Future Path

Future adapter work must remain explicit and reviewed.

Do not wrap live Sparkbot `ChatUser`, PIN, breakglass, vault DB, or decryption behavior until a later safety review.
