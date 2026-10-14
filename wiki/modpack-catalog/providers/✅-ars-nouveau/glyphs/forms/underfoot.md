# Underfoot

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_underfoot`
- Source class: `MethodUnderfoot`

## Source-pinned behavior

Underfoot resolves the following spell effects beneath the caster. In the ordinary cast/entity invocation path, Ars Nouveau first checks whether the caster is riding an entity; otherwise it searches a narrowly inflated area beneath the caster for another entity; if neither case applies, it resolves against the block below the caster.

When invoked through the direct block-use overloads, it resolves against the block below the caster.

Its default mana cost is **5**; the effective cost remains provider-configurable.

## Compatible augments

The exact source exposes **no compatible augments** for this Form.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:iron_boots` + `#minecraft:wooden_pressure_plates`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned: using the crafted Glyph server-side records it in Ars player data and consumes the Glyph in survival. Runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns this under-caster target-selection behavior. Black Arcana must not reuse its nearby-entity selection as an implicit targeting contract: Black Arcana target geometry remains server-validated and bounded. The provider capability also occupies the generic "resolve magic directly beneath the caster" niche for deduplication analysis.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

## Mapeamento para perks — targeting real

- **Source pin:** [`MethodUnderfoot.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodUnderfoot.java), Ars Nouveau 5.13.1.
- **Alvo em cast genérico e onCastOnEntity:** primeiro `caster.getVehicle()`; senão `world.getEntities(caster, caster.getBoundingBox().inflate(0.1,1.5,0.1))` e o primeiro da lista; se nenhum, usa `BlockHitResult` no bloco abaixo. **Divergência por overload:** `onCastOnBlock` sempre aponta ao bloco sob o caster, sem busca de entidades. **Mana:** default 5; `getCompatibleAugments()=augmentSetOf()`. **Perks:** a primeira entidade encontrada não é automaticamente alvo de combate nem critério de propriedade RPG; não reimplementar target finder sem auditoria e sem hook.
- **Status:** ✅ método/fonte identificado; ⛔ mutação de targeting por perk RPG não verificada. Ars controla SpellResolver, custos e cadeia de efeitos; Black Arcana só controla suas casts. Runtime/Survival: PENDING.
