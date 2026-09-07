# Hexalia 1.3.6 — Relics, wards, binding and wearables

## Status

`SOURCE-PINNED 1.3.6 / HIGH-IMPACT INDEPENDENT CAPABILITIES AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Canonical source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

This page covers significant Hexalia behavior that does not fit cleanly under Small Cauldron, Nature's Ritual, Celestial Infusion, Mutation, Mortar & Pestle, Censer or the idol family.

Installed pack identity remains `hexalia-neoforge-1.3.6.jar` with runtime metadata `1.3.5`; source-derived formulas remain runtime-QA gated.

# Spiritroot Tether — persistent Mob binding/transport

## Acquisition

Source-pinned shaped recipe:

- `hexalia:earth_node`;
- `minecraft:ender_pearl`;
- three `minecraft:string` in the registered pattern.

Registered item durability: `32`.

## Capture authority

`SpiritrootTetherItem` captures only targets that are `Mob` instances.

Capture is rejected when:

- the Mob entity type is in `#hexalia:spiritroot_uncapturable`;
- the Mob is currently a vehicle;
- the Mob has a passenger;
- the Mob implements `OwnableEntity` and is owned by someone other than the interacting player;
- or the Mob is not alive under the remaining admission path.

For an admitted Mob, the provider stores:

- entity type ResourceLocation;
- serialized Mob NBT produced by `saveWithoutId`;
- original UUID;
- encoded custom name when present.

The original Mob is then discarded and the tether loses one durability.

This is a real persistent binding/containment mechanism, not a visual leash and not a soul-resource abstraction.

## Release

Using a tether containing a Mob on a block without shift:

- attempts to reconstruct the stored entity via `EntityType.loadEntityRecursive`;
- places it above the clicked block;
- marks reconstructed Mob instances as persistence-required;
- clears captured-Mob data on successful release;
- costs one durability.

The provider contains a retry path using the stored original UUID when needed.

## Anchor binding / cross-dimensional dispatch

When the tether contains no Mob, shift-use on a block tagged `#hexalia:spiritroot_bound_blocks` stores:

- target dimension;
- target BlockPos.

When a Mob is captured and a valid anchor has previously been recorded, shift-use can reconstruct the Mob above that bound location in the stored target dimension, clear the captured Mob and cost one durability.

### Deduplication significance

This occupies a concrete typed entity-binding/transport role.

Black Arcana Binding must not duplicate "capture arbitrary admitted Mob NBT into handheld object and release it at a bound anchor" as a generic spell with no materially different identity.

It does **not** prove:

- blood-link authority;
- ownership of an entity's soul;
- external provider mana/resource authority;
- player-to-player binding;
- Black Arcana contract/curse authority.

Any future bridge must preserve the provider's capture admission, owner restrictions, NBT persistence and durability cost. Do not create a second serialized Mob snapshot.

# Dreamcatcher — fueled anti-Phantom ward

## Acquisition

Source-pinned shaped recipe uses:

- Sticks;
- String;
- Feathers;
- one `hexalia:fire_node`.

## Fuel model

The placed Dreamcatcher has persistent fuel state.

- only `hexalia:fire_node` is accepted as fuel;
- one inserted Fire Node grants `30000` fuel ticks;
- fuel decrements only while it is night;
- while fuel remains, shift + empty-hand extraction returns one Fire Node and zeroes the remaining fuel.

This means the Fire Node is provider fuel for the Dreamcatcher but does not establish a global Fire Node energy pool.

## Ward behavior

Every 20 ticks, while night and fueled:

- scans `Phantom` entities in an AABB inflated by `HexaliaConfig.dreamcatcherRadius()`;
- source default radius is `16`;
- ignites each Phantom for `HexaliaConfig.phantomIgniteDuration()`;
- source default ignition duration is `100` ticks = 5 seconds;
- applies Slowness amplifier `1` for `60` ticks = Slowness II for 3 seconds.

### Deduplication significance

Dreamcatcher is a persistent, fuel-backed anti-Phantom ward. Black Arcana should not duplicate this as a generic passive anti-Phantom field.

It does not establish broad ward authority over arbitrary hostile mobs, projectiles, magic or dimensions.

# Thornbow — ammunition-free bleeding bow

## Acquisition

Source-pinned shaped recipe:

- `hexalia:earth_node`;
- `hexalia:rabbage`;
- Sticks;
- String.

Registered durability: `128`.

## Execution

The Thornbow:

- starts bow-style charging without checking for an arrow stack;
- directly creates its own `ThornArrowEntity` server-side;
- projectile speed is `power * 3.0F`;
- fully charged projectiles are marked critical;
- costs `2` bow durability per shot;
- generated Thorn Arrows cannot be picked up.

`ThornArrowEntity` has base damage `1.5D` and, on hitting a LivingEntity, applies `hexalia:bleeding` amplifier 0 for `60` ticks = 3 seconds.

### Deduplication significance

This occupies an ammunition-free botanical bleeding-weapon niche. It does not create a provider spell-casting pipeline and should not be treated as an Iron's-style spell cast.

# Athame — infrastructure tool, not blood-dagger authority

The source-pinned Athame performs provider infrastructure operations:

- shift-use on planks: removes the plank and drops a Ritual Brazier;
- use on `#hexalia:resin_logs`: converts/strips supported logs and drops Tree Resin;
- use on a Lotus Flower: drops Lotus Blossom and destroys the flower;
- each successful server-side operation costs one item durability where applicable.

No audited Athame path consumes player health, blood fluid or blood-volume resource.

Therefore the Athame must **not** be classified as evidence that Hexalia owns Black Arcana blood sacrifice, Hematic Reservoir or blood-cost casting.

# Briar Sickle — bounded vegetation utility

Briar Sickle is a utility tool rather than a separate spell system.

Source-pinned use behavior:

- scans a horizontal `3×3` centered on the clicked position;
- admits grasses, ferns, flowers, saplings and leaves;
- normal mode destroys with ordinary drops;
- shift mode explicitly drops resources then removes the block;
- successful area clear costs one durability.

It has faster destroy speeds for vegetation and standard main-hand attack modifiers, but no separate magical resource or cast pipeline.

# Wearables and stealth/adaptation

## Earplugs

While worn in the head slot and the player crouches:

- refreshes vanilla Invisibility for 20 ticks when necessary;
- stores a custom-data marker indicating that the invisibility came from this item;
- if damageable, loses one durability every 20 game ticks while sustaining the crouch invisibility in survival;
- when the condition ends, it clears its own marker and removes Invisibility if that marked state existed.

Cross-mod QA is warranted if another provider refreshes Invisibility while the Earplugs marker is active.

## Ghostveil

Ghostveil itself is a chest wearable marker; targeting behavior is implemented through Hexalia's armor behavior helper and the NeoForge target-change event.

Source-pinned target-clearing rule:

- player must wear Ghostveil;
- minimum detect distance is 6 blocks;
- a Mob attempting to target the player can have its new target cleared when distance is >6 and ≤16 blocks;
- while the player crouches, the upper forget distance becomes 24 blocks.

This is target-acquisition interference, not vanilla Invisibility.

## Bogshade Boots

When worn:

- while the player is in water/bubble: refreshes Water Breathing I for 60 ticks and Dolphin's Grace I for 60 ticks;
- otherwise, if grounded above a block in `#hexalia:bogshade_no_slow`, refreshes Speed I for 40 ticks.

This is provider equipment adaptation rather than spellcasting.

# Silkweave and Moonweave — magic resistance

Hexalia stores per-piece magic-resistance percentages through persistent item data components.

Source-pinned values:

- each Silkweave piece: `0.05` = 5%;
- each Moonweave piece: `0.10` = 10%;
- matching complete set bonus: `0.10` = 10%;
- combined resistance is clamped to `0.0–1.0`.

Therefore source-level complete-set totals are:

- full Silkweave: `4 × 5% + 10% = 30%`;
- full Moonweave: `4 × 10% + 10% = 50%`.

The audited NeoForge incoming-damage hook applies Hexalia resistance to:

- `minecraft:magic`;
- `minecraft:indirect_magic`;
- `minecraft:wither`;
- `minecraft:dragon_breath`.

Moonweave also has a separate brewing interaction: a full Moonweave set multiplies generic Hexalia `BrewItem` duration by `1.5`.

### Integration consequence

Black Arcana must not assume this is a universal resistance to every custom Black Arcana damage source. Compatibility depends on the actual DamageType/tag/classification Black Arcana uses and requires runtime integration testing.

# Decorative exclusions

## Candle Skull / Wither Candle Skull

Source inspection found light/extinguish, waterlogging, particles and sound only. The Wither variant uses soul-fire visual particles but no audited status aura, necromancy field or curse behavior.

These blocks are therefore classified as decorative/ambient for the magic-capability matrix and should not reserve a spell domain merely because of their aesthetic.

# Black Arcana integration rules

- Spiritroot Tether is a provider-owned persistent binding/transport system; do not duplicate its stored Mob state or pretend a captured Mob is a Black Arcana soul object.
- Dreamcatcher is a provider-owned fueled ward; passive Phantom ticks are not casts/mastery events.
- Thornbow is a weapon/projectile path; preserve projectile causality if any external progression hook is ever added.
- Athame is not a blood-cost authority.
- Wearable effects remain provider-owned passive equipment effects and must not enter the Black Arcana cast pipeline.
- Hexalia magic resistance must be treated according to actual DamageType interoperability, not thematic similarity.
- Source implementation classes remain non-contractual for integration unless a stable external boundary is verified.

# Runtime/API QA blockers

1. reconcile public/source `1.3.6` with installed runtime metadata `1.3.5`;
2. validate Spiritroot Tether entity admission, cross-dimensional release and persistence against the installed modpack;
3. test Dreamcatcher fuel/runtime defaults in the installed JAR;
4. verify Thornbow Bleeding and damage interaction with the pack's combat pipeline;
5. verify Earplugs/Ghostveil interaction with external stealth/AI mods;
6. verify Silkweave/Moonweave resistance against Black Arcana custom DamageTypes before intentionally supporting it;
7. do not enable provider-specific progression adapters without a supported causal event/boundary.
