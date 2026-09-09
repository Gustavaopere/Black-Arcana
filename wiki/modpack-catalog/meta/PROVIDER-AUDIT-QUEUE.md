# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

Este arquivo é a fila **operacional corrente**. O snapshot detalhado anterior foi preservado sem alterações em [`PROVIDER-AUDIT-QUEUE-2026-09-07.md`](./PROVIDER-AUDIT-QUEUE-2026-09-07.md).

Autoridade física deste checkpoint:

- Minecraft 1.21.1;
- NeoForge `21.1.248`;
- modlist física mais recente: **595 entradas top-level**;
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- dependências internas/jarjar não contam como providers top-level.

O snapshot histórico de 2026-09-07 usava **612 entradas / 103 candidatos** e não é mais autoridade de presença, versão nem denominador de progresso.

## Cobertura global

Ver [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

- cobertura canônica em `main` antes da Phase 2AF: **34/100 = 34%**;
- Phase 2AF / PR #135 fecha `not_enough_glyphs` como candidato #35;
- após merge da PR #135: **35/100 = 35%**;
- provider parcial não recebe ponto inteiro;
- o denominador de 100 é operacional e deve ser alterado se a reconciliação física dos 595 rows mudar o conjunto magic/cross-domain.

## Phase 2AF — trabalho ativo

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `not_enough_glyphs` | `not_enough_glyphs-1.21.1-4.6.1.jar` | SOURCE-PINNED 4.6.1 / 40 REGISTROS CONDICIONAIS NO PACK / 39 SOURCE-ENABLED / 4 FORMS + 36 EFFECTS / BINDER 25 STORAGE + 10 CASTER / 13 PERKS / PR #135 — CANDIDATO A CANÔNICO NO MERGE |

A antiga marcação `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` para NEG está obsoleta e não deve recolocar o provider na fila após o merge.

## Concorrência — não colidir

No checkpoint de abertura da Phase 2AF havia trabalho concorrente dedicado para:

- `ars_two_way_portals` — PR #125;
- `ars_polymorphia` — PR #126;
- `ars_sable` — PR #128.

Esses owners devem ser rechecados antes de qualquer nova edição porque PRs podem fechar/mergear entre checkpoints.

## Próxima seleção

O próximo provider só pode ser escolhido após:

1. novo fetch de `origin/main`;
2. verificação da modlist física atual;
3. pesquisa de branch/PR equivalente;
4. leitura do catálogo já presente em `main`;
5. confirmação da versão exata e do source/API/release aplicável.

`ars_n_spells` é um candidato de alta prioridade porque a modlist física atual contém **3.3.2**, enquanto o snapshot histórico registrava 3.3.0 e material anterior catalogava 3.2.4. Portanto qualquer detalhe não revalidado em 3.3.2 permanece fail-closed.

## Providers parcialmente fechados — não contam como concluídos

Exemplos atuais:

- `leylines` — nomes públicos parciais; inventário total atual não verificado;
- `somakespells` — catálogo granular atual ainda não fechado;
- `cataclysm_spellbooks` — artefato instalado 1.1.13 sem source público exato equivalente já fechado;
- `gaze` — superfície pública auditada, mas registry/source-JAR exato ainda não fechado.

## Regras de fila

- presença/versão vêm da modlist/JAR atual, não do snapshot histórico;
- um README preparatório, guia lido ou branch antiga não equivale a catálogo canônico;
- source público de versão diferente não autoriza promover internals da versão instalada;
- capability repacked mantém provenance/namespace e não cria duplicata semântica;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, contingency, targeting ou world mutation de provider;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar sua presença e versão contra a modlist física atual de 595 entradas.