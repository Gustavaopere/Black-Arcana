# Provider Audit Queue — Companions! 1.3.4 delta

Date: `2026-09-23`

This is a narrow status overlay over the historical `PROVIDER-AUDIT-QUEUE.md`. It prevails for `companions` until the current physical magic-provider queue is regenerated from the sibling's newest physical modlist.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `companions` | `companions-neoforge-1.21.1-1.3.4.jar` / runtime `1.3.4` / physical SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1` | `✅ MAGIC-BOOK SEMANTIC CATALOG COMPLETE / 9 SOURCE-PINNED PLAYER MAGIC ACTIONS / ALL 9 SOURCE-LEVEL SURVIVAL ROUTES CLOSED / REGISTRATIONS UNCONDITIONAL / SOUL-MAGE REUSE DEDUPED / ASSEMBLED-PACK RUNTIME QA FAIL-CLOSED` |

## Evidence

Physical authority:

- sibling `neoforge-rpg-skilltree@39d358ec8de20d647cecbfe4e8c0a0181cc6b12f`;
- certified physical dossier `✅-companions v1.3.4.md`;
- physical order `#104`;
- current JAR `companions-neoforge-1.21.1-1.3.4.jar`;
- mod id `companions`;
- runtime `1.3.4`;
- physical SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1`.

Source pin:

`Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`

The provider-owned commit bumps project version from 1.3.3 to 1.3.4. Source-to-physical byte equality is not claimed.

## Semantic closure

The exact source-pinned item registry contains nine active `AbstractMagicBook` registrations:

1. `book_ice_shard`;
2. `book_ice_tornado`;
3. `book_fire_mark`;
4. `book_heal_ring`;
5. `book_stone_spikes`;
6. `book_brace`;
7. `book_magic_ray`;
8. `book_black_hole`;
9. `book_naginata`.

No config/mod-presence branch wraps those registrations. The `Magic Books` config section changes numerical/behavioral settlement and cooldowns, not whether these nine identities exist.

Catalog-level survival acquisition is closed:

- Ice Shard / Ice Tornado — Overworld Minion + Copper Coin;
- Fire Mark / Brace — Nether Minion + Nether Coin;
- Heal Ring / Stone Spikes — End Minion + End Coin;
- Black Hole / Magic Ray — provider injection into vanilla chest loot tables;
- Naginata — provider recipe.

Soul Mage accepts these books in three dedicated inventory slots and has one AI goal per book identity. Those AI casts are deduplicated against the same provider-owned book action rather than counted again.

## Semantic delta

Companions! contributes **+9 `COUNTED_SOURCE_PINNED`** objects.

Strict semantic minimum:

`1382 + 9 = 1391`.

The technical provider-component denominator remains `PENDING REBASE`; this delta does not revive the stale historical 100-component denominator.

## Remaining runtime QA

Still fail-closed:

- exact assembled-pack boot and registry parity;
- deployed config values;
- live recipe/loot/trade behavior;
- player and Soul Mage casts;
- damage/heal/projectile attribution;
- block grief/protection behavior;
- multiplayer owner/team settlement;
- persistence/reload/chunk/dimension behavior.

These runtime gates are not semantic inventory gates.

Canonical provider files:

- [Companions! provider summary](../providers/%E2%9C%85-companions/README.md)
- [1.3.4 Magic Book inventory](../providers/%E2%9C%85-companions/SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md)
