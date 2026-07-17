# Arc Consumer Runtime Baseline

This document defines the narrow public LIMA Runtime contract published for
Arc Bot v0.9. It is a fake-executor-only integration boundary. It does not add
Ollama, a cloud provider, credentials, connector execution, or network access.

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
- `executor_ref`: a non-empty reference containing `fake`.
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
non-fake executor references, executor exceptions, and malformed or unsafe
executor results.

The deterministic installed-package proof is:

```powershell
python scripts/prove_arc_consumer_baseline.py
```

This baseline is not product or production readiness and does not authorize a
real provider, Ollama, external network access, credentials, tools, connectors,
file mutation, browser control, device control, robotics, or office-system
actions.
