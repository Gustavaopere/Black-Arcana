# Weapons of Miracles 2.0.178 — exact skill disposition

Status: `64/64 EXACT-CURRENT SKILL IDS DISPOSITIONED`

The exact physical/publisher-matched `WOMSkills` registrar contains **64 unique skill IDs**. This table classifies every ID against the Black Arcana semantic-magic rule.

`COUNTED_EXACT` means the supernatural action identity and catalog-level current reachability are closed. `CONDITIONAL` means the identity exists but current normal reachability remains open. `EXCLUDED` means the skill exists but is outside the semantic-magic metric by definition.

| # | WOM skill ID | Provider category | State | Semantic disposition |
|---:|---|---|---|---|
| 1 | `wom:ender_step` | Dodge | `COUNTED_EXACT` | provider teleport/evasion action; deliberate active supernatural movement |
| 2 | `wom:ender_obscuris` | Dodge | `COUNTED_EXACT` | deliberate teleport behind the last valid target |
| 3 | `wom:shadow_step` | Dodge | `COUNTED_EXACT` | deliberate shadow-state movement action |
| 4 | `wom:precise_roll` | Dodge | `EXCLUDED` | enhanced ordinary roll/evasion |
| 5 | `wom:dodge_master` | Dodge | `EXCLUDED` | enhanced/automatic dodge window; combat technique rather than supernatural identity |
| 6 | `wom:bull_charge` | Dodge | `EXCLUDED` | physical forward charge/push technique |
| 7 | `wom:time_travel` | Dodge | `COUNTED_EXACT` | deliberate temporal position/health registration and return-style action |
| 8 | `wom:punishment_kick` | Dodge | `EXCLUDED` | martial kick/stun technique |
| 9 | `wom:counter_attack` | Guard | `EXCLUDED` | guard/parry counter technique |
| 10 | `wom:vengeful_parry` | Guard | `EXCLUDED` | timed guarding stance |
| 11 | `wom:perfect_bulwark` | Guard | `EXCLUDED` | omnidirectional guard behavior |
| 12 | `wom:soul_protection` | Guard | `EXCLUDED` | reactive TAKE_DAMAGE_PRE protection/charge behavior; no independent cast root |
| 13 | `wom:shulker_cloak` | Guard | `EXCLUDED` | reactive TAKE_DAMAGE_PRE defensive charge behavior; no independent cast root |
| 14 | `wom:buster_parade` | Guard | `EXCLUDED` | weapon windup/guard-break combat technique |
| 15 | `wom:arrow_tenacity` | Passive | `EXCLUDED` | permanent projectile-stun passive |
| 16 | `wom:pain_anticipation` | Passive | `EXCLUDED` | automatic delayed combat trigger |
| 17 | `wom:latent_retribution` | Passive | `EXCLUDED` | automatic delayed combat trigger |
| 18 | `wom:vampirize` | Passive | `EXCLUDED` | damage-linked healing passive |
| 19 | `wom:critical_knowledge` | Passive | `EXCLUDED` | critical-damage chance passive |
| 20 | `wom:heart_shield` | Passive | `EXCLUDED` | recovering shield passive |
| 21 | `wom:mindset` | Passive | `EXCLUDED` | health-threshold passive |
| 22 | `wom:adrenaline` | Passive | `EXCLUDED` | health-threshold passive |
| 23 | `wom:dancing_blade` | Passive | `EXCLUDED` | passive combat modifier/trigger |
| 24 | `wom:meditation` | Passive | `EXCLUDED` | provider PassiveSkill despite deliberate crouch setup |
| 25 | `wom:inner_growth` | Passive | `EXCLUDED` | automatic innate-power regeneration |
| 26 | `wom:dopamine` | Passive | `EXCLUDED` | dash-damage to stamina conversion passive |
| 27 | `wom:manipulator` | Passive | `EXCLUDED` | block-timing stamina passive |
| 28 | `wom:lethal_focus` | Passive | `EXCLUDED` | stacking damage passive |
| 29 | `wom:spider_techniques` | Mover | `EXCLUDED` | wall-running locomotion helper |
| 30 | `wom:aqua_maneuvre` | Mover | `EXCLUDED` | swimming locomotion helper |
| 31 | `wom:natural_sprinter` | Mover | `EXCLUDED` | running locomotion helper |
| 32 | `wom:lunatic_vivacity` | Identity | `EXCLUDED` | combat phase-cycling identity; no distinct supernatural action established |
| 33 | `wom:voodoo_magic` | Identity | `COUNTED_EXACT` | deliberate player-driven health↔stamina conversion |
| 34 | `wom:back_and_forth` | Identity | `EXCLUDED` | distance-conditioned combat/stun behavior |
| 35 | `wom:shooting_style` | Identity | `EXCLUDED` | empty-hand kick fighting style |
| 36 | `wom:proximity_exploiter` | Identity | `EXCLUDED` | automatic nearby-entity innate-power regeneration |
| 37 | `wom:all_eyes_on_you` | Identity | `EXCLUDED` | automatic block/dodge trigger state |
| 38 | `wom:all_eyes_on_me` | Identity | `EXCLUDED` | automatic multi-attack trigger state |
| 39 | `wom:avatar_of_might` | Identity | `COUNTED_EXACT` | deliberate charged shockwave plus temporary stun immunity |
| 40 | `wom:charybdis` | Weapon Innate | `EXCLUDED` | stamina-fed multi-hit whirlwind combat technique |
| 41 | `wom:agony_plunge` | Weapon Innate | `COUNTED_EXACT` | Sky Dive relocates/levitates through a deliberate supernatural dive sequence |
| 42 | `wom:true_berserk` | Weapon Innate | `COUNTED_EXACT` | deliberate supernatural wrath/transformation-style weapon state |
| 43 | `wom:demonic_ascension` | Weapon Innate | `COUNTED_EXACT` | deliberate demonic possession/ascension state with teleport/effect lifecycle |
| 44 | `wom:plunder_perdition` | Weapon Innate | `COUNTED_EXACT` | provider-presented Ender Ritual / ancient Ender arcane action |
| 45 | `wom:regierung` | Weapon Innate | `EXCLUDED` | context-dependent weapon guard/attack combo; no separate supernatural identity established |
| 46 | `wom:sakura_state` | Weapon Innate | `EXCLUDED` | weapon combat state/technique; no separate supernatural identity established |
| 47 | `wom:ender_blast` | Weapon Innate | `EXCLUDED` | provider explicitly presents it as End technological weapon power |
| 48 | `wom:ender_fusion` | Weapon Innate | `EXCLUDED` | provider explicitly presents it as End technological weapon power |
| 49 | `wom:lunar_eclipse` | Weapon Innate | `COUNTED_EXACT` | deliberate lunar supernatural state/effect action |
| 50 | `wom:solar_arcano` | Weapon Innate | `COUNTED_EXACT` | deliberate stellar/solar supernatural action |
| 51 | `wom:rechargement` | Weapon Innate | `EXCLUDED` | weapon reload/recharge operation |
| 52 | `wom:orbital_beam` | Weapon Innate | `EXCLUDED` | technological orbital strike rather than supernatural magic |
| 53 | `wom:flash_mutilation` | Weapon Innate | `CONDITIONAL` | teleport-around-target supernatural action; exact owner exists but normal current acquisition is not closed |
| 54 | `wom:unbreakable` | Weapon Innate | `EXCLUDED` | active defensive weapon state with stun/damage handling; no separate supernatural/arcane identity established |
| 55 | `wom:satsujin_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 56 | `wom:demon_mark_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 57 | `wom:ruine_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 58 | `wom:herrscher_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 59 | `wom:torment_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 60 | `wom:lunar_echo_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 61 | `wom:solar_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 62 | `wom:napoleon_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 63 | `wom:evil_tachi_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |
| 64 | `wom:unbreakable_passive` | Weapon Passive | `EXCLUDED` | weapon-passive support |

## Accounting

- exact registry IDs: **64**;
- `COUNTED_EXACT`: **12**;
- `CONDITIONAL`: **1**;
- `EXCLUDED`: **51**;
- supernatural semantic roots: **13**;
- strict semantic contribution: **+12**.

Category membership is a provider fact; semantic disposition is the catalog classification. A magical-looking name alone is insufficient: reactive/passive/technical behavior remains excluded unless it is a discrete player-owned supernatural action.
