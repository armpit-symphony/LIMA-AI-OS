# Governed stack map

Four repositories make up this stack. They are separate repos with separate
CI, and each one pins the others by exact commit. This document is the map:
who depends on whom, which commit each consumer holds, and why they differ.

## The repositories

| Repo | Role | Executes? |
|---|---|---|
| [LIMA-AI-OS](https://github.com/armpit-symphony/LIMA-AI-OS) | The governed kernel. Decides. | No |
| [LIMA-Guardian-Suite](https://github.com/armpit-symphony/LIMA-Guardian-Suite) | Policy authority behind the kernel. | No |
| [Lima-Office](https://github.com/armpit-symphony/Lima-Office) | Supervisor / control plane. Coordinates workers. | No |
| [Arc-Bot-shell](https://github.com/armpit-symphony/Arc-Bot-shell) | Worker shell and operator client. | Only under a grant |
| [Sparkbot](#sparkbot) | Desktop product shell. Separate lifecycle. | Out of scope here |

The load-bearing split: **LIMA decides, shells execute.** A `GovernedDecision`
structurally cannot authorize execution — its `__post_init__` rejects any
execution flag and `to_dict` pins all three to `False`. Nothing in the stack
can make a decision into permission.

## Request flow

```
Arc operator CLI
  -> Lima-Office Supervisor          (authenticated, loopback only)
     -> Guardian Suite               (policy)
     -> LIMA run_governed_request    (governed decision, never executable)
     -> LIMA issue_execution_grant   (optional, separate contract)
  -> back to Arc
     -> Arc honours the grant        (only if Arc is independently opted in)
```

Both channels are HMAC-SHA256 authenticated over canonical JSON with replay
stores. The Supervisor refuses to bind a non-loopback address; Arc refuses to
call one.

## Two gates, held by different parties

Execution needs **both**, and each defaults off:

1. **Office** must be started with `--execution-opt-in` before it will issue a
   grant at all.
2. **Arc** must be invoked with `--execute-granted-capability` before it will
   honour one.

Neither party can enable the other. A grant is a *necessary* condition for
execution, never a sufficient one — `requires_operator_opt_in` is pinned
`True` in grant v0.1, so an enforcer that has not been opted in must still
deny. See [GOVERNED_EXECUTION_GRANT.md](GOVERNED_EXECUTION_GRANT.md).

## Consumer pin map

Each consumer pins LIMA by exact commit. **They deliberately hold different
commits.** Checking one against another and "fixing" the difference is a
mistake; check each against its own repo's `stack.lock.json`.

| Consumer | LIMA commit | Policy | Why |
|---|---|---|---|
| Lima-Office | `0718af2` | tracking | Needs `issue_execution_grant`; tracks LIMA `main`. |
| Arc-Bot-shell | `40d6f13` | frozen | LIMA v0.1 RC1 public API freeze, attested by a test. Arc consumes grants as JSON off the wire and imports nothing from `lima`, so it does not need newer LIMA. |
| Sparkbot | `4e7c648` | — | Older preview-consumer pin. Predates the grant contract. See below. |

Guardian Suite is pinned at `69e8432` by both Office and Arc.

Office and Arc each hold a `stack.lock.json` declaring every place a pin is
written down, with a checker that fails the build when copies disagree and a
`bump-pin.py` that moves them together. Arc's LIMA pin alone appears in nine
places. See each repo's `docs/DEPENDENCY_PIN_LOCK.md`.

Sparkbot has no such lock yet.

## Sparkbot

**There are two Sparkbot repositories and they are not forks of each other.**
Picking the wrong one is the most common way to waste time here.

| | [`armpit-symphony/Sparkbot`](https://github.com/armpit-symphony/Sparkbot) | [`sparkpit-labs/Sparkbot`](https://github.com/sparkpit-labs/Sparkbot) |
|---|---|---|
| Role | Active development | Public V1.0.0 release |
| Size | ~39.8 MB | ~0.35 MB |
| Latest work | 2026-07-23, LIMA RC pin | 2026-06-21, "Merge public V1.0.0 release" |

**Work in `armpit-symphony/Sparkbot`.** It is the full repository and the one
carrying current LIMA integration. `sparkpit-labs/Sparkbot` is the curated
public release surface; treat it as a publication target, not a working tree.

The local checkout is `C:\Users\limap\Sparkbot`, pointed at
`armpit-symphony` over SSH (`git@github-armpit:...`). Note that
`C:\Users\limap\sparkbot` is the *same directory* — Windows paths are
case-insensitive — not a second clone.

### What matters about Sparkbot for this stack

Sparkbot is a **third LIMA consumer** and the one furthest behind. It pins
LIMA at `4e7c648` in `backend/pyproject.toml`, which predates both Arc's
frozen RC1 pin and the execution-grant contract entirely. So:

- Sparkbot cannot receive or honour execution grants. It is a preview/preflight
  consumer only.
- `4e7c648` is the same commit Arc's operator trust baseline was accidentally
  stuck on. Arc has been corrected; Sparkbot has not been touched.
- Sparkbot's pin is a single site today, so it has no drift problem yet — but
  it also has no lock to prevent one.

Sparkbot is architecturally unrelated to the Office/Arc control plane: it is a
Tauri desktop app with a FastAPI backend sidecar, and it does not participate
in the Supervisor/worker protocol. Changes here do not affect it unless its
LIMA pin is moved.

### Before moving Sparkbot's LIMA pin

Moving it from `4e7c648` to a current commit crosses the LIMA v0.1 RC1 public
API freeze. Check Sparkbot's LIMA call sites against the frozen surface first,
and treat it as its own reviewed change — not a routine bump.

## Historical commits are not pins

Across these repos, roughly a hundred commit hashes appear in audit records,
proof packets, baseline documents, and test fixtures. They record what was
true when something was attested. They are **not** pins, must never be
rewritten to match a current pin, and are deliberately excluded from every
`stack.lock.json`.
