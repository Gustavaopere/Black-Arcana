# Fantasy Armor 1.2.4-1.21.1 — exact source magic surface

## Evidence

Physical provider:

- `fantasy_armor-neoforge-1.2.4-1.21.1.jar`;
- mod id `fantasy_armor`;
- physical SHA-1 `2b103680ca80a1d617dcae74630c4df8e93d3c55`.

Sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Exact official source pin:

`kend1e/FANTASY-ARMOR@0d58f07346fd7fffc08fac907aa908e5e4295667`

The pin is the 2026-03-31 release commit that changes the NeoForge 1.21.1 `mod_version` to `1.2.4-1.21.1`.

## Structural inventory

Exact NeoForge Java source cardinality: **19 classes**.

Relevant families:

| Surface | Exact-source role | Semantic action count |
|---|---|---:|
| `FantasyArmor` | registers configs/items/armor/creative tab | 0 |
| `FAItems` | normal item registry; Moon Crystal | 0 |
| `FAArmorItems` | creates four armor pieces for every armor set | 0 |
| `FAArmorSet(s)` | 29 equipment-set identities/factories | 0 |
| `FAArmorAttributes*` | equipment stat configuration | 0 |
| `FAArmorEffectsConfig` | configured MobEffect list per full set | 0 |
| `FAArmorEffectHandler` | refreshes effects while matching full set is equipped | 0 |
| client model/render classes | presentation | 0 |

## Registry/search closure

Exact-source searches at the release pin establish:

- `spell`: no Java implementation result;
- `ritual`: no source result;
- `cast`: no source result;
- active item `use(`: no source result;
- `InteractionResult`: no source result;
- `KeyMapping`: no source result.

The only source registration families are item/armor/creative-tab/config surfaces.

A localization hit containing spell-like prose does not establish a spell registry and is not counted.

## Armor content

Exact provider roster: **29 armor sets**.

Armor item cardinality:

`29 sets × 4 pieces = 116 armor pieces`.

Additional provider item:

- `fantasy_armor:moon_crystal`.

No active-use behavior is defined for Moon Crystal in the exact item registration; it is a normal item in the source surface.

## Default effect surface

All 29 armor sets have default full-set effect entries in `FAArmorEffectsConfig`.

Distinct default vanilla MobEffect identities used:

1. `minecraft:jump_boost`;
2. `minecraft:water_breathing`;
3. `minecraft:night_vision`;
4. `minecraft:fire_resistance`;
5. `minecraft:regeneration`;
6. `minecraft:haste`;
7. `minecraft:luck`;
8. `minecraft:strength`;
9. `minecraft:resistance`.

The handler applies/refreshes those effects while the full matching set is equipped.

They are **Minecraft-owned effect identities**, not Fantasy Armor spell/action registrations.

## Deduplication rule

Do not convert any of these into Black Arcana spell identities:

- armor-set names;
- armor pieces;
- Moon Crystal;
- vanilla effect IDs;
- armor attribute modifiers;
- passive full-set refresh behavior;
- lore prose suggesting supernatural power.

A future active action would require a new exact provider release audit before counting.

## Semantic result

- spells: **0**;
- rites/rituals: **0**;
- active equivalent magic actions: **0**;
- passive gear/effect content: present and cataloged.

Strict semantic delta: **+0**.

Status: **✅ source-pinned zero-semantic gear-magic closure**.

## Clean-room boundary

Only registry identities, cardinalities, configuration roles and high-level observed behavior are recorded.

No implementation body, model, texture or proprietary asset is reused by Black Arcana.
