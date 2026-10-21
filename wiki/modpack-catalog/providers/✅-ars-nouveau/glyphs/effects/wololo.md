# Wololo

Status: `SOURCE-PINNED 5.13.1 / MANIPULATION EFFECT / SEMANTICS+ACQUISITION AUDITED`

- Registry id: `ars_nouveau:wololo`
- Display name: `Wololo`
- Default mana cost: `30`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Wololo` recolors compatible entities, equipment and blocks using dye/color data selected from the caster, spell color or Randomize.

The pinned source can:

- recolor sheep and compatible mobs;
- recolor dyeable armor when Sensitive or when targeting an armor stand;
- recolor item entities with compatible color components;
- recolor signs;
- recolor blocks through matching crafting recipes while preserving compatible block-entity data;
- call `IWololoable` on provider-compatible block entities;
- use a bounded crafting-recipe cache (`MAX_RECIPE_CACHE = 16`).

Compatible augments are `Randomize` and `Sensitive`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `#c:dyes` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Black Arcana boundary

Wololo owns its recoloring/transformation settlement. Black Arcana must not replay the same block/item/entity transformation and must not infer generic transformation authority from a cosmetic result.

If future Black Arcana transmutation overlaps, uniqueness must be mechanical rather than presentation-only.

## QA / runtime

Source is pinned to 5.13.1. Full-pack recipe/mod-interaction QA remains pending.

## Engenharia de perks — evidência de execução individual

- **Classe versionada:** [`EffectWololo.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java) no Ars Nouveau 5.13.1.
- **Registry:** a classe declara `super("wololo","Wololo")`; ficha usa `ars_nouveau:wololo` e não `ars_nouveau:glyph_wololo`.
- **Escolha de cor:** `getDye` lê dye de inventário de `TileCaster`, offhand de outros casters, ou fallback Randomize/partícula da spell. **Entidades:** colore `Sheep`, componentes `BASE_COLOR/DYED_COLOR` de itens/equipamentos, ou usa `MobAccessor.callMobInteract` por fake player.
- **Mundo:** em blocos implementando `IWololoable` chama `setColor`; em sinais tenta `DyeItem.tryApplyToSign`; senão resolve receita de crafting de dye e bloco, converte blockstate mantendo propriedades e restaura block entity data quando mesma classe. Cache de receitas `FixedStack` com máximo `16`.
- **Perks:** alteração cromática não significa dano/status. Sensitivity e randomization afetam alvo/paleta por código; efeitos de bloco são provider-owned e não podem ser duplicados por observer.
- **Status:** ✅ code pin/identidade; ⚠️ downstream, config e Survival pendentes; mutação por RPG perk só pode ocorrer via [eventos reais](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e adapter validado, não por inferência temática.
