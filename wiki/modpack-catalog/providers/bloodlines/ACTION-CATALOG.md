# Bloodlines 3.0.9 — action catalog

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

All 29 provider actions are registered in `VampirismRegistries.Keys.ACTION`. Bloodlines therefore extends the Vampirism action pipeline instead of creating a parallel action engine. Activation, duration, cooldown, action selection and synchronization remain provider-native; Black Arcana must observe/bridge those settlements rather than emulate them.

## Registry inventory — 29/29

| Bloodline | Count | Registered actions |
|---|---:|---|
| Gravebound | 12 | `gravebound_devour_soul_action`, `gravebound_soul_infusion_action`, `gravebound_lingering_devour`, `gravebound_soul_claiming`, `gravebound_crit_action`, `gravebound_mist_form_action`, `gravebound_end_mist_form_action`, `gravebound_phylactery_teleport_action`, `gravebound_ghost_walk_action`, `gravebound_phylactery_soul_transfer_action`, `gravebound_possession_action`, `gravebound_possession_swap_action` |
| Noble | 5 | `noble_celerity_action`, `noble_mesmerise_action`, `noble_leeching_action`, `noble_invisibility_action`, `noble_flank_action` |
| Zealot | 4 | `zealot_shadowwalk_action`, `zealot_darkcloak_action`, `zealot_wall_climb_action`, `zealot_frenzy_action` |
| Ectotherm | 3 | `ectotherm_frostlord_action`, `ectotherm_dolphin_leap_action`, `ectotherm_ink_splash_action` |
| Bloodknight | 5 | `bloodknight_crimson_leap_action`, `bloodknight_sanguine_infusion_action`, `bloodknight_blood_hunt_action`, `bloodknight_day_walker_action`, `bloodknight_blood_extraction_action` |

## Shared authority rules

- Vampire Bloodline actions subclass Vampirism's Vampire action base; the Bloodline wrapper hides them unless the player belongs to the corresponding Bloodline.
- Gravebound normal actions subclass `DefaultGraveboundAction`, which blocks normal use/selection while cached Mist Form is active.
- Actions attached through `BloodlineActionSkill` remain gated by the Bloodlines skill/rank/point topology described in `SKILL-CATALOG.md`.
- Config values are provider-owned defaults. Integrations must not hardcode them as immutable protocol constants.
- Soul-consuming Gravebound actions route through `GraveboundSoulAction`: activation fails when `currentSouls - cost <= 0`, so a successful action must leave at least 1 Soul. Creative mode bypasses the debit but not the pre-activation Soul availability check.

# Noble actions

## Celerity — `bloodlines:noble_celerity_action`

Default contract:

- cooldown: **60 s**;
- duration: **5 s**;
- rank speed modifier (`ADD_MULTIPLIED_TOTAL`): **0 / 0.20 / 0.40 / 0.60**;
- Step Height +0.5 from configured Bloodline rank **3** onward;
- enabled by config.

The action adds permanent modifiers for the action window and removes them on deactivation. Provider action lifecycle is therefore the cleanup authority.

## Mesmerise — `bloodlines:noble_mesmerise_action`

Default:

- cooldown **60 s**;
- duration **20 s**;
- enabled by config.

The action toggles the Bloodlines extension flag on Vampirism special attributes. The downstream mesmerise behavior must remain provider-owned.

## Leeching — `bloodlines:noble_leeching_action`

Default:

- cooldown **120 s**;
- duration **10 s**;
- enabled by config.

Activation:

- sets the Noble leeching mode to 1, or 2 when Enhanced Leeching is enabled;
- adds `+0.5 ADD_MULTIPLIED_BASE` to Vampirism `BLOOD_EXHAUSTION` during the action.

Damage settlement occurs later in `BloodlineNoble.onDealDamage(...)`: damage provenance determines exhaustion/Weakness, Vampirism blood gain and optional healing. Black Arcana must not add a second lifesteal or blood settlement for the same hit.

## Noble Invisibility — `bloodlines:noble_invisibility_action`

This subclasses Vampirism `InvisibilityVampireAction` rather than duplicating the mechanic.

