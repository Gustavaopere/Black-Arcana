# Black Arcana QA

Canonical Stage 05 / 05A presentation QA documents:

- `casting-ux-manual-matrix.md` — acceptance matrix and current PENDING/PASS/FAIL/BLOCKED state;
- `casting-ux-real-client-runbook.md` — real-client execution and evidence procedure;
- `fixtures/stage05-real-client/README.md` — removable deterministic Minecraft 1.21.1 datapack fixture for hazard thresholds, normal/non-normal tooltip controls, Arcane Resistance 0/15/30 states, Iron cooldown/cost gate states, and stale-profile reload validation;
- `stage05a11-resistance-forecast.md` — automated implementation/authority evidence for selected-spell resistance and predictable-gate presentation.

The fixture is supporting infrastructure only. Its presence, its JUnit schema validation and a green CI run do not mark any manual matrix row PASS. Only direct real-client observations recorded under the runbook may change manual acceptance state.

When a requested gate state cannot be produced by a legitimate provider/runtime configuration, keep that subcase `BLOCKED`; do not add a debug bypass or fabricate client state solely to satisfy the matrix.
