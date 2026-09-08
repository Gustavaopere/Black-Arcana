# Ars Elemental 0.7.10.1 — registry inventory

Status: `BOOTSTRAP + HIGH-IMPACT REGISTRIES SOURCE-PINNED / FULL ITEM-ID FLATTENING NOT REQUIRED FOR PHASE 2U`

Source checkpoint: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`.

## Bootstrap

`ArsElemental` registers STARTUP, COMMON and CLIENT configs, then calls:

1. `ModRegistry.registerRegistries(modEventBus)`;
2. `ArsNouveauRegistry.init()`;
3. during common setup, `ArsNouveauRegistry.postInit()` and `CompatUtils.checkCompats()`.

This is the runtime reachability boundary used by Phase 2U.

## NeoForge registry families

`ModRegistry.registerRegistries()` wires provider registers for:

- armor materials;
- blocks;
- items;
- entity types;
- block entities;
- menus;
- particles;
- mob effects;
- potions;
- enchantments;
- attributes;
- recipe types and serializers;
- worldgen features;
- block-state-provider type;
- creative tab;
- data components.

## Provider keys and tags

DamageType ResourceKeys:

- `ars_elemental:beheading`
- `ars_elemental:poison`
- `ars_elemental:hellfire`
- `ars_elemental:spark`
- `ars_elemental:water_jet`
- `ars_elemental:cavitation`

Enchantment ResourceKeys:

- `ars_elemental:mirror_shield`
- `ars_elemental:soulbound`

Relevant provider tags:

- `ars_elemental:blacklist_bag_item`
- `ars_elemental:soulbound_extra`
- `ars_elemental:attraction_ritual_blacklist`
- `ars_elemental:charm_blacklist`
- `ars_elemental:fiery`
- `ars_elemental:aerial`
- `ars_elemental:insect`

## Recipe infrastructure

Custom recipe types/serializers:

- `ars_elemental:head_cut`
- `ars_elemental:netherite_upgrade`

The provider also registers config-condition codec `sauce:ae_config`, which is used by Nullify Defense's generated glyph recipe gate.

`postInit()` adds the provider Netherite Upgrade recipe type to Ars Nouveau's enchanting-recipe type list.

## Data component

Provider data component `ars_elemental:p4e` stores `ElementProtectionFlag` with persistent and network-synchronized codecs. It participates in dropped-item protection and alternate client spellbook texture behavior.

## Source capability

Advanced Collector, Depositor, Warp and Splitter relay block entities expose Ars Nouveau `SOURCE_CAPABILITY` by returning their own Source storage. This is Ars Source ownership, not a Black Arcana resource.

## Ars API registries

Production Ars-facing registrations:

- GlyphRegistry: 39 spell parts;
- RitualRegistry: 8 rituals;
- FamiliarRegistry: 3 familiars;
- PerkRegistry: 3 perks;
- Perk providers: 48 armor items;
- SpellCasterRegistry: 8 caster items.

## Entity types

The provider source registers 32 EntityTypes, covering:

- Siren, Flarecannon/Firenando and Flashjack base/familiar entities;
- Flashing Weald Walker;
- four elemental mages;
- provider summons;
- spell/projectile/marker entities for magnet, interpolation, lightning, spikes, phalanx, Water Jet, geysers and Mist Cloud.

An EntityType being registered does not prove a corresponding player-accessible glyph. `phalanx_projectile` is the key example: the associated MethodCarianPhalanx glyph is development-only in the production registration path.

## Network registry

Protocol `1` registers exactly two payloads:

- play-to-server Curio Bag open intent;
- play-to-client Discharge visual payload.

See `SYSTEMS.md` for authority details.