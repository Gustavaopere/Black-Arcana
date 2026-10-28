# Demon Warrior archetype profiles

Status: `BINARY_VERIFIED` for the exact publisher Acolyte 1.0.3 artifact; assembled-pack behavior, installed-JAR hash equality and physical QA are `NOT_VERIFIED` / `NOT_TESTED`. This is an Acolyte loadout/configuration surface and adds **0 Acolyte-owned spells**. See [release evidence](../BINARY-CONTRACTS-1.0.3.md) and the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).

`data/acolyte/archetype/demon/warrior.json` supplies the `demon/warrior` key returned by `DemonWarriorEntity#getArchetypeName()Ljava/lang/String;` (PCs 0–2). It contains 7 entries, in the order below, with total weight **76**. Entries omit explicit IDs, so the loader assigns `demon/warrior:0` through `demon/warrior:6`. These are profile IDs, not entity registry IDs.

## Selection and biome variants

All entries omit `biomes`, `name` and `skin`; every shipped entry is eligible in every biome. Each entry has probability `weight/76` in this unchanged publisher pool. The tier totals are 40/76 for tier 1, 24/76 for tier 2 and 12/76 for tier 3. Reloaded datapacks can change that denominator and eligibility. The [loadout pipeline](../systems/archetype-loadout-pipeline.md) documents parsing, filtering, ordinal IDs, persistence and equipment application.

All seven biome folders use this same loadout pool: **desert, jungle, plains, savanna, snowy, swamp and taiga**. Skin variant is chosen independently as 0, 1 or 2; the packaged paths are `acolyte:textures/entity/generic_skin/<folder>/demon<variant>.png`. Folder resolution checks biome path text in order: `taiga`, `desert`, `jungle`, `savanna`, `snowy` or `frozen`, `swamp`, then `badlands`→`desert`; everything else resolves to `plains`. Thus these 21 skin combinations do not establish 21 different spell pools.

## Stats and timing

HP uses Minecraft health points (2 HP = 1 heart); armor and attack are base attribute values before equipment and host combat resolution. Intervals use game ticks, with 20 ticks = 1 second at the nominal tick rate. `quality` is a host goal parameter, not a spell level. All entries default to XP reward 15, barrage count 1 and first-single-use delay 30 ticks; none overrides movement speed 0.25 or follow range 24 blocks.

| Profile suffix | Tier | Weight | HP | Base attack | Base armor | `attack_interval` | `quality` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `:0` | 1 | 20/76 | 35.0 | 0.0 | 3.0 | 25 | 0.3 |
| `:1` | 1 | 20/76 | 35.0 | 0.0 | 3.0 | 50 | 0.3 |
| `:2` | 2 | 12/76 | 50.0 | 1.5 | 6.0 | 20 | 0.3 |
| `:3` | 2 | 12/76 | 50.0 | 1.5 | 6.0 | 40 | 0.3 |
| `:4` | 3 | 4/76 | 65.0 | 3.0 | 9.0 | 20 | 0.3 |
| `:5` | 3 | 4/76 | 65.0 | 3.0 | 9.0 | 20 | 0.3 |
| `:6` | 3 | 4/76 | 65.0 | 3.0 | 9.0 | 40 | 0.3 |

The melee goal receives interval bounds `[floor(attack_interval/2), floor(attack_interval/2)+10]`, combo chance 0.3 and melee movement modifier 1.3. These bounds are goal inputs; animation and host scheduling determine hits. Tier-3 sword rows `:4`/`:5` have barrage bounds **30–50 ticks**, and axe row `:6` has **50–70 ticks**, each at level **1–1**, count **1**. Other rows have no barrage spell. All shipped single-use spell slots are empty; if supplied by datapack, this role passes level **1–1** and delay `[single_use_spell_delay, +20]`. Quality is parsed but this role never passes it to its melee or barrage goals. Damage combines the row's base attack attribute with equipment and host melee resolution; the profile does not declare final damage per hit.

## Spell slots and equipment

Namespace key: `I:` = `irons_spellbooks:`, `M:` = `minecraft:`, `A:` = `acolyte:`. Every listed spell belongs to Iron's. `—` means an empty slot/list. All defense and utility lists are empty; all attack/mobility lists not explicitly shown are empty. Equipment names identify items, not copied item definitions.

| Suffix | Attack list | Barrage | Single-use | Mobility list | Equipment by slot |
|---|---|---|---|---|---|
| `:0` | — | — | — | — | mainhand `M:golden_sword` |
| `:1` | — | — | — | — | mainhand `M:golden_axe` |
| `:2` | — | — | — | — | mainhand `M:golden_sword`; chest `A:warrior_tier2_chestplate` |
| `:3` | — | — | — | — | mainhand `M:golden_axe`; chest `A:warrior_tier2_chestplate` |
| `:4` | — | `I:flaming_strike` | — | — | mainhand `M:golden_sword`; chest `A:warrior_tier3_chestplate` |
| `:5` | — | `I:throw` | — | — | mainhand `M:golden_sword`; chest `A:warrior_tier3_chestplate` |
| `:6` | — | `I:frost_step` | — | — | mainhand `M:golden_axe`; chest `A:warrior_tier3_chestplate` |

Every shipped entry omits `head`; `DemonEntity` consequently equips one random cosmetic horn item from `acolyte:demon_horns_0` through `acolyte:demon_horns_3`. Chest, legs and feet follow the profile (omitted slots clear); mainhand is applied only when currently empty. Offhand is parsed by the schema but is not applied by the shared equipment population method. Non-null items applied by `ArchetypeUtils` receive drop chance 0.

Recruitment target, emerald cost, contract duration and player mana debit: **N/A**. The confirmation handler accepts `HumanEntity`, not this demon family. Target choice, attack reach and host spell resolution are delegated to the [corresponding entity/AI contract](../entities/demon-warrior.md). Profile selection itself deals no damage and creates no projectile.

## Evidence and limits

Resource authority: `data/acolyte/archetype/demon/warrior.json`, `profiles[0..6]`; these tables are a factual transcription of identifiers and numeric settings, not redistributed JSON. Binary authority: `ArchetypeProfile#fromJson(JsonObject)` PCs 0–917 (defaults/slots), `ArchetypeLoader#rollProfile(String,Random,ServerLevelAccessor,BlockPos)` PCs 0–94 and `#rollWeighted(List,Random)` PCs 0–106; `DemonWarriorEntity#registerArchetypeGoals()V` (PCs 0–205); `DemonEntity#finalizeSpawn(...)` PCs 0–203; `ModUtils#resolveBiomeFolder(...)` PCs 0–135. Exact formulas and delegated boundaries are limited to the publisher artifact identified by the linked evidence. No installed-pack configuration, spell success, equipment rendering, restart behavior, protection behavior, perk integration or runtime balance was tested.
