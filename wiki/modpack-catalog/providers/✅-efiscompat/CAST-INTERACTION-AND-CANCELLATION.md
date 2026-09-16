# `efiscompat` 3.1.0 — cast interaction and cancellation

This document records the server-relevant interaction seams observed at exact source revision `domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4`.

It is a factual provider inventory. It is **not** permission to reproduce these mixins in Black Arcana.

## Authority model

The compat does not construct a separate spell state machine. It queries and mutates the existing Iron's casting lifecycle through Iron's own API/events:

- `MagicData.getPlayerMagicData(...)` for server-side cast state;
- `SpellPreCastEvent` / `SpellOnCastEvent` for cast lifecycle observation;
- `Utils.serverSideCancelCast(...)` for cancellation;
- `AbstractSpell.onServerCastComplete(...)` / Iron's `CancelCastPacket.cancelCast(...)` as presentation cleanup seams.

Therefore:

- Iron's owns the cast, spell, mana and cooldown semantics;
- Epic Fight owns combat/action/stun/animation state;
- `efiscompat` owns only the reconciliation policy between those states;
- Black Arcana owns none of those provider internals and must not double-process them.

## Pre-cast gate

`PlayerAnimationEvents.beforeSpellCast(SpellPreCastEvent)` is server-player-only.

Before animation selection, it gets the Epic Fight `ServerPlayerPatch` and evaluates a provider-local `canCastSpell(...)` condition. The event is canceled when either condition is true:

1. Epic Fight reports the player stunned; or
2. `tickSinceLastAction <= currentItemAttackStrengthDelay * castingDelay`.

`castingDelay` is provider config with default `0.0`. The source comment describes the value as a fraction of the current main-weapon attack delay.

### Boundary

This is an Iron's pre-cast veto driven by Epic Fight state. It is not a Black Arcana global casting rule. Black Arcana must not import this formula automatically for BA-native spells.

If BA later needs Epic Fight-aware cast gating, the rule must be designed as a BA adapter contract against the physical Epic Fight version and enter the single BA server-authoritative cast pipeline before cost commit/effect execution according to BA's own transactional invariants.

## Skill execution cancellation

`MixinSkillExecution` targets Epic Fight `SkillContainer.requestCasting`.

When the executor is a server player and Iron's `MagicData.isCasting()` is true:

- it calls `Utils.serverSideCancelCast(serverPlayer, true)`;
- it deliberately does **not** cancel the Epic Fight skill request.

The resulting policy is: **skill wins; Iron's cast is canceled first**.

The upstream comment mentions Epic Fight Nightfall skills as examples. That comment is not treated as a separate provider contract.

## Guard cancellation

`MixinGuard` injects after Epic Fight `GuardSkill.isExecutableState`.

Only when Epic Fight already returned executable and execution is server-side does the compat inspect Iron's cast state. If casting, it calls:

`serverSideCancelCast(player, castCancelCooldown || castType == CONTINUOUS)`.

Consequences at source level:

- guard is not made executable by the compat;
- successful guard eligibility can interrupt an Iron's cast;
- the cancellation cooldown flag follows provider config, except continuous casts force the flag true.

The precise meaning/duration of Iron's cancellation cooldown remains Iron's authority.

## Dodge cancellation

`MixinDodge` follows the same return-point structure on `DodgeSkill.isExecutableState` with one extra provider gate:

- cancellation occurs only when `EnableDodgeCancelling` is true;
- default is `true`;
- cooldown flag is `castCancelCooldown || castType == CONTINUOUS`.

Again, the compat does not own dodge eligibility or the Iron's cooldown implementation.

## Generic Epic Fight skill cancellation

The `SkillContainer.requestCasting` mixin is broader than the dedicated guard/dodge hooks. Any Epic Fight skill reaching that request path while the player is casting can trigger `serverSideCancelCast(..., true)` before the skill continues.

Catalog consequence: future BA/Epic Fight integration must test event/skill ordering rather than assuming only dodge and guard can interrupt an Iron's cast.

## `ComboBasicAttack` special case

`MixinComboBasicAttack` targets the string class name:

`com.p1nero.invincible.skill.ComboBasicAttack`

and injects at `isExecutableState` HEAD. If the server-side player is casting in Iron's, it sets the attack result to `false`.

This differs from the other skill hooks:

- it blocks that attack instead of canceling the spell;
- the target class belongs to another compatibility surface, not Iron's or core Epic Fight by namespace;
- exact `neoforge.mods.toml` does not declare a dependency for that target namespace.

The current physical top-level modlist has no entry whose mod id/name directly identifies `invincible` or Nightfall. That does **not** prove the class is absent from every loaded artifact, but it means target availability must not be assumed from the top-level inventory.

### QA disposition

`MixinComboBasicAttack` target resolution is **runtime QA / fail-closed**. No Black Arcana adapter may depend on this target until the physical class owner and target stability are proven.

## Cast completion / cancel animation cleanup

Two common mixins react to Iron's lifecycle seams:

### `MixinCancelAnimation`

Injects at `CancelCastPacket.cancelCast` HEAD and, when an Epic Fight `ServerPlayerPatch` exists:

- synchronizes `OFF_ANIMATION_MIDDLE`;
- synchronizes `OFF_ANIMATION_HIGHEST`;
- refreshes living motion from the current item.

This is animation cleanup around an Iron's-owned cancellation; it does not replace the cancellation itself.

### `MixinOnSpellFinish`

Injects at `AbstractSpell.onServerCastComplete` HEAD.

- LONG casts clear the middle animation layer;
- CONTINUOUS casts clear middle + highest layers.

Again, the Iron's spell completes through Iron's own method; the compat resets Epic Fight animation state.

## Required common mixin inventory

Exact `mixins.epicironcompat.json` common list:

1. `MixinCancelAnimation`
2. `MixinComboBasicAttack`
3. `MixinDodge`
4. `MixinGuard`
5. `MixinOnSpellFinish`
6. `MixinSkillExecution`

The mixin config has `required: true` and injector `defaultRequire: 1`.

Catalog closure records this exact source behavior but does not assert every target applies successfully in the physical modpack.

## Black Arcana integration disposition

| Surface | Provider owner | Black Arcana disposition |
|---|---|---|
| Iron's `SpellPreCastEvent` veto | Iron's event + `efiscompat` policy | do not reuse as BA global gate |
| Epic Fight stunned/recent-action state | Epic Fight | future adapter may query only through verified boundary |
| Iron's server cast cancellation | Iron's | never duplicate or cancel twice |
| guard/dodge/skill interruption policy | `efiscompat` for Iron's↔Epic Fight | provider-native first; BA does not shadow it |
| Iron's cancellation cooldown | Iron's | no second cooldown ledger |
| BA-native cast acceptance | Black Arcana | remains canonical BA pipeline |
| BA cost commit/replay safety | Black Arcana | unchanged |
| BA targeting/effects/world policy | Black Arcana | unchanged |
| RPG progression | RPG Skill Tree through real contracts only | no authority derived from this compat |

## Anti-double-processing rule

For Iron's-origin casts, `efiscompat` already owns the Epic Fight interruption reconciliation represented above. A Black Arcana observer must not independently cancel the same Iron's cast or reapply a cooldown just because it observes the same dodge/guard/skill action.

For BA-native casts, no behavior is inherited implicitly. Any future Epic Fight bridge must have explicit provenance, one canonical cancellation decision, and deterministic ordering relative to BA cost reservation/commit and effect execution.