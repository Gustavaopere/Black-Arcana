# Touch

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_touch`
- Source class: `MethodTouch`

## Source-pinned behavior

Touch resolves the following spell effects directly against the targeted block or entity. A bare cast without a block/entity target reports failure in the exact source. Its default mana cost is **5**; the effective cost is provider-configurable.

The form also emits its provider-owned resolution particles/sound and requests a temporary fading-light presentation around the resolved target.

When invoked from a Rune caster context against an entity, the form returns Ars Nouveau's `SUCCESS_NO_EXPEND` result rather than a normal success result; that provider-specific settlement behavior must remain Ars-owned.

## Compatible augments

The exact source permits only:

- `ars_nouveau:glyph_sensitive` — extends targeting to air and fluids according to Ars Nouveau's own targeting semantics.

`MethodTouch` explicitly marks itself as a default starter glyph.

## Authority / Black Arcana consequence

Ars Nouveau owns direct Touch resolution, Rune interaction semantics, particles/lights and provider mana/config values. Black Arcana must not reinterpret a Touch cast as authority to bypass its own server targeting or `WorldEffectPolicy`; Black Arcana spells keep their canonical target validation even if an Ars bridge uses this provider method.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS AUDITED / PACK RUNTIME QA PENDING`