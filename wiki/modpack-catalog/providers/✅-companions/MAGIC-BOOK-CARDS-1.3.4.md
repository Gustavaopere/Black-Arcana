# Companions! 1.3.4 — canonical Magic Book action cards

Status: `✅ CATALOGED / 9 OF 9 MAGIC BOOK ACTIONS MATERIALIZED / COUNTED_SOURCE_PINNED / +9 STRICT / RUNTIME QA SEPARATE`

This index materializes the complete source-pinned Magic Book semantic inventory for the current Companions! 1.3.4 catalog.

## Complete action set — 9/9

- [Ice Shard Magic Book](magic-books/ice-shard.md) — `companions:book_ice_shard`
- [Ice Tornado Magic Book](magic-books/ice-tornado.md) — `companions:book_ice_tornado`
- [Fire Mark Magic Book](magic-books/fire-mark.md) — `companions:book_fire_mark`
- [Heal Ring Magic Book](magic-books/heal-ring.md) — `companions:book_heal_ring`
- [Stone Spikes Magic Book](magic-books/stone-spikes.md) — `companions:book_stone_spikes`
- [Brace Magic Book](magic-books/brace.md) — `companions:book_brace`
- [Magic Ray Magic Book](magic-books/magic-ray.md) — `companions:book_magic_ray`
- [Black Hole Magic Book](magic-books/black-hole.md) — `companions:book_black_hole`
- [Naginata Magic Book](magic-books/naginata.md) — `companions:book_naginata`

## Closure checklist

- physical provider identity is pinned by the sibling modlist to `companions-neoforge-1.21.1-1.3.4.jar`, mod id `companions`, runtime `1.3.4`, SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1`;
- semantic source authority is `Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`;
- `CompanionsItems` registers exactly nine `AbstractMagicBook` subclasses directly;
- no provider config/mod-presence branch conditionally creates or removes those nine identities;
- source-level survival acquisition is closed for all nine;
- Soul Mage reuse is deduplicated against the same nine identities;
- projectiles, effects, coins, armor, companions, summons and AI goals are not double-counted;
- deployed config values and assembled-pack runtime behavior remain QA, not catalog-denominator blockers.

## Acquisition closure

| Route | Covered actions |
|---|---|
| Overworld Minion + Copper Coin | Ice Shard, Ice Tornado |
| Nether Minion + Nether Coin | Fire Mark, Brace |
| End Minion + End Coin | Heal Ring, Stone Spikes |
| vanilla chest-table injection | Black Hole, Magic Ray |
| provider recipe | Naginata |

## Deduplication

The Soul Mage accepts the same Magic Book items and has dedicated goals for all nine identities. That is reuse of the provider-owned action, not a second spell/action family.

Naginata's crouch-dependent firing pattern is a mode/variant of `companions:book_naginata`, not a tenth semantic identity.

## Explicit non-counts

The following remain `+0` under this provider checkpoint:

- Magic Book item containers as a second identity beyond their one-to-one magical action;
- Soul Mage AI goals as duplicate actions;
- provider projectiles/effects created by a book;
- Mage/Holy Robe/Crystallized Blood equipment;
- coins and ordinary acquisition items;
- summoned companions and ordinary companion attacks;
- hostile-mob skills not independently established as qualifying player-facing magic actions.

## Authority boundary

Companions! owns Magic Book use, provider projectiles/effects, cooldown configuration, acquisition and Soul Mage consumption. Black Arcana does not duplicate those settlements. RPG Skill Tree remains progression/Mastery/perk authority only through verified boundaries.

Sources: [SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md](SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md) and [README.md](README.md).
