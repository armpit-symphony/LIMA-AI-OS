# V1-G16 Guarded File Mutation Policy Work Order

Date: 2026-06-15
Branch: `prepare-v1-guarded-file-mutation-policy-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_policy_contract_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, mutate files, or add runtime execution.

## Approval Dependency

V1-G16 implementation may start only after the operator explicitly approves:

`docs/V1_G16_GUARDED_FILE_MUTATION_POLICY_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/guardian/v1_file_mutation_policy.py`.
2. Add deterministic validators for guarded file mutation policy metadata.
3. Require file edit/delete request classification.
4. Require mutation intent scope.
5. Require shell/harness-provided file authority metadata.
6. Require operator approval evidence metadata.
7. Require workspace/root boundary metadata.
8. Require path traversal rejection metadata.
9. Require destructive delete confirmation metadata.
10. Require rollback expectations.
11. Require dry-run preview and diff/patch preview expectations.
12. Require audit/evidence linkage.
13. Reject raw sensitive content.
14. Keep actual file mutation execution unimplemented.
15. Add candidate exports only in `lima/guardian/__init__.py`.
16. Add V1-G16 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G16 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G16 file map
- actual file mutation, delete, overwrite, or patch application
- user-file reads beyond tests/fixtures
- raw file content persistence
- mutation without approval
- mutation outside approved scope
- consumer repo changes
- shell runtime wiring
- provider/model routing
- connector/browser/network/device/robotics/physical-world behavior
- external sends
- final API freeze
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G16 operator decision packet.

If approved, implement only the guarded file mutation policy/authority contract slice on branch `v1-g16-guarded-file-mutation-policy`. Actual file mutation execution remains unapproved.
