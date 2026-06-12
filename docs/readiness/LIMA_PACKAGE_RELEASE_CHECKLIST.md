# LIMA Package Release Checklist

## Branch

`audit-lima-release-readiness-gap-and-package-checklist`

## Checklist Status

Checklist status: `DRAFT_BLOCKING_CHECKLIST`.

Release status: `NOT_READY`.

This checklist defines the package/release gates that must be satisfied before any LIMA Runtime release candidate,
package publication, compatibility freeze, or product-readiness claim.

## Package Identity Gate

Required:

- package name remains `lima-runtime`
- current package version is recorded
- Python requirement is recorded
- build backend is recorded
- package include pattern is recorded
- license metadata warning is resolved or explicitly dispositioned
- package metadata changes receive static coverage and audit

Current evidence:

- package name: `lima-runtime`
- current version: `0.0.1`
- Python requirement: `>=3.11`
- build backend: `setuptools.build_meta`
- package include pattern: `include = ["lima*"]`
- license metadata warning: `unresolved_before_release_readiness`

## Build And Artifact Gate

Required:

- source copy for build proof is outside the repository
- wheel and sdist are built outside the repository
- isolated install proof uses `--no-index`
- generated artifacts are not committed
- artifact hashes, publish policy, and rollback policy are defined before publication
- no package publication occurs from a proof branch

Current evidence:

- controlled package proof is `COMPLETE_WITH_AUDIT`
- package publish readiness is `NOT_READY`
- build artifacts must not be committed

## Public API Gate

Required:

- final public API freeze decision exists
- candidate exports are independently audited against `lima.kernel.__all__`
- top-level runtime exports remain unapproved unless the freeze explicitly changes that
- consumer compatibility and deprecation policy is documented
- private/internal consumer surfaces remain forbidden

Current evidence:

- public API status is `CANDIDATE_ONLY`
- top-level runtime exports are not approved
- consumer proof branches must use `from lima.kernel import <exported-name>`

## Consumer Proof Gate

Required:

- operator delivery confirmation is recorded
- consumer proof packets are supplied by consumer teams
- proof packets are redaction-reviewed before archive or audit
- each supplied proof packet receives a LIMA-side proof-result audit
- compatibility freeze is blocked until required proof audits pass

Current evidence:

- operator delivery confirmation: `RECORDED_MANUAL_DELIVERY_ONLY`
- LIMA state: `WAITING_ON_CONSUMER_PROOF_PACKET_RESPONSES`
- Sparkbot proof packet: `not_supplied_yet`
- Arc Bot proof packet: `not_supplied_yet`
- LIMA Robo OS proof packet: `not_supplied_yet`
- LIMA Office proof packet: `not_supplied_yet`
- Future shell proof packet: `not_supplied_yet`

## Runtime And Security Gate

Required:

- release branch confirms no runtime behavior expansion
- no consumer wiring is added
- no provider/model routing is added
- no Guardian authority expansion is added
- no approval enforcement is added
- no HumanInput bridge activation is added
- no storage/persistence runtime is added
- no connectors, browser/file/network behavior, external sends, live discovery, scanning, pairing, credential use,
  device control, robotics, drones, IoT, or physical-world behavior are added

Current evidence:

- runtime integration: `NOT_READY`
- product readiness: `NOT_READY`
- physical-world readiness: `BLOCKED`

## Documentation Gate

Required:

- release notes distinguish proof-only, release-candidate, and product-ready states
- install/verify instructions include `import lima`, `import lima.kernel`, and approved proof-public imports only
- uninstall/rollback instructions are documented
- SparkPit Labs site/product copy is reviewed so it does not claim production readiness prematurely
- consumer onboarding docs point to proof packet and public API freeze status

Current evidence:

- proof-stage docs exist
- product-ready release docs do not exist
- SparkPit Labs product-readiness claims remain blocked

## Validation Gate

Required before any release-candidate branch is accepted:

- focused package/release static tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git status --short --branch`
- independent release-readiness audit

## Release Decision Gate

Allowed release decisions:

- `remain_proof_only`
- `prepare_release_candidate_after_gates`
- `pause_waiting_on_consumer_proof`
- `resolve_package_metadata_warning`

Forbidden release decisions:

- `publish_package_now`
- `claim_product_ready`
- `finalize_public_api_freeze_without_packet_audits`
- `wire_consumers`
- `enable_runtime_integration`
- `enable_physical_world_behavior`

## Current Checklist Verdict

`NOT_READY_FOR_RELEASE`.

The package has proof-stage build and import evidence, but LIMA is still waiting on consumer proof packet responses,
final public API freeze, package metadata warning disposition, artifact/publish policy, release docs, and independent
release-readiness audit.
