# Ace's Spell Utils — network, mixins and example objects

Source scope: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`.

## Network registry

`PayloadHandler` creates an optional versioned registrar with protocol string `4.0.0` and registers **8 play-to-client payloads**:

1. `AddShaderEffectPacket`
2. `RemoveShaderEffectPacket`
3. `TriggerImpactFramePacket`
4. `TriggerChromaticAberrationPacket`
5. `TriggerRibbonPacket`
6. `TriggerRoarPacket`
7. `TriggerDomePacket`
8. `TriggerShakePacket`

No C2S payload is registered in that exact handler. These packets transport visual/client presentation instructions; they are not evidence of a client-authoritative cast/resource protocol.

Black Arcana should not route magic intent through these visual payloads or treat receipt of a VFX packet as proof that a server-authoritative Black Arcana action occurred.

## Required mixins — 2

The mixin config is `required: true`, `defaultRequire: 1`, and contains two server/common mixins.

### `LivingEntityMixin`

Injects after writes to `LivingEntity.invulnerableTime` in:

- `hurt(...)`;
- `handleDamageEvent(...)`.

It adds the entity's `evasive` attribute value to `invulnerableTime`.

Because the same source also has an Evasive NeoForge event handler, exact combined runtime behavior is provider-owned and must be tested rather than re-derived by Black Arcana.

### `PlayerMixin`

Injects cancellably at the head of `Player.dropEquipment`. When the server player has `keep_inv_on_death`, the drop is canceled.

This works with provider attachment/events. Black Arcana must not install another equivalent death/drop hook for provider state.

## Example item registry — 27 real registrations

`ExampleItemRegistry.register(...)` is invoked unconditionally by the mod constructor. The creative tab alone is dev-environment gated. Therefore these are real source registry entries even though their intended role is demonstration/support.

### API/item examples — 11

- `example_sheath`
- `example_staff`
- `example_curio`
- `example_imbue_staff`
- `example_imbue_curio`
- `example_passive_ability_spellbook`
- `example_unqiue_ability_spellbook` — registry spelling preserved
- `example_gun`
- `example_ap_sword`
- `example_ap_magic_sword`
- `example_loot_bag`

### VFX examples — 12

Impact-frame variants:

- `example_impact_frame_white`
- `example_impact_frame_red`
- `example_impact_frame_blue`
- `example_impact_frame_green`
- `example_impact_frame_purple`
- `example_impact_frame_white_aberration`

Other VFX examples:

- `example_chromatic_aberration`
- `example_trail`
- `example_ribbon`
- `example_roar`
- `example_roar_ring`
- `example_dome`

### Armor examples — 4

- `example_armor_helmet`
- `example_armor_chestplate`
- `example_armor_leggings`
- `example_armor_boots`

Total: **27**.

## Recipe-viewer hiding

The exact data tag `c:hidden_from_recipe_viewers` explicitly lists 10 example items:

- example sheath/staff/imbue staff;
- example curio/imbue curio;
- example passive ability spellbook;
- example loot bag;
- example gun;
- example AP sword;
- example AP magic sword.

The tag does **not** list all 27 registry entries. Do not generalize it into “all examples are hidden” or “examples are not registered”.

## Example passive-ability runtime

`SpellbookAbilities` contains two example event handlers for the two passive spellbook examples. On a qualifying damage event, equipped example books can use their cooldown helper and spawn an Iron's `Comet` entity.

These are demonstration/runtime objects bundled by the utility mod. They are not standalone `AbstractSpell` registrations and therefore do not increase the provider spell count above zero.

They do, however, prove why Black Arcana must not treat “example” as synonymous with “dead code”: provider events may reference those registered objects.

## Creative tab boundary

The custom Ace's Spell Utils creative tab is registered only when `!FMLEnvironment.production`. This affects discoverability, not the unconditional registration of `ExampleItemRegistry` or its referenced event behavior.

## Deduplication rule

- 27 example items = registry objects, **not 27 spells**.
- VFX payloads = presentation transport, **not cast authority**.
- passive example procs = provider example runtime, **not Black Arcana proc hooks**.
- required mixins remain provider-owned; do not add overlapping iframe/death hooks without a demonstrated non-duplicating boundary.
