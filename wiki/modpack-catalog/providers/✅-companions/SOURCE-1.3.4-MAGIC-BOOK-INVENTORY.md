# Companions! 1.3.4 — source-pinned Magic Book inventory

## Evidence boundary

Installed/current provider identity from the sibling physical dossier:

- `companions-neoforge-1.21.1-1.3.4.jar`;
- mod id `companions`;
- runtime `1.3.4`;
- physical SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1`;
- physical order `#104` in the current 587-entry top-level modlist.

Exact public source checkpoint:

`Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f`

The commit changes the project version from 1.3.3 to 1.3.4. Source-build byte equality to the physical JAR is not claimed.

## Active Magic Book inventory

The exact `CompanionsItems` registry contains nine active Magic Book items. Each is an `AbstractMagicBook` subclass and represents one discrete provider-owned magical action.

| # | Registry ID | Display identity | Concrete class | Source-pinned action surface | Default cooldown | Survival acquisition |
|---:|---|---|---|---|---:|---|
| 1 | `companions:book_ice_shard` | Ice Shard Magic Book | `IceShardBook` | launches the provider ice-shard projectile from the caster; projectile receives the caster's recent combat target hint when available | 180 ticks | Overworld Minion + Copper Coin random reward |
| 2 | `companions:book_ice_tornado` | Ice Tornado Magic Book | `IceTornadoBook` | summons the provider tornado projectile immediately ahead of the caster | 200 ticks | Overworld Minion + Copper Coin random reward |
| 3 | `companions:book_fire_mark` | Fire Mark Magic Book | `FireMarkBook` | places a provider Fire Mark ring at a looked-at block within the source-defined trace range, with caster-position fallback | 140 ticks | Nether Minion + Nether Coin random reward |
| 4 | `companions:book_heal_ring` | Heal Ring Magic Book | `HealRingBook` | creates the provider healing-ring projectile/effect at the caster | 200 ticks | End Minion + End Coin random reward |
| 5 | `companions:book_stone_spikes` | Stone Spikes Magic Book | `StoneSpikesBook` | creates a forward ground-spike pattern with a central row and two angled side rows | 140 ticks | End Minion + End Coin random reward |
| 6 | `companions:book_brace` | Brace Magic Book | `BraceBook` | launches the provider Brace projectile along the caster's look direction | 160 ticks | Nether Minion + Nether Coin random reward |
| 7 | `companions:book_magic_ray` | Magic Ray Magic Book | `MagicRayBook` | builds a provider magic ray from successive ray pieces along the look direction until the configured/source-bounded path is exhausted or blocked | 200 ticks | injected into vanilla chest-table loot |
| 8 | `companions:book_black_hole` | Black Hole Magic Book | `BlackHoleBook` | launches the provider black-hole projectile forward from the caster | 160 ticks | injected into vanilla chest-table loot |
| 9 | `companions:book_naginata` | Naginata Magic Book | `NaginataBook` | targets along the player's look trace and calls down provider naginata projectiles; crouch input changes the provider firing pattern without minting a second action identity | 140 ticks | dedicated provider recipe |

Default cooldowns are source defaults, not deployed-pack measurements. The Mage armor set can modify Magic Book cooldowns through provider logic/config and is not a separate spell identity.

## Registration closure

The nine registrations are direct `ITEMS.register(...)` entries in the exact 1.3.4 `CompanionsItems` source. No conditional registration branch, mod-presence gate or provider config switch wraps those nine entries.

The exact `Magic Books` config section exposes behavior/numerical values rather than identity enable toggles. Source defaults include:

| Config surface | Source default |
|---|---:|
| Magic Ray fragment damage | 5.5 |
| Ice Tornado damage | 3.0 |
| Stone Spike damage | 4.0 |
| Fire Mark effect radius | 2.5 blocks |
| Heal Ring healing | 6.0 |
| Black Hole attraction radius | 12.0 blocks |
| Black Hole attraction speed | 1.45 |
| Small Ice Shard damage | 2.5 |
| Small Ice Shard freeze duration | 100 ticks |
| spell world-grief permission | true |

These defaults are catalog metadata only. Effective deployed config, protection hooks and final damage/heal settlement remain runtime QA.

## Survival reachability

### Overworld Minion

A tamed Minion in its Overworld variant accepts a Copper Coin. On provider success it returns one of:

- `book_ice_shard`;
- `book_ice_tornado`.

The exact source success threshold is 0.25 before the two-book random choice.

### Nether Minion

A tamed Minion in its Nether variant accepts a Nether Coin. On provider success it returns one of:

- `book_fire_mark`;
- `book_brace`.

The exact source success threshold is 0.45 before the two-book random choice.

### End Minion

A tamed Minion in its End variant accepts an End Coin. On provider success it returns one of:

- `book_heal_ring`;
- `book_stone_spikes`.

The exact source success threshold is 0.55 before the two-book random choice.

### Vanilla chest injection

The exact provider server-event handler modifies Minecraft chest loot tables and adds candidate entries for:

- `book_black_hole`;
- `book_magic_ray`.

Each book entry carries a provider random-chance condition of 0.045. The final effective chest distribution is still subject to Minecraft loot-pool selection and assembled datapack/runtime behavior; no simplified end probability is inferred here.

### Naginata recipe

The exact 1.3.4 data resources include `data/companions/recipe/book_naginata.json` producing `companions:book_naginata`.

This closes a provider-owned catalog-level survival path for all nine Magic Books.

## Soul Mage deduplication

The Soul Mage owns a three-slot inventory whose slots accept only `AbstractMagicBook` items. Its exact source registers dedicated goals for all nine Magic Book identities.

That is **reuse**, not nine additional semantic actions:

`player Magic Book identity = Soul Mage Magic Book identity`

The semantic ledger therefore counts each book once under Companions! ownership.

## Explicit non-counts

The following are not added to the semantic-magic numerator by this checkpoint:

- Magic Book item containers as a second identity beyond their one-to-one action;
- Soul Mage AI goals as duplicate spells;
- projectiles spawned by a Magic Book;
- Mage/Holy Robe/Crystallized Blood equipment;
- coins;
- status effects;
- ordinary companion attacks;
- summoned companion entities;
- other weapons/items/blocks;
- hostile-mob skills not independently established as player-facing actions.

A later provider-wide action audit may classify additional qualifying supernatural player actions, but they are not inferred from thematic similarity.

## Evidence state

- current physical identity: strong, SHA-pinned sibling evidence;
- exact semantic registry: strong, version-correlated official source pin;
- source-to-physical byte equivalence: not proven;
- nine action identities: closed;
- nine survival routes: closed at source/catalog level;
- provider enable/disable registration gates: none found around the nine registrations;
- assembled-pack runtime/config behavior: fail-closed.

Disposition: **`COUNTED_SOURCE_PINNED / +9`**.
