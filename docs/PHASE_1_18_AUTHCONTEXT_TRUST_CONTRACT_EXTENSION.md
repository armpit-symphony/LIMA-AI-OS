# Phase 1.18 AuthContext / Trust Contract Extension

## Purpose

Add contract-level types for identity, session, trusted device context, identity confidence, and owner-autonomy context.

This phase does not implement live auth, trusted device enforcement, or autonomy enforcement.

## Core Rule

References are not authority.

`actor_ref`, `session_ref`, `trusted_context_ref`, `autonomy_notes`, and privacy metadata remain passive unless resolved through future verified contracts and Guardian policy.

## New Contracts

Phase 1.18 adds descriptive auth/trust contracts in `lima.contracts.auth`.

Enums:

- `TrustLevel`: unknown, untrusted, low, medium, high, owner verified, operator verified.
- `IdentityFactor`: known device, login session, voice match, face match, operator PIN, hardware key, location context, behavior pattern, biometric signal, future BCI signal, manual operator review, unknown.
- `SessionStatus`: unknown, active, expired, revoked, suspicious, locked.
- `AutonomyAuthority`: none, passive metadata, owner profile required, policy required, Guardian required.

Dataclasses:

- `TrustedDeviceContext`: describes trusted-context references, device/session/actor refs, trust level, confidence, verification timestamps, signals, anomaly flags, and metadata.
- `IdentityConfidence`: describes identity confidence score, factors, required threshold, pass/fail state, expiry, and metadata.
- `SessionContext`: describes session reference, actor reference, shell, session status, timestamps, scope, and metadata.
- `OwnerAutonomyContext`: describes owner autonomy references, profile reference, autonomy level, authority posture, capability references, constraints, and metadata.

Protocol:

- `TrustContextProtocol`: exposes describe-only methods for trusted context, identity confidence, session context, and owner-autonomy context.

## Non-Goals

- no live auth
- no session lookup
- no trusted device enforcement
- no autonomy enforcement
- no PIN verification
- no face/voice recognition implementation
- no BCI/thought interpretation
- no production Sparkbot adapter
- no Guardian enforcement

## TrustedDeviceContext Rules

`TrustedDeviceContext` describes signals and confidence only.

It does not:

- approve actions
- reduce risk by itself
- bypass Guardian
- verify identity by itself
- authorize critical actions

## IdentityConfidence Rules

`IdentityConfidence` records confidence factors.

It does not:

- log a user in
- verify a PIN
- perform face/voice recognition
- approve actions
- bypass Guardian

BCI/thought-adjacent signals:

- biometric
- confirm-only
- cannot directly approve execution
- cannot directly control tools/drivers/robots
- cannot bypass Guardian

## SessionContext Rules

`SessionContext` describes session state and scope.

It does not:

- create a live session
- verify a live session
- approve actions
- authorize high/critical behavior by itself

## OwnerAutonomyContext Rules

`OwnerAutonomyContext` references owner autonomy profile/capability rules.

It does not:

- enforce autonomy
- approve actions
- reduce risk by itself
- override law/human safety
- override Guardian

## Future Adapter Use

Future Sparkbot adapter work may carry refs to these contracts.

But production adapter remains blocked until:

- identity/session mapping is reviewed
- trusted context resolution is designed
- autonomy profile resolution is designed
- privacy/redaction enforcement is designed
- Guardian enforcement is designed

## Acceptance Criteria

- contract types exist
- docs describe passive nature
- no live auth/session/trust/autonomy behavior
- no Sparkbot imports
- no enforcement methods
- tests validate contract shape and forbidden methods
- references remain not authority
