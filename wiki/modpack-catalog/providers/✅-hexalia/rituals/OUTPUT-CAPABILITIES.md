# Hexalia 1.3.6 — Nature's Ritual output capabilities

## Estado

`SOURCE-PINNED 1.3.6 / ALL 19 PLAYER-FACING RITUAL OUTPUTS CLASSIFIED / HIGH-IMPACT BEHAVIOR PATHS AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Source authority:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

This document complements [NATURES-RITUAL-CATALOG.md](NATURES-RITUAL-CATALOG.md): that file closes the **19/19 recipes**; this file classifies what those outputs actually do and which Black Arcana capability families they overlap.

The installed physical file is named `hexalia-neoforge-1.3.6.jar` but reports runtime metadata `1.3.5`. Every implementation statement here is therefore `SOURCE-PINNED 1.3.6`, not exact installed-runtime validation.

## 1. Elemental Nodes — 4 outputs

### Fire Node
- ID: `hexalia:fire_node`
- registration: plain `Item`
- Nature's Ritual reagent/output
- downstream recipe/component role

### Water Node
- ID: `hexalia:water_node`
- registration: plain `Item`
- Nature's Ritual reagent/output
- downstream recipe/component role

### Air Node
- ID: `hexalia:air_node`
- registration: plain `Item`
- Nature's Ritual reagent/output
- downstream recipe/component role

### Earth Node
- ID: `hexalia:earth_node`
- registration: plain `Item`
- Nature's Ritual reagent/output
- downstream recipe/component role

At the exact 1.3.6 pin these four nodes are registered as ordinary item components rather than standalone ticking spell entities. Their major gameplay authority is as Hexalia ritual/crafting reagents — including Astrylis, Kelpweave Blade, Rootshaper, Bloomwrap, Nautilite, Windsong and idols.

Do not turn the node names themselves into proof of a generic elemental spell engine.

## 2. Aegiflora — Creeper-explosion interception

- ritual output: `hexalia:aegiflora`
- provider event: `ExplosionEvent.PRE`
- trigger restriction: explosion direct source must be a `Creeper`
- search radius: `8` blocks, spherical distance test
- normal Aegiflora charges: `2`
- Withered Aegiflora charges: `1`

When a qualifying Creeper explosion begins and a charged Aegiflora is found within radius 8, Hexalia interrupts/cancels the explosion and consumes one charge.

Lifecycle:

1. normal Aegiflora starts at 2 charges;
2. first absorption reduces to 1 and converts normal Aegiflora to Withered Aegiflora;
3. second absorption reduces to 0 and replaces it with a Dead Bush.

This is **not** a generic anti-explosion ward. The source path is explicitly Creeper-direct-source-specific.

Dedup impact: environmental/world-protection, wards/barriers. Black Arcana must not re-cancel the same explosion or convert each intercepted explosion into repeated cast settlement.

## 3. Astrylis — timed crop/sapling growth field

- ritual output: `hexalia:astrylis`
- activation item: one `hexalia:celestial_crystal`, consumed unless creative
- default active duration: `1200 ticks = 60 s`
- default bonemeal interval: `240 ticks = 12 s`
- scan volume per application: X/Z `-4..4`, Y `-2..2` around the plant
- eligible blocks: `BonemealableBlock` + vanilla `CROPS` or `SAPLINGS` tags

While active, Astrylis periodically calls the provider/vanilla bonemeal path on valid crops and saplings. Save/reload catch-up logic can perform up to 5 missed applications in one tick when expected applications exceed recorded applications.

Dedup impact: persistent agricultural growth field. It is not a repeated spell cast and should not grant mastery per bonemeal pulse or per grown crop.

## 4. Grimshade — undead conversion + persistent hostile field

- ritual output: `hexalia:grimshade`
- activation: `hexalia:hex_focus`; the shown path does not consume the Focus
- one-shot conversion radius: AABB inflated by `2.5`
- default active duration: `2400 ticks = 120 s`
- default effect radius: `16`

### Activation conversions

On activation:

- nearby `Skeleton` entities are replaced by newly created `WitherSkeleton` entities at the same position/rotation;
- Skeleton Skull item entities are converted to Wither Skeleton Skulls, respecting a shared conversion cap;
- Skeleton Skull / Skeleton Wall Skull blocks can be converted to Wither variants, preserving compatible state properties;
- the skull item/block conversion cap is `3` total for that activation path.

### Persistent field

While active and server difficulty is not Peaceful, all alive `LivingEntity` targets in the configured AABB except Players receive every tick:

- vanilla Wither: `60 ticks`, amplifier `0`;
- vanilla Weakness: `60 ticks`, amplifier `0`.

The collision path applies the same pair to non-player living entities touching the block.

Dedup impact: necromantic conversion, area debuff/control and world/entity transformation. Black Arcana must not reinterpret every field tick as a cast or duplicate provider conversions.

## 5. Rabbage Seeds → Rabbage — throwable Bleeding projectile

Nature's Ritual produces `hexalia:rabbage_seeds`. The seeds grow `hexalia:rabbage_crop`, whose produce `hexalia:rabbage` has an active projectile use.

When a Rabbage item is used:

- launches a `RabbageProjectile` at velocity `1.5`, inaccuracy `1.0`;
- consumes one item unless creative;
- awards vanilla item-used stat.

On hit against a LivingEntity:

- thrown damage: `1`;
- applies `hexalia:bleeding` for `100 ticks = 5 s`, amplifier `0`.

Dedup impact: prepared/cultivated throwable offense + provider Bleeding. The ritual output is therefore capability-bearing even though the immediate output is only seeds.

## 6. Nautilite — aquatic aura / hostile aquatic damage

- ritual output: `hexalia:nautilite`
- placement: requires source water; block remains waterlogged
- activation: `hexalia:hex_focus`; shown path does not consume Focus
- default duration: `2400 ticks = 120 s`
- default effect radius: `16`

Every active server tick:

### Players in AABB
- if in water or rain: apply Conduit Power `40 ticks`, amplifier `0`;
- if Mining Fatigue is present: remove it. This removal is not nested inside the water/rain condition in the 1.3.6 source.

### Drowned / Guardians
If the entity is a Drowned or Guardian, is in water/rain, and is within provider radius using `closerThan`:

- receives `2.0` magic damage **every active tick**.

On expiry, Nautilite destroys its own block without drops.

Dedup impact: aquatic adaptation/ward + persistent anti-aquatic-mob damage field. The per-tick damage is provider-owned and must not become a Black Arcana repeated-cast/proc source.

## 7. Windsong — projectile-nullification field

- ritual output: `hexalia:windsong`
- activation: `hexalia:hex_focus`; shown path does not consume Focus
- default duration: `600 ticks = 30 s`
- default radius: `6`

Every active server tick, Windsong gathers all entities in its AABB whose runtime type is `Projectile` and discards them if not already removed.

There is no source-side owner/team/projectile-subtype filter in this path.

On expiry, Windsong destroys its own block without drops.

Dedup impact: projectile negation/barrier. Black Arcana must not add a second deletion/counterspell settlement for projectiles already removed by the provider.

## 8. Lourdes — cleanse + regeneration aura

- ritual output: `hexalia:lourdes`
- activation resource: one `hexalia:lotus_blossom`, consumed unless creative
- default duration: `600 ticks = 30 s`
- default radius: `8.0`
- pulse interval: `20 ticks = 1 s`
- targets: alive Players + Animals in AABB

Every pulse:

1. removes every active MobEffect whose category is `HARMFUL`;
2. if vanilla Regeneration is absent or has less than 30 ticks remaining, applies Regeneration for `40 ticks`, amplifier `0`.

Dedup impact: cleanse/healing aura. This is materially stronger than a simple heal pulse because it category-cleanses harmful MobEffects.

## 9. Morphora — area mutation engine

- ritual output: `hexalia:morphora`
- activation input: Mutavis item/stack
- implementation scan: horizontal square X/Z `-3..3`, same Y, excluding the Morphora block itself
- possible target positions per activation: up to 48 neighboring positions before recipe filtering

For each non-air neighboring block:

1. derive the block's default item;
2. query a `hexalia:mutation` recipe;
3. if matched, destroy the block with drops disabled;
4. apply the recipe's `MutationOutput`;
5. emit provider effects.

Mutavis is consumed once only if at least one mutation succeeded and the player is not creative.

### Config/source mismatch

`HexaliaCommonConfig` exposes `morphoraRadius` with default `6` and sanitization `1..32`, but `MorphoraBlock` at the exact 1.3.6 pin uses hard-coded `MUTATION_RADIUS = 3` and does not call that config in the audited activation path.

Therefore:

`EFFECTIVE MORPHORA MUTATION RADIUS = 3 IN PINNED SOURCE PATH / CONFIG ENTRY DEFAULT 6 APPEARS UNUSED HERE / RUNTIME QA REQUIRED`.

Dedup impact: bounded area block transmutation/world conversion. Any Black Arcana mutation/transmutation mechanic requires distinct authority and `WorldEffectPolicy` for Black Arcana-owned mutations; it must not re-run Hexalia's provider changes.

## 10. Kelpweave Blade — water/rain mobility weapon

- ritual output: `hexalia:kelpweave_blade`
- class: custom SwordItem

### Melee hit
Applies vanilla Movement Slowness:

- duration `100 ticks = 5 s`;
- amplifier `0`.

### Water/rain dash
Use can begin only while player `isInWaterOrRain()` and the item is not on cooldown.

On release:

- minimum charge: `10 ticks = 0.5 s`;
- charge fraction: `min(usedTicks / 20.0, 1.0)`;
- forward speed: `1.8 + charge × 1.2`;
- vertical lift: `0.25 + charge × 0.20`;
- sets player velocity from look vector, resets fall distance;
- starts auto-spin attack for `20 ticks` with `8.0F` damage parameter;
- cooldown: `60 ticks = 3 s`;
- durability cost per dash: `1` unless creative.

At maximum one-second charge, the source formula yields forward speed `3.0` and lift term `0.45` before look-vector Y contribution.

### Water/rain self-repair
While the stack is damaged and the owning inventory-tick entity is a Player touching water/rain, every server inventory tick has `5%` chance to repair one durability point.

Dedup impact: aquatic dash/mobility weapon + self-repair + slow. It is not an Iron's spell or Black Arcana cast.

## 11. Rootshaper — adaptive 3×3 mining tool

- ritual output: `hexalia:rootshaper`
- tool modes: pickaxe / shovel
- mining speed constant: `9.0`
- attack damage bonus: `+4.0`
- attack speed modifier: `-2.8`

Left-clicking a block recomputes the tool mode from target tags, preferring pickaxe when applicable, then shovel.

### Shift 3×3 break
On server `BlockEvent.BREAK`, if the player:

- is holding Rootshaper in main hand;
- is holding Shift;

Hexalia computes a 3×3 plane perpendicular to the dominant player-look axis. For each of the eight adjacent positions it checks:

- not air;
- destroy speed >= 0;
- Rootshaper is correct tool for drops;

then calls `player.gameMode.destroyBlock(adjacentPos)`.

A ThreadLocal `BREAKING` guard prevents recursive Rootshaper expansion from nested break events.

Dedup/progression impact: these are explicitly player-gameMode block breaks in the source path, which is stronger causal evidence than an autonomous machine. Even so, any RPG Mastery integration must deduplicate the original break and up to eight induced breaks according to an explicit progression contract rather than assuming every secondary block is an independent spell action.

## 12. Sage Pendant — XP-orb tripling with durability cost

- ritual output: `hexalia:sage_pendant`
- item durability: `32`
- active location: player **offhand** only
- NeoForge boundary: `PlayerXpEvent.PickupXp`

On XP orb pickup while the Sage Pendant is in offhand:

`newOrbValue = value + floor(value × 2.0)`

For ordinary nonnegative integer XP orb values, this is exactly `3 × value`.

Each qualifying pickup damages the pendant by `1` durability unless the player is creative.

Dedup/progression impact: Hexalia is already mutating the actual XP orb value at pickup. RPG Skill Tree or Black Arcana must not multiply the already-boosted value again unless a separate explicit contract intentionally consumes post-provider XP. No synthetic XP reward loop should be created from observing the pendant.

## 13. Bloomwrap armor — four distinct nature-linked defenses/buffs

### Bloomwrap Hat
- output: `hexalia:bloomwrap_hat`
- while worn in HEAD slot, provider knockback helper multiplies incoming knockback strength by `0.20` (`80%` reduction).
- NeoForge applies this through `LivingKnockBackEvent`.

### Bloomwrap Robes
- output: `hexalia:bloomwrap_robes`
- while worn in CHEST slot and incoming damage source entity is another LivingEntity, provider reflects `15%` of the post-provider incoming event amount back as thorns damage.
- NeoForge path: `LivingIncomingDamageEvent`.

### Bloomwrap Leggings
- output: `hexalia:bloomwrap_leggings`
- player tick check every `20 ticks`;
- scans AABB radius `4.0` for vanilla small/tall flowers;
- if any flower is found, applies Regeneration `60 ticks`, amplifier `0`.

### Bloomwrap Boots
- output: `hexalia:bloomwrap_boots`
- player tick check every `20 ticks`;
- if block below is tagged Dirt, Leaves, Small Flowers or Tall Flowers, applies Movement Speed `60 ticks`, amplifier `0`.

Dedup impact: nature-conditioned armor already covers knockback resistance, damage reflection, flower-linked regeneration and terrain-linked speed. Black Arcana/RPG equipment perks must avoid double-processing these provider-owned effects.

## Output classification summary

| Output family | Count | Primary capability |
|---|---:|---|
| elemental reagent nodes | 4 | ritual/crafting resource components |
| persistent magical plants | 7 | Aegiflora, Astrylis, Grimshade, Nautilite, Windsong, Lourdes, Morphora |
| cultivated projectile line | 1 | Rabbage Seeds → Rabbage Bleeding projectile |
| ritual tools/weapons/accessories | 3 | Kelpweave Blade, Rootshaper, Sage Pendant |
| ritual armor pieces | 4 | Bloomwrap Hat/Robes/Leggings/Boots |
| **total player-facing outputs** | **19** | matches Nature's Ritual recipe catalog |

## Black Arcana authority rule

These outputs remain Hexalia-owned after the ritual finishes. Their subsequent ticks, attacks, block changes, XP pickup modifications, projectiles and equipment events are **not** new Black Arcana casts merely because the player originally created the item through a ritual.

Future bridges must preserve:

- causal provenance;
- exactly-once progression settlement;
- provider resource/equipment/world authority;
- bounded scans/effects;
- `WorldEffectPolicy` only for world changes Black Arcana itself initiates;
- fail-closed behavior when no supported provider event/API exists.
