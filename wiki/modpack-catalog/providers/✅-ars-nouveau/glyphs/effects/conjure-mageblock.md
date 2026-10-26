# Conjure Mageblock

- Registry ID: `ars_nouveau:glyph_phantom_block`
- Source class: `EffectPhantomBlock`
- School: Conjuration
- Default tier: **1**
- Default mana: **5**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates Ars Nouveau Mage Blocks in provider-calculated AOE/depth positions after world-bounds, replacement, collision and claim checks. Without Amplify they are temporary and use the duration modifier; one Amplify makes the created Mage Block permanent. Casting on an entity redirects the placement geometry around/below that entity.

Compatible augments: AOE, Pierce, Amplify, Extend Time, Reduce Time. Amplify is limited to 1 by default.

Identity note: installed-line registry path remains `glyph_phantom_block`; the source class itself notes a possible class rename only for 1.22.

## Acquisition / learning

- Provider-generated Glyph recipe: `#c:glass_blocks` ×8.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Permanent or temporary Ars Mage Blocks remain Ars-owned. Black Arcana cannot use this capability to bypass `WorldEffectPolicy`, restoration ownership or bounded world-mutation budgets.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectPhantomBlock.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPhantomBlock.java), Ars Nouveau 5.13.1.
- **Identidade:** registry `ars_nouveau:glyph_phantom_block`; classe `EffectPhantomBlock`; display Conjure Mageblock. `onResolveBlock` percorre `SpellUtil.calcAOEBlocks` e ajusta posição à face (exceto hit interior). Verifica bounds, `destroyRespectsClaim`, replaceable e `world.isUnobstructed(MAGE_BLOCK,collision fakePlayer)` antes de criar o bloco.
- **Persistência:** cria `MAGE_BLOCK` com `MageBlock.TEMPORARY=!hasBuff(Amplify)` e, se `MageBlockTile` presente, define cor, `lengthModifier=getDurationMultiplier`, `isPermanent=hasBuff(Amplify)`; Amplify tem limite default 1. Ramo entity constrói BlockHitResult sob o alvo e segue o mesmo método.
- **Perks:** permanência é **toggle de Amplify**, não duração infinita calculada por seconds. O countdown real pertence ao `MageBlockTile`; claims e colisions permanecem provider-owned. Não usar hook genérico de stats para conceder bloco permanente sem validação específica.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.

## Certificação técnica estática — Conjure Mageblock (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Registry `ars_nouveau:glyph_phantom_block` ↔ `EffectPhantomBlock` do publisher JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A prova binária cobre classe/ID, **não equivalência do corpo de método**. Fontes `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectPhantomBlock.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPhantomBlock.java), [MageBlockTile.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/MageBlockTile.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java).

| Eixo de perk | Comportamento observado e boundary |
|---|---|
| Targeting e AOE | `onResolveBlock` percorre `SpellUtil.calcAOEBlocks(...,spellStats)` e muda `pos` para `pos.relative(rayTraceResult.getDirection())` **somente quando `!rayTraceResult.isInside()`**. Valida `world.isInWorldBounds(pos)`, `BlockUtil.destroyRespectsClaim` nesse destino, `BlockState.canBeReplaced()` e `world.isUnobstructed(MAGE_BLOCK,...,CollisionContext.of(fakePlayer))`. `onResolveEntity` cria `BlockHitResult(entity.position,Direction.DOWN,entity.blockPosition().below(),true)` e reusa exatamente o caminho de bloco; não autoriza raio de alvo ou projectile customizado. |
| Permanent versus temporary | Em `world.setBlockAndUpdate` seleciona `MageBlock.TEMPORARY=!spellStats.hasBuff(AugmentAmplify.INSTANCE)`. Se a colocação gerar `MageBlockTile`, atribui `tile.lengthModifier=spellStats.getDurationMultiplier()`, `tile.isPermanent=spellStats.hasBuff(AugmentAmplify.INSTANCE)`, cor de `MAGEBLOCK_TIMELINE`, `tile.updateBlock()` e então `ShapersFocus.tryPropagateBlockSpell`. O **retorno boolean de setBlockAndUpdate não é verificado**; a existência de MageBlockTile atua como gate para configuração/propagação, não prova de uma transação persistida. |
| Timer efetivo e NBT | `MageBlockTile.tick()` retorna cedo se `isPermanent`; caso contrário, no servidor, incrementa `age` e remove o bloco se `age > (20*15+20*5*lengthModifier)`. Padrão com multiplier0: limiar **300 ticks** (comparação estritamente `>`), com +100 ticks por unidade de `lengthModifier`. `age`, `lightColor`, `permanent` e `modifier` são serializados em NBT; não assumir expiry por wall-clock durante chunk descarregado. `MageBlockTile.onDispel` destrói o bloco sem drops independentemente do modo permanente, mas hook externo mutador não comprovado. |
| Parâmetros e ownership | `getDefaultManaCost()=5`, Tier I, school CONJURATION; augments `AOE`, `Pierce`, `Amplify`, `Extend Time` e `AugmentDurationDown` (limite default Amplify1). O comentário `todo: 1.22 rename` **não** altera class/registry do 5.13.1. Ars mantém entidade de bloco, armazenamento NBT e countdown; `WorldEffectPolicy` de Black Arcana governa somente suas world mutations; RPG Skill Tree não duplica bloco permanente ou cronômetro por perk sem adapter validado. |

**QA pendente:** efetividade de placement e claims, conflitos após mudança de mundo, dispel de variantes, persistência de `MageBlockTile`, unload/restart, AOE, multiplicador negativo/duration config, `ShapersFocus`, causalidade e consumo real de mana. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Stage 06.05/09 inalterado.
