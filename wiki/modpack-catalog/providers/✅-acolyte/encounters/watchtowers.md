# Watchtowers — Acolyte 1.0.3

Todas as variantes desta ficha usam estrutura `minecraft:jigsaw`, etapa `surface_structures`, tamanho jigsaw **1**, altura inicial absoluta **0** projetada em `WORLD_SURFACE_WG`, `spawn_overrides` vazio e expansion hack desativado. Os start pools usam um elemento `minecraft:single_pool_element`, peso **1**, projeção `rigid`, processadores `minecraft:empty` e fallback `minecraft:empty`. Esses parâmetros descrevem geração, não um cast.

Sete configurações e sete sets separados preservam as variantes de bioma. Cada set tem uma entrada de peso **1**, placement `minecraft:random_spread`, **spacing 70**, **separation 40** (chunks); a distância máxima do centro de cada estrutura é **16 blocos**.

| ID da estrutura / start pool / template | Configuração exata | Pool exato | Template exato | Salt do set |
| --- | --- | --- | --- | --- |
| `acolyte:watchtower/acacia_watchtower` | `data/acolyte/worldgen/structure/watchtower/acacia_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/acacia_watchtower.json` | `data/acolyte/structure/watchtower/acacia_watchtower.nbt` | 512847639 |
| `acolyte:watchtower/birch_watchtower` | `data/acolyte/worldgen/structure/watchtower/birch_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/birch_watchtower.json` | `data/acolyte/structure/watchtower/birch_watchtower.nbt` | 723849561 |
| `acolyte:watchtower/dark_oak_watchtower` | `data/acolyte/worldgen/structure/watchtower/dark_oak_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/dark_oak_watchtower.json` | `data/acolyte/structure/watchtower/dark_oak_watchtower.nbt` | 619283745 |
| `acolyte:watchtower/jungle_watchtower` | `data/acolyte/worldgen/structure/watchtower/jungle_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/jungle_watchtower.json` | `data/acolyte/structure/watchtower/jungle_watchtower.nbt` | 408572916 |
| `acolyte:watchtower/mangrove_watchtower` | `data/acolyte/worldgen/structure/watchtower/mangrove_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/mangrove_watchtower.json` | `data/acolyte/structure/watchtower/mangrove_watchtower.nbt` | 304918527 |
| `acolyte:watchtower/oak_watchtower` | `data/acolyte/worldgen/structure/watchtower/oak_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/oak_watchtower.json` | `data/acolyte/structure/watchtower/oak_watchtower.nbt` | 947382615 |
| `acolyte:watchtower/spruce_watchtower` | `data/acolyte/worldgen/structure/watchtower/spruce_watchtower.json` | `data/acolyte/worldgen/template_pool/watchtower/spruce_watchtower.json` | `data/acolyte/structure/watchtower/spruce_watchtower.nbt` | 836472910 |

O caminho de cada set é `data/acolyte/worldgen/structure_set/<material>_watchtower.json`; o biome tag de cada linha abaixo vem de `data/acolyte/tags/worldgen/biome/has_<material>_watchtower.json`.

| Tag selecionada pela estrutura | Biomas declarados |
| --- | --- |
| `#acolyte:has_acacia_watchtower` | `minecraft:savanna`, `minecraft:savanna_plateau`, `minecraft:windswept_savanna` |
| `#acolyte:has_birch_watchtower` | `minecraft:birch_forest`, `minecraft:old_growth_birch_forest` |
| `#acolyte:has_dark_oak_watchtower` | `minecraft:dark_forest` |
| `#acolyte:has_jungle_watchtower` | `minecraft:jungle`, `minecraft:sparse_jungle`, `minecraft:bamboo_jungle` |
| `#acolyte:has_mangrove_watchtower` | `minecraft:mangrove_swamp`, `minecraft:swamp` |
| `#acolyte:has_oak_watchtower` | `minecraft:plains`, `minecraft:sunflower_plains`, `minecraft:forest`, `minecraft:flower_forest` |
| `#acolyte:has_spruce_watchtower` | `minecraft:taiga`, `minecraft:snowy_taiga`, `minecraft:snowy_plains`, `minecraft:old_growth_pine_taiga`, `minecraft:old_growth_spruce_taiga`, `minecraft:grove`, `minecraft:snowy_slopes` |

Cada NBT registra um `acolyte:demon_spawn_marker_<material>`, `spawnCount=2`, `hasSpawned=false`: **duas tentativas** de spawn aleatório archer/warrior/mage sob a regra do [marcador](demon-spawn-markers.md). Nenhuma entidade é gravada diretamente nesses sete templates. Cada um contém um container com `acolyte:chests/watchtower/<material>_watchtower`, cujo recurso está em `data/acolyte/loot_table/chests/watchtower/<material>_watchtower.json`.

As sete tabelas compartilham o acesso mágico: arcane essence como entrada ponderada na primeira pool, scrolls aleatórios de qualidade **0–0,5** em **1–2 rolagens**, condicionados a chance **0,25**; poor ink em **0–2 rolagens**; basic curios em uma rolagem com chance **0,2**. Esses são parâmetros de loot de Iron’s; a magia concreta não é fixada pelo watchtower. Ver [Chest loot](chest-loot.md).

**Evidência exata:** sete trios de caminhos da tabela, sete sets, sete biome tags e sete loot tables com a substituição literal do material. São fatos de recursos consumidos pelo jigsaw host; não há necessidade de copiar template ou implementar um gerador equivalente.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
