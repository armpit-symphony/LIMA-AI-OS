# Redaction / Privacy Contract

## Purpose

Define how LIMA Runtime classifies, references, redacts, retains, and exposes sensitive data in audit/spine events.

This contract does not implement redaction. This contract does not implement storage. This contract does not authorize access. This contract defines the required data handling model for future runtime work.

## Core Rule

Audit and lineage must be useful without leaking sensitive data.

Raw secrets must never be written to audit/spine events.

Sensitive data should be stored by reference when needed:

- `content_ref`
- `evidence_ref`
- `secret_ref`
- `transcript_ref`
- `file_ref`
- `memory_ref`
- `sensor_ref`
- `model_context_ref`

## Privacy Classes

PUBLIC:

- safe to show in normal logs/docs/UI

INTERNAL:

- internal operational data

PRIVATE:

- user/private workspace data

CONFIDENTIAL:

- sensitive business/user data

SECRET:

- credentials, API keys, vault material, tokens, passwords

RESTRICTED:

- regulated/highly sensitive data, identity, legal, medical, financial, or customer-sensitive data

SAFETY_CRITICAL:

- robot safety, physical-world risk, operator safety, hazardous environment data

BIOMETRIC:

- voiceprints, face, body, gait, BCI/thought-adjacent signals

UNKNOWN:

- default until classified

## Redaction Classes

NONE:

- no redaction needed

SUMMARY_ONLY:

- store summary, not raw content

REFERENCE_ONLY:

- store reference ID, not raw content

HASH_ONLY:

- store hash/fingerprint only

MASKED:

- store masked value

SECRET_REF_ONLY:

- vault/secret ref only, never raw

DROP:

- do not store

OPERATOR_ONLY:

- visible only to authorized operator view

BREAKGLASS_ONLY:

- visible only in scoped breakglass view

## Retention Classes

EPHEMERAL:

- short-lived runtime/session only

SHORT:

- short operational retention

STANDARD:

- normal audit retention

EXTENDED:

- long-lived compliance/debug retention

LEGAL_HOLD:

- cannot be deleted until released

DO_NOT_STORE:

- never persist raw content

## Visibility Classes

PUBLIC_VIEW:

- public or user-facing safe

OPERATOR_VIEW:

- operator-only

ADMIN_VIEW:

- admin-only

SECURITY_VIEW:

- security/audit-only

BREAKGLASS_VIEW:

- breakglass-only

SYSTEM_ONLY:

- machine-readable/internal only

NO_VIEW:

- never displayed raw

## Reference Types

content_ref:

- reference to stored/summarized content

evidence_ref:

- reference to evidence artifact

secret_ref:

- vault/secret reference only

transcript_ref:

- voice transcript or meeting transcript reference

file_ref:

- uploaded/generated file reference

memory_ref:

- memory item reference

sensor_ref:

- robot/device sensor reference

model_context_ref:

- prompt/context/model input reference

approval_ref:

- approval evidence reference

policy_ref:

- policy/rule reference

## Data Handling Rules

- raw secrets are never stored in events
- tokens/API keys/passwords are SECRET_REF_ONLY or DROP
- raw voice transcripts default to PRIVATE or CONFIDENTIAL and SUMMARY_ONLY or REFERENCE_ONLY
- future BCI/thought-adjacent data defaults to BIOMETRIC and REFERENCE_ONLY or DROP
- robot sensor data defaults to SAFETY_CRITICAL or BIOMETRIC depending content
- terminal output may contain secrets and should default to REFERENCE_ONLY with redaction
- browser/network data may contain private data and should default to REFERENCE_ONLY unless safe
- model prompts/context may contain private data and should default to REFERENCE_ONLY or SUMMARY_ONLY
- file contents should be referenced, not copied into audit events
- memory contents should be referenced or summarized, not copied raw
- approvals can store metadata but not raw PINs/tokens/secret material

## Audit Event Requirements

Spine/Audit events should include:

- `privacy_class`
- `redaction_class`
- `retention_class`
- `visibility_class`
- `content_ref` when raw content is externalized
- `evidence_refs`
- `secret_refs` when applicable
- `redacted_summary` when safe
- `contains_secret` flag when known
- `contains_biometric` flag when known
- `contains_safety_critical` flag when known
- `data_subject_ref` when applicable
- `retention_expires_at` when applicable

## Critical Source Defaults

HumanInput:

- text: PRIVATE unless public context
- voice: PRIVATE/BIOMETRIC depending stored audio/voiceprint
- future_bci: BIOMETRIC + REFERENCE_ONLY or DROP

IntentEnvelope:

- normalized_text can be PRIVATE
- typed_args may be CONFIDENTIAL
- use SUMMARY_ONLY/REFERENCE_ONLY for sensitive args

GuardianDecision:

- can store metadata and reason
- must not store raw secrets

ApprovalMetadata:

- store method/status/scope
- never store raw PIN, hardware key material, signed token secret, or credential

ToolExposureDecision:

- can store selected_tools/packs
- must not store raw tool secrets/args

ModelCallEvent:

- prompt/context should be REFERENCE_ONLY or SUMMARY_ONLY
- model output may be PRIVATE/CONFIDENTIAL depending content

ToolCallEvent:

- args/results may need REFERENCE_ONLY
- external sends require evidence refs

TerminalEvent:

- command may be CONFIDENTIAL
- output should default REFERENCE_ONLY with secret scanning later

RobotEvent:

- sensor data REFERENCE_ONLY
- movement/manipulation SAFETY_CRITICAL
- camera/mic/biometric data BIOMETRIC/RESTRICTED

FileEvent:

- file contents by file_ref
- destructive ops record path/target_ref safely, not raw file content

Network/BrowserEvent:

- URLs may be sensitive
- authenticated pages/content by REFERENCE_ONLY

## Sparkbot Extraction Notes

- `stream_chat_with_tools()` must avoid writing raw prompt/tool args/results directly into audit events
- voice transcript path needs `transcript_ref` and transcript confidence
- terminal/PTY path must avoid raw secret leakage in terminal output
- dynamic skills must declare privacy/redaction requirements
- browser/file/network/comms tools must classify args/results before audit persistence
- robotics bridge must classify sensor/physical-world data

## Redaction vs Authorization

Redaction/privacy controls do not authorize execution. `GuardianDecision` still gates execution. `ApprovalMetadata` still records approval evidence. Redaction controls what can be stored, displayed, retained, or referenced.

## Acceptance Criteria

- Redaction/privacy doc exists.
- `PrivacyClass`, `RedactionClass`, `RetentionClass`, `VisibilityClass` contracts exist.
- Reference metadata contract exists.
- Audit/spine events can carry privacy/redaction/retention/visibility fields.
- Raw secrets are documented as never stored in audit events.
- BCI/thought-adjacent data is BIOMETRIC and never direct control/approval.
- Robot sensor/physical-world data has safety/privacy defaults.
- No runtime redaction implementation exists.
- No storage implementation exists.
- No Sparkbot code copied.
- Tests validate import/contract shape only.
