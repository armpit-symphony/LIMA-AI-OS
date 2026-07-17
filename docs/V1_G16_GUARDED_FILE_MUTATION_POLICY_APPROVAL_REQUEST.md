# V1-G16 Guarded File Mutation Policy Approval Request

Date: 2026-06-15
Branch: `prepare-v1-guarded-file-mutation-policy-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, mutate files, create patch application behavior, wire shells, touch consumers, route providers/models, activate HumanInput, invoke connectors, execute browser/network/device/robotics/physical-world behavior, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G16 implementation of the guarded file mutation policy contract slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G15, readiness rollups, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G16 Objective

Implement the smallest guarded file mutation policy/authority contract slice.

The slice should define policy metadata for:

- file edit/delete request classification
- file mutation intent scope
- shell/harness-provided file authority
- user/operator approval evidence
- workspace/root boundary
- path traversal rejection
- destructive delete confirmation
- rollback expectations
- dry-run preview expectations
- diff/patch preview expectations
- audit/evidence linkage
- no raw secret/file-content persistence
- no mutation without approval
- no mutation outside approved scope
- no consumer integration

## Required Distinction

V1-G16 must clearly separate:

- policy/authority contract
- preview/dry-run behavior
- actual file mutation execution

Actual file mutation execution remains unapproved until a future exact operator decision.

## Approved Files If Operator Says Yes

Candidate policy files:

- `lima/guardian/v1_file_mutation_policy.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G16_GUARDED_FILE_MUTATION_POLICY.md`
- `docs/V1_G16_GUARDED_FILE_MUTATION_POLICY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g16_guarded_file_mutation_policy.json`
- `tests/test_v1_g16_guarded_file_mutation_policy.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G16 may add only deterministic local policy validation for file mutation authority metadata.

Allowed if approved:

- classify file edit/delete request metadata
- validate file mutation intent scope metadata
- validate shell/harness-provided file authority metadata
- validate operator approval evidence metadata
- validate workspace/root boundary metadata
- validate path traversal rejection metadata
- validate destructive delete confirmation metadata
- validate rollback expectation metadata
- validate dry-run preview expectation metadata
- validate diff/patch preview expectation metadata
- validate audit/evidence linkage metadata
- reject raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, and customer data
- prove no mutation can be marked allowed without approval evidence and scope metadata

## Explicitly Forbidden

V1-G16 must not add:

- actual file mutation execution
- file delete execution
- file overwrite execution
- patch application behavior
- user-file reads beyond tests/fixtures
- raw file content persistence
- consumer integration
- shell runtime wiring
- provider/model routing
- tool execution
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external sends
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
- request classification is required
- mutation intent scope is required
- shell/harness file authority metadata is required
- operator approval evidence metadata is required
- workspace/root boundary metadata is required
- path traversal rejection is represented
- destructive delete confirmation is represented
- rollback expectations are represented
- dry-run preview expectations are represented
- diff/patch preview expectations are represented
- audit/evidence linkage is represented
- mutation without approval fails closed
- mutation outside approved scope fails closed
- raw secrets and raw file contents fail closed
- no actual file mutation behavior is added
- no consumer integration is added

## Rollback Plan If Approved

Rollback must remove only:

- `lima/guardian/v1_file_mutation_policy.py`
- V1-G16 candidate exports added to `lima/guardian/__init__.py`
- V1-G16 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G16 files
- actual file mutation, delete, overwrite, or patch application is added
- path traversal could pass
- mutation without approval could pass
- mutation outside approved scope could pass
- raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, or customer data can persist or emit
- consumer repo changes are required
- shell runtime wiring is added
- provider/model routing is added
- connector/browser/network/device/robotics/physical-world behavior is added
- external sends are added
- final API freeze is claimed
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Actual file mutation behavior added: no.
- Preview/dry-run runtime behavior added: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/device/robotics/physical-world behavior added: no.
- Final API freeze approved: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g16-guarded-file-mutation-policy` and implement only the approved policy/authority contract slice. Do not implement actual file mutation execution.
