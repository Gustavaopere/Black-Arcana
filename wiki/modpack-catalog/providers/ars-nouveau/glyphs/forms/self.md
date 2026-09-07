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

## Authority / Black Arcana consequence

Ars Nouveau owns Self-form resolution and its mana/config semantics. Black Arcana self-targeted spells remain distinct Black Arcana cast definitions and still pass through canonical server authority, transactional costs, cooldowns and Arcane Danger where applicable; Ars Self must not become a shortcut around those contracts.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS AUDITED / PACK RUNTIME QA PENDING`