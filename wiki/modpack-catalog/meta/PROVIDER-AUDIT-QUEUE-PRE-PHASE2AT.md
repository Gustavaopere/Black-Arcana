# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

Este arquivo é a fila operacional corrente. O snapshot detalhado anterior à Phase 2AS foi preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AS.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AS.md). O snapshot histórico de 2026-09-07 permanece em [`PROVIDER-AUDIT-QUEUE-2026-09-07.md`](./PROVIDER-AUDIT-QUEUE-2026-09-07.md).

Autoridade física deste checkpoint:

- Minecraft 1.21.1;
- NeoForge `21.1.248`;
- modlist física mais recente: **595 entradas top-level**;
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- dependências internas/jarjar não contam como providers top-level.

O snapshot histórico de 2026-09-07 usava 612 entradas / 103 candidatos e não é mais autoridade de presença, versão nem denominador.

## Cobertura global

Ver [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

- `main@ac4df420158616d2fb993fb5fbf6b8325c207c27` é a base canônica desta Phase 2AS;
- cobertura canônica nessa base: **46/100 = 46%**;
- Phase 2AR / PR #154 fechou `backportedspellbooks` como componente #46 e já está canônica;
- esta revisão Phase 2AS representa **47/100 = 47%** apenas como candidato até reconciliação final + CI GREEN + merge + confirmação pós-merge;
- Phase 2AQ / PR #152 permanece componente #45 canônico em `main@bdf5271c265b5f40ee5a9e7695c7d71374a4c31c`;
- PR #153 corrigiu somente evidência de metadata da Phase 2AP, com **zero delta de cobertura**;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção preservada: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AS — Apothic Compats 0.2.4.2 — candidate #47

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `apothic_compats` | `apothic_compats-0.2.4.2.jar` | CANDIDATO PHASE 2AS / EXACT PHYSICAL 0.2.4.2 + EXACT OFFICIAL SOURCE VERSION / APOTHEOSIS COMPAT DATAPACK+RUNTIME HELPERS / 0 SPELLS+GLYPHS+RITUALS / 0 CAST RESOURCE / ARS NOUVEAU+MALUM COMPATS / 3 MIXINS / 4 MALUM CUSTOM AFFIX CODECS / PROJECTILE ATTRIBUTE PASS / COMPONENT #47 CANDIDATE / APOTHEOSIS-DRIFT+BYTE+FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical artifact `apothic_compats-0.2.4.2.jar`, mod ID `apothic_compats`, version 0.2.4.2, SHA-1 `46d3699a4af63531fe84c69fdd2623fbe71fbc75`.
- Exact official source: `ianm1647/apothic-compats@0b9c900344dc536e4748e3ad0f3f18e03f2c3ba4`.
- Exact root tree: `76e2e650732584a315b3faa3ab94ff8953e6caad`; exact Java subtree was recursively inspected with `truncated=false`.
- Exact source metadata: Minecraft 1.21.1, version 0.2.4.2, NeoForge development baseline 21.1.242, MIT metadata.
- Exact generated metadata requires NeoForge, Minecraft, Placebo `[9.6.1,)` and Apotheosis `[8.0.1,)`; Ars Nouveau, Malum and other targets are compatibility targets rather than hard TOML dependencies.
- Source development Apotheosis baseline is 8.6.0 while the physical pack contains Apotheosis 8.8.0; runtime/data compatibility remains fail-closed QA.
- Complete exact source tree exposes **0 standalone spells, 0 glyphs, 0 rituals, 0 provider-owned mana/cast resource, 0 provider cast controller and 0 provider packet/payload surface observed**.
- Exact mixin count is 3: Candle Holder, Double Skull and Skull Candle adapters to Apothic Enchanting `EnchantmentStatBlock` Arcana/Quanta stats.
- Optional Curios content registers 11 provider items when Curios is loaded and provider config enables it.

### Ars Nouveau boundary

- Physical Ars Nouveau: 5.13.1.
- One conditional provider gem: `apothic_compats:ars_nouveau/mana`.
- Gem/affix definitions consume Ars-native max mana, mana regen, spell damage, warding and mob-effect surfaces; they do **not** create another Ars mana/casting authority.
- 14 Ars affix-loot equipment entries, 3 Ars gear sets and 3 regular Wilden invaders are source-closed.
- Ancient variants exist in source but also require Ancient Reforging; no Ancient Reforging identifier is present in the current physical modlist, so those variants are not promoted to active-pack behavior.

### Malum boundary

- Physical Malum: 1.8.2.
- Exactly 3 provider gems: `malum/soul_stained`, `malum/thief`, `malum/etheric` under the `apothic_compats` namespace.
- Provider definitions consume Malum/Lodestone/Apothic attributes and effects, including Soul Ward, scythe proficiency, charge, arcane resonance and magic-stat surfaces.
- `ModAffixRegistry` conditionally registers exactly 4 Malum custom affix codecs: `scythe_thunderstruck`, `scythe_cleaving`, `staff_thunderstruck`, `staff_cleaving`.
- Cleaving may issue additional normal player attacks against nearby eligible entities with a provider-local recursion guard.
- Thunderstruck applies nearby provider-created mob-attack damage tagged lightning and bypass-armor.
- These are provider affix procs, not Black Arcana spells or Backlash.

### Runtime glue boundary

- `AttributeEvents` processes server-side projectile join, scales projectile velocity by Apothic `ARROW_VELOCITY`, and uses persistent-data boolean `apothic_compats.proj.done` to prevent repeat application.
- The marker is one-shot event deduplication, not a player/world magic persistence subsystem.
- `AffixEvents` handles a high-priority invulnerability check and delegates only to provider Aether/Create affix helpers when those targets are loaded.
- No mod ID `ae2` is present in the physical inventory; source AE2 compatibility remains dormant in this snapshot.

### Provider authority

- Apotheosis/Apothic owns affix, gem, loot, category, invader and generic attribute/proc semantics.
- Ars Nouveau owns Ars spells, mana, effects, entities and equipment runtime.
- Malum/Lodestone owns Malum magic attributes/effects/charge/Soul Ward/item semantics.
- Apothic Enchanting owns its Eterna/Quanta/Arcana enchanting-stat semantics; provider `Arcana` does not equal Black Arcana `Arcane Danger`.
- Apothic Compats owns only its compatibility definitions, custom affix codecs, conditional Curios content and exact observed event/mixin glue.
- Black Arcana retains canonical server-authoritative casting, transactional costs, targeting, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- BA must not duplicate the projectile velocity pass, create a second Ars/Malum resource settlement path, or re-enter Cleaving/Thunderstruck as BA offensive proc chains.
- RPG Skill Tree receives no runtime authority.

### Canonicalization gate

Component #47 is only represented by this branch until the final gate. It becomes canonical after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge and post-merge `main` confirmation. Phase 3 remains blocked.

## Immediate canonical predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 46 | Phase 2AR / PR #154 | `backportedspellbooks` | CANÔNICO em `main@ac4df420158616d2fb993fb5fbf6b8325c207c27`; 6 spells + Pale Flora + bounded content/worldgen/procs |
| 45 | Phase 2AQ / PR #152 | `apothic_compat` | CANÔNICO em `bdf5271c265b5f40ee5a9e7695c7d71374a4c31c`; 0 spells, 13 loot-category overrides + affix blacklist compat |
| 44 | Phase 2AP / PR #151 | `create_enchantment_industry_plus` | CANÔNICO; PR #153 posterior corrigiu metadata com zero delta |
| 43 | Phase 2AO / PR #150 | `soul_fire_d` | CANÔNICO |
| 42 | Phase 2AN / PR #149 | `apothic_attributes` | CANÔNICO |
| 41 | Phase 2AM / PR #147 | `reliquified_lenders_cataclysm_new_relics_fix` | CANÔNICO |
| 40 | Phase 2AL / PR #145 | `efiscompat` | CANÔNICO |
| 39 | Phase 2AK / PR #144 | `emf_compat_iron_spells` | CANÔNICO |
| 38 | Phase 2AJ / PR #143 | `aces_spell_utils` | CANÔNICO |
| 37 | Phase 2AH / PR #140 | `monstersspellbooks` | CANÔNICO |
| — | Phase 2AI / PR #141 | `somakespells` | re-audit canônico, zero delta; permanece parcial |
| 36 | Phase 2AG / PR #137 | `ars_n_spells` | CANÔNICO |
| 35 | Phase 2AF / PR #135 | `not_enough_glyphs` | CANÔNICO |

O detalhamento completo anterior permanece no snapshot PRE-PHASE2AS e nos arquivos individuais de provider/phase.

## Concorrência — não colidir

A Phase 2AS foi criada sobre `main@ac4df420158616d2fb993fb5fbf6b8325c207c27`. Nenhum PR/branch equivalente de Apothic Compats foi encontrado no gate inicial.

Antes do merge:

1. buscar `origin/main` novamente;
2. se `main` avançou, reconciliar semanticamente a branch antes de validar;
3. não usar CI anterior à última reconciliação como evidência final;
4. revisar diff final para garantir escopo documental e preservação de trabalhos simultâneos;
5. executar/confirmar CI no HEAD exato reconciliado;
6. somente então mergear e confirmar SHA final da `main`.

## Próxima seleção após Phase 2AS

Selecionar somente depois de:

1. latest-main gate imediatamente pré-merge;
2. CI GREEN no HEAD reconciliado da Phase 2AS;
3. merge e confirmação do `main` final;
4. CI pós-merge no SHA exato da main, quando aplicável;
5. verificação da modlist física atual;
6. pesquisa de PR/branch equivalente;
7. leitura do catálogo já canônico;
8. confirmação da versão exata e do melhor source/API/release aplicável.

Continuar preferindo componentes cuja superfície atual possa ser fechada sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais sob a evidência atual.

## Providers parcialmente fechados — não contam como concluídos

Exemplos atuais:

- `leylines` — nomes públicos parciais; inventário total atual não verificado;
- `somakespells` — exact artifact/release e release-line auditados, mas inventário granular atual ainda não fechado;
- `cataclysm_spellbooks` — artefato instalado 1.1.13 sem source público exato equivalente já fechado;
- `gaze` — superfície pública auditada, mas registry/source-JAR exato ainda não fechado.

## Regras de fila

- presença/versão vêm da modlist/JAR atual, não do snapshot histórico;
- README preparatório, guia lido ou branch antiga não equivale a catálogo canônico;
- source público de versão diferente não autoriza promover internals da versão instalada;
- exact source-version pin não equivale automaticamente a byte-for-byte JAR reproducibility;
- library/API ou compat provider pode fechar com zero spells se zero registro próprio for demonstrado e suas superfícies reais estiverem inventariadas;
- compatibility bridge pode fechar semanticamente no publisher/source evidence ceiling quando o escopo atual é explicitamente bounded, mantendo internals não provados fail-closed;
- API/framework que migrou para sibling provider deve manter authority no provider atual;
- client presentation hook não é cast authority;
- cross-provider cast cancellation/reconciliation não vira segundo cast authority;
- registry/example/animation/compatibility/fire/recipe/data-map/affix/gem object não vira spell por contagem;
- provider magic attribute/resource referenced by a compat does not transfer that resource authority to the compat or to Black Arcana;
- capabilities repacked mantêm provenance/namespace e não criam duplicata semântica automaticamente;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, targeting, summon lifecycle, proc pipeline, relic migration/settlement, fire-framework settlement, recipe/resource settlement, loot-category/affix/gem settlement, presentation adapter, projectile attribute pass ou world mutation de provider;
- private reflection usada internamente por provider não é automaticamente API de integração segura para Black Arcana;
- source-family label ou Java symbol não deve ser confundido com registry ID sem evidência;
- provider parcial continua zero até inventário atual fechar ao teto de evidência aceito;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para o estado operacional detalhado imediatamente anterior a esta Phase 2AS, consultar `PROVIDER-AUDIT-QUEUE-PRE-PHASE2AS.md`.

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha histórica, reconciliar presença e versão contra a modlist física atual.
