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

- Phase 2AF / PR #135 está canônica em `main@6ef2fb6fee567dc4fbe3d340166829d042132bfb`;
- cobertura canônica antes da Phase 2AG: **35/100 = 35%**;
- esta revisão Phase 2AG fecha `ars_n_spells` como componente #36;
- quando esta revisão estiver em `main`: **36/100 = 36%**;
- provider parcial não recebe ponto inteiro;
- denominador 100 permanece operacional e deve ser reconciliado se a modlist física mudar.

## Phase 2AG — Ars 'n' Spells

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `ars_n_spells` | `ars_n_spells-3.3.2.jar` | EXACT PHYSICAL/RELEASE 3.3.2 / OFFICIAL NEOFORGE 1.21.1 SOURCE BASELINE 3.3.0 @ `a9930223...` / 5 RITUAIS SOB PACK COM IRON'S / 5 MANA MODES / SPELL LOOM + CARRIERS / 8 PROXY TRANSPORT SLOTS, 0 STANDALONE SEMANTIC SPELLS / EXACT 3.3.2 INTERNALS UNVERIFIED / PHASE 2AG CLOSURE REVISION |

### Evidence boundary

- Exact physical JAR SHA-1: `2d2274ff786c42ea46c53fec866116f83d98fe5a`.
- Exact 3.3.1 release removes the transaction receipt HUD.
- Exact 3.3.2 release fixes contextual Iron's mana-HUD visibility and declares no config, network-protocol or save-format change from 3.3.1.
- Official NeoForge 1.21.1 source branch is version 3.3.0, not 3.3.2; class/signature/registry parity on the installed binary is therefore not invented.
- The current semantic catalog records five ritual identities, five mana modes, the provider-owned carrier/cross-cast lifecycle and the fixed eight-slot Iron's proxy pool.
- `ars_cross_1..8` are real registry objects used as transport slots; they do not create eight fixed semantic spells for deduplication.

## Phase 2AF — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `not_enough_glyphs` | `not_enough_glyphs-1.21.1-4.6.1.jar` | CANÔNICO VIA PR #135 / SOURCE-PINNED 4.6.1 / 40 REGISTROS CONDICIONAIS / 39 SOURCE-ENABLED / 4 FORMS + 36 EFFECTS / BINDER 25 STORAGE + 10 CASTER / 13 PERKS |

A antiga marcação de NEG como `CATÁLOGO GRANULAR PENDENTE` permanece obsoleta.

## Concorrência — não colidir

Rechecado na abertura da Phase 2AG. Continuam abertos trabalhos dedicados para:

- `ars_two_way_portals` — PR #125;
- `ars_polymorphia` — PR #126;
- `ars_sable` — PR #128.

Esses providers não devem ser editados por esta fase. Rechecá-los novamente antes de qualquer seleção futura.

## Próxima seleção após Phase 2AG

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
- Black Arcana não duplica mana, casting, cooldown, contingency, targeting ou world mutation de provider;
- proxy/bridge transport identity não deve ser confundida com spell semântico adicional;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.