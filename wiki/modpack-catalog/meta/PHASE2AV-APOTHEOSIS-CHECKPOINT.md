# Phase 2AV — Apotheosis 8.8.0 checkpoint

## Status

Phase 2AV audits the installed `apotheosis` 8.8.0 Adventure/RPG provider as candidate component **#50**.

Branch base at tranche creation: `main@f3a3f95a10cf830b6bf973612d519e53d9168adc`.

Canonical coverage at that base: **49/100 = 49%**, with Phase 2AU / PR #158 already merged. This checkpoint describes **50/100 = 50% only as a candidate** until the branch is reconciled with the latest `main`, CI is GREEN on the exact reconciled HEAD, the PR is merged and final `main` is confirmed.

No Stage 07 runtime implementation is part of this tranche.

## Physical pack authority

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level modlist entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- physical artifact `Apotheosis-1.21.1-8.8.0.jar`;
- mod id `apotheosis`;
- physical SHA-1 `1e4837fcaf24fe73dba1082656736d872690b303`.

Related physical artifacts remain separate providers:

- Apothic Attributes 2.10.1;
- Apothic Enchanting 1.6.2;
- Apothic Spawners 1.4.0;
- Placebo 9.9.2.

They are not re-counted by this phase.

## Publisher / source pin

Publisher evidence:

- CurseForge project `313970`;
- exact file id `8826922`;
- `Apotheosis-1.21.1-8.8.0.jar`;
- NeoForge / Minecraft 1.21.1;
- published 2026-09-07;
- sources/stock-data files exposed alongside the release;
- current project license label All Rights Reserved.

Exact official source:

- repository `Shadows-of-Fire/Apotheosis`;
- commit `e825cd9dcb9a6fff5e163659812ff32390e343a6`;
- commit message `8.8.0`;
- commit date 2026-09-07;
- root tree `98ffba7432210ac6b5d807a83fc8e49e74db31fd`;
- exact `dev/shadowsoffire/apotheosis` Java package tree `a517a5e6ecf47bc1eae07c28206868a4317ffb8b`.

Exact metadata declares Minecraft 1.21.1, Java 21, NeoForge 21.1.235+, Placebo 9.9.2+, Apothic Attributes 2.10.0+, Apothic Enchanting 1.6.2+ optional/ordered after, Apothic Spawners 1.4.0+ optional/ordered after, and Curios optional at 9.5.1+1.21.1+.

The installed pack satisfies the declared mandatory minimums. That range check does not itself prove complete runtime compatibility.

## Provider semantic closure

Exact bootstrap establishes provider-owned registry keys for:

- rarity;
- affix;
- gem;
- affix loot entry;
- invader;
- rogue spawner;
- elite;
- purity weights;
- augment;
- tiered augment;
- rarity override.

The exact provider also owns reforging, salvaging, augmenting, gem-cutting/workstation/menu/recipe surfaces plus affixed-item/gem/rarity and related item state.

Observed persistent/runtime state includes provider attachments for player world tier/unlocks, invader cooldown/data, spawn data, bonus loot tables and damage reductions.

This is Adventure/RPG gear/loot/encounter/progression runtime. It does not transfer Black Arcana's casting, ritual, hazard, corruption/strain or world-safety authority.

## Network closure

Seven exact payload providers are registered:

- `apotheosis:config` — PLAY CLIENTBOUND, version `4`;
- `apotheosis:boss_spawn` — CLIENTBOUND, version `1`;
- `apotheosis:link_item` — SERVERBOUND, version `1`;
- `apotheosis:radial_state` — BIDIRECTIONAL, version `1`;
- `apotheosis:gem_case_select` — BIDIRECTIONAL, version `1`;
- `apotheosis:world_tier` — BIDIRECTIONAL, version `1`;
- `apotheosis:reroll_result` — CLIENTBOUND, version `1`.

Relevant server validation:

- item-link C2S validates current slot/menu context;
- gem-case C2S validates the held gem-case item and selected gem against the provider registry;
- world-tier C2S accepts a manual change only when provider configuration allows it and the requested tier is unlocked;
- radial-state server handling mutates provider UI/state only.

These are provider-native interaction/state messages, not Black Arcana cast-intent packets.

## Casting / magic-authority boundary

No standalone spell, mana, ritual or casting registration/payload surface was observed in the exact 8.8.0 source-tree/bootstrap/network audit.

This is a negative catalog observation, not a claim that every provider implementation detail is a public API. `Spellbreaker` in the 8.8.0 changelog is an affix name and is not evidence of a spell runtime.

Black Arcana therefore retains canonical authority over:

- server-authoritative casting and targeting;
- transactional costs/replay protection;
- BA cooldowns/charges;
- hazards and destructive-world policy;
- rituals;
- Corruption and Strain;
- Arcane Danger;
- Backlash;
- world safety.

No second mana/resource or cast pipeline is introduced.

## Reload / integration contract

The provider's core rarity/affix/gem/loot/encounter/augment registries are dynamic/data-backed and synchronized. Any future Black Arcana integration must be reload-aware and provider-native first; it must not mirror provider registries as a competing authority.

Implementation classes inspected here establish factual behavior/ownership only. A future adapter may use only a proven exact-version public/data/event seam. If no safe seam is established, integration remains fail-closed.

## Licensing / clean-room

- exact source root license: MIT;
- generated source metadata: MIT;
- exact source assets: All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

These evidence layers are recorded separately. The audit is `REFERENCE_ONLY / COMPATIBILITY_TARGET`; no provider code/assets/text are copied or adapted.

## Remaining fail-closed QA

- exact source↔physical-JAR byte reproducibility;
- direct physical-vs-publisher artifact hash equality;
- complete-modpack data reload/event ordering;
- complete-modpack mixin/runtime interactions;
- dedicated/client smoke for these provider paths;
- optional Curios / optional Apothic runtime behavior;
- stability of implementation classes that are not explicit supported APIs;
- future-version parity.

## Merge gate

Before canonicalizing component #50:

1. fetch latest `origin/main`;
2. reconcile the branch if `main` advanced;
3. review the final diff and exact scope;
4. require CI GREEN on the exact reconciled HEAD;
5. merge without discarding concurrent work;
6. confirm PR state and final `main` SHA;
7. verify applicable post-merge workflow/status.

Phase 3 remains blocked until the catalog/deduplication pass establishes actual Black Arcana gaps.
