# Governed execution grant

`lima.contracts.governed_execution_grant` is the one contract in LIMA that can
carry execution authority. Everything else in the kernel decides; this is the
only thing that permits.

## Why it is a separate contract

A `GovernedDecision` cannot authorize execution and never will. Its
`__post_init__` rejects any execution flag, and `to_dict` pins
`execution_allowed`, `side_effects_allowed`, and `executable` to `False`.

That invariant is load-bearing, so the grant was added as a **separate type**
rather than by relaxing the decision. No existing consumer starts authorizing
execution merely because it received a decision — a consumer that never asks
for a grant cannot be handed one by accident.

## Shape

| Constant | Value |
|---|---|
| `GRANT_CONTRACT` | `lima.governed_execution_grant` |
| `GRANT_VERSION` | `v0.1` |
| `GRANT_MODE` | `single_use_operator_gated` |
| `MAX_TTL_SECONDS` | `300` |

A grant names exactly one capability, tenant, worker, and action type. It is
bound to the Guardian decision and the governed decision that produced it, is
short-lived, and is single-use.

`requires_operator_opt_in` is pinned `True` in v0.1 and a grant that tries to
waive it fails construction. A grant is therefore a **necessary** condition
for execution and never a sufficient one.

## Issuing

```python
from lima.runtime import issue_execution_grant, ExecutionGrantDenied
```

Only a decision with status `allowed_dry_run` is grantable. Every precondition
denies with a fixed reason code — `guardian_binding_required`,
`decision_not_allowed`, `approval_still_required`, `capability_required`,
`ttl_invalid`, and so on — so a refusal is always attributable.

Issuing a grant performs no execution, no provider call, and no side effect.

## Consuming

The consumer must check the grant against what it *asked for*, not against
what the grant claims. Arc derives the expected capability from the action it
submitted and compares; a grant naming a different capability is refused with
`execution_grant_binding_mismatch`. Reading the capability back off the grant
would make the check compare the grant to itself.

Single use is enforced at the Supervisor by a SQLite `UNIQUE` constraint on
`(tenant_id, worker_id, grant_id, nonce)`, so a replayed grant loses the race
rather than being honoured twice.

## The second gate

A valid grant still does nothing unless the consumer has been independently
opted in by an operator. In this stack that is two separate flags held by two
separate parties, both defaulting off:

- Office: `--execution-opt-in` (will it issue a grant at all)
- Arc: `--execute-granted-capability` (will it honour one)

Lima-Office proves all four combinations in CI, including each denial:
`execution_grant_absent`, `arc_execution_opt_in_disabled`, and
`document_root_not_configured`. A gate nobody has watched fail is not a gate
worth trusting.

## Current capability scope

`document_read` only, bounded to a configured document root with path
containment resolved before the check, and a 1 MB ceiling. The consumer
returns byte counts and identifiers — never document content.

Additional capabilities are each their own reviewed change.

See also: [GOVERNED_STACK_MAP.md](GOVERNED_STACK_MAP.md).
