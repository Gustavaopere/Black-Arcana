# Black Arcana — Catálogo Global de Magia e Feitiços

Última sincronização: 2026-09-15

Este arquivo é o índice operacional global de catalogação do projeto. A árvore canônica detalhada é `wiki/modpack-catalog/providers/`; os ledgers globais são `wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md` e `wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md`. Este índice resume esses fechamentos e separa **catalogação** de **runtime/integração**.

## Legenda obrigatória

- ✅ **Catalogado** — existe inventário/contrato de catálogo suficientemente fechado para o escopo indicado. Isso inclui providers cujo fechamento correto é **zero** objetos mágicos próprios.
- ❌ **Não catalogado** — o mod/conteúdo foi identificado, mas não existe inventário mágico fechado no Black Arcana.
- 🟡 **Em implementação** — catalogação já existe e uma implementação canônica está sendo construída em tranche ativa.
- ⚠️ **Parcial/condicionado** — existe cobertura parcial, presença/versão atual não foi revalidada, ou falta evidência suficiente para afirmar catálogo integral.
- ⛔ **Bloqueado** — catalogação não pode prosseguir sem fonte/artefato/contrato obrigatório ausente.

**Regra:** estes marcadores descrevem o estado de **catalogação**, salvo quando uma coluna diz explicitamente `Runtime`. Um provider pode estar ✅ catalogado e continuar ⚠️ em runtime, ABI, balanceamento, config efetiva ou full-pack QA.

## Snapshot de autoridade usado

