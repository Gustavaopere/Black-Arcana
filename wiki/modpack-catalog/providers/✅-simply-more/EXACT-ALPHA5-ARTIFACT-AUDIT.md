# Simply More 1.3.0 Alpha 5 — exact artifact semantic audit

## Purpose

Close the complete current-pack **player-invoked supernatural action denominator** for physical Simply More Alpha 5 without treating All Rights Reserved implementation as reusable source material.

This audit separates:

1. exact physical/publisher identity;
2. exact current artifact action-surface structure;
3. semantic classification/deduplication;
4. deployed acquisition/Awakening/config reachability.

The first three are closed here. Deployed reachability remains separate and keeps the provider ⚠️ / +0 strict.

## Artifact identity

- physical row: #502;
- physical JAR: `simplymore-forge-1.3.0_alpha.jar`;
- mod id: `simplymore`;
- runtime: `1.3.0_alpha`;
- physical SHA-1: `51636477cd5c378f42d9700e1fe35cd952c8f4f1`;
- publisher CurseForge File: `8736778`;
- publisher file name: `simplymore-neoforge-1.3.0_alpha5+1.21.1.jar`;
- current sibling checkpoint used for pack-presence classification: `neoforge-rpg-skilltree@8aa9b92197c2a6eed5b67b16fa6b6a4adb88fd35`;
- NON-MERGE exact audit PR: #446;
- final audit HEAD: `53155432f050554cd2dec4e5bd1125c1cffaf72f`;
- exact audit run: `36516484341` — GREEN;
- audit artifact: `11011476182`;
- audit artifact digest: `sha256:e2d668d43f80663370e6ddcf03feab090e8de432e70ab13a5cfbb329cfeab859`.

The audit downloads the exact Curse Maven artifact for File `8736778` and fails before inspection unless SHA-1 equals the physical pack digest.

## Clean-room scope

Simply More is All Rights Reserved.

The audit retains only factual interoperability/catalog evidence:

- cryptographic digest and mod metadata;
- class/resource identities;
- superclass/interface relationships;
- bounded method names/signatures;
- bounded invocation targets for selected action methods;
- ItemRegistry class references and direct registered IDs;
- localization keys, never localization prose;
- packet-class identities needed to exclude hidden input surfaces.

It does not retain or publish the upstream JAR, full disassembly, reconstructed source, protected assets or implementation bodies.

## Exact action-surface closure

### New Simply Swords active API — 10 actions

The exact artifact has **11** concrete Unique classes implementing `UniqueWeaponActiveAbility`.

Exactly **10** of them declare a provider `activate(...)` implementation:

1. Black Pearl;
2. Blade of the Grotesque;
3. Grandfrost;
4. Lustrous Moxie;
5. Magmaseep;
6. Moundshifter;
7. Ruyi Jingu Bang;
8. Soulfracture;
9. Stasis;
10. The Blood Harvester.

The eleventh class is `IdolItem` / Ruptured Idol. It declares **no** player-action method. The exact release-line Simply Swords interface defaults its activation fallback to false when the item provides no implementation, so interface membership alone does not mint a semantic action.

Result: **10** current player-action roots from the new active API surface.

### Legacy direct-use uniques — 13 actions

The exact artifact contains **13** concrete non-active-interface Unique classes that each declare their own `use(...)` player surface and are referenced by the exact ItemRegistry:

1. Boa's Fang;
2. Culterex;
3. Death's Eyrie;
4. Glimmerstep;
5. Great Slither;
6. Matterbane;
7. Myrmedge;
8. Perforiscus;
9. Revvengine;
10. Serpentine Valour;
11. Smouldering Ruin;
12. The Vessel Breach;
13. Tidebreaker.

The bounded audit retains only call-target facts needed to prove these are not inert `super.use` placeholders. Their current use paths reach provider effects such as targeting, held-use flow, spawned provider abilities/entities, teleports, combat/effect application and cooldown settlement.

