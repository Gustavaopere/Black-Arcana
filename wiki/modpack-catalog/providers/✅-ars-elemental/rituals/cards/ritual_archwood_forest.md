# Ars Elemental 0.7.10.1 — `ars_elemental:ritual_archwood_forest`

**✅ Prova binária exata (2026-10-13):** `ars_elemental:ritual_archwood_forest` está inscrito por `ArsNouveauRegistry.registerRituals → RitualRegistry.registerRitual` no JAR físico/publicador 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`), [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para ID estático, **+0** novas raízes; `COUNTED_SOURCE_PINNED` abaixo descreve o checkpoint histórico de defaults. Custos Source e comportamento de runtime/Survival ⚠️. [Dossiê](../../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — ritual individualizado** · **⚠️ config/QA Survival pendentes**.

## Identidade do source

- **Registry ID:** `ars_elemental:ritual_archwood_forest`, registrado em Ars `RitualRegistry` pelo `ArsNouveauRegistry.registerRituals()`.
- **Posição editorial:** 7/8, sem relevância para registro/execução.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.


## Contrato e defaults auditados

Extends exact Ars Nouveau 5.13.1 `ConjureBiomeRitual`.

Provider-specific behavior:

- base biome target is Ars Nouveau Archwood Forest;
- grass is placed at `ritualY - 1`, dirt at the other generated layers;
- at most one consumed Archfruit Pod changes the target biome:
  - Bombegrante -> Blazing Forest;
  - Frostaya -> Cascading Forest;
  - Mendosteen -> Flourishing Forest;
  - Bastion -> Vexing Caves;
  - Flashing Pod -> Flashing Forest;
- non-default selected biome is persisted in ritual NBT.

Inherited exact behavior:

- base radius: 7;
- each consumed Ars Source Gem adds its stack count to the radius;
- tracker is initialized around `getPos().below(3)` with the resolved radius;
- each successful placement also calls Ars `RitualUtil.changeBiome` for that position;
- `blocksBeforeSourceNeeded = 5`;
- after five successful block placements the ritual marks itself as needing Source;
- `getSourceCost()` returns 50;
- tracker and radius are persisted by the base ritual.

This means the source contract is **50 Ars Source per five successful placement steps**, not a Black Arcana cost and not a one-time 50-Source total inferred from the tablet description.

## Causalidade, segurança e QA

Os campos acima reproduzem os contratos factuais da auditoria do source e do Ars 5.13.1 quando herdados. Não constituem medição no pack físico. Recursos Source, alteração de blocos/biomas, entidades, scheduler, persistência e cleanup permanecem provider-owned. Black Arcana não cobra Source duas vezes nem reexecuta rituais; efeitos destrutivos próprios passam por `WorldEffectPolicy`. Sem hook real, integração **⛔ fail-closed**.

**Fontes:** [rituais](../../RITUALS.md) · [registries](../../REGISTRIES.md) · [acquisition](../../ACQUISITION.md). Clean-room factual, sem código/JSON/assets upstream.

## Engenharia de perks — contrato causal do ritual 0.7.10.1

- **Source checkpoint exato:** [`ArchwoodForestRitual.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/rituals/forest/ArchwoodForestRitual.java). Pin de versionamento, **não** prova binária de equivalência da implementação ao JAR.
- **Executor herdado:** [Ars Nouveau ConjureBiomeRitual/FeaturePlacementRitual](https://github.com/baileyholl/Ars-Nouveau/tree/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual) no host 5.13.1.
- **Herança confirmada:** estende `ConjureBiomeRitual` do Ars 5.13.1: raio base 7 somado à quantidade Source Gem-tag; `ManhattenTracker(brazier.below(3),radius,2,radius)`, no máximo um bloco colocado com sucesso por tick, `RitualUtil.changeBiome` em cada colocação, `getSourceCost=50`, `setNeedsSource(true)` a cada 5 placements.
- **Terreno/bioma:** GRASS_BLOCK na layer Y−1, DIRT nas demais; default biome ARCHWOOD_FOREST. Um Archfruit Pod consumido pode apontar BLazing/Bombegrante, Cascading/Frostaya, Flourishing/Mendosteen, Vexing/Bastion ou Flashing/Flashing Pod. `canConsumeItem` limita um Archfruit Pod e aceita Source Gems conforme super.
- **Persistência:** grava `biome` especial na NBT via `ResourceKey` e pai guarda tracker/radius; source não comprova proteção de claim por cada `setBlock`. **Perks:** nunca repetir worldgen, Source ou bioma.
- **Estado:** ✅ ID física do JAR e assinatura do source pinned; ⚠️ equivalência implementation-JAR, config deploy, helpers/host, protection e Survival pendentes; ⛔ adapter de perks RPG e mutabilidade externa não comprovados. Sem dupla Source/cast/concessão de Mastery.