- when the base Vampirism `VAMPIRE_INVISIBILITY` skill is enabled, Noble's separate action is hidden and `canBeUsedBy` returns false;
- when both the Noble skill and Vampirism invisibility skill are present, Bloodlines modifies the **base** invisibility action through `ActionEvent` hooks;
- combined defaults: cooldown **10 s**, duration **45 s**.

This is an explicit deduplication contract: integrations should treat the two skills as one provider action surface once both are learned.

## Flank — `bloodlines:noble_flank_action`

Default:

- cooldown **15 s**;
- configured max target range **300**;
- blocked while Vampirism Bat is active;
- default sight requirement enabled.

The action raycasts for a LivingEntity and teleports the player behind it only when the provider's visibility condition succeeds. Vampirism `TELEPORT_DISTANCE` refinement can multiply the range. Server players are dismounted before the final teleport.

# Zealot actions

## Shadowwalk — `bloodlines:zealot_shadowwalk_action`

Defaults:

- max light level **6** at origin and destination;
- cooldown by rank: **15 / 8 / 5 / 3 s**;
- blocked while Bat is active.

The implementation uses **Vampirism `vaTeleportMaxDistance`** as the base range, optionally multiplied by Vampirism `TELEPORT_DISTANCE` refinement. Although Bloodlines also defines `zealotShadowwalkmaxDistance=25`, the audited action implementation does not use that config value. Treat that field as a static config/code mismatch until runtime QA.

Destination validation rejects misses, invalid collision/liquid destinations and targets that fail the darkness gate.

## Dark Cloak — `bloodlines:zealot_darkcloak_action`

Defaults:

- max light level **10**;
- cooldown **0 s**;
- configured duration `Integer.MAX_VALUE` seconds, but the implementation clamps before converting to ticks.

With the default value the effective provider timer is clamped to **2,147,483,620 ticks** (`107,374,181 s`) rather than overflowing. Every 10 ticks the action rechecks light and terminates when the darkness condition no longer holds.

## Wall Climb — `bloodlines:zealot_wall_climb_action`

Defaults:

- cooldown **20 s**;
- duration **15 s**;
- vertical climb speed **0.3**.

While active, the implementation changes Y velocity only on the **client side** when horizontal collision is detected; crouching sets the climb speed to zero and fall distance is cleared. Because movement authority is client-sensitive here, dedicated-server/movement-mod QA is mandatory before Black Arcana depends on the result.

## Frenzy — `bloodlines:zealot_frenzy_action`

Defaults:

- cooldown **60 s**;
- duration **15 s**;
- rank `BLOCK_BREAK_SPEED` modifier (`ADD_MULTIPLIED_TOTAL`): **0.10 / 0.15 / 0.20 / 0.25**.

The modifier is removed on deactivation and restored on reactivation.

# Ectotherm actions

## Lord of Frost — `bloodlines:ectotherm_frostlord_action`

Defaults:

- cooldown **15 s**;
- duration by rank: **15 / 30 / 60 / 120 s**;
- Lord-of-Frost-duration skill multiplier: **2×**;
- increased attack-damage gate: rank **3** by default;
- attack-damage multipliers by rank config: **1.25 / 1.35 / 1.50 / 1.75**; implementation applies `value - 1` with `ADD_MULTIPLIED_BASE` after the configured rank gate.

If Ice Lord is enabled, activation toggles `icePhasing`; deactivation clears it. Frozen Attack/Slowness Attack crit hooks are evaluated while this action is active.

## Dolphin Leap — `bloodlines:ectotherm_dolphin_leap_action`

Defaults:

- requires the player to be **in water** at activation;
- cooldown **7 s**;
- duration **5 s**.

The server sends `ClientboundLeapPacket` to perform the leap-side movement. Fall distance is suppressed while active, and Movement Speed II is refreshed periodically. This packet/client movement surface requires runtime QA with other movement providers.

## Ink Splash — `bloodlines:ectotherm_ink_splash_action`

Defaults:

- requires water;
- cooldown **60 s**;
- Blindness duration **150 ticks**.

The action builds an AABB from the player's block position and inflates it by 3 blocks on each axis, then applies Blindness to every other `LivingEntity` returned in that volume. No ally/faction filter is present in the audited method.

# Bloodknight actions

