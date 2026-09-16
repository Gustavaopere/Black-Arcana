# Ars Technica 2.7.6 — registries

Status: `SOURCE-PINNED REGISTRY INVENTORY`

Source checkpoint: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`.

## Spell parts

Production `GlyphRegistry`: **11** entries. The full finite spell-part inventory is normalized in [`GLYPHS.md`](GLYPHS.md).

## Blocks — 3

| ID | Class / role |
|---|---|
| `ars_technica:source_motor` | `SourceMotorBlock` — Ars Source → Create kinetic generation. |
| `ars_technica:precise_relay` | `PreciseRelay` — Ars Source relay with provider-customizable transfer cooldown. |
| `ars_technica:transmutation_turret` | `TransmutationTurretBlock` — provider spell-processing turret using Source and a specialized Ars `TileCaster`. |

`precise_relay` is intentionally not treated as a second Source network. Its block entity derives from Ars `RelayTile` and transfers between Ars `AbstractSourceMachine` instances.

## Block entities — 3

- `ars_technica:source_motor_block_entity`
- `ars_technica:precise_relay_tile`
- `ars_technica:transmutation_turret_block_entity`

## Misc entity types — 8

- `ars_technica:arcane_polish_entity`
- `ars_technica:arcane_hammer_entity`
- `ars_technica:arcane_press_entity`
- `ars_technica:arcane_compact_entity`
- `ars_technica:arcane_pack_entity`
- `ars_technica:arcane_fusion_entity`
- `ars_technica:arcane_whirl_entity`
- `ars_technica:item_projectile_entity`

These are provider processing/projectile entities. They do not establish independent Black Arcana cast causality.

## Items and provider equipment

Concrete registrations/source-created block items at this checkpoint include:

- `calibrated_precision_mechanism`
- `technomancer_helmet`
- `technomancer_chestplate`
- `technomancer_leggings`
- `technomancer_boots`
- `artificer_cap`
- `artificer_tunic`
- `artificer_pants`
- `artificer_shoes`
- `machinaguard_helmet`
- `machinaguard_chestplate`
- `machinaguard_leggings`
- `machinaguard_boots`
- `transmutation_focus`
- `spy_monocle`
- `giant_experience_gem`
- `gargantuan_experience_gem`
- `source_motor`
- `transmutation_turret`
- `pocket_factory`
- `mark_of_technomancy`
- `blank_disc`

The old `ars_technica:runic_spanner` is not a second registered wrench in 2.7.6: `ItemRegistry` aliases that old ID to `create:wrench`, and the provider uses a persistent `runic_wrench` data component/mixins to retain Arcane Wrench semantics for migrated stacks.

No independent `precise_relay` block item is registered by the audited source path; the block is reached through provider conversion of the base Ars Source Relay.

## Ars perk surface

One provider perk is registered:

- `ars_technica:thread_pressure` — `PressurePerk`.

All **12 armor pieces** are registered as Ars perk providers. Each receives four perk-provider groups, each group accepting Ars `PerkSlot.ONE`, `TWO` or `THREE` under the exact provider registration path. Black Arcana and RPG Skill Tree must not replace that Ars armor-thread authority.

## Persistent data components — 3

- `ars_technica:air` — persistent float, used by Pressure/backtank integration;
- `ars_technica:zoomed` — persistent boolean, Spy Monocle client/use state;
- `ars_technica:runic_wrench` — persistent boolean carried on Create's wrench for Arcane Wrench compatibility/migration.

## Bootstrap/lifecycle

The provider constructor registers its normal registries, registers `PressurePerk`, registers all eleven glyphs, installs the Create/Catnip Source Motor packet registry, and registers COMMON/CLIENT config specs. During common setup it adds Ars armor perk providers and registers Create Source Motor stress values. The Source Motor is registered with stress capacity **256** and generator speed **256** in the provider setup.

Runtime registry presence in the installed 2.7.6 JAR/full pack remains a separate validation gate; this file records the exact source registration surface.