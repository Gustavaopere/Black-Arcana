# Black Arcana — Catálogo Global de Magia e Feitiços

Última sincronização: 2026-09-14

Este arquivo é o índice operacional global de catalogação do projeto. Ele não substitui os catálogos clean-room, mapas de proveniência, especificações ou `plans/STATUS.md`; ele aponta para essas evidências e separa **catalogação** de **implementação**.

## Legenda obrigatória

- ✅ **Catalogado** — existe inventário/contrato de catálogo suficientemente fechado para o escopo indicado.
- ❌ **Não catalogado** — o mod/conteúdo foi identificado, mas não existe inventário de spells/mecânicas mágicas fechado no Black Arcana.
- 🟡 **Em implementação** — catalogação já existe e a implementação canônica está sendo construída em uma tranche ativa.
- ⚠️ **Parcial/condicionado** — existe cobertura parcial, de host/API/capacidade, ou a evidência física atual não é suficiente para afirmar catálogo integral.
- ⛔ **Bloqueado** — catalogação não pode prosseguir sem uma fonte/artefato/contrato obrigatório que está ausente.

**Regra:** estes marcadores descrevem o estado de **catalogação**, salvo quando uma coluna diz explicitamente `Runtime`. Um spell pode estar ✅ catalogado e ainda estar ⚠️ parcial no runtime.

## Snapshot de autoridade usado

- Black Arcana: `main@942431299bdb7afdbe893db2951f5294137cf735`.
- RPG Skill Tree sibling: `main@9e88db8f6b37c1bfbbd331f6684504a76e4aef40`.
- O sibling mantém `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`, como inventário versionado de integração.
- O Black Arcana mantém `docs/reference/runtime-host-baseline.md`, derivado do `modlist agora atual.txt` fornecido em 2026-08-26, para o baseline de Iron's, Ars Nouveau, Eidolon e Malum.
- O sibling documenta que o runtime carregado é a autoridade e que `modlist agora atual.txt` é um snapshot externo; o arquivo físico atual não está versionado no Git. Por isso este índice **não declara exaustividade física do pack além da evidência versionada disponível**. Quando a modlist/runtime atual for regenerada e versionada, este arquivo deve ser reconciliado antes de promover novos mods como presentes.

## 1. Hosts mágicos instalados com evidência Black Arcana

| Mod | Mod ID / versão instalada evidenciada | Conteúdo mágico | Estado do catálogo | Evidência / observação |
| --- | --- | --- | --- | --- |
| Iron's Spells 'n Spellbooks | `irons_spellbooks` — `1.21.1-3.16.3` | ✅ host explícito de spells | ⚠️ Parcial/condicionado | API/capacidades e integração foram auditadas; **não existe inventário integral de todos os spells do mod** no Black Arcana. |
| Ars Nouveau | `ars_nouveau` — `1.21.1-5.13.0` | ✅ sistema mágico/spellcraft | ⚠️ Parcial/condicionado | Host/capacidades, Blink/Warp/familiars e limites de integração são catalogados; **não existe inventário integral de glyphs/spells do mod**. |
| Eidolon: Repraised | versão instalada `1.21.1-0.5.0.2` | ✅ sistema mágico/ritual | ⚠️ Parcial/condicionado | Host/capacidades e seam policy são catalogados; **não existe inventário integral de rituais/spells**. |
| Malum | versão instalada `1.21.1-1.8.2` | ✅ sistema mágico/espiritual | ⚠️ Parcial/condicionado | Host/capacidades e Spirit Rite/resource boundary são catalogados; **não existe inventário integral de magia/ritos**. |

Fonte principal: `docs/reference/runtime-host-baseline.md`, `docs/reference/host-capability-map.md` e código/testes canônicos de integração.

## 2. Mods/addons mágicos ou spellbook identificados no inventário versionado do sibling

Os itens abaixo foram promovidos para este índice porque o inventário versionado os coloca diretamente nos ecossistemas Ars ou Iron's/spellbook e o próprio nome/título fornece evidência explícita de spell/magic **ou** de extensão direta do sistema mágico. Isso não prova o conjunto de spells interno. Uma linha só recebe ✅ depois de possuir catálogo próprio com escopo fechado e evidência da versão auditada.

### 2.1 Evidência explícita de spells/spellbooks/magic no título

| Mod | Mod ID | Versão do snapshot | Estado do catálogo | Próximo requisito / cobertura |
| --- | --- | --- | --- | --- |
| Ars 'n' Spells | `ars_n_spells` | `3.0.2` | ✅ Catalogado | `ARS-N-SPELLS-3.0.2.md`: 8 registros-proxy `AbstractSpell` sem efeito próprio + 5 rituais; spells dinâmicos de Ars/Iron's transportados pelo bridge não são recontados como conteúdo do addon. |
| Cataclysm: Spellbooks | `cataclysm_spellbooks` | `1.1.12-1.21` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |
| Deeper and Darker: Spellbooks | `darkermagic` | `1.3.3-1.21.1` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |
| Farmer's Spell 'n Spellbooks | `farmers_spell` | `1.0.4.0-1.21.1` | ✅ Catalogado | `FARMERS-SPELL-1.0.4.0.md`: 6/6 registros runtime em `SpellRegistry`, todos na escola `farmers_spell:gluttony`; `BerserkCleaverSpell.java` está totalmente comentado e não é contado como spell runtime. |
| Ignis Soulfires: Spellbooks | `ignissoulfires_spellbooks` | `1.1.0` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |
| ISS: Magic From The East | `iss_magicfromtheeast` | `1.1.5` | ❌ Não catalogado | Confirmar inventário mágico e catalogar conteúdo observável. |
| Leyline Spellbooks | `leylines` | `1.0.3` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |
| Monsters & Spellbooks | `monsterspellbooks` | `0.0.14` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |
| Iron's Spells Magic Schools | `magic_schools` | `1.0` | ⚠️ Parcial/condicionado | Determinar se adiciona spells, escolas apenas, ou ambos; catalogar o que for mágico. |
| Paladin Spells | `paladin_spells` | `1.21.1-1.1.1` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |
| Specs: Iron's Spells 'n Spellbooks Addon | `specs_irons_spellbooks` | `1.6.4` | ⚠️ Parcial/condicionado | O título prova vínculo ao sistema; confirmar se adiciona spells antes de inventário spell-level. |
| Wind's Spellbooks | `wind_spellbooks` | `1.0.5` | ❌ Não catalogado | Inventariar spells públicos/observáveis e proveniência. |

### 2.2 Extensões mágicas de ecossistema cujo conteúdo spell-level ainda precisa ser provado

| Mod | Mod ID | Versão do snapshot | Estado do catálogo | Condição |
| --- | --- | --- | --- | --- |
| Ars Additions | `ars_additions` | `1.21.1-21.3.0` | ⚠️ Parcial/condicionado | Confirmar quais entradas são spells/glyphs versus suporte/conteúdo não-spell. |
| Ars Controle | `ars_controle` | `1.21.1-1.6.15` | ⚠️ Parcial/condicionado | Confirmar conteúdo mágico catalogável. |
| Ars Creo | `ars_creo` | `5.4.0` | ⚠️ Parcial/condicionado | Integração Ars/Create identificada; confirmar spell/glyph inventory. |
| Ars Elemancy | `ars_elemancy` | `1.18.3` | ⚠️ Parcial/condicionado | Confirmar spell/glyph inventory. |
| Ars Elemental | `ars_elemental` | `0.7.10.1` | ⚠️ Parcial/condicionado | Confirmar spell/glyph inventory. |
| Ars Polymorphia | `ars_polymorphia` | `1.0.3` | ⚠️ Parcial/condicionado | Confirmar spell/glyph inventory. |
| Ars Sable | `ars_sable` | `1.1.2` | ⚠️ Parcial/condicionado | Confirmar spell/glyph inventory. |
| Ars Technica | `ars_technica` | `2.7.6` | ⚠️ Parcial/condicionado | Integração Ars/Create identificada; confirmar spell/glyph inventory. |
| Ars Nouveau: Two-Way Portals | `ars_two_way_portals` | `2.0.0` | ⚠️ Parcial/condicionado | Conteúdo mágico identificado; confirmar se há spells/glyphs próprios. |
| Ars Zero | `ars_zero` | `2.0.2` | ⚠️ Parcial/condicionado | Confirmar spell/glyph inventory. |
| Alshanex's Familiars Mod | `alshanex_familiars` | `1.21.1_v4.0.3` | ⚠️ Parcial/condicionado | Sistema familiar mágico identificado; confirmar spells próprios versus entidades/suporte. |
| Iron's Apothic | `irons_apothic` | `2.2.1` | ⚠️ Parcial/condicionado | Confirmar se adiciona spells ou somente integração/itens. |
| Ironsable | `ironsable` | `1.2.0` | ⚠️ Parcial/condicionado | Confirmar conteúdo spell-level antes de promover para inventário de spells. |
| Create: Wizardry | `create_wizardry` | `1.21.1-0.5.1-pre1` | ⚠️ Parcial/condicionado | Conteúdo mágico/Create identificado; confirmar spell-level e fonte pública antes de catalogar. |

