# Demon spawn markers — Acolyte 1.0.3

**Tipo:** nove blocos com nove block items pareados, uma classe de bloco, um tipo de block entity `acolyte:demon_spawn_marker_be`. Cada linha preserva o mesmo ID em **ambos** os registries bloco/item.

| ID de bloco e block item | Material devolvido pela loot table publicada |
| --- | --- |
| `acolyte:demon_spawn_marker_oak` | `minecraft:oak_planks` |
| `acolyte:demon_spawn_marker_spruce` | `minecraft:spruce_planks` |
| `acolyte:demon_spawn_marker_birch` | `minecraft:birch_planks` |
| `acolyte:demon_spawn_marker_dark_oak` | `minecraft:dark_oak_planks` |
| `acolyte:demon_spawn_marker_acacia` | `minecraft:acacia_planks` |
| `acolyte:demon_spawn_marker_jungle` | `minecraft:jungle_planks` |
| `acolyte:demon_spawn_marker_mangrove` | `minecraft:mangrove_planks` |
| `acolyte:demon_spawn_marker_cobblestone` | `minecraft:cobblestone` |
| `acolyte:demon_spawn_marker_stone_bricks` | Nenhuma loot table própria correspondente empacotada |

As oito loot tables `data/acolyte/loot_table/blocks/demon_spawn_marker_<material>.json` das oito primeiras linhas fazem uma rolagem para o material comum, condicionada a `minecraft:survives_explosion`. Não devolvem o próprio marcador. A ausência da nona tabela e das cinco tavern tables é observação do archive, não promessa de comportamento sob datapacks.

O ticker existe somente no servidor e para o tipo de block entity correto. O estado começa `spawnCount=1`, `hasSpawned=false`. Enquanto `allowDemonStructureSpawning=false`, apenas aguarda. No primeiro tick elegível, tenta `spawnCount` escolhas iguais entre **demon warrior / archer / mage**; para cada entidade procura espaço não sólido de dois blocos até 3 blocos acima e offsets X/Z −1…1, com apoio não ar. Se não encontrar, usa o bloco acima do marcador. Finaliza como `STRUCTURE`, marca persistência, e adiciona ao servidor. Ao terminar marca `hasSpawned=true`, inclusive se uma criação de entidade falhou; portanto não descrever como reposição contínua.

`spawnCount` e `hasSpawned` são salvos/carregados; uma contagem carregada é limitada inferiormente a 1. Não há limite superior demonstrado no carregamento. Os templates podem publicar contagens e estados diferentes: castelos incluem marcadores já consumidos; ver as respectivas fichas. A persistência do booleano reduz reexecução após recarga, mas exatamente uma execução sob crash não foi testada.

**Evidência exata:** `net/raptorzizi/acolyte/registries/ModBlocksRegistry.class`, `<clinit>()V` PCs 73–184 e `registerBlock(Ljava/lang/String;Ljava/util/function/Supplier;)Lnet/neoforged/neoforge/registries/DeferredBlock;` PCs 0–15, `registerBlockItem(Ljava/lang/String;Lnet/neoforged/neoforge/registries/DeferredBlock;)V` PCs 0–14. `net/raptorzizi/acolyte/registries/ModBlockEntityRegistry.class`, `lambda$static$1()Lnet/minecraft/world/level/block/entity/BlockEntityType;` PCs 0–128 e `<clinit>()V` PCs 27–40. `net/raptorzizi/acolyte/block/demon_spawn_marker/DemonSpawnMarkerBlock.class`, `getTicker(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/block/entity/BlockEntityType;)Lnet/minecraft/world/level/block/entity/BlockEntityTicker;` PCs 0–28. `net/raptorzizi/acolyte/block/demon_spawn_marker/DemonSpawnMarkerBlockEntity.class`, `tick(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;Lnet/raptorzizi/acolyte/block/demon_spawn_marker/DemonSpawnMarkerBlockEntity;)V` PCs 0–251, `findValidSpawnPos(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/core/BlockPos;)Lnet/minecraft/core/BlockPos;` PCs 0–105; `saveAdditional(Lnet/minecraft/nbt/CompoundTag;Lnet/minecraft/core/HolderLookup$Provider;)V` PCs 6–26; `loadAdditional` com mesmo descritor PCs 6–39.

**Integração:** observar entidades produzidas e finalização. Não há cast, custo de mana, cooldown de magia ou mutator Black Arcana demonstrado pelo marcador.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
