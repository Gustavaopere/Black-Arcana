# Human Mage archetype profiles

Status: `BINARY_VERIFIED` for the exact publisher Acolyte 1.0.3 artifact; assembled-pack behavior, installed-JAR hash equality and physical QA are `NOT_VERIFIED` / `NOT_TESTED`. This is an Acolyte loadout/configuration surface and adds **0 Acolyte-owned spells**. See [release evidence](../BINARY-CONTRACTS-1.0.3.md) and the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).

`data/acolyte/archetype/human/mage.json` supplies the `human/mage` key returned by `HumanMageEntity#getArchetypeName()Ljava/lang/String;` (PCs 0–2). It contains 11 entries, in the order below, with total weight **76**. Entries omit explicit IDs, so the loader assigns `human/mage:0` through `human/mage:10`. These are profile IDs, not entity registry IDs.

## Selection and biome variants

All entries omit `biomes`, `name` and `skin`; every shipped entry is eligible in every biome. Each entry has probability `weight/76` in this unchanged publisher pool. The tier totals are 40/76 for tier 1, 24/76 for tier 2 and 12/76 for tier 3. Reloaded datapacks can change that denominator and eligibility. The [loadout pipeline](../systems/archetype-loadout-pipeline.md) documents parsing, filtering, ordinal IDs, persistence and equipment application.

All seven biome folders use this same loadout pool: **desert, jungle, plains, savanna, snowy, swamp and taiga**. Skin variant is chosen independently as 0, 1 or 2; the packaged paths are `acolyte:textures/entity/generic_skin/<folder>/human<variant>.png`. Folder resolution checks biome path text in order: `taiga`, `desert`, `jungle`, `savanna`, `snowy` or `frozen`, `swamp`, then `badlands`→`desert`; everything else resolves to `plains`. Thus these 21 skin combinations do not establish 21 different spell pools.

## Stats and timing

HP uses Minecraft health points (2 HP = 1 heart); armor and attack are base attribute values before equipment and host combat resolution. Intervals use game ticks, with 20 ticks = 1 second at the nominal tick rate. `quality` is a host goal parameter, not a spell level. All entries default to XP reward 15, barrage count 1 and first-single-use delay 30 ticks; none overrides movement speed 0.25 or follow range 24 blocks.

| Profile suffix | Tier | Weight | HP | Base attack | Base armor | `attack_interval` | `quality` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `:0` | 1 | 10/76 | 30.0 | 0.0 | 0.0 | 25 | 0.4 |
| `:1` | 1 | 10/76 | 30.0 | 0.0 | 0.0 | 25 | 0.4 |
| `:2` | 1 | 10/76 | 30.0 | 0.0 | 0.0 | 25 | 0.4 |
| `:3` | 1 | 10/76 | 30.0 | 0.0 | 0.0 | 25 | 0.4 |
| `:4` | 2 | 6/76 | 45.0 | 0.0 | 4.0 | 25 | 0.6 |
| `:5` | 2 | 6/76 | 45.0 | 0.0 | 4.0 | 25 | 0.6 |
| `:6` | 2 | 6/76 | 45.0 | 0.0 | 4.0 | 25 | 0.6 |
| `:7` | 2 | 6/76 | 45.0 | 0.0 | 4.0 | 50 | 0.6 |
| `:8` | 3 | 4/76 | 60.0 | 0.0 | 5.0 | 25 | 0.7 |
| `:9` | 3 | 4/76 | 60.0 | 0.0 | 0.0 | 25 | 0.7 |
| `:10` | 3 | 4/76 | 60.0 | 0.0 | 5.0 | 25 | 0.7 |

The main `WizardAttackGoal` receives each row's interval as its lower interval and that value +20 as its upper interval. It receives spell-quality bounds `[quality, quality+0.1]`, so tier 1/2/3 main-cast quality ranges are `[0.4,0.5]`, `[0.6,0.7]`, `[0.7,0.8]`. Conversion from quality to the selected spell's concrete level is delegated to Iron's `WizardAttackGoal`; this Acolyte binary does not provide a fixed numeric level for those main casts. Barrage and single-use calls supply level bounds **1–1**. Barrage interval defaults to **80–100 ticks**, count **1**; first single-use delay defaults to **30–50 ticks**. Host casting time, cooldown, range, projectile behavior, mana and spell damage remain host-defined; the interval bounds are goal inputs, not guaranteed cast-completion cadence.

