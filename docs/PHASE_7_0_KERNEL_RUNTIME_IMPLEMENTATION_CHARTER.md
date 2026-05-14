# Phase 7.0 Kernel Runtime Implementation Charter

Phase 7.0 opens Phase 7 as a no-code kernel runtime implementation charter lane. It defines the minimum safe future runtime implementation path for the LIMA Kernel without implementing runtime behavior.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Charter Decision

The smallest future runtime implementation slice that could be considered later is a non-executing kernel intake-to-candidate coordinator. It would only accept already-typed, explicit testable inputs and produce non-executable candidate metadata for Guardian review. It must not parse raw natural language, execute tools, enforce approval, persist audit, call models, call network services, mutate files, wire Sparkbot, or touch physical-world drivers.

Phase 7.0 does not approve that implementation. It only defines the charter for deciding whether a later phase may propose it.

## Future Runtime Slice Constraints

- Input must be typed and explicit, not inferred from raw natural language.
- Output must be non-executable candidate metadata.
- Candidate metadata must not authorize itself.
- GuardianDecision must remain the future authority boundary.
- Approval state must remain descriptive until a later approved enforcement phase.
- Audit/spine/memory must be designed before persistence is implemented.
- Sparkbot must remain reference/spec material unless a future phase approves integration.
- Robo-OS and physical-world behavior remain blocked.

## Required Preconditions Before Any Runtime Code

- Eligible and forbidden files must be mapped.
- Tests must be specified before implementation.
- Rollback expectations must be defined.
- Audit proof requirements must be defined.
- Allowed input and output shapes must be defined.
- Safety gates must be explicit.
- Approval boundaries must be explicit.
- Phil must explicitly approve the future runtime implementation scope.

## Next Gate

Phase 7.1 may map the first runtime slice eligibility as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
