# Self

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_self`
- Source class: `MethodSelf`

## Source-pinned behavior

Self resolves the following spell effects against the caster. The exact source consistently redirects block/entity invocation surfaces back to the invoking caster rather than the externally selected target.

Its default mana cost is **10**; the effective cost remains Ars Nouveau configuration state.

## Compatible augments

The exact source exposes **no compatible augments** for this Form.

`MethodSelf` explicitly marks itself as a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `#minecraft:wooden_pressure_plates` + `minecraft:iron_chestplate`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, Self is considered known without consuming a Glyph item.
- The generated recipe still exists; provider Glyph learning rejects the item while Self is currently configured as a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns Self-form resolution and its mana/config semantics. Black Arcana self-targeted spells remain distinct Black Arcana cast definitions and still pass through canonical server authority, transactional costs, cooldowns and Arcane Danger where applicable; Ars Self must not become a shortcut around those contracts.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

## Mapeamento para perks — targeting real

- **Source pin:** [`MethodSelf.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodSelf.java), Ars Nouveau 5.13.1.
- **Resolver:** `onCast`, `onCastOnBlock` e `onCastOnEntity` convertem o destino em `EntityHitResult(caster/playerIn)`, enviando `resolver.onResolveEffect` ao próprio caster — mesmo que o jogador tenha clicado outro bloco/entidade. **Mana:** default 10; starter por `defaultedStarterGlyph=true`. **Augments:** `getCompatibleAugments() = augmentSetOf()` (nenhum). **Efeitos:** emitter e sound são visuais e não confirmam resultado de cada effect da cadeia. **Perks:** mudar target self para aliado/inimigo seria alteração de contrato da Form, sem hook comprovado.
- **Status:** ✅ método/fonte identificado; ⛔ mutação de targeting por perk RPG não verificada. Ars controla SpellResolver, custos e cadeia de efeitos; Black Arcana só controla suas casts. Runtime/Survival: PENDING.
