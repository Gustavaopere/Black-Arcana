# Second Wind — Undying Charm

Status: `SOURCE-PINNED 21.3.0 / DEATH-ORDER QA PENDING`

- Registry item: `ars_additions:undying_charm`
- Default charges: 1
- Recharge: 2000 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:totem_of_undying`, `minecraft:crying_obsidian`, `minecraft:glowstone`

## Behavior

On `LivingDeathEvent`, only when the dying entity is a `Player`, the provider:

1. sets health to 1;
2. removes all active effects;
3. applies Regeneration for 900 ticks at amplifier 1;
4. applies Absorption for 100 ticks at amplifier 1;
5. applies Fire Resistance for 800 ticks at amplifier 0;
6. broadcasts the vanilla totem-use entity event;
7. cancels the death event;
8. consumes one charm charge outside creative mode.

## Boundary

This is a provider-owned death-prevention transaction. Black Arcana/RPG death saves must not trigger as if the canceled provider death had completed, and event ordering with other death-prevention providers requires runtime QA.