## Crimson Leap — `bloodlines:bloodknight_crimson_leap_action`

Defaults:

- cooldown **20 ticks**;
- duration **50 ticks**;
- activation cost **8 Vampirism blood**;
- blocked while Bat is active.

Unlike most Bloodlines action configs, Crimson Leap's cooldown/duration values are already defined and returned in **ticks**. The gate requires `blood - cost > 0`; the player cannot spend to zero. Movement is delegated by server packet to the client and fall distance is suppressed during the duration.

## Sanguine Infusion — `bloodlines:bloodknight_sanguine_infusion_action`

Defaults:

- cooldown **30 s**;
- duration **3000 s**;
- initial cost **3 blood**;
- upkeep interval **160 ticks**;
- actual upkeep debit **2 blood per interval**;
- movement speed `+0.75 ADD_MULTIPLIED_TOTAL`;
- jump strength `+0.25 ADD_MULTIPLIED_TOTAL`;
- Safe Fall Distance +5;
- optional Step Height +0.75 or Mining Efficiency +0.20 according to the sibling infusion skill.

Static mismatch: the config comment says the interval is time for **1 blood** to be used, but the implementation calls `useBlood(2, true)`. The code is source authority for observed settlement; do not silently rewrite the config description.

## Blood Hunt — `bloodlines:bloodknight_blood_hunt_action`

Defaults:

- cooldown **30 s**;
- duration **3000 s**;
- initial cost **3 blood**;
- upkeep interval **140 ticks**;
- actual upkeep debit **2 blood per interval**.

The action makes the player invisible. Hidden Strike is causally tied to Blood Hunt elsewhere: a qualifying crouched vanilla critical can apply Weakness/Slowness and forcibly deactivate Blood Hunt.

The same config-description mismatch exists: the comment describes one blood per interval while implementation debits two.

## Daywalker — `bloodlines:bloodknight_day_walker_action`

Defaults:

- cooldown **300 s**;
- duration **180 s**;
- initial cost **5 blood**;
- upkeep interval **45 ticks**;
- actual upkeep debit **2 blood per interval**.

The action sets the Bloodlines daywalker flag and refreshes Vampirism Sunscreen for 22 ticks at amplifier 1 every 20 ticks. Deactivation clears the flag and removes Sunscreen.

## Blood Extraction — `bloodlines:bloodknight_blood_extraction_action`

Default cooldown: **900 s**.

Activation requires:

- Glass Bottle in offhand;
- targeted entity is a `VampirismEntity`;
- target is vampire;
- ExtendedCreature state exists;
- target can currently be bitten.

On success:

1. consume one Glass Bottle;
2. subtract **3** from the target ExtendedCreature blood state;
3. add one Vampirism Vampire Blood Bottle to the player.

This is a provider-native target-resource → item conversion and must not be mirrored as an extra Black Arcana reward.

# Gravebound actions

## Shared Soul-action settlement

For `GraveboundSoulAction` subclasses:

- required Souls are checked against persistent Gravebound state;
- `souls - cost <= 0` rejects activation;
- successful debit uses `State.addSouls(-cost)` and syncs `BloodlineManager`;
- Creative skips the debit, but the availability gate is still evaluated first.

## Devour Soul — `bloodlines:gravebound_devour_soul_action`

Cooldown by rank: **75 / 60 / 40 / 20 s**.

No Soul cost. Target eligibility remains `BloodlineGravebound.canDevour(...)`, including EntitySoulData, health threshold, distance and player-alive-time gates.

Static settlement finding: for any targeted `LivingEntity` while the manager is Gravebound, the action returns `true` even when `canDevour(...)` is false. Therefore an invalid living target may still be reported as successful to the action handler and consume cooldown. Runtime-test before attaching any completion-sensitive Black Arcana trigger.

## Soul Infusion — `bloodlines:gravebound_soul_infusion_action`

Defaults:

- cost **4 Souls**;
- cooldown **30 s**;
- duration **10 s**;
- immediate heal **5 health**.

Regeneration II and Resistance I are applied for 25 ticks and refreshed every 20 ticks while the action lasts.

## Lingering Devour — `bloodlines:gravebound_lingering_devour`

Defaults:

