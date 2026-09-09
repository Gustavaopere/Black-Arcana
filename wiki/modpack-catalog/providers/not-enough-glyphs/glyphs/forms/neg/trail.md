# Trail

- Registry: `not_enough_glyphs:trail`
- Class: `MethodTrail`
- Status: enabled; NEG-native
- Tier: **II**; default mana: **50**
- Semantics: launches NEG `TrailingProjectile`, which repeatedly resolves the remainder of the Ars spell along its path. Audited projectile code caps total procs at 20.
- Acquisition: Dragon's Breath + 2 Echo Shards + Air Essence.
- Boundary: provider projectile/resolver authority; no second BA tick/projectile loop.