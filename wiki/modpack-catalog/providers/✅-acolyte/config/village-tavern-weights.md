# Village tavern weights — Acolyte 1.0.3

**Tipo:** família de dez inteiros `COMMON`, arquivo `acolyte-common.toml`. Todas as dez opções têm intervalo inclusivo **1–100**; não existe peso zero autorizado pelo spec. Para desativar a adição use a opção `pool=disabled`.

| Chave TOML | Field de `ModCommonConfigs` | Default | Registro `<clinit>()V`, PCs | Leitura de `ModVillageAddition`, PCs |
| --- | --- | --- | --- | --- |
| `tavern_placement.plains.streets_weight` | `PLAINS_TAVERN_STREETS_WEIGHT` | 3 | 77–94 | 61–70 |
| `tavern_placement.plains.houses_weight` | `PLAINS_TAVERN_HOUSES_WEIGHT` | 12 | 97–115 | 73–82 |
| `tavern_placement.desert.streets_weight` | `DESERT_TAVERN_STREETS_WEIGHT` | 3 | 157–174 | 105–114 |
| `tavern_placement.desert.houses_weight` | `DESERT_TAVERN_HOUSES_WEIGHT` | 12 | 177–195 | 117–126 |
| `tavern_placement.taiga.streets_weight` | `TAIGA_TAVERN_STREETS_WEIGHT` | 3 | 237–254 | 149–158 |
| `tavern_placement.taiga.houses_weight` | `TAIGA_TAVERN_HOUSES_WEIGHT` | 12 | 257–275 | 161–170 |
| `tavern_placement.savanna.streets_weight` | `SAVANNA_TAVERN_STREETS_WEIGHT` | 3 | 317–334 | 193–202 |
| `tavern_placement.savanna.houses_weight` | `SAVANNA_TAVERN_HOUSES_WEIGHT` | 12 | 337–355 | 205–214 |
| `tavern_placement.snowy.streets_weight` | `SNOWY_TAVERN_STREETS_WEIGHT` | 3 | 397–414 | 237–246 |
| `tavern_placement.snowy.houses_weight` | `SNOWY_TAVERN_HOUSES_WEIGHT` | 12 | 417–435 | 249–258 |

`ModVillageAddition.addNewVillageBuilding(Lnet/neoforged/neoforge/event/server/ServerStartingEvent;)V` lê cada valor e o entrega a `addTavern(Lnet/minecraft/core/Registry;Lnet/minecraft/core/Registry;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;II)V`. Os PCs 120–193 escolhem o destino segundo [placement](village-tavern-placement.md). `addBuildingToPool(Lnet/minecraft/core/Registry;Lnet/minecraft/core/Registry;Lnet/minecraft/resources/ResourceLocation;Ljava/lang/String;I)V`, PCs 48–118, insere o peso no pool runtime e na lista de entradas ponderadas. Um pool de destino ausente é ignorado nos PCs 11–28.

O peso relativo da rua é aplicado ao template `acolyte:streets/<bioma>_tavern_01`; o de casa ao template `acolyte:tavern/houses/tavern_<bioma>`. Ambos usam elemento legacy, projeção rígida e processador vazio no método de adição, PCs 0–46. A validação dos números não demonstra frequência real em vilas geradas, compatibilidade com outros modificadores ou reload em jogo.

**Evidência exata:** `net/raptorzizi/acolyte/config/ModCommonConfigs.class`, `<clinit>()V` PCs 77–435; `net/raptorzizi/acolyte/worldgen/ModVillageAddition.class`, métodos e descritores acima.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
