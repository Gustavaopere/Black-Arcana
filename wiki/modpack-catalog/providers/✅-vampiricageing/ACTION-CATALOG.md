# Vampiric Ageing 1.21-1.4.21 — action catalog

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

The installed Black Arcana combination includes Werewolves, so the effective registry surface is **9 Actions**: 8 always registered by Vampiric Ageing plus 1 Werewolf Action registered conditionally.

## Inventory — 9/9

| Faction | Action ID | Provider class |
|---|---|---|
| Vampire | `vampiricageing:drain_blood_action` | `DrainBloodAction` |
| Vampire | `vampiricageing:celerity_action` | `CelerityAction` |
| Hunter | `vampiricageing:hunter_teleport_action` | `HunterTeleportAction` |
| Hunter | `vampiricageing:limited_hunter_batmode_action` | `LimitedHunterBatModeAction` |
| Vampire | `vampiricageing:water_walking_action` | `WaterWalkingAction` |
| Vampire | `vampiricageing:step_assist_action` | `StepAssistAction` |
| Hunter | `vampiricageing:step_assist_hunter_action` | `StepAssistHunterAction` |
| Hunter | `vampiricageing:hunter_wise_eye_action` | `HunterEyeAction` |
| Werewolf | `vampiricageing:improved_senses_action` | `WerewolfEyeAction` |

## Vampire Actions

### Celerity — `vampiricageing:celerity_action`

Default gate: Vampire Age >= **1**.

Defaults:

- cooldown: **60 s** (`*20` in the Action);
- duration: **8 s** (`*20`);
- configured `celerityActionMultiplier`: **1.025**;
- Action applies that configured value through `MOVEMENT_SPEED`, `ADD_MULTIPLIED_TOTAL`.

Static semantic warning: using `1.025` directly as an `ADD_MULTIPLIED_TOTAL` amount is not the same as a conventional 1.025× final multiplier; the implementation adds a +1.025 total-multiplier component. Preserve source behavior until runtime measurement/intent is resolved.

The modifier is provider-created on activation and removed by provider ID on deactivation.

### Blood Tap / Drain Blood — `vampiricageing:drain_blood_action`

Default gate: Vampire Age >= **3**.

Defaults:

- cooldown: **150 s**;
- duration: **45 s**;
- enabled by config.

The Action itself only opens the active window. Settlement occurs in `AgeingEventHandler.onHurt(...)`: when the attacking Vampire has this Action active, the provider derives Vampirism `BITE_TYPE`, delegates to target bite/ExtendedCreature/Player blood state, then calls `VampirePlayer.drinkBlood(...)` and fires the Vampirism drink-blood event.

This is a strict deduplication boundary: Black Arcana must not award an additional blood payout for the same hit.

### Water Walking — `vampiricageing:water_walking_action`

Default gate: Vampire Age >= **4** via the provider Skill handler.

Defaults:

- feature enabled;
- cooldown config: **0**;
- duration config: `Integer.MAX_VALUE`, clamped before conversion to ticks.

Activation toggles a Vampiric Ageing extension field on the Vampire special-attributes object. Provider lifecycle clears it on deactivation.

### Vampire Step Assist — `vampiricageing:step_assist_action`

Default gate: Vampire Age >= **2**.

- adds **+0.5 Step Height** (`ADD_VALUE`);
- default cooldown **0**;
- default duration config `Integer.MAX_VALUE`, clamped before `*20`.

Static units warning: `getCooldown()` returns the config value directly, unlike normal second-based Actions that multiply by 20. The default 0 hides the discrepancy; non-zero configuration requires runtime QA.

## Hunter Actions

### Hunter Teleport — `vampiricageing:hunter_teleport_action`

Default gate: cumulative Tainted Age >= **8** and Hunter Bat Mode inactive.

Defaults:

- cooldown: **20 s**;
- max distance: **35 blocks**;
- enabled.

The provider raycasts the looked-at spot, validates collision/liquid state, temporarily positions the player for validation and then, for a `ServerPlayer`, disconnects riding state and calls `teleportTo(...)`. Failed validation restores the original position and returns false.

### Limited Bat Mode — `vampiricageing:limited_hunter_batmode_action`

Default gate: cumulative Tainted Age >= **10**.

Defaults:

- cooldown: **120 s**;
- duration: **240 s**;
- transformed duration config: `Integer.MAX_VALUE - 1`, clamped before tick conversion;
- flight speed: **0.02**;
- extra food exhaustion/update: **0.008**;
- sun restriction toggle: false by default.

Activation:

- sets Hunter ageing Bat Mode state;
- grants `mayfly`/`flying` and provider flight speed;
- changes player dimensions/pose;
- applies `-1 ADD_MULTIPLIED_TOTAL` to Armor and Armor Toughness while active.

Use is blocked in water, in The End, in a Vampirism bat-blacklisted dimension, while riding, and optionally by sun. Deactivation restores normal flight authority according to spectator/creative state and removes the provider modifiers.

Static control-flow mismatch: initial `canBeUsedBy` rejects `(blacklisted dimension) OR End`; `onUpdate`'s first dimension branch tests `(blacklisted dimension) AND End`. This is recorded for runtime QA and must not be normalized silently.

### Hunter Step Assist — `vampiricageing:step_assist_hunter_action`

Default gate: base Hunter Age >= **4**.

- +0.5 Step Height;
- default cooldown 0;
- effectively persistent default duration via clamped `Integer.MAX_VALUE` config.

Same raw-cooldown units warning as Vampire Step Assist.

### Wise Eye — `vampiricageing:hunter_wise_eye_action`

Default gate: base Hunter Age >= **5**.

Intended/default config surface:

- `wiseEyeCooldown=10`;
- `wiseEyeDuration=120`;
- slowdown enabled.

Activation sets `AgeingPlayerCache.hasBypassInvisibility=true` and, by default, applies Movement Speed `-0.95 ADD_MULTIPLIED_TOTAL`. Deactivation clears both.

Source-level mismatch:

- `getCooldown()` returns `wiseEyeCooldown` directly, with no `*20`;
- **`getDuration()` does not read `wiseEyeDuration` at all**. It reads `HunterAgeingConfig.stepAssistDuration`, clamps it and multiplies by 20. With defaults, the advertised 120-duration setting is therefore not the actual source path.

Any exact timing dependency must remain fail-closed until runtime QA.

## Werewolf Action

### Improved Senses — `vampiricageing:improved_senses_action`

Present because Werewolves is installed.

Default compound gate:

- Werewolf Age >= **5**;
- `improvedSensesSensesRequirement=true`;
- Werewolves `SENSE` skill enabled.

Defaults:

- cooldown config: **10** returned directly by the Action;
- duration config: **120**, clamped then `*20`;
- slowdown enabled.

Activation uses the same provider invisibility-bypass cache as Wise Eye and applies Movement Speed `-0.95 ADD_MULTIPLIED_TOTAL`; cleanup clears both.

Because the cooldown is returned raw while the duration is explicitly converted to ticks, the cooldown's unit semantics require runtime verification before exact-timing integration.

## Shared integration rule

The Vampirism/Werewolves Action handler owns activation, active state, cooldown and lifecycle. Black Arcana may observe provider state or require provider Skills/Age gates, but it must not duplicate movement, blood settlement, invisibility bypass, flight, Step Height or Action cleanup.
