# Phase 4.0 Runtime Extraction Readiness Planning

Phase 4.0 starts Phase 4 as planning only.

It does not move runtime behavior, import Sparkbot, wire production routes, implement shell behavior, execute tools, call models, persist audit events, enforce approvals, or touch physical-world systems.

## Purpose

Phase 4.0 defines the safe sequence for approaching runtime extraction after Phase 3 closed the non-production kernel pipeline safety work.

The central question is:

Which runtime boundary can be safely approached first, and what contracts, fixtures, tests, and safety gates must exist before any behavior moves?

## Recommended First Boundary

The recommended first runtime-extraction readiness boundary is:

Sparkbot reference inventory refresh for runtime extraction planning.

This is not code movement. It is a read-only planning step to re-check Sparkbot as the spec before choosing an extraction target.

The refresh should focus on:

- HumanInput/chat/voice entrypoints.
- IntentEnvelope-adjacent payload shapes.
- Guardian request and fake GuardianDecision-adjacent paths.
- model routing boundaries.
- tool catalogue and tool-pack scoping boundaries.
- approval and breakglass surfaces.
- audit/spine lineage surfaces.
- terminal/PTY and operator control surfaces.
- file/browser/network action surfaces.
- robotics/Robo-OS-adjacent action surfaces, if present.

## Required Phase 4 Sequence

Phase 4 should proceed through readiness gates before moving behavior:

1. Phase 4.0 - Runtime Extraction Readiness Planning.
2. Phase 4.1 - Sparkbot Runtime Reference Refresh.
3. Phase 4.2 - Runtime Boundary Candidate Selection.
4. Phase 4.3 - Boundary Extraction Safety Gate.
5. Phase 4.4 - Boundary Fixture Contract Extension, if approved.
6. Phase 4.5 - Boundary Readiness Review.
7. Only after explicit approval: narrow non-production extraction or adapter work.

The exact numbering may change if a readiness review finds gaps. Do not skip reference refresh, candidate selection, or safety gates.

## Phase 4.0 GO

Phase 4.0 may add:

- planning documentation
- static planning fixture metadata
- static planning tests
- project tracking updates

## Phase 4.0 NO-GO

Phase 4.0 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot imports or wiring
- production route imports
- model calls
- tool execution
- terminal or PTY execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

## Sparkbot Handling

Sparkbot remains the spec and reference source.

During Phase 4.0, do not inspect local Sparkbot as part of implementation. The first safe place for Sparkbot inspection is Phase 4.1, and even then it must be read-only unless a later explicit phase approves code movement.

Local Sparkbot may contain dirty prototype code. Treat it as reference material, not a source to copy blindly.

## Phase 4.0 Decision

GO for Phase 4.1 Sparkbot Runtime Reference Refresh.

NO-GO for runtime extraction implementation.

NO-GO for Sparkbot integration.

NO-GO for product shell implementation.

NO-GO for physical-world action.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
