# Gamerules — Acolyte 1.0.3

**Tipo:** cinco gamerules booleanas de categoria `SPAWNING`; **default publisher: `true` para todas**. Os defaults do registro não provam os valores salvos no mundo.

| Nome exato da regra | Field de `ModGameRules` | Registro `<clinit>()V` | Consumidor observado |
| --- | --- | --- | --- |
| `allowDemonStructureSpawning` | `ALLOW_DEMON_STRUCTURE_SPAWNING` | PCs 0–12 | `DemonSpawnMarkerBlockEntity.tick`, PCs 21–35 |
| `allowHumanStructureSpawning` | `ALLOW_HUMAN_STRUCTURE_SPAWNING` | PCs 15–27 | `TavernSpawnMarkerBlockEntity.tick`, PCs 56–70 |
| `allowHornMerchantSpawning` | `ALLOW_HORN_MERCHANT_SPAWNING` | PCs 30–42 | `HornMerchantSpawner.tick`, PCs 36–50 |
| `allowDemonNaturalSpawning` | `ALLOW_DEMON_NATURAL_SPAWNING` | PCs 45–57 | `ModUtils.checkDemonSpawnRules`, PCs 0–28 |
| `allowHumanNaturalSpawning` | `ALLOW_HUMAN_NATURAL_SPAWNING` | PCs 60–72 | `ModUtils.checkHumanSpawnRules`, PCs 0–28 |

As duas regras de estruturas bloqueiam somente os ticks dos marcadores correspondentes. O helper `DemonSpawner.spawnRandom` não consulta essas regras; `HumanSpawner.spawnRandom` também não, inclusive quando usado por ovo de spawn. A regra do Horn Merchant é lida depois da redefinição de seu timer. As duas regras naturais são consultadas pelo predicado apenas quando o accessor é uma instância de `ServerLevel`; o restante do predicado é descrito em [Demon spawning](../encounters/demon-spawning.md) e [Human spawning](../encounters/human-spawning.md). Não inferir que as cinco regras removem entidades existentes, bloqueiam toda criação por comando/ovo ou desativam a geração dos prédios.

**Evidência exata:** `net/raptorzizi/acolyte/setup/ModGameRules.class`, `<clinit>()V` PCs 0–75; `init()V` PC 0 é o ponto de inicialização chamado por `net/raptorzizi/acolyte/AcolyteMod.class`, construtor, PC 4. Consumidores: `net/raptorzizi/acolyte/block/demon_spawn_marker/DemonSpawnMarkerBlockEntity.class`, `tick(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;Lnet/raptorzizi/acolyte/block/demon_spawn_marker/DemonSpawnMarkerBlockEntity;)V`; variante tavern com a respectiva classe no último argumento; `net/raptorzizi/acolyte/entity/mobs/horn_merchant/HornMerchantSpawner.class`, `tick(Lnet/minecraft/server/level/ServerLevel;ZZ)I`; `net/raptorzizi/acolyte/util/ModUtils.class`, `checkDemonSpawnRules` / `checkHumanSpawnRules` com descritor `(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/ServerLevelAccessor;Lnet/minecraft/world/entity/MobSpawnType;Lnet/minecraft/core/BlockPos;Lnet/minecraft/util/RandomSource;)Z`.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
