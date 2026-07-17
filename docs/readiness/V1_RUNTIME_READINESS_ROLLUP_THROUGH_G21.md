# V1 Runtime Readiness Rollup Through G21

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g21`
API status: `CANDIDATE_ONLY`

## Required Verdicts

- V1 runtime authority chain: `CANDIDATE_ONLY`
- Guarded file mutation policy: `CANDIDATE_ONLY`
- File mutation preview/diff: `CANDIDATE_ONLY`
- Consumer proof packet audit intake: `CANDIDATE_ONLY`
- Live approval evidence/capture metadata: `CANDIDATE_ONLY`
- Provider/model routing authority metadata: `CANDIDATE_ONLY`
- Consumer integration compatibility/freeze metadata: `CANDIDATE_ONLY`
- Live provider/model calls: `NOT_APPROVED`
- Secret lookup and credential access: `NOT_APPROVED`
- Model dispatch and fallback execution: `NOT_APPROVED`
- Raw approval factor verification: `NOT_APPROVED`
- Approval-token issuance: `NOT_APPROVED`
- Actual file edit/delete/mutation execution: `NOT_APPROVED`
- Consumer integration: `BLOCKED`
- Consumer repository edits: `NOT_APPROVED`
- Live consumer imports/calls: `NOT_APPROVED`
- Connector/browser/network authority: `NOT_APPROVED`
- Physical-world readiness: `BLOCKED`
- Final public API freeze: `NOT_APPROVED`
- Runtime export cleanup: `NOT_APPROVED`
- Product readiness: `NOT_READY`

## Package Proof Status

The package proof and related proof-packet work remain accepted as static evidence only. V1-G18 adds a LIMA-side proof packet audit-intake validator, but that intake metadata is still proof, not consumer integration or runtime authority.

V1-G19 adds sanitized live approval evidence/capture metadata validation, but that evidence is still proof, not raw approval-factor verification, approval-token issuance, or execution authority.

V1-G20 adds sanitized provider/model routing authority metadata validation, but that metadata is still proof, not live provider dispatch, secret lookup, model execution, fallback execution, or consumer integration.

V1-G21 adds sanitized consumer integration compatibility/freeze metadata validation, but that metadata is still proof, not consumer repo mutation, live consumer imports/calls, shell wiring, final public API freeze, runtime export cleanup, or product readiness.

## V1-G11 Status

V1-G11 implemented typed runtime request and GuardianDecision preflight metadata.

Accepted evidence:

- deterministic local typed request builder
- non-executing GuardianDecision preflight gate
- safe informational/planning/drafting requests remain non-executing
- destructive file-mutation shaped requests require operator approval
- provider/model/tool/browser/network/device/robotics/physical-world shaped claims remain blocked by the current gate

## V1-G12 Status

V1-G12 implemented redacted durable audit/evidence metadata and an explicit local append-only JSONL candidate store.

Accepted evidence:

- reviewed V1-G11 request/decision metadata can produce redacted audit event and lineage records
- records are proof, not authority
- scoped local lookup requires tenant/shell constraints
- raw secrets, prompts, file contents, approval PINs, approval tokens, and customer data fail closed
- destructive file records require approval evidence

## V1-G14 Status

V1-G14 implemented local non-executing destructive edit/delete approval-enforcement metadata.

Accepted evidence:

- exact `Approve-V1-G14` decision was recorded
- sanitized approval evidence is required for destructive file-mutation proof
- missing, mismatched, stale, replayed, denied, revoked, expired, or superseded approval evidence fails closed
- approval metadata remains proof, not broad execution authority
- no file mutation behavior, approval-token issuance, provider/model routing, shell wiring, connector behavior, browser/network/device/robotics/physical-world behavior, or consumer integration was added

## V1-G15 Status

V1-G15 implemented the shell/harness guiderail input contract.

Accepted evidence:

- exact `Approve-V1-G15` decision was recorded
- shells/harnesses can provide structured guiderail input metadata
- guardrail mode, capability profile, approval policy, actor/session/tenant/shell scope, allowed lanes, destructive/file/provider/connector/browser/physical-world policies, emergency stop, rollback, approval evidence, and audit/evidence linkage expectations are explicit
- provider/model, connector, browser/network, and physical-world fields are policy metadata only
- raw sensitive content fails closed
- no shell runtime wiring, provider/model routing, connector behavior, browser/network behavior, file mutation behavior, physical-world behavior, or consumer integration was added

## V1-G16 Status

V1-G16 implemented the guarded file mutation policy contract.

Accepted evidence:

- exact `Approve-V1-G16` decision was recorded
- file edit/delete/file-mutation request classification is explicit
- destructive mutation classification is explicit
- workspace/root boundary, path traversal rejection, and target path normalization expectations are explicit
- shell/harness-provided file authority metadata is required
- operator approval evidence requirements are explicit
- dry-run preview, diff/patch preview, rollback, destructive delete confirmation, and audit/evidence linkage expectations are explicit
- tenant, shell, actor, and session scope are explicit
- raw secrets, prompts, file contents, diff/patch contents, approval PINs, approval tokens, and customer data fail closed
- no user-file read, write, delete, overwrite, patch application, preview/diff runtime behavior, actual mutation execution, provider/model routing, connector behavior, browser/network/device/robotics/physical-world behavior, or consumer integration was added

## V1-G17 Status

V1-G17 implemented the file mutation preview/diff runtime slice.

Accepted evidence:

- exact `Approve-V1-G17` decision was recorded
- dry-run file mutation preview metadata is validated
- redacted diff/patch preview metadata is validated
- V1-G16 guarded file mutation policy linkage is required
- path scope, workspace/root, and path traversal rejection metadata are required
- rollback plan metadata is required
- approval evidence linkage is required
- user/operator confirmation linkage is required
- shell/harness policy linkage is required
- audit/evidence linkage is required
- tenant, shell, actor, and session scope are explicit
- raw secrets, prompts, file contents, diff/patch contents, approval PINs, approval tokens, and customer data fail closed
- no user-file read, write, delete, overwrite, patch application, actual mutation execution, provider/model routing, connector behavior, browser/network/device/robotics/physical-world behavior, or consumer integration was added

## V1-G18 Status

V1-G18 implemented the consumer proof packet audit-intake metadata slice.

Accepted evidence:

- exact `Approve-V1-G18` decision was recorded
- `sparkbot`, `arc_bot`, `lima_robo_os`, `lima_office`, and `future_shell` proof packet families are supported
- consumer repository/ref/commit metadata is required
- proof packet, audit packet, and machine-readable summary paths are required
- validation commands and reported results are required
- proposed import/call shape evidence is accepted only as evidence
- normalized metadata examples are required and redacted
- capability profile expectations are required
- Guardian and approval boundary expectations are required
- dry-run and non-execution confirmation is required
- no-live-consumer-runtime-path and no-bypass confirmations are required
- independent audit requirement is required
- packet statuses normalize to `received`, `missing`, `blocked`, `rejected`, and `accepted_static_evidence`
- raw secrets, prompts, file contents, approval PINs, approval tokens, credentials, and customer data fail closed
- no consumer repo mutation, consumer code import, consumer runtime call, consumer integration, provider/model routing, connector/browser/network/file/device/robotics/physical-world behavior, scheduled task execution, external send, final freeze, or product readiness was added

## V1-G19 Status

V1-G19 implemented the live approval evidence/capture metadata slice.

Accepted evidence:

- exact `Approve-V1-G19` decision was recorded
- approval evidence id and challenge id metadata are required
- request id or Guardian decision id linkage is required
- tenant, shell, actor, session, and approver scope metadata are required
- approval intent and action-scope metadata are required and non-authorizing
- action risk class and action family metadata are required
- outcomes normalize to `approved`, `denied`, `revoked`, `stale`, `expired`, `superseded`, and `blocked`
- freshness, expiration, and replay-prevention metadata are required
- factor evidence is accepted only as redacted summary metadata
- capture source metadata must be policy-trusted and cannot invoke a consumer runtime
- audit/evidence linkage is required
- proof-not-authority, no raw PIN/token/secret/customer-data, no approval-token issuance, and no execution-authority confirmations are required
- `evidence_is_current` is true only for approved, fresh, not-expired, not-replayed evidence
- a deterministic `record_hash` is returned over sanitized metadata
- raw PINs, approval tokens, raw factors, secrets, prompts, file contents, credentials, and customer data fail closed
- no raw PIN verification, raw factor persistence, approval-token issuance, action execution, file mutation execution, consumer integration, provider/model routing, connector/browser/network/device/robotics/physical-world behavior, final freeze, or product readiness was added

## V1-G20 Status

V1-G20 implemented the provider/model routing authority metadata slice.

Accepted evidence:

- exact `Approve-V1-G20` decision was recorded
- route id, route family, and route intent scope metadata are required
- request id or Guardian decision id linkage is required
- tenant, shell, actor, and session scope metadata are required
- provider id, model id, model role, and provider boundary metadata are required
- data sensitivity and prompt context class metadata are required without accepting raw prompts
- requested and allowed tool-pack scope metadata are required
- requested tool packs cannot exceed allowed tool packs
- credential metadata is accepted only as reference metadata or no-key-local metadata
- budget, cost, and latency metadata are required
- fallback chain metadata is required
- fallback candidates must inherit the same gates
- approval evidence linkage is required when risk policy requires approval
- provider configuration reference metadata is required
- audit/evidence linkage is required
- proof-not-authority, no raw prompt/secret/credential/customer-data, no secret lookup, no live provider call, and no execution-authority confirmations are required
- a deterministic `record_hash` is returned over sanitized metadata
- raw prompts, raw customer data, credentials, provider tokens, API keys, secrets, and raw model responses fail closed
- live provider/model call, model dispatch, fallback execution, Token Guardian live routing, secret lookup, credential access, tool execution, consumer, connector/browser/network/device/robotics/physical-world, final freeze, and product readiness claims fail closed
- no live provider/model routing, provider/model calls, model dispatch, fallback execution, provider readiness checks, secret lookup, credential access, tool execution, consumer integration, connector/browser/network/device/robotics/physical-world behavior, final freeze, or product readiness was added

## V1-G21 Status

V1-G21 implemented the consumer integration compatibility/freeze metadata slice.

Accepted evidence:

- exact `Approve-V1-G21` decision was recorded
- compatibility packet id metadata is required
- consumer packet family, consumer name, consumer repository, consumer branch/ref, and consumer commit SHA metadata are required
- `sparkbot`, `arc_bot`, `lima_robo_os`, `lima_office`, and `future_shell` compatibility families are supported
- candidate export surface refs are required
- runtime symbol refs are required
- import surface expectation metadata is required and must remain metadata-only
- fixture compatibility matrix metadata is required
- version compatibility metadata is required
- Guardian boundary compatibility metadata is required
- approval boundary compatibility metadata is required
- provider/model route boundary compatibility metadata is required
- consumer runtime call prohibition metadata is required
- no consumer repo mutation confirmation is required
- no live import/call confirmation is required
- final public API freeze not claimed confirmation is required
- audit/evidence linkage metadata is required
- proof-not-authority, no raw content/secret/credential/customer-data, and no execution-authority confirmations are required
- a deterministic `record_hash` is returned over sanitized metadata
- raw file contents, prompts, customer data, credentials, provider tokens, API keys, and secrets fail closed
- consumer repo mutation, consumer code import, consumer runtime call, final API freeze, runtime export cleanup, provider/model call, secret lookup, credential access, tool execution, connector/browser/network/device/robotics/physical-world, and product-readiness claims fail closed
- no consumer repo mutation, consumer file writes, consumer code imports, consumer runtime calls, consumer integration, shell wiring, final public API freeze, runtime export cleanup, live provider/model calls, secret lookup, credential access, tool execution, file mutation execution, connector/browser/network/device/robotics/physical-world behavior, scheduled task execution, external sends, external database writes, or product readiness was added

## Capability-Open / Authority-Gated Posture

LIMA AI OS is capability-open and authority-gated.

Capability-open means LIMA is intended to govern broad capabilities across bots, shells, workstations, office systems, models, tools, files, browser, network, connectors, devices, robots, drones, IoT, automation, and physical-world systems.

Authority-gated means current candidate lanes allow only the authority they explicitly prove. A blocked capability means "not authorized by the current gate," not "impossible forever."

## Consumer Compatibility Freeze Status

Consumer integration compatibility/freeze metadata: `CANDIDATE_ONLY`

V1-G21 proves that LIMA can validate sanitized consumer compatibility metadata locally and deterministically. It does not edit consumer repositories, import consumer code, call consumer runtimes, wire shells, finalize public APIs, clean up exports, or approve product readiness.

## Provider Model Routing Authority Status

Provider/model routing authority metadata: `CANDIDATE_ONLY`

V1-G20 proves that LIMA can validate sanitized provider/model routing authority metadata locally and deterministically. It does not call providers/models, read secrets, access credentials, dispatch model requests, execute fallback, execute tools, or approve consumer integration.

## Live Approval Evidence Status

Live approval evidence/capture metadata: `CANDIDATE_ONLY`

V1-G19 proves that LIMA can validate sanitized approval evidence metadata locally and deterministically. It does not verify raw approval factors, persist raw PINs, issue approval tokens, execute actions, or approve consumer integration.

## Consumer Proof Packet Intake Status

Consumer proof packet audit intake: `CANDIDATE_ONLY`

V1-G18 proves that LIMA can validate consumer proof packet metadata locally and deterministically. It does not edit consumer repos, import consumer code, call consumer runtimes, wire shells, or approve integration.

## Current Blocked Areas

- Live provider/model calls are blocked.
- Secret lookup and credential access are blocked.
- Model dispatch and fallback execution are blocked.
- Actual file edit/delete/mutation execution is blocked.
- Raw live approval factor verification is blocked.
- Approval-token issuance is blocked.
- Connector behavior is blocked.
- Browser/network behavior is blocked.
- HumanInput bridge activation is blocked.
- Device/robot/drone/IoT/physical-world behavior is blocked.
- Consumer repository edits are blocked.
- Live consumer imports/calls are blocked.
- Consumer integration is blocked.
- Final public API freeze is not approved.
- Runtime export cleanup is not approved.
- Product readiness is not approved.

## Consumer Integration Status

Consumer integration: `BLOCKED`

Sparkbot, Sparkbot_shell, Arc-Bot-shell, LIMA Robo OS, LIMA Office, and other consumer repositories must remain unwired until final public API freeze, export review, proof packets, audits, and explicit integration approvals land. V1-G18 gives LIMA a proof intake boundary. V1-G21 gives LIMA compatibility/freeze metadata semantics. Neither approves consumer repository edits or live imports/calls.

## Product Readiness Status

Product readiness: `NOT_READY`

The current chain is candidate runtime authority infrastructure. It is not a product release, production readiness claim, consumer integration approval, final public API freeze, or runtime export cleanup approval.

## Final API Freeze Status

Final public API freeze: `NOT_APPROVED`

Candidate exports exist for approved slices, and V1-G21 can validate compatibility evidence against those candidate surfaces. No public API freeze is approved. Runtime export cleanup remains outside current gates unless a dedicated final-freeze approval lane exists.

## Physical-World Readiness Status

Physical-world readiness: `BLOCKED`

Device, robot, drone, IoT, humanoid, vehicle, facility, safety-critical, and physical-world actions require a dedicated physical-world authority and safety lane before they can be allowed.

## Next Recommended Lane

Next recommended lane: prepare V1-G22 final public API freeze approval request.

Reason: V1-G18 can intake consumer proof packets, V1-G19 can validate approval evidence metadata, V1-G20 can validate provider/model route authority metadata, and V1-G21 can validate consumer compatibility/freeze metadata. The next product-moving gap for safe Sparkbot and Arc-Bot-shell testing is a narrow final public API freeze gate that reviews candidate exports, import surfaces, compatibility fixtures, and unresolved blockers before any runtime export cleanup, consumer repository edits, live imports/calls, or consumer integration are approved.

Do not implement final public API freeze, runtime export cleanup, consumer repo edits, consumer runtime imports/calls, live provider/model calls, credential handling, external sends, file mutation execution, connector/browser/network behavior, physical-world behavior, or product-readiness claims without future exact approvals.
