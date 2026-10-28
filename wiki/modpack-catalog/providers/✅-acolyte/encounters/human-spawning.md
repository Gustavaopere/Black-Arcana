# Human spawning — Acolyte 1.0.3

**Tipo:** família de aparecimento natural e helper de seleção aleatória. Não é magia independente.

Os três biome modifiers usam `neoforge:add_spawns`, alvo `#minecraft:is_overworld`, grupos de tamanho mínimo/máximo **1/1**. Os pesos são relativos ao pool de spawning, não percentuais.

| Entidade | Peso natural | Recurso exato no archive |
| --- | --- | --- |
| `acolyte:human_archer` | 1 | `data/acolyte/neoforge/biome_modifier/human_archer_spawns.json` |
| `acolyte:human_mage` | 1 | `data/acolyte/neoforge/biome_modifier/human_mage_spawns.json` |
| `acolyte:human_warrior` | 1 | `data/acolyte/neoforge/biome_modifier/human_warrior_spawns.json` |

O predicado natural exige biome fora da tag indicada por `net.neoforged.neoforge.common.Tags.Biomes.NO_DEFAULT_MONSTERS`, dificuldade diferente de `PEACEFUL`, `Mob.checkMobSpawnRules` e ausência de qualquer `HumanEntity` no AABB do bloco inflado em 300 blocos. Não há chamada de teste de escuridão neste método. Sua regra `allowHumanNaturalSpawning` é consultada quando o accessor é `ServerLevel`. O limite de proximidade inclui subclasses e não significa um raio esférico.

`ModCommonSetup.spawnPlacements(Lnet/neoforged/neoforge/event/entity/RegisterSpawnPlacementsEvent;)V` registra as três entidades `ON_GROUND`, heightmap `MOTION_BLOCKING_NO_LEAVES`, com operação **OR**. PCs 81–159. O predicado é uma contribuição à composição de spawn placements; não presumir veto universal se outro mod registrar condições OR adicionais.

`HumanSpawner.spawnRandom` sorteia **archer / warrior / mage com peso igual 1/1/1**, centraliza a entidade no X/Z do bloco, escolhe orientação, chama `finalizeSpawn` com **`MobSpawnType.STRUCTURE`**, adiciona a entidade ao servidor e a retorna; uma criação nula retorna nulo. Ele não é o scheduler natural, não verifica terreno, não consulta gamerule e não marca persistência nesse método. Seus consumidores observados são o ovo de spawn aleatório e o TavernSpawnMarker; spawn natural usa os recursos e o predicado acima. As magias eventuais continuam pertencendo a Iron’s e dependem do arquétipo.

**Evidência exata:** `net/raptorzizi/acolyte/entity/mobs/wizards/human/HumanSpawner.class`, `spawnRandom(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/core/BlockPos;)Lnet/raptorzizi/acolyte/entity/mobs/wizards/human/HumanEntity;`, PCs 0–100 seleção/nulo, 101–163 posicionamento/finalização/inserção; `net/raptorzizi/acolyte/util/ModUtils.class`, `checkHumanSpawnRules(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/core/BlockPos;Lnet/minecraft/util/RandomSource;)Z`, PCs 0–111; `net/raptorzizi/acolyte/setup/ModCommonSetup.class`, método acima. O vínculo do predicado foi conferido em `ModCommonSetup` com `javap -v`: BootstrapMethods #0 → `checkDemonSpawnRules`, #1 → `checkHumanSpawnRules`; os métodos de evento têm `@SubscribeEvent`. O consumidor do ovo é `net/raptorzizi/acolyte/registries/ModItemsRegistry$2.class`, `useOn(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;`, PC 31.

**Integração:** observar spawn e origem reais; não converter a rolagem do helper em uma distribuição natural ou tratar todos os mobs da família como casts iniciados.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
