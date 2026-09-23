# Black Arcana — Catálogo Global de Magia e Feitiços

Última sincronização: 2026-09-23

Este arquivo é o índice operacional global de catalogação do projeto. A árvore detalhada canônica é `wiki/modpack-catalog/providers/`; o ledger semântico reconstruível é `wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md`; e a cobertura técnica de componentes é `wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md`.

O objetivo deste índice é responder duas perguntas sem misturá-las:

1. quais providers possuem ações mágicas semanticamente contáveis e já possuem inventário atual suficientemente fechado;
2. quais providers/extensões mágicas foram auditados mas contribuem zero ações independentes, permanecem condicionais ou ainda precisam ser revalidados.

## Legenda obrigatória

- ✅ **Catalogado** — existe inventário/contrato suficientemente fechado para o escopo indicado; isso inclui fechamento correto em **zero** objetos mágicos próprios.
- ❌ **Não catalogado** — provider/conteúdo confirmado, mas sem inventário mágico fechado.
- 🟡 **Em implementação** — catalogação existe e uma implementação canônica está sendo construída em tranche ativa.
- ⚠️ **Parcial/condicionado** — inventário, configuração, survival reachability, elegibilidade atual ou presença física ainda não fecha o requisito necessário.
- ⛔ **Bloqueado** — falta fonte/artefato/contrato obrigatório para prosseguir com segurança.

**Regra:** estes marcadores descrevem **catalogação**, salvo quando uma coluna diz explicitamente `Runtime`. `COUNTED_*` também é estado de confiança do inventário semântico, não certificado de runtime, ABI, balanceamento ou full-pack QA.

## Snapshot de autoridade

- Black Arcana base desta reconciliação: `main@3936635bd32f316ae57976bd9af7b333baac0a5a`.
- RPG Skill Tree sibling mais recente consultado: `main@4767f5c637c02c6d91ccb43a86ea1539f42a2e9b`.
- O índice físico sibling atual reconcilia **587 entradas top-level incluindo o modloader**; para Create: Wizardry, a linha certificada atual é **#166**. O antigo snapshot Black Arcana de 595 entradas abaixo permanece histórico até regeneração integral do denominator mágico.
- Snapshot físico canônico registrado nos ledgers do Black Arcana: Minecraft `1.21.1`, NeoForge `21.1.248`, **595 entradas top-level**, SHA-1 da modlist `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.
- O sibling mantém `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`, como inventário versionado histórico de integração. Quando houver divergência, evidência física/canônica posterior do Black Arcana vence.

## 1. Ledger semântico global atual — 40 providers / 1344 objetos

Esta tabela reproduz o conjunto **strict-counted** do ledger canônico. O contador inclui uma identidade apenas uma vez sob seu dono semântico: spell standalone, glyph/spell-part primitivo, ritual/rite ou ação sobrenatural equivalente. Escolas, itens, equipamentos, familiars, efeitos/status, recursos, aliases, slots-proxy, composições arbitrárias de Ars e consequências secundárias não geram nova identidade.

| Provider | Linha física/canônica | Objetos contados | Estado do inventário | Base semântica resumida |
| --- | --- | ---: | --- | --- |
| Ars Nouveau | `5.13.1` | 109 | ✅ `COUNTED_SOURCE_PINNED` | 5 Forms + 13 Augments + 67 Effects + 24 rituals; chains arbitrárias excluídas. |
| Ars Additions | `21.3.0` | 5 | ✅ `COUNTED_SOURCE_PINNED` | 3 glyphs + 2 rituals. |
| Ars Controle | `1.6.15` | 9 | ✅ `COUNTED_SOURCE_PINNED` | 1 effect + 8 filters/spell parts. |
| Ars Technica | `2.7.6` | 11 | ✅ `COUNTED_SOURCE_PINNED` | 11/11 spell parts registrados. |
| Ars Hex | `5.0.4b` | 1 | ✅ `COUNTED_SOURCE_PINNED` | 1 glyph Malum-backed atual sob o conjunto físico de providers. |
| Ars Zero | `2.0.2` | 12 | ✅ `COUNTED_RELEASE_BOUNDED` | 12 capacidades únicas atuais; variantes AOE/Amplifier copiadas e desabilitadas excluídas. |
| Ars Elemental | `0.7.10.1` | 47 | ✅ `COUNTED_SOURCE_PINNED` | 39 production spell parts + 8 rituals. |
| Ars 'n' Spells | `3.3.2` | 5 | ✅ `COUNTED_SOURCE_PINNED` | 5 rituais; oito `ars_cross_*` são slots-proxy e contribuem zero. |
| Iron's Spells 'n Spellbooks | `3.16.3` | 110 | ✅ `COUNTED_EXACT` | 110/110 registros ativos; Cloud of Regeneration deprecated excluído. |
| Apprentice's Codex | `0.9.7.1` | 83 | ✅ `COUNTED_SOURCE_PINNED` | 83-spell registry inventory. |
| Asterism Arcanum | `1.21.1-0.1.0` | 10 | ✅ `COUNTED_SOURCE_PINNED` | 10 spells survival; `astral_gateway` permanece condicional separadamente. |
| Backported Spellbooks | físico `0.1.2` / embedded `0.1.0` | 6 | ✅ `COUNTED_RELEASE_BOUNDED` | 6 standalone Iron's spells no teto oficial da release. |
| Deeper & Darker Spellbooks | `1.3.3` Variant B | 4 | ✅ `COUNTED_RELEASE_BOUNDED` | 4 summon spells atuais: Warden, Shattered, Sculk Centipede e Sculk Snapper. |
| Discerning The Eldritch | `1.4.4` | 22 | ✅ `COUNTED_SOURCE_PINNED` | 22/22 spells registrados, incluindo ritual-school spells uma vez. |
| Dreamless Spells | `1.1.9` | 4 | ✅ `COUNTED_SOURCE_PINNED` | 4 spells atuais registrados. |
| GTBC's Geomancy Plus | `1.1.0-1.21.1` | 12 | ✅ `COUNTED_RELEASE_BOUNDED` | 10 Geo + 2 Holy; acquisition/reachability fechada no nível de catálogo. |
| Farmer's Spell 'n Spellbooks | `1.0.5.1-1.21.1` | 6 | ✅ `COUNTED_SOURCE_PINNED` | 6 Gluttony spells; focus + Scroll Forge fecham reachability de catálogo. |
| SnackPirate's Aeromancy Additions | `1.2.8` | 10 | ✅ `COUNTED_SOURCE_PINNED` | 10 Wind spells ativos; 5 registros comentados excluídos. |
| Fire's Ender Expansion | `2.4.1` | 11 | ✅ `COUNTED_SOURCE_PINNED` | 11/11 spells ativos. |
| IronSable | `1.2.0` | 7 | ✅ `COUNTED_RELEASE_BOUNDED` | 7 spells próprios; 10 physicalized Iron's spells não duplicam identidades. |
| ISS: Magic From The East | `1.1.5` | 22 | ✅ `COUNTED_SOURCE_PINNED` | 11 Symmetry + 11 Spirit; Dune sem spell ativo. |
| Legendary Spellbooks | `0.3.2` | 30 | ✅ `COUNTED_SOURCE_PINNED` | 30 spell identities atuais. |
| Monsters & Spellbooks | `0.0.16.3` | 98 | ✅ `COUNTED_RELEASE_BOUNDED` | Registry semanticamente estável no intervalo 0.0.16.2/0.0.16.3. |
| Paladin Spells | `1.1.1` | 5 | ✅ `COUNTED_SOURCE_PINNED` | 5/5 Holy spells; blockers conhecidos permanecem QA de runtime. |
| Wind's Spellbooks | `1.0.5` | 7 | ✅ `COUNTED_RELEASE_BOUNDED` | 7/7 Wind spells publisher/runtime-observed. |
| Ypsilon's Fundamentalism | `1.1.7.1` | 15 | ✅ `COUNTED_SOURCE_PINNED` | 15/15 registros ativos; prototypes comentados excluídos. |
| Tunes n' Tomes | `1.1.0-HOTFIX` | 16 | ✅ `COUNTED_RELEASE_BOUNDED` | 16 Melodic spells atuais; ownership Sound migrado não é duplicado. |
| Alshanex's Familiars | `4.0.3` | 18 | ✅ `COUNTED_EXACT` | 7 spells + 11 `ritual_recipe`; casts externos/familiar AI não duplicados. |
| Cataclysm: Spellbooks | `1.1.13` | 59 | ✅ `COUNTED_EXACT` | 59 registros incondicionais; 10 root localization keys sem registro excluídas. |
| Leyline Spellbooks | `1.0.3` | 14 | ✅ `COUNTED_EXACT` | 14 registros incondicionais; generic Iron's config permanece runtime QA. |
| Gaze | `1.1.7.1` | 1 | ✅ `COUNTED_EXACT` | Soulward Shield contado; 26 Spirit Rites permanecem condicionais à config efetiva. |
| Goety | `3.1.4` | 361 | ✅ `COUNTED_EXACT` | 123 Focus + 238 non-Focus rituals após deduplicação/reachability. |
| Goety Iron | `3.1` | 14 | ✅ `COUNTED_EXACT` | 2 Focus + 12 rituais distintos; acquisition rituals deduplicados. |
| Goety Cataclysm | `1.21.1-1.8.2` | 52 | ✅ `COUNTED_EXACT` | 28 Focus + 24 rituais distintos; acquisition rituals deduplicados. |
| Eidolon: Repraised | `0.5.0.2` | 42 | ✅ `COUNTED_SOURCE_PINNED` | 18 chants player-facing + 24 ritual recipes; dummy/empty entries excluídas. |
| Vampirism | `1.10.13` | 19 | ✅ `COUNTED_SOURCE_PINNED` | 14 Vampire + 3 Hunter + 2 shared Lord actions. |
| Bloodlines | `3.0.9` | 28 | ✅ `COUNTED_SOURCE_PINNED` | 29 action registrations menos Sorcerous Strike, sem survival reachability normal. |
| Werewolves | `2.0.3.3` | 8 | ✅ `COUNTED_SOURCE_PINNED` | 3 form actions + Howling + Rage + Sense + Fear + Leap. |
| Hexalia | físico `1.3.6` / runtime metadata `1.3.5` | 25 | ✅ `COUNTED_RELEASE_BOUNDED` | 19 Nature's Ritual + 6 Celestial Infusion identities. |
| Malum | `1.8.2` | 26 | ✅ `COUNTED_RELEASE_BOUNDED` | 26 Spirit Rites; 37 Geas effects e 9 spirit types são inventariados, mas excluídos da métrica de ação. |
| **Total estrito reconstruível** |  | **1344** |  | Denominador semântico global ainda incompleto; nenhuma porcentagem final é declarada. |

## 2. Providers auditados com zero objetos semânticos independentes

Zero é um resultado de catálogo válido quando a auditoria fecha que o mod apenas transporta, adapta, equipa ou integra ações de outro provider.

| Provider | Versão | Estado | Fechamento |
| --- | --- | --- | --- |
| Ignis Soulfires: Spellbooks | `1.1.0` | ✅ `ZERO_BRIDGE_INFRA` | Bridge/gear/loot support; 0 spell/ritual/action registry próprio. |
| Ars Creo | `5.4.0` | ✅ Catalogado | Bridge Ars↔Create; 0 glyph/spell registry próprio no source pin. |
| Ars Elemancy | `1.18.3` | ✅ Catalogado | Gear/especialização elemental; `registerGlyphs()` e `registerPerks()` vazios. |
| Ars Polymorphia | `1.0.3` | ✅ `ZERO_SEMANTIC_BRIDGE` | Compat de recipe conflict; 0 spell/glyph/ritual/action registry próprio. |
| Ars Sable | `1.1.2` | ✅ `ZERO_SEMANTIC_BRIDGE` | Infraestrutura espacial/compat; 0 spell/glyph/ritual/action registry próprio. |
| Ars Nouveau: Two-Way Portals | `2.0.0` | ✅ `ZERO_SEMANTIC_PORTAL_INFRA` | Artefato exato; 0 spell/glyph/ritual/rite/ability independente. |
| Vampire Spells Addon | `0.0.9` | ✅ `ZERO_BRIDGE_INFRA` | Source-pinned Iron's↔Vampirism behavior/policy overlay; 0 provider-owned spell/school/ritual/action registry; runtime bridge QA separado. |
| Create: Wizardry | `1.21.1-0.5.1-pre1` | ✅ `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION` | Presença física #166 e source pin exato da versão revalidados; Blaze Caster/Mana Siphon usam spells/mana do Iron's, mas não há provider-owned spell registry/resource. +0 semântico; runtime QA separado. |
| Ars Sophisticated Compatibility | `0.3.0` | ✅ `ZERO_SEMANTIC_BRIDGE` | Artefato físico/publisher reconciliado como Sophisticated Backpacks↔Ars Nouveau compat; 0 standalone spells, glyphs/spell-parts ou rituals; runtime/API QA permanece separado. |
| Reliquified L_Ender's Cataclysm — New Relics Fix | `1.0.2` | ✅ `ZERO_SEMANTIC_BRIDGE` | Bridge Relics 0.10→0.12 para cinco relics já pertencentes ao addon original; 0 novas identidades de relic ou spell; runtime QA separado. |

## 3. Providers mágicos atuais ainda condicionais no ledger

| Provider | Linha | Estado | Motivo |
| --- | --- | --- | --- |
| T.O Magic n' Extras / Traveloptics | `4.4.0.1-1.21.1` | ⚠️ Parcial/condicionado | 33 IDs registrados exatos catalogados, mas `blackout` survival reachability e risco estrutural de loot modifier permanecem abertos; +0 estrito e componente não fechado. |
| Gaze — Spirit Rites | `1.1.7.1` | ⚠️ Condicionado | 26 rites player-facing existem no artefato, porém `disableGazeRites` pode suprimir o registry e o valor COMMON implantado não está disponível. O spell Soulward Shield já está contado separadamente na tabela estrita. |
| Asterism Arcanum — `astral_gateway` | `1.21.1-0.1.0` | ⚠️ Condicionado | Provider possui 10 ações survival já contadas; `astral_gateway` permanece fora do strict count até fechar sua condição/reachability. |

## 4. Candidatos herdados do snapshot antigo do sibling — presença atual não afirmada

As entradas abaixo existiam em `docs/MODPACK_SCOPE.md` derivado de `modlist(20260822-201255).txt`, mas **não receberam fechamento canônico específico encontrado na árvore atual** durante esta reconciliação. Elas não entram em denominador atual nem são tratadas como fisicamente presentes sem nova evidência.

| Mod | Mod ID | Última versão no snapshot sibling | Estado |
| --- | --- | --- | --- |
| Iron's Spells Magic Schools | `magic_schools` | `1.0` | ⚠️ Revalidar presença física e determinar spells/escolas próprios. |
| Specs: Iron's Spells 'n Spellbooks Addon | `specs_irons_spellbooks` | `1.6.4` | ⚠️ Revalidar presença física e confirmar spells próprios. |
| Iron's Apothic | `irons_apothic` | `2.2.1` | ⚠️ Revalidar presença física e conteúdo spell-level. |

Entradas de suporte como `arsdelight`, `reliquified_ars_nouveau`, `efiscompat`, `irons_jewelry`, `irons_spells_dynamic_skilltree` e `reliquified_irons_spells_and_spellbooks` também não são promovidas como spell-bearing apenas por associação de ecossistema.

## 5. Referência clean-room externa

| Referência | Presença no pack atual | Estado | Cobertura |
| --- | --- | --- | --- |
| Mahou Tsukai | ⚠️ não afirmada neste snapshot | ✅ Catalogado | `mahou-observable-catalog.md`: 53 linhas observáveis; 53/53 classificadas. Referência clean-room, não provider/runtime obrigatório. |

## 6. Black Arcana — catálogo próprio

`docs/design/candidate-specifications.md` contém **32 contratos de candidatos** no nível de design/implementation-facing: 7 Dominion/wards, 5 Liminal, 7 Noetic, 5 Eidetic Arsenal e 8 Sanguine/Sepulchral/Cinder. Catálogo de contrato não implica implementação ou balanceamento final.

Estado global dessa camada: ✅ **Catalogado (32 contratos)**.

### 6.1 Noetic / Stage 07.07

`docs/provenance/STAGE-07-07-NOETIC-SPELL-PROVENANCE.md` fecha a proveniência individual dos sete candidatos. Todos estão ✅ catalogados; runtime permanece separado e Stage 07.07 continua parcial conforme `plans/STATUS.md`.

| Spell Black Arcana | Catálogo/proveniência | Runtime |
| --- | --- | --- |
| Astral Severance | ✅ Catalogado | ⚠️ Stage 07.07 parcial; `main` possui múltiplas tranches canônicas de Astral, sem promoção de completude individual neste índice. |
| Namescry | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Gaze of Stillness | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Nullifying Gaze | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Occult Appraisal | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |
| Borrowed Sight | ✅ Catalogado | ⚠️ Câmera server-authored canônica; aceitação real-client D031 permanece pendente. |
| Pact Sanctuary | ✅ Catalogado | ⚠️ Stage 07.07 parcial. |

## 7. Resumo de cobertura

As métricas têm denominadores diferentes:

- ✅ **Ledger semântico strict-counted:** **40 providers / 1344 objetos mágicos reconstruíveis**.
- ⚠️ **Denominador semântico global:** ainda incompleto; portanto **nenhuma porcentagem final de spells/magia é declarada**.
- ✅ **Cobertura técnica de componentes:** **67/100 = 67%** no ledger `CATALOG-COVERAGE-CURRENT.md`. Esse percentual mede componentes técnicos, não spells.
- ✅ **Zero-semantic/infra explicitamente auditados nesta reconciliação:** 9 providers listados acima; zero não significa ausência de auditoria.
- ⚠️ **Current-ledger conditionals destacados:** Traveloptics, 26 Gaze Spirit Rites e Asterism `astral_gateway`.
- ⚠️ **Legacy sibling candidates sem presença física atual afirmada:** `magic_schools`, `specs_irons_spellbooks`, `irons_apothic`.
- ✅ **Create: Wizardry saiu desta lista:** presença física atual #166 e source pin 1.21.1-0.5.1-pre1 estão revalidados; o provider fecha em +0 spells próprios porque automatiza spells do Iron's sem registrar identidades próprias.
- ✅ **Mahou Tsukai clean-room:** 53/53 linhas observáveis classificadas; presença física atual não afirmada.
- ✅ **Black Arcana próprio:** 32 contratos de candidatos; Noetic 7/7 com proveniência individual.

## 8. Regra de manutenção

Ao receber uma modlist/runtime inventory mais recente:

1. registrar SHA/fingerprint e fonte física;
2. reconciliar presença, remoção e version drift antes de trabalho spell-level;
3. não inferir spell-bearing apenas por dependência, título ou associação de ecossistema;
4. usar `wiki/modpack-catalog/providers/` como árvore canônica detalhada e `wiki/modpack-catalog/meta/` para os denominadores globais;
5. promover `❌`/`⚠️` para `✅` somente quando o escopo declarado estiver completo e revisado, inclusive quando o resultado correto for zero semantic magic;
6. manter Runtime separado: catalogação não implica implementação, compatibilidade, integração ou balanceamento concluídos;
7. quando sibling/versionado e snapshot físico divergirem, a evidência física mais recente vence;
8. não publicar subtotais de um subconjunto legado como se fossem cobertura global.
