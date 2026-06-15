# V1-G15 Shell/Harness Guiderail Contract Approval Request

Date: 2026-06-15
Branch: `prepare-v1-shell-harness-guiderail-contract-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, change runtime behavior, wire consumers, route providers/models, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world actions, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G15 implementation of the shell/harness guiderail input contract slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. The V1-G14 audit, V1 invariant audit, authority-lane decision matrix, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G15 Objective

Implement the smallest candidate contract slice that lets shells and harnesses pass structured guiderail input to LIMA before future authority lanes expand.

The contract should define:

- capability profile
- guardrail mode
- approval policy
- actor scope
- session scope
- tenant scope
- shell scope
- allowed capability lanes
- destructive edit/delete policy
- file mutation policy
- provider/model policy
- connector policy
- browser/network policy
- physical-world policy
- emergency stop expectations
- rollback expectations
- dry-run versus execution-authorized posture
- operator approval evidence expectations
- audit/evidence linkage expectations

## Approved Files If Operator Says Yes

Candidate contract files:

- `lima/shells/contracts/v1_guiderail_input.py` (new)
- `lima/shells/contracts/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT.md`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g15_shell_harness_guiderail_contract.json`
- `tests/test_v1_g15_shell_harness_guiderail_contract.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G15 may add only deterministic local contract validation for guiderail input metadata. It may validate and normalize structured fields, but it must not wire shells or execute capabilities.

Allowed if approved:

- validate capability profile metadata
- validate guardrail mode metadata
- validate actor/session/tenant/shell scope metadata
- validate approval policy metadata
- validate allowed capability lane metadata
- validate destructive edit/delete and file mutation policy metadata
- validate provider/model policy metadata as policy metadata only
- validate connector policy metadata as policy metadata only
- validate browser/network policy metadata as policy metadata only
- validate physical-world policy metadata as blocked-until-dedicated-lane metadata
- validate emergency stop and rollback expectation metadata
- validate dry-run versus execution-authorized posture metadata
- validate operator approval evidence expectation metadata
- validate audit/evidence linkage expectation metadata
- reject raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, and customer data

## Explicitly Forbidden

V1-G15 must not add:

- consumer integration
- shell runtime wiring
- live provider/model routing
- model calls
- tool execution
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- file mutation, delete, overwrite, or external file action behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external sends
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- approval-token issuance
- raw PIN verification or persistence
- raw secret, prompt, file, customer, approval token, or PIN persistence
- approval metadata as broad execution authority
- runtime export cleanup
- final API freeze
- V1 product readiness or production readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- fixture records `CANDIDATE_ONLY`
- shell/harness guiderail input requires capability profile
- guardrail mode is required
- approval policy is required
- actor/session/tenant/shell scope is required
- allowed capability lanes are required
- destructive edit/delete policy is required
- file mutation policy is required
- provider/model policy is accepted only as policy metadata
- connector policy is accepted only as policy metadata
- browser/network policy is accepted only as policy metadata
- physical-world policy remains blocked until dedicated physical-world authority lane
- emergency stop and rollback expectations are represented where relevant
- dry-run versus execution-authorized posture is explicit
- operator approval evidence expectations are explicit
- audit/evidence linkage expectations are explicit
- raw sensitive content fails closed
- no runtime wiring or live execution is added

## Rollback Plan If Approved

Rollback must remove only:

- `lima/shells/contracts/v1_guiderail_input.py`
- V1-G15 candidate exports added to `lima/shells/contracts/__init__.py`
- V1-G15 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G15 files
- consumer repo changes are required
- shell runtime wiring is added
- live provider/model routing is added
- live HumanInput bridge behavior is activated
- connector, browser, network, file mutation, device, robotics, or physical-world behavior is added
- external sends are added
- raw sensitive content can persist or emit
- approval metadata becomes broad execution authority
- final API freeze is claimed
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Runtime implementation approved by this request: no.
- Operator approval recorded: no.
- Runtime behavior added: no.
- Guiderail contract implementation added: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g15-shell-harness-guiderail-contract` and implement only the approved V1-G15 candidate contract slice. If not approved, revise the request or keep LIMA at `CANDIDATE_ONLY`.
