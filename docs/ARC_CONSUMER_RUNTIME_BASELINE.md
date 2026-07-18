# Arc Consumer Runtime Baseline

This document defines the narrow public LIMA Runtime contract published for
Arc Bot v0.9. It remains the compatible fake-executor path after the v1.1
loopback Ollama expansion. The separate v1.1 contract is documented in
ARC_LOOPBACK_OLLAMA_RUNTIME_V1_1.md.

## Public API

```python
from lima.harness import execute_v1_live_provider_model_call
```

The entrypoint accepts a `Mapping[str, Any]` and a caller-injected callable. It
returns a normalized `dict[str, Any]`.

## Arc request contract

The Arc consumer request requires:

- `request_id`: non-empty Arc action identity.
- `runtime_consumer`: exactly `arc_bot_shell`.
- `requested_action`: exactly `arc.local_model_preview`.
- `guardian_decision`: an allow decision with a non-empty `decision_id`,
  `allowed=true`, and `requires_approval=false`.
- `executor_kind`: `fake` for new consumers.
- `executor_ref`: a non-empty executor evidence reference. Historical v0.9
  requests remain compatible only for the exact `in_process_fake_executor`
  reference when `executor_kind` is absent.
- `normalized_request`: a non-empty mapping containing the bounded Arc request
  context.
- `evidence_refs`: an optional sequence of evidence references.

The executor receives the exact Guardian `decision_id` and the normalized
Guardian decision. LIMA does not generate or replace this identity.

## Fake executor result contract

The in-process fake executor must return:

- non-empty `provider`, `model`, and `output_text` values;
- `network_called=false`;
- `credentials_used=false`;
- `ollama_called=false` when present.

The normalized LIMA record repeats the same `guardian_decision_id` at the top
level, in `guardian_decision`, and in `evidence`.

## Fail-closed boundary

LIMA rejects the request before executor invocation when the Guardian decision
is missing, has a missing or empty `decision_id`, is denied, or requires
approval. It also rejects malformed requests, unsupported consumers or actions,
unsupported executor kinds, executor exceptions, and malformed or unsafe
executor results. Executor kind is not inferred from a substring in the
executor reference.

The deterministic installed-package proof is:

```powershell
python scripts/prove_arc_consumer_baseline.py
```

This baseline is not product or production readiness and does not authorize a
real provider, Ollama, external network access, credentials, tools, connectors,
file mutation, browser control, device control, robotics, or office-system
actions.
