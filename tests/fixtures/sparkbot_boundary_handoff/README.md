# Sparkbot Boundary Handoff Fixtures

These fixtures describe a LIMA-local handoff package for a future Sparkbot-owned dry-run proof branch.

They are synthetic and inert. They do not touch the public Sparkbot repository, import Sparkbot modules, wire Sparkbot routes, call models, execute tools, access connectors, persist data, open networks, use credentials, control devices, or touch Robo-OS or physical-world systems.

The intended future Sparkbot proof remains:

```text
Sparkbot-owned normalization -> KernelRequest -> LimaKernel.evaluate(...) -> dry-run ExecutionResult
```

No production Sparkbot integration is claimed by these fixtures.
