# Grave Prayer

Status: `COUNTED_RELEASE_BOUNDED`

## Identity

Grave Prayer / Ankh prayer near a Decorative Grave.

## Exact 9.5.6 evidence

Exact `PrayerHelper.onGrave(...)` action, `PRAY_ON_GRAVE` identity, packaged Ankh recipe/advancement and publisher-documented Ankh prayer loop.

## Semantic accounting

**+1 `COUNTED_RELEASE_BOUNDED`**. The physical Ankh/item wrapper is not an extra action.

## Authority / boundary

Tombstone owns prayer execution, Knowledge of Death interaction and prayer cooldown/state. Black Arcana may observe causal completion but must not duplicate the prayer or rewards.

Exact config signatures expose `prayerCooldown`; the exact audit did not observe a prayer enable/disable field. Runtime mechanics and multiplayer persistence remain separate QA.
