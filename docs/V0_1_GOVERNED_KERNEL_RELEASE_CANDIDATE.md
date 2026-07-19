# LIMA v0.1 Governed-Kernel Release Candidate

## Status

`lima-runtime` version `0.1.0rc1` is an installable, candidate-only package
for Sparkbot and Arc consumer validation. It is not a production release, an
approval executor, a provider runtime, or a robotics runtime.

The supported public entrypoint is exactly
`lima.runtime.run_governed_request`:

```python
from lima.runtime import run_governed_request
```

The entrypoint returns a Guardian-gated `GovernedDecision`. An allowed preview
is still non-executable: `executable`, `execution_allowed`, and
`side_effects_allowed` remain `False`.

## Consolidated Recovery Lineage

This release candidate is based on main commit
`deea1c4f5b6d3455a7e97e4b621e22b8d22a6244`, which already contains this
recovery history in order:

| Capability | Commit |
|---|---|
| Governed dry-run kernel | `702b0554203f83002815362c7fce783e18ddbf03` |
| Guardian Core policy seam | `17fab7cbf8befa846444437fd1108847c42ff9c0` |
| Consumer checkpoint manifest | `cbddc3c763565c6958d46711abc6195a792a2868` |
| Arc consumer runtime baseline | `04eb204a710c4e8f5f15759fbbe31e831a9a6029` |

No recovery commit is replayed or duplicated by the release-candidate branch.
The optional `guardian_core.policy` import remains the Guardian integration
seam. When Guardian Core is absent or fails, LIMA falls back to its
non-executing policy adapter and fails closed for unknown or actionable work.

## Installation And Pinning

CI builds the wheel
`lima_runtime-0.1.0rc1-py3-none-any.whl` and publishes it as the
`lima-runtime-v0.1.0rc1-wheel` workflow artifact. The wheel has no runtime
dependencies.
Only `lima`, `lima.contracts`, and `lima.governed_kernel` are packaged.
Historical Guardian execution, harness, provider, I/O, tool-pack, persistence,
service, shell, and spine packages are absent from the wheel. The clean-install
proof verifies those exclusions from both the wheel archive and the installed
environment.
CI sets `SOURCE_DATE_EPOCH=1784353973`, builds the wheel twice, and requires
the two SHA-256 values to match before upload. This fixed epoch is the timestamp
of the recorded main base commit. It controls archive timestamps only; package
identity remains the reviewed source and exact commit pin.


For source-based consumer testing, pin the exact reviewed PR head:

```text
lima-runtime @ git+https://github.com/armpit-symphony/LIMA-AI-OS.git@<exact-reviewed-pr-head>
```

Replace the placeholder only with the immutable commit reported on the
release-candidate PR after review. Do not pin the moving branch name.

After the PR merges, consumers may instead pin the exact merge commit. Do not
tag `v0.1.0rc1` or publish the package to a registry without a separate
operator approval and exact-head verification.

## Consumer Use

Sparkbot decision preview and Arc governed preflight may submit a mapping to
`run_governed_request`. They may display or audit the returned decision. They
must not treat `allowed=True` as execution authority; for the supported
preview actions it means only `allowed_dry_run`.

The installed package exposes release evidence:

```python
import lima

assert lima.__version__ == "0.1.0rc1"
manifest = lima.get_release_candidate_manifest()
assert manifest["execution_allowed"] is False
assert manifest["production_ready"] is False
```

## Explicitly Blocked

- approval execution and approval-token issuance
- model or provider calls
- tool or connector calls
- network actions
- outbound messages
- file mutation
- credentials and privileged reveal
- background or hidden actions
- robotics, IoT, drones, and physical-world actions
- production-readiness claims

Historical experimental harness contracts remain in the repository for
regression compatibility. They are not packaged and are not part of the
supported v0.1 governed-kernel release-candidate surface.

## Release Gate

Before an operator considers a tag or registry publication:

1. verify the exact PR head;
2. review the recovery lineage and package diff;
3. require full tests and the clean-wheel consumer proof to pass;
4. verify the built wheel SHA-256 from CI;
5. verify no dependency, provider, tool, connector, or robotics surface was
   added;
6. obtain separate explicit operator approval.

Do not tag or publish from this work order.
