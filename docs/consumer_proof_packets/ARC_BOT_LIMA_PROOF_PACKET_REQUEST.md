# Arc Bot LIMA Proof Packet Request

## Status

REQUEST_ONLY.

Arc Bot remains readiness/proof-only. No Arc Bot repo path may integrate LIMA runtime paths until LIMA package build
proof, isolated install proof, public API freeze, and Arc Bot-owned proof packet audit are complete.

## Requested Packet

The Arc Bot team should provide a LIMA proof packet with:

- proposed import/call shape
- expected `lima-runtime` package version or commit/ref
- normalized metadata examples for office-worker task previews
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

- no Arc Bot wiring is active
- no office-worker execution path calls LIMA
- no connector read/write bypasses Guardian
- no file/browser/network action bypasses Guardian
- no outbound email, text, chat, ticket, form, or customer-facing send bypasses Guardian
- no scheduler/background task is routed through LIMA
- no device, robot, drone, IoT, or physical-world behavior is routed through LIMA

## Expected LIMA Boundary

Arc Bot may only propose dry-run, already-normalized metadata against candidate public imports documented in
`docs/readiness/LIMA_PUBLIC_API_FREEZE_CANDIDATE.md`.

No Arc Bot implementation work is requested by this LIMA-side document.

## Delivery

- owner:
- date:
- consumer repo/ref:
- LIMA package version/ref:
- independent audit branch:
