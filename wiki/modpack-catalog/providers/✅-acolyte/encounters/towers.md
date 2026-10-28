# Towers — Acolyte 1.0.3

Todas as variantes desta ficha usam estrutura `minecraft:jigsaw`, etapa `surface_structures`, tamanho jigsaw **1**, altura inicial absoluta **0** projetada em `WORLD_SURFACE_WG`, `spawn_overrides` vazio e expansion hack desativado. Os start pools usam um elemento `minecraft:single_pool_element`, peso **1**, projeção `rigid`, processadores `minecraft:empty` e fallback `minecraft:empty`. Esses parâmetros descrevem geração, não um cast.

O conjunto `acolyte:tower`, `data/acolyte/worldgen/structure_set/tower.json`, escolhe as duas variantes com pesos **1/1**. Placement `minecraft:random_spread`: **spacing 60**, **separation 35** (chunks), salt **183650294**. Distância máxima do centro: **16 blocos**.

| ID da estrutura / start pool / template | Configuração exata | Pool exato | Template exato |
| --- | --- | --- | --- |
| `acolyte:tower/tower_0` | `data/acolyte/worldgen/structure/tower/tower_0.json` | `data/acolyte/worldgen/template_pool/tower/tower_0.json` | `data/acolyte/structure/tower/tower_0.nbt` |
| `acolyte:tower/tower_1` | `data/acolyte/worldgen/structure/tower/tower_1.json` | `data/acolyte/worldgen/template_pool/tower/tower_1.json` | `data/acolyte/structure/tower/tower_1.nbt` |

Biome selector `#acolyte:has_tower`, definido em `data/acolyte/tags/worldgen/biome/has_tower.json`, `replace=false`: `#minecraft:is_forest`, `#minecraft:is_hill`, `#minecraft:is_taiga`, `minecraft:snowy_plains`, `#c:is_plains`.

Ambos os templates registram três [Demon spawn markers](demon-spawn-markers.md) ativos com contagens 2/1/1: **quatro tentativas** de geração aleatória por torre. Não há entidade diretamente gravada nesses NBTs. A distribuição de especializações pertence aos marcadores, não à variante geométrica.

| Template | Referências de aquisição e containers |
| --- | --- |
| `tower_0` | `acolyte:chests/generic/beetroot` ×1; `acolyte:chests/tower/tower_loot` ×1; `acolyte:chests/tower/tower_loot_magic` ×1 |
| `tower_1` | `acolyte:chests/generic/prison` ×1; `acolyte:chests/generic/consumables` ×2; `acolyte:chests/tower/tower_loot` ×1 |

O tower 0 expõe `tower_loot_magic`, com scroll aleatório host condicionado a uma chance de 0,4; o tower 1 expõe `generic/prison`, que pode selecionar scroll ou curios host em sua segunda rolagem. Ambos expõem loot comum com possível poor ink. Os parâmetros relevantes ficam em [Chest loot](chest-loot.md).

**Evidência exata:** caminhos da tabela, set e biome tag acima. Os recursos são consumidos pelo jigsaw host; os caminhos Java do marcador são documentados na ficha da família.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
