# Tavern spawn markers — Acolyte 1.0.3

**Tipo:** cinco blocos e cinco block items pareados, uma classe de bloco e um tipo de block entity `acolyte:tavern_spawn_marker_be`. Cada linha representa o mesmo ID em ambos os registries bloco/item.

| ID de bloco e block item | Uso no template de tavern |
| --- | --- |
| `acolyte:tavern_spawn_marker_oak` | Plains |
| `acolyte:tavern_spawn_marker_acacia` | Savanna |
| `acolyte:tavern_spawn_marker_spruce` | Snowy |
| `acolyte:tavern_spawn_marker_cobblestone` | Taiga |
| `acolyte:tavern_spawn_marker_sandstone` | Desert |

O ticker só funciona no servidor para o tipo correto. Efetua verificação a cada **100 ticks**, com fase derivada da posição; não há gate de dia/noite. Exige `allowHumanStructureSpawning=true`; a rolagem prossegue quando `nextFloat() <= 0.4`. Conta **somente `HumanMageEntity`** no AABB do bloco inflado em **50** e interrompe com contagem ≥4. Esse cap não conta explicitamente warriors e archers: não tratá-lo como limite de quatro humanos totais.

Busca até **20** posições X/Z nos offsets **−5…4**, descendo do Y do marcador +3 até −3; exige apoio de renderização sólida e não ar, pés/cabeça não sólidos. Sem local retorna e tenta em futura verificação. Com local chama `HumanSpawner.spawnRandom`, que escolhe archer/warrior/mage igualmente e finaliza como `STRUCTURE`. Não existe flag `hasSpawned` nem contagem persistida neste block entity; é uma superfície recorrente de encontro/recrutamento. Os valores 50/5/100/4 são constantes deste comportamento, não knobs de config.

Nenhuma loot table própria `data/acolyte/loot_table/blocks/tavern_spawn_marker_*.json` está empacotada. A presença de block items pareados não prova que quebrar um marcador permita coletá-lo em survival.

**Evidência exata:** `net/raptorzizi/acolyte/registries/ModBlocksRegistry.class`, `<clinit>()V` PCs 8–67; `registerBlock(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredBlock;` PCs 0–15 e `registerBlockItem(Ljava/lang/String;Lnet/neoforged/neoforge/registries/DeferredBlock;)V` PCs 0–14. `net/raptorzizi/acolyte/registries/ModBlockEntityRegistry.class`, `lambda$static$0()Lnet/minecraft/world/level/block/entity/BlockEntityType;` PCs 0–76 e `<clinit>()V` PCs 11–24. `net/raptorzizi/acolyte/block/tavern_spawn_marker/TavernSpawnMarkerBlock.class`, `getTicker(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/block/entity/BlockEntityType;)Lnet/minecraft/world/level/block/entity/BlockEntityTicker;` PCs 0–28. `net/raptorzizi/acolyte/block/tavern_spawn_marker/TavernSpawnMarkerBlockEntity.class`, `tick(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;Lnet/raptorzizi/acolyte/block/tavern_spawn_marker/TavernSpawnMarkerBlockEntity;)V` PCs 0–145 (intervalo 8–49, gamerule 56–70, sorteio 71–87, contagem 88–122, spawn 123–145); `findValidSpawnPos(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/core/BlockPos;)Lnet/minecraft/core/BlockPos;` PCs 0–201.

**Integração:** a contagem de magos e a reposição contínua devem ser testadas com recrutamento e multiplayer. Não inferir que `allowHumanNaturalSpawning` controla este caminho.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
