# V1-G17 File Mutation Preview/Diff Work Order

Date: 2026-06-16
Branch: `prepare-v1-file-mutation-preview-diff-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_preview_diff_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, generate previews, compute diffs, mutate files, or add runtime execution.

## Approval Dependency

V1-G17 implementation may start only after the operator explicitly approves:

`docs/V1_G17_FILE_MUTATION_PREVIEW_DIFF_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/guardian/v1_file_mutation_preview.py`.
2. Add deterministic validators for non-mutating preview/diff metadata.
3. Require V1-G16 guarded file mutation policy linkage.
4. Require dry-run preview metadata.
5. Require redacted diff/patch preview metadata.
6. Require path scope and workspace/root boundary metadata.
7. Require path traversal rejection metadata.
8. Require rollback plan metadata.
9. Require approval evidence linkage metadata.
10. Require user/operator confirmation linkage metadata.
11. Require shell/harness policy linkage metadata.
12. Require audit/evidence linkage metadata.
13. Reject raw sensitive content, raw file content, and raw diff/patch content.
14. Keep actual file mutation execution unimplemented.
15. Add candidate exports only in `lima/guardian/__init__.py`.
16. Add V1-G17 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G17 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G17 file map
- actual file mutation, delete, overwrite, write, or patch application
- raw file content persistence
- raw diff or patch content persistence
- preview/diff metadata becoming execution authority
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

Record exactly one valid operator choice in the V1-G17 operator decision packet.

If approved, implement only the non-mutating file mutation preview/diff metadata slice on branch `v1-g17-file-mutation-preview-diff`. Actual file mutation execution remains unapproved.
