# Vampiric Ageing 1.21-1.4.21 — state authority

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## `AgeingManager` is canonical

Vampiric Ageing attaches a synchronized `AgeingManager` to supported players/entities through NeoForge attachment storage and TeamLapen sync helpers.

Canonical player state includes:

- `IAgeType type` / serialized `typeId`;
- `IAgeMethod method`;
- `int ageRank`;
- `int rankProgress`;
- optional Age-Type-specific `TypeState`.

Serialized player keys include:

- `ageing_type`;
- `ageing_rank`;
- `ageing_rank_progress`;
- type-specific fields.

Black Arcana must not create a second authoritative representation of those values in scoreboards, tags, capability mirrors or custom persistent NBT.

## Type/method resolution

`CapabilityHelper.setDefaultAgeTypeAndMethod(player)` resolves the current Vampirism/Werewolves faction against the registered Age Types, selects the enabled matching type and then selects the enabled method whose `getValidType()` matches that type.

This means faction/provider state precedes the Ageing layer. A Black Arcana gate must fail closed if the expected provider faction/type/method cannot be resolved.

## Rank changes

`AgeingManager.increaseRankPoints(...)` is the progression settlement authority. On threshold crossing it increments exactly one rank and resets progress to zero. It then syncs the attachment.

`onAgeChange(...)` is also the reconciliation point for:

- old-type attribute cleanup;
- current age-based transient attributes;
- provider Skill enable/disable;
- creation/reset of type-specific state where applicable.

Do not emulate this reconciliation after changing an external Black Arcana state; observe the provider's resulting state instead.

## Hunter `HunterState`

Hunter has a dedicated `TypeState` containing:

- `taintedAgeBonus` → `ageing_tainted_age`;
- `taintedTicks` → `ageing_tainted_ticks`;
- `ticksInSun` → `ageing_sun_ticks`;
- `transformed` → `ageing_transformed`.

`CapabilityHelper.getCumulativeTaintedAge(player)` is the canonical derived-age function:

- returns 0 outside Hunter/Tainted-Blood authority;
- returns 0 when there is no temporary tainted bonus and no permanent transformation;
- otherwise uses `baseAge + temporaryBonus`;
- permanent transformation substitutes a fixed bonus of 6.

Hunter death handling separately resets temporary Tainted Blood state and resets permanent transformation only when `permanentTransformationDeathReset` is enabled. Default for that config is false.

## Faction changes

The provider listens for Vampirism faction-level changes. Losing a faction / changing faction can clear Age Type, Age Rank and progress and re-run provider type/method selection. Hunter-specific Tainted effects/transformation receive additional cleanup on leaving Hunter.

Any Black Arcana perk whose validity depends on an Age Type must therefore revalidate after faction changes rather than assuming an unlock remains permanently valid.

## Death and reset policy

Global `deathReset` defaults to true. `ageLostOnDeath=0` is documented by the provider as the full-reset behavior; positive values may reduce the rank by that configured amount instead. Hunter Tainted state has its own death lifecycle as described above.

Black Arcana must not persist an Age-derived benefit across provider death/faction reset unless its own design explicitly says it is independent of Vampiric Ageing and cannot create a contradictory provider state.

## Provider action/cache state

Action active/cooldown state belongs to the Vampirism/Werewolves Action handlers. Additional transient extension state includes:

- Vampire water-walking flag;
- Hunter ageing Bat Mode flag;
- `AgeingPlayerCache.hasBypassInvisibility` for Wise Eye / Improved Senses;
- Hunter Tainted timers/solar state.

These are implementation surfaces, not independent progression resources. They should be read only when a stable hook is required and runtime compatibility is proven.

## Fail-closed rule

When the exact installed provider does not expose a safe stable read for Age Type, method, rank, progress, cumulative Tainted Age or Action state, the integration must decline to activate rather than guessing from visible effects, attributes, advancement text or player tags.
