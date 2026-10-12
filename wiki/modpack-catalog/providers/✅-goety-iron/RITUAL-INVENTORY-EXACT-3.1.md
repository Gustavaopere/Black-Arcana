# Goety Iron 3.1 — matriz nominal de rituais do JAR exato

Status: **✅ 14/14 resource paths verificados**, **✅ 12/12 rituais não-Focus distintos**, **✅ 2/2 receitas de Focus deduplicadas** · `COUNTED_EXACT` · **+0 novas identidades** nesta individualização.

## Proveniência reproduzível

- Mod ID: `goetyiron`; runtime `3.1`; JAR `GoetyIron-1.21.1-NeoForge-3.1.jar`.
- SHA-1 do artefato publisher idêntico ao snapshot físico: `c8529867e798661ed01fb2948abda23735888fc6`; tamanho factual: `507646` bytes.
- CurseForge: projeto `1367643`, arquivo `8662179`; Modrinth `tZpynDu5 / YZXNIxvk`.
- Auditoria original NON-MERGE [PR #205](https://github.com/Gustavaopere/Black-Arcana/pull/205), com cardinalidade 14/2/12.
- **Reauditoria** no [workflow #38186445480](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38186445480) a partir da branch isolada `audit/goety-iron-3.1-ritual-identities-20261011`, commit `474f17eda068883629b9017eaf5c6f37ae980e0e`. O job validou hash exato antes de emitir 14 `RITUAL_ROW` text-only. Nenhum JAR, receita JSON integral, bytecode, asset ou corpo de source de terceiros é commitado.
- `goety:ritual` é o **tipo de recipe** em todas as 14 entradas. A coluna de subtipo corresponde ao campo `ritual_type`, não a novo spell registry.

## Matriz íntegra de resource path → outcome

| # | Resource path literal | `ritual_type` | `result_ids` literal | Outcome semanticamente identificado | Condições top-level | Disposição |
|---:|---|---|---|---|---|---|
| 1 | `data/goetyiron/recipe/convert_icespider_to_frostgiantspider.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:frost_giant_spider_servant` | `[]` | `COUNTED_EXACT` |
| 2 | `data/goetyiron/recipe/convert_illager_to_archevoker.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:archevoker_servant` | `[]` | `COUNTED_EXACT` |
| 3 | `data/goetyiron/recipe/convert_illager_to_cryomancer.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:cryomancer_servant` | `[]` | `COUNTED_EXACT` |
| 4 | `data/goetyiron/recipe/convert_illager_to_cultist.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:cultist_servant` | `[]` | `COUNTED_EXACT` |
| 5 | `data/goetyiron/recipe/convert_illager_to_pyromancer.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:pyromancer_servant` | `[]` | `COUNTED_EXACT` |
| 6 | `data/goetyiron/recipe/convert_knight_to_fireboss.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:fire_boss_servant` | `[]` | `COUNTED_EXACT` |
| 7 | `data/goetyiron/recipe/convert_piglin_to_alchemist_servant.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:alchemist_servant` | `[]` | `COUNTED_EXACT` |
| 8 | `data/goetyiron/recipe/convert_villager_to_heretic.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goety:heretic_servant` | `[]` | `COUNTED_EXACT` |
| 9 | `data/goetyiron/recipe/convert_villager_to_priest.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:priest_servant` | `[]` | `COUNTED_EXACT` |
| 10 | `data/goetyiron/recipe/fiery_focus.json` | `goety:craft` | `goetyiron:fiery_focus` | `goetyiron:fiery_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 11 | `data/goetyiron/recipe/hemolytic_ring.json` | `goety:craft` | `goetyiron:hemolytic_ring` | `goetyiron:hemolytic_ring` | `[]` | `COUNTED_EXACT` |
| 12 | `data/goetyiron/recipe/rotten_spell_book.json` | `goety:craft` | `irons_spellbooks:rotten_spell_book` | `irons_spellbooks:rotten_spell_book` | `[]` | `COUNTED_EXACT` |
| 13 | `data/goetyiron/recipe/summon_dead_king_servant.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goetyiron:deadking_servant` | `[]` | `COUNTED_EXACT` |
| 14 | `data/goetyiron/recipe/tarnished_focus.json` | `goety:craft` | `goetyiron:tarnished_focus` | `goetyiron:tarnished_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |

## Deduplicação e interpretações

- **10** recipes `goety:convert_complete_tamed` usam `goety:jei_dummy/none` em `result_ids`, mas possuem destino verdadeiro no campo semântico de conversão. Este marcador **não é um resultado mágico ou item obtível** e jamais é contado como 13ª identidade.
- **2** recipes `goety:craft` não-Focus produzem `goetyiron:hemolytic_ring` e `irons_spellbooks:rotten_spell_book`, respectivamente.
- **2** recipes `goety:craft` produzem `goetyiron:fiery_focus` e `goetyiron:tarnished_focus`, respectivamente: aquisição dos **Focus holders já contados** `FIERY_FOCUS` e `TARNISHED_FOCUS`. Não acrescentam rituais independentes ao mínimo semântico.
- Todas as 14 apresentam lista `neoforge:conditions`/`conditions` **vazia/ausente na análise de topo**. Não se infere ausência de gates funcionais em payload, configuração, advancement, dependências ou run-time.
- Nenhum nome derivado do path é promovido a **registro de spell** sem prova. As identidades do catálogo são os 12 rituais empacotados, cada um vinculado a seu path e outcome.
- **Contagem permanece 2 Focuses + 12 rituais = 14 identidades**, todas já incluídas nos mínimos **1.851 global / 1.849 escopo**. Esta entrega adiciona **+0 novas identidades**.

## Limites

A matriz não prova inputs, custos, tempo, geometria, instância de mob convertida, requisitos de progressão, Soul Energy, integridade de settlement, equip ou real Survival. Goety mantém rituais/servant lifecycle e Soul Energy; Iron's mantém spells/entidades/atributos de origem; Goety Iron faz a ponte. Black Arcana não constrói outro ritual engine/servant state sem API/hook e testes causais. A divergência de licença CurseForge MIT × Modrinth ARR mantém postura clean-room estrita.

Consulte [índice das 12 fichas](RITUAL-CARDS-3.1.md) e [auditoria estrutural original](EXACT-3.1-ARTIFACT-AUDIT.md).
