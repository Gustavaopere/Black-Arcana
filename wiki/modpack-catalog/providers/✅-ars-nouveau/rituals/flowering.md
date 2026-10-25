# Flowering

Status: `SOURCE-PINNED 5.13.1 / FEATURE-PLACEMENT RITUAL`

- Registry id: `ars_nouveau:ritual_flowering`
- Class: `FloweringRitual`
- Base check radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native modes

Flowering inherits `FeaturePlacementRitual`, using its bounded shuffled-position/feature-by-feature placement model.

### Default mode

It registers:

- a randomized flower-placement feature drawn from 16 vanilla flower blocks;
- a bonemeal feature.

### Desert modifier

If a sand-tag item has been consumed, it switches to:

- sparse Cactus placement;
- Dead Bush placement.

Only one sand variant selector is accepted. Source Gems remain separately accepted to enlarge the feature radius.

## Authority / Black Arcana boundary

Feature selection, probabilities, radius and world placement remain Ars Nouveau authority. Black Arcana must not replay flowers/cactus/bonemeal operations or award progression per placed block.

Independent Black Arcana environmental mutation remains bounded and subject to project world-safety policy.

## QA

Source behavior is pinned to 5.13.1. Protection/claim compatibility for every feature implementation remains full-pack runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`FloweringRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/FloweringRitual.java), `com.hollingsworth.arsnouveau.common.ritual.FloweringRitual`, Ars 5.13.1. [`FeaturePlacementRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/FeaturePlacementRitual.java) é executor auxiliar.
- **Herança:** `FloweringRitual extends FeaturePlacementRitual` com `checkRadius=7`; `onStart` do pai soma `ItemTagProvider.SOURCE_GEM_TAG` conforme `ItemStack.getCount()`, monta `targetPositions` em raio geométrico, embaralha e processa features sequencialmente. O pai conclui após esgotar cada lista e **retorna após um sucesso** de `onPlace` em seu tick; tentativas falhadas podem ser percorridas no mesmo tick.
- **Features por modo:** sem sand-tag: `PlaceBlockFeature(1.5,0.8,randomFlower16)` e `BonemealFeature(5,0.8)`. Com `ItemTags.SAND`: `PlaceBlockFeature(3,0.04,CACTUS)` e `PlaceBlockFeature(1.5,0.1,DEAD_BUSH)`. `canConsumeItem` aceita no máximo um seletor sand enquanto não usado, além de Source Gems.
- **Persistência/QA:** pai grava `featureIndex`, `positionIndex`, `checkRadius` e reconstrói via `setup()` no read; seleção aleatória/featureMap merece QA após save/restart. Aumentar raio afeta candidatos potenciais e custo do loop; nenhum budget adicional externo provado. WorldEffectPolicy vale para mutações próprias do Black Arcana, não para um segundo replay Ars.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.

## Certificação técnica estática — flower/desert feature consumers (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Classe `FloweringRitual` e ID `ars_nouveau:ritual_flowering` estão no manifesto do publisher 5.13.1; SHA-1 do JAR `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` é **identidade class→ID**, não equivalência dos métodos. Fonte upstream fixada `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [FloweringRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/FloweringRitual.java), [FeaturePlacementRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/FeaturePlacementRitual.java), [PlaceBlockFeature.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/features/PlaceBlockFeature.java), [BonemealFeature.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/features/BonemealFeature.java).

| Campo para perks | Contrato source-pinned e ressalvas |
|---|---|
| Runtime e geometria | `FeaturePlacementRitual` inicia com `checkRadius=7`; `onStart` soma `ItemStack.getCount()` dos ingredientes na tag `SOURCE_GEM_TAG`. Para cada feature gera uma lista `getTargetPositions()` de `BlockPos.betweenClosed` entre offsets e filtra por distância euclidiana `<=checkRadius`, embaralha com `Collections.shuffle`. **Não** é garantia de grade quadrada preenchida nem raio 7 fixo após gemas. |
| Progressão e tempo | `tick()` só age no servidor, com `while(true)`: testa candidatos sequencialmente até uma operação `onPlace` retornar true; então `return` **sem aumentar `positionIndex`**. No próximo tick, o gate `isEnoughBlocksFrom` consulta `featureMap` e bloqueia a mesma posição se distância `<=distanceFromOthers`. Na exaustão de posições avança `featureIndex`; ao esgotar todas chama `setFinished()`. **No máximo um retorno true por tick**, mas potencialmente muitas tentativas por tick, sem limite fixo de iterações por consumidor. |
| Features default | `PlaceBlockFeature(1.5, 0.8, randomFlower16)`: a lista definida no construtor tem 16 blocos de flores vanilla, inclusive flores altas; chance 0.8 somente se suporte abaixo não for ar e `state.canSurvive`. `BonemealFeature(5,0.8)` testa vanilla `BoneMealItem.applyBonemeal` na posição `pos.below()` com `ANFakePlayer` e 64 bone meal em stack local. |
| Features desert | Qualquer `ItemTags.SAND` consumido altera para `PlaceBlockFeature(3,0.04,CACTUS)` e `PlaceBlockFeature(1.5,0.1,DEAD_BUSH)`. `canConsumeItem` admite apenas o primeiro seletor sand enquanto `!isDesert`, além de `super.canConsumeItem` para Source Gem. Distâncias 3/1.5 são **separações entre placements da mesma feature**, não raios de busca. |
| Mutação de mundo | `PlaceBlockFeature.onPlace` chama `BlockItem.place(new BlockPlaceContext(...ANFakePlayer...))`, mas retorna `true` **sem inspecionar o resultado** de `place`; assim o `featureMap` pode registrar sucesso lógico sem bloco realmente colocado. `BonemealFeature` retorna o boolean da bonemeal vanilla; os caminhos têm proteção/claims potencialmente distintas. Não afirmar um callback único de sucesso ou drop/XP por planta. |
| Custo/estado/persistência | `FloweringRitual` herda `AbstractRitual.getSourceCost()=0` (**não equivale a ritual grátis**: ingrediente/ativação são do brazier). O pai persiste `featureIndex`, `positionIndex` e `checkRadius`, mas **não serializa `targetPositions` nem `featureMap`**; `read()` chama `setup()` e embaralha novos alvos. Retomar após save/restart não prova identidade dos alvos nem espaçamento anterior. |
| Authority | Flowering é provider-owned Ars, inclusive aleatoriedade e world mutations; `WorldEffectPolicy` do Black Arcana não intercepta esse caminho. Alterar raio, tentativa, seleção, chance ou Mastery requer um hook comprovado, orçamento de varredura e deduplicação. Nenhuma perk mutadora do RPG Skill Tree está demonstrada. |

**QA obrigatória:** inserção via tag no modpack, claims por feature, sucesso real vs retorno de `BlockItem.place`, reordenação no restart, mundo carregado, performance com grande número de Source Gems e replay. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
