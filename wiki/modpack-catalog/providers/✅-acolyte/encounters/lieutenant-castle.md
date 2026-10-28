# Lieutenant castle — Acolyte 1.0.3

Todas as variantes desta ficha usam estrutura `minecraft:jigsaw`, etapa `surface_structures`, tamanho jigsaw **1**, altura inicial absoluta **0** projetada em `WORLD_SURFACE_WG`, `spawn_overrides` vazio e expansion hack desativado. Os start pools usam um elemento `minecraft:single_pool_element`, peso **1**, projeção `rigid`, processadores `minecraft:empty` e fallback `minecraft:empty`. Esses parâmetros descrevem geração, não um cast.

**ID de estrutura e start pool:** `acolyte:lieutenant_castle/lieutenant_castle`. Distância máxima do centro: **80 blocos**.

| Superfície | Caminho exato no archive |
| --- | --- |
| Estrutura | `data/acolyte/worldgen/structure/lieutenant_castle/lieutenant_castle.json` |
| Start pool | `data/acolyte/worldgen/template_pool/lieutenant_castle/lieutenant_castle.json` |
| Template selecionado | `data/acolyte/structure/lieutnant_castle/lieutnant_castle.nbt` |
| Structure set | `data/acolyte/worldgen/structure_set/lieutenant_castle.json` |
| Biome tag | `data/acolyte/tags/worldgen/biome/has_lieutenant_castle.json` |

A grafia **`lieutnant_castle`** é real no template; não normalizar para o caminho da estrutura. O pool aponta para `acolyte:lieutnant_castle/lieutnant_castle`. O set tem uma entrada de peso **1**, placement **`minecraft:concentric_rings`**, distance **64**, spread **40**, count **10**, salt **612748391**, preferred biomes `#acolyte:has_lieutenant_castle`. Não é um random-spread com spacing/separation e count 10 é parâmetro da geração em anéis, não dez mobs por prédio.

A tag tem `replace=false` e os valores `#minecraft:is_forest`, `#minecraft:is_hill`, `#minecraft:is_taiga`, `minecraft:snowy_plains`, `#c:is_plains`, `minecraft:savanna`, `minecraft:savanna_plateau`, `minecraft:windswept_savanna`, `minecraft:meadow`.

O template registra **um `acolyte:lieutenant`** e um armor stand, além de **três demon markers ativos** com `spawnCount` 4/1/1: seis tentativas adicionais de escolha archer/warrior/mage pelos [marcadores](demon-spawn-markers.md). A gamerule do marcador não demonstra veto à entidade Lieutenant já gravada no template. Não somar esses registros a novos IDs de estrutura.

**Aquisição por containers do NBT:** `acolyte:chests/castle/castle_loot_magic_rare` ×1; `acolyte:chests/castle/castle_loot` ×2; `irons_spellbooks:chests/filler_storage_loot` ×4; `minecraft:chests/village/village_fletcher` ×1; `irons_spellbooks:chests/component_storage` ×1. `castle_loot_magic_rare` fornece scrolls de qualidade 0,3–0,8 segundo o recurso; ver [Chest loot](chest-loot.md). Loot do boss é superfície distinta do loot dos containers.

**Evidência exata:** cinco caminhos da tabela; leitura factual das referências e parâmetros do publisher. Não há gerador Java Acolyte específico demonstrado: o consumidor da configuração é o codec host `minecraft:jigsaw`.

## Limite de integração e QA

Acolyte controla este contexto de encontro/configuração; Iron’s mantém a identidade e resolução das magias, scrolls e recompensas de seu namespace. A observação do JAR não valida um ponto mutador para Black Arcana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não foi comprovada igualdade de hash com o JAR instalado. Esta ficha resume fatos de interoperabilidade, sem reproduzir implementação, NBT ou assets.

**Base:** publisher `acolyte-1.0.3.jar`, CurseForge file `8098233`, SHA-1 `ad0abc821f3f8a6573ac19a50970fc1bc46b4275`; [contratos binários](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).
