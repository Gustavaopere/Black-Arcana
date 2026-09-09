# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

Este arquivo é a fila operacional corrente. O snapshot detalhado anterior à Phase 2AT foi preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AT.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AT.md). O snapshot histórico de 2026-09-07 permanece em [`PROVIDER-AUDIT-QUEUE-2026-09-07.md`](./PROVIDER-AUDIT-QUEUE-2026-09-07.md).

Autoridade física deste checkpoint:

- Minecraft 1.21.1;
- NeoForge `21.1.248`;
- modlist física mais recente: **595 entradas top-level**;
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- dependências internas/jarjar não contam como providers top-level.

O snapshot histórico de 2026-09-07 usava 612 entradas / 103 candidatos e não é mais autoridade de presença, versão nem denominador.

## Cobertura global

Ver [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

- `main@063135e690b4c066db582be1be6dd1e1387f1758` é a base canônica desta Phase 2AT;
- cobertura canônica nessa base: **47/100 = 47%**;
- Phase 2AS / PR #155 fechou `apothic_compats` como componente #47 e já está canônica; workflow pós-merge #2239 é GREEN no SHA exato;
- esta revisão Phase 2AT representa **48/100 = 48%** apenas como candidato até reconciliação final + CI GREEN + merge + confirmação pós-merge;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção preservada: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AT — Apothic Spawners 1.4.0 — candidate #48

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `apothic_spawners` | `ApothicSpawners-1.21.1-1.4.0.jar` | CANDIDATO PHASE 2AT / EXACT PHYSICAL 1.4.0 + EXACT OFFICIAL RELEASE SOURCE / SPAWNER LIFECYCLE+PERSISTENCE+MODIFIER PROVIDER / 0 SPELLS+GLYPHS+RITUALS / 0 CAST RESOURCE / 16 STATS / 32 STOCK MODIFIER RECIPES / 2 MIXINS / 1 CLIENTBOUND CONFIG PAYLOAD / NUCLEAR SPAWNER BOUNDED REACTION / COMPONENT #48 CANDIDATE / BYTE+FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical artifact `ApothicSpawners-1.21.1-1.4.0.jar`, mod ID `apothic_spawners`, version 1.4.0, SHA-1 `b3be29751daea738e691db8949cce079e5aae3be`.
- Publisher file: CurseForge project/file `986583 / 8469405`, released 2026-07-20 for NeoForge Minecraft 1.21.1.
- Official repository: `Shadows-of-Fire/Apothic-Spawners`.
- Exact release commit: `d3bc0b40d46bee476fc770f8e4e44a1c35ecddd3`, message `1.4.0`.
- Exact release tree: `7cd127fe22a9810b22bd8203cb2286d53b840e25`.
- The later `1.21` branch HEAD is five commits ahead only in translation/schema documentation; exact compare showed no Java/gameplay datapack drift.
- Exact source metadata closes Minecraft 1.21.1, Java 21, NeoForge 21.1.187+ and Placebo 9.9.0+; the physical pack has NeoForge 21.1.248 and Placebo 9.9.2.
- Complete exact source surface exposes **0 standalone spells, 0 glyphs, 0 rituals, 0 provider-owned mana/cast resource and no provider C2S cast-intent path**.

### Runtime / registry boundary

- Exact Java source count: 27 files.
- Exactly 16 `spawner_stat` registry identities.
- Exactly 32 stock modifier recipes: 16 direct + 16 inverse.
- Modifier operations observed: `add` and `set`.
- One `spawner_modifier` recipe type/serializer.
- One Capturing enchantment effect component, one modifier advancement trigger, one spawn-egg item-sub-predicate, entity blacklist tag and unstable-spawner loot key.
- Exactly 2 common mixins and 0 client mixins.
- Mixins replace the vanilla Spawner block/item implementation and `MOB_SPAWNER` block-entity factory with provider equivalents; they do not establish casting authority.
- Five config values.
- One PLAY clientbound configuration payload, protocol/version string `2`; no C2S spell/cast controller is present.
- Explicit tile NBT persistence includes stats, player-modified state, instability countdown and captured spawn data.
- Provider events own Capturing, Echoing loot/XP, No-AI/movable behavior, spawn-egg blacklist and spawner-specific despawn semantics.

### Nuclear Spawner boundary

Exact 1.4.0 behavior closes the bounded instability reaction:

- instability countdown: 60 ticks;
- provider removes/replaces the spawner as part of its own lifecycle;
- explosion radius: 8;
- 12 spawn attempts from the captured spawn snapshot;
- provider loot key `apothic_spawners:gameplay/unstable_spawner`.

This is a provider-owned world reaction, not a Black Arcana spell. For BA-caused destruction/mutation, BA first applies canonical `WorldEffectPolicy`. If that permitted world effect naturally transitions an Apothic spawner into provider instability, the subsequent provider transition remains Apothic Spawners authority and must not be processed a second time by BA.

### Provider authority

- Apothic Spawners owns spawner stats, modifier recipes, block/item/block-entity lifecycle, tile persistence, Capturing/Echoing, its config payload and Nuclear Spawner behavior.
- Black Arcana retains canonical server-authoritative casting, transactional costs, targeting, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- Capturing/Echoing are not promoted to BA spell identities merely because they have magical theming.
- BA must not duplicate the 16-stat modifier runtime, mirror provider NBT, add a second loot/XP pass, alter generic mob despawn from thematic similarity, or invoke provider Nuclear Spawner helpers to bypass world policy.
- RPG Skill Tree receives no spawner-runtime authority; any progression effect requires a real bounded contract rather than direct mutation of provider internals.

### License / clean-room boundary

License evidence remains layered rather than flattened: source code/generated metadata indicate MIT, source assets are All Rights Reserved, and the current CurseForge project surface labels the project All Rights Reserved. This audit is factual/read-only; no provider code/assets/text are copied into Black Arcana.

### Remaining fail-closed QA

- byte-for-byte source↔physical-JAR reproducibility;
- direct physical-vs-publisher-file hash equality;
- complete-modpack reload/event ordering;
- provider explosion interaction with protection/world-policy mods;
- alternate spawner implementation compatibility;
- external machine-spawner/summon integration.

These unresolved QA rows do not hide a known spell/cast surface; they remain runtime compatibility validation, not a reason to invent provider magic identities.

### Canonicalization gate

Component #48 is only represented by this branch until the final gate. It becomes canonical after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge and post-merge `main` confirmation. Phase 3 remains blocked.

## Immediate canonical predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 47 | Phase 2AS / PR #155 | `apothic_compats` | CANÔNICO em `main@063135e690b4c066db582be1be6dd1e1387f1758`; post-merge workflow #2239 GREEN |
| 46 | Phase 2AR / PR #154 | `backportedspellbooks` | CANÔNICO em `ac4df420158616d2fb993fb5fbf6b8325c207c27`; 6 spells + Pale Flora + bounded content/worldgen/procs |
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

O detalhamento completo anterior permanece no snapshot PRE-PHASE2AT e nos arquivos individuais de provider/phase.

## Concorrência — não colidir

A Phase 2AT foi criada sobre `main@063135e690b4c066db582be1be6dd1e1387f1758`. Nenhum PR/branch equivalente de Apothic Spawners foi encontrado no gate inicial; a branch corrente é `docs/magic-catalog-phase2at-apothic-spawners-1.4.0`.

Antes do merge:

1. buscar `origin/main` novamente;
2. verificar se o HEAD da própria branch/PR mudou;
3. se `main` avançou, reconciliar semanticamente a branch antes de validar;
4. não usar CI anterior à última reconciliação como evidência final;
5. revisar diff final para garantir escopo documental e preservação de trabalhos simultâneos;
6. executar/confirmar CI no HEAD exato reconciliado;
7. somente então mergear e confirmar SHA final da `main`.

## Próxima seleção após Phase 2AT

Selecionar somente depois de:

1. latest-main gate imediatamente pré-merge;
2. CI GREEN no HEAD reconciliado da Phase 2AT;
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
- registry/example/animation/compatibility/fire/recipe/data-map/affix/gem/spawner-stat/modifier object não vira spell por contagem;
- provider magic attribute/resource referenced by a compat does not transfer that resource authority to the compat or to Black Arcana;
- capabilities repacked mantêm provenance/namespace e não criam duplicata semântica automaticamente;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, targeting, summon lifecycle, proc pipeline, relic migration/settlement, fire-framework settlement, recipe/resource settlement, loot-category/affix/gem settlement, presentation adapter, projectile attribute pass, spawner modifier/persistence lifecycle ou world mutation de provider;
- private reflection usada internamente por provider não é automaticamente API de integração segura para Black Arcana;
- source-family label ou Java symbol não deve ser confundido com registry ID sem evidência;
- provider parcial continua zero até inventário atual fechar ao teto de evidência aceito;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para o estado operacional detalhado imediatamente anterior a esta Phase 2AT, consultar `PROVIDER-AUDIT-QUEUE-PRE-PHASE2AT.md`.

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha histórica, reconciliar presença e versão contra a modlist física atual.
