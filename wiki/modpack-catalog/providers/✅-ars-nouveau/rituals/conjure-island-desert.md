# Conjure Island: Desert

Status: `SOURCE-PINNED 5.13.1 / BIOME-WORLDGEN RITUAL`

- Registry id: `ars_nouveau:ritual_conjure_island_desert`
- Class: `ConjureDesertRitual`
- Base radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Source cost: `50` per provider Source request
- Source request cadence: every `5` successful placements
- Placement budget: at most one successful block placement per ritual tick
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

The ritual inherits `ConjureBiomeRitual` and defaults to Desert biome output.

### Desert mode

- top island layer: Sand;
- deeper generated layers: Sandstone.

### Badlands modifier

If a terracotta-tag item is consumed, the provider switches the biome to Badlands and creates a depth-dependent material profile:

- depth 1: Red Sand;
- depth 2: Orange Terracotta;
- depth 3–4: Red Terracotta;
- deeper layer: Terracotta.

Only one terracotta variant selector is accepted. Source Gem-tag inputs remain radius modifiers.

Every successful placed block also invokes the provider biome-change helper. The shared helper requests 50 Source every five successful placements.

## Authority / Black Arcana boundary

Terrain generation, biome conversion, Source accounting and persistent tracker state are Ars Nouveau authority. Black Arcana must not duplicate blocks or biome changes.

Independent Black Arcana terrain/biome mechanics remain subject to `WorldEffectPolicy` and bounded scheduling.

## QA

Source behavior is pinned to 5.13.1. As with the Plains variant, direct protection/claim preflight is not explicit in this helper path and therefore requires runtime validation.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`ConjureDesertRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/ConjureDesertRitual.java) no Ars 5.13.1. Executor herdado [`ConjureBiomeRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ConjureBiomeRitual.java).
- **Contrato herdado:** `ConjureDesertRitual extends ConjureBiomeRitual`. Em `onStart`, `radius=7+sum(SourceGemTag.count)` e cria `ManhattenTracker(brazier.below(3),radius,2,radius)`. `tick` consulta no máximo `radius` próximos candidatos por iteração e retorna depois de **um** placement bem-sucedido; testa distância euclidiana ao brazier e `canBeReplaced`.
- **Bioma e profundidade:** padrão DESERT, coloca SAND somente no nível do brazier Y−1, SANDSTONE nas demais camadas elegíveis. Com qualquer `ItemTags.TERRACOTTA`, muda bioma para BADLANDS e distribui RED_SAND depth1, ORANGE_TERRACOTTA depth2, RED_TERRACOTTA depths3–4, TERRACOTTA demais.
- **Source:** `ConjureBiomeRitual` chama `RitualUtil.changeBiome` a cada placement, acumula `blocksPlaced` e, a cada `>=5`, reseta contador e marca `setNeedsSource(true)`; custo declarado `getSourceCost=50`, **não** débito fixo por tick. Pai serializa `tracker` e `radius`; estado dos blocos/bioma e Source efetivo precisam de teste de restart.
- **Segurança:** `setState` realiza `world.setBlock(pos,state,2)` e o helper exibido não possui claim preflight explícito; é lacuna de admissão a auditar, não permissão para bypass em magia Black Arcana.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.
