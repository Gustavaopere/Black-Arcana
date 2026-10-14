# Ars Elemental 0.7.10.1 — `ars_elemental:ritual_pollination`

**✅ Prova binária exata (2026-10-13):** `ars_elemental:ritual_pollination` está inscrito por `ArsNouveauRegistry.registerRituals → RitualRegistry.registerRitual` no JAR físico/publicador 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`), [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para ID estático, **+0** novas raízes; `COUNTED_SOURCE_PINNED` abaixo descreve o checkpoint histórico de defaults. Custos Source e comportamento de runtime/Survival ⚠️. [Dossiê](../../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — ritual individualizado** · **⚠️ config/QA Survival pendentes**.

## Identidade do source

- **Registry ID:** `ars_elemental:ritual_pollination`, registrado em Ars `RitualRegistry` pelo `ArsNouveauRegistry.registerRituals()`.
- **Posição editorial:** 3/8, sem relevância para registro/execução.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.


## Contrato e defaults auditados

- Accelerates nearby Bee pollination progress in radius 15.
- Adds 100 to `successfulPollinatingTicks` when a bee is actively pollinating.
- Uses a persisted backoff field to reduce work when no bees are relevant.
- Explicit Source cost: 10.

## Causalidade, segurança e QA

Os campos acima reproduzem os contratos factuais da auditoria do source e do Ars 5.13.1 quando herdados. Não constituem medição no pack físico. Recursos Source, alteração de blocos/biomas, entidades, scheduler, persistência e cleanup permanecem provider-owned. Black Arcana não cobra Source duas vezes nem reexecuta rituais; efeitos destrutivos próprios passam por `WorldEffectPolicy`. Sem hook real, integração **⛔ fail-closed**.

**Fontes:** [rituais](../../RITUALS.md) · [registries](../../REGISTRIES.md) · [acquisition](../../ACQUISITION.md). Clean-room factual, sem código/JSON/assets upstream.

## Engenharia de perks — contrato causal do ritual 0.7.10.1

- **Source checkpoint exato:** [`PollinationRitual.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/rituals/PollinationRitual.java). Pin de versionamento, **não** prova binária de equivalência da implementação ao JAR.
- **Clock/backoff:** `getBackoff()` retorna `60+backoff`; valor inicial 0, quando não há abelhas e não houve trabalho `setBackoff(100)` (ciclo passa de 60 para 160 game ticks); senão volta a 0. Campo `backoff` é serializado em NBT.
- **Targets:** procura `Bee` em AABB `inflate(15)`, e para cada abelha com `bee.beePollinateGoal.isPollinating()`, aumenta `successfulPollinatingTicks += 100`. Variável `flag` acumula `!bee.hasNectar()` por OR; apenas quando `flag` é true marca `setNeedsSource(true)`. Isto acelera *pollination* da abelha, **não** o estado de mel do hive.
- **Source:** custo declarado 10, sem afirmar cobrança por abelha; acesso aos campos do objetivo da abelha é provider-native, não API garantida para adapter RPG.
- **Estado:** ✅ ID física do JAR e assinatura do source pinned; ⚠️ equivalência implementation-JAR, config deploy, helpers/host, protection e Survival pendentes; ⛔ adapter de perks RPG e mutabilidade externa não comprovados. Sem dupla Source/cast/concessão de Mastery.
