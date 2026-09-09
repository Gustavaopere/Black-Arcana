# Registry and content surface — Apothic Attributes 2.10.1

Exact source: `Shadows-of-Fire/Apothic-Attributes@686361b2c7b0e76bf4158890bb8a2e42ef805622`.

## Central bootstrap

`ALObjects.bootstrap(IEventBus)` bootstraps and registers the provider's central registry helper. The exact closed inventory is below.

## Custom synchronized registries

- `apothic_attributes:entity_equipment_slot`
- `apothic_attributes:entity_slot_group`

## Attributes — 22

1. `armor_pierce`
2. `armor_shred`
3. `arrow_damage`
4. `arrow_velocity`
5. `cold_damage`
6. `crit_chance`
7. `crit_damage`
8. `current_hp_damage`
9. `dodge_chance`
10. `draw_speed`
11. `experience_gained`
12. `fire_damage`
13. `ghost_health`
14. `healing_received`
15. `life_steal`
16. `mining_speed`
17. `overheal`
18. `projectile_damage`
19. `prot_pierce`
20. `prot_shred`
21. `elytra_flight`
22. `cooldown_reduction`

All 22 are added through `EntityAttributeModificationEvent` to living entity types by the provider bootstrap/runtime.

## Mob effects — 7

- `bleeding`
- `detonation`
- `grievous`
- `knowledge`
- `sundering`
- `vitality`
- `flying`

## Potions — 31

- resistance / long_resistance / strong_resistance
- absorption / long_absorption / strong_absorption
- haste / long_haste / strong_haste
- fatigue / long_fatigue / strong_fatigue
- wither / long_wither / strong_wither
- sundering / long_sundering / strong_sundering
- knowledge / long_knowledge / strong_knowledge
- vitality / long_vitality / strong_vitality
- grievous / long_grievous / strong_grievous
- levitation
- flying / long_flying / extra_long_flying

## Damage types — 5

- `bleeding`
- `detonation`
- `current_hp_damage`
- `fire_damage`
- `cold_damage`

Provider datapack taxonomy:

- `neoforge:is_magic`: detonation, fire_damage, cold_damage;
- `neoforge:is_physical`: current_hp_damage;
- `minecraft:bypasses_armor`: bleeding, detonation, fire_damage, cold_damage;
- `apothic_attributes:cannot_critically_strike`: current_hp_damage + `#bypasses_invulnerability`;
- `apothic_attributes:is_non_physical`: joined magic/poison/wither/fire/explosion/lightning/freezing families.

## Data components — 2

- `bonus_attribute_modifiers` — deprecated for removal; persistent + network-synchronized vanilla `ItemAttributeModifiers` representation;
- `bonus_stack_attribute_modifiers` — persistent + network-synchronized provider `StackAttributeModifiers` representation.

## Attachments — 3

- `pre_damage_health` — temporary pre-damage health fact;
- `aux_dmg_tracker` — serialized auxiliary-damage tracker;
- `cooldowns` — serialized, synchronized cooldown tracker with copy-on-death behavior.

## Equipment-slot surface

Built-in provider slot objects — 7:

- mainhand, offhand, head, chest, legs, feet, body.

Provider slot groups — 11:

- any
- any_vanilla
- mainhand
- offhand
- hand
- head
- chest
- legs
- feet
- armor
- body

These are an attribute-modifier abstraction. They are not Black Arcana loadout slots or cast slots.

## Other registry objects

- particle: `apoth_crit`
- sound: `dodge`
- provider tag contracts: `dynamic_base`, `is_non_physical`, `cannot_critically_strike`

## Spell-content result

No standalone Apothic Attributes spell/glyph/ritual registry surface was observed in the exact source. The provider contributes combat/attribute/effect infrastructure and consumable potion content, not a parallel magic cast engine.
