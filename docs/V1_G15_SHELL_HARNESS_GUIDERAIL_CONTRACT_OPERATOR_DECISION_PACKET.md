# V1-G15 Shell/Harness Guiderail Contract Operator Decision Packet

Date: 2026-06-15
Branch: `prepare-v1-shell-harness-guiderail-contract-approval-request`
API status: `CANDIDATE_ONLY`

Decision packet status: `awaiting_operator_decision`

This packet records the valid operator choices for the exact V1-G15 shell/harness guiderail input contract approval request. It does not change runtime behavior, modify `lima/`, approve implementation, wire shells, or approve product readiness by itself.

## Decision Source

The decision source is:

- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_APPROVAL_REQUEST.md`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_WORK_ORDER.md`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_PREFLIGHT_AUDIT.md`
- `docs/readiness/V1_NEXT_AUTHORITY_LANE_DECISION_MATRIX.md`

The approval request asks:

> Do you explicitly approve V1-G15 implementation of the shell/harness guiderail input contract slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

General product direction, the authority-lane matrix, this packet, or broad statements that guiderail input is needed do not count as implementation approval.

## Current Decision State

- Operator approval recorded: no.
- Implementation approved: no.
- Approved next implementation branch: `none`.
- Current next action: operator chooses exactly one valid option below.

## Decision Record

No operator choice has been recorded for implementation.

- Recorded choice: `none`
- Recorded approval wording: `none`
- Recorded revision request: `none`
- Recorded pause reason: `none`
- Approved implementation branch: `none`
- Implementation approved: no

## Decision Record Validation Rules

- `none`: valid only while every Decision Record field remains `none` and implementation approved remains `no`.
- `Approve-V1-G15`: valid only with the exact required approval wording, approved branch `v1-g15-shell-harness-guiderail-contract`, no revision request, no pause reason, and implementation approved set to `yes`.
- `Revise-V1-G15`: valid only with a non-empty revision request, no approval wording, no approved implementation branch, no pause reason, and implementation approved set to `no`.
- `Pause`: valid only with a non-empty pause reason, no approval wording, no approved implementation branch, no revision request, and implementation approved set to `no`.
- Any mixed state is invalid and must be treated as no approval.
- Missing, misspelled, or extra choice values are invalid and must be treated as no approval.
- Implementation may start only from the valid `Approve-V1-G15` state.

## Decision Record Templates

Use one template only.

Template for no recorded choice:

```text
Recorded choice: none
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: none
Implementation approved: no
```

Template for `Approve-V1-G15`:

```text
Recorded choice: Approve-V1-G15
Recorded approval wording: I explicitly approve V1-G15 implementation of the shell/harness guiderail input contract slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_APPROVAL_REQUEST.md.
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: v1-g15-shell-harness-guiderail-contract
Implementation approved: yes
```

Template for `Revise-V1-G15`:

```text
Recorded choice: Revise-V1-G15
Recorded approval wording: none
Recorded revision request: <required revision request>
Recorded pause reason: none
Approved implementation branch: none
Implementation approved: no
```

Template for `Pause`:

```text
Recorded choice: Pause
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: <required pause reason>
Approved implementation branch: none
Implementation approved: no
```

## Valid Operator Choices

### `Approve-V1-G15`

This choice is valid only if the operator explicitly approves the exact V1-G15 request scope.

Required approval wording:

`I explicitly approve V1-G15 implementation of the shell/harness guiderail input contract slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_APPROVAL_REQUEST.md.`

If recorded, the next branch may be:

- `v1-g15-shell-harness-guiderail-contract`

If recorded, the only approved scope is:

- `shell_harness_guiderail_input_contract_slice`

### `Revise-V1-G15`

This choice asks for a narrower or different request. It keeps implementation unapproved.

### `Pause`

This choice keeps LIMA at `CANDIDATE_ONLY` and does not start V1-G15 implementation.

## If `Approve-V1-G15` Is Recorded

Implementation must stay inside the already named V1-G15 scope:

- `lima/shells/contracts/v1_guiderail_input.py`
- `lima/shells/contracts/__init__.py`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT.md`
- `docs/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g15_shell_harness_guiderail_contract.json`
- `tests/test_v1_g15_shell_harness_guiderail_contract.py`

Any different file requires a new gate update before implementation.

## Recommended Next Step

Record exactly one operator choice in this packet.

If `Approve-V1-G15` is recorded, implement the approved candidate contract slice on branch `v1-g15-shell-harness-guiderail-contract`. Stop before consumer integration or any authority expansion beyond this contract.
