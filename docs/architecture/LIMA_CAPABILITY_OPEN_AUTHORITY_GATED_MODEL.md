# LIMA Capability-Open Authority-Gated Model

Date: 2026-06-15
Branch: `docs-lima-capability-open-authority-gated-posture`
API status: `CANDIDATE_ONLY`

LIMA AI OS is intended to govern broad capabilities across bots, shells, workstations, office systems, devices, robots, drones, IoT, automation, connectors, model routing, browser actions, network actions, file actions, and physical-world systems.

The architecture posture is capability-open and authority-gated.

## Core Posture

Capability-open means LIMA is designed to classify and govern any capability that a shell, harness, connector, driver, or future runtime exposes.

Authority-gated means a capability can be used only after the relevant authority lane, approval policy, actor/session/tenant scope, audit/evidence contract, safety boundary, and validation evidence exist.

A capability being blocked today means "not authorized by the current gate." It does not mean "impossible forever."

Dry-run and non-executing language applies to the current candidate lanes. It is not a statement that the long-term product vision is dry-run only.

## Shell And Harness Responsibilities

Shells and harnesses provide guiderail input that lets LIMA classify a request against the right boundary.

Shells and harnesses are expected to provide, when relevant:

- capability profiles
- guardrail mode or guiderail input options
- approval policy
- actor scope
- session scope
- tenant scope
- shell scope
- allowed capability lanes
- emergency-stop semantics
- rollback semantics
- dry-run versus execution-authorized posture
- evidence references

Shells and harnesses do not bypass LIMA authority. They supply the structured context LIMA needs to classify, gate, approve, audit, and prevent bypass.

## LIMA Responsibilities

LIMA's job is:

- request classification
- authority enforcement
- approval requirements
- audit/evidence linkage
- redaction
- tenant/shell/actor/session boundary checks
- bypass prevention
- proof that consequential work crossed the correct Guardian boundary

Guardian remains the syscall gate. Model calls, tool calls, file mutations, network actions, browser actions, connector writes, device actions, robot actions, drone actions, IoT actions, office actions, and physical-world systems must not bypass the relevant Guardian authority lane.

## Destructive Edit/Delete Policy

Destructive edit/delete/file mutation requires explicit approval unless a future approved policy lane defines otherwise.

Current V1 evidence proves only a local non-executing approval-enforcement gate. It does not approve file mutation execution.

Any future guarded file mutation policy lane must define:

- what counts as destructive edit/delete/file mutation
- which actors can approve it
- how approval evidence is recorded
- how replay, stale approval, revoked approval, denied approval, and scope mismatch fail closed
- how audit/evidence records stay proof instead of execution authority
- what rollback or recovery evidence must exist before execution can be considered

## Physical-World Policy

Physical-world behavior requires a dedicated physical-world authority and safety lane before it can be allowed.

Device, robot, drone, IoT, humanoid, vehicle, environmental, facilities, safety-critical, or other physical-world actions remain blocked until that dedicated lane defines:

- capability profile requirements
- operator authority requirements
- emergency-stop semantics
- dry-run and simulation expectations
- hazard and risk classification
- evidence and telemetry requirements
- rollback or mitigation expectations
- field safety validation
- explicit operator approval

## Consumer Integration Boundary

Consumer integration still requires proof packets, audits, final API freeze, and explicit integration approval.

Sparkbot, Sparkbot_shell, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and other consumer repositories must not be wired to LIMA runtime behavior until the required proof, audit, freeze, and integration gates are complete.

## What Current Blocking Means

When current V1 docs or tests say provider/model routing, tools, browser/network/file behavior, connectors, devices, robotics, physical-world behavior, shell wiring, or consumer integration are blocked, the intended meaning is:

- the current candidate lane does not authorize the capability
- the current tests must fail closed if that capability appears
- a future dedicated authority lane may approve the capability after its own contracts, tests, audit evidence, and operator approval

This is not product readiness. This document clarifies architecture posture only. It does not approve implementation, consumer integration, live execution, final API freeze, or production use.
