# Conjure Island: Desert

Status: `SOURCE-PINNED 5.13.1 / BIOME-WORLDGEN RITUAL`

- Registry id: `ars_nouveau:ritual_conjure_island_desert`
- Class: `ConjureDesertRitual`
- Base radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Source cost: `50` per provider Source request
- Source request cadence: every five counted eligible attempts (`setBlock` return unverified)
- Placement budget: at most one eligible placement attempt per ritual tick (actual block write unchecked)
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

Every eligible placement attempt also invokes the provider biome-change helper. The shared helper requests 50 Source every five successful placements.

## Authority / Black Arcana boundary

Terrain generation, biome conversion, Source accounting and persistent tracker state are Ars Nouveau authority. Black Arcana must not duplicate blocks or biome changes.

Independent Black Arcana terrain/biome mechanics remain subject to `WorldEffectPolicy` and bounded scheduling.

## QA

Source behavior is pinned to 5.13.1. As with the Plains variant, direct protection/claim preflight is not explicit in this helper path and therefore requires runtime validation.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`ConjureDesertRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/ConjureDesertRitual.java) no Ars 5.13.1. Executor herdado [`ConjureBiomeRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ConjureBiomeRitual.java).
- **Contrato herdado:** `ConjureDesertRitual extends ConjureBiomeRitual`. Em `onStart`, `radius=7+sum(SourceGemTag.count)` e cria `ManhattenTracker(brazier.below(3),radius,2,radius)`. `tick` consulta no máximo `radius` próximos candidatos por iteração e retorna depois de **um** placement bem-sucedido; testa distância euclidiana ao brazier e `canBeReplaced`.
- **Bioma e profundidade:** padrão DESERT, coloca SAND somente no nível do brazier Y−1, SANDSTONE nas demais camadas elegíveis. Com qualquer `ItemTags.TERRACOTTA`, muda bioma para BADLANDS e distribui RED_SAND depth1, ORANGE_TERRACOTTA depth2, RED_TERRACOTTA depths3–4, TERRACOTTA demais.
- **Source:** `ConjureBiomeRitual` chama `RitualUtil.changeBiome` a cada placement, acumula `blocksPlaced` e, a cada `>=5` tentativas elegíveis contabilizadas (não resultado confirmado de `setBlock`), reseta contador e marca `setNeedsSource(true)`; custo declarado `getSourceCost=50`, **não** débito fixo por tick. Pai serializa `tracker` e `radius`; estado dos blocos/bioma e Source efetivo precisam de teste de restart.
- **Segurança:** `setState` realiza `world.setBlock(pos,state,2)` e o helper exibido não possui claim preflight explícito; é lacuna de admissão a auditar, não permissão para bypass em magia Black Arcana.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática — Desert / Badlands (2026-10-25)

**✅ STATIC_TECHNICAL_CATALOG_ONLY · ⛔ mutating_hook=NOT_VERIFIED · ⚠️ physical_qa=NOT_TESTED.** Identidade compilada: ars_nouveau:ritual_conjure_island_desert → ConjureDesertRitual (publisher 5.13.1, JAR SHA-1 02782d071ee5fab3b5c4b8ced67b7e1748277dfd). A checagem binária confirma a associação ID/classe, **não** a equivalência dos corpos dos métodos com o source do commit baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157.

**Fontes:** [ConjureDesertRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/ConjureDesertRitual.java), [ConjureBiomeRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ConjureBiomeRitual.java), [ManhattenTracker.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ManhattenTracker.java), [RitualUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/RitualUtil.java).

- **Ativação e inputs:** ConjureBiomeRitual.onStart executa setup no servidor, soma ItemStack.getCount() dos itens SOURCE_GEM_TAG ao radius inicial 7 e monta ManhattenTracker(getPos().below(3),radius,2,radius). ConjureDesertRitual.onStart muda de Biomes.DESERT para Biomes.BADLANDS se houver ItemTags.TERRACOTTA entre os consumidos. canConsumeItem permite um seletor terracotta e Source Gems adicionais.
- **Scan/cadência:** em tick do servidor, for(int i=0;i<radius;i++) solicita no máximo radius candidatos do tracker.computeNext(), filtra distância euclidiana entre centros <=radius e BlockState.canBeReplaced(); tracker nulo (computeNext()==null) encerra com setFinished(). O tracker carrega cursor/profundidade/espelho Z; não é um cast de área instantâneo. Após o primeiro candidato elegível, a execução retorna.
- **Superfícies mutadoras e confirmação:** ConjureBiomeRitual.setState(nextPos,state) chama getWorld().setBlock(pos,state,2) **sem conferir o boolean**. Em seguida RitualUtil.changeBiome(getWorld(),nextPos,biome), playSound e blocksPlaced++ acontecem mesmo se a colocação não foi confirmada. Logo, blocksPlaced mede **tentativas elegíveis contabilizadas**, não blocos efetivamente colocados. É no máximo uma tentativa elegível por tick; biome write e block write não são uma transação indivisível.
- **Terreno e profundidade:** modo Desert: Blocks.SAND no plano Y do brazier menos 1; Blocks.SANDSTONE nos outros níveis elegíveis. Com terracotta: depth = getPos().getY()-placePos.getY(); 1=RED_SAND, 2=ORANGE_TERRACOTTA, 3/4=RED_TERRACOTTA, demais=TERRACOTTA; biome Badlands. Não inferir mudança de dano, projétil, alvos-vivos ou cooldown de spell deste ritual.
- **Granularidade de bioma:** RitualUtil.changeBiome consulta Registries.BIOME, obtém LevelChunk e altera PalettedContainer<Holder<Biome>> de LevelChunkSection; no servidor marca chunk dirty/unsaved e envia ChangeBiomePacket a jogadores que rastreiam o chunk. Portanto não afirmar que altera **somente** o biome do BlockPos individual, nem assumir que a área alterada equivale exatamente aos blocos visualmente formados.
- **Source e NBT:** ConjureBiomeRitual.getSourceCost()=50, blocksBeforeSourceNeeded=5. Quando blocksPlaced>=5, redefine blocksPlaced=0 e chama setNeedsSource(true). Esse agrupamento decorre de **5 tentativas elegíveis**, não 5 colocações confirmadas e nem 50 Source por tick. O read/write do pai persiste tracker e radius, mas **não persiste blocksPlaced**; save/restart pode reiniciar a contagem de tentativas entre pedidos Source, exigindo QA real de cobrança. No read do filho, Badlands é restaurado verificando itens consumidos; tag radius ausente usa getInt("radius") sem fallback nesta classe.
- **Segurança/integração:** nem setState nem o trecho de changeBiome demonstram destroyRespectsClaim como preflight local; isso não prova permissão de bypass no modpack. WorldEffectPolicy governa somente world effects **próprios** do Black Arcana. Ars retém authority dos blocos, bioma, Source, loop e NBT. RPG Skill Tree fornece progressão/Mastery/perks/gates só mediante adapter real; não duplicar biomes/placements, atribuir XP a cada tentativa ou ampliar radius sem budget de chunk, packets, volume e claims.

**Gates físicos pendentes:** setBlock retornando false, limites de altura/chunk, permissões de claims, alcance e atualização de biome no cliente, restart em lote de cinco, custo real, sobreposição de biomas de outros mods e performance/multiplayer. mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED.