- cost **2 Souls**;
- cooldown **250 s**;
- entity duration **30 s**;
- initial radius **4.5**;
- radius growth trends toward **8.0** across the duration;
- Poison II effect entry, 50 ticks.

Requires a target block. The provider creates and owns `LingeringDevourEntity`; downstream soul/death settlement must follow that entity's own logic rather than a generic AoE-kill approximation.

## Soul Claiming — `bloodlines:gravebound_soul_claiming`

Defaults:

- cooldown **3000 s**;
- duration **20 s**;
- no activation Soul cost.

While active, qualifying kills by the Gravebound are passed through `canDevour(..., ignoreDistance=true, ignoreDead=true)` and then `devour(..., applyDamage=false)`. Damage already tagged as `DEVOUR_SOUL` is excluded to prevent recursive claiming.

When Passive Soul Claiming is enabled, the same death hook remains active permanently and the selectable action is hidden.

## Sorcerous Strike — `bloodlines:gravebound_crit_action`

Defaults:

- cooldown **90 s**;
- action window **10 s**;
- additional vanilla-critical damage multiplier **+1.25**.

The next qualifying vanilla critical consumes `critStrikeActive` and applies Wither.

Two static blockers are recorded:

1. the skill/action has registry/node/config entries but the node is absent from the configured Gravebound tree and from rank-default lists; survival reachability is unproven;
2. config defines `sorcerousStrikeWitherDuration=8 s`, but the hit implementation uses `sorcerousStrikeDuration` instead, producing **10 s** Wither with defaults. The specific Wither-duration config appears unused in the audited source.

## Mist Form — `bloodlines:gravebound_mist_form_action`

Mist Form is not a normal manual survival action. From configured immortality rank **3**, Bloodlines force-enables its skill, and the lethal-damage hook sets the state and toggles the action when resurrection conditions pass.

Defaults:

- duration **20 s**;
- cooldown **90 s**, or **30 s** with Faster Resurrection;
- required Souls by rank: **15 / 12 / 8 / 5**;
- reduced-cost array with Cheaper Resurrection: **10 / 8 / 6 / 3**;
- flight speed **0.015**.

While active:

- Armor `-1 ADD_MULTIPLIED_TOTAL`;
- Armor Toughness `-1 ADD_MULTIPLIED_TOTAL`;
- Max Health `-0.15 ADD_MULTIPLIED_TOTAL`;
- NeoForge Creative Flight +1;
- forced crouching-sized mist dimensions.

On deactivation the state pays the resurrection Soul cost only when `state.getSouls() > requiredSouls`. Having **exactly** the configured cost is insufficient and falls into the death path. This strict reserve-one behavior must be preserved unless the provider itself is patched intentionally.

## End Mist Form — `bloodlines:gravebound_end_mist_form_action`

Visible/usable only during Mist Form. Cooldown is **20 ticks**.

Activation intentionally clears cached Mist Form and reapplies the stored killing damage source for 1000 damage, or kills the player directly if no source is present. This is a voluntary death/abort action, not a free exit.

## Phylactery Teleport — `bloodlines:gravebound_phylactery_teleport_action`

Defaults:

- regular cost **4 Souls**;
- Mist Form cost **6 Souls**;
- cooldown **300 s**.

Requires a bound Phylactery, the player to be in the **same dimension** as the stored Phylactery, and a provider-approved safe dismount/location search. Souls are consumed only after a valid destination is found and teleport succeeds.

## Ghost Walk — `bloodlines:gravebound_ghost_walk_action`

Defaults:

- cost **6 Souls**;
- cooldown **400 s**;
- duration **20 s**.

The action toggles the synchronized Gravebound `ghostWalk` cache. Collision/phasing implementation elsewhere must remain the provider authority; the `ghostwalk_blacklist` includes Obsidian, Crying Obsidian, Bedrock, Barrier, End Stone, End Portal Frame and air-tag entries.

## Phylactery Soul Transfer — `bloodlines:gravebound_phylactery_soul_transfer_action`

Default cooldown **30 s**. Transfer quantum is hardcoded **5 Souls**.

The action:

1. requires a bound/resolvable Phylactery;
2. removes up to 5 Souls from Phylactery storage;
3. adds as many as fit into the player's current Soul cap;
4. returns unused transfer capacity to the Phylactery;
5. updates cache and syncs state.

