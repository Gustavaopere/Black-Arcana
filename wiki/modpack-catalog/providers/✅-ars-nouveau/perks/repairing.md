# Repairing

- Registry ID: `ars_nouveau:thread_repairing`
- Source class: `RepairingPerk`
- Minimum slot: Tier 1 (inherited default).
- Tick cadence: `attemptRepair()` returns unless game time is divisible by 200 and the stack is damaged.
- Repair level: `PerkUtil.countForPerk(thread_repairing, entity)`.
- Repair amount: `min(currentDamage, (int)repairLevel + Config.BASE_ARMOR_REPAIR_RATE)`.
- Cost: exactly 20 Ars mana per successful repair tick; no repair occurs if current mana < 20.
- Tier-3 aggregate behavior: when effective Repairing count is >=3, `onAdded()` marks all equipped armor stacks with Ars' `UNBREAKING` data component. `onRemoved()` clears that component from all armor slots.
- Caller surface confirmed in 5.13.1: equipped `AnimatedMagicArmor` calls `attemptRepair` from its server-side `inventoryTick`; Enchanter's Sword/Shield also expose inventory-tick callers in this provider line.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 1 Anvil + 2 Manipulation Essence; `sourceCost: 0`.

## Authority / integration

Repairing spends **Ars Nouveau mana** and mutates Ars/magical equipment durability. Black Arcana must not charge a second resource, repair the same tick again, or mirror the tier-3 unbreakable marker. Resource settlement remains provider-native.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`. Config-resolved `BASE_ARMOR_REPAIR_RATE` remains runtime/config QA rather than an invented numeric default.