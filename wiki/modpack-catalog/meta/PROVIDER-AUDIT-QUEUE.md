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

- Phase 2AF / PR #135 fechou componente #35;
- Phase 2AG / PR #137 está canônica em `main@2de722272814d2d5664266f5fc8ad05ba25d2940` e fechou componente #36;
- cobertura canônica atual: **36/100 = 36%**;
- Phase 2AH avança `monstersspellbooks` apenas como checkpoint parcial e soma **0 pontos**;
- provider parcial não recebe ponto inteiro;
- denominador 100 permanece operacional e deve ser reconciliado se a modlist física mudar.

## Phase 2AH — Monsters & Spellbooks

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `monstersspellbooks` | `monstersspellbooks-0.0.16.3.jar` | EXACT PHYSICAL/RELEASE 0.0.16.3 / SHA-1 `b3aa89fd...` / CF `1428928/8788560` / PUBLIC CURRENT SOURCE HEAD `1ab9b72...` WITH STALE BUILD METADATA 0.0.14 / 98 SOURCE-BASELINE SPELL REGISTRATIONS / SOURCE SCHOOLS NECRO+AERO / EXACT CURRENT REGISTRY/API+AERO STATE UNVERIFIED / PARTIAL / 0 NEW COVERAGE POINTS |

### Phase 2AH evidence boundary

- Current publisher surface says `90+ spells` and `2 new spell schools`.
- Official public source head registers 98 spell objects across 11 families but its build metadata still declares mod `0.0.14`, NeoForge `21.1.216` and Iron's `1.21.1-3.15.4`.
- Exact installed pack uses 0.0.16.3, NeoForge `21.1.248` and Iron's `1.21.1-3.16.3`.
- Exact 0.0.16.3 changelog says some Aero remnants were removed; public source still registers an Aero school and no Aero spells. Current Aero state is therefore fail-closed.
- CurseForge says MIT while source `gradle.properties` says All Rights Reserved; `TEMPLATE_LICENSE.txt` applies to the MDK template, not the addon implementation. Provenance remains review-required/read-only.

## Phase 2AG — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_n_spells` | `ars_n_spells-3.3.2.jar` | CANÔNICO VIA PR #137 / EXACT PHYSICAL+RELEASE 3.3.2 / OFFICIAL NEOFORGE 1.21.1 SOURCE BASELINE 3.3.0 / 5 RITUAIS / 5 MANA MODES / SPELL LOOM+CARRIERS / 8 PROXY TRANSPORT SLOTS, 0 STANDALONE SEMANTIC SPELLS / EXACT 3.3.2 INTERNALS FAIL-CLOSED |

## Concorrência — não colidir

Rechecado na abertura da Phase 2AH. Permanecem reservados por trabalhos dedicados:

- `ars_two_way_portals` — PR #125;
- `ars_polymorphia` — PR #126;
- `ars_sable` — PR #128.

Rechecar estado real das PRs antes da próxima seleção.

## Próxima seleção após Phase 2AH

O componente #37 continua disponível. Selecionar apenas depois de:

1. fetch da `main` mais recente;
2. verificação da modlist física atual;
3. pesquisa de PR/branch equivalente;
4. leitura do catálogo já canônico;
5. confirmação da versão exata e do melhor source/API/release aplicável.

Preferir um provider cuja evidência current-exact permita realmente fechar o componente; não inflar a cobertura para compensar blockers de artifact/source.

## Providers parcialmente fechados — não contam como concluídos

Exemplos atuais:

- `monstersspellbooks` — source baseline amplo, mas exact 0.0.16.3 registry/API parity não fechada;
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
- nomes temáticos (`soul`, `lich`, `gravity`, `space`, etc.) exigem comparação semântica, não equivalência automática;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.