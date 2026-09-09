# Phase 2AM checkpoint — Apothic Attributes 2.10.1

## State

`CATALOG CLOSURE CANDIDATE / EXACT SOURCE-VERSION PIN / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical `main`: `433233164f61bbf6b6d5cb8aa9625cf286a79a23`
- predecessor: Phase 2AL / PR #145, component #40 (`efiscompat`)
- branch: `docs/magic-catalog-phase2am-apothic-attributes-2.10.1`
- canonical coverage at branch creation: `40/100 = 40%`
- proposed result after canonical merge: `41/100 = 41%`

The original Apothic work began concurrently from `main@73a425051d242a33af157a3f73ca816498e8eba8` under a stale Phase 2AL label. While it was being audited, PR #145 merged `efiscompat` as the canonical Phase 2AL/component #40. Apothic was therefore re-based semantically by creating this new Phase 2AM branch directly from `main@433233164f61bbf6b6d5cb8aa9625cf286a79a23`; no ours/theirs conflict strategy was used and efiscompat evidence is preserved.

## Physical identity

- artifact: `ApothicAttributes-1.21.1-2.10.1.jar`
- mod id: `apothic_attributes`
- version: `2.10.1`
- SHA-1: `6a6b84d09801621df5cc2c8a68f35bd93a6cda0f`
- physical NeoForge: `21.1.248`
- physical Placebo: `9.9.2`
- physical Curios: `9.5.1+1.21.1`

## Exact source

`Shadows-of-Fire/Apothic-Attributes@686361b2c7b0e76bf4158890bb8a2e42ef805622`

Source metadata is exact semantic version 2.10.1 and targets Minecraft 1.21.1 / Java 21 / NeoForge 21.1.235 / Placebo 9.9.0, with Curios optional. Generated runtime metadata declares compatible minimum ranges satisfied by the physical pack.

## Closed inventory

- 0 standalone spells/glyphs/rituals observed;
- 2 synchronized custom registries;
- 22 attributes;
- 7 mob effects;
- 31 potions;
- 37 generated brewing mixes;
- 5 damage types;
- 2 data components;
- 3 attachments;
- 7 equipment slot objects;
- 11 slot groups;
- 3 provider tags;
- 1 particle + 1 sound;
- 2 clientbound PLAY payloads;
- 7 common + 1 client mixin;
- server-side `AbilityCooldowns` public API;
- conditional Curios modifier bridge;
- provider config/combat formulas and reload behavior.

## Critical boundaries

- no second cast engine or mana/resource authority is introduced by this provider;
- Apothic owns its combat formulas and generic proc runtime;
- BA Backlash remains BA-owned and must not trigger normal Apothic offensive proc chains by intentional integration;
- Apothic `cooldown_reduction` does not automatically apply to BA cooldowns;
- Curios remains Curios authority, Apothic owns only its modifier bridge, and BA retains its bounded snapshot provider;
- exact Detonation source discrepancy (`DamageTypes.BLEEDING` call) is recorded literally rather than corrected by assumption;
- Phase 3 remains blocked.

## Provenance

- root upstream source license: MIT;
- upstream assets: All Rights Reserved;
- `StackAttributeModifiersEvent.java` has a file-level Forge Development LLC / SPDX LGPL-2.1-only header;
- source inspection is read-only factual cataloging;
- no code/assets copied or adapted;
- byte-for-byte source/JAR equality is not claimed.

## Merge protocol

Before merge:

1. fetch latest `main`;
2. reconcile if advanced;
3. review diff for preservation of prior canonical evidence;
4. ensure central provenance ledger/indices are updated;
5. run Black Arcana CI on exact reconciled HEAD;
6. require applicable unit/diff/build/JAR/GameTest/dedicated-server gates GREEN;
7. resolve review findings;
8. merge only with expected exact HEAD;
9. confirm final `main` SHA and post-merge CI evidence.
