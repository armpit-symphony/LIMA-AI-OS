# V1-G17 File Mutation Preview/Diff

Date: 2026-06-16
Branch: `v1-g17-file-mutation-preview-diff`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_preview_diff_slice`

V1-G17 implements the approved non-mutating file mutation preview/diff runtime slice. It validates sanitized dry-run preview metadata and redacted diff/patch preview metadata for proposed file mutations that link back to a V1-G16 guarded file mutation policy record.

This implementation does not read user files, write files, delete files, overwrite files, apply patches, persist raw content, route providers/models, wire shells, activate HumanInput, invoke connectors, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G17_FILE_MUTATION_PREVIEW_DIFF_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G17` template.

Approved implementation branch:

- `v1-g17-file-mutation-preview-diff`

Approved runtime scope:

- `file_mutation_preview_diff_runtime_slice`

## Runtime Files

- `lima/guardian/v1_file_mutation_preview.py`
- `lima/guardian/__init__.py`

## Runtime Symbols

- `V1FileMutationPreviewError`
- `validate_v1_file_mutation_preview_diff`

## Behavior Added

V1-G17 adds one deterministic local preview/diff metadata validator:

- requires V1-G16 guarded file mutation policy linkage
- requires dry-run file mutation preview metadata
- requires redacted diff/patch preview metadata
- requires path scope validation metadata
- requires workspace/root validation metadata
- requires path traversal rejection metadata
- requires rollback plan metadata
- requires approval evidence linkage
- requires user/operator confirmation linkage
- requires shell/harness policy linkage
- requires audit/evidence linkage
- requires tenant, shell, actor, and session scope
- returns a deterministic `record_hash`
- keeps execution, side-effect, file read/write/delete/mutation/overwrite, and patch application flags false

## Required Distinction

V1-G17 separates:

- V1-G16 policy/authority contract: required as linked input
- preview/dry-run metadata behavior: implemented as sanitized validation
- actual file mutation execution: not approved and not implemented

## Fail-Closed Cases

The validator rejects:

- missing V1-G16 policy linkage
- mismatched policy record hash
- missing dry-run preview metadata
- missing redacted diff/patch preview metadata
- raw file content persistence claims
- raw diff or patch persistence claims
- actual file write/delete/mutation/overwrite or patch application claims
- missing path scope validation
- missing workspace/root validation
- missing path traversal rejection representation
- traversal, absolute, home, or drive paths
- missing rollback plan metadata
- missing approval evidence linkage
- missing user/operator confirmation linkage
- missing shell/harness policy linkage
- missing audit/evidence linkage
- raw secrets, prompts, file contents, diff/patch contents, approval PINs, approval tokens, and customer data
- provider/model/tool/browser/network/device/robotics/physical-world claims
- consumer integration claims

## Boundaries

- Runtime behavior added: yes, only the approved non-mutating preview/diff metadata validator.
- Actual file mutation execution added: no.
- File read behavior added: no.
- File write behavior added: no.
- File delete behavior added: no.
- File overwrite behavior added: no.
- Patch application behavior added: no.
- Raw file content persistence added: no.
- Raw diff/patch content persistence added: no.
- Approval-token issuance added: no.
- Raw PIN verification added: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/device/robotics/physical-world behavior added: no.
- External sends added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- Product readiness approved: no.

## Readiness Result

V1-G17 is ready for independent audit.

The next smallest safe step is a separate V1-G17 audit branch. Do not proceed to actual file mutation execution, consumer integration, shell wiring, provider/model routing, final API freeze, or product-readiness claims from this implementation branch.