This is a transfer, not Soul creation.

## Possession — `bloodlines:gravebound_possession_action`

Defaults:

- cost **3 Souls**;
- cooldown **120 s**;
- duration **100 s**.

Target must be alive and belong to `bloodlines:possession_whitelist`.

Audited whitelist (14 vanilla types):

- Zombie;
- Husk;
- Drowned;
- Skeleton;
- Bogged;
- Silverfish;
- Wither Skeleton;
- Villager;
- Zombie Villager;
- Creeper;
- Wolf;
- Enderman;
- Phantom;
- Stray.

On server the player's camera is moved to the possessed target. Bloodlines then routes possession-specific movement and interaction packets, including melee/ranged attacks, Creeper ignition and block interaction. No modded entity is implicitly supported merely because it resembles a whitelisted mob.

Logout/entity-leave/death hooks clear possession state to avoid stale ownership.

## Possession Swap — `bloodlines:gravebound_possession_swap_action`

Defaults:

- cost **2 Souls**;
- cooldown **20 s**.

Only available while a possessed entity reference exists. It swaps the player and possessed entity positions and then consumes Souls. It does not itself terminate Possession.

# Cross-action static findings

1. **29/29 registry entries are closed in source.**
2. **Action timers use mixed units.** Most config values are seconds and classes multiply by 20, while Crimson Leap and End Mist Form use raw ticks. Never normalize by field name alone.
3. **Bloodknight long-duration defaults are really seconds.** Sanguine Infusion and Blood Hunt default to 3000 s because their getters multiply config values by 20.
4. **Bloodknight periodic descriptions disagree with code.** Three upkeep actions debit 2 blood, not the 1 implied by their config comments.
5. **Shadowwalk own distance config is not used by the audited action implementation.**
6. **Sorcerous Strike specific Wither duration config is not used by the hit hook.**
7. **Sorcerous Strike survival reachability is unproven.**
8. **Devour Soul can report success without devouring.** Completion-sensitive consumers must not use action activation alone as proof of Soul acquisition.
9. **Mist Form has strict reserve-one semantics.** Exact-cost Souls do not satisfy the deactivation resurrection branch.
10. **Possession support is whitelist-driven and vanilla-only by default.**
11. **Movement-heavy actions require dedicated-server QA:** Wall Climb, Dolphin Leap, Crimson Leap, teleport, Ghost Walk, Mist Form flight and Possession.

# Black Arcana integration contract for actions

Black Arcana may:

- observe Vampirism `ActionEvent` where appropriate;
- read the provider action handler and Bloodline state;
- gate Black Arcana content on canonical action/skill/rank state;
- add completion-sensitive rewards only from a causal event that proves provider settlement.

Black Arcana must not:

- start a parallel cooldown/duration timer for a Bloodlines action;
- charge Vampirism blood or Gravebound Souls a second time;
- infer action success from button press/activation when the provider can later reject or settle conditionally;
- bypass Bloodline/skill/rank/Phylactery/Soul gates;
- broaden Possession to arbitrary entities without an explicit compatibility decision;
- reinterpret ticks as seconds or vice versa without reading the exact action implementation;
- compensate for the static mismatches above silently.

# Runtime QA gates

Before marking action runtime QA confirmed, test at minimum:

- all 29 registry entries instantiate and appear under the expected skill/bloodline gates;
- cooldown and duration persistence/sync across reconnect;
- each mixed-unit timer against actual ticks;
- Shadowwalk, Flank and Phylactery Teleport failure/success cooldown behavior;
- Wall Climb/Dolphin Leap/Crimson Leap under dedicated server and movement mods;
- Bloodknight initial/upkeep blood debits exactly once;
- Devour invalid-target cooldown behavior;
- Sorcerous Strike reachability and 8-vs-10-second Wither discrepancy;
- Mist Form exact-cost vs greater-than-cost behavior, logout kill, vulnerable damage and cooldown reduction;
- Phylactery transfer conservation;
- Possession whitelist, packet authority, logout/death cleanup and Possession Swap;
- passive Soul Claiming deduplication with Devour/Soul Claiming damage.
