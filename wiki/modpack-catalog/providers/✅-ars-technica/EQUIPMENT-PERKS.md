# Ars Technica 2.7.6 — equipment and perks

Status: `SOURCE-PINNED EQUIPMENT/PERK CONTRACT`

Source checkpoint: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`.

## Armor families — 12/12

Three four-piece Ars magic-armor families are registered:

1. Technomancer — `technomancer_helmet`, `technomancer_chestplate`, `technomancer_leggings`, `technomancer_boots`;
2. Artificer / Light Technomancer — `artificer_cap`, `artificer_tunic`, `artificer_pants`, `artificer_shoes`;
3. Machinaguard / Heavy Technomancer — `machinaguard_helmet`, `machinaguard_chestplate`, `machinaguard_leggings`, `machinaguard_boots`.

All three classes extend Ars `AnimatedMagicArmor`, implement `ISpellModifierItem` and `IManaDiscountEquipment`, expose Ars armor-perk data, and report minimum armor tier 2.

### Common mana/Manipulation behavior

Every piece computes its mana discount from the spell recipe by summing **20% of the configured casting cost of every spell part that belongs to Ars Manipulation**. The provider returns the ceiling of that sum as the equipment discount.

COMMON source defaults applied per piece:

- max mana attribute: **+100** (`armorMaxMana`, configurable 0–10,000);
- mana regen bonus: **+4** (`armorManaRegen`, configurable 0–100).

Manipulation-power differences per equipped piece:

- Artificer: **+2** Manipulation Power;
- Technomancer: **+1** Manipulation Power;
- Machinaguard: **+0.5** Manipulation Power.

Technomancer additionally adds **+0.025 knockback resistance** per piece in its audited class. The Artificer and Machinaguard classes do not add that same modifier in the audited source.

These bonuses are provider/Ars equipment modifiers. RPG Skill Tree may gate or expose progression only through a real integration contract; it must not become owner of these mana, school-power or thread semantics.

## Armor perk-provider layout

`ArsNouveauRegistry.postInit()` registers every one of the 12 armor items as an Ars `PerkRegistry` provider. For each armor item, the source supplies four perk groups, and each group accepts `PerkSlot.ONE`, `PerkSlot.TWO` or `PerkSlot.THREE`.

The provider also adds Sauce's elemental armor-up recipe type to Ars Nouveau's enchanting recipe types. This is provider-owned equipment progression, not a Black Arcana unlock surface.

## Pressure Thread

Registry id: `ars_technica:thread_pressure`.

Provider description: ultra-high-pressure air stored through an Ars armor thread for use by other tools.

The exact implementation is not merely descriptive:

- server-side `AnimatedMagicArmorMixin` finds the armor stack holding the highest Pressure perk instance;
- a persistent float component `ars_technica:air` stores the reserve;
- outside water, per inventory tick air gain is `(2 × pressurePerkCount - 1) × 0.01`;
- cap is `600 + pressurePerkCount × 300`;
- while underwater, the source path subtracts 1 air every 20 game ticks;
- client-side the current component value is mirrored into persistent entity data `VisualBacktankAir` for presentation;
- `BacktankUtilMixin` intercepts Create `BacktankUtil.getAllWithAir()` and returns the Pressure-bearing armor stack when present.

Therefore the Pressure reserve is a provider-owned Ars-Technica/Create bridge. Black Arcana must not create, mirror, refill or debit a second air/pressure account for the same capability.

## Transmutation Focus

Registry id: `ars_technica:transmutation_focus`.

It is an Ars Nouveau Curio and `ISpellModifierItem`. Its exact source behavior includes:

- unconditionally adding Ars `Fortune` to the spell-stat builder when its item modifier participates;
- acting as `hasFocus()` for provider processing logic;
- doubling Polish and Press normal processing capacity;
- multiplying Polish base speed 2.0 and Press base speed 4.0 by **2.5×**;
- increasing Whirl processing cadence in the provider processing path;
- causing the provider `EffectCrush` mixin to double stack count only for CrushRecipe outputs whose chance is below 100%, capped at the result item's max stack size;
- being treated as always present by `TransmutationTurretSpellResolver`.

These are modifications of one Ars/provider spell context. A second generic Fortune/yield proc sourced from Black Arcana around the same processing event would violate deduplication.

## Schematicannon set proximity

When enabled in COMMON config (default `true`), `SchematicannonMixin` checks for a nearby player wearing any complete Ars Technica armor family or a tagged Curio. Default range is **8 blocks**. While Create's Schematicannon is RUNNING and a qualifying player is nearby, the provider decrements `printerCooldown` by one additional tick every second game tick.

This is an Ars Technica modification of Create's machine cadence. Create remains owner of the Schematicannon's printing lifecycle and material consumption. Black Arcana must not replay cannon ticks or infer a second processing operation from the speed boost.

The audited implementation performs its local ServerPlayer AABB query from the Schematicannon tick path. Performance/compatibility under the current large pack is a runtime QA item, not a Black Arcana behavior to reproduce.