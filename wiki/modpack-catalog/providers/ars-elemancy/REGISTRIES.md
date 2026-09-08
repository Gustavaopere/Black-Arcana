# Ars Elemancy 1.18.3 — exact registry surface

Status: `SOURCE-PINNED / RUNTIME REGISTRY QA PENDING`

Source: `Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`.

## Items

`ModItems` owns one Item DeferredRegister and constructs:

- 7 foci;
- 7 essences;
- 7 bangles;
- 7 medium ArmorSets × 4 pieces = 28;
- 7 light ArmorSets × 4 pieces = 28;
- 7 heavy ArmorSets × 4 pieces = 28.

Total: **105 item registrations**.

`FusedEssence` exists as a class but is not registered by `ModItems` at this checkpoint and is not counted.

## Blocks

A Block DeferredRegister exists, but no provider block registration was found in `ModItems`: **0 owned blocks**.

## Armor materials

`AAMaterials` registers **33 ArmorMaterial entries**:

- 12 base elemental materials: light/medium/heavy × Fire/Water/Earth/Air;
- 21 fused/Elemancer materials: light/medium/heavy × Tempest/Silt/Mire/Vapor/Lava/Cinder/Elemental.

The 21 fused/Elemancer materials back the 21 owned armor sets. The 12 base-element material entries are support/compat registry surface, not 12 additional owned armor sets.

## Ars spell/perk surface

- `ArsNouveauRegistry.registerGlyphs()` is empty;
- `registeredSpells` receives no local spell parts;
- `registerPerks()` is empty;
- local glyph count: **0**;
- local perk count: **0**.

Three `PerkSlot` values are inserted into Ars' `PerkSlot.PERK_SLOTS` map:

- `ars_elemancy:four` = 4;
- `ars_elemancy:five` = 5;
- `ars_elemancy:six` = 6.

These are slot values, not perks or RPG progression nodes.

## Recipe/config auxiliary registries

`ModRegistry` registers:

- one CreativeModeTab: `general`;
- one local RecipeType named `armor_upgrade`;
- one local RecipeSerializer named `armor_upgrade`, backed by Sauce `ElementalArmorRecipe.Serializer`.

Tracked effective recipe JSONs for armor use `type: sauce:armor_upgrade`; therefore the existence of the local `ars_elemancy:armor_upgrade` registration is recorded separately from the resource recipe type and not normalized by assumption.

The DataComponentType and condition-codec DeferredRegisters are attached to the bus, but no local entries were found at this checkpoint.

## Damage tags

Four DamageType TagKeys are declared:

- `ars_elemancy:fire_damage`
- `ars_elemancy:water_damage`
- `ars_elemancy:earth_damage`
- `ars_elemancy:air_damage`

Use of damage/absorption behavior ultimately delegates through Sauce/Ars Elemental contracts; exact effective tag population remains datapack/runtime QA.