# Empathy

Status: `COUNTED_RELEASE_BOUNDED`

## Identity

Enhanced prayer identity: Empathy.

## Exact 9.5.6 evidence

Exact provider bonus key `bonus.tombstone.pray_of_empathy` and `PrayerHelper.empathy(...)`.

## Semantic accounting

**+1 `COUNTED_RELEASE_BOUNDED`**.

## Authority / boundary

Tombstone owns prayer selection/effect settlement.

Exact config signatures expose `prayerCooldown`; the exact audit did not observe a prayer enable/disable field. Runtime mechanics and multiplayer persistence remain separate QA.
