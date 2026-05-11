# Breakglass Evolution

## Purpose

This document describes how breakglass should evolve in the LIMA product doctrine.

This phase does not change existing breakglass behavior. It does not implement adaptive trust gates, approval enforcement, policy enforcement, GuardianDecision behavior, Sparkbot wiring, ARC Bot behavior, robot control, execution, or audit persistence.

## Old Mental Model

Risky action -> PIN or breakglass.

That model is useful for emergency or privileged override, but it is too blunt to become the normal product UX.

## Future LIMA Model

Intent -> risk/context evaluation -> least-friction safe gate -> interrupt only when needed.

Low-risk work should flow with minimal interruption. Medium-risk work may ask for confirmation. High-risk digital work may require screen approval, PIN, passkey, operator confirmation, companion-device confirmation, or dual control. Voice actions may need voice confirmation, challenge phrase, known-speaker confidence, or companion-device approval. Physical-world actions need environmental checks, interlocks, emergency stop support, dry run or simulation where possible, and stricter operator confirmation.

## Breakglass Role

Breakglass remains available as rare emergency or privileged override.

Breakglass should not be treated as the default approval path for normal product work.

PIN or passkey remains appropriate for some screen-based high-risk actions. Voice and physical-world contexts need different confirmation modes.

## Non-runtime Boundary

This document is doctrine only. It does not:

- change breakglass runtime behavior
- implement trust gates
- implement approvals
- implement execution
- create audit persistence
- authorize robot or physical-world action
