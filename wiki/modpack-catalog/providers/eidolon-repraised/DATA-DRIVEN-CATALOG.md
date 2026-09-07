# Eidolon: Repraised 0.5.0.2 — Data-Driven Catalog

Status: `OFFICIAL DATAGEN INVENTORIED — 18 CHANTS + 4 CHANT CONVERSIONS + 24 RITUAL RECIPES / COMMAND-CHANT SURFACE PRESENT BUT NO OFFICIAL ENTRY GENERATED / RUNTIME QA PENDING`

Canonical source: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## 1. Official chant recipes — 18

`EidChantProvider` generates exactly 18 `eidolon_repraised:chant` recipes. The committed generated resources confirm the recipe representation (`id` + ordered `signs`).

1. `dark_prayer`
2. `dark_animal_sacrifice`
3. `dark_touch`
4. `darklight_chant`
5. `dark_villager_sacrifice`
6. `zombify_villager`
7. `enthrall_spell`
8. `light_prayer`
9. `light_chant`
10. `holy_touch`
11. `lay_on_hands`
12. `cure_zombie`
13. `smite_chant`
14. `sunder_armor`
15. `reinforce_armor`
16. `frost_touch`
17. `fire_chant`
18. `create_water`

### Registry-versus-recipe distinction

The Java spell registry contains 20 technical spell entries, but only 18 are emitted as normal chant recipes. `undead_lure` and `basic_incense` are absent from `EidChantProvider`. Therefore:

- `undead_lure` is registered in Java but has no provider-generated normal chant recipe and its exact 0.5.0.2 `cast()` is empty;
- `basic_incense` is explicitly a dummy `PrayerSpell` for the incense subsystem and has no fixed normal chant recipe.

Neither should be represented as a normal survival chant without runtime/data evidence from the actual pack.

## 2. Chant conversion recipes — 4

`EidChantConversionProvider` generates exactly four conversions consumed by Dark Touch / Holy Touch:

| Recipe | Alignment | Input | Output | Minimum devotion |
|---|---|---|---|---:|
| `convert_inlay_holy` | Light | Gold Inlay | Holy Symbol | 10 |
| `convert_inlay_unholy` | Dark | Pewter Inlay | Unholy Symbol | 10 |
| `convert_top_hat` | neutral/dummy deity | Black Wool | Top Hat | 0 |
| `convert_disc` | neutral/dummy deity | `neoforge:music_discs` | Parousia Disc | 0 |

The conversion recipe itself does not hardcode a mana value in this provider generator. Dark/Holy Touch therefore falls back to the spell cost unless a datapack-provided conversion explicitly supplies a non-negative override through the recipe schema/runtime object.

Black Arcana must never precompute the conversion output or price independently of Eidolon's RecipeManager.

## 3. Official ritual recipes — 24

`EidRitualProvider` emits 24 committed ritual JSONs under `data/eidolon_repraised/recipe/rituals/`:

- 11 summon ritual recipes;
- 2 brazier crafting rituals;
- 10 generic provider-specific rituals;
- 1 structure-location ritual.

This is distinct from `RitualRegistry`, which contains 10 hardcoded generic ritual prototypes. Recipe subclasses can construct additional runtime Ritual instances dynamically. Therefore the recipe set is authoritative for gameplay availability; commented hardcoded constants do not imply the equivalent recipe content is inactive.

### 3.1 Summon rituals — 11

`SummonRitualRecipe.getRitual()` constructs a new `SummonRitual` directly from the recipe entity id. Summoned mobs are created server-side with `MobSpawnType.MOB_SUMMONED`; mobs receive finalize-spawn handling and `setCanPickUpLoot(true)`. They are not automatically classified as player-owned/tamed by this ritual class.

| Runtime recipe id | Count | Reagent | Pedestal requirements | Focus requirements |
|---|---:|---|---|---|
| `summon_zombie` | 1 | Charcoal | Soul Shard + Rotten Flesh | Rotten Flesh |
| `summon_skeleton` | 1 | Charcoal | Soul Shard + Bone | Bone |
| `summon_phantom` | 1 | Charcoal | Soul Shard + Phantom Membrane | Phantom Membrane |
| `summon_creeper` | 1 | Charcoal | Soul Shard + Gunpowder | Gunpowder |
| `summon_wither_skeleton` | 1 | Charcoal | Soul Shard + Bone | Soul Sand |
| `summon_husk` | 3 | Charcoal | Soul Shard + Rotten Flesh | sand-tag ingredient |
| `summon_drowned` | 3 | Charcoal | Soul Shard + Rotten Flesh | prismarine-gem-tag ingredient |
| `summon_stray` | 1 | Charcoal | Soul Shard + Bone | String |
| `summon_wraith` | 1 | Charcoal | Soul Shard + Tattered Cloth | Tattered Cloth |
| `summon_slimy_slug` | 3 | Pumpkin Seeds | Soul Shard + Slime Ball | none |
| `summon_raven` | 3 | Beetroot Seeds | Soul Shard + Feather | none |

The source generator method's human-facing variable names (`summon_slugs`, `summon_ravens`) do not determine the runtime recipe id; `SummonRitualRecipe.getId()` derives the id from the entity registry path, producing the committed files `summon_slimy_slug` and `summon_raven`.

### 3.2 Brazier crafting rituals — 2

| Runtime recipe id | Reagent | Pedestal requirements | Focus | Health requirement | Result |
|---|---|---|---|---:|---|
| `brazier_craft_sapping_sword` | Iron Sword | Shadow Gem; Soul Shard ×2; Nether Wart ×2; Ghast Tear | Potion of Harming | 20 | Sapping Sword |
| `brazier_craft_sanguine_amulet` | Basic Amulet | Diamond-gem tag; Redstone Dust ×4; Lesser Soul Gem | Potion of Harming | 40 | Sanguine Amulet |

`ItemRitualRecipe` constructs a `CraftingRitual`/`SanguineRitual` and can preserve reagent components when configured. These are provider-owned health-cost crafting transactions and must not be treated as ordinary crafting recipes by Black Arcana progression without semantic classification.

### 3.3 Generic rituals — 10

| Ritual | Reagent | Pedestal requirements | Required invariant/focus |
|---|---|---|---|
| `crystal` | Bone Meal | Redstone Dust ×2 | none |
| `deceit` | Emerald-gem tag | Emerald-gem tag; Fermented Spider Eye; Mushroom tag; Soul Shard ×2 | none |
| `allure` | Rose Bush | Golden Apple; Red Dye ×2; Soul Shard ×2 | none |
| `repelling` | Nautilus Shell | Iron-ingot tag; Leather; Quartz-gem tag; Soul Shard ×2 | none |
| `daylight` | Sunflower | Charcoal; Wheat Seeds; Soul Shard ×2 | none |
| `moonlight` | Black-dye tag | Snowball; Spider Eye; Soul Shard ×2 | none |
| `purify` | Glistering Melon Slice | Enchanted Ash ×2; Potion of Healing; Soul Shard ×2 | none |
| `absorption` | Death Essence | Tattered Cloth ×2; Bone; Soul Shard ×2 | Summoning Staff present |
| `recharging_soulfire` | Lesser Soul Gem | Blaze Powder ×2; Redstone Dust | Soulfire Wand present |
| `recharging_chill` | Lesser Soul Gem | Snowball ×2; Redstone Dust | Bonechill Wand present |

The effect semantics of these rituals are documented in `RITUAL-CATALOG.md`.

### 3.4 Catacomb locator — 1

The generated runtime id is `eidolon_repraised:ritual_locate_catacombs`, derived by `LocationRitualRecipe.getId()` from the Catacombs structure tag. Requirements generated by 0.5.0.2:

- reagent: Map;
- pedestal: Compass + Magic Ink + Raven Feather;
- no focus items;
- health requirement: 0.

`LocationRitualRecipe` constructs a provider `LocationRitual` for the structure tag. This is a native structure-divination capability.

## 4. Command chant extension surface

Eidolon 0.5.0.2 registers `CommandChantRecipe`. A datapack command chant contains:

- an id;
- ordered Signs;
- a list of command strings;
- a mana cost.

It materializes an `ExecCommandSpell`. Server-side, if command blocks are enabled, that spell executes each non-empty configured command using the caster's command source with **permission level 2** and suppressed output; when a player is absent, Eidolon can use its fake player.

No official 0.5.0.2 command chant is emitted by `EidChantProvider`/the official datagen inspected here. The capability nevertheless exists as an extension surface for datapacks.

### Security/integration rule

Black Arcana must treat command chants as an untrusted/privileged datapack surface:

- never synthesize commands from player-controlled strings;
- never mirror or re-execute the command list;
- never grant additional permission;
- never use a command chant as proof of a safe generic spell effect without inspecting the loaded recipe;
- fail closed when a perk/integration cannot identify or whitelist the command-chant semantics.

## 5. Exact artifact boundary

The source repository keeps ordinary authored recipes under `src/main/resources` and provider-generated chant/ritual recipes under `src/generated/resources`. The audited generated JSONs are committed at the exact 0.5.0.2 source pin. Runtime packaging of the installed JAR still requires dedicated artifact/runtime QA before claiming byte-for-byte equality with these source resources.