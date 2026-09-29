# ShadowsZ 1.1.9 — exact artifact audit

## Purpose

Close the complete current **semantic action inventory** of physical ShadowsZ 1.1.9 without treating All Rights Reserved implementation as reusable source material.

This audit separates three questions:

1. exact physical/publisher identity;
2. complete action/spell denominator;
3. deployed reachability/config state.

Only the first two are closed here. Deployed world/config state remains a separate conditional gate.

## Artifact identity

- physical row: #500;
- physical JAR: `shadowsz-1.1.9.jar`;
- mod id: `shadowsz`;
- runtime: `1.1.9`;
- physical SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- publisher Modrinth version: `Z5VFhs8D`;
- publisher CurseForge file: `8626238`;
- final NON-MERGE audit PR: #443;
- final audit HEAD: `2ea4f054a2cecc487bc27d629824a865a502e4dd`;
- exact audit run: `36430580803` — GREEN;
- audit artifact: `10973381572`;
- audit artifact digest: `sha256:fc7094ce04ef92d420a28fcae4c1c7bb18fa99f77442c59a8a37f1d55925b0d9`.

The publisher artifact downloaded during the audit has SHA-1 `f946eb3a8181e1964279f163f430ccbba6c4edcd`, exactly equal to the physical pack digest.

## Clean-room scope

The publisher artifact is All Rights Reserved.

The audit retains only factual interoperability/catalog evidence:

- cryptographic digest;
- metadata;
- archive/class/resource identities;
- localization **keys**, not localized prose values;
- field/method/constant signatures;
- bounded action-router mappings;
- bounded method call/field sets needed to distinguish semantic roots, aliases and management surfaces;
- exact configuration/gamerule field names and defaults.

The audit does not retain or publish:

- the upstream JAR;
- full disassembly;
- decompiled implementation bodies;
- protected assets;
- localization prose;
- numerical implementation formulas beyond identifying which config field is read.

## Exact spell registry

The exact artifact exposes:

- one ShadowsZ spell deferred registry;
- exactly **3** spell fields;
- exactly **3** registered spell IDs;
- **0** conditional branch instructions in the static registration path.

Exact IDs:

1. `shadowsz:miasma`;
2. `shadowsz:umbral_bond`;
3. `shadowsz:aura_of_the_monarch`.

Exact localization keys independently reconcile the same three roots.

## Exact action routers

`ShadowActionC2S` exposes exactly **20** individual action codes:

- SUMMON;
- DISMISS;
- RENAME;
- BEHAVIOR;
- REMOVE;
- TELEPORT;
- ASSIGN_SLOT;
- TOGGLE_SLOT;
- TOGGLE_EYES;
- ATTACK_TARGET;
- DISMISS_ALL;
- OPEN_STORAGE;
- TOGGLE_PICKUP;
- SUMMON_ALL;
- AGGRO;
- SPEND_POINT;
- DESPAWN_WILD;
- OPEN_MOUNT;
- FUSE;
- OPEN_EQUIPMENT.

`ShadowGroupC2S` exposes exactly **5** group action codes:

- SAVE;
- DELETE;
- SUMMON;
- DISMISS;
- TOGGLE.

Every action code was reconciled to its provider method.

## Semantic classification

### Independent supernatural roots

Exact bounded effect facts close these seven non-spell supernatural actions:

1. **Shadow Eyes** — `toggleShadowEyes`;
2. **Shadow Arising** — `ShadowEvents.tryAbsorb`;
3. **Summon Shadow** — `summon`;
4. **Dismiss Shadow** — `dismiss` / `dismissInternal`;
5. **Position Swap** — `teleportSwap`;
6. **Despawn Wild Shadows** — `despawnWildShadows`;
7. **Shadow Fusion** — `fuseShadows`, explicitly gated by `FUSION_ENABLED`.

Together with the three exact registered spells, the complete current 1.1.9 semantic denominator is **10**.

### Deduplicated aliases and excluded management

The audit does not count these as additional semantic roots:

- Summon All / Dismiss All;
- group summon / dismiss / toggle;
- attack order;
- rename;
- behavior / aggro stance;
- assign/toggle slots;
- pickup toggle;
- group save/delete;
- storage;
- mount inventory;
- equipment UI;
- permanent release;
- spend point / leveling / title progression;
- administrative power grant/revoke.

The batch/group summon/dismiss surfaces converge on the already counted Summon/Dismiss causal actions.

### Downstream spell helpers

- `UmbralBondSpell.onCast` routes into provider guardian-binding behavior; `bindGuardian` is downstream of the registered `umbral_bond` spell and adds no second identity.
- `AuraOfTheMonarchSpell.onCast` applies the provider Aura effect; Aura conversion/helper state is downstream of `aura_of_the_monarch` and adds no second spell/action identity.
- Miasma tick effects are downstream of `miasma`.

## Reachability guard facts

The final reinforced audit closes the following exact-current guard topology:

- `ShadowActionC2S.handle` calls `ShadowSummoner.isAttuned`;
- `MiasmaSpell.checkPreCastConditions` calls `ShadowSummoner.isAttuned`;
- `UmbralBondSpell.checkPreCastConditions` calls `ShadowSummoner.isAttuned`;
- `AuraOfTheMonarchSpell.checkPreCastConditions` calls `ShadowSummoner.isAttuned`;
- `AttunementChoiceC2S.handle` calls `ModGameRules.canAttune` before granting powers;
- `ModGameRules.canAttune` has overloads that check server permission when restriction applies.

Publisher documentation independently states that all ShadowsZ keybinds, menus and spells remain inactive until attunement, and that `shadowszRestrictPowers=true` restricts power acquisition to operators.

Therefore physical artifact completeness does **not** establish deployed survival reachability.

## Exact config defaults

The exact artifact exposes these booleans:

- `progressMode=true`;
- `levelingEnabled=true`;
- `blackTexture=true`;
- `fusionEnabled=false`;
- `equipmentEnabled=false`.

The exact gamerule default is:

- `shadowszRestrictPowers=false`.

These are artifact defaults only. They are not substituted for the effective deployed world/config state.

Of these values, only `fusionEnabled` changes the semantic denominator directly: Shadow Fusion is the tenth semantic root. Equipment, progression, leveling and presentation settings do not mint additional roots under the Black Arcana metric.

## Semantic result

Current exact inventory:

- 3 registered Umbral spells;
- 6 core non-spell supernatural actions;
- 1 Fusion action gated by `fusionEnabled`;
- **10 total semantic identities**.

Because every player-facing power surface is attunement-gated and the effective deployed `shadowszRestrictPowers` gamerule is unavailable, strict contribution remains **+0**.

Evidence state: **exact inventory / conditional active surface**.

See [DEPLOYED-STATE-CHECKLIST.md](DEPLOYED-STATE-CHECKLIST.md) for the remaining promotion gate.