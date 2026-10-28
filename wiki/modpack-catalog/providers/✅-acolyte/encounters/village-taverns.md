# Village taverns — Acolyte 1.0.3

**Tipo:** cinco variantes de tavern acrescentadas aos pools de vilas vanilla. São cinco superfícies de encontro, sem cinco novos `worldgen/structure/*.json` próprios ou sets de spacing/separation. Junto dos 13 IDs configurados de castelo/Lieutenant/tower/watchtower, compõem as **18 variantes publicadas**. Os **28 NBTs** do archive são templates/pedaços: não 28 IDs adicionais de estruturas.

| ID do pool de tavern | Recurso do pool | Template de rua | Template escolhido pelo pool | Template de casa adicionado diretamente |
| --- | --- | --- | --- | --- |
| `acolyte:village/plains/tavern` | `data/acolyte/worldgen/template_pool/village/plains/tavern.json` | `data/acolyte/structure/streets/plains_tavern_01.nbt` | `data/acolyte/structure/tavern/tavern_plains.nbt` | `data/acolyte/structure/tavern/houses/tavern_plains.nbt` |
| `acolyte:village/desert/tavern` | `data/acolyte/worldgen/template_pool/village/desert/tavern.json` | `data/acolyte/structure/streets/desert_tavern_01.nbt` | `data/acolyte/structure/tavern/tavern_desert.nbt` | `data/acolyte/structure/tavern/houses/tavern_desert.nbt` |
| `acolyte:village/taiga/tavern` | `data/acolyte/worldgen/template_pool/village/taiga/tavern.json` | `data/acolyte/structure/streets/taiga_tavern_01.nbt` | `data/acolyte/structure/tavern/tavern_taiga.nbt` | `data/acolyte/structure/tavern/houses/tavern_taiga.nbt` |
| `acolyte:village/savanna/tavern` | `data/acolyte/worldgen/template_pool/village/savanna/tavern.json` | `data/acolyte/structure/streets/savanna_tavern_01.nbt` | `data/acolyte/structure/tavern/tavern_savanna.nbt` | `data/acolyte/structure/tavern/houses/tavern_savanna.nbt` |
| `acolyte:village/snowy/tavern` | `data/acolyte/worldgen/template_pool/village/snowy/tavern.json` | `data/acolyte/structure/streets/snowy_tavern_01.nbt` | `data/acolyte/structure/tavern/tavern_snowy.nbt` | `data/acolyte/structure/tavern/houses/tavern_snowy.nbt` |

Cada pool publicado tem fallback `minecraft:empty`, um elemento `minecraft:legacy_single_pool_element`, peso **1**, projeção `rigid`, processador `minecraft:empty`; a localização é `acolyte:tavern/tavern_<bioma>`. O template de rua liga ao pool Acolyte por jigsaw `acolyte:tavern_entrance`. O template de casa é inserido diretamente no pool vanilla de casas e não acrescenta um ID configurado de estrutura.

Na inicialização do servidor, `ModVillageAddition` usa o config `tavern_placement.<bioma>.pool`: default `streets`, com peso de rua **3** e peso de casa **12**, cada peso válido em **1–100**. Destinos exatos: `minecraft:village/<bioma>/streets` e `minecraft:village/<bioma>/houses`; escolha `both` alcança ambos, `disabled` nenhum. As tags e as condições de geração da vila base continuam pertencendo a Minecraft/datapacks. Um pool de destino ausente é ignorado. A injeção acessa `StructureTemplatePool.templates` e substitui `rawTemplates`: `META-INF/accesstransformer.cfg` declara exposição pública do primeiro campo e exposição pública/remoção de final do segundo. Essa dependência de access transformer pertence ao bootstrap Acolyte; a aplicação efetiva do AT e a compatibilidade desses campos no host/pack montado permanecem `NOT_VERIFIED`. Os acessos aparecem em `addBuildingToPool` nos PCs 60, 81 e 115. Detalhes dos quinze knobs reais em [placement](../config/village-tavern-placement.md) e [weights](../config/village-tavern-weights.md).

| Variante | Marcadores nos templates principal e casa, por template | Containers e loot vanilla por template |
| --- | --- | --- |
| Plains | 1 `acolyte:tavern_spawn_marker_oak` | 1 `minecraft:chests/village/village_butcher`; 2 `minecraft:chests/village/village_plains_house` |
| Desert | 4 `acolyte:tavern_spawn_marker_sandstone` | 1 `minecraft:chests/village/village_butcher`; 3 `minecraft:chests/village/village_desert_house` |
| Taiga | 1 `acolyte:tavern_spawn_marker_cobblestone` | 1 `minecraft:chests/village/village_butcher`; 2 `minecraft:chests/village/village_taiga_house` |
| Savanna | 1 `acolyte:tavern_spawn_marker_acacia` | 1 `minecraft:chests/village/village_butcher`; 2 `minecraft:chests/village/village_savanna_house` |
| Snowy | 1 `acolyte:tavern_spawn_marker_spruce` | 1 `minecraft:chests/village/village_butcher`; 2 `minecraft:chests/village/village_snowy_house` |

Os templates de rua não contêm marcador nem container de loot; os corpos de tavern e suas versões casa contêm os [Tavern spawn markers](tavern-spawn-markers.md), responsáveis por humanos aleatórios e oportunidade de recrutamento. Não há spell ID ou pool de scroll Acolyte fixado por esses corpos de tavern. O número de marcadores Desert não garante 16 humanos: cada marcador conta apenas magos no mesmo alcance e os demais gates continuam ativos.

**Evidência exata:** os quinze NBTs e cinco pools da primeira tabela; `net/raptorzizi/acolyte/worldgen/ModVillageAddition.class`, `addNewVillageBuilding(Lnet/neoforged/neoforge/event/server/ServerStartingEvent;)V` PCs 44–261 (plains 44–85, desert 88–129, taiga 132–173, savanna 176–217, snowy 220–261), `addTavern(Lnet/minecraft/core/Registry;Lnet/minecraft/core/Registry;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;II)V` PCs 120–196; `addBuildingToPool(Lnet/minecraft/core/Registry;Lnet/minecraft/core/Registry;Lnet/minecraft/resources/ResourceLocation;Ljava/lang/String;I)V` PCs 0–118. A ligação de evento é confirmada por `@SubscribeEvent` em `addNewVillageBuilding` e `@EventBusSubscriber` na classe; `javap -v`, BootstrapMethods #0/#1, confirma `minecraft:village/\u0001/streets` e `minecraft:village/\u0001/houses`. Os IDs exatos dos destinos vanilla também constam dessas concatenações; os caminhos de templates estão nos PCs 48–50, 92–94, 136–138, 180–182 e 224–226.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
