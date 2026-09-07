# Vampirism Integrations 1.10.2 — provider audit

Status: `SOURCE-PINNED 1.10.2 / CURRENT-PACK ELIGIBLE BRIDGES IDENTIFIED / JADE DISCOVERABLE + COLD SWEAT DEFAULT-ENABLED / RUNTIME QA PENDING`

## Version authority

- mod id: `vampirism_integrations`
- installed JAR: `vampirism_integrations-1.21.1-1.10.2.jar`
- runtime version: `1.10.2`
- Minecraft: `1.21.1`
- loader: NeoForge
- required base provider in the current pack: Vampirism `1.10.13`
- official source: `TeamLapen/VampirismIntegrations`
- exact audited source pin: `bff02b9686408691aea2c0c910ccb712edb18bd5`
- source license at the pinned revision: GNU LGPL v3
- Black Arcana provenance: `docs/provenance/REFERENCE_LEDGER.md`, `SOURCES.md`, `THIRD_PARTY_NOTICES.md`

The pinned source is the 1.10.2 line published on 2026-06-30. Its `gradle.properties` declares `main_version=1`, `major_version=10`, `minor_version=2`.

The source audit is read-only provenance evidence. No Vampirism Integrations code or assets are copied/adapted into Black Arcana by this catalog.

## Provider class

Vampirism Integrations is a **compatibility provider**, not an independent spell engine, faction or progression tree. Its job is to preserve Vampirism semantics when another supported mod is present.

This distinction is mandatory for the Black Arcana catalog:

- a HUD integration is not a new mechanical capability;
- a temperature modifier does not create a second temperature system;
- a blood conversion data map does not create a second blood authority;
- a villager converter does not create another faction authority;
- dormant source code for a missing mod is not an active capability of the installed pack.

## Current-pack result

The current 612-entry modlist contains the addon itself plus the relevant installed targets below:

| Target | Current pack | Source activation path | Audit result |
|---|---|---|---|
| Vampirism | installed `1.10.13` | `ModCompatLoader` dummy/base compat | ELIGIBLE BASE TARGET |
| Cold Sweat | installed `2.4.2` | registered `ColdSweatCompat`, accepted range `[2.2.3,)`, generated config default enabled | **ELIGIBLE / DEFAULT-ENABLED / RUNTIME UNCONFIRMED** |
| Jade | installed `15.10.6+neoforge` | independent `@WailaPlugin` discovery | **TARGET PRESENT / PLUGIN DISCOVERABLE / RUNTIME UNCONFIRMED** |
| Biomes O' Plenty | absent | registered `BOPCompat` | INACTIVE IN CURRENT PACK |
| WAILA/WTHIT mod id `waila` | absent | registered `WailaModCompat` | INACTIVE IN CURRENT PACK |
| EvilCraft | absent | registered `EvilCraftCompat` | INACTIVE IN CURRENT PACK |
| CraftTweaker | absent | registered `CrafttweakerCompat` | INACTIVE IN CURRENT PACK |
| Tough As Nails | absent | registered `TANCompat` | INACTIVE IN CURRENT PACK |
| MCA (`mca`) | absent | registered `MCACompat` + conditional data maps | INACTIVE IN CURRENT PACK |
| ChoiceTheorem's Overhauled Village | absent | registered CTOV compat | INACTIVE IN CURRENT PACK |
| Guard Villagers | absent | registered compat | INACTIVE IN CURRENT PACK |

### Important correction: Cold Sweat activation state

Source-level evidence proves that the target is present, the installed target version satisfies the declared range and the generated compat config is enabled by default. That proves **eligibility under stock configuration**, not actual runtime activation.

`ModCompatLoader` also requires the user's generated config to remain enabled and setup to complete without throwing. Until `/vampirism-integrations loaded` is checked in the exact pack, Black Arcana must not assume the Cold Sweat modifier path actually loaded.

### Important correction: Jade

`JadeModCompat` is not added to the central `ModCompatLoader` in 1.10.2, but that does **not** make Jade dormant. `JadePlugin` is annotated with Jade's `@WailaPlugin`, so Jade can discover it through its own plugin system when Jade is installed.

The current pack has Jade, therefore the source-level state is **discoverable with target present**. Exact plugin registration/rendering remains runtime QA rather than inferred PASS.

### Important correction: MineColonies

The 1.10.2 Gradle/deploy configuration references MineColonies as an optional build dependency, and MineColonies is installed in the pack. However, at the exact source pin there is no current MineColonies Java compat module and no MineColonies entry is added to `ModCompatLoader`. The source references found are build/deploy configuration only.

Therefore **MineColonies presence does not prove an active Vampirism Integrations mechanic in 1.10.2**. This remains fail-closed unless a concrete runtime path is found in the installed JAR or later provider source.

## What Cold Sweat would do if the compat loads

For Vampire players, the bridge adds transient modifiers to Cold Sweat's provider attributes:

- `cold_sweat:freezing_point` — lowers the freezing point by the configured Vampire cold-resistance amount;
- `cold_sweat:burning_point` — scales the burning point by the configured heat-vulnerability factor.

Defaults in 1.10.2:

- `enableTemperatureVampires = true`;
- `vampireColdResistance = 30 °C` before Cold Sweat unit conversion;
- `vampireBurningPointModifier = 0.7`.

The source path reconciles the modifiers on faction-level change, respawn and login and removes them when the player is no longer a Vampire.

Cold Sweat remains the authority for body temperature, thresholds and thermal consequences. Vampirism Integrations only changes the Vampire's provider attributes when the compat is actually prepared.

## What the Jade plugin exposes if discovered/registered

The 1.10.2 `JadePlugin` declares Vampirism information providers for:

- entity blood;
- player faction/Lord information;
- entity faction;
- Garlic Diffuser;
- Village Totem;
- Pedestal charging;
- Alchemy Table;
- Potion Table;
- Weapon Table;
- Research/Hunter Table;
- Altar of Inspiration;
- Altar of Infusion;
- Altar Pillar.

This is a presentation/query bridge. It does not modify blood, faction, altar or recipe settlement.

## Conditional data-map capabilities

The source also ships conditional Vampirism data-map entries for external providers. In the audited revision they include:

- MCA villagers: blood value 15 and custom conversion handler;
- Capybara: blood value 10 and default converter/overlay when the external entity exists;
- BOP blood fluid: conversion rate `0.4`;
- EvilCraft blood fluid: conversion rate `0.8`;
- Blood Magic Life Essence fluid: conversion rate `0.8`;
- Tinkers blood fluid: conversion rate `0.8`;
- EvilCraft filled blood orb: item blood value `800`.

All are guarded by mod/entity-existence conditions. None of those target providers are active in the current modlist snapshot, so these are **supported-but-inactive contracts**, not current gameplay capabilities.

## Documents

- [`ACTIVE-INTEGRATIONS.md`](./ACTIVE-INTEGRATIONS.md) — exact current-pack eligible/dormant compatibility inventory and runtime activation gate.
- [`TECHNICAL-AUDIT.md`](./TECHNICAL-AUDIT.md) — loader, Jade discovery, Cold Sweat authority, conditional data maps and failure behavior.
- [`INTEGRATION-RULES.md`](./INTEGRATION-RULES.md) — Black Arcana boundaries and deduplication rules.

## Closure gate

Source-level cataloging of the current-pack eligible/discoverable bridges is complete when:

1. Jade registration surface is documented;
2. Cold Sweat modifiers/gates are documented without inferring runtime activation;
3. registered-but-absent integrations are not promoted to current capabilities;
4. conditional data maps are separated from current-pack eligible integrations;
5. exact source/license provenance is recorded before source-derived constraints are treated as canonical;
6. Notion and global provider queue/matrix are synchronized.

Do **not** mark runtime QA confirmed until the exact installed combination has been exercised in game/dedicated server.