# Goety Cataclysm 1.21.1-1.8.2 — 48 receitas rituais do JAR exato

✅ **48/48 paths comprovados**: 24 aquisições de Focus deduplicadas e 24 rituais não-Focus, classificação `COUNTED_EXACT`. Esta individualização acrescenta **+0 novas identidades semânticas**.

## Prova de procedência

Artefato instalado/publisher: `goety_cataclysm-1.21.1-1.8.2.jar`, mod ID `goety_cataclysm`, SHA-1 `4e3052a082200371b36e1a88fdce05e294d82757`; tamanho da cópia verificada: **1755990 bytes**. CurseForge projeto `1224214`, arquivo `8518940`; modlist sibling `main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`, posição física #306. A auditoria original NON-MERGE [PR #206](https://github.com/Gustavaopere/Black-Arcana/pull/206) já provava 28 Focus + 24 rituais distintos.

A reextração [GitHub Actions #38190078609](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38190078609) no audit commit NON-MERGE `449444fc897659bb3ab2506ff61c5b1920aa4148` confirmou o **hash antes de emitir as 48 linhas textuais** `RITUAL_ROW`. Cada item é recipe `goety:ritual`; a coluna `ritual_type` é subtipo, não um novo ID de spell. Nenhum JAR, bytecode, asset ou JSON integral de receita upstream foi incorporado.

| # | Path literal do JAR | `ritual_type` | `result_ids` literal | Outcome semântico | Conditions de topo | Contagem |
|---:|---|---|---|---|---|---|
| 1 | `data/goety_cataclysm/recipe/convert_blazes_to_ignited_berserker.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:ignited_berserker` | `[]` | `COUNTED_EXACT` |
| 2 | `data/goety_cataclysm/recipe/convert_deepling_servant_to_deepling_brute.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:deepling_brute_servant` | `[]` | `COUNTED_EXACT` |
| 3 | `data/goety_cataclysm/recipe/convert_deepling_servant_to_deepling_priest.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:deepling_priest_servant` | `[]` | `COUNTED_EXACT` |
| 4 | `data/goety_cataclysm/recipe/convert_deepling_servant_to_deepling_warlock.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:deepling_warlock_servant` | `[]` | `COUNTED_EXACT` |
| 5 | `data/goety_cataclysm/recipe/convert_draugr_to_draugr_necromancer.json` | `goety:convert_complete_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:draugr_necromancer_servant` | `[]` | `COUNTED_EXACT` |
| 6 | `data/goety_cataclysm/recipe/convert_drowned_servant_to_drowned_host.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:drowned_host_servant` | `[]` | `COUNTED_EXACT` |
| 7 | `data/goety_cataclysm/recipe/convert_koboleton_to_kobolediator_servant.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:kobolediator` | `[]` | `COUNTED_EXACT` |
| 8 | `data/goety_cataclysm/recipe/convert_koboleton_to_wadjet_servant.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:wadjet` | `[]` | `COUNTED_EXACT` |
| 9 | `data/goety_cataclysm/recipe/convert_modern_remnant_to_ancient_remnant_servant.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:ancient_remnant` | `[]` | `COUNTED_EXACT` |
| 10 | `data/goety_cataclysm/recipe/convert_wildfire_to_ignited_revenant.json` | `goety:convert_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:ignited_revenant` | `[]` | `COUNTED_EXACT` |
| 11 | `data/goety_cataclysm/recipe/fabricator.json` | `goety:craft` | `goety_cataclysm:fabricator` | `goety_cataclysm:fabricator` | `[]` | `COUNTED_EXACT` |
| 12 | `data/goety_cataclysm/recipe/focus/abyssal_beam_focus.json` | `goety:craft` | `goety_cataclysm:abyssal_beam_focus` | `goety_cataclysm:abyssal_beam_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 13 | `data/goety_cataclysm/recipe/focus/abyssal_mine_focus.json` | `goety:craft` | `goety_cataclysm:abyssal_mine_focus` | `goety_cataclysm:abyssal_mine_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 14 | `data/goety_cataclysm/recipe/focus/abyssal_orb_focus.json` | `goety:craft` | `goety_cataclysm:abyssal_orb_focus` | `goety_cataclysm:abyssal_orb_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 15 | `data/goety_cataclysm/recipe/focus/battlefield_focus.json` | `goety:craft` | `goety_cataclysm:battlefield_focus` | `goety_cataclysm:battlefield_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 16 | `data/goety_cataclysm/recipe/focus/cursed_cairn_focus.json` | `goety:craft` | `goety_cataclysm:cursed_cairn_focus` | `goety_cataclysm:cursed_cairn_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 17 | `data/goety_cataclysm/recipe/focus/cursed_grave_focus.json` | `goety:craft` | `goety_cataclysm:cursed_grave_focus` | `goety_cataclysm:cursed_grave_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 18 | `data/goety_cataclysm/recipe/focus/cursed_tomb_focus.json` | `goety:craft` | `goety_cataclysm:cursed_tomb_focus` | `goety_cataclysm:cursed_tomb_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 19 | `data/goety_cataclysm/recipe/focus/death_laser_focus.json` | `goety:craft` | `goety_cataclysm:death_laser_focus` | `goety_cataclysm:death_laser_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 20 | `data/goety_cataclysm/recipe/focus/desert_crush_focus.json` | `goety:craft` | `goety_cataclysm:desert_crush_focus` | `goety_cataclysm:desert_crush_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 21 | `data/goety_cataclysm/recipe/focus/desert_raid_focus.json` | `goety:craft` | `goety_cataclysm:desert_raid_focus` | `goety_cataclysm:desert_raid_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 22 | `data/goety_cataclysm/recipe/focus/earth_shake_focus.json` | `goety:craft` | `goety_cataclysm:earth_shake_focus` | `goety_cataclysm:earth_shake_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 23 | `data/goety_cataclysm/recipe/focus/extinct_flame_focus.json` | `goety:craft` | `goety_cataclysm:extinct_flame_focus` | `goety_cataclysm:extinct_flame_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 24 | `data/goety_cataclysm/recipe/focus/flare_bomb_focus.json` | `goety:craft` | `goety_cataclysm:flare_bomb_focus` | `goety_cataclysm:flare_bomb_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 25 | `data/goety_cataclysm/recipe/focus/kakourgos_focus.json` | `goety:craft` | `goety_cataclysm:kakourgos_focus` | `goety_cataclysm:kakourgos_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 26 | `data/goety_cataclysm/recipe/focus/kyria_focus.json` | `goety:craft` | `goety_cataclysm:kyria_focus` | `goety_cataclysm:kyria_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 27 | `data/goety_cataclysm/recipe/focus/lightning_spear_focus.json` | `goety:craft` | `goety_cataclysm:lightning_spear_focus` | `goety_cataclysm:lightning_spear_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 28 | `data/goety_cataclysm/recipe/focus/polemistis_focus.json` | `goety:craft` | `goety_cataclysm:polemistis_focus` | `goety_cataclysm:polemistis_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 29 | `data/goety_cataclysm/recipe/focus/sandstorm_focus.json` | `goety:craft` | `goety_cataclysm:sandstorm_focus` | `goety_cataclysm:sandstorm_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 30 | `data/goety_cataclysm/recipe/focus/storm_serpent_focus.json` | `goety:craft` | `goety_cataclysm:storm_serpent_focus` | `goety_cataclysm:storm_serpent_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 31 | `data/goety_cataclysm/recipe/focus/sunken_current_focus.json` | `goety:craft` | `goety_cataclysm:sunken_current_focus` | `goety_cataclysm:sunken_current_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 32 | `data/goety_cataclysm/recipe/focus/sunken_swell_focus.json` | `goety:craft` | `goety_cataclysm:sunken_swell_focus` | `goety_cataclysm:sunken_swell_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 33 | `data/goety_cataclysm/recipe/focus/sunken_tribune_focus.json` | `goety:craft` | `goety_cataclysm:sunken_tribune_focus` | `goety_cataclysm:sunken_tribune_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 34 | `data/goety_cataclysm/recipe/focus/thunder_rage_focus.json` | `goety:craft` | `goety_cataclysm:thunder_rage_focus` | `goety_cataclysm:thunder_rage_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 35 | `data/goety_cataclysm/recipe/focus/void_vortex_focus.json` | `goety:craft` | `goety_cataclysm:void_vortex_focus` | `goety_cataclysm:void_vortex_focus` | `[]` | `FOCUS_ACQUISITION_DEDUP` |
| 36 | `data/goety_cataclysm/recipe/thrall/summon_aptrgangr_servant.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:aptrgangr` | `[]` | `COUNTED_EXACT` |
| 37 | `data/goety_cataclysm/recipe/thrall/summon_cindaria_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:cindaria_servant` | `[]` | `COUNTED_EXACT` |
| 38 | `data/goety_cataclysm/recipe/thrall/summon_clawdian_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:clawdian` | `[]` | `COUNTED_EXACT` |
| 39 | `data/goety_cataclysm/recipe/thrall/summon_deepling_angler_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:deepling_angler_servant` | `[]` | `COUNTED_EXACT` |
| 40 | `data/goety_cataclysm/recipe/thrall/summon_deepling_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:deepling_servant` | `[]` | `COUNTED_EXACT` |
| 41 | `data/goety_cataclysm/recipe/thrall/summon_draugr_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:draugr_servant` | `[]` | `COUNTED_EXACT` |
| 42 | `data/goety_cataclysm/recipe/thrall/summon_elite_draugr_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:elite_draugr_servant` | `[]` | `COUNTED_EXACT` |
| 43 | `data/goety_cataclysm/recipe/thrall/summon_hippocamtus_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:hippocamtus` | `[]` | `COUNTED_EXACT` |
| 44 | `data/goety_cataclysm/recipe/thrall/summon_koboleton_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:koboleton_servant` | `[]` | `COUNTED_EXACT` |
| 45 | `data/goety_cataclysm/recipe/thrall/summon_prowler_servant.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:the_prowler` | `[]` | `COUNTED_EXACT` |
| 46 | `data/goety_cataclysm/recipe/thrall/summon_royal_draugr_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:royal_draugr_servant` | `[]` | `COUNTED_EXACT` |
| 47 | `data/goety_cataclysm/recipe/thrall/summon_urchinkin_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:urchinkin_servant` | `[]` | `COUNTED_EXACT` |
| 48 | `data/goety_cataclysm/recipe/thrall/summon_zombie_amethyst_crab_servant_thrall.json` | `goety:summon_tamed` | `goety:jei_dummy/none` | `goety_cataclysm:zombie_amethyst_crab` | `[]` | `COUNTED_EXACT` |

## Deduplicação e classificação

- **24** Focus acquisition recipes `goety:craft` do tipo primário `goety:ritual` pertencem a **24 holders já contados** e não geram identidades mágicas extras.
- **24** não-Focus têm outcomes distintos: **10 conversões** (9 `goety:convert_tamed`, 1 `goety:convert_complete_tamed`), **13 invocações/thralls** (`goety:summon_tamed`), **1 fabricator** (`goety:craft`).
- `goety:jei_dummy/none` representa placeholder para exibição de resultado de conversão/summon, **não é uma recompensa nem o destino da transformação**.
- Os outros **4 Focuses** (sem caminho ritual nesta matriz) são `AMETHYST_CLUSTER_FOCUS`, `ASHEN_BREATH_FOCUS`, `VOID_RUNE_FOCUS`, `WATER_SPEAR_FOCUS`. Sua atribuição a crafting comum ocorre **por exclusão controlada** do split 28 Focus = 24 ritual + 4 crafting já provado. Não há aqui prova de seus recipe paths de crafting normal.
- `conditions=[]` indica somente a ausência de condições de topo reconhecidas pelo scanner. Não garante viabilidade em Survival nem ausência de custos.
- No ledger, permanece **28 Focus + 24 rituais = 52**. Mínimos **1851 global / 1849 escopo** inalterados, denominador final aberto; **+0 novas identidades semânticas**.

## Limites de execução

**⚠️** Não verificados ingredientes, tempo, altar, Soul Energy, progressão, entidades de origem, parâmetros de spawn, config efetiva, multiplayer, save/restart e QA físico Survival. **⛔** Não inventar hooks/APIs nem duplicar runtime de Goety, Cataclysm ou Black Arcana. Licença ARR: clean-room estrito.

[24 fichas individuais](RITUAL-CARDS-1.21.1-1.8.2.md) · [README](README.md) · [auditoria física](EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md).
