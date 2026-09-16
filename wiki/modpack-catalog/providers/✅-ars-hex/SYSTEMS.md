# Ars Hex 5.0.4b — Compatibility Systems

Status: `SOURCE BRIDGES CLOSED / INSTALLED CONFIG + HOST INTEROP QA OPEN`

## Iron's school map

`ISSCompat.postInit()` maps Ars schools to Iron's schools:

| Ars school | Iron's school |
|---|---|
| Elemental Earth | Nature |
| Elemental Fire | Fire |
| Elemental Water | Ice |
| Elemental Air | Lightning |
| Conjuration | Evocation |

The provider also stores Iron school-power/resistance attribute pairs for Nature, Fire, Ice and Lightning. No Evocation pair is added to `schoolAttributes` in this class.

## Ars spell-damage bridge

Listener: `SpellDamageEvent.Pre`

Preconditions:

- target must be a `LivingEntity`;
- current spell-context index must be > 0.

The provider reads the spell part immediately preceding the current context index and loops over that part's Ars schools.

For each mapped school:

`damageBuff = ironSchool.getPowerFor(caster) × IronsSchoolDamageBonusScaling`

`damageRes = ironSchool.getResistanceFor(target)`

`event.damage = event.damage × (1 + damageBuff - damageRes)`

Consequences:

- this is an Ars damage event modified by Iron's attributes; it is not a second Iron's spell execution;
- one mapped school produces one multiplier pass;
- multiple mapped schools on the same part traverse the loop repeatedly, so the source applies factors sequentially;
- provider-specific resistance/power settlement must not be applied again by Black Arcana or RPG progression.

## Optional general Iron's spell-power merge

Source config toggle:

`IronsDamageBonusMerge = false` by default.

When enabled, the exact source obtains:

`target.getAttributeValue(AttributeRegistry.SPELL_POWER)`

and then applies:

`event.damage = event.damage × (1 + targetSpellPower × IronsDamageBonusScaling)`

The use of **target** rather than caster is preserved as an exact source observation. Phase 2W does not silently correct it and does not claim its installed effect until the generated config/runtime is tested.

## Ars Elemental armor → Iron's attribute bridge

Listener: `ItemAttributeModifierEvent`.

When an item implements Sauce `IElementalArmor` and is an `ArmorItem`:

- each mapped Ars school receives `+0.05` `ADD_MULTIPLIED_BASE` to the corresponding Iron school spell-power attribute in that armor slot;
- if a school has no map or no `schoolAttributes` entry, the source returns from the handler;
- when the general merge toggle is enabled, the armor also receives Iron general `SPELL_POWER` with `ADD_VALUE = 1 × IronsDamageBonusScaling`.

The exact installed Ars Elemental 0.7.10.1 `ElementalArmor` implements Sauce `IElementalArmor`, so this bridge is materially relevant to the current pack, subject to runtime version compatibility.

## Iron's particle bridge — 5 registrations

When Iron's is loaded, Ars Hex registers:

1. `ars_hex:wisp_iss`
2. `ars_hex:snowflake_iss`
3. `ars_hex:electricity_iss`
4. `ars_hex:fire_iss`
5. `ars_hex:firefly_iss`

Client providers wrap the corresponding Iron's particle providers. The first four are added to Ars `ParticleTypeProperty` with the source boolean `true`; Firefly uses `false`.

This is presentation compatibility, not client gameplay authority.

## COMMON config surface and alias risk

`HexConfigs.Common` constructs three conceptual fields:

- `IronsDamageBonusMerge` — default `false`;
- `IronsDamageBonusScaling` — conceptual default `0`, range 0..100;
- `IronsSchoolDamageBonusScaling` — conceptual default `1`, range 0..100.

However both scaling fields are defined with the exact persisted path string:

`IronsDamageBonusScaling`

NeoForge's 1.21.1 `ModConfigSpec.ConfigValue` reads/writes by its stored path, so these two source fields cannot be treated as independently persisted keys. Exact installed generation/correction/cache behavior remains a runtime/config QA item; Phase 2W does not invent two separate user settings.

The duplicate path remains present on the later Ars-Unity main snapshot, so it is not merely a transient typo corrected immediately after 5.0.4b.

## Damage-type/tag datagen intent

`AHDamageTypeTagsProvider` contains intended mappings including:

- Iron Lightning/Nature/Fire/Ice magic damage into Sauce Air/Earth/Fire/Water damage tags;
- Ars/Ars Elemental damage types into Iron's Fire/Ice/Lightning/Nature magic tags;
- a Lodestone `IS_MAGIC` tag bridge.

`AHItemTagProvider` similarly contains intended Malum/Hexerei item/block-tag additions.

But the release-aligned committed `src/generated/resources/data/ars_hex/` directory contains only `recipe/`. Because the build does not automatically run data generation, Phase 2W classifies these as **datagen intent, packaged state unconfirmed** until the physical JAR is inspected.

## Version-drift gate

Release-aligned source was built against:

- NeoForge 21.1.210;
- Ars 5.11.0.1267;
- Ars Elemental 0.7.6.12.117;
- Iron's 3.14.8;
- Lodestone 1.8.3.549;
- Malum 1.8.2.150;
- preferred Sauce 0.0.16.46.

Current physical pack contains NeoForge 21.1.248, Ars 5.13.1, Ars Elemental 0.7.10.1, Iron's 3.16.3, Lodestone 1.8.2 and Malum 1.8.2. The Ars Hex JAR exposes nested Sauce 0.0.16.46 in the physical modlist.

There are no Ars Hex mixin targets to validate, but event/API/attribute/library compatibility still requires installed runtime QA.
