# Sparkbot Public V1-G56 Handoff Artifact

This directory contains the temporary readable handoff artifacts for Sparkbot public repository maintainers.

Primary artifact:

- `sparkbot-public-v1-g56-runtime-authority-chain-audit.bundle`

Expected branch:

- `v1-g56-runtime-authority-chain-audit`

Expected commit:

- `ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2`

Bundle SHA256:

- `3B366845D4EE78EE43B9F787ECAB2CF7CF4C7848154A49ED4805ED9292A9B69F`

Suggested verification:

```bash
sha256sum sparkbot-public-v1-g56-runtime-authority-chain-audit.bundle
git bundle verify sparkbot-public-v1-g56-runtime-authority-chain-audit.bundle
git bundle list-heads sparkbot-public-v1-g56-runtime-authority-chain-audit.bundle
```

Expected bundle head:

```text
ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2 refs/heads/v1-g56-runtime-authority-chain-audit
```

Suggested import:

```bash
git fetch sparkbot-public-v1-g56-runtime-authority-chain-audit.bundle refs/heads/v1-g56-runtime-authority-chain-audit:refs/heads/v1-g56-runtime-authority-chain-audit
git checkout v1-g56-runtime-authority-chain-audit
git rev-parse HEAD
```

Expected `HEAD`:

```text
ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2
```

Local validation already run before handoff:

```bash
python -m pytest -q tests/test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider
git diff --check
git status --short --branch
```

Results:

- focused G56 smoke test: `8 passed`
- `git diff --check`: clean
- status: clean on `v1-g56-runtime-authority-chain-audit`

Use the bundle to preserve the exact commit SHA. Patch files are not included in this branch because the bundle is the authoritative transfer artifact.