### 2.3 Entradas de suporte não promovidas como fonte de spells

O mesmo inventário contém `arsdelight`, `reliquified_ars_nouveau`, `efiscompat`, `irons_jewelry`, `irons_spells_dynamic_skilltree` e `reliquified_irons_spells_and_spellbooks`. Eles **não são contados como mods spell-bearing neste índice apenas por associação de ecossistema**. Se evidência pública/runtime mostrar spells próprios, devem ser promovidos por uma atualização evidenciada.

## 3. Referência clean-room externa já catalogada

| Referência | Presença no pack atual | Estado do catálogo | Cobertura |
| --- | --- | --- | --- |
| Mahou Tsukai | ⚠️ não afirmada por este snapshot global | ✅ Catalogado | `mahou-observable-catalog.md`: 53 linhas observáveis; 53/53 classificadas em `classification-matrix.md`. Uso apenas como referência pública/observável clean-room, não como provider/runtime obrigatório. |

## 4. Black Arcana — catálogo próprio

`docs/design/candidate-specifications.md` contém **32 contratos de candidatos** catalogados no nível de design/implementação-facing: 7 Dominion/wards, 5 Liminal, 7 Noetic, 5 Eidetic Arsenal e 8 Sanguine/Sepulchral/Cinder. Isso é catálogo de contrato, não afirma que todos estejam implementados ou balanceados.

Estado global dessa camada: ✅ **Catalogado (32 contratos)**.

### 4.1 Noetic / Stage 07.07 — spells catalogados individualmente

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

## 5. Resumo de cobertura

Este resumo conta **linhas de mods no índice versionado**, não quantidade de spells internos:

- ✅ Catálogo integral de spells/mecânicas do mod de referência: **1** (`Mahou Tsukai`, referência clean-room; presença atual não afirmada).
- ⚠️ Hosts instalados com cobertura parcial de capacidade/API, mas sem inventário integral de spells: **4** (Iron's, Ars Nouveau, Eidolon, Malum).
- ✅ Addons com catálogo próprio fechado no snapshot versionado: **2** (`Ars 'n' Spells` 3.0.2: 8 proxies sem efeito próprio + 5 rituais; `Farmer's Spell 'n Spellbooks` 1.0.4.0: 6/6 spells runtime registrados).
- ❌ Addons com evidência explícita de spell/magic no inventário, ainda sem catálogo próprio: **8**.
- ⚠️ Addons de título explicitamente mágico cujo tipo exato de conteúdo ainda precisa ser confirmado: **2** (`magic_schools`, `specs_irons_spellbooks`).
- ⚠️ Extensões de ecossistema que exigem confirmação spell-level antes de catalogação integral: **14**.
- ✅ Contratos próprios Black Arcana: **32** candidatos catalogados.
- ✅ Noetic Stage 07.07: **7/7** spells com proveniência individual catalogada.

## 6. Regra de manutenção

Ao receber uma modlist/runtime inventory mais recente:

1. registrar SHA/fingerprint e fonte física;
2. adicionar/remover/driftar mods antes de qualquer trabalho de spell catalog;
3. não inferir spell-bearing apenas por dependência ou nome de ecossistema;
4. para cada mod confirmado com spells/magia, criar ou apontar um catálogo observável/proveniência dedicado;
5. promover `❌`/`⚠️` para `✅` somente quando o inventário definido estiver completo e revisado;
6. manter `Runtime` separado: catalogação não implica implementação, integração ou balanceamento concluídos.
