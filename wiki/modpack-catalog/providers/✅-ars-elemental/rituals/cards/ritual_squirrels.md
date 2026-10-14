# Ars Elemental 0.7.10.1 — `ars_elemental:ritual_squirrels`

**✅ Prova binária exata (2026-10-13):** `ars_elemental:ritual_squirrels` está inscrito por `ArsNouveauRegistry.registerRituals → RitualRegistry.registerRitual` no JAR físico/publicador 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`), [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para ID estático, **+0** novas raízes; `COUNTED_SOURCE_PINNED` abaixo descreve o checkpoint histórico de defaults. Custos Source e comportamento de runtime/Survival ⚠️. [Dossiê](../../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — ritual individualizado** · **⚠️ config/QA Survival pendentes**.

## Identidade do source

- **Registry ID:** `ars_elemental:ritual_squirrels`, registrado em Ars `RitualRegistry` pelo `ArsNouveauRegistry.registerRituals()`.
- **Posição editorial:** 5/8, sem relevância para registro/execução.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.


## Contrato e defaults auditados

- Name: Fast Squirrels.
- Targets Ars Starbuncles.
- Radius 15, doubled to 30 when Gold Block was consumed.
- Refresh interval comes from `SQUIRREL_REFRESH_RATE`; source default is 600 ticks.
- Applies Movement Speed amplifier 1 for 2400 ticks and Jump amplifier 0 for 2400 ticks.
- Explicit Source cost: 150.

## Causalidade, segurança e QA

Os campos acima reproduzem os contratos factuais da auditoria do source e do Ars 5.13.1 quando herdados. Não constituem medição no pack físico. Recursos Source, alteração de blocos/biomas, entidades, scheduler, persistência e cleanup permanecem provider-owned. Black Arcana não cobra Source duas vezes nem reexecuta rituais; efeitos destrutivos próprios passam por `WorldEffectPolicy`. Sem hook real, integração **⛔ fail-closed**.

**Fontes:** [rituais](../../RITUALS.md) · [registries](../../REGISTRIES.md) · [acquisition](../../ACQUISITION.md). Clean-room factual, sem código/JSON/assets upstream.

## Engenharia de perks — contrato causal do ritual 0.7.10.1

- **Source checkpoint exato:** [`SquirrelRitual.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/rituals/SquirrelRitual.java). Pin de versionamento, **não** prova binária de equivalência da implementação ao JAR.
- **Filtro/alcance:** somente `Starbuncle` em AABB expandida por `15*modifier`, `modifier=2` se Gold Block foi consumido, senão 1. `canConsumeItem` aceita um `Items.GOLD_BLOCK` apenas enquanto lista de consumidos vazia.
- **Cadência:** opera quando `server.gameTime%Common.SQUIRREL_REFRESH_RATE.get()==0`, default 600 ticks no catálogo. Aplica `MOVEMENT_SPEED` por 2400 ticks amplifier1 e `JUMP` por 2400 ticks amplifier0; chama `setNeedsSource(true)` dentro do loop quando Starbuncle existe. Cost declarado 150.
- **Perks:** manter efeitos de entidade, raio e Source como provider-owned; `getSourceCost` não prova debit por Starbuncle ou por refresh.
- **Estado:** ✅ ID física do JAR e assinatura do source pinned; ⚠️ equivalência implementation-JAR, config deploy, helpers/host, protection e Survival pendentes; ⛔ adapter de perks RPG e mutabilidade externa não comprovados. Sem dupla Source/cast/concessão de Mastery.
