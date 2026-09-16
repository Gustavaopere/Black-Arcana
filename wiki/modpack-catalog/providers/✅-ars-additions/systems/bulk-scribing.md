# Bulk Scribing

Status: `SOURCE-PINNED 21.3.0 / RECIPE+SOURCE COST AUDITED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Custom recipe type: `ars_additions:bulk_scribing`.

The exact generated datapack contains one generic recipe instance: `ars_additions:bulk_scriber`. The behavior is implemented by `BulkScribingRecipe`, so it operates across compatible provider items rather than one hard-coded output.

## Matching contract

The Imbuement Chamber reagent is the destination item to be scribed. Exactly **one pedestal item** must be present and it must act as the spell source/scriber.

Accepted scriber item classes are:

- Ars Spell Book;
- Ars Spell Parchment;
- Ars Manipulation Essence.

The pedestal scriber must expose a valid non-empty spell through the provider caster contract.

The destination reagent must either:

- implement Ars `IScribeable`; or
- implement `ItemCasterProvider` and currently contain a spell different from the source spell.

Blank Parchment is converted into normal Spell Parchment before scribing.

## Source cost

Normal Source cost is exactly the spell cost stored on the pedestal scriber. The method contains a 1000-Source fallback when no valid provider caster can be found, but normal recipe matching rejects that invalid state before crafting.

## Settlement

Assembly copies the destination stack and invokes its provider `IScribeable.onScribe` contract using Ars `ANFakePlayer` with the pedestal scriber in main hand. The recipe therefore delegates actual spell/configuration transfer to the target item's own provider implementation rather than manually copying arbitrary NBT.

## Black Arcana boundary

Bulk Scribing is provider configuration transfer. Black Arcana must not copy spell NBT independently, infer a new cast from the scribing operation, charge a second resource transaction or translate the transferred Ars spell into Black Arcana persistence without an explicit supported contract.
