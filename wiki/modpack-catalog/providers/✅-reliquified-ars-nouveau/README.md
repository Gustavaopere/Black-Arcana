# Reliquified Ars Nouveau — 0.8.1

Status: `✅ CATALOGED / CURRENT PHYSICAL 0.8.1 / COUNTED_SOURCE_PINNED / 19 PROVIDER-OWNED RELIC ABILITY ROOTS / +19 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current physical Project Library modlist authority records:

- JAR: `reliquified_ars_nouveau-1.21.1-0.8.1.jar`;
- mod id: `reliquified_ars_nouveau`;
- runtime: `0.8.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- mixin config: `reliquified_ars_nouveau.mixins.json`;
- physical SHA-1: `4be1f4b0fd7fbec6618596e2e7c3705db88a7579`.

## Exact-version source pin

Official repository: `Octo-Studios/reliquified_ars_nouveau`.

Source checkpoint: `125e1e3a723d8bc7050026e0670f8ac49535c8bc` on branch `1.21.1`.

At this checkpoint `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `mod_id=reliquified_ars_nouveau`;
- `mod_version=0.8.1`;
- NeoForge development baseline `21.1.194`.

`neoforge.mods.toml` describes the provider as a compatibility addon between Relics and Ars Nouveau and declares required ranges:

- Relics `[0.12.3,)`;
- Ars Nouveau `[5.10.2,)`;
- Curios `[9.3.1+1.21.1,)`.

The current pack uses Relics `0.12.8` and Ars Nouveau `5.13.1`, satisfying the declared provider ranges. Range satisfaction is not an assembled-runtime PASS.

Source license metadata is `All Rights Reserved`. This catalog is clean-room factual interoperability analysis; it does not authorize copying source, assets, localization or implementation bodies.

Physical-JAR ↔ source-build byte equality has not been established, so this evidence state is `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

## Registry and semantic inventory

`ItemRegistry` registers exactly **19 provider-owned relic items**. Across those provider item classes, exact source inspection closes exactly **19 distinct `AbilityTemplate.builder(...)` roots**. The English localization contains the same 19 owner-scoped ability roots.

### Counted ability roots

| # | Registered item | Item display name | Ability ID | Localized ability name |
|---:|---|---|---|---|
| 1 | `architects_staff` | Architect's Staff | `bridgecraft` | Arcane Masonry |
| 2 | `archmage_glove` | Archmage Glove | `multicasted` | Echo Spell |
| 3 | `ballistarian_bracer` | Ballistarian Bracer | `ballistary` | Spectral Volley |
| 4 | `cloak_of_concealment` | Cloak of Concealment | `absorption` | Mana Barrier |
| 5 | `emblem_of_assault` | Emblem of Assault | `onslaught` | Battle Echo |
| 6 | `emblem_of_defense` | Emblem of Defense | `sentinel` | Runic Watch |
| 7 | `emblem_of_devotion` | Emblem of Devotion | `devotion` | Orbit of Devotion |
| 8 | `flaming_bracer` | Flaming Bracer | `pyroclastic` | Pyroclastics |
| 9 | `horn_of_the_wild_hunter` | Horn of the Wild Hunter | `summoner` | Call of the Pack |
| 10 | `illusionists_mantle` | Illusionist's Mantle | `deception` | Deceptive Response |
| 11 | `mana_ring` | Mana Ring | `resonance` | Arcane Reserve |
| 12 | `quantum_bubble` | Quantum Bubble | `stasis` | Quantification |
| 13 | `ring_of_last_will` | Ring of Last Will | `last_will` | Last Will |
| 14 | `ring_of_thrift` | Ring of Thrift | `thrift` | Mana Thrift |
| 15 | `spiked_cloak` | Spiked Cloak | `thorn_burst` | Thorn Burst |
| 16 | `staff_of_the_spectral_walker` | Staff of the Spectral Walker | `spectral` | Spectral Dash |
| 17 | `whirling_broom` | Whirling Broom | `broom` | Whirling Flight |
| 18 | `whirlisprig_petals` | Whirlisprig Petals | `petal_lift` | Petal Lift |
| 19 | `wing_of_the_wild_stalker` | Wing of the Wild Stalker | `wild_flight` | Predatory Flight |

Rank/stat modifiers, experience sources, item containers, spawned entities/projectiles, status effects and downstream consequences are not counted as additional semantic identities.

## Provider-native reachability

The exact source set closes the same **19 classes** under both:

- `AbilityTemplate.builder(...)`; and
- `LootTemplate.builder(...)`.

Every ability-bearing relic therefore has provider-native source-level loot routing through both:

- `LootEntries.ARS_NOUVEAU`;
- `LootEntries.ARS_NOUVEAU_LIKE`.

`LootEntries.ARS_NOUVEAU` admits matching magic/Ars-like biome names and chest tables across dimensions with weight `600`. `LootEntries.ARS_NOUVEAU_LIKE` admits magic/Ars-like chest-table paths or Ars-namespaced chest tables across dimensions, also with weight `600`.

This is sufficient source-level evidence for a provider-owned acquisition route for all 19 counted ability-bearing relics. It does not prove final assembled loot-table mutation, world generation frequency or player acquisition in a particular save.

## Semantic disposition

The Black Arcana semantic metric counts discrete provider-owned supernatural player actions while excluding the relic item/gear container itself and downstream effects.

The 19 owner-scoped Relics ability roots are distinct provider actions and are therefore **`COUNTED_SOURCE_PINNED`**.

Semantic contribution: **+19 strict objects**.

## Authority boundaries

- Reliquified Ars Nouveau owns these relic ability identities and its Ars-specific Relics integration.
- Relics owns the generic relic progression/ability framework.
- Ars Nouveau owns glyph/spell registry semantics, source/mana and native spell execution when an ability delegates to Ars.
- A relic ability that invokes an Ars spell/glyph/effect does not mint a second copy of that Ars identity.
- Black Arcana must not duplicate relic progression, source/mana settlement, Ars casting or provider ability execution.
- RPG Skill Tree remains sibling authority only for its own progression, attributes, Mastery, perks and gates through verified contracts.

## Runtime and compatibility QA remains separate

Catalog closure does not assert assembled-pack PASS. Relevant runtime gates include:

- client + dedicated-server boot with physical Reliquified Ars Nouveau 0.8.1, Relics 0.12.8 and Ars Nouveau 5.13.1;
- actual provider loot injection and survival acquisition in the assembled pack;
- relic equip/progression persistence and independent multiplayer state;
- abilities that read, spend or mutate Ars source/mana;
- abilities that cast/delegate Ars spell recipes or spawn provider entities/projectiles;
- no duplicate cast/resource/cooldown/progression settlement;
- packet/mixin compatibility across reload, reconnect and restart.

## Result

**✅ Cataloged — `COUNTED_SOURCE_PINNED`.**

Current semantic inventory: **19 provider-owned supernatural Relics ability roots**. Strict global semantic delta: **+19**.
