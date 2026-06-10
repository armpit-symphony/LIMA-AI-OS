# LIMA Office Proof Packet Request

## Status

REQUEST_ONLY.

LIMA Office remains readiness/proof-only. No LIMA Office repo path may integrate LIMA runtime paths until LIMA package
build proof, isolated install proof, public API freeze, and LIMA Office-owned proof packet audit are complete.

## Requested Packet

The LIMA Office team should provide a LIMA proof packet with:

- proposed import/call shape
- expected `lima-runtime` package version or commit/ref
- normalized metadata examples for office/customer work previews
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

## Office And Customer Data Fields

The packet must include:

- customer/tenant data boundary
- connector boundary
- approval boundary
- external-send boundary
- file/browser/network boundary

## Required Non-Execution Confirmation

The packet must explicitly confirm:

- no LIMA Office wiring is active
- no customer/tenant data path calls LIMA live
- no connector read/write bypasses Guardian
- no external send bypasses Guardian
- no file/browser/network action bypasses Guardian
- no scheduled task or background worker is routed through LIMA
- no device, robot, drone, IoT, or physical-world behavior is routed through LIMA

## Expected LIMA Boundary

LIMA Office may only propose dry-run, already-normalized metadata against candidate public imports documented in
`docs/readiness/LIMA_PUBLIC_API_FREEZE_CANDIDATE.md`.

No LIMA Office implementation work is requested by this LIMA-side document.

## Delivery

- owner:
- date:
- consumer repo/ref:
- LIMA package version/ref:
- independent audit branch:
