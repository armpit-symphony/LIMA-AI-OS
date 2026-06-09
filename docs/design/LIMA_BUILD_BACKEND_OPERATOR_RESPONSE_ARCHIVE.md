# LIMA Build Backend Operator Response Archive

## Branch

`design-lima-build-backend-operator-response-archive`

## Purpose

This document defines how a future branch should archive an operator response to the LIMA build-backend environment
approval request.

The current package build blocker remains:

- `pyproject.toml` declares build backend `setuptools.build_meta`
- `pyproject.toml` declares build requirement `setuptools>=68`
- the active Python 3.12 environment has pip
- `setuptools` is not installed
- direct import of `setuptools.build_meta` fails
- local no-network wheel build proof remains blocked

This branch is design-only. It does not record an actual operator response, install dependencies, create environments,
run build tooling, build wheels, publish packages, modify package metadata, touch runtime files, touch consumer
repositories, wire Sparkbot or Arc Bot, or claim package/product readiness.

## Archive Principle

An archived operator response is evidence, not execution.

The archive may document what the operator approved, declined, or withheld. It must not itself perform environment
preparation, dependency installation, backend provisioning, wheel proof, package publication, Sparkbot proof, Arc Bot
proof, or product-readiness promotion.

If the response is missing, ambiguous, partial, contradictory, or unsafe, the archive result must be blocked.

## Source Request

The archived response must trace back to:

- `docs/design/LIMA_BUILD_BACKEND_OPERATOR_APPROVAL_REQUEST.md`
- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_APPROVAL_REQUEST_READINESS_REVIEW.md`
- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_APPROVAL_REQUEST_AUDIT.md`
- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_APPROVAL_REQUEST_STATIC_TESTS_AUDIT.md`

The archive must preserve the original decision set:

- approved: existing backend-ready environment
- approved: prepare controlled local environment
- approved: use operator-provided offline source
- declined / keep blocked

No archive path may infer approval from silence.

## Future Archive Shape

A later response-archive branch should add one audit document, and optionally one response transcript if the repo
standard allows archiving it.

Preferred future files:

- `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_AUDIT.md`
- optional `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_SOURCE.md`

The optional source file may contain the operator-provided response only if it contains no secrets, tokens, private
filesystem credentials, registry credentials, private URLs requiring credentials, or sensitive environment details.
Otherwise the archive must contain a redacted summary and note that sensitive source material was withheld.

## Required Archive Fields

The future archive audit must record:

- source request path
- response source or redacted reference
- operator decision
- target environment path or identifier
- network access allowed: yes/no/not supplied
- dependency installation allowed: yes/no/not supplied
- offline source supplied: yes/no/not supplied
- offline source path/reference, redacted if sensitive
- expected `setuptools` version
- operator notes, redacted if sensitive
- operator name/date or redacted operator reference
- ambiguity assessment
- safety assessment
- whether the response is actionable
- whether package build proof remains blocked
- next branch allowed by the archived response
- explicit statement that no environment preparation happened on the archive branch

Missing required archive fields must block any readiness or build-proof claim.

## Decision Interpretation

### Existing Backend-Ready Environment

Actionable only if the response includes:

- an explicit existing environment identifier
- confirmation that `setuptools>=68` is expected to already be available
- approval to inspect Python, pip, `setuptools` version, and direct backend import
- approval for no-network wheel proof only after backend import succeeds, if wheel proof is requested later

This decision does not authorize dependency installation, network access, package publication, consumer repo changes, or
runtime changes.

### Prepare Controlled Local Environment

Actionable only if the response includes:

- target environment path or identifier
- explicit dependency installation choice
- explicit network access choice
- expected `setuptools` version or approved source policy
- provenance requirement for any provided package source

This decision does not authorize build proof on the archive branch. It only allows a later separately scoped branch to
prepare or verify the environment if all approval fields are complete.

### Operator-Provided Offline Source

Actionable only if the response includes:

- local source path or artifact reference
- expected `setuptools` version
- provenance note
- confirmation that network access is not needed for backend provisioning

The archive must redact sensitive local paths if they reveal private tenant, credential, or infrastructure details.

### Declined / Keep Blocked

If declined, withheld, or not supplied:

- package build proof remains blocked
- repo-checkout import/example proof remains the current package-adjacent evidence
- no environment preparation, install, wheel build, or package-readiness claim may occur

## Ambiguity And Fail-Closed Rules

The future archive must be marked blocked if:

- the response is missing
- the response does not choose exactly one decision
- network permission is unclear for any path requiring network
- dependency-install permission is unclear for any path requiring install
- target environment is missing for an environment-specific approval
- offline source reference is missing for an offline-source approval
- expected `setuptools` version is missing when backend provisioning is approved
- the response authorizes package publication
- the response authorizes consumer repo changes
- the response authorizes runtime behavior changes
- the response contains credentials, secrets, tokens, or unsafe private details that cannot be redacted safely
- the response attempts to approve Sparkbot/Arc product readiness
- the response conflicts with LIMA Guardian or non-execution boundaries

Blocked archive status must preserve the current package build blocker.

## Redaction Rules

The archive must not include:

- passwords
- tokens
- API keys
- registry credentials
- private package registry auth headers
- private URLs containing credentials
- raw environment variables containing secrets
- tenant/customer identifiers
- sensitive local paths that reveal private infrastructure
- private network addresses unless explicitly safe and necessary
- raw command output containing secrets

Allowed redacted forms:

- `[redacted-secret]`
- `[redacted-token]`
- `[redacted-private-path]`
- `[redacted-private-url]`
- `[redacted-operator]`

## Future Allowed Archive Branch

A later archive branch may:

- add `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_AUDIT.md`
- optionally add `docs/audits/LIMA_BUILD_BACKEND_OPERATOR_RESPONSE_ARCHIVE_SOURCE.md`
- summarize the operator decision
- mark the response actionable, blocked, or declined
- recommend the next branch based on the archived response
- run standard validation

That branch must not:

- install `setuptools`
- run `pip install`
- run `pip wheel`
- run `python -m build`
- create virtual environments
- download dependencies
- access PyPI or registries
- build wheels or sdists
- publish packages
- commit wheel, sdist, build, cache, virtualenv, or wheelhouse artifacts
- modify `pyproject.toml`
- modify package metadata
- modify `lima/`
- modify tests or examples
- touch public Sparkbot
- touch Arc Bot repositories
- touch Robo-OS repositories
- wire Sparkbot or Arc Bot
- add provider/model calls
- add storage or persistence
- add Guardian enforcement
- add HumanInput runtime bridge
- add live adapters
- run shell/browser/network/file mutation behavior
- start background workers, subprocesses, threads, queues, daemons, or schedulers
- use credentials or secrets
- control devices, robots, drones, or physical-world systems

## Next Branch Selection

If the archived response approves an existing backend-ready environment, the recommended next branch may be:

`verify-lima-approved-existing-build-backend-environment`

If the archived response approves controlled local environment preparation, the recommended next branch may be:

`design-lima-controlled-build-backend-environment-preparation`

If the archived response approves an operator-provided offline source, the recommended next branch may be:

`design-lima-offline-build-backend-source-verification`

If the response is declined, missing, ambiguous, or unsafe, the recommended next branch should remain:

`audit-lima-build-backend-operator-response-blocked`

## Sparkbot And Arc Bot Impact

This design does not make LIMA ready for Sparkbot or Arc Bot.

It only defines how to archive the operator response needed to decide the package build-backend path.

Sparkbot/Arc readiness still requires:

- archived operator response
- approved package build backend environment
- local wheel build proof
- isolated install/import proof
- Sparkbot-owned proof packet
- Arc Bot-owned proof packet
- operator delivery confirmation
- public API compatibility freeze
- product-ready release decision

## Recommended Next Branch

`audit-lima-build-backend-operator-response-archive`
