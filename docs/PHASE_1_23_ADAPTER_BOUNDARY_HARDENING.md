# Phase 1.23 Adapter Boundary Hardening

## Purpose

Harden tests that protect LIMA adapters from production/runtime coupling.

## Scope

This phase adds boundary tests only.

It does not implement adapters.
It does not wire production routes.
It does not modify Sparkbot.

## Protected Boundary

Adapters may:

- accept neutral payloads
- return contract objects such as HumanInput
- carry passive metadata

Adapters may not:

- import Sparkbot
- import FastAPI/WebSocket route layers
- call models
- execute tools
- open terminal/PTY
- call Robo-OS
- access DB/storage
- access env vars
- call network
- persist audit data
- enforce Guardian/policy/approval/autonomy

## Forbidden Imports and Methods

Forbidden import categories include:

- Sparkbot runtime modules
- FastAPI, WebSocket, APIRouter, Request, and Depends route layers
- Sparkbot route, CRUD, model, service, and ChatUser modules
- model/tool execution paths such as stream_chat_with_tools and execute_tool
- terminal/PTY/subprocess modules
- filesystem, env, socket, and network clients
- SQLite, SQLAlchemy, Redis, and other storage clients
- payment, cloud, robotics, Docker, Kubernetes, and model-provider clients

Forbidden adapter method categories include:

- execution methods
- model/tool call methods
- route wiring methods
- persistence methods
- terminal/driver/robot methods
- IntentCompiler, GuardianDecision, approval, policy, auth, trust, autonomy, and secret methods

The current SparkbotHumanInputAdapter remains limited to:

- adapt_chat_payload
- adapt_voice_payload
- adapt_meeting_payload
- adapt_operator_payload

## Why This Matters

Adapter code is the first place where production wiring could creep in. Boundary tests keep LIMA safe before real adapter work.

Adapters are allowed to normalize neutral input into HumanInput. They are not allowed to become live Sparkbot routes, execution surfaces, persistence writers, model callers, tool callers, Guardian enforcers, or robot drivers.

## Acceptance Criteria

- adapter boundary tests exist
- tests scan local lima/adapters only
- forbidden imports blocked
- forbidden methods blocked
- current adapter still returns HumanInput only
- no runtime behavior added
