# Black Arcana QA

Canonical Stage 05 real-client QA documents:

- `casting-ux-manual-matrix.md` — acceptance matrix and current PENDING/PASS/FAIL/BLOCKED state;
- `casting-ux-real-client-runbook.md` — real-client execution and evidence procedure;
- `casting-ux-real-client-evidence.md` — exact-SHA campaign/evidence ledger; automated preparation or artifact delivery never creates manual PASS evidence;
- `fixtures/stage05-real-client/README.md` — removable deterministic Minecraft 1.21.1 datapack fixture for hazard thresholds, normal/non-normal tooltip controls, Arcane Resistance 0/15/30 states, Iron cooldown/cost gate states, and stale-profile reload validation;
- `stage05a11-resistance-forecast.md` — historical automated implementation/authority evidence for selected-spell resistance and predictable-gate presentation. Under D034, Stage 05A remains blocked from promotion/audit progression until Stage 05 is fully complete.

The fixture is supporting infrastructure only. Its presence, its JUnit schema validation and a green CI run do not mark any manual matrix row PASS. Only direct real-client observations recorded under the runbook and evidence ledger may change manual acceptance state.

When a requested gate state cannot be produced by a legitimate provider/runtime configuration, keep that exercised subcase `BLOCKED`; do not add a debug bypass or fabricate client state solely to satisfy the matrix. Lack of an attached graphical client in an automated/repository-only session does not by itself convert untouched rows from `PENDING` to `BLOCKED`.

D034 is authoritative for numbered-stage promotion: Stage 05 remains active until its plan-defined physical/runtime-input/provider acceptance is complete. Stage 05A and later numbered stages must not be promoted while Stage 05 remains incomplete.
