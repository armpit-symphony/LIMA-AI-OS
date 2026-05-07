# Reference Repositories

These repositories ground LIMA Runtime extraction. They are references, not sources to blindly copy during Phase 0.

## Sparkbot

Repository: `https://github.com/armpit-symphony/Sparkbot`

Role:

- Source of truth.
- Battle-tested shell and current implementation.
- Contains the hidden runtime/kernel pieces.
- Holds recent Guardian, model routing, tool policy, MCP, Spine, memory, approval, and audit improvements.

Observed Phase 0 notes:

- Sparkbot has a Guardian Suite service surface for auth, policy, executive journaling, verifier, token routing, task scheduling, pending approvals, memory, vault, and Spine.
- Sparkbot documents a Guardian/Spine flow where model routing, tool policy, guarded execution, audit, memory, and task lineage connect.
- Sparkbot includes MCP registry and run planning surfaces that already distinguish plan/approval state from direct execution.
- Recent Sparkbot changes should be reviewed before any extraction, especially around approval redaction, breakglass, token routing, memory lifecycle, and run timelines.
- Phase 0.6 adds `docs/SPARKBOT_ENTRYPOINT_INVENTORY.md` as a required pre-extraction step so chat, voice, model, tool, Guardian, terminal, browser, network, meeting, and robotics entrypoints are classified before code moves.

## LIMA-Guardian-Suite

Repository: `https://github.com/armpit-symphony/LIMA-Guardian-Suite`

Role:

- Earlier Guardian extraction.
- Useful reference for module shape and Guardian components.
- May lag recent Sparkbot Guardian improvements.

Observed Phase 0 notes:

- The extracted Guardian shape includes policy, auth, executive, verifier, vault, token guardian, task guardian, memory, meeting recorder, and pending approvals.
- Some files still import Sparkbot application modules such as `app.crud`, `app.models`, and route-level services.
- Future extraction must decouple Guardian core from Sparkbot app models while keeping a Sparkbot adapter.

## LIMA-Robo-OS

Repository: `https://github.com/armpit-symphony/LIMA-Robo-OS`

Role:

- Robotics driver/runtime layer.
- Future LIMA Runtime IO driver boundary.
- Should register capabilities, support dry runs, expose telemetry, and require Guardian approval for physical execution.

Observed Phase 0 notes:

- Robo-OS has command contracts for robot ID, environment, requested action, risk level, approval requirement, Guardian decision, MCP tool name, args, result, telemetry snapshot, and audit timestamp.
- The roadmap points toward a bridge from natural language to MCP tools, simulation first, then guarded hardware support.
- Medium/high real-world motion requires human-in-loop approval. Unknown or unsafe commands should block by default.

## No Secrets

Reference repo inspection for Phase 0 is architectural only. Do not import secrets, tokens, local databases, production deployment settings, or live credentials into LIMA-AI-OS.
