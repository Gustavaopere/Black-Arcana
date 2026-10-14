# Break

- Registry ID: `ars_nouveau:glyph_break`
- Source class: `EffectBreak`
- School: Elemental Earth
- Default tier: **1**
- Default mana: **10**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Break destroys harvestable blocks in provider-calculated AOE/depth geometry. It checks Ars Nouveau's claim-respect helper and a provider break blacklist before mutation. Amplify/Dampen change harvest capability; Fortune and Extract synthesize Fortune/Silk Touch levels for the provider break operation; Sensitive switches the simulated tool to shears; Randomize may skip candidate blocks.

Compatible augments: Amplify, Dampen, Pierce, AOE, Extract, Fortune, Sensitive, Randomize. Default Fortune limit is 4 and Sensitive limit is 1. It is explicitly a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:iron_pickaxe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, Break is considered known without consuming a Glyph item.
- The generated recipe still exists; provider Glyph learning rejects the item while Break is currently configured as a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns its break/loot/claim semantics. Any Black Arcana block destruction still requires `WorldEffectPolicy`, loaded-chunk/budget controls and Black Arcana causal ownership; Ars Break is not a world-policy bypass.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectBreak.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectBreak` no Ars 5.13.1, método `onResolveBlock`.
- **Alvos/blocos:** `SpellUtil.calcAOEBlocks` recebe multiplicador AOE e contagem Pierce. Ajusta amplificação por Mining Fatigue, seleciona ferramenta simulada (shears com Sensitive; diamond pickaxe conforme tag/stack). **Loot:** Fortune até 4 e Extract/Silk Touch são aplicados à ferramenta simulada; Sensitive até 1. **Admissão:** bounds, `canBlockBeHarvested`, `BREAK_BLACKLIST`, `BlockUtil.destroyRespectsClaim` e `breakExtraBlock`. Randomize *pula* posição com probabilidade de teste `random.nextFloat()<count*0.25F`. Cada quebra aceita pode propagar `ShapersFocus.tryPropagateBlockSpell`. **Perks:** preservar claims, limites de work e causalidade de cada bloco, sem duplicar loot.
- **Limite de integração:** ✅ fonte estática identificada; ⚠️ parâmetros condicionados à configuração carregada; ⛔ nenhum hook externo de mutação verificado. Mana, targeting e settlement pertencem a Ars; RPG Skill Tree não substitui o resolver. Gameplay/Survival e adapter real: PENDING.
