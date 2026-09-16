# Ars Nouveau — Armor Perk Slot Providers

State: `SOURCE-PINNED 5.13.1 / 12 PROVIDERS VERIFIED`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

`PerkRegistry.registerPerkProvider(...)` defines the allowed perk-slot topology for Ars armor. The lists below are provider data, not RPG Skill Tree nodes. Slot values are Ars' `PerkSlot.ONE/TWO/THREE` = 1/2/3.

The three nested lists registered per armor item correspond to that item's perk-holder tiers 0/1/2; the item UI/code presents armor tier as `perkHolder.getTier() + 1`, so this page labels them Armor Tier 1/2/3.

| Provider item constant | Armor Tier 1 | Armor Tier 2 | Armor Tier 3 |
|---|---|---|---|
| `BATTLEMAGE_BOOTS` | `[1]` | `[1,1]` | `[1,1,2]` |
| `BATTLEMAGE_HOOD` | `[1]` | `[1,1]` | `[1,1,2]` |
| `BATTLEMAGE_LEGGINGS` | `[1]` | `[1,2]` | `[1,1,3]` |
| `BATTLEMAGE_ROBES` | `[1]` | `[1,2]` | `[1,1,3]` |
| `ARCANIST_HOOD` | `[1]` | `[1,2]` | `[1,1,3]` |
| `ARCANIST_BOOTS` | `[1]` | `[1,2]` | `[1,2,2]` |
| `ARCANIST_LEGGINGS` | `[1]` | `[1,3]` | `[1,2,3]` |
| `ARCANIST_ROBES` | `[1]` | `[1,3]` | `[1,2,3]` |
| `SORCERER_BOOTS` | `[1]` | `[1,2]` | `[1,2,3]` |
| `SORCERER_ROBES` | `[2]` | `[2,3]` | `[2,2,3]` |
| `SORCERER_LEGGINGS` | `[2]` | `[2,3]` | `[2,2,3]` |
| `SORCERER_HOOD` | `[1]` | `[1,2]` | `[1,2,3]` |

## Perk application semantics

`AnimatedMagicArmor#getDefaultAttributeModifiers` walks the perk instances stored in the armor's `ARMOR_PERKS` component and calls each perk's `applyAttributeModifiers(..., instance.getSlot().value(), EquipmentSlotGroup.bySlot(...))`. It then also adds Ars-owned armor-derived `MAX_MANA` and `MANA_REGEN_BONUS` attributes based on armor tier.

The server-side equipped-armor tick also invokes `ITickablePerk.tick(...)` for tickable perks and calls `RepairingPerk.attemptRepair(...)`.

## Deduplication / authority

- Slot topology belongs to Ars Nouveau.
- A Tier-3 Ars perk slot is **not** equivalent to an RPG Skill Tree perk tier.
- RPG Skill Tree may only gate/provide progression through a real bridge; it must not rewrite `ARMOR_PERKS`, reinterpret slot values or duplicate Ars attribute modifiers.
- Black Arcana must observe provider-native outcomes rather than replaying Thread logic.
- External armor/perk integrations must preserve item identity and event causality; fail closed if a safe API boundary cannot be verified.
