# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

Este arquivo é a fila operacional corrente. O snapshot detalhado de 2026-09-07 permanece preservado em [`PROVIDER-AUDIT-QUEUE-2026-09-07.md`](./PROVIDER-AUDIT-QUEUE-2026-09-07.md).

Autoridade física deste checkpoint:

- Minecraft 1.21.1;
- NeoForge `21.1.248`;
- modlist física mais recente: **595 entradas top-level**;
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- dependências internas/jarjar não contam como providers top-level.

O snapshot histórico de 2026-09-07 usava 612 entradas / 103 candidatos e não é mais autoridade de presença, versão nem denominador.

## Cobertura global

Ver [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

- Phase 2AH / PR #140 está canônica em `main@e8b7c4a0b77c2f803423047f5d1442f870d02fc8`;
- cobertura canônica atual: **37/100 = 37%**;
- Phase 2AI re-audita `somakespells` sob a regra atual de fechamento;
- Somake permanece parcial porque o inventário granular atual 1.0.8-fix não está fechado;
- Phase 2AI produz **0 delta de cobertura**;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AI — Somake Spells 1.0.8-fix

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `somakespells` | `somakespells-1.0.8-1.21.1-fix.jar` | EXACT PHYSICAL+RELEASE IDENTITY / OFFICIAL 1.0.x RELEASE SURFACE AUDITED / PUBLISHER `OVER 50` SCALE / COMPLETE CURRENT SPELL REGISTRY NOT AVAILABLE / EXACT SOURCE+API NOT LOCATED / AQUA↔T.O RUNTIME QA BLOCKED / ZERO COVERAGE DELTA / FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`.
- CurseForge project/file: `1461634 / 8417850`, exact 1.0.8-fix release dated 2026-07-12.
- Exact fix repairs Symmetry and Spirit Elemental Charges not applying buffs.
- Official 1.0.8/1.0.7/1.0.6 notes expose named spell/progression migrations, but they are not a cumulative registry manifest.
- Publisher says `over 50 spells`; this cannot be converted into exact count, IDs, school totals or current membership.
- No publisher-controlled exact 1.0.8-fix source revision or complete current registry/API table was located.
- The exact current JAR was not directly inspectable through the available repository/web tooling in this phase; no class/API/registry internals are invented.
- Physical `traveloptics` 1.21.1 alpha/deprecated coexistence keeps Somake Aqua authority/runtime interaction QA-blocked.

### Closure condition

Somake may only leave the partial bucket after trusted exact-current inventory evidence becomes available, such as a clean-room exact-artifact registry/resource inventory, publisher-controlled exact source/registry/API, or equivalent trusted exact inventory evidence. Runtime Aqua/T.O and optional-provider QA remain separate gates.

## Phase 2AH — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `monstersspellbooks` | `monstersspellbooks-0.0.16.3.jar` | CANÔNICO VIA PR #140 / EXACT PHYSICAL+RELEASE 0.0.16.3 / 98 SPELL REGISTRATIONS CLOSED SEMANTICALLY / NECRO+AERO SCHOOLTYPES OBSERVED IN SOURCE ONLY / AERO 0 SPELL REGISTRATIONS + INSTALLED AERO STATE UNVERIFIED AFTER 0.0.16.3 CLEANUP / EXACT BINARY NUMERICAL/API INTERNALS FAIL-CLOSED |

## Phase 2AG — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_n_spells` | `ars_n_spells-3.3.2.jar` | CANÔNICO VIA PR #137 / EXACT PHYSICAL+RELEASE 3.3.2 / OFFICIAL NEOFORGE SOURCE BASELINE 3.3.0 / 5 RITUAIS / 5 MANA MODES / SPELL LOOM+CARRIERS / 8 TRANSPORT PROXIES, 0 SPELLS SEMÂNTICOS INDEPENDENTES |

## Phase 2AF — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `not_enough_glyphs` | `not_enough_glyphs-1.21.1-4.6.1.jar` | CANÔNICO VIA PR #135 / SOURCE-PINNED 4.6.1 / 40 REGISTROS CONDICIONAIS / 39 SOURCE-ENABLED / 4 FORMS + 36 EFFECTS / BINDER 25 STORAGE + 10 CASTER / 13 PERKS |

## Concorrência — não colidir

Phase 2AI reutiliza a árvore Somake já canônica da antiga Phase 2O / PR #86. Não existe PR Somake aberto equivalente no início desta fase; a nova branch foi criada sobre a `main` atual em vez de reviver a branch histórica stale.

Antes de selecionar qualquer provider seguinte, reexecutar pesquisa de PRs/branches; não confiar em listas de concorrência antigas.

## Próxima seleção após Phase 2AI

Como Somake permanece parcial, o próximo provider deve ser escolhido por probabilidade real de fechamento, não pela ordem histórica. Antes da seleção:

1. fetch da `main` mais recente;
2. verificação da modlist física atual;
3. pesquisa de PR/branch equivalente;
4. leitura do catálogo já canônico;
5. confirmação da versão exata e do melhor source/API/release aplicável.

Preferir um componente cujo inventário atual possa ser fechado sem inferência. `cataclysm_spellbooks`, `gaze` e `leylines` permanecem candidatos parciais a reavaliação, sujeitos a evidência e concorrência atuais.

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
- capabilities repacked mantêm provenance/namespace e não criam duplicata semântica automaticamente;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, targeting, summon lifecycle ou world mutation de provider;
- source-family label não deve ser confundido com SchoolType sem evidência;
- provider parcial continua zero até inventário atual fechar ao teto de evidência aceito;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.