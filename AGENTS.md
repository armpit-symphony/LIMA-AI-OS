# Codex Project Guidance

This repository is the source of truth for LIMA-AI-OS / LIMA Runtime project direction.

LIMA-AI-OS belongs to SparkPit Labs. It is the trust-governed natural-language operating runtime/kernel for AI-controlled software, workflows, automation, devices, robots, drones, and humanoid systems. Sparkbot is the open-source hobby/R&D shell and publicity/reference model, not the kernel. LIMA AI Office, ARC Bot, custom office-worker bots, and physical-world systems are future product shells or consumers on top of the runtime.

Before doing work, read these files in order:

1. `docs/CURRENT_PROJECT_STATE.md`
2. `README.md`
3. `docs/ROADMAP.md`
4. `docs/DECISIONS.md`
5. `docs/EXTRACTION_PLAN.md`

Follow the LIMA Runtime Architect discipline:

- Contracts first.
- Guardian always.
- Sparkbot is the spec.
- Extract, do not rewrite.
- Robo-OS is a gated driver.
- LIMA Runtime is the kernel.

Preserve the project sequence:

- Contracts first.
- Fixtures second.
- Tests third.
- Safety gates before runtime.

Do not add runtime behavior unless the task explicitly approves it.

Do not wire Sparkbot unless the task explicitly approves it. Do not import Sparkbot, wire live Sparkbot routes, import FastAPI/WebSocket routes, import `stream_chat_with_tools`, or import `execute_tool` unless a future approved phase says to do so.

Do not implement ARC Bot, custom business/private-sector bots, robot control, real `IntentCompiler`, real `GuardianDecision`, adaptive trust enforcement, approval, execution, audit persistence, physical-world action, live auth/session lookup, trusted device enforcement, or autonomy enforcement unless the task explicitly approves it.

Use `python3` when available. If `python3` or `python3.exe` is unavailable but `python` resolves to Python 3.x, use `python` and report the exact version.

Always run validation appropriate to the change. For docs/config guidance changes, at minimum run:

- `python3 --version || python --version`
- `python3 -m compileall lima || python -m compileall lima`
- `python3 -m pytest -q || python -m pytest -q`
- `git diff --check`

Never merge or tag without explicit operator approval.

Final reports must include branch, commit, files changed, validation results, boundary results, blockers, and the recommended next smallest safe step.
