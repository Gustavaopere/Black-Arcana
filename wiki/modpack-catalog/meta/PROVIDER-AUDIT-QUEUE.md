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

- Phase 2AG / PR #137 está canônica em `main@2de722272814d2d5664266f5fc8ad05ba25d2940`;
- cobertura canônica antes da Phase 2AH: **36/100 = 36%**;
- esta revisão Phase 2AH fecha `monstersspellbooks` como componente #37 ao limite de evidência disponível;
- quando esta revisão estiver em `main`: **37/100 = 37%**;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AH — Monsters & Spellbooks

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `monstersspellbooks` | `monstersspellbooks-0.0.16.3.jar` | EXACT PHYSICAL/RELEASE 0.0.16.3 / CURRENT OFFICIAL SOURCE HEAD `1ab9b72a...` WITH STALE 0.0.14 METADATA / 98 SPELL REGISTRATIONS CLOSED SEMANTICALLY / NECRO SCHOOL ACTIVE / AERO SCHOOL RETAINED BUT 0 ACTIVE REGISTRATIONS AFTER SOFT DELETE / EXACT 0.0.16.3 NUMERICAL/API INTERNALS UNVERIFIED / PHASE 2AH CLOSURE REVISION |

### Evidence boundary

- Physical JAR SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`.
- CurseForge project/file: `1428928 / 8788560`, exact 0.0.16.3 release dated 2026-09-01.
- Current official source head: `RedReaper28/Monsters-Spellbooks-1.21.1@1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`.
- Current public `ModSpellRegistry` contains **98** explicit registrations: 5 blood, 12 ender, 3 evocation, 10 fire, 4 holy, 8 hydro, 8 ice, 14 lightning, 7 nature, 25 necro, 2 technomancy.
- Public release-work compare from `823532a3...` to `1ab9b72a...` does not modify `ModSpellRegistry`, supporting inventory stability through the 0.0.16.2/0.0.16.3 work interval.
- Exact 0.0.16.2 release says Aero was soft-deleted. Current source still registers an Aero SchoolType but zero Aero spell registrations.
- Source `gradle.properties` remains stale at `mod_version=0.0.14`, NeoForge 21.1.216 and Iron's 3.15.4; therefore exact installed-JAR class/API/numeric parity is not invented.

## Phase 2AG — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_n_spells` | `ars_n_spells-3.3.2.jar` | CANÔNICO VIA PR #137 / EXACT PHYSICAL+RELEASE 3.3.2 / OFFICIAL NEOFORGE SOURCE BASELINE 3.3.0 / 5 RITUAIS / 5 MANA MODES / SPELL LOOM+CARRIERS / 8 TRANSPORT PROXIES, 0 SPELLS SEMÂNTICOS INDEPENDENTES |

## Phase 2AF — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `not_enough_glyphs` | `not_enough_glyphs-1.21.1-4.6.1.jar` | CANÔNICO VIA PR #135 / SOURCE-PINNED 4.6.1 / 40 REGISTROS CONDICIONAIS / 39 SOURCE-ENABLED / 4 FORMS + 36 EFFECTS / BINDER 25 STORAGE + 10 CASTER / 13 PERKS |

## Concorrência — não colidir

Rechecado na abertura da Phase 2AH. Não existe PR/branch equivalente para `monstersspellbooks`.

Antes de selecionar qualquer provider seguinte, reexecutar pesquisa de PRs/branches; não confiar em listas de concorrência antigas.

## Próxima seleção após Phase 2AH

Selecionar somente depois de:

1. fetch da `main` mais recente;
2. verificação da modlist física atual;
3. pesquisa de PR/branch equivalente;
4. leitura do catálogo já canônico;
5. confirmação da versão exata e do melhor source/API/release aplicável.

Não escolher automaticamente um provider apenas porque o snapshot histórico ainda diz `PENDENTE`; PRs recentes e a árvore atual de `main` são a autoridade operacional.

## Providers parcialmente fechados — não contam como concluídos

Exemplos atuais:

- `leylines` — nomes públicos parciais; inventário total atual não verificado;
- `somakespells` — catálogo granular atual ainda não fechado;
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
- provider-retained school objects sem spell registrations não devem inflar o inventário ativo;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.