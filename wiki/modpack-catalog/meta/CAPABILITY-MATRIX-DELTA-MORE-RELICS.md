# Capability Matrix — More Relics 1.7.7 delta

Data: `2026-09-07`

This file is a narrow semantic overlay over `../CAPABILITY-MATRIX.md`. It prevails only for capability families explicitly named below until the next integral matrix regeneration.

Evidence level: exact installed artifact + exact official 1.7.7 publisher release + current publisher content/loot list + recent release changelogs. No official exact source pin was located; provider-specific internals remain unavailable.

## Relic/equipment powers

Add More Relics as **strong equipment-based capability coverage** through the Relics host framework.

Current publisher description lists 29 named relics and says the addon contains `25+` high-quality relics, including evolved forms.

This substantially reduces novelty space for generic “magic accessory grants one special passive/active power” concepts.

Black Arcana artifact concepts remain legitimate only where their mechanic is materially distinct and depends on Black Arcana-owned contracts rather than simply duplicating an existing relic effect in another item.

## Relic evolution

Public evolution chains include:

- Tyrant Mask → King Crimson;
- Slumbering Amulet → Whispering Amulet → Made in Heaven;
- Depleted Spool → Weavers Spool;
- Converging Orb → Wonder of U.

Effective coverage:

`PROVIDER-NATIVE ITEM EVOLUTION / RELICS-HOSTED`

Do not recreate a generic “level accessory until it evolves into stronger named accessory” subsystem inside Black Arcana/RPG solely for More Relics-like content.

## Health-threshold / conditional item behavior

Exact 1.7.7 publisher changelog makes **Eject Button** health threshold configurable.

This establishes current equipment coverage for health-threshold-triggered behavior. Exact ability output/formula is not promoted beyond publisher evidence.

## Vulnerability / target debuff item behavior

Exact 1.7.7 changelog makes **Bionic Eye** Vulnerability levels configurable.

This occupies item-driven Vulnerability/debuff territory. It does not transfer authority to Black Arcana Corruption/Strain and does not imply a generic debuff API.

## Multi-hit / repeated-hit equipment behavior

Exact 1.7.7 changelog records a fix intended to stop **Twin Fangs** from hitting infinitely under some conditions.

Deduplication consequence:

Any Black Arcana combat observer must not amplify or replay provider repeated-hit settlement. If a provider attack emits multiple legitimate damage events, progression/hazard logic needs its own exactly-once/causal policy rather than assuming every damage callback is a distinct player-authored action.

## Damage-boost cooldown behavior

More Relics 1.7.6 documents a **Mass Gauntlet** damage-boost cooldown, with a publisher-stated default of 0.2 seconds at that checkpoint and common-config configurability.

Black Arcana does not add a second cooldown or infer exact current 1.7.7 value unless separately verified.

## Status/mood behavior

Exact 1.7.7 documents **Moodworm** status indication, configurable mood-change duration and a balance/stat correction.

This is provider-owned item/status state, not RPG Mastery or Black Arcana Strain.

## Client-side indicator/UI overlap

More Relics 1.7.6+ renders selected statuses/effects as icons above the food bar; 1.7.7 allows individual icon disabling.

This is presentation coverage only.

Matrix consequence:

`CLIENT INDICATOR != GAMEPLAY AUTHORITY`

No Black Arcana/RPG event may be driven from the icon surface.

## Loot-distribution overlap

The current publisher page maps relics into:

- Bastions/Nether;
- Buried Treasure;
- Sculk/Ancient City/Deep Dark;
- Mineshafts;
- Mountains;
- Swamps;
- Deserts;
- Caves;
- Taiga;
- End;
- Strongholds;
- Woodland Mansions;
- Pillager Outposts;
- dungeons;
- low-chance broad loot pools.

This is substantial exploration/equipment reward coverage. Black Arcana reward design must consider economic duplication, but these provider loot tables do not become Black Arcana progression authority.

## Current host incompatibility gate

This capability delta has a hard operational qualifier.

Current pack:

- More Relics `1.7.7`;
- Relics `0.12.8` Beta.

Publisher More Relics notice:

- NeoForge Relics `0.11` and `0.12` are not supported;
- use Relics `0.10.7.8` for 1.21.1;
- exact 1.7.7 says a future mini-beta may target `0.12.8`.

Therefore all More-Relics-specific current capability claims are useful for **semantic deduplication**, but not for approving a runtime bridge.

Effective integration state:

`UPSTREAM-UNSUPPORTED CURRENT HOST COMBINATION / PROVIDER-SPECIFIC FAIL-CLOSED`

## Progression boundary

Relics remains authority of the host relic progression/data/evolution framework. More Relics supplies addon content.

RPG Skill Tree must not treat Relics XP/evolution as its own state. It may only react through a real causal/provider contract with deduplication.

No Mastery for:

- item merely equipped;
- passive effect uptime;
- client icon visible;
- relic XP ticking under provider rules;
- repeated equip/unequip spam.

## Black Arcana overlap decision

More Relics materially occupies:

- special magical accessories;
- active/passive item abilities;
- conditional health behavior;
- target debuff item mechanics;
- repeated-hit and damage-boost item behavior;
- evolved accessory chains;
- specialized exploration loot.

It does **not** occupy Black Arcana's:

- server-authoritative casting transaction;
- dangerous transactional resource costs;
- Arcane Danger/Resistance/Corruption/Strain/Backlash;
- bounded ritual world effects;
- Mortal Ledger/Soul Anchor semantics;
- spell-domain field authority.

No Phase 3 row is unblocked from More Relics by this delta. Current provider-specific integration remains `BLOCKED / FAIL-CLOSED` until the unsupported Relics 0.12.8 pairing is resolved by real QA/provider support.