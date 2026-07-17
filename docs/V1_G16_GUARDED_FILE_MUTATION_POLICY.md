# V1-G16 Guarded File Mutation Policy

Date: 2026-06-16
Branch: `v1-g16-guarded-file-mutation-policy`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_policy_contract_slice`

V1-G16 implements the approved guarded file mutation policy contract slice. It validates policy metadata for file edit/delete/file-mutation requests and returns a deterministic non-executing policy record.

This implementation does not read user files, write files, delete files, apply patches, execute tools, route providers/models, wire shells, activate HumanInput, invoke connectors, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G16_GUARDED_FILE_MUTATION_POLICY_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G16` template.

Approved implementation branch:

- `v1-g16-guarded-file-mutation-policy`

Approved runtime scope:

- `guarded_file_mutation_policy_contract_slice`

## Runtime Files

- `lima/guardian/v1_file_mutation_policy.py`
- `lima/guardian/__init__.py`

## Runtime Symbols

- `V1FileMutationPolicyError`
- `validate_v1_guarded_file_mutation_policy`

## Behavior Added

V1-G16 adds one deterministic local policy validator:

- requires file edit/delete/file-mutation request classification
- requires destructive mutation classification
- requires mutation intent scope and target path normalization metadata
- requires workspace/root boundary metadata
- requires path traversal, absolute path, and outside-workspace rejection metadata
- requires shell/harness-provided file authority metadata
- requires operator approval evidence expectations
- requires dry-run preview expectations
- requires diff/patch preview expectations
- requires rollback expectations
- requires destructive delete confirmation expectations
- requires audit/evidence linkage with proof-not-authority semantics
- requires tenant, shell, actor, and session scope
- returns a deterministic `record_hash`
- keeps execution and side-effect flags false

## Required Distinction

V1-G16 separates:

- policy/authority contract: implemented as local metadata validation
- preview/dry-run behavior: required by policy, not implemented here
- actual file mutation execution: not approved and not implemented

## Fail-Closed Cases

The validator rejects:

- missing request classification
- missing mutation intent scope
- missing shell/harness file authority
- missing operator approval evidence requirements
- missing workspace/root boundary metadata
- missing path traversal rejection metadata
- missing destructive delete confirmation policy
- missing rollback expectations
- missing dry-run preview expectations
- missing diff/patch preview expectations
- missing audit/evidence linkage
- mutation without approval policy
- mutation outside approved scope
- path traversal targets
- absolute paths, drive paths, and home paths
- mismatched normalized target path metadata
- raw secrets, raw prompts, raw file contents, raw diff/patch content, approval PINs, approval tokens, and customer data
- forged execution authority claims
- provider/model/tool/browser/network/device/robotics/physical-world claims
- consumer integration claims

## Boundaries

- Runtime behavior added: yes, only the approved local non-executing policy contract validator.
- Actual file mutation execution added: no.
- File read behavior added: no.
- File write behavior added: no.
- File delete behavior added: no.
- Patch application behavior added: no.
- Preview/dry-run runtime behavior added: no.
- Approval-token issuance added: no.
- Raw PIN verification added: no.
- Raw file content persistence added: no.
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

V1-G16 is ready for independent audit.

The next smallest safe step is a separate V1-G16 audit branch. Do not proceed to actual file mutation execution, preview/diff runtime behavior, consumer integration, shell wiring, provider/model routing, final API freeze, or product-readiness claims from this implementation branch.
