# Adaptive Trust Gates

## Purpose

This document defines future adaptive trust gate doctrine for LIMA AI OS.

Adaptive trust gates are future doctrine only in this phase. No trust-gate engine, approval engine, runtime enforcement, GuardianDecision behavior, Sparkbot wiring, ARC Bot behavior, custom bot behavior, robot control, or audit persistence is implemented here.

## Future Gate Categories

- `silent_or_logged`: low-risk, reversible, low-sensitivity actions may proceed with logging in a future runtime.
- `normal_confirmation`: medium-risk actions may ask for a simple user confirmation.
- `screen_confirmation`: screen-based high-risk digital actions may require explicit screen approval.
- `step_up_auth`: higher-risk digital actions may require PIN, passkey, operator confirmation, or equivalent future step-up.
- `companion_device_confirmation`: sensitive actions may require confirmation from a trusted companion device.
- `voice_challenge_confirmation`: voice actions may require voice confirmation, challenge phrase, known-speaker confidence, or companion-device approval.
- `dual_control`: high-impact actions may require two authorized operators.
- `dry_run_required`: consequential actions may require a non-executing preview, simulation, or plan review.
- `physical_safety_interlock_required`: physical-world actions may require environmental checks, interlocks, emergency stop support, simulation, and stricter operator confirmation.
- `breakglass_required`: rare emergency or privileged override path.

## Risk Dimensions

- reversibility
- data sensitivity
- financial impact
- security impact
- operational impact
- physical-world consequence
- actor trust
- environment trust
- shell type
- tool or driver capability

## Channel Examples

### Screen-based

Screen-based actions can use normal confirmation, screen confirmation, step-up auth, companion device confirmation, or dual control depending on risk.

### Voice-based

Voice actions may need voice challenge confirmation, known-speaker confidence, repeated intent, or companion-device approval when risk increases.

### Physical World

Physical-world actions require stricter treatment: dry run where possible, environmental checks, physical interlocks, emergency stop support, operator confirmation, and deterministic driver safety in later phases.

## Breakglass Posture

Breakglass remains an emergency or privileged override. It should not become the normal product UX. Users want low-risk work to flow with minimal interruption, while high-risk work should receive the least-friction safe gate that still protects people, systems, data, and operations.

## Non-runtime Boundary

This document does not:

- implement adaptive trust enforcement
- implement a policy engine
- implement an approval engine
- implement GuardianDecision behavior
- implement runtime execution
- change existing breakglass behavior
- authorize physical-world action
