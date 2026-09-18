# Black Arcana QA

Canonical Stage 05 real-client QA documents:

- `casting-ux-manual-matrix.md` — acceptance matrix and current PENDING/PASS/FAIL/BLOCKED state;
- `casting-ux-real-client-runbook.md` — real-client execution and evidence procedure;
- `stage05-block-j-provider-real-profile.md` — mandatory companion profile for Block J provider-real preparation and authority observations; supporting automation never creates physical PASS evidence;
- `casting-ux-real-client-evidence.md` — exact-SHA campaign/evidence ledger; automated preparation or artifact delivery never creates manual PASS evidence;
- `fixtures/stage05-real-client/README.md` — removable deterministic Minecraft 1.21.1 datapack fixture for hazard thresholds, normal/non-normal tooltip controls, Arcane Resistance 0/15/30 states, Iron cooldown/cost gate states, and stale-profile reload validation;
- `stage05a11-resistance-forecast.md` — historical automated implementation/authority evidence for selected-spell resistance and predictable-gate presentation. Under D035, this historical Stage 05A note no longer blocks implementation progression; manual evidence remains deferred to Stage 09.
- `provider-catalog-deployed-evidence.md` + `provider-catalog-deployed-evidence-collector.py` — read-only catalog evidence collector for current-pack provider hashes and narrowly selected deployed config keys. It supports conditional-provider closure only; running it never creates Stage 05 PASS evidence or automatic catalog promotion.

The fixture is supporting infrastructure only. Its presence, its JUnit schema validation and a green CI run do not mark any manual matrix row PASS. Only direct real-client observations recorded under the runbook and evidence ledger may change manual acceptance state.

When a requested gate state cannot be produced by a legitimate provider/runtime configuration, keep that exercised subcase `BLOCKED`; do not add a debug bypass or fabricate client state solely to satisfy the matrix. Lack of an attached graphical client in an automated/repository-only session does not by itself convert untouched rows from `PENDING` to `BLOCKED`.

D035 is authoritative for validation timing: Stage 05 engineering may close after implementation/integration/deterministic acceptance and explicit transfer of physical rows. Those rows remain PENDING in the Stage 09 release campaign and may never be inferred as PASS from automation.
