# Stage 05 real-client QA fixture

This directory is a removable data pack for the Stage 05 / 05A.11 manual client gate. It is not loaded by Black Arcana automatically and must not be shipped as production gameplay data.

## Purpose

The fixture makes the manual matrix reproducible without adding debug commands, bypasses or client-authored gameplay state. It uses only the existing strict Black Arcana datapack loaders plus existing synthetic provider spells.

Prerequisites for the full fixture:

- Minecraft 1.21.1 / NeoForge;
- Black Arcana build under test;
- Iron's Spells 'n Spellbooks loaded for `black_arcana:irons_integration_probe`;
- Ars Nouveau loaded for `black_arcana:ars_integration_probe`.

If a provider is absent, mark only the scenarios that depend on that provider `BLOCKED`; do not treat missing provider behavior as a Black Arcana PASS or FAIL.

## Install

1. Copy the `stage05-real-client` directory into the target world's `datapacks/` directory, preserving `pack.mcmeta` and the `data/` directory at the pack root.
2. Start/open the world and run `/reload` as an operator.
3. Confirm the reload succeeds before collecting evidence. A reload error invalidates the fixture run.
4. Open the Black Arcana loadout editor. The fixture publishes presentation metadata for the Iron and Ars integration probes so they can be added to the server-authoritative loadout when their provider engines are installed.

The pack declares data-pack format 48, the format used by Minecraft Java 1.21/1.21.1.

## Static hazard controls

`black_arcana:irons_integration_probe` is the non-normal control:

- tier: `DANGEROUS`;
- minimum Arcane Resistance: `10`;
- recommended Arcane Resistance: `30`.

`black_arcana:ars_integration_probe` is the normal control:

- tier: `NORMAL`;
- minimum/recommended Arcane Resistance: `0/0`.

The Ars presentation key is intentionally the provider probe's canonical translation key. If that key is not localized in the build under test, the untranslated key is not evidence about hazard correctness; record it separately only if localization itself is being reviewed.

## Deterministic Arcane Resistance states

The fixture binds explicit QA-only containment profiles to two vanilla items. Only equipped standard slots count; carrying the items elsewhere in inventory does not contribute.

- `minecraft:stick` = +15 Arcane Resistance;
- `minecraft:blaze_rod` = +15 Arcane Resistance.

Use the Iron probe selected in the HUD:

1. Remove both fixture items from the six standard equipment slots: effective resistance should be `0`, which is below the minimum `10`.
2. Hold exactly one fixture item in main hand or off hand: effective resistance should be `15`, which is between minimum `10` and recommended `30`.
3. Hold the stick in one hand and the blaze rod in the other: effective resistance should be `30`, which meets the recommendation.

Do not use vanilla armor values as an implicit substitute; Black Arcana deliberately ignores vanilla armor/toughness unless an explicit containment profile exists.

## Predictable gate states available from the existing Iron probe

The Iron synthetic spell already has:

- mana cost: `20` Iron mana;
- cooldown: `40` ticks;
- progression gate: unconditional allow.

That provides legitimate states without changing production semantics:

### CLEAR

Put the Iron probe in the authoritative loadout, wait until its cooldown is finished, and ensure the player has at least 20 Iron mana. Select the probe. The preflight line may report only that no predictable gate blocks; it must not promise cast success.

### COOLDOWN

From CLEAR, cast the Iron probe successfully once. Immediately keep/reselect it while the 40-tick cooldown is active. The read-only gate forecast should report the cooldown category.

### COST

Wait until the cooldown is clear, then reduce Iron mana below 20 through legitimate provider gameplay/casts. With the Iron probe still valid in the authoritative loadout, the gate forecast should report the resource-cost category. Do not use a client-only edited value as evidence.

### PROGRESSION

`BLOCKED` with this fixture. The Iron, Ars and Malum synthetic engines currently install progression as unconditional allow. Producing a progression denial would require a different legitimate runtime spell/provider contract or a debug-only hook, so this fixture intentionally does not fabricate one.

### IDENTITY / LOADOUT

Exercise only if the real client/runtime can retain a selected spell while the server-authoritative loadout legitimately removes or rejects it. If the normal synchronization path clears selection before the forecast can be observed, record the matrix subcase as `BLOCKED` rather than manufacturing stale client state.

### PROJECTION / RUNTIME UNAVAILABLE

Exercise only through a legitimate unavailable provider/runtime configuration. Do not disable internal services or patch packets solely to manufacture this state.

## Datapack reload / stale-forecast fixture

The active Iron hazard file starts at profile version 1, DANGEROUS, thresholds 10/30.

For the reload transition:

1. Select the Iron probe and make a resistance forecast visible.
2. Record the before state in one continuous capture.
3. Replace the contents of `data/black_arcana/black_arcana/hazards/irons_integration_probe.json` in the installed world datapack with `alternates/irons_integration_probe.reload.json`.
4. Run `/reload`.
5. The synchronized static profile should become profile version 2, tier `FORBIDDEN`, thresholds `20/40`.
6. Confirm an older in-flight/cache result for DANGEROUS 10/30 cannot overwrite the new static preflight or gate/resistance presentation.
7. Restore the original repository version after the test if more baseline scenarios remain.

## Removal

Delete this fixture from the world's `datapacks/` directory and run `/reload` or restart the world. Do not leave these QA-only profiles enabled in normal gameplay evidence.

## Evidence rule

This fixture only makes states reproducible. It does not authorize any manual matrix row to be marked PASS without direct real-client observation recorded according to `docs/qa/casting-ux-real-client-runbook.md`.
