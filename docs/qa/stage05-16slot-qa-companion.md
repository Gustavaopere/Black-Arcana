# Stage 05 — 16-slot QA companion

## Purpose

`black_arcana_stage05_qa` is a removable, test-only NeoForge companion mod for the Stage 05 Block I physical acceptance row. It exists only to provide sixteen legitimate server-registered Black Arcana spell identities so the canonical 16-slot loadout bound can be exercised in a real client without adding debug ingress or production gameplay content.

The companion is not a substitute for physical evidence. Its build, installation or presence does not make the Block I matrix row PASS.

## Authority boundary

The companion uses the existing `ArcanaServerRuntimeManager.addInitializer(...)` extension point. On server runtime creation it installs exactly sixteen selection-only spell definitions and execution engines under namespace `black_arcana_stage05_qa`.

The fixture spells intentionally deny execution before world mutation. They exist to make a legitimate server-owned 16-entry loadout possible; they do not create free production spells, bypass loadout validation, weaken casting gates or transfer authority to the client.

All companion Java/resources live under `src/stage05QaFixture/`. The canonical production `black_arcana-*.jar` must remain free of the companion mod ID, fixture classes and fixture resources. CI verifies this isolation.

## Exact-SHA delivery

After this fixture infrastructure is merged, a successful `main` workflow publishes two independent seven-day artifacts for the same commit SHA:

- `black-arcana-<full SHA>` — canonical production Black Arcana JAR;
- `black-arcana-stage05-qa-<full SHA>` — removable Stage 05 QA companion JAR.

For Block I, use the production JAR and companion artifact from the same exact `main` SHA. Do not mix a companion from one SHA with a production JAR from another SHA.

Record before testing:

- tested `main` SHA;
- successful exact-SHA workflow run ID;
- production artifact name, ID and digest;
- companion artifact name, ID and digest;
- extracted production JAR filename and independently checked digest;
- extracted companion JAR filename and independently checked digest.

Artifact publication is delivery/preflight evidence only. It is not manual PASS evidence.

## Block I profile procedure

1. Start from the exact physical modpack instance selected for the manual campaign.
2. Remove any older Black Arcana production JAR and any older `black_arcana_stage05_qa` companion JAR from the instance.
3. Install the exact-SHA production Black Arcana JAR.
4. Install the matching exact-SHA Stage 05 QA companion JAR.
5. Confirm the game loads with both `black_arcana` and `black_arcana_stage05_qa` present and no duplicate-mod warning.
6. Establish a legitimate server-owned loadout containing the sixteen companion spell identities.
7. Reopen/reconnect as required by the canonical Block I runbook and prove every canonical slot `0..15` is physically reachable through supported radial paging/selection.
8. Confirm selection remains non-casting and paging cannot select a seventeenth slot or substitute a different spell identity.
9. Record the required interaction evidence in `docs/qa/casting-ux-real-client-evidence.md` before changing the matrix state.

If the exact companion fails to load or cannot produce a legitimate server-owned 16-entry loadout, record the concrete attempted blocker or failure according to the runbook. Do not modify production runtime semantics merely to force a PASS.

## Isolation from other manual rows

The companion changes the available spell registry by adding sixteen QA-only identities. Therefore it should be enabled only for Block I, or any other row that explicitly declares the companion as part of its test profile.

Do not silently use evidence collected with `black_arcana_stage05_qa` installed to satisfy unrelated production-only rows. For Blocks A–H and J, use the normal campaign profile unless the row explicitly requires this companion and the evidence records that fact.

After Block I evidence is captured, remove the companion before returning to production-only campaign rows unless the runbook explicitly says otherwise.

## Removal

Removing the companion JAR removes the QA mod and its runtime initializer. The companion is not production content and must not be shipped as part of the Black Arcana production artifact or modpack release.
