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

## Certificação técnica estática para perks — Evaporate (2026-10-25)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` associa `ars_nouveau:glyph_evaporate` à classe `EffectEvaporate`. Essa prova identifica registry/classfile, **não** garante equivalência dos métodos source. Sources `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectEvaporate.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectEvaporate.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java).

| Campo para perks | Fluxo e limitações confirmados no source |
|---|---|
| Targeting e geometria | `onResolveBlock` obtém `SpellUtil.calcAOEBlocks(shooter,hitPos,hit,getAoeMultiplier(),count(AugmentPierce))`. Para **cada** `BlockPos p` tenta `evaporate(world,p,...)` e depois **as seis** posições `p.relative(Direction.values())`: **7 chamadas por candidato AOE**, não 7 alterações confirmadas. Os deslocamentos podem se sobrepor entre candidatos e repetir o mesmo bloco. |
| Admissão do ramo líquido | `evaporate` lê `BlockState`; quando `!world.getFluidState(p).isEmpty()` **e** `state.getBlock() instanceof LiquidBlock`, chama `world.setBlock(p,Blocks.AIR.defaultBlockState(),3)`. O caminho não filtra especificamente `Fluids.WATER`: discrimina `FluidState` não vazio e LiquidBlock, inclusive conteúdos de mods que satisfizerem esses predicados. |
| Admissão do ramo waterlogged | Caso anterior não ocorra, quando `state.getBlock() instanceof SimpleWaterloggedBlock` e possui `BlockStateProperties.WATERLOGGED`, executa `state.setValue(...,Boolean.FALSE)` via `world.setBlock(p,...,3)`. **Não verifica se o FluidState está preenchido antes deste segundo ramo**; flags WATERLOGGED e tipo de bloco são seus gates diretos. |
| Mutação, callbacks e sucesso | Nos dois ramos que passam, o código chama `ShapersFocus.tryPropagateBlockSpell` **sem verificar o retorno boolean de `world.setBlock`**; assim a propagação pode ocorrer após uma tentativa não confirmada de mutação. Não existe `BlockUtil.destroyRespectsClaim`, `BlockEvent.BreakEvent`, `world.isInWorldBounds` nem `BlockEvent.EntityPlaceEvent` explícito nesta classe. Isso é **risco condicionado à integração e config do pack**, não prova de bypass ou exploit. |
| Parâmetros e custos | `getDefaultManaCost()=50`, `getCompatibleAugments()` admite somente `AugmentAOE` e `AugmentPierce`; não há `Sensitive`, `Extend Time`, tipo de dano ou cooldown por efeito na implementação. O AOE usa largura `1+floor(AOE)`, altura `1+ceil(AOE)` e profundidade `1+Pierce` pelo helper. A conta de 7 chamadas por candidato é **multiplicador de trabalho**, não custo adicional de mana comprovado. |
| Integração/authority | Ars Nouveau retém resolver, mana, escolha dos líquidos, alterações de BlockState e propagação ShapersFocus. Black Arcana não pode utilizar o método nativo do Ars como atalho para seu `WorldEffectPolicy`, que rege somente alterações próprias. RPG Skill Tree pode conceder gates/Mastery/perks por bridge real, não dobrar propagação, contagem de evaporações, chance de dropar itens ou execução por cada posição. |

**Gates fail-closed:** claims e callbacks de addons, blocos modded com WATERLOGGED, retornos falsos de setBlock, sobreposição de AOE, tentativas repetidas de ShapersFocus, limites de altura/chunk e performance. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Não promover Stage 06.05 ou Stage 09.