- Black Arcana: `main@fc519f4649315e6ef2ed80be536fea1e41a1408d`.
- RPG Skill Tree sibling: `main@3bbd7f381df64eff8463e20068c67d76d51463fe`.
- Snapshot físico canônico registrado nos ledgers do Black Arcana: Minecraft `1.21.1`, NeoForge `21.1.248`, **595 entradas top-level**, SHA-1 da modlist `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.
- O sibling mantém `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`, como inventário versionado de integração. Ele é útil como histórico, mas **não vence** evidência física posterior do Black Arcana.
- Quando uma versão do sibling diverge de um provider já fechado contra a modlist/JAR físico mais recente, este índice usa a evidência física/canônica do Black Arcana.

## 1. Hosts mágicos principais

| Mod | Mod ID / versão física evidenciada | Estado do catálogo | Cobertura canônica | Runtime |
| --- | --- | --- | --- | --- |
| Iron's Spells 'n Spellbooks | `irons_spellbooks` — `1.21.1-3.16.3` | ✅ Catalogado | **110/110 spells base** catalogados por escola na árvore canônica. | ⚠️ Integrações/adapters e QA permanecem separados do fechamento documental. |
| Ars Nouveau | `ars_nouveau` — `1.21.1-5.13.1` | ✅ Catalogado | Modelo composicional e inventário finito de glyphs normalizados; **24/24 rituais source-pinned** com páginas individuais. Combinações arbitrárias de glyphs não são enumeradas como spells fixos. | ⚠️ Config/runtime/full-pack QA continua separado. |
| Eidolon: Repraised | `eidolon_repraised` — `1.21.1-0.5.0.2` | ✅ Catalogado | **20/20** registry entries de spell, **18/18** chants oficiais, **4/4** conversions, **10/10** prototypes genéricos, **24/24** receitas rituais oficiais e **16/16** research keys inventariados. | ⚠️ Byte-equality, settlement ambíguo, survival reachability e runtime QA pendentes onde documentado. |
| Malum | `malum` — `1.21.1-1.8.2` | ✅ Catalogado | **26 Spirit Rites** semanticamente aditivos fechados no intervalo 1.8.2; **37 Geas effect types** e **9 SpiritArcanaType** inventariados como superfícies não aditivas ao contador semântico. | ⚠️ Runtime/API/recipes e conflito de licença permanecem gates separados. |

## 2. Addons/providers com spell/magic explícito

Uma linha recebe ✅ quando o escopo mágico próprio está fechado no nível de evidência declarado, mesmo quando o resultado correto é zero novos spells semânticos.

| Mod | Mod ID | Versão física/canônica | Estado do catálogo | Cobertura |
| --- | --- | --- | --- | --- |
| Ars 'n' Spells | `ars_n_spells` | `3.3.2` | ✅ Catalogado | 5 rituais próprios no baseline NeoForge 3.3.0; 8 `ars_cross_*` são slots-proxy de transporte e contam **0** standalone spells novos. Release física 3.3.2 e deltas 3.3.1/3.3.2 estão separados do baseline source. |
| Cataclysm: Spellbooks | `cataclysm_spellbooks` | `1.1.13-1.21` | ✅ Catalogado | Artefato físico hash-matched: **59/59** registros atuais; 10 root keys somente de tradução/WIP excluídas. |
| Deeper and Darker: Spellbooks | `darkermagic` | `1.3.3-1.21.1` Variant B | ✅ Catalogado | **4/4** summon spells fechados: Warden, Shattered, Sculk Centipede e Sculk Snapper. Source público 1.3.0 é apenas baseline histórico, não autoridade binária 1.3.3. |
| Farmer's Spell 'n Spellbooks | `farmers_spell` | `1.0.5.1-1.21.1` | ✅ Catalogado | **6/6** spells Gluttony, source-pinned; rota de aquisição via Gluttony Focus + Iron's Scroll Forge fechada no nível de catálogo. |
| Ignis Soulfires: Spellbooks | `ignissoulfires_spellbooks` | `1.1.0` | ✅ Catalogado | Artefato exato fecha **0 spells/rituais/ações mágicas próprios**; provider é `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT` e `ZERO_BRIDGE_INFRA` no ledger semântico. |
| ISS: Magic From The East | `iss_magicfromtheeast` | `1.1.5` | ✅ Catalogado | **22/22** spells ativos (`11 Symmetry + 11 Spirit`); Dune registrada com 0 spells ativos; Launch/Qigong Controlling comentados e excluídos. |
| Leyline Spellbooks | `leylines` | `1.0.3` | ✅ Catalogado | Artefato físico hash-matched: **14** spell identities registradas incondicionalmente; escola `leylines:ley`. |
| Monsters & Spellbooks | `monstersspellbooks` | `0.0.16.3` | ✅ Catalogado | Inventário semântico contemporâneo da release fecha **98** registros; estabilidade do registry no intervalo 0.0.16.2/0.0.16.3 verificada. Internals binários exatos e presença de Aero SchoolType no JAR continuam não verificados. |
| Iron's Spells Magic Schools | `magic_schools` | último snapshot sibling: `1.0` | ⚠️ Parcial/condicionado | Não há fechamento canônico específico encontrado na árvore atual. Revalidar presença/versão física e determinar se adiciona spells, escolas ou ambos antes de promoção. |
| Paladin Spells | `paladin_spells` | `1.21.1-1.1.1` | ✅ Catalogado | **5/5** spells Holy catalogados; blockers de Bulwark, Sworn Protector, Bedrock Skin e Ram permanecem QA de runtime, não lacuna de catálogo. |
| Specs: Iron's Spells 'n Spellbooks Addon | `specs_irons_spellbooks` | último snapshot sibling: `1.6.4` | ⚠️ Parcial/condicionado | Não há fechamento canônico específico encontrado na árvore atual. Revalidar presença física e confirmar se existem spells próprios. |
| Wind's Spellbooks | `wind_spellbooks` | `1.0.5` | ✅ Catalogado | **7/7** spell IDs observados em dump derivado de registry alinhado ao artefato 1.0.5; fórmulas internas não são inferidas sem fonte/binário apropriado. |

## 3. Extensões mágicas de ecossistema

| Mod | Mod ID | Versão física/canônica | Estado do catálogo | Cobertura |
| --- | --- | --- | --- | --- |
| Ars Additions | `ars_additions` | `1.21.1-21.3.0` | ✅ Catalogado | Source-pinned catalog complete: **3/3 glyphs + 2/2 rituais**, além de perks/charms/sistemas catalogados. |
| Ars Controle | `ars_controle` | `1.21.1-1.6.15` | ✅ Catalogado | Source-pinned catalog complete: **9/9 Ars spell parts** e 6/6 sistemas player-facing catalogados. |
| Ars Creo | `ars_creo` | `5.4.0` | ✅ Catalogado | Bridge Ars↔Create fechado; **0 glyphs/spells próprios** no registry auditado. |
| Ars Elemancy | `ars_elemancy` | `1.18.3` | ✅ Catalogado | Provider de gear/especialização elemental fechado; `registerGlyphs()` e `registerPerks()` vazios no source pin, portanto **0 glyphs próprios**. |
| Ars Elemental | `ars_elemental` | `0.7.10.1` | ✅ Catalogado | **39/39 production spell parts**, **8/8 rituais**, 3/3 familiars e demais superfícies source-pinned catalogadas. |
| Ars Polymorphia | `ars_polymorphia` | `1.0.3` | ✅ Catalogado | `ZERO_SEMANTIC_BRIDGE`: compat de recipe-conflict sem spell/glyph/ritual/action registry próprio. |
| Ars Sable | `ars_sable` | `1.1.2` | ✅ Catalogado | `ZERO_SEMANTIC_BRIDGE`: infraestrutura espacial/compat Ars↔Sable sem spell/glyph/ritual/action registry próprio. |
| Ars Technica | `ars_technica` | `2.7.6` | ✅ Catalogado | Source catalog closed: **11/11 spell parts** mais sistemas Ars↔Create/technomancy catalogados. |
| Ars Nouveau: Two-Way Portals | `ars_two_way_portals` | `2.0.0` | ✅ Catalogado | Artefato exato `ZERO_SEMANTIC_PORTAL_INFRA`: 0 spells/glyphs/rituais próprios. |
| Ars Zero | `ars_zero` | `2.0.2` | ✅ Catalogado | Release-pinned: **12** capacidades únicas de glyph atuais normalizadas; superfícies multiphase/voxel/static-staff catalogadas. |
| Alshanex's Familiars Mod | `alshanex_familiars` | `1.21.1_v4.0.3` | ✅ Catalogado | Artefato exato: **7 spells + 11 rituais = 18 objetos mágicos semânticos** próprios. |
| Iron's Apothic | `irons_apothic` | último snapshot sibling: `2.2.1` | ⚠️ Parcial/condicionado | Não há fechamento canônico específico encontrado na árvore atual; revalidar presença física e conteúdo spell-level antes de promoção. |
| Ironsable | `ironsable` | `1.2.0` | ✅ Catalogado | **7/7 provider-owned spell IDs** com catálogo semântico fechado; bytecode/API/runtime contracts continuam separados. |
| Create: Wizardry | `create_wizardry` | último snapshot sibling: `1.21.1-0.5.1-pre1` | ⚠️ Parcial/condicionado | Não há fechamento canônico específico encontrado na árvore atual; revalidar presença física e conteúdo spell-level/fonte antes de promoção. |

### 3.1 Entradas de suporte sem spell próprio provado

Entradas como `arsdelight`, `reliquified_ars_nouveau`, `efiscompat`, `irons_jewelry`, `irons_spells_dynamic_skilltree` e `reliquified_irons_spells_and_spellbooks` não são promovidas como spell-bearing apenas por associação de ecossistema. Se evidência física/runtime demonstrar objetos mágicos próprios, recebem uma árvore/catálogo dedicado.

## 4. Referência clean-room externa já catalogada

| Referência | Presença no pack atual | Estado do catálogo | Cobertura |
| --- | --- | --- | --- |
| Mahou Tsukai | ⚠️ presença atual não afirmada por este índice | ✅ Catalogado | `mahou-observable-catalog.md`: 53 linhas observáveis; 53/53 classificadas em `classification-matrix.md`. Uso apenas como referência pública/observável clean-room. |

## 5. Black Arcana — catálogo próprio

`docs/design/candidate-specifications.md` contém **32 contratos de candidatos** catalogados no nível de design/implementação-facing: 7 Dominion/wards, 5 Liminal, 7 Noetic, 5 Eidetic Arsenal e 8 Sanguine/Sepulchral/Cinder. Isso é catálogo de contrato, não afirma que todos estejam implementados ou balanceados.

Estado global dessa camada: ✅ **Catalogado (32 contratos)**.

### 5.1 Noetic / Stage 07.07 — spells catalogados individualmente

O mapa canônico `docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md` fecha a cadeia clean-room individual dos sete candidatos abaixo. Todos estão ✅ **catalogados** em proveniência; o runtime continua separado e Stage 07.07 permanece parcial.

| Spell Black Arcana | Catálogo/proveniência | Runtime |
| --- | --- | --- |
| Astral Severance | ✅ Catalogado | ⚠️ Parcial — runtime canônico avançou até PR #248; production MOVE profile/values, player-facing cast/channel/upkeep, remote interaction, tuning e D031 ainda não estão todos fechados. |
| Namescry | ✅ Catalogado | ⚠️ Stage 07.07 parcial; este índice não promove implementação individual além da evidência de `plans/STATUS.md`. |
| Gaze of Stillness | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Nullifying Gaze | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Occult Appraisal | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Borrowed Sight | ✅ Catalogado | ⚠️ Parcial — câmera server-authored é canônica; aceitação real-client D031 permanece pendente. |
| Pact Sanctuary | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |

## 6. Resumo de cobertura

As métricas abaixo têm denominadores diferentes e não devem ser misturadas:

- ✅ **Hosts principais catalogados:** **4/4** — Iron's, Ars Nouveau, Eidolon: Repraised e Malum.
- ✅ **Addons/providers com spell/magic explícito catalogados nesta tabela:** **10/12**.
- ⚠️ **Addons explícitos ainda condicionados:** **2/12** — `magic_schools`, `specs_irons_spellbooks`.
- ✅ **Extensões de ecossistema catalogadas nesta tabela:** **12/14**.
- ⚠️ **Extensões ainda condicionadas:** **2/14** — `irons_apothic`, `create_wizardry`.
- ✅ **Mínimo semântico global reconstruível canônico:** **1344 objetos mágicos**. O denominador semântico global permanece incompleto; **nenhuma porcentagem semântica final é declarada**.
- ✅ **Cobertura técnica de componentes do catálogo:** **66/100 = 66%** no ledger canônico. Esse número mede componentes técnicos, não quantidade/percentual de spells.
- ✅ **Referência clean-room Mahou Tsukai:** 53/53 linhas observáveis classificadas; presença física atual não afirmada.
- ✅ **Contratos próprios Black Arcana:** 32 candidatos catalogados.
- ✅ **Noetic Stage 07.07:** 7/7 spells com proveniência individual catalogada; runtime continua parcial.

Providers `ZERO_*` contam como ✅ **catalogados** quando a evidência fecha corretamente que contribuem zero objetos mágicos independentes. Zero não é ausência de auditoria.

## 7. Regra de manutenção

Ao receber uma modlist/runtime inventory mais recente:

1. registrar SHA/fingerprint e fonte física;
2. reconciliar presença/remoção/version drift antes de trabalho spell-level;
3. não inferir spell-bearing apenas por dependência, nome ou associação de ecossistema;
4. usar `wiki/modpack-catalog/providers/` como árvore canônica detalhada e os ledgers de `wiki/modpack-catalog/meta/` para métricas globais;
5. promover `❌`/`⚠️` para `✅` somente quando o escopo declarado estiver completo e revisado — inclusive quando o resultado correto for zero semantic magic;
6. manter Runtime separado: catalogação não implica implementação, compatibilidade, integração ou balanceamento concluídos;
7. quando sibling/versionado e snapshot físico divergirem, a evidência física mais recente vence.