## Spell slots and equipment

Namespace key: `I:` = `irons_spellbooks:`, `M:` = `minecraft:`, `A:` = `acolyte:`. Every listed spell belongs to Iron's. `—` means an empty slot/list. All defense and utility lists are empty; all attack/mobility lists not explicitly shown are empty. Equipment names identify items, not copied item definitions.

| Suffix | Attack list | Barrage | Single-use | Mobility list | Equipment by slot |
|---|---|---|---|---|---|
| `:0` | `I:magic_missile` | — | — | — | mainhand `I:copper_spell_book`; head `A:wizard_tier1_helmet` |
| `:1` | `I:firebolt` | — | — | — | mainhand `I:copper_spell_book`; head `A:wizard_tier1_helmet` |
| `:2` | `I:icicle` | — | — | — | mainhand `I:copper_spell_book`; head `A:wizard_tier1_helmet` |
| `:3` | `I:firecracker` | — | — | — | mainhand `I:copper_spell_book`; head `A:wizard_tier1_helmet` |
| `:4` | `I:blood_needles` | `I:ray_of_siphoning` | — | — | mainhand `I:iron_spell_book`; head `A:wizard_tier2_helmet`; chest `A:wizard_tier2_chestplate` |
| `:5` | `I:ball_lightning` | `I:chain_lightning` | — | — | mainhand `I:iron_spell_book`; head `A:wizard_tier2_helmet`; chest `A:wizard_tier2_chestplate` |
| `:6` | `I:guiding_bolt` | `I:wisp` | — | — | mainhand `I:iron_spell_book`; head `A:wizard_tier2_helmet`; chest `A:wizard_tier2_chestplate` |
| `:7` | `I:poison_breath` | — | `I:root` | — | mainhand `I:iron_spell_book`; head `A:wizard_tier2_helmet`; chest `A:wizard_tier2_chestplate` |
| `:8` | `I:wither_skull` | — | `I:summon_swords` | `I:teleport` | mainhand `I:gold_spell_book`; head `A:wizard_tier3_helmet`; chest `A:wizard_tier3_chestplate` |
| `:9` | `I:guiding_bolt` | `I:arrow_volley` | `I:summon_vex` | — | mainhand `I:gold_spell_book`; head `A:wizard_tier3_helmet`; chest `A:wizard_tier3_chestplate` |
| `:10` | `I:acupuncture` | `I:blood_slash` | `I:raise_dead` | — | mainhand `I:gold_spell_book`; head `A:wizard_tier3_helmet`; chest `A:wizard_tier3_chestplate` |

Head, chest, legs and feet follow the profile (omitted slots clear); mainhand is applied only when currently empty. Offhand is parsed by the schema but is not applied by the shared equipment population method. Non-null items applied by `ArchetypeUtils` receive drop chance 0.

Human tier 1/2/3 recruitment costs **5/7/9 emeralds** for **24,000/48,000/72,000 game ticks** (20/40/60 nominal minutes); recruitment adds no mana debit. See the [recruitment contract](../systems/recruitment-contract.md). Target choice, attack reach and host spell resolution are delegated to the [corresponding entity/AI contract](../entities/human-mage.md). Profile selection itself deals no damage and creates no projectile.

## Evidence and limits

Resource authority: `data/acolyte/archetype/human/mage.json`, `profiles[0..10]`; these tables are a factual transcription of identifiers and numeric settings, not redistributed JSON. Binary authority: `ArchetypeProfile#fromJson(JsonObject)` PCs 0–917 (defaults/slots), `ArchetypeLoader#rollProfile(String,Random,ServerLevelAccessor,BlockPos)` PCs 0–94 and `#rollWeighted(List,Random)` PCs 0–106; `HumanMageEntity#registerArchetypeGoals()V` (PCs 0–196); `HumanEntity#finalizeSpawn(...)` PCs 0–203; `ModUtils#resolveBiomeFolder(...)` PCs 0–135. Exact formulas and delegated boundaries are limited to the publisher artifact identified by the linked evidence. No installed-pack configuration, spell success, equipment rendering, restart behavior, protection behavior, perk integration or runtime balance was tested.
