# Ars Nouveau — Evaporate

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / CLAIM/RUNTIME QA PENDING`

- Registry id: `ars_nouveau:glyph_evaporate`
- Display name: Evaporate
- School: Manipulation
- Default tier: 1
- Default mana cost: 50
- Compatible augments: AOE, Pierce

## Provider-native behavior

Evaporate removes fluid blocks in the affected area and clears the `WATERLOGGED` property on compatible waterlogged blocks. AOE/Pierce expand coverage, and the implementation also checks adjacent directions around each calculated target position.

## Safety note

The inspected `EffectEvaporate` path does not itself show the claim check used by several other Ars block-mutating effects. That absence is recorded as a runtime/full-pack protection QA item rather than silently assuming equivalent protection behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:sponge` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this fluid-removal spell. Independent Black Arcana fluid destruction must route through `WorldEffectPolicy`; Black Arcana must not replay an Ars Evaporate mutation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectEvaporate`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectEvaporate.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectEvaporate.java), Ars Nouveau 5.13.1.
- **Geometria:** `onResolveBlock` percorre `SpellUtil.calcAOEBlocks(...AOE,count(Pierce))` e chama `evaporate` na posição **e em todas as seis direções**; potencial 7 tentativas por candidato antes de overlaps, não 7 conversões garantidas.
- **Mutação:** se há FluidState não vazio **e** `state.getBlock() instanceof LiquidBlock`, muda para AIR; caso contrário se `SimpleWaterloggedBlock` com propriedade `WATERLOGGED`, altera a property para false. Em ambos os ramos pode propagar `ShapersFocus.tryPropagateBlockSpell`.
- **QA de proteção:** esta classe não chama `destroyRespectsClaim` no trecho mutador; é uma pendência para investigar admissão externa e claims, sem afirmar exploit. Mana default 50, augments apenas AOE/Pierce; não impor adicional via RPG nem usar o caminho Ars para WorldEffectPolicy de Black Arcana.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.
