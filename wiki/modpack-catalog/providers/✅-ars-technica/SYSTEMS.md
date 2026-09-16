# Ars Technica 2.7.6 — provider systems

Status: `SOURCE-PINNED SYSTEM CONTRACT / INSTALLED RUNTIME QA OPEN`

Exact source checkpoint: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`.

## Authority map

| System | Native authority | Black Arcana boundary |
|---|---|---|
| Player mana / Ars spell recipe / caster | Ars Nouveau | never debit or settle a second Ars mana transaction |
| Source storage/network | Ars Nouveau | no parallel Source balance or mirrored transfers |
| Create kinetics/stress/recipes | Create | no duplicated recipe output, stress or kinetic settlement |
| Ars Technica processing entities | Ars Technica | descendants of the provider cast; do not reclassify as new BA casts |
| Pressure thread / `air` component | Ars Technica + Ars perk system + Create backtank bridge | no second air/pressure reserve |
| Technomancer armor threads | Ars PerkRegistry | RPG Skill Tree/BA may only interact through real provider contracts |
| Source Motor | Ars Technica conversion boundary: Ars Source → Create rotation | observe if needed; never settle Source or stress twice |
| Transmutation Turret | Ars Technica + Ars turret/caster contracts | one provider Source/cast transaction; no replay |
| Precise Relay | Ars relay/source machinery | cooldown customization does not make BA owner of transfers |

## Source Motor

Registry: `ars_technica:source_motor` / `source_motor_block_entity`.

The block entity extends Create `GeneratingKineticBlockEntity` and is registered with provider stress capacity 256 and generator speed 256.

Exact source properties:

- generated-speed UI range: **−256..+256 RPM**;
- stress-capacity ratio state is persisted as `GeneratedStressUnitsRatio`;
- normal Source Motor UI constrains that ratio to **0..100%**;
- `Fueled` and `HasRedstoneSignal` are persisted;
- once every 20 block-entity ticks, while not redstone-disabled, it attempts provider Source consumption;
- Source lookup/debit uses Ars `SourceUtil.takeSourceMultipleWithParticles(..., 10, sourceCost)`;
- successful/failed debit owns the `fueled` state, which in turn gates generated rotation;
- generated speed becomes zero if unfueled, redstone-disabled or no longer the expected Source Motor block.

### Source-cost formula

Let:

- `r = generatedStressUnitsRatio / 100`;
- `v = abs(configured RPM)`;
- `m = sourceMotorSpeedToSourceMultiplier`, source default **4.0**.

The provider computes:

`round(r × v × m)` Source per one-second consumption attempt.

If `r == 0` or the motor is overstressed, cost is zero. For a non-zero ratio/speed combination that rounds to zero, the source path returns a minimum cost of 1.

This conversion is already one transactional Ars→Create boundary. Black Arcana must not debit Source after observing motor rotation and must not create a second stress/energy account around it.

## Precise Relay

Registry: `ars_technica:precise_relay` / `precise_relay_tile`.

`PreciseRelayTile` derives from Ars `RelayTile`. Server-side transfers remain Ars Source transfers between `AbstractSourceMachine` block entities. Ars Technica only changes scheduling frequency and presentation.

Cooldown state:

- custom `-1` means provider default scheduling, one transfer opportunity per 20 game ticks;
- `0` means no modulo stall in the provider function;
- any other custom value schedules on `gameTime % customCooldown == 0`;
- custom value is persisted in NBT;
- normal UI range is controlled by COMMON config: default minimum **5 ticks**, maximum **600 ticks**.

The Arcane Wrench conversion path accepts only the exact base Ars `Relay` class, replaces it with Precise Relay server-side, preserves the old block-entity NBT, then initializes cooldown to the configured relay minimum. Other relay subclasses are deliberately not converted.

## Ars Rune cooldown customization

`RuneTileMixin` adds a persistent `ticksUntilChargeCount` to Ars `RuneTile`. When set, the mixin overwrites the host rune's `ticksUntilCharge` after `castSpell`. Provider fallback/default is 40 ticks. The normal GUI range defaults to **5..600 ticks** through COMMON config.

This changes Ars rune cadence but not cast authority or cost ownership.

## Transmutation Turret

Registry: `ars_technica:transmutation_turret` / `transmutation_turret_block_entity`.

The provider extends Ars `BasicSpellTurretTile` and keeps Ars turret behavior dispatch.

For a stored spell:

1. it computes source cost as `spell.getCost() × transmutationTurretSourceCostMultiplier`;
2. COMMON source default multiplier is **2.0**;
3. if cost > 0, it atomically requires Ars Source through `SourceUtil.takeSourceMultipleWithParticles` before cast execution;
4. it sends the Ars one-shot turret animation;
5. it constructs the Ars fake player and `TileCaster` context;
6. its specialized resolver executes through Ars `TURRET_BEHAVIOR_MAP` when a supported cast type exists.

`TransmutationTurretSpellResolver` treats the provider Transmutation Focus as present. Any descendant resolver remains the specialized resolver.

Therefore this is one server-owned Source→Ars-spell operation. Black Arcana must not separately settle the spell's nominal mana cost, duplicate the Source charge, or count resolver descendants as new user casts.

## Fuse / Arcane Fusion

`glyph_fuse` creates `ArcaneFusionEntity` using the provider's own child spell context. The entity searches nearby item/fluid ingredients, resolves a Create Mixing recipe appropriate to the selected fusion type and consumes only the resources selected for the bounded number of iterations.

Important exact bounds/behavior:

- AOE factor stored by the entity is `1 + spellStats.getAoeMultiplier()`;
- recipe iterations are clamped to at most `round(AOE × 4)` after item/fluid availability;
- result items are spawned once at impact;
- result fluids are first offered to nearby fluid handlers, then may be placed into nearby air blocks;
- provider config `fluidCanBePlaced` default: `true`;
- `fluidSourcesCanBePlaced` default: `true`;
- `fluidMaxPlacementsPerFuse` default: **16**, allowed range 1–256;
- provider fluid placement uses 1000 mB as a full fluid block and searches a local AABB around the fusion result.

These are provider-native world mutations. They are not retroactively sent through Black Arcana `WorldEffectPolicy`; that policy remains mandatory only for Black Arcana-owned destructive/world-mutating effects. A future BA effect must not use provider behavior as an excuse to bypass its own policy.

## Whirl processing

`glyph_whirl` creates `ArcaneWhirlEntity`; its processing mode is chosen from the following Ars part after Whirl:

- Conjure Water → Create Splashing/Washing;
- Flare → Smoking;
- Smelt → Blasting;
- Hex → Haunting.

The provider owns the processing entity and its Create recipe settlement. Transmutation Focus increases provider processing cadence. Black Arcana must not interpret each processed stack as another cast/proc chain.

## Apply / Insert / Telefeast world and inventory mutation

These spell parts interact directly with provider/NeoForge item/fluid capabilities or recipe results:

- Apply consumes/uses the provider-selected application item and may replace a block with a recipe result or spawn a result item;
- Insert moves nearby item entities into valid item handlers/containers and supports split distribution;
- Telefeast extracts and consumes/forwards eligible food/drink items or compatible fluid-filled outputs, preserving returned containers where implemented.

Their item/fluid/block effects settle inside the provider operation. Black Arcana observation must be non-replaying and causal.

## COMMON source defaults relevant to interoperability

| Config | Default | Source range/meaning |
|---|---:|---|
| `armorMaxMana` | 100 | 0–10,000, per armor piece |
| `armorManaRegen` | 4 | 0–100, per armor piece |
| `schematicCannonSpeedBoostEnabled` | true | enables nearby Technomancer acceleration |
| `schematicCannonSpeedBoostRange` | 8.0 | provider proximity range |
| `sourceMotorSpeedToSourceMultiplier` | 4.0 | 0–100 |
| `fluidCanBePlaced` | true | Fuse result-fluid world placement |
| `fluidSourcesCanBePlaced` | true | permits full source-fluid blocks |
| `fluidMaxPlacementsPerFuse` | 16 | 1–256 |
| `runeMinCooldown` | 5 | 0–40 |
| `runeMaxCooldown` | 600 | 40–6000 |
| `relayMinCooldown` | 5 | 0–40 |
| `relayMaxCooldown` | 600 | 40–6000 |
| `transmutationTurretSourceCostMultiplier` | 2.0 | 0.1–10.0 |
| `obliterateFortuneBaseChance` | 0.15 | 0.0–5.0 |

These are source defaults. Installed generated config values have not yet been compared and are not claimed equal to these defaults.

## Version-drift/runtime gate

Ars Technica 2.7.6 source declares dependencies compatible with Ars Nouveau `[1.21.1-5.11,)`, Create `[6.0.8,)` and NeoForge `[21.1.205,)`, but the source build itself pins Ars 5.11.0.1267/Create 6.0.8 while the pack is on newer host versions. Version ranges are not proof that mixins and behavioral assumptions still work. Dedicated-server/full-pack QA remains required.