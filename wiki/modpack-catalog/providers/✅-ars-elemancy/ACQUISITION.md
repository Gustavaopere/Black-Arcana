# Ars Elemancy 1.18.3 — acquisition

Status: `SOURCE-PINNED DEFAULT DATA / EFFECTIVE DATAPACK QA PENDING`

## Essences — Imbuement Chamber

All seven essence recipes cost **3000 Source**.

| Result | Reagent | Pedestals |
|---|---|---|
| Tempest Essence | Ars Manipulation Essence | Water Essence + Air Essence |
| Cinder Essence | Ars Manipulation Essence | Fire Essence + Air Essence |
| Silt Essence | Ars Manipulation Essence | Earth Essence + Air Essence |
| Mire Essence | Ars Manipulation Essence | Water Essence + Earth Essence |
| Vapor Essence | Ars Manipulation Essence | Water Essence + Fire Essence |
| Lava Essence | Ars Manipulation Essence | Fire Essence + Earth Essence |
| Elemancer Essence | Ars Source Gem | Air + Fire + Water + Earth Essences |

A commented-out Mark of Mastery recipe is not active and is not cataloged as obtainable from Ars Elemancy.

## Foci — Enchanting Apparatus

Each dual focus uses its fused essence as reagent and the two corresponding Ars Elemental foci as pedestals. Elemancer Focus uses Elemancer Essence plus the four base elemental foci.

Tracked resource JSONs specify **`sourceCost: 0`** for these focus recipes.

## Bangles — Enchanting Apparatus

Each dual bangle combines the two corresponding Ars Elemental bangles. The generated recipe family:

- uses one base bangle as reagent;
- uses the other base bangle as a pedestal;
- adds `ars_elemental:mark_of_mastery`;
- adds 2 matching fused essences;
- costs **7000 Source**;
- preserves reagent NBT.

Elemancer Bangle has three alternative pair routes:

1. Tempest + Lava;
2. Cinder + Mire;
3. Silt + Vapor.

Each uses Mark of Mastery, 2 Elemancer Essences and 7000 Source.

## Armor — Sauce ElementalArmorRecipe

Tracked armor recipe resources use `type: sauce:armor_upgrade` and cost **7000 Source**.

For a dual identity, every armor piece combines the matching piece from each of the two base Ars Elemental sets, plus:

- Mark of Mastery;
- 2 matching fused essences;
- the alternate base piece as pedestal(s);
- NBT preservation of the reagent path.

The source tree contains these recipe families for light, medium and heavy output names. The current Java `AEApparatusProvider` explicitly constructs the medium families, while tracked `src/main/resources` also contains light/heavy JSON recipes. Because `src/main/resources` is packaged independently of datagen, the resource surface is recorded as runtime data while the datagen/resource mismatch remains a maintenance finding.

Elemancer armor supports the three fused-pair routes used by the Elemancer Bangle: Tempest+Lava, Cinder+Mire, Silt+Vapor.

Effective server datapacks can replace these defaults; runtime pack QA remains required.