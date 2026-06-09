# LIMA Build Backend Operator Approval Request

## Branch

`design-lima-build-backend-operator-approval-request`

## Purpose

This document defines the operator-facing approval request needed before any branch prepares a Python environment for
LIMA package build proof.

The current package build blocker is explicit:

- `pyproject.toml` declares build backend `setuptools.build_meta`
- `pyproject.toml` declares build requirement `setuptools>=68`
- the active Python 3.12 environment has pip
- `setuptools` is not installed
- direct import of `setuptools.build_meta` fails
- local no-network wheel build proof remains blocked

This branch is design-only. It does not request implicit approval, install dependencies, create environments, run build
tooling, build wheels, publish packages, modify package metadata, touch runtime files, touch consumer repositories,
wire Sparkbot or Arc Bot, or claim product readiness.

## Request Summary

The future operator request should ask for one of these explicit decisions:

- approve use of an existing environment that already has `setuptools>=68`
- approve preparing a controlled local environment with `setuptools>=68`
- approve using an operator-provided offline wheelhouse or pre-provisioned backend source
- decline environment preparation and keep package build proof blocked

No approval option should authorize package publication, runtime changes, consumer repo changes, or product readiness
claims.

## What The Operator Is Being Asked To Approve

The operator may approve a controlled environment path that makes `setuptools>=68` available only for package build
proof.

The approval should be specific about:

- target environment path or identifier
- whether dependency installation is allowed
- whether network access is allowed
- whether an offline wheelhouse or local package source is supplied
- whether a temporary isolated environment may be created
- whether no-network wheel proof may run after backend import succeeds

If the operator does not explicitly approve one of these, the next branch must remain blocked from preparing the
environment.

## Approval Options

### Option A: Use Existing Backend-Ready Environment

Operator approves:

- use of an already-prepared Python environment
- verification of Python, pip, and `setuptools` version
- direct import check for `setuptools.build_meta`
- no-network wheel proof after backend availability is proven

Operator does not approve:

- dependency installation
- network access
- package publication
- package metadata changes
- consumer repo changes

### Option B: Prepare Controlled Local Environment

Operator approves:

- creating or using a named local environment
- installing or providing `setuptools>=68`
- recording whether network access was used
- recording package source/provenance

Operator must also choose:

- network allowed: yes/no
- offline source supplied: yes/no
- environment path or identifier

This option requires explicit operator approval before any installation command runs.

### Option C: Use Operator-Provided Offline Source

Operator approves:

- use of a specific offline wheelhouse or local package source
- verifying package identity and version
- no-network backend provisioning
- recording source provenance

Operator must provide:

- local source path or artifact reference
- expected `setuptools` version
- provenance note

### Option D: Decline Environment Preparation

Operator declines or withholds approval.

Result:

- package build proof remains blocked
- repo-checkout import/example proof remains the current package-adjacent evidence
- no install, environment creation, wheel build, or package-readiness claim occurs

## Approval Record Template

Archive-ready operator response template:

```text
LIMA build backend environment approval response

Decision:
- [ ] Approved: existing backend-ready environment
- [ ] Approved: prepare controlled local environment
- [ ] Approved: use operator-provided offline source
- [ ] Declined / keep blocked

Target environment:

Network access allowed:
- [ ] yes
- [ ] no

Dependency installation allowed:
- [ ] yes
- [ ] no

Offline source supplied:
- [ ] yes
- [ ] no

Offline source path/reference, if any:

Expected setuptools version:

Operator notes:

Operator name/date:
```

The next branch must archive the operator response before performing any approved environment preparation.

## Required Evidence After Approval

A later verification branch must record:

- operator approval response
- target environment
- Python version
- pip version
- `setuptools` version
- `setuptools.build_meta` import result
- network-use status
- dependency-install status
- package source/provenance
- temporary-artifact status
- confirmation that no artifacts were committed
- confirmation that `pyproject.toml` was not changed
- confirmation that `lima/` was not changed
- confirmation that no consumer repositories were touched
- validation result

Missing evidence blocks package build readiness claims.

## Future Allowed Verification Flow

Only after explicit approval:

1. Confirm clean repo and approved branch scope.
2. Archive approval response.
3. Inspect Python and pip version.
4. Inspect or provide `setuptools>=68`.
5. Import `setuptools.build_meta`.
6. If backend import fails, stop and record blocker.
7. If backend import succeeds, run separately scoped no-network build proof only if that branch allows it.
8. Keep artifacts outside the repo.
9. Run validation.
10. Record proof without claiming Sparkbot, Arc Bot, or product readiness.

## Forbidden In This Design Branch

This branch must not:

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

## Sparkbot And Arc Bot Impact

This approval request does not make LIMA ready for Sparkbot or Arc Bot.

It only prepares a controlled decision point for resolving the package build-backend blocker. Sparkbot/Arc readiness
still requires:

- approved package build backend environment
- local wheel build proof
- isolated install/import proof
- Sparkbot-owned proof packet
- Arc Bot-owned proof packet
- operator delivery confirmation
- public API compatibility freeze
- product-ready release decision

## Recommended Next Branch

`audit-lima-build-backend-operator-approval-request`

