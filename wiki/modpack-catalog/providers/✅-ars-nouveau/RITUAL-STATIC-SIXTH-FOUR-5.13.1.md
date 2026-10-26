# Ars Nouveau 5.13.1 — sexto lote: fechamento documental do recorte de 24 rituais

**Objetivo:** concluir os quatro contratos estáticos restantes, preservando runtime, clean-room, deduplicação e integração fail-closed. O 24/24 é **apenas para as 24 fichas de rituais da classe/registry binariamente identificadas**, não certificação integral de Ars Nouveau nem prova funcional no modpack.

## Proveniência

- Modlist física do sibling RPG Skill Tree: Minecraft 1.21.1, Ars Nouveau `5.13.1`, `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`.
- Source revision exato: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.
- [Auditoria binária de 85 glyphs + 24 rituais](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md): identidade de ID↔classe no binário, **não** equivalência de código de métodos, admissão de mobs, claims nem execução real em pack.
- Claims homologados exclusivamente: `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

| Ritual | Classes e consumidores reais | Incerteza que impede mutating perk |
|---|---|---|
| [Conjure Island Desert](rituals/conjure-island-desert.md) | `ConjureDesertRitual` / `ConjureBiomeRitual` / `ManhattenTracker` / `RitualUtil.changeBiome`: Desert Sand/Sandstone ou Badlands com Terracotta | `setState` chama `setBlock` sem conferir retorno; **`blocksPlaced` conta tentativas elegíveis**. Biome data pode alcançar mais de um bloco. `blocksPlaced` não persistido; custo Source 50 requisitado a cada 5 contagens pode reagrupar em restart. |
| [Conjure Island Plains](rituals/conjure-island-plains.md) | `ConjurePlainsRitual` gera GRASS_BLOCK em Y−1 e DIRT no resto; Frostaya Pod muda chave para SNOWY_PLAINS, não coloca snow automaticamente | Mesmos `setBlock` e `changeBiome` sem transação conjunta e contagem Source após cinco tentativas; `isSnowy`, `radius`, `tracker` persistem, mas `blocksPlaced` não. |
| [Summon Animals](rituals/summon-animals.md) | `RitualAnimalSummoning` + `SummonRitualRecipe`: pool `SpawnerData` por bioma vs receita `WeightedMobType` | **Contradição de tipos no source:** `recipe.mobs` produz `WeightedMobType`, mas execução só aceita `entry instanceof MobSpawnSettings.SpawnerData` para invocar/incrementar. `bats.json` gerado tem count=5/Amethyst Shard, porém esse arquivo não prova spawn funcional. `MobSource` declarado e não consultado em getMobs. Mesmo no caminho baseline, `addFreshEntity` não é verificado. |
| [Summon Wilden](rituals/summon-wilden.md) | `RitualWildenSummoning`: incrementProgress a cada 20 ticks, work a cada 60; três wildens normais, ou Chimera após três drops | `progress>=8/15` **não é contagem de spawns**. Chimera testa até **11×11×5=605 BlockPos**, `EventHooks.canEntityGrief`, destroy speed, harvest level4 e `destroyBlockSafelyWithoutSound`, que publica `BlockEvent.BreakEvent`, sem conferir retorno de destruição. |

## Guardrails de implementação

1. **World safety e biomas:** `RitualUtil.changeBiome` altera containers de bioma por chunk e pacotes de sincronização; isso não é uma mudança isolada de block state. O `WorldEffectPolicy` do Black Arcana **somente** governa alterações próprias BA, não converte os callbacks do Ars em autoridade BA. Não aumentar radius sem custo de chunk, packet, world-border e permissão de claim.
2. **Source e persistência:** `ConjureBiomeRitual.getSourceCost()=50` e `blocksBeforeSourceNeeded=5`; `blocksPlaced` não persiste. `RitualAnimalSummoning` e `RitualWildenSummoning` herdam `AbstractRitual.getSourceCost()=0`, **não equivalem a rituais grátis**: tablets e itens são outros custos próprios do brazier. Nunca inventar cooldown de spell ou converter Source para mana BA.
3. **Fauna e variantes do datapack:** `WeightedMobType` e `MobSpawnSettings.SpawnerData` **não são tipos iguais**. Não afirmar que recipes custom, bats, weights de modded mobs ou `MOB_LIST` estão funcionais; QA com binário e cliente é obrigatório. Spawn não confirmado pelo retorno de `addFreshEntity`; progress do código não mede necessariamente entidade admitida.
4. **Destruição no boss:** whitelist de Wilden drops, tags, condições `canEntityGrief` e callback `BlockEvent.BreakEvent` exigem QA. 605 é volume **candidato**, não número de quebras. Não reexecutar spawn, drop, efeito de boss ou prêmio por loop usando RPG Skill Tree.
5. **Authority:** Ars Nouveau é provider de seus rituais e Source; Black Arcana continua dono do próprio runtime/casting/rituais/hazards/Corruption/Strain e persistência. RPG Skill Tree fornece progressão, Mastery, atributos, perks e gates apenas via boundary existente e verificado.
6. **Continuidades de Stage:** Stage 06.05 segue pendente de validação física; Stage 09 continua campanha de aceitação real. CI/Java build/GameTests não substituem QA do Ars com o JAR instalado.

**Pendências físicas:** equivalência dos métodos do publisher 5.13.1, recipe bats.json, campos MobSource e regras por bioma, claims, retorno real de setBlock e addFreshEntity, NBT/restart e agendamento Source, biome packet/chunk, Wilden mob grief em mundo protegido, performance e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

**Contadores após merge, para o recorte atual:** rituais **24/24**, fichas Ars Nouveau **77/138**, fichas globais **77/2075**, providers integralmente certificados **0/164**. Universos mais amplos podem requerer novas fichas; não tratar 24/24 como total mágico do mod.
