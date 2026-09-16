# `efiscompat` 3.1.0 — data-driven animation and presentation

Exact source revision: `domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4`.

This file catalogs presentation/runtime identities so Black Arcana can deduplicate safely without treating visual mappings as spell content.

## Animation registry

`Animation.registerAnimations(...)` creates an Epic Fight animation builder under namespace `efiscompat`.

The exact source declares **35 animation accessor fields** across three semantic families:

- cast animations;
- chant animations;
- continuous animations.

They include one-hand, two-hand, staff-left/right, bow, flying, stomp, explosion and other pose variants. Some entries are `StaticAnimation`, some are `AimAnimation`, and flying variants use `ActionAnimation` properties.

These are **animation identities**, not magic/spell registrations.

One source animation (`CHANTING_TWO_HAND_BOW`) reads Iron's server casting state to adjust animation play speed. This remains presentation timing around Iron's state; it does not authorize or execute the spell.

## Data reload surface

`EpicFightIronCompat` installs a NeoForge `AddReloadListenerEvent` listener that adds `SpellAnimationLoader`.

`SpellAnimationLoader` is a `SimpleJsonResourceReloadListener` rooted at:

`spell_animations`

On reload it:

1. clears the in-memory mapping;
2. reads every JSON resource in that reload namespace/path;
3. extracts each `spells` object;
4. builds an `AnimationSet` for every named spell entry;
5. skips a mapping whose animation construction throws;
6. exposes lookup by spell name.

No second spell registry is created. The string key is used solely to choose animation behavior for a spell already owned by Iron's or an Iron's addon.

## Nine-field mapping schema

Each spell animation set can provide:

1. `chant_animation`
2. `cast_animation`
3. `continuous_animation`
4. `staff_chant_animation_r`
5. `staff_cast_animation_r`
6. `staff_chant_animation_l`
7. `staff_cast_animation_l`
8. `staff_continuous_animation_r`
9. `staff_continuous_animation_l`

Empty strings are treated as null. Missing or invalid per-field values can fall back to the `default` animation set.

If a spell name has no dedicated mapping, lookup falls back to `default` as a whole.

## Default mapping

The exact built-in `default.json` maps:

- chant → `CHANTING_ONE_HAND_TOP`;
- cast → `CASTING_ONE_HAND_TOP`;
- continuous → `CONTINUOUS_TWO_HAND_FRONT`;
- right staff chant → `CHANTING_ONE_HAND_STAFF_RIGHT`;
- right staff cast → `CASTING_ONE_HAND_STAFF_FRONT_RIGHT`;
- left staff chant → `CHANTING_ONE_HAND_STAFF_LEFT`;
- left staff cast → `CASTING_ONE_HAND_STAFF_FRONT_LEFT`;
- right staff continuous → `CONTINUOUS_ONE_HAND_STAFF_RIGHT`;
- left staff continuous → `CONTINUOUS_ONE_HAND_STAFF_LEFT`.

This default is provider presentation policy, not a spell-domain default for Black Arcana.

## Animation resolution

`Animation.getAnimation(name)` resolves in this order:

1. public field on the provider `Animation` class;
2. public field on Epic Fight `Animations`;
3. explicit animation registry key when the string contains `:`;
4. otherwise null with a warning.

The provider therefore permits data packs to select either built-in compat animations, Epic Fight animations or registry-addressable animation IDs.

Black Arcana must not infer that an arbitrary animation registry key is a stable gameplay hook.

## Staff selection

`SpellAnimationProvider` chooses the correct member of the nine-field set using:

- cast phase (`CHANT`, `CAST`, `CONTINUOUS`);
- main-hand staff state;
- off-hand staff state.

`CompatUtils` considers an item staff-like when either:

- the item is an Iron's `StaffItem`; or
- the item's registry ID occurs in provider config `staffWeapon`.

The default staff list contains provider-selected Iron's item IDs. Catalog records the mechanism but does not promote that mutable list into a Black Arcana staff taxonomy.

## Event-driven animation selection

`PlayerAnimationEvents` is server-player scoped for the Iron's cast events it handles.

### Pre-cast

For LONG casts it selects `CHANT`; for CONTINUOUS casts it selects `CONTINUOUS`, then synchronizes the Epic Fight animation when one resolves.

### On cast

For non-continuous casts it selects `CAST`, clears the middle layer, and synchronizes the selected cast animation.

Continuous animation is started at the pre-cast phase instead of the on-cast phase.

The provider relies on Epic Fight synchronization; no separate Black Arcana network protocol is created by this catalog.

## Client mixin inventory

Exact required client mixins:

1. `MixinRenderItemBase`
2. `MixinFirstPersonRenderer`
3. `MixinPlayerAnimatorCompat`
4. `MixinIronAnimationHelper`
5. `MixinChargeSpellLayerVanilla`
6. `MixinHotbarChangeInventory`

Together with the 6 common mixins documented separately, the exact mixin manifest contains 12 required entries.

Catalog closure does not assert that every client target remains stable on the physical host versions; that remains runtime QA.

## Bundled third-party mappings

The exact resource tree includes data-driven mapping files under provider-owned `spell_animations` for:

- Iron's Spells itself;
- ESS Requiem;
- Traveloptics / T.O Magic n' Extras;
- the provider default mapping.

The existence of a mapping means only “the compat knows an animation preference for that spell name.” It does not transfer ownership of the mapped spell to `efiscompat` and does not create a new semantic spell entry.

The physical pack currently includes Iron's `3.16.3`, ESS Requiem `0.1.7`, and Traveloptics `4.4.0.1-1.21.1`. Mapping correctness against those exact physical addon versions remains runtime QA.

## First-person configuration boundary

The publisher README recommends disabling Iron's own first-person casting arms/items when using this compat:

- `showFirstPersonArms = false`
- `showFirstPersonItems = false`

That recommendation concerns overlapping presentation paths. It does not alter server cast authority.

Black Arcana must not programmatically mutate those Iron's client settings as part of BA gameplay authority.

## Config surface used by presentation

- `staffWeapon`
- `hideTwoHandedItems`
- `hideOffHandItems`

Casting-interaction config values are documented in the cast-interaction file.

## Black Arcana disposition

| Provider surface | Semantic class | BA disposition |
|---|---|---|
| 35 animation accessors | presentation | do not count as spells; do not copy assets |
| spell animation JSON mapping | presentation data | do not count as spells/domains |
| Epic Fight synchronized animation | provider-native presentation | do not create parallel Iron's-specific animation channel |
| staff classification list | provider-local presentation config | do not reuse as BA equipment authority |
| Iron's spell ID lookup | host identity read | Iron's remains spell owner |
| BA-native cast visuals | Black Arcana presentation | future separate adapter only, driven by BA canonical state |
| BA server cast validity | Black Arcana runtime | never inferred from animation state |

## Clean-room rule

No animation JSON, animation model, texture, source implementation or provider asset is copied into Black Arcana by this audit. Source/data are inspected read-only to identify authority, deduplication and future interoperability constraints.