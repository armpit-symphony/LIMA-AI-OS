# Shell-Owned Translator Fixtures

These fixtures are synthetic and non-executing. They describe future
Sparkbot/Arc-owned translation inputs and outputs without implementing a
translator.

Only fixtures with `translation_state: "translated"` may be mapped into
`KernelRequest` by tests. Fixtures with `blocked` or `needs_clarification`
must not call `LimaKernel`.

These fixtures are not public Sparkbot integration, Arc Bot integration,
HumanInput runtime input, IntentEnvelope runtime records, Guardian authority,
provider routing, model calls, tool execution, connector access, persistence,
live discovery, Robo-OS access, device control, robotics, drones, or
physical-world behavior.
