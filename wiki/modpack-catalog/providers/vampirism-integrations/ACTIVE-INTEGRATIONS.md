# Vampirism Integrations 1.10.2 — Current-Pack Integration Inventory

Status: `CURRENT 612-MOD SNAPSHOT RECONCILED / SOURCE ELIGIBILITY CATALOGED / RUNTIME ACTIVATION UNCONFIRMED`

Source pin: `TeamLapen/VampirismIntegrations@bff02b9686408691aea2c0c910ccb712edb18bd5`.

## How activation works

`ModCompatLoader` only prepares a registered compat when all of the following are true:

1. its target mod id is loaded by NeoForge;
2. the generated compatibility config entry is enabled;
3. the target version satisfies the compat's accepted range, when one is declared;
4. setup does not throw; an exception unloads that compat from the loader.

Therefore source presence, target presence and a default-enabled config are only **eligibility evidence**. They do not prove that the compat actually prepared in the user's exact runtime.

Jade is a special case: its current plugin is not routed through `ModCompatLoader`; Jade discovers `JadePlugin` through `@WailaPlugin`. Target presence plus that discovery path proves that the plugin is discoverable, but exact runtime registration still belongs to runtime QA.

## Central loader registrations in 1.10.2

| Compat | Target mod id | Current modlist | Current-pack status |
|---|---|---|---|
| Vampirism base | `vampirism` | present `1.10.13` | ELIGIBLE / required base target present |
| BOP | `biomesoplenty` | absent | DORMANT |
| WAILA | `waila` | absent | DORMANT |
| EvilCraft | `evilcraft` | absent | DORMANT |
| CraftTweaker | target provider not installed | absent | DORMANT |
| Tough As Nails | target provider not installed | absent | DORMANT |
| MCA | `mca` | absent | DORMANT |
| CTOV | target provider not installed | absent | DORMANT |
| Cold Sweat | `cold_sweat` | present `2.4.2` | **ELIGIBLE / DEFAULT-ENABLED / RUNTIME UNCONFIRMED** |
| Guard Villagers | target provider not installed | absent | DORMANT |

Several old compat classes still exist in the repository but are explicitly commented out in the 1.10.2 central registration list. They are not counted as current loader capabilities merely because files remain in source.

## Eligible bridge A — Cold Sweat 2.4.2

### Compatibility gate

`ColdSweatCompat` declares:

- target mod id `cold_sweat`;
- accepted version range `[2.2.3,)`;
- current pack target `2.4.2`, which satisfies that declared range;
- configuration enabled by default.

Those facts make the bridge eligible under stock configuration. They do **not** prove that the user's actual generated config still enables it or that setup completed without exception.

### Config defaults

| Config | Default | Meaning in source |
|---|---:|---|
| `enableTemperatureVampires` | `true` | enables Vampire temperature modifiers |
| `vampireColdResistance` | `30` | subtract 30 °C-equivalent from Cold Sweat freezing point after provider unit conversion |
| `vampireBurningPointModifier` | `0.7` | total-multiplier factor applied to Cold Sweat burning point |

### Settlement path if the compat actually loads

On player login, respawn or Vampirism faction-level change:

1. query `Helper.isVampire(player)`;
2. obtain Cold Sweat `freezing_point` and `burning_point` attributes;
3. for Vampires, add transient modifiers with id `vampirism:vampire_modifier` when absent;
4. for non-Vampires, remove those modifiers.

Cold modifier:

- operation: `ADD_VALUE`;
- amount: provider conversion of `-vampireColdResistance` from Celsius to Cold Sweat Minecraft units.

Heat modifier:

- operation: `ADD_MULTIPLIED_TOTAL`;
- amount: `-1 + vampireBurningPointModifier`;
- default amount therefore `-0.3`, i.e. the burning-point attribute is scaled by provider attribute semantics to the configured 0.7 factor.

### Authority boundary

The integration never owns core body temperature. Cold Sweat remains authority for:

- world/body temperature calculation;
- insulation;
- environmental sources;
- freezing/burning thresholds;
- consequences of thermal exposure;
- its own attribute evaluation.

Black Arcana must not add a second generic Vampire temperature modifier on top of this bridge. Until runtime activation is proven, consumers that require this compat specifically must fail closed rather than assuming the modifier exists.

## Discoverable bridge B — Jade 15.10.6

### Discovery path

`JadePlugin` is annotated `@WailaPlugin`. It is therefore discoverable by Jade's plugin scanner independently of the central Vampirism Integrations loader when Jade is present.

The current modlist contains Jade, so the source-level state is **TARGET PRESENT / PLUGIN DISCOVERABLE**. Exact plugin registration/rendering remains runtime QA rather than an inferred PASS.

### Common/server data providers

The plugin registers block/entity data providers for:

- Garlic Diffuser;
- Totem;
- Pedestal;
- Alchemy Table;
- Potion Table;
- player faction.

### Client components

The plugin registers components for:

- entity blood (`PathfinderMob`);
- player faction;
- entity faction;
- Garlic Diffuser;
- Totem;
- Pedestal;
- Alchemy Table;
- Potion Table;
- Weapon Table;
- Altar of Inspiration;
- Altar of Infusion;
- Research/Hunter Table;
- Altar Pillar.

### User-facing Jade configuration owned by this plugin

Confirmed keys include:

- `vampirism:entity_blood.max_for_render` — default 40, range 0–100;
- `vampirism:entity_blood.icon_per_line` — default 10, range 5–300;
- `vampirism:entity_blood.show_fraction` — default false;
- `vampirism:player_faction.lord_level_number` — default false.

These options only change presentation. They do not alter the underlying Vampirism data.

## Supported but inactive conditional data maps

The provider ships data-driven contracts whose entries are conditionally activated only if the external target exists.

### Entity blood/conversion

| External target | Contract | Current pack |
|---|---|---|
| MCA male/female villager | blood `15`; custom `vampirism_integrations:mca` converter | inactive — `mca` absent |
| Capybara | blood `10`; default Vampirism converter + overlay | inactive — target entity/mod absent |

### Fluid blood conversion

| Fluid | Conversion rate | Current pack |
|---|---:|---|
| `biomesoplenty:blood` | `0.4` | inactive |
| `evilcraft:blood` | `0.8` | inactive |
| `bloodmagic:life_essence_fluid` | `0.8` | inactive |
| `tconstruct:blood` | `0.8` | inactive |

### Item blood

- `evilcraft:blood_orb_filled` → blood value `800`, conditional on EvilCraft; inactive in current pack.

## Source modules that must not be promoted automatically

The exact 1.10.2 repository still contains source/config references for systems that are not current eligible bridges. Examples include Survive and several `old/` integrations. The central registration list comments many of these out.

The rule is strict: **compiled/source-present ≠ registered ≠ target-installed ≠ eligible ≠ runtime-active**.

## MineColonies boundary

MineColonies is installed in the current pack and appears in the provider's Gradle/deploy dependency configuration. No current MineColonies Java compat module or `ModCompatLoader` registration was found at the exact 1.10.2 pin. It therefore remains `NO CURRENT AUDITABLE RUNTIME BRIDGE FOUND`, not active or eligible through the central loader.

## Runtime confirmation command

The addon registers:

`/vampirism-integrations loaded`

It reports compats actually prepared by the central `ModCompatLoader`. This command is the direct runtime gate for the Cold Sweat loader path in the exact installed pack. It does not prove independent plugin discovery such as Jade, so Jade must be validated separately in runtime QA.

Until those checks are executed, the catalog state remains **source-eligible/discoverable**, not runtime-confirmed.