# Human Archer archetype profiles

Status: `BINARY_VERIFIED` for the exact publisher Acolyte 1.0.3 artifact; assembled-pack behavior, installed-JAR hash equality and physical QA are `NOT_VERIFIED` / `NOT_TESTED`. This is an Acolyte loadout/configuration surface and adds **0 Acolyte-owned spells**. See [release evidence](../BINARY-CONTRACTS-1.0.3.md) and the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).

`data/acolyte/archetype/human/archer.json` supplies the `human/archer` key returned by `HumanArcherEntity#getArchetypeName()Ljava/lang/String;` (PCs 0–2). It contains 7 entries, in the order below, with total weight **76**. Entries omit explicit IDs, so the loader assigns `human/archer:0` through `human/archer:6`. These are profile IDs, not entity registry IDs.

## Selection and biome variants

All entries omit `biomes`, `name` and `skin`; every shipped entry is eligible in every biome. Each entry has probability `weight/76` in this unchanged publisher pool. The tier totals are 40/76 for tier 1, 24/76 for tier 2 and 12/76 for tier 3. Reloaded datapacks can change that denominator and eligibility. The [loadout pipeline](../systems/archetype-loadout-pipeline.md) documents parsing, filtering, ordinal IDs, persistence and equipment application.

All seven biome folders use this same loadout pool: **desert, jungle, plains, savanna, snowy, swamp and taiga**. Skin variant is chosen independently as 0, 1 or 2; the packaged paths are `acolyte:textures/entity/generic_skin/<folder>/human<variant>.png`. Folder resolution checks biome path text in order: `taiga`, `desert`, `jungle`, `savanna`, `snowy` or `frozen`, `swamp`, then `badlands`→`desert`; everything else resolves to `plains`. Thus these 21 skin combinations do not establish 21 different spell pools.

## Stats and timing

HP uses Minecraft health points (2 HP = 1 heart); armor and attack are base attribute values before equipment and host combat resolution. Intervals use game ticks, with 20 ticks = 1 second at the nominal tick rate. `quality` is a host goal parameter, not a spell level. All entries default to XP reward 15, barrage count 1 and first-single-use delay 30 ticks; none overrides movement speed 0.25 or the archer base follow range of 32 blocks. `ArchetypeUtils.applyProfileStats` resets to captured base values and applies only explicit `statOverrides`; an absent follow-range override does not replace the archer base with the 24-block value used by other roles.

| Profile suffix | Tier | Weight | HP | Base attack | Base armor | `attack_interval` | `quality` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `:0` | 1 | 20/76 | 30.0 | 8.0 | 0.0 | 10 | 0.3 |
| `:1` | 1 | 20/76 | 30.0 | 8.0 | 0.0 | 10 | 0.3 |
| `:2` | 2 | 12/76 | 50.0 | 10.0 | 4.0 | 7 | 0.3 |
| `:3` | 2 | 12/76 | 50.0 | 10.0 | 4.0 | 7 | 0.3 |
| `:4` | 3 | 4/76 | 80.0 | 12.0 | 6.0 | 5 | 0.4 |
| `:5` | 3 | 4/76 | 80.0 | 12.0 | 6.0 | 5 | 0.4 |
| `:6` | 3 | 4/76 | 80.0 | 12.0 | 6.0 | 5 | 0.4 |

`UniversalRangedGoal` receives the row's interval, movement modifier 1.0 and a **15-block** attack radius. Each ranged attack constructs one vanilla arrow; base-arrow damage is `profile.attack_damage/2`, while final damage depends on vanilla projectile velocity/collision. The exact projectile contract is on the linked role card. Tier-3 barrage slots pass level **1–1**, interval **80–100 ticks**, count **1**. The `spells_quality` value is parsed but is not passed to that barrage goal. All shipped single-use slots are empty; a datapack-supplied single-use spell receives level **1–1** and default delay **30–50 ticks**. Spell cast time, mana, damage and projectile behavior are delegated to Iron's.

## Spell slots and equipment

Namespace key: `I:` = `irons_spellbooks:`, `M:` = `minecraft:`, `A:` = `acolyte:`. Every listed spell belongs to Iron's. `—` means an empty slot/list. All defense and utility lists are empty; all attack/mobility lists not explicitly shown are empty. Equipment names identify items, not copied item definitions.

| Suffix | Attack list | Barrage | Single-use | Mobility list | Equipment by slot |
|---|---|---|---|---|---|
| `:0` | — | — | — | — | mainhand `M:bow`; chest `A:archer_tier1_chestplate` |
| `:1` | — | — | — | — | mainhand `M:crossbow`; chest `A:archer_tier1_chestplate` |
| `:2` | — | — | — | — | mainhand `M:bow`; head `A:archer_tier2_helmet`; chest `A:archer_tier2_chestplate` |
| `:3` | — | — | — | — | mainhand `M:crossbow`; head `A:archer_tier2_helmet`; chest `A:archer_tier2_chestplate` |
| `:4` | — | `I:fire_arrow` | — | — | mainhand `M:bow`; head `A:archer_tier3_helmet`; chest `A:archer_tier3_chestplate` |
| `:5` | — | `I:magic_arrow` | — | — | mainhand `M:bow`; head `A:archer_tier3_helmet`; chest `A:archer_tier3_chestplate` |
| `:6` | — | `I:poison_arrow` | — | — | mainhand `M:crossbow`; head `A:archer_tier3_helmet`; chest `A:archer_tier3_chestplate` |

Head, chest, legs and feet follow the profile (omitted slots clear); mainhand is applied only when currently empty. Offhand is parsed by the schema but is not applied by the shared equipment population method. Non-null items applied by `ArchetypeUtils` receive drop chance 0.

Human tier 1/2/3 recruitment costs **5/7/9 emeralds** for **24,000/48,000/72,000 game ticks** (20/40/60 nominal minutes); recruitment adds no mana debit. See the [recruitment contract](../systems/recruitment-contract.md). Target choice, attack reach and host spell resolution are delegated to the [corresponding entity/AI contract](../entities/human-archer.md). Profile selection itself deals no damage and creates no projectile.

## Evidence and limits

Resource authority: `data/acolyte/archetype/human/archer.json`, `profiles[0..6]`; these tables are a factual transcription of identifiers and numeric settings, not redistributed JSON. Binary authority: `ArchetypeProfile#fromJson(JsonObject)` PCs 0–917 (defaults/slots), `ArchetypeLoader#rollProfile(String,Random,ServerLevelAccessor,BlockPos)` PCs 0–94 and `#rollWeighted(List,Random)` PCs 0–106; `HumanArcherEntity#registerArchetypeGoals()V` (PCs 0–143); `HumanEntity#finalizeSpawn(...)` PCs 0–203; `ModUtils#resolveBiomeFolder(...)` PCs 0–135. Exact formulas and delegated boundaries are limited to the publisher artifact identified by the linked evidence. No installed-pack configuration, spell success, equipment rendering, restart behavior, protection behavior, perk integration or runtime balance was tested.
