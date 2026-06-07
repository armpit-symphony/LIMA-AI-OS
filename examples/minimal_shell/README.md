# LIMA Minimal Example Shell

This local example proves that a shell-shaped caller can import LIMA, instantiate
`LimaKernel`, pass already-normalized metadata, and receive dry-run results.

This is not Sparkbot integration, Arc Bot integration, public product wiring, or
live runtime behavior.

## What It Demonstrates

- `from lima.kernel import LimaKernel` works.
- A local shell can build a normalized `KernelRequest`.
- `LimaKernel.evaluate(...)` returns a dry-run `ExecutionResult`.
- An explicit `SimulatedDiscoveryAdapter` can return synthetic surfaces.
- Non-execution invariants remain false.

## What It Does Not Do

- parse raw natural language
- call models or providers
- execute tools
- mutate files
- open browsers
- call networks or sockets
- scan, connect, pair, or use credentials
- persist events
- start workers, schedulers, threads, or subprocesses
- import Sparkbot, Arc Bot, or Robo-OS
- control devices, robots, drones, or physical-world systems

## Local Use

Run from the repository root:

```bash
python -m examples.minimal_shell.example_shell
```

The output is a redacted dry-run summary only. Any future Sparkbot or Arc Bot
consumer branch should treat this as a dependency-shape proof, not as runtime
integration approval.
