# Forestation

Status: `SOURCE-PINNED 5.13.1 / FEATURE-PLACEMENT RITUAL`

- Registry id: `ars_nouveau:ritual_forestation`
- Class: `ForestationRitual`
- Base check radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native feature modes

Forestation inherits Ars Nouveau's `FeaturePlacementRitual`, which constructs a shuffled bounded target-position list for each feature and processes features sequentially, returning after each successful placement.

### Default forest

- Oak/Birch random tree feature;
- provider bonemeal feature.

### Taiga modifier

Exactly one Brown Mushroom selects the taiga family, including:

- Spruce trees;
- conversion of dirt/grass to Podzol;
- fern/large fern placement;
- Brown Mushroom placement;
- grass placement;
- rare Sweet Berry Bush placement with randomized vanilla age.

### Jungle modifier

Exactly one Glow Berries item selects the jungle family, including:

- big Jungle trees;
- normal Jungle trees;
- cocoa placement;
- grass, melon and fern placement.

Brown Mushroom and Glow Berries are mutually exclusive variant selectors. Source Gem-tag items remain separately accepted as radius augments.

## Bounded placement model

`FeaturePlacementRitual` starts at radius 7, builds positions inside the radius, shuffles them, checks minimum separation per feature and advances feature-by-feature. It returns after a successful `onPlace`, rather than executing every candidate in one tick.

## Authority / Black Arcana boundary

Terrain vegetation conversion, feature probabilities, placement order and radius modifiers remain Ars Nouveau authority. Black Arcana must not replay generated trees/plants or treat each feature as an independent ritual completion.

Independent Black Arcana environmental creation remains bounded and subject to `WorldEffectPolicy` where it mutates the world.

## QA

Source structure is pinned to 5.13.1. The base helper does not itself prove every protection/claim integration for every `IPlaceableFeature`; representative full-pack world-safety QA remains required.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`ForestationRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/ForestationRitual.java), `com.hollingsworth.arsnouveau.common.ritual.ForestationRitual`, Ars 5.13.1. [`FeaturePlacementRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/FeaturePlacementRitual.java) é executor auxiliar.
- **Modo baseline:** `RandomTreeFeature([OAK,BIRCH],5,0.8)` e `BonemealFeature(6,0.8)`; `FeaturePlacementRitual` monta alvos em `checkRadius=7`, embaralha, usa `featureIndex/positionIndex` e espaçamento mínimo para feature; Source Gem-tag aumenta raio pela contagem consumida.
- **Taiga:** 1 Brown Mushroom permite `RandomTreeFeature(SPRUCE,8,0.8)`, `ConvertBlockFeature` Dirt/Grass→Podzol (0.8), Fern/Large Fern (0.1, probabilidade adicional 0.3 para Large Fern), Brown Mushroom (0.1), Grass (0.1), Sweet Berry Bush (0.01, age sorteada 0..3). **Jungle:** Glow Berries ativa Big Jungle tree (12,0.3), Jungle sapling (6,0.95), Cocoa (6,0.4), Grass (0.1), Melon (0.01) e Fern (0.1). Seletoras Brown Mushroom/Glow Berries são mutuamente exclusivas em `canConsumeItem`.
- **Persistência/risco:** o pai serializa `featureIndex`, `positionIndex`, `checkRadius` e executa no máximo uma feature com `onPlace` **bem-sucedido** por `tick()` antes de retornar. Não é uma garantia de uma única **tentativa** por tick, pois existe laço que avança por posições. Crescimento/estrutura, claims e compatibilidade addon exigem teste físico; perks RPG não podem aumentar raio por regravar NBT do ritual.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.
