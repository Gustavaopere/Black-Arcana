# Plow

- Registry: `not_enough_glyphs:plow`
- Class: `EffectPlow`
- Status: enabled; NEG-native
- Default mana: **5**; tier otherwise inherited from the Ars effect contract in the audited class
- Semantics: hoe/tilling-style block interaction with AOE. The class explicitly checks Ars `BlockUtil.destroyRespectsClaim` before applying the use-on action.
- Acquisition: Earth Essence + Stone Hoe at the Scribe's Table.
- Boundary: provider world-action authority; Black Arcana must not replay the mutation or debit Ars mana again.