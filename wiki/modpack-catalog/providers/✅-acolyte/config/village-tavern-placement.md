# Village tavern placement — Acolyte 1.0.3

**Tipo:** família de cinco opções `COMMON`, arquivo registrado `acolyte-common.toml`. Não há opção de magia, dano, mana ou recrutamento nesta família.

Cada chave `tavern_placement.<bioma>.pool` aceita exatamente `streets`, `houses`, `both` ou `disabled`, com default `streets` para os cinco biomas. A validação exige uma string presente nessa lista; a comparação é literal.

| Chave TOML | Field de `ModCommonConfigs` | Registro `<clinit>()V`, PCs | Leitura no consumidor, PCs |
| --- | --- | --- | --- |
| `tavern_placement.plains.pool` | `PLAINS_TAVERN_POOL` | 45–74 | 52–58 |
| `tavern_placement.desert.pool` | `DESERT_TAVERN_POOL` | 125–154 | 96–102 |
| `tavern_placement.taiga.pool` | `TAIGA_TAVERN_POOL` | 205–234 | 140–146 |
| `tavern_placement.savanna.pool` | `SAVANNA_TAVERN_POOL` | 285–314 | 184–190 |
| `tavern_placement.snowy.pool` | `SNOWY_TAVERN_POOL` | 365–394 | 228–234 |

O consumidor é `ModVillageAddition.addNewVillageBuilding(Lnet/neoforged/neoforge/event/server/ServerStartingEvent;)V`. Em `addTavern(Lnet/minecraft/core/Registry;Lnet/minecraft/core/Registry;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;II)V`, PCs 120–137 selecionam a rua, 140–158 a casa, 161–193 ambos; o caminho default chega ao retorno no PC 196 sem adicionar construção. Isso cobre `disabled`. A aplicação ocorre no início do servidor aos pools compartilhados; não altera vilas já geradas.

Os destinos são `minecraft:village/<bioma>/streets` e `minecraft:village/<bioma>/houses`; os templates e a relação rua → tavern estão em [Village taverns](../encounters/village-taverns.md). Os pesos ficam em [Village tavern weights](village-tavern-weights.md). Um peso é relativo às demais entradas do pool, não uma chance absoluta de uma vila conter tavern.

**Evidência exata:** `net/raptorzizi/acolyte/config/ModCommonConfigs.class`, `<clinit>()V` PCs 10–475 e `isValidPool(Ljava/lang/Object;)Z` PCs 0–29; `net/raptorzizi/acolyte/worldgen/ModVillageAddition.class`, métodos acima. `net/raptorzizi/acolyte/AcolyteMod.class`, `<init>(Lnet/neoforged/bus/api/IEventBus;Lnet/neoforged/fml/ModContainer;)V` PCs 77–98 registra `COMMON`.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
