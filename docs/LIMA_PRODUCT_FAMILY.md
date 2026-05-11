# LIMA Product Family

## Purpose

This document defines non-runtime product-family doctrine for LIMA AI OS and the shells or consumers that may later sit on top of it.

It is reference metadata only. Product names do not imply implementation. Shell descriptions do not imply shell wiring. No Sparkbot import, ARC Bot implementation, custom bot generator, robot command, driver behavior, approval flow, execution path, or audit persistence is added by this document.

## Product Family Roles

### LIMA AI OS

LIMA AI OS is the trust-governed operating runtime and kernel underneath shells. It owns the long-term Guardian-gated runtime boundary, contracts, trust boundary, model harness, spine, drivers, tool packs, and persistence interface.

Current status: doctrine reference only.

Future status: governed runtime underneath approved shells and future driver-plane consumers.

### Sparkbot

Sparkbot is the open-source hobby/R&D shell and reference source for lessons learned. It is not the LIMA kernel. Some sensitive or commercial pieces may be removed before public release. Sparkbot remains a source of truth for extraction discipline, but this phase does not import Sparkbot, wire Sparkbot routes, or migrate Sparkbot behavior.

Current status: reference shell and R&D source.

Future status: one shell that may later run on top of LIMA AI OS after explicit approved integration phases.

### ARC Bot

ARC Bot is a future commercial office-worker shell under the LIMA AI / SparkPit Labs product family. It is intended for office, admin, IT, research, reporting, and workflow support.

Current status: future product doctrine only.

Future status: commercial shell that may later use LIMA AI OS contracts and trust gates.

### Custom Business And Private-Sector Bots

Custom business and private-sector bots are future client-specific shells. Each future shell may define its own shell manifest, tool-pack scope, policy profile, trust gates, and audit posture.

Current status: future shell doctrine only.

Future status: client-specific shells built on LIMA AI OS after explicit approved phases.

### Robo And Automation Consumers

Robo and automation systems are future deterministic driver-plane consumers. LIMA AI OS should govern intent, safety posture, policy, evidence, approvals, and command authorization. Deterministic drivers should handle physical execution in later phases.

Current status: future driver-plane doctrine only.

Future status: Guardian-gated deterministic driver consumers, with physical-world action blocked until explicit safety and driver phases.

### SparkPit Labs

SparkPit Labs is the product and service provider building the LIMA family.

## Non-runtime Boundary

This document does not:

- implement LIMA AI OS runtime behavior
- import Sparkbot
- wire Sparkbot
- implement ARC Bot
- generate custom business bots
- implement Robo-OS or robot control
- implement adaptive trust enforcement
- create GuardianDecision behavior
- approve, enforce, execute, or persist audit data

Contracts first. Guardian always. Sparkbot is the spec. Extract, do not rewrite. Robo-OS is a gated driver. LIMA Runtime is the kernel.
