# Castles — Acolyte 1.0.3

Todas as variantes desta ficha usam estrutura `minecraft:jigsaw`, etapa `surface_structures`, tamanho jigsaw **1**, altura inicial absoluta **0** projetada em `WORLD_SURFACE_WG`, `spawn_overrides` vazio e expansion hack desativado. Os start pools usam um elemento `minecraft:single_pool_element`, peso **1**, projeção `rigid`, processadores `minecraft:empty` e fallback `minecraft:empty`. Esses parâmetros descrevem geração, não um cast.

O conjunto `acolyte:castle`, recurso `data/acolyte/worldgen/structure_set/castle.json`, seleciona as três variantes com pesos **1/1/1**. Placement `minecraft:random_spread`: **spacing 85**, **separation 50** (chunks), salt **947261038**. Distância máxima do centro em cada configuração: **80 blocos**.

| ID da estrutura / start pool / template | Configuração exata | Pool exato | Template exato | Marcadores no template |
| --- | --- | --- | --- | --- |
| `acolyte:castle/castle_0` | `data/acolyte/worldgen/structure/castle/castle_0.json` | `data/acolyte/worldgen/template_pool/castle/castle_0.json` | `data/acolyte/structure/castle/castle_0.nbt` | 2 marcadores ainda ativos × spawnCount 2 = 4 tentativas |
| `acolyte:castle/castle_1` | `data/acolyte/worldgen/structure/castle/castle_1.json` | `data/acolyte/worldgen/template_pool/castle/castle_1.json` | `data/acolyte/structure/castle/castle_1.nbt` | 3 ativos com contagens 3/1/1 = 5 tentativas; 1 já hasSpawned=true |
| `acolyte:castle/castle_2` | `data/acolyte/worldgen/structure/castle/castle_2.json` | `data/acolyte/worldgen/template_pool/castle/castle_2.json` | `data/acolyte/structure/castle/castle_2.nbt` | 2 ativos com contagens 3/2 = 5 tentativas; 1 já hasSpawned=true |

O biome selector é `#acolyte:has_castle`, definido em `data/acolyte/tags/worldgen/biome/has_castle.json` com `replace=false`: `#minecraft:is_forest`, `#minecraft:is_hill`, `#minecraft:is_taiga`, `minecraft:snowy_plains`, `#c:is_plains`, `minecraft:savanna`, `minecraft:savanna_plateau`, `minecraft:windswept_savanna`, `minecraft:meadow`. As tags referidas são dependências abertas à composição de datapacks.

Os [Demon spawn markers](demon-spawn-markers.md) fornecem o encontro e respeitam a gamerule de estrutura; as contagens acima são tentativas potenciais do estado salvo do template, não spawn garantido nem número de magos. Nenhuma entidade está gravada diretamente nestes três NBTs.

| Template | Referências de aquisição de loot e quantidade de containers |
| --- | --- |
| `castle_0` | `acolyte:chests/generic/consumables` ×1; `irons_spellbooks:chests/filler_storage_loot` ×3; `irons_spellbooks:chests/component_storage` ×1; `irons_spellbooks:chests/bookshelf_loot` ×2 |
| `castle_1` | `acolyte:chests/castle/castle_loot_magic` ×1; `irons_spellbooks:chests/filler_storage_loot` ×4; `acolyte:chests/generic/consumables` ×1; `acolyte:chests/castle/castle_loot` ×2 |
| `castle_2` | `acolyte:chests/castle/castle_loot_magic_rare` ×1; `acolyte:chests/generic/consumables` ×1; `irons_spellbooks:chests/bookshelf_loot` ×1; `irons_spellbooks:chests/filler_storage_loot` ×2; `irons_spellbooks:chests/component_storage` ×1; `acolyte:chests/castle/castle_loot` ×1 |

As tabelas `castle_loot_magic` / `castle_loot_magic_rare` distribuem recursos e scrolls de Iron’s, sem fixar uma magia Acolyte; detalhes em [Chest loot](chest-loot.md). O castelo 0 referencia loot host diretamente, apesar de não conter uma tabela Acolyte com `magic` em seu nome.

**Evidência exata:** caminhos da tabela, `data/acolyte/worldgen/structure_set/castle.json` e `data/acolyte/tags/worldgen/biome/has_castle.json`; os parâmetros e relações foram resumidos do publisher. Não há método Java de geração de castelo Acolyte a atribuir: o codec `minecraft:jigsaw` é o consumidor do recurso. O comportamento dos marcadores tem descritores/PCs em sua ficha.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
