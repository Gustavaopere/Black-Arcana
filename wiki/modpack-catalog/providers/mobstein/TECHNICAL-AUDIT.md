# Mobstein 5.4.4 — technical, provenance and QA audit

## Scope

This is an artifact/public-documentation audit for the installed Mobstein provider. It deliberately does **not** decompile the installed JAR and does not treat undocumented internals as known.

## 1. Exact installed artifact

From the current physical modlist:

- filename: `mobstein-5.4.4-neoforge-1.21.1.jar`;
- mod id: `mobstein`;
- runtime name: `Mobstein`;
- runtime version: `5.4.4`;
- modlist classification note: `MCreator mod`;
- SHA-1: `3672d88f940ddd474a5429d7066b099cd0ce0c29`;
- CurseForge/package fingerprint: `3386302902`.

The same modlist currently contains:

- GeckoLib `4.9.2`;
- JEI `19.53.0.425`;
- Sable `2.0.5`.

Presence does not prove compatibility. It only fixes the exact installed identities for later QA.

## 2. Exact publisher release

Official CurseForge evidence:

- project ID `1193873`;
- author Pecsitonic;
- project license **All Rights Reserved**;
- Client & Server environment;
- exact NeoForge 1.21.1 file ID `8040734`;
- filename exactly matches the installed file;
- release date `2026-05-04`;
- release type `Release`;
- 5.4.4 release note: `Mobstein now is compatible with "Sable Mod"`.

The exact file identity matches the current modlist filename/version. The modlist's SHA-1 remains the local binary identity; CurseForge's public file page is the publisher release identity.

## 3. Public dependency statements

The publisher guide states that the 1.20.1/1.21.1 line requires **GeckoLib** and tells users to ensure **JEI** is installed.

The current pack has both. This establishes only presence alignment, not an API-level Black Arcana integration contract.

The 5.4.4 release separately declares Sable compatibility. It does not identify the exact Sable version or publish a compatibility matrix.

## 4. Source/provenance boundary

No official public Mobstein source repository or exact source revision for 5.4.4 was located during this checkpoint.

The CurseForge project is All Rights Reserved and additionally states that the mod may not be reposted and that unofficial published ports are not allowed.

Black Arcana posture:

- `REFERENCE_ONLY / COMPATIBILITY_TARGET / ALL RIGHTS RESERVED`;
- publisher documentation and release metadata may be used to catalog observable/player-facing behavior;
- no Mobstein code/assets/text are copied into Black Arcana;
- no installed-JAR decompilation is used to fill catalog gaps;
- no private class/method/event/registry name is invented;
- provider-specific implementation remains fail-closed without a supported external boundary.

## 5. What public evidence closes

Publisher documentation is sufficient to establish the semantic existence of:

- Clinical Stretch resurrection and an approximately 15-second night-time preparation window;
- ten named resurrected creature forms and their documented utility/taming behavior;
- body-part/full-body/organ processing;
- Surgery Stretch and six documented construction types;
- four provider construction perks and their public ranges;
- Subject Assembly Machine mannequin flow;
- seven failed-experiment variants;
- Dr. Mobstenio and Igor progression surfaces;
- five syringe types and their broad roles;
- three named structures and their broad biome placement;
- Witherstein's syringe-awakened three-stage encounter;
- explicit Reviver exclusion for Resurrected Warden and Frankenstein;
- a publisher claim of Sable compatibility in 5.4.4.

## 6. What public evidence does not close

The following remain `UNVERIFIED`:

- exact registry IDs for entities/items/blocks/effects/structures;
- exact damage/health/speed values outside the explicitly published Surgery Stretch ranges;
- AI target selectors, ownership storage and tame-state persistence;
- entity/event API hooks;
- exact resurrection transaction lifecycle;
- duplicate-prevention/replay handling for Stretch operations;
- exact random organ probability and organ identities;
- Witherstein stage thresholds, spawn counts, loot/reward identities and repeatability;
- exact Sable 2.0.5 behavior;
- server-side chunk/sublevel lifecycle behavior;
- external API stability/support policy;
- interaction with Epic Fight, RPG progression, Black Arcana or other necromancy providers.

## 7. Static semantic QA risks

These are not claimed bugs. They are points where the public contract requires runtime verification before an adapter can depend on it.

### 7.1 Approximate Clinical Stretch timing

The guide says approximately 15 seconds. Treating this as an exact 300-tick API contract would be unjustified. Runtime code must not be designed around an inferred exact timer unless a supported boundary exposes one.

### 7.2 “Any mob” Reviver wording

The same official guide explicitly excludes Resurrected Warden and Frankenstein from Reviver Syringe revival. Therefore the broad phrase cannot be interpreted as literally universal.

### 7.3 Igor Suspicious Syringe count

The guide says several are required and mentions a maximum of four. Exact accumulation/reset/failure semantics are not exposed and need runtime observation before integration.

### 7.4 Putrid Horse stages

The guide says approximately five aesthetic rot stages. Do not freeze an exact five-state persistence schema from that wording.

### 7.5 Surgery Stretch “perks”

The public ranges are useful factual behavior, but the term `perk` must not be conflated with RPG Skill Tree. Provider-specific generation/distribution internals are not known.

### 7.6 Blacksmithstrength presentation

The guide explicitly says Frankenstein's nearby `Blacksmithstrength` grants speed despite a strength-looking icon. Preserve the publisher's observed semantic description; do not infer an effect registry or attribute implementation.

### 7.7 Sable compatibility

5.4.4 claims compatibility with Sable, but the current pack's Sable is 2.0.5 and the release note gives no version. Required runtime checks include:

- Clinical/Surgery/Assembly blocks on or near sublevels;
- resurrected companion transform/position correctness;
- riding behavior where applicable;
- AI/pathing across the physical/sublevel boundary;
- death/removal/owner cleanup;
- no duplication during assembly/disassembly where Mobstein inventories/entities are involved.

Black Arcana does not patch those semantics speculatively.

## 8. Runtime QA matrix required before provider-specific integration

| Area | Minimum evidence |
|---|---|
| Load | dedicated server + physical client load with exact 5.4.4 artifact |
| Clinical Stretch | night route, day route with Lightningbolt Syringe, interruption/break/reload behavior |
| Duplicate safety | repeated interaction, reconnect, chunk unload/reload, block break during operation |
| Resurrection ownership | tamed owner identity, death, respawn/revival, cross-dimension behavior |
| Reviver exclusions | Warden/Frankenstein explicit negative cases |
| Organs | extraction completion, random result cardinality, Resurrected Villager alternative route |
| Surgery Stretch | all six types, four provider perks, invalid input restrictions, cleanup |
| Assembly Machine | custom head creation + mannequin, no unintended ability inheritance |
| Igor | table proximity, failure/reset, syringe count, output exclusion of 062/097 |
| Witherstein | awakening identity, stages, completion, repeatability and reward semantics |
| Sable 2.0.5 | block/entity/riding/AI/lifecycle correctness on current physical stack |
| Multiplayer | owner/friendly-fire/access control and no cross-player state leakage |

## 9. Black Arcana implementation consequence

No Mobstein-specific Java adapter is approved by this audit.

Allowed now:

- factual Wiki coverage;
- semantic deduplication;
- provider-authority mapping;
- future QA planning;
- provider-neutral handling of ordinary Minecraft entity facts where no Mobstein-private state is required.

Blocked now:

- reflective/private-state integration;
- copied/decompiled implementation;
- invented Mobstein event/API contracts;
- automatic Mobstein↔Black Arcana resource conversion;
- duplicate resurrection/companion/progression settlement.

Current disposition: `CATALOG ADVANCED / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED`.