# Ignis Soulfires 1.8.0 — semantic action cards

Status: `8/8 EXACT ACTION ROOTS MATERIALIZED`

These cards cover the provider's discrete supernatural player actions under the Black Arcana semantic-magic metric. Numerical values remain provider/config authority and are not frozen here.

## 1. Bulwark Deployment

- owner: `ignissoulfires:bulwark_of_the_soul_flame`;
- class: defensive conjuration / barrier deployment;
- trigger: server-authoritative Bulwark control state + item use outside the shift-charge branch;
- exact seam: `deployBulwark(...)`;
- result: spawns provider `BulwarkOfTheSoulFlameWall` at a valid looked-at placement;
- acquisition: exact shaped crafting/smithing owner routes;
- state: `COUNTED_EXACT`.

Wall wave, item consumption, protection outcomes and blocked attacks are action consequences/state, not extra roots.

## 2. Bulwark Charge

- owner: `ignissoulfires:bulwark_of_the_soul_flame`;
- class: charged mobility/offense;
- trigger: shift-use then release;
- exact seam: `releaseUsing(...)` + `chargeCooldown` + Cataclysm `ChargeAttachment`;
- result: directional player charge with provider-defined settlement;
- state: `COUNTED_EXACT`.

Charge damage/knockback are downstream effects.

## 3. Soul-Fire Chain

- owner: `ignissoulfires:souled_gauntlet_of_bulwark`;
- class: targeted control / pull / soul-fire strike;
- trigger: shift-channel;
- exact seams: `chainCooldown`, `chainRange`, `chainPullSpeed`, `chainHitDamage`, `chainHitKnockback`;
- result: resolves first eligible target along the look path, pulls it toward the user and finishes the terminal hit/effects;
- acquisition: exact `cataclysm:weapon_fusion` owner route;
- state: `COUNTED_EXACT`.

Pull, damage, Stun and Blazing Brand are stages of this one action.

## 4. Gauntlet Charge

- owner: `ignissoulfires:souled_gauntlet_of_bulwark`;
- class: charged mobility/offense;
- trigger: non-shift charged use then release;
- exact seam: distinct `chargeCooldown` branch + Cataclysm `ChargeAttachment`;
- result: forward charge with provider-defined timer/knockback/damage-per-effective-charge state;
- state: `COUNTED_EXACT`.

Attachment hit consequences are not separate actions.

## 5. Soul-Fire Stun Area

- owner: `ignissoulfires:the_souled_immolator`;
- class: area control / soul-fire burst;
- trigger: charged shift release;
- exact seams: provider area cooldown/radius/stun-damage path;
- result: resolves the provider AoE against eligible nearby entities;
- acquisition: exact `cataclysm:weapon_fusion` owner route;
- state: `COUNTED_EXACT`.

Each affected entity, Stun, Blazing Brand, VFX and screen shake remain consequences of the single AoE action.

## 6. Flame Strike

- owner: `ignissoulfires:the_souled_immolator`;
- class: projected soul-fire strike;
- trigger: charged non-shift release;
- exact seam: `spawnFlameStrike(...)` + distinct `strikeCooldown`;
- result: creates the provider forward flame-strike outcome when a valid spawn path exists;
- state: `COUNTED_EXACT`.

Spawned effect entities/particles and downstream hits are part of this action.

## 7. Incinerator Dash

- owner: `ignissoulfires:the_souled_incinerator`;
- class: charged dash / offensive traversal;
- trigger: shift release after the exact 60-tick charge threshold;
- exact seams: `dashCooldown`, `dashDamage`, `dashKnockback` + Cataclysm `ChargeAttachment`;
- result: launches the user forward and settles the dash attack;
- acquisition: exact smithing-transform owner route;
- state: `COUNTED_EXACT`.

Damage, knockback, Stun and Blazing Brand are downstream consequences.

## 8. Incinerator Slam

- owner: `ignissoulfires:the_souled_incinerator`;
- class: ground/forward strike sequence;
- trigger: non-shift release after the exact 60-tick charge threshold;
- exact seams: `useIncineratorSlam(...)`, `spawnStrike(...)`, `slamCooldown`;
- result: resolves the forward strike sequence as one causal slam;
- state: `COUNTED_EXACT`.

Individual spawned strikes are substeps, not independent semantic powers.

## Supporting provider abilities outside the semantic numerator

The exact artifact also exposes thrown-tool operation, tool return, distance breaking/actions, 3×3 Souled tool behavior, prospecting, Tree Cap, tool-mode cycling, passive Souled Blazing Grips behavior, armor effects and horse-armor effects. These remain catalog-relevant gameplay surfaces but are metric-excluded because the global ledger does not turn ordinary tool modes, gear/passives or downstream effects into extra spell-equivalent identities.