# LIMA Robo OS Proof Packet Request

## Status

REQUEST_ONLY.

LIMA Robo OS remains readiness/proof-only. No Robo OS repo path may integrate LIMA runtime paths until LIMA package build
proof, isolated install proof, public API freeze, Robo OS-owned proof packet audit, and separate physical-world operator
approval are complete.

## Requested Packet

The LIMA Robo OS team should provide a LIMA proof packet with:

- proposed import/call shape
- expected `lima-runtime` package version or commit/ref
- normalized metadata examples for simulated or blocked robot/device intent
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

## Physical-World Safety Fields

The packet must include:

- emergency stop boundary
- HumanInput approval boundary
- device/driver boundary
- live discovery prohibition
- actuation prohibition
- physical-world safety gate requirement

## Required Non-Execution Confirmation

The packet must explicitly confirm:

- no Robo OS wiring is active
- no live discovery is active
- no scanning is active
- no connection attempt is active
- no pairing is active
- no credential use is active
- no device/driver control is active
- no robot/drone actuation is active
- no physical-world behavior is routed through LIMA
- no emergency stop, approval, or Guardian boundary is bypassed

## Expected LIMA Boundary

LIMA Robo OS may only propose dry-run, already-normalized metadata against candidate public imports documented in
`docs/readiness/LIMA_PUBLIC_API_FREEZE_CANDIDATE.md`.

No Robo OS implementation work is requested by this LIMA-side document.

## Delivery

- owner:
- date:
- consumer repo/ref:
- LIMA package version/ref:
- independent audit branch:
