# Ars Elemental 0.7.10.1 — systems and authority

Status: `SOURCE-PINNED SYSTEM SURFACE / CONFIG + FULL-PACK QA PENDING`

## Ars-owned resources

Ars Elemental extends Ars Nouveau mana and Source. It does not define a Black Arcana resource channel.

Source-backed provider systems include:

- rituals;
- Everfull Urn and elemental upstream/elevator-style infrastructure;
- Siren generation;
- advanced source relays exposing Ars `SOURCE_CAPABILITY`;
- Enchanting Apparatus recipes and focus upgrades.

Black Arcana must never translate these into a second mana/Source pool or debit them twice.

## Foci

Registered focus items include:

- greater Fire, Water, Air and Earth foci;
- Necrotic Focus;
- lesser Fire, Water, Air and Earth foci.

Source common defaults:

- lesser matching-school cost discount: `0.15`;
- greater matching-school cost discount: `0.25`;
- elemental focus buff defaults: `+1.0` for each school;
- elemental focus debuff defaults: `-1.0` for each school;
- glyph empowering: enabled;
- conditional regeneration bonus: enabled.

These are source defaults, not proof of the user's installed config values.

## Armor

There are 12 elemental armor sets / 48 pieces. Common source defaults expose per-piece Ars mana modifications:

- max mana bonus: 100;
- mana regen bonus: 4.

See `PERKS.md` for provider slot layouts.

## Caster providers

`postInit()` registers eight Ars SpellCaster providers:

1. Spell Horn;
2. Air Caster Tome;
3. Fire Caster Tome;
4. Earth Caster Tome;
5. Water Caster Tome;
6. Anima/Necromancy Caster Tome;
7. Manipulation/Shapers Caster Tome;
8. Chain Lens.

## Ars-core school/augment modifications

`postInit()` adds or expands provider classification/compatibility on Ars core parts:

- Necromancy school: Heal, Summon Vex, Wither, Hex, plus local Life Link/Charm and core Summon Undead;
- Air school: core Cut;
- Fire school: core Evaporate;
- Firework accepts Dampen;
- Launch accepts Extend Time and Duration Down;
- Gravity accepts Sensitive;
- Windshear accepts Fortune.

These are provider-owned changes to the Ars spell graph. A bridge must use the final provider classification rather than maintaining a stale independent school table.

## Turrets and projectiles

Ars Elemental registers normal and rotating turret behaviors for Homing Projectile and Arc Projectile. Turret casts remain Ars casts; entity/projectile creation does not establish a Black Arcana root cast.

## Network

Protocol version: `1`.

Two payloads are registered:

- `ars_elemental:open_curio_bag`, play-to-server. The server resolves the currently equipped CurioHolder before opening its container; the packet carries intent, not inventory authority.
- visual Discharge payload, play-to-client. Its payload type is constructed with `ArsNouveau.prefix("discharge_effect")`, producing namespace `ars_nouveau:discharge_effect` despite implementation in the addon. It carries positions/color for particles and is not damage authority.

## World systems

Provider world behavior includes Flashing Archwood worldgen, themed biomes/features, provider spawn placements, Archwood rituals, Ritual of Awakening extension and configured flashing-biome lightning.

World effects produced by the provider remain provider-owned. Black Arcana's own destructive effects still require `WorldEffectPolicy`.

## Config seam

Important source defaults include:

- `frame_skip_recipe=false`;
- `always_thunder=true`;
- `extra_biomes=1`;
- `homing_nerf=false`;
- `magesAggro=true`;
- Squirrel refresh 600 ticks;
- Pierce Lens limit 10;
- Chain Lens limit 15;
- client focus rendering enabled;
- client alternate netherite spellbook texture enabled.

Installed config and cross-mod behavior require runtime QA before integration assumptions are promoted.