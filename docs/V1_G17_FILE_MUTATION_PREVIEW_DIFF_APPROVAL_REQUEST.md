# V1-G17 File Mutation Preview/Diff Approval Request

Date: 2026-06-16
Branch: `prepare-v1-file-mutation-preview-diff-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, generate live previews, compute live diffs, read user files, write files, delete files, apply patches, wire shells, touch consumers, route providers/models, activate HumanInput, invoke connectors, execute browser/network/device/robotics/physical-world behavior, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G17 implementation of the file mutation preview/diff runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G16, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G17 Objective

Implement the smallest non-mutating file mutation preview/diff runtime slice.

The slice should define and validate metadata for:

- dry-run file mutation preview
- redacted diff/patch preview metadata
- no raw file content persistence
- no actual file write/delete
- path scope and workspace/root validation
- path traversal rejection
- rollback plan metadata
- approval evidence linkage
- user/operator confirmation linkage
- shell/harness policy linkage
- audit/evidence linkage
- test coverage expectations
- stop conditions

## Required Distinction

V1-G17 must clearly separate:

- guarded file mutation policy from V1-G16
- preview/dry-run metadata behavior for proposed file mutations
- actual file mutation execution

Actual file mutation execution remains unapproved until a future exact operator decision.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/guardian/v1_file_mutation_preview.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G17_FILE_MUTATION_PREVIEW_DIFF.md`
- `docs/V1_G17_FILE_MUTATION_PREVIEW_DIFF_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g17_file_mutation_preview_diff.json`
- `tests/test_v1_g17_file_mutation_preview_diff.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G17 may add only deterministic local non-mutating preview/diff metadata validation.

Allowed if approved:

- validate V1-G16-style guarded file mutation policy linkage
- validate path scope and workspace/root boundary metadata
- validate path traversal rejection metadata
- validate dry-run preview metadata
- validate redacted diff/patch preview metadata
- validate rollback plan metadata
- validate approval evidence linkage metadata
- validate user/operator confirmation linkage metadata
- validate shell/harness policy linkage metadata
- validate audit/evidence linkage metadata
- reject raw secrets, raw prompts, raw file contents, raw diff/patch contents, approval PINs, approval tokens, and customer data
- prove preview/diff metadata cannot mark actual mutation as executed or allowed

## Explicitly Forbidden

V1-G17 must not add:

- actual file mutation execution
- file delete execution
- file write execution
- file overwrite execution
- patch application behavior
- live filesystem mutation
- raw file content persistence
- raw diff or patch content persistence
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
- V1-G16 policy linkage is required
- dry-run preview metadata is required
- redacted diff/patch preview metadata is required
- raw file content persistence fails closed
- actual file write/delete/patch execution fails closed
- path scope and workspace/root validation metadata are required
- path traversal rejection is represented
- rollback plan metadata is required
- approval evidence linkage is required
- user/operator confirmation linkage is required
- shell/harness policy linkage is required
- audit/evidence linkage is required
- provider/model/tool/browser/network/device/robotics/physical-world claims fail closed
- no consumer integration is added

## Rollback Plan If Approved

Rollback must remove only:

- `lima/guardian/v1_file_mutation_preview.py`
- V1-G17 candidate exports added to `lima/guardian/__init__.py`
- V1-G17 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G17 files
- actual file mutation, delete, overwrite, write, or patch application is added
- preview/diff behavior requires raw file content persistence
- path traversal could pass
- preview/diff metadata can grant execution authority
- mutation without approval could pass
- mutation outside approved scope could pass
- raw secrets, raw prompts, raw file contents, raw diff/patch contents, approval PINs, approval tokens, or customer data can persist or emit
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
- Preview/diff runtime behavior added: no.
- Actual file mutation execution approved: no.
- Actual file mutation execution added: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/device/robotics/physical-world behavior added: no.
- Final API freeze approved: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g17-file-mutation-preview-diff` and implement only the approved non-mutating preview/diff metadata slice. Do not implement actual file mutation execution.
