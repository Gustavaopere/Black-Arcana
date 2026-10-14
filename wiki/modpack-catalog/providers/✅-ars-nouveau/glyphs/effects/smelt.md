# Ars Nouveau — Smelt

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_smelt`
- Display name: Smelt
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 100
- Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive

## Provider-native behavior

Smelt processes blocks through normal smelting recipes and world items through recipe lookup. Source caps item processing at `round(4 * (1 + AOE multiplier + Pierce count))`. Sensitive limits the effect to item entities. Dampen switches item processing to Smoking recipes; Amplify switches item processing to Blasting recipes and also raises harvest capability for block targets. Claim/harvest checks precede block conversion.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:blast_furnace` ×4 + `#c:rods/blaze`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this remote magical processing path. Black Arcana must not double-convert blocks/items or duplicate output generation when Ars is causal. A separate Black Arcana transmutation effect would require a materially different forbidden-magic contract, not a cosmetic furnace replacement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSmelt`).

## Dossiê de engenharia para perks — classe de efeito

- **Source pin:** [`EffectSmelt.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSmelt.java), Ars Nouveau 5.13.1.
- **Geometria e volume:** `maxItemSmelt=(int)Math.round(4*(1+aoeMultiplier+count(Pierce)))`; percorre `ItemEntity` em AABB `inflate(aoeMultiplier+1)`, limitando por *unidades processadas*, não por entidades. Sensitive em bloco força caminho de itens; sem Sensitive percorre `SpellUtil.calcAOEBlocks` e `smeltBlock`.
- **Receitas:** blocos usam `RecipeType.SMELTING` e `canBlockBeHarvested` + `destroyRespectsClaim`; resultado BlockItem muda estado, resultado não-bloco remove e solta item. Em itens: Dampen prioriza `SMOKING`; senão Amplify `BLASTING`; senão `SMELTING`. A cada unidade processada reduz stack original em 1 e emite `ItemEntity` do resultado.
- **Perks:** aumentar AOE/Pierce altera tanto cap de itens quanto geometria; receitas/outputs e claim checks pertencem ao provider. Não usar esse caminho para duplicação de item, nem confundir item-per-second com magic damage.
- **Status:** ✅ source exato lido; ⚠️ entidade auxiliar, caps runtime e Survival requerem testes; API por efeito não foi validada contra RPG/Black Arcana. Sem autorização para segunda liquidação de dano/recurso/target.
