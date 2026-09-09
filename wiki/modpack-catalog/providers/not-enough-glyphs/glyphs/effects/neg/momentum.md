# Momentum

- Registry: `not_enough_glyphs:momentum`
- Class: `EffectMomentum`
- Registration: NEG still passes it through `APIRegistry.registerSpell`
- Current source status: **disabled** because the class returns `isEnabled() = false`
- Acquisition: no generated glyph recipe in the exact 4.6.1 source tree.
- Semantics: movement-speed/momentum manipulation exists in source but is not active default content.
- Dedup: do not count it as an active current-pack capability unless provider config/source state changes.