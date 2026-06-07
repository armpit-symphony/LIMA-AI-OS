# Arc Boundary Handoff Fixtures

These fixtures describe a LIMA-local handoff package for a future Arc-owned dry-run proof branch.

They are synthetic and inert. They do not touch Arc Bot repositories, the public Sparkbot repository, import Arc modules, wire Arc routes, schedule work, call models, execute tools, access connectors, persist data, open networks, use credentials, control devices, or touch Robo-OS or physical-world systems.

The intended future Arc proof remains:

```text
Arc-owned normalization -> KernelRequest -> LimaKernel.evaluate(...) -> dry-run ExecutionResult
```

No production Arc integration is claimed by these fixtures.
