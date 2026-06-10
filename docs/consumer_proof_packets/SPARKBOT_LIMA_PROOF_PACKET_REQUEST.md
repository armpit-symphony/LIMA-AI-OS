# Sparkbot LIMA Proof Packet Request

## Status

REQUEST_ONLY.

Sparkbot remains readiness/proof-only. No Sparkbot repo path may integrate LIMA runtime paths until LIMA package build
proof, isolated install proof, public API freeze, and Sparkbot-owned proof packet audit are complete.

## Requested Packet

The Sparkbot team should provide a LIMA proof packet with:

- proposed import/call shape
- expected `lima-runtime` package version or commit/ref
- normalized metadata examples
- capability profile expectations
- Guardian/approval boundary expectations
- dry-run behavior expectations
- non-execution confirmation
- confirmation that no live product path calls LIMA yet
- confirmation that no tool/model/connector/browser/file/network/scheduled task/external send/device/robot/drone/IoT/
  physical-world behavior bypasses Guardian
- validation commands
- proof packet owner/date
- independent audit requirement

## Required Non-Execution Confirmation

The packet must explicitly confirm:

- no Sparkbot wiring is active
- no provider/model call path is routed through LIMA
- no tool execution is routed through LIMA
- no browser/file/network action is routed through LIMA
- no external send is routed through LIMA
- no scheduler/background task is routed through LIMA
- no device, robot, drone, IoT, or physical-world behavior is routed through LIMA

## Expected LIMA Boundary

Sparkbot may only propose dry-run, already-normalized metadata against candidate public imports documented in
`docs/readiness/LIMA_PUBLIC_API_FREEZE_CANDIDATE.md`.

No Sparkbot implementation work is requested by this LIMA-side document.

## Delivery

- owner:
- date:
- consumer repo/ref:
- LIMA package version/ref:
- independent audit branch:
