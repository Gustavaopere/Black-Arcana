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

## Authority / Black Arcana consequence

Ars Nouveau owns this under-caster target-selection behavior. Black Arcana must not reuse its nearby-entity selection as an implicit targeting contract: Black Arcana target geometry remains server-validated and bounded. The provider capability also occupies the generic "resolve magic directly beneath the caster" niche for deduplication analysis.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS AUDITED / PACK RUNTIME QA PENDING`