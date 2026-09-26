# Reliquified Iron's Spells 'n Spellbooks — 0.2.7

Status: `✅ CATALOGED / CURRENT PHYSICAL 0.2.7 / COUNTED_SOURCE_PINNED / 25 PROVIDER-OWNED RELIC ABILITY ROOTS / +25 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current physical Project Library authority (2026-09-16):

- JAR: `reliquified_irons_spells_and_spellbooks-1.21.1-0.2.7.jar`;
- mod id: `reliquified_irons_spells_and_spellbooks`;
- runtime: `0.2.7`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `e22fd94c87cb88b3cfa4637c48a1058260d35a9b`;
- mixin config: `reliquified_irons_spells_and_spellbooks.mixins.json`.

The sibling legacy dossier `PROJECT-INSTRUCTIONS/modlist/reliquified-irons-spells-n-spellbooks.md` identifies the same provider/version but is not used as the newest physical authority.

## Exact source pin

Official repository: `Octo-Studios/reliquified-irons-spells-n-spellbooks`.

Exact source checkpoint: `1dfa5557ae3ae59c793682bd8e386f81d7feaa32` on branch `1.21.1`.

That commit is dated 2026-06-09, carries commit message `Version bump - 0.2.7`, and its `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `mod_id=reliquified_irons_spells_and_spellbooks`;
- `mod_version=0.2.7`;
- NeoForge development baseline `21.1.200`.

The source metadata declares required Relics version range `[0.12.3,)`; the current pack uses Relics 0.12.8, which satisfies that declared range. Range satisfaction is not an assembled-runtime PASS.

Source license metadata is `All Rights Reserved`; this audit is clean-room factual inspection only and does not imply code/assets/text reuse rights.

## Registry and semantic inventory

`RISASItems` registers **24 provider-owned items**. The exact source search across all provider item classes closes **25 distinct `AbilityTemplate.builder(...)` roots in 23 relic classes**.

`HatOfOmniscienceItem` is the one registered item without its own ability template; it is therefore gear/content but contributes no semantic action by itself.

Two relics own two ability roots each:

- `ShadowClawsItem`: `shadow_claws` + `shadow_slash`;
- `SlicerItem`: `slicer_weapon` + `slicer`.

All other ability-bearing relic classes own one root each.

### Counted ability roots

| # | Relic/item | Ability ID | Localized ability name |
|---:|---|---|---|
| 1 | Bloodstained Voodoo Doll | `voodoo_mark` | Blood Mark |
| 2 | Cardiac Trap | `cardiac_trap` | Heart Stop |
| 3 | Cloak of the Bloody Feather | `blood_feather` | Blood Feather |
| 4 | Dimension Key | `dimension_key` | Interdimensional Corridor |
| 5 | Dragon Blood Vial | `dragon_blood` | Blood Drop |
| 6 | Echo Glove | `echo_glove` | Echo Strike |
| 7 | Ender Bow | `ender_bow` | Ender Arrow |
| 8 | Flask of the Red Mist | `red_mist` | Red Mist |
| 9 | Galaxy Devourer Diadem | `galaxy_devourer_diadem` | Event Horizon |
| 10 | Immaterial Disperser | `immaterial_disperser` | Dispersal |
| 11 | Living Flesh | `living_flesh` | Living Pursuit |
| 12 | Lunar Sextant | `lunar_sextant` | Starfall |
| 13 | Mask of Hunger | `hunger_mask` | Draining Hunger |
| 14 | Mirror of Transgression | `mirror_of_transgression` | Returning Gleam |
| 15 | Pulsar Mantle | `pulsar_mantle` | Pulsar Burst |
| 16 | Ring of Blades | `ring_of_blades` | Bloody Blade |
| 17 | Ring of Elusiveness | `elusiveness` | Elusiveness |
| 18 | Sealed Claymore | `sealed_claymore` | Seal of Claymores |
| 19 | Sealed Rapier | `sealed_rapier` | Seal of Rapiers |
| 20 | Sealed Sword | `sealed_sword` | Seal of Swords |
| 21 | Shadow Claws | `shadow_claws` | Shadow Claws |
| 22 | Shadow Claws | `shadow_slash` | Shadow Slash |
| 23 | Sinner's Crown | `sinner_crown` | Procession of Sinners |
| 24 | Slicer | `slicer_weapon` | Bloody Knuckles |
| 25 | Slicer | `slicer` | Meat Grinder |

Rank modifiers, statistics, experience sources, spawned projectiles/entities, status effects and downstream consequences are not counted as additional semantic identities.

## Reachability

Every one of the **23 ability-bearing relic classes** constructs a `LootTemplate` containing `RISASLootEntries.ANY_STRUCTURE`.

`RISASLootEntries.ANY_STRUCTURE` is source-defined with:

- dimension regex `.*`;
- biome regex `.*`;
- loot-table regex `irons_spellbooks:chests\/[\w_\/]*[\w]+[\w_\/]*`;
- weight `500`.

This closes a provider-native source-level acquisition route through Iron's structure chest loot for every counted ability-bearing relic.

## Semantic disposition

The Black Arcana semantic metric counts discrete provider-owned supernatural player actions, while excluding the item/gear container itself and downstream effects.

These 25 ability roots are provider-owned Relics-framework actions with distinct causal gameplay identities. They are therefore **`COUNTED_SOURCE_PINNED`**.

Semantic contribution: **+25 strict objects**.

The physical JAR hash is known, but byte-for-byte equivalence between the installed artifact and the public source build has not been established; therefore this is not labeled `COUNTED_EXACT`.

## Authority boundaries

- Reliquified Iron's owns these relic ability identities and their Relics-framework state.
- Relics owns the generic relic progression/ability framework.
- Iron's Spells owns external spell registries, mana, cooldowns and spell runtime when an ability references or reuses Iron's mechanics.
- A Reliquified ability invoking an Iron's spell/effect does not mint a second copy of the Iron's spell identity.
- Black Arcana must not create duplicate relic progression, duplicate mana/cooldown settlement or a second execution path for provider abilities.
- RPG Skill Tree remains sibling authority for its own progression/attributes/Mastery/perks/gates only through real contracts.

## Runtime and compatibility QA remains separate

Catalog closure does not assert assembled-pack PASS. Relevant runtime gates include:

- client + dedicated-server boot with physical 0.2.7, Relics 0.12.8 and Iron's 3.16.3;
- actual structure-loot generation in the assembled pack;
- relic equip/progression persistence and independent multiplayer state;
- abilities that read/restore Iron's mana;
- abilities that reuse Iron's damage sources or summoned-weapon mechanics;
- no double-cast/double-charge/double-loot settlement;
- packet/mixin compatibility and restart/reload lifecycle.

## Result

**✅ Cataloged — `COUNTED_SOURCE_PINNED`.**

Current semantic inventory: **25 provider-owned supernatural relic ability roots**. Strict global semantic delta: **+25**.
