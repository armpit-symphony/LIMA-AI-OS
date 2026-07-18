# Arc Loopback Ollama Runtime v1.1

This document defines the narrow LIMA Runtime contract that allows an Arc
local-model preview to reach a caller-injected loopback Ollama executor. It is
an expansion of the published fake-executor baseline, not a generic provider,
network, connector, tool, or action framework.

## Public API

    from lima.harness import execute_v1_live_provider_model_call

The public callable shape remains
Callable[[Mapping[str, Any]], Mapping[str, Any]]. LIMA validates the request
before invoking the consumer-supplied callable and returns a normalized
dict[str, Any].

LIMA contains no Ollama HTTP client, provider SDK client, credential lookup,
cloud fallback, or endpoint discovery in this contract.

## Executor kinds

Arc runtime requests use an explicit executor_kind:

- fake
- loopback_ollama

Executor safety is never inferred from a substring in executor_ref.
Historical Arc v0.9 requests with the exact in_process_fake_executor reference
remain compatible as fake. New consumers should always send executor_kind.

## Loopback Ollama request

loopback_ollama is accepted only when all of these conditions hold:

- runtime_consumer is exactly arc_bot_shell;
- requested_action is exactly arc.local_model_preview;
- the Guardian decision has a non-empty decision_id, allow status,
  allowed=true, and requires_approval=false;
- executor_kind is exactly loopback_ollama;
- network_scope is exactly loopback_only;
- credentials_used=false;
- external_side_effects=false;
- endpoint is an HTTP base URL using exactly 127.0.0.1 or localhost with an
  explicit valid port;
- model is non-empty;
- normalized_request is a non-empty bounded request mapping.

Paths other than an empty path or /, URL credentials, queries, fragments,
HTTPS, wildcard addresses, LAN/private addresses, public addresses, remote
hostnames, malformed ports, and missing ports are rejected before invocation.

The executor receives the validated endpoint, model, network scope, false
credential/side-effect flags, normalized request, evidence references, and
the exact Guardian decision and decision_id.

## Successful result

A successful executor result must report:

- provider=ollama;
- the same non-empty model and normalized loopback endpoint;
- non-empty output_text;
- network_called=true;
- network_scope=loopback_only;
- ollama_called=true;
- credentials_used=false;
- external_side_effects=false;
- status=completed;
- optional non-negative duration_ms;
- no error category or message.

LIMA preserves these fields in the normalized result and preserves sanitized
metadata, excluding model output, in the evidence mapping. The Guardian
decision_id is unchanged in the executor input, normalized result, Guardian
decision mapping, and evidence mapping.

## Controlled unavailable result

An invoked executor may return status=unavailable with no output text and one
of these sanitized categories:

- service_unavailable
- model_unavailable
- timeout
- malformed_response
- executor_error

The error message must be a short, single-line, sanitized message. Raw
exception traces, raw prompts, credentials, secrets, and sensitive customer
payloads are not accepted. A raised executor exception becomes the controlled
public error "provider executor failed" without chaining the raw exception.

## Denied surfaces

Guardian deny and approval-required decisions never reach the executor. The
contract does not authorize external email, files, browsers, connectors,
devices, robotics, office-system actions, credentials, cloud providers, LAN
or public network endpoints, arbitrary HTTP execution, fallback, or hidden
background work.

The installed-package proof uses an in-process Ollama-shaped callable and
performs no real network request:

    python scripts/prove_arc_loopback_ollama_runtime.py
