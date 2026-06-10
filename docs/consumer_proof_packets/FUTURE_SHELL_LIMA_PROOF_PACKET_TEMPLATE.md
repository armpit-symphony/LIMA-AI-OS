# Future Shell LIMA Proof Packet Template

## Status

REQUEST_ONLY.

Future shells remain readiness/proof-only. No future bot, shell, workstation, service, device, robot, drone, or office
automation repo path may integrate LIMA runtime paths until LIMA package build proof, isolated install proof, public API
freeze, and that shell's proof packet audit are complete.

## Requested Packet

The future shell team should provide a LIMA proof packet with:

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

- no shell wiring is active
- no provider/model call path is routed through LIMA
- no connector/tool execution bypasses Guardian
- no browser/file/network action bypasses Guardian
- no external send bypasses Guardian
- no scheduler/background task is routed through LIMA
- no live discovery, scanning, connection, pairing, credential use, device control, robot/drone control, IoT behavior, or
  physical-world behavior is routed through LIMA

## Expected LIMA Boundary

Future shells may only propose dry-run, already-normalized metadata against candidate public imports documented in
`docs/readiness/LIMA_PUBLIC_API_FREEZE_CANDIDATE.md`.

No future shell implementation work is requested by this LIMA-side document.

## Delivery

- owner:
- date:
- consumer repo/ref:
- LIMA package version/ref:
- independent audit branch:
