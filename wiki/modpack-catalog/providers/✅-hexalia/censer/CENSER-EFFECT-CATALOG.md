# Hexalia 1.3.6 — Censer Effect Catalog

## Status

`SOURCE-PINNED 1.3.6 / HERB COMBINATIONS 10/10 / EXECUTION LIFECYCLE AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Canonical source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

Installed pack identity remains `hexalia-neoforge-1.3.6.jar` with runtime metadata reporting `1.3.5`. The behavior below is therefore release-line source evidence, not exact installed-runtime acceptance evidence.

## Provider-owned lifecycle

The Censer is a persistent Hexalia herb-combination effect source, not a Black Arcana cast surface.

Source-pinned execution:

- the block entity stores exactly two single-item herb slots;
- herbs may be inserted only while the Censer is unlit;
- both inputs must satisfy `#hexalia:herbs` at normal player insertion;
- only combinations registered in `CenserEffectRegistry` may ignite;
- successful ignition consumes/clears both stored herbs;
- ignition may be performed by a player with a provider-recognized fire starter or by dispenser path;
- the chosen `HerbCombination` and burn time are persisted;
- provider default effect radius: `16` blocks;
- provider default burn duration: `7200 ticks = 360 s = 6 min`;
- effect interval: `40 ticks = 2 s`;
- the handler is applied once directly at ignition and the block-entity tick also applies while `burnTime % 40 == 0`;
- shovel interaction can extinguish an active Censer;
- when burn time reaches zero, the Censer clears its active combination and extinguishes itself.

Because the ignition path calls the effect immediately and the first server tick can observe the initial `7200` value as divisible by 40, exact first-pulse cadence should be runtime-tested rather than normalized away in Black Arcana.

## 10/10 combinations

| Combination | Provider key/name | Source-pinned effect |
|---|---|---|
| Siren Kelp + Spirit Bloom | Tidewarden | Players in Censer area receive Resistance I for 120 ticks and Slow Falling I for 120 ticks. |
| Ghost Fern + Siren Kelp | Ethereal Grazing | Searches adult breed-ready `Animal` entities in the area and nearby same-type partners within 4 blocks; calls provider/vanilla child-spawn breeding path. |
| Dreamshroom + Siren Kelp | Tide's Memory | Tries up to 20 random positions around the Censer for water; on success spawns either Kelp or a Prismarine Shard item entity. |
| Dreamshroom + Spirit Bloom | Miner's Respite | Players receive Night Vision I for 240 ticks and Haste I for 120 ticks; a bounded local block scan probabilistically repairs Damaged Anvil→Chipped Anvil or Chipped Anvil→Anvil. |
| Dreamshroom + Ghost Fern | Phantom Drift | Item entities in the area are teleported to a point 0.75 blocks from the Censer along their current radial direction and their velocity is zeroed. |
| Ghost Fern + Spirit Bloom | Undead Veil | Undead mobs in the area are calmed: target/last-hurt references are cleared, persistent anger is stopped/cleared where applicable, and path navigation stops. |
| Witchweed + Ghost Fern | Withering Calm | Every LivingEntity in the area receives Wither I for 80 ticks; mobs are additionally calmed. This includes players because the source filter is `LivingEntity`, not hostile-only. |
| Witchweed + Spirit Bloom | Hollow Aura | Every LivingEntity in the area has every currently active MobEffect removed. This is a full status-effect purge, not harmful-only cleansing. |
| Witchweed + Dreamshroom | Blighted Bloom | Performs a bounded local world mutation: up to 6 changes per application; Dirt/Grass Block can become Mycelium, Mycelium can grow red/brown mushrooms above, and Mushroom Cows have a random chance to become brown variant. |
| Witchweed + Siren Kelp | Tidal Pull | Pulls Animals, Monsters and ItemEntities toward the Censer by adding bounded distance-scaled velocity. Players and arbitrary non-matching entities are not selected by this handler. |

Combination ordering is normalized by Hexalia's `HerbCombination` key semantics; the catalog treats each registered pair as one provider recipe identity.

## Quantitative execution notes

### Tidewarden

Each application refreshes:

- `minecraft:resistance`, duration 120 ticks, amplifier 0;
- `minecraft:slow_falling`, duration 120 ticks, amplifier 0.

The provider's 40-tick pulse interval means these effects overlap/refresh while the Censer remains active.

### Ethereal Grazing

The handler does not merely set animals into love mode. It directly calls `spawnChildFromBreeding(level, second)` for qualifying same-type adults within squared distance ≤16. This is provider-owned reproductive settlement and must not be duplicated by a Black Arcana tick hook.

### Tide's Memory

Each pulse performs at most 20 random water-position attempts and spawns at most one item when water is found. The output is randomly Kelp or Prismarine Shard.

### Miner's Respite

The scan is spatially bounded to x/z `±radius` and y `±2`; each scanned position passes a `1/12` random gate before an anvil repair attempt. One application can therefore affect multiple anvils, but only inside that bounded local volume.

### Phantom Drift

This is item relocation rather than a continuous velocity magnet. Each matching item is teleported close to the Censer center and stopped.

### Withering Calm

The Wither application is broad: all living entities in the AABB, including players and non-hostile mobs. Only Mob instances receive the calming side effect.

### Hollow Aura

The handler removes the full current active-effect set from each LivingEntity. It does not distinguish beneficial, harmful, Hexalia, Black Arcana or external-provider MobEffects.

Cross-mod consequence: any Black Arcana mechanic represented as a vanilla/NeoForge `MobEffect` could be removed by this provider behavior if present in range. Corruption/Strain channels that are not MobEffects must not be incorrectly mapped into this purge just to create compatibility.

### Blighted Bloom

This is destructive/world-mutating provider behavior, but its own implementation does not use Black Arcana `WorldEffectPolicy`. Black Arcana must not intercept and re-settle provider block mutation as if it were a Black Arcana cast. If the modpack requires cross-provider world-protection compatibility, it needs a verified boundary and explicit policy decision rather than duplicate mutation.

### Tidal Pull

Selection is explicitly bounded to `Animal`, `Monster` or `ItemEntity`. The velocity magnitude uses `0.12 / clamp(distance, 1, radius)` along the normalized direction toward the Censer.

## Deduplication impact

The Censer occupies several semantic spaces simultaneously:

- defensive aura/buff field;
- animal reproduction automation;
- resource/item generation;
- utility repair aura;
- item displacement;
- undead/mob pacification;
- hostile Wither field;
- full status dispel/cleanse field;
- bounded local terrain mutation;
- telekinetic pull field.

Black Arcana should not clone these as generic persistent witch-aura spells. A future forbidden field can exist only when its identity, admission, cost, hazards, authority and bounded effects are materially distinct.

## Authority and safety rules

- Hexalia owns Censer herb validation, burn state, pulse timing and effect settlement.
- Do not turn each 40-tick pulse into a Black Arcana cast or mastery event.
- Dispenser ignition has no causal player by construction; progression systems must fail closed rather than invent ownership.
- Do not double-apply breeding, item generation, anvil repair, MobEffect purge, mob calming or block mutation.
- Black Arcana `WorldEffectPolicy` remains authoritative only for Black Arcana-originated destructive effects; provider-originated Censer mutations require a separate interoperability contract if pack-wide protection is desired.
- Public implementation classes/functional interfaces are not treated as a stable external API.

## Runtime/API QA blockers

1. resolve physical release filename `1.3.6` versus installed runtime metadata `1.3.5`;
2. verify all 10 combinations and default config values in the installed pack;
3. verify first-pulse cadence after ignition, including the immediate call plus block-entity modulo path;
4. verify cross-mod status removal caused by Hollow Aura;
5. verify world-protection interaction for Blighted Bloom and automated/dispenser ignition;
6. identify a supported provider event/API before any Black Arcana progression bridge is enabled.
