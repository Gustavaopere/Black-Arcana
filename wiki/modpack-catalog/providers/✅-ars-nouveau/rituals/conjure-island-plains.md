# Conjure Island: Plains

Status: `SOURCE-PINNED 5.13.1 / BIOME-WORLDGEN RITUAL`

- Registry id: `ars_nouveau:ritual_conjure_island_plains`
- Class: `ConjurePlainsRitual`
- Base radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Source cost: `50` per provider Source request
- Source request cadence: every five counted eligible attempts (`setBlock` result unchecked)
- Placement budget: at most one eligible placement attempt per ritual tick (actual block write unverified)
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

The ritual inherits `ConjureBiomeRitual`. On start it builds a Manhattan tracker centered three blocks below the ritual and increases radius by consumed Source Gems.

For eligible positions inside the spherical radius, the ritual places:

- Grass Block at ritual Y−1;
- Dirt at the other generated island layers.

Each successful placement also calls Ars Nouveau's biome-change helper for the ritual biome. The default biome is Plains.

If one Frostaya Pod is consumed, the ritual switches biome output to Snowy Plains while preserving the same island block construction rules.

The generation loop is bounded: each ritual tick searches up to `radius` candidate tracker positions but returns immediately after the first eligible placement attempt (setBlock result unchecked). Every five eligible attempts, it resets the local counter and marks the ritual as needing Source.

## Authority / Black Arcana boundary

Block placement, biome mutation, Source-gem radius augmentation, Source debit and tracker persistence are Ars Nouveau authority. Black Arcana must not duplicate island blocks/biome changes or replace this with an unbounded worldgen operation.

Independent Black Arcana terrain/biome mutation remains subject to `WorldEffectPolicy` and explicit bounded-work contracts.

## QA

Source behavior is pinned to 5.13.1. Protection/claim interaction is not explicitly visible in `ConjureBiomeRitual`'s placement path and therefore requires full-pack runtime QA rather than inference.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`ConjurePlainsRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/ConjurePlainsRitual.java) no Ars 5.13.1. Executor herdado [`ConjureBiomeRitual.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ConjureBiomeRitual.java).
- **Volume e orçamento:** herda `ConjureBiomeRitual`: `radius=7+SourceGemCount`; `ManhattenTracker` centrado 3 blocos abaixo; por tick examina no máximo `radius` posições da sequência e realiza **no máximo 1 tentativa elegível de placement, sem conferir setBlock** com `setState` + `RitualUtil.changeBiome`. A cada 5 placements marca `setNeedsSource(true)` e reinicia contador; Source cost declarado 50.
- **Composição:** padrão PLAINS com GRASS_BLOCK em Y−1 e DIRT em outras camadas; se `FROSTAYA_POD` foi consumido, marca `isSnowy` e usa biome `SNOWY_PLAINS` mantendo as mesmas layers. `canConsumeItem` aceita uma escolha Frostaya além de Source Gems.
- **Persistência e risco:** `ConjurePlainsRitual` serializa `isSnowy`; pai serializa `tracker`/`radius`. Os caminhos `ConjureBiomeRitual.setState` e `changeBiome` não exibem claim gate local; não presumir proteção universal nem implementá-lo duplicadamente em RPG.
- **Perks:** raio e chamadas de worldgen implicam volume, biome e Source distintos; não transformar este ritual em cast de bioma de Black Arcana ou gratificar cada bloco como ritual individual.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática — Plains / Snowy Plains (2026-10-25)

**✅ STATIC_TECHNICAL_CATALOG_ONLY · ⛔ mutating_hook=NOT_VERIFIED · ⚠️ physical_qa=NOT_TESTED.** Publisher ars_nouveau-1.21.1-5.13.1.jar, SHA-1 02782d071ee5fab3b5c4b8ced67b7e1748277dfd: identidade ars_nouveau:ritual_conjure_island_plains → ConjurePlainsRitual comprovada, **não** equivalência de bytecode dos métodos. Sources fixados em baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157: [ConjurePlainsRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/ConjurePlainsRitual.java), [ConjureBiomeRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ConjureBiomeRitual.java), [RitualUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/RitualUtil.java), [ManhattenTracker.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/ManhattenTracker.java).

- **Seleção de variante:** ConjurePlainsRitual constrói Biomes.PLAINS. Se consumir BlockRegistry.FROSTAYA_POD.asItem(), onStart marca isSnowy e escolhe Biomes.SNOWY_PLAINS. canConsumeItem permite um Frostaya Pod além de SOURCE_GEM_TAG do pai. onStart e read/write do filho persistem isSnowy, mas read só seleciona Snowy Plains quando esse boolean é true.
- **Alcance e algoritmo:** ConjureBiomeRitual usa radius=7 mais contagens ItemStack de SOURCE_GEM_TAG. O centro do ManhattenTracker é getPos().below(3), com parâmetros radius,2,radius. O tick em servidor percorre até radius candidatos computeNext() por invocação, exige distância euclidiana <=radius e BlockState.canBeReplaced, conclui quando tracker devolve null. Não executa todo o worldgen em um único efeito; trabalha candidato a candidato.
- **Composição:** ConjurePlainsRitual.stateForPos escolhe Blocks.GRASS_BLOCK em nextPos.getY()==getPos().getY()-1; nos demais níveis, Blocks.DIRT. O modo Snowy Plains **não gera diretamente neve** pelo stateForPos: troca o bioma e a apresentação VFX, mantendo as mesmas layers de grass/dirt. Não inventar materiais por biome distinto.
- **Contabilização versus confirmação:** ConjureBiomeRitual.setState(nextPos,state) chama getWorld().setBlock(pos,state,2) **sem testar o resultado**. Em seguida chama RitualUtil.changeBiome, playSound, blocksPlaced++ e retorna. Assim, mesmo que setBlock falhe, um candidato elegível pode ser contabilizado; **uma tentativa elegível contabilizada por tick** não é prova de um bloco colocado. Biome write é efeito distinto do block write.
- **Biome mutation:** RitualUtil.changeBiome edita PalettedContainer<Holder<Biome>> das LevelChunkSection, dirty chunk e envia ChangeBiomePacket ao tracking set no servidor. A cobertura efetiva de quart biome não equivale necessariamente à posição única do bloco e requer QA de save/reload, chunks e outros mods que mudam biomas.
- **Source:** getSourceCost()=50, blocksBeforeSourceNeeded=5 e setNeedsSource(true) após cinco incrementos de blocksPlaced. Contador é de **tentativas elegíveis**, não necessariamente colocação efetiva. O pai persiste tracker e radius em NBT, mas **não persiste blocksPlaced**: um restart no meio da janela pode mudar o ponto da próxima cobrança. O RitualBrazierTile permanece autoridade de transações Source. Não há cooldown de spell ou dano ofensivo nesta implementação.
- **Boundaries:** ausência de destroyRespectsClaim no trecho de setState não prova resultado de claim; fazer QA in-game antes de supor proteção/bypass. WorldEffectPolicy limita mutações originárias do Black Arcana, não substitui o Ars. RPG Skill Tree não cria um segundo ritual, não concede Mastery por bloco tentado e não altera raio/bioma sem adapter real, deduplicação e budget para área, tempo e pacotes de rede.

**Pendências:** efetividade do setBlock, restart em lote de cinco, alcance do changeBiome, NBT legado, Source disponível, chunks e claim guards, reload e performance com muitos Source Gems. mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED. Stage 06.05 e Stage 09 não promovidos.
