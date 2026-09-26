# Dissonance

Status: `COUNTED_RELEASE_BOUNDED`

## Identity

Enhanced prayer identity: Dissonance.

## Exact 9.5.6 evidence

Exact provider bonus key `bonus.tombstone.pray_of_dissonance` and `PrayerHelper.dissonance(...)`.

## Semantic accounting

**+1 `COUNTED_RELEASE_BOUNDED`**.

## Authority / boundary

Tombstone owns prayer selection/effect settlement. Do not create a parallel Black Arcana prayer with the same provider identity.

Exact config signatures expose `prayerCooldown`; the exact audit did not observe a prayer enable/disable field. Runtime mechanics and multiplayer persistence remain separate QA.
