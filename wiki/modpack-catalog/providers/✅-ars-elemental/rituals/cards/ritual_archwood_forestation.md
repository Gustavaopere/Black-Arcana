# Ars Elemental 0.7.10.1 — `ars_elemental:ritual_archwood_forestation`

**✅ Prova binária exata (2026-10-13):** `ars_elemental:ritual_archwood_forestation` está inscrito por `ArsNouveauRegistry.registerRituals → RitualRegistry.registerRitual` no JAR físico/publicador 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`), [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para ID estático, **+0** novas raízes; `COUNTED_SOURCE_PINNED` abaixo descreve o checkpoint histórico de defaults. Custos Source e comportamento de runtime/Survival ⚠️. [Dossiê](../../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — ritual individualizado** · **⚠️ config/QA Survival pendentes**.

## Identidade do source

- **Registry ID:** `ars_elemental:ritual_archwood_forestation`, registrado em Ars `RitualRegistry` pelo `ArsNouveauRegistry.registerRituals()`.
- **Posição editorial:** 8/8, sem relevância para registro/execução.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.


## Contrato e defaults auditados

Extends exact Ars Nouveau 5.13.1 `FeaturePlacementRitual`.

Provider-specific behavior:

- always adds a Bonemeal feature;
- a consumed specific Archwood sapling selects Blazing, Cascading, Vexing, Flourishing or Flashing feature families;
- selected families place their corresponding tree, thematic resource/plant and Archfruit Pod;
- without a specific variant it draws from all five Archwood tree families and all five pod families;
- adds provider `PlaceableLightFeature` after the variant features.

Inherited exact behavior:

- base `checkRadius`: 7;
- each consumed Ars Source Gem increases `checkRadius` by its stack count;
- target positions are generated within the radius, shuffled, and processed feature-by-feature;
- the tick loop returns after one successful feature placement, or advances until the ritual finishes;
- `featureIndex`, `positionIndex` and `checkRadius` are persisted;
- the base class does not override `getSourceCost()`; exact `AbstractRitual.getSourceCost()` therefore supplies **0**.

The Source Gems here are radius augment inputs. The inherited source path does not establish an ongoing positive Source pull for this ritual at this pin.

## Causalidade, segurança e QA

Os campos acima reproduzem os contratos factuais da auditoria do source e do Ars 5.13.1 quando herdados. Não constituem medição no pack físico. Recursos Source, alteração de blocos/biomas, entidades, scheduler, persistência e cleanup permanecem provider-owned. Black Arcana não cobra Source duas vezes nem reexecuta rituais; efeitos destrutivos próprios passam por `WorldEffectPolicy`. Sem hook real, integração **⛔ fail-closed**.

**Fontes:** [rituais](../../RITUALS.md) · [registries](../../REGISTRIES.md) · [acquisition](../../ACQUISITION.md). Clean-room factual, sem código/JSON/assets upstream.

## Engenharia de perks — contrato causal do ritual 0.7.10.1

- **Source checkpoint exato:** [`ArchwoodForestationRitual.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/rituals/forest/ArchwoodForestationRitual.java). Pin de versionamento, **não** prova binária de equivalência da implementação ao JAR.
- **Executor herdado:** [Ars Nouveau ConjureBiomeRitual/FeaturePlacementRitual](https://github.com/baileyholl/Ars-Nouveau/tree/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual) no host 5.13.1.
- **Executor confirmado:** estende `FeaturePlacementRitual` Ars 5.13.1: Source Gem incrementa checkRadius a partir de 7; alvos embaralhados em raio, avanço por posições, retorna após um `onPlace` bem-sucedido, persiste `featureIndex`, `positionIndex` e `checkRadius` no pai.
- **Seleção/outputs:** `addFeatures` sempre inclui `BonemealFeature(6,0.4)` e `PlaceableLightFeature(4,0.1)`; `biomeType` 0..4 seleciona Blazing, Cascading, Vexing, Flourishing ou Flashing tree (RandomTreeFeature distance8/chance0.8), planta tema e Archpod; default -1 mistura cinco tipos de árvore e diferentes Archpods.
- **Mutação em admissão:** `canConsumeItem(stack)` modifica `biomeType` quando recebe sapling selecionável; também o redefine para -1 em stack não-seletor e só chama super/retorna o resultado no final. Isto é detalhe operacional a verificar em reload/ordem de consumo: não interpretar verificação como função pura.
- **QA/perks:** `biomeType` não é serializado neste trecho pelo addon (pai só index/radius). Persistência exata da variante após reload não está demonstrada; não alterar Source ou plano de feature por perk.
- **Estado:** ✅ ID física do JAR e assinatura do source pinned; ⚠️ equivalência implementation-JAR, config deploy, helpers/host, protection e Survival pendentes; ⛔ adapter de perks RPG e mutabilidade externa não comprovados. Sem dupla Source/cast/concessão de Mastery.
