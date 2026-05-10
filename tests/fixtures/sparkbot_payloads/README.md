# Sparkbot Payload Fixture Mirrors

These fixtures are LIMA-owned synthetic mirrors of Sparkbot input payload shapes inspected at Sparkbot commit `f7d5ee2054794ea7156ffb51a009c058cb7757e6`.

They are not copied Sparkbot request objects, production contracts, verified identity evidence, authorization evidence, or route wiring. They contain no real user messages, credentials, live tokens, or private data.

No fixture imports Sparkbot, wires production routes, calls models, executes tools, opens terminal/PTY, triggers robot actions, or creates authority. Production adapter work remains blocked.

Fixture categories:

- `chat_payloads.json`: chat message stream and WebSocket message input shapes.
- `voice_payloads.json`: voice upload and transcript input shapes.
- `meeting_payloads.json`: meeting/roundtable room message and artifact shapes.
- `operator_payloads.json`: terminal/operator request and WebSocket input shapes.
- `mcp_approval_payloads.json`: MCP explain-plan and approval input shapes.
- `robot_request_payloads.json`: robotics natural-language command request shapes.

If a fixture category is not confirmed in a future inspected Sparkbot commit, keep the file with an empty array and note the missing surface here before updating tests.

Before real adapter work, Sparkbot `origin/main` must be rechecked, payload drift must be reviewed, and these mirrors must be updated if Sparkbot shapes changed.
