# Auto Turret

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:auto_turret`
- **School:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 40`
- `baseManaCost = 80`
- `manaCostPerLevel = 20`
- `castTime = 40 ticks / 2 s`
- placement targeting range: **8 blocks**

Damage per turret shot:

`4 * spellPower / 100 * AUTO_TURRET damage multiplier`

Initial projectile/ammo count:

`8 + round(8 * spellPower / 100)`

Turret maximum health:

`20 + (spellLevel - 1) * 10`

Owner restock mana cost:

`spell mana cost / 4`

## Server-authoritative placement

The spell captures a client placement preview but admission is re-resolved on the server. It rejects invalid placement and positions already occupied by another Auto Turret in the placement box. The admitted block position is persisted in cast data and restored/revalidated at execution.

## Autonomous entity lifecycle

The provider spawns an owner-bound `AutoTurretEntity` with its anchor, damage, initial ammo, restock cost and health frozen from the cast.

Exact autonomous combat timing includes:

- target search cadence: every **10 ticks** when a new target is needed;
- charge time before a shot: **15 ticks**;
- post-shot cooldown: **8 ticks**;
- first auto-lock shot delay: **10 ticks**;
- lock retention before target reconsideration: **60 ticks**;
- lost-line-of-sight tolerance: **20 ticks**;
- empty-ammo discard delay: **100 ticks**.

The turret searches within its FOLLOW_RANGE (base 24), validates combat targets and line of sight, applies provider-owned hit damage, and spends one internal bullet after firing.

## Restocking and mana authority

Only the owner can restock by interacting with the turret. If ammo is below the initial capacity, the provider directly reads the owner's canonical Iron's `MagicData` mana, requires enough for `restockManaCost`, subtracts that amount once, synchronizes mana, and restores ammo to the initial count.

The turret therefore has **ammunition state but not a second magical mana pool**. Restock cost is paid from Iron's mana.

## Authority / deduplication

The original summon is one cast. Autonomous turret shots are provider-owned downstream activity; they must not become repeated Black Arcana casts or per-shot Mastery farming.

Black Arcana must not duplicate the turret target loop, ammo ledger, restock payment or shot damage. RPG integration requires a deliberately bounded causal contract rather than observing every autonomous hit.

## Confidence

`SOURCE-PINNED PLACEMENT + STATS + AUTONOMOUS TIMING + OWNER RESTOCK / FULL MODPACK TARGETING AND PERSISTENCE QA PENDING`