Result: **13** legacy player-action roots.

### Mimicry — one shared action

The exact artifact contains one abstract `MimicryItem` base plus **25** concrete Mimicry forms.

Exact structural facts:

- all 25 concrete forms are referenced by ItemRegistry;
- none of the 25 overrides the inherited player-action methods;
- the abstract base declares `use`, `onUseTick` and `getUseDuration`;
- its exact `use` route calls provider `AttackUtils.holdToUse`.

The forms are therefore presentations/variants of one shared transformation action rather than 25 independent action identities.

Result: **1** Mimicry action root.

## Explicit exclusions

### Ruptured Idol / removed Idol variants

`IdolItem` implements the host active interface but declares no provider action implementation and is excluded.

The four `TO_REMOVE` implementation classes remain present in the JAR:

- Ascended Idol;
- Tarnished Idol;
- Holylight;
- Darksent.

The exact ItemRegistry references **none** of those implementation classes and does reference `RemovedItem` compatibility proxies. They do not add current semantic roots.

### Reforming Remnant

The exact artifact exposes `ReformingRemnantItem.use`, and its only C2S packet is `C2STransformRemnantPacket`.

Release-correlated source shows this path opens a selection screen and converts/initializes a selected weapon result. Under the Black Arcana metric this is an item reformation/upgrade/preparation workflow, not a standalone combat/spell/ritual action.

Result: **+0 semantic roots**.

### Optional Mythic Metals Tidesinger action

The exact artifact contains `TidesingerSwordItem` with a use/release surface and an exact `MythicMetalsCompatRegistry` reference.

Release-correlated source gates that compat registry behind `Platform.isModLoaded("mythicmetals")`. The current physical sibling modlist at `8aa9b92197c2a6eed5b67b16fa6b6a4adb88fd35` contains no Mythic Metals top-level mod.

Therefore Tidesinger is an optional-dependency action surface that is **not present in the current assembled pack denominator**.

### Passive/proc/implicit surfaces

Previously documented passive/on-hit/aura behavior and the four Simply More-owned weapon implicits remain outside the semantic-action metric. Effects, projectiles/entities, HUD state, cooldowns and downstream consequences are not counted separately from their root action.

## Packet/input completeness

The exact artifact contains exactly one provider C2S packet class:

`net/rosemarythyme/simplymore/networking/c2s/C2STransformRemnantPacket`.

It is the Reforming Remnant transformation path already classified above. No separate provider keybind/C2S action family remains outside the item-action inventory.

## Current semantic denominator

| Surface | Count |
|---|---:|
| New active-API player actions | 10 |
| Legacy direct-use player actions | 13 |
| Shared Mimicry transformation | 1 |
| **Current Simply More semantic actions** | **24** |

Evidence state: **exact physical artifact structure + release-correlated semantic classification**.

## Remaining deployed-reachability gate

The complete action denominator is now closed, but strict contribution remains fail-closed.

Before any of the 24 roots enter the strict global minimum, current assembled-pack evidence must close the effective player-reachability surface, including:

- host Simply Swords Awakening/unlock behavior for active-API uniques;
- current provider acquisition/reformation routes for the surviving action-bearing uniques;
- effective Mimicry form-disable configuration where it can change usable transformation outcomes;
- any current-pack config/datapack/script state that suppresses otherwise present actions.

Artifact/source defaults are not substituted for effective deployed state.

## Result

- exact physical/publisher artifact identity: **closed**;
- complete current-pack semantic action denominator: **24**;
- Tidesinger optional Mythic Metals surface: **excluded because Mythic Metals is absent from the current physical modlist**;
- Reforming Remnant: **excluded as upgrade/preparation**;
- Idol/TO_REMOVE surfaces: **excluded as inert/proxy**;
- deployed active/reachability state: **open**;
- strict contribution: **+0**;
- provider status: **⚠️ partial / conditioned**.