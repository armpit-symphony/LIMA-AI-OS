# V1-G18 Consumer Proof Packet Audit Intake Approval Request

Date: 2026-06-16
Branch: `prepare-v1-consumer-proof-packet-audit-intake-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, touch consumer repositories, import consumer code, wire consumers, call consumer runtimes, route providers/models, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, mutate files outside this LIMA branch, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G18 implementation of the LIMA-side consumer proof packet audit intake slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G17, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G18 Objective

Implement the smallest LIMA-side consumer proof packet audit intake slice.

The slice should define how LIMA receives, normalizes, and audits proof packet metadata from separate consumer teams without editing those consumer repositories.

Consumer packet families covered:

- Sparkbot proof packet intake
- Arc Bot proof packet intake
- LIMA Robo OS proof packet intake
- LIMA Office proof packet intake
- future shell/harness proof packet intake

## Required Artifact Fields

Each received packet should provide metadata for:

- consumer name
- consumer repository URL or repository identifier
- consumer branch/ref
- consumer commit SHA
- proof packet path
- audit packet path
- machine-readable fixture or summary path
- validation commands and reported results
- proposed import/call shape evidence
- normalized metadata examples
- capability profile expectations
- Guardian/approval boundary expectations
- dry-run and non-execution confirmation
- explicit confirmation that no live consumer runtime path calls LIMA yet
- explicit confirmation that no tool/model/connector/browser/file/network/scheduled task/external send/device/robot/drone/IoT/physical-world bypass is claimed
- independent audit requirement
- received/missing/blocked packet status

## Required Distinction

V1-G18 must clearly separate:

- LIMA-side proof packet intake and audit metadata
- future consumer integration approval
- actual consumer runtime wiring

Consumer integration remains blocked until proof packets, audits, final API freeze, and explicit integration approval land.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/guardian/v1_consumer_proof_packet_intake.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE.md`
- `docs/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g18_consumer_proof_packet_audit_intake.json`
- `tests/test_v1_g18_consumer_proof_packet_audit_intake.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G18 may add only deterministic local non-executing proof packet metadata validation.

Allowed if approved:

- validate required proof packet artifact fields
- validate repository/ref/commit/path evidence metadata
- validate proposed import/call shape evidence as evidence only
- validate normalized metadata examples
- validate capability profile expectations
- validate Guardian/approval boundary expectations
- validate dry-run and non-execution confirmations
- validate no live consumer runtime path calls LIMA yet
- validate no bypass claims for tool/model/connector/browser/file/network/scheduled task/external send/device/robot/drone/IoT/physical-world behavior
- validate independent audit requirement
- normalize packet status values: `received`, `missing`, `blocked`, `rejected`, `accepted_static_evidence`
- produce a LIMA-side status ledger record
- reject raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, credentials, and customer data

## Explicitly Forbidden

V1-G18 must not add:

- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- live provider/model routing
- tool execution
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- file mutation execution
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- approval-token issuance
- raw PIN verification or persistence
- final API freeze
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- fixture records `CANDIDATE_ONLY`
- required artifact fields are enforced
- Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, and future shell packet families are represented
- repo/ref/commit/path evidence is required
- proposed import/call shape evidence is accepted only as evidence
- normalized metadata examples are required
- capability profile expectations are required
- Guardian/approval boundary expectations are required
- dry-run and non-execution confirmation is required
- no live consumer runtime path calls LIMA yet
- bypass claims fail closed
- independent audit requirement is enforced
- received/missing/blocked packet statuses are normalized
- no consumer repo mutation is added
- no consumer integration is added
- raw sensitive content fails closed

## Rollback Plan If Approved

Rollback must remove only:

- `lima/guardian/v1_consumer_proof_packet_intake.py`
- V1-G18 candidate exports added to `lima/guardian/__init__.py`
- V1-G18 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G18 files
- consumer repo work is required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- proof packet metadata can grant runtime authority
- raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, credentials, or customer data can persist or emit
- live provider/model routing is added
- connector/browser/network/device/robotics/physical-world behavior is added
- file mutation execution is added
- scheduled task execution is added
- external sends are added
- final API freeze is claimed
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Final API freeze approved: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g18-consumer-proof-packet-audit-intake` and implement only the approved LIMA-side proof packet audit intake metadata slice. Do not touch consumer repos or implement consumer integration.
