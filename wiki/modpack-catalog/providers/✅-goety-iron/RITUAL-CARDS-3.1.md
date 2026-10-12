# Goety Iron 3.1 — 12 fichas de rituais não-Focus

**✅ 12/12 fichas nominais `COUNTED_EXACT` individualizadas** usando os 14 paths e outcomes reextraídos do publisher JAR hash-matched (SHA-1 `c8529867e798661ed01fb2948abda23735888fc6`). [Matriz factual completa](RITUAL-INVENTORY-EXACT-3.1.md) · [workflow de reauditoria #38186445480](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38186445480).

As receitas têm type `goety:ritual`, **10** subtipos `goety:convert_complete_tamed` e **2** subtipos `goety:craft` que não são Focus. As duas outras receitas `goety:craft` produzem Focuses já contados, portanto não possuem nova ficha de ritual.

| # | Resource path / stem literal | `ritual_type` | Outcome exato | Ficha |
|---:|---|---|---|---|
| 1 | `convert_icespider_to_frostgiantspider` | `goety:convert_complete_tamed` | `goetyiron:frost_giant_spider_servant` | [Abrir](rituals/convert_icespider_to_frostgiantspider.md) |
| 2 | `convert_illager_to_archevoker` | `goety:convert_complete_tamed` | `goetyiron:archevoker_servant` | [Abrir](rituals/convert_illager_to_archevoker.md) |
| 3 | `convert_illager_to_cryomancer` | `goety:convert_complete_tamed` | `goetyiron:cryomancer_servant` | [Abrir](rituals/convert_illager_to_cryomancer.md) |
| 4 | `convert_illager_to_cultist` | `goety:convert_complete_tamed` | `goetyiron:cultist_servant` | [Abrir](rituals/convert_illager_to_cultist.md) |
| 5 | `convert_illager_to_pyromancer` | `goety:convert_complete_tamed` | `goetyiron:pyromancer_servant` | [Abrir](rituals/convert_illager_to_pyromancer.md) |
| 6 | `convert_knight_to_fireboss` | `goety:convert_complete_tamed` | `goetyiron:fire_boss_servant` | [Abrir](rituals/convert_knight_to_fireboss.md) |
| 7 | `convert_piglin_to_alchemist_servant` | `goety:convert_complete_tamed` | `goetyiron:alchemist_servant` | [Abrir](rituals/convert_piglin_to_alchemist_servant.md) |
| 8 | `convert_villager_to_heretic` | `goety:convert_complete_tamed` | `goety:heretic_servant` | [Abrir](rituals/convert_villager_to_heretic.md) |
| 9 | `convert_villager_to_priest` | `goety:convert_complete_tamed` | `goetyiron:priest_servant` | [Abrir](rituals/convert_villager_to_priest.md) |
| 10 | `hemolytic_ring` | `goety:craft` | `goetyiron:hemolytic_ring` | [Abrir](rituals/hemolytic_ring.md) |
| 11 | `rotten_spell_book` | `goety:craft` | `irons_spellbooks:rotten_spell_book` | [Abrir](rituals/rotten_spell_book.md) |
| 12 | `summon_dead_king_servant` | `goety:convert_complete_tamed` | `goetyiron:deadking_servant` | [Abrir](rituals/summon_dead_king_servant.md) |

## Contagem e limites

- **✅ 14/14** resource paths em [RITUAL-INVENTORY-EXACT-3.1.md](RITUAL-INVENTORY-EXACT-3.1.md): **12 não-Focus** individualizados e **2 Focus-acquisition** deduplicados (consulte [FOCUS-CARDS-3.1.md](FOCUS-CARDS-3.1.md)).
- `goety:jei_dummy/none` é **placeholder** em `result_ids` das 10 conversões, não é outcome nem identidade extra; o destino real está no campo semântico da recipe.
- Todos os 14 top-level conditions retornaram `[]` no scanner auditado; isso não certifica custos ou possibilidade efetiva em Survival.
- **+0 novas identidades semânticas**: Goety Iron permanece com **14** no ledger (**2 Focuses + 12 rituais**), globais mínimos **1.851 / 1.849** inalterados.
- **⚠️ QA não realizado:** custos/Soul, mob de origem, conteúdo detalhado de receitas, config habilitada, categoria/dimensão, settlement, ownership, save/restart, multiplayer e Survival. **⛔** sem hook/API seguro, não fazer integração runtime; nenhuma nova magia BA criada.

Clean-room: esta árvore armazena apenas path, subtype, ID e fatos de outcome, nunca JAR/recipe JSON/bytecode/assets upstream.
