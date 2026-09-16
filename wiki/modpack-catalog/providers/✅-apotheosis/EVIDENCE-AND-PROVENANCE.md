# Apotheosis 8.8.0 — Evidence and provenance

## Physical authority

Current physical modpack authority:

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- artifact `Apotheosis-1.21.1-8.8.0.jar`;
- mod id `apotheosis`;
- physical SHA-1 `1e4837fcaf24fe73dba1082656736d872690b303`;
- physical Placebo 9.9.2;
- physical Apothic Attributes 2.10.1;
- physical Apothic Enchanting 1.6.2;
- physical Apothic Spawners 1.4.0.

Presence/version/hash claims come from the physical inventory rather than publisher naming alone. The Apothic modules are independent installed provider components and are not re-counted by this Apotheosis record.

## Publisher evidence

Current publisher surface identifies:

- CurseForge project `313970`;
- exact 8.8.0 file id `8826922`;
- file name `Apotheosis-1.21.1-8.8.0.jar`;
- published 2026-09-07;
- NeoForge / Minecraft 1.21.1;
- accompanying sources and stock-data files;
- current project license label All Rights Reserved.

The publisher license label is retained separately from exact source-code and asset-license evidence.

## Exact official source pin

Official repository: `Shadows-of-Fire/Apotheosis`.

Exact 8.8.0 source:

- commit `e825cd9dcb9a6fff5e163659812ff32390e343a6`;
- commit message `8.8.0`;
- commit date 2026-09-07;
- root tree `98ffba7432210ac6b5d807a83fc8e49e74db31fd`;
- exact `src/main/java/dev/shadowsoffire/apotheosis` package tree `a517a5e6ecf47bc1eae07c28206868a4317ffb8b`.

## Exact source metadata

At the exact 8.8.0 commit:

- mod id `apotheosis`;
- mod version 8.8.0;
- Minecraft 1.21.1;
- Java 21;
- NeoForge baseline/range 21.1.235 / `[21.1.235,)`;
- Placebo baseline/range 9.9.2 / `[9.9.2,)`;
- Apothic Attributes baseline/range 2.10.0 / `[2.10.0,)`;
- Apothic Enchanting 1.6.2+ is an ordered-after optional dependency;
- Apothic Spawners 1.4.0+ is an ordered-after optional dependency;
- Curios 9.5.1+1.21.1+ is optional;
- generated source metadata license string is MIT;
- generated metadata registers three Apotheosis mixin configuration names.

The physical pack's NeoForge 21.1.248, Placebo 9.9.2 and Apothic Attributes 2.10.1 satisfy the mandatory declared minimums. Installed Apothic Enchanting 1.6.2 and Apothic Spawners 1.4.0 satisfy the optional version floors when present. This range reconciliation does not prove full runtime compatibility or source↔JAR reproduction.

## Provider bootstrap / registry evidence

The exact `Apotheosis` bootstrap establishes these provider registry keys:

- `apotheosis:rarity`;
- `apotheosis:affix`;
- `apotheosis:gem`;
- `apotheosis:affix_loot_entry`;
- `apotheosis:invader`;
- `apotheosis:rogue_spawner`;
- `apotheosis:elite`;
- `apotheosis:purity_weights`;
- `apotheosis:augment`;
- `apotheosis:tiered_augment`;
- `apotheosis:rarity_override`.

The dynamic-holder initialization is provider-owned and data/reload-oriented. Exact class inspection additionally establishes:

- `AffixRegistry` as a tier-aware dynamic registry for provider affixes;
- `GemRegistry` as a tier-aware dynamic registry for provider gems;
- `InvaderRegistry` as a tier-aware dynamic registry for provider invader definitions;
- `RogueSpawnerRegistry`, `EliteRegistry` and `AugmentRegistry` as weighted dynamic registries;
- `RarityRegistry` and `AffixLootRegistry` as provider dynamic registries.

These classes are inspected only to establish factual ownership and lifecycle. This audit does not declare implementation classes to be binary-stable public APIs.

## Item / workstation authority

Exact bootstrap/provider holders register or initialize Adventure/RPG surfaces including:

- affixed-item, gem, rarity and related data components;
- reforging;
- salvaging;
- augmenting;
- gem cutting;
- corresponding provider menus/workstations/recipe serializers;
- provider gear/loot systems and affix results.

These remain Apotheosis-owned item/loot/transformation semantics. Black Arcana must not reinterpret them as its casting, ritual or resource state.

## Attachment / persistent-state evidence

Exact provider holders establish attachments/state for:

- `PLAYER_TIER`;
- `TIER_UNLOCKS`;
- `INVADER_COOLDOWN`;
- `INVADER_DATA`;
- `SPAWN_DATA`;
- `BONUS_LOOT_TABLES`;
- `DAMAGE_REDUCTIONS`.

`PLAYER_TIER` is provider player state and `TIER_UNLOCKS` stores unlocked `WorldTier` values. World tiers are `HAVEN`, `FRONTIER`, `ASCENT`, `SUMMIT`, `PINNACLE`.

Provider tier changes remain server-gated. `WorldTier.setWorldTier` enforces provider configuration/unlock rules before mutating tier state and emits provider-side follow-up behavior/event state. Black Arcana does not mirror or own this tier state.

## Exact network inventory

Exact bootstrap registers seven payload providers:

| Payload | Flow | Version | Observed responsibility |
|---|---|---:|---|
| `apotheosis:config` | CLIENTBOUND | `4` | synchronized Adventure configuration |
| `apotheosis:boss_spawn` | CLIENTBOUND | `1` | provider boss announcement data |
| `apotheosis:link_item` | SERVERBOUND | `1` | link current inventory/menu item into provider chat representation |
| `apotheosis:radial_state` | BIDIRECTIONAL | `1` | provider radial UI/state |
| `apotheosis:gem_case_select` | BIDIRECTIONAL | `1` | provider gem-case UI/selection |
| `apotheosis:world_tier` | BIDIRECTIONAL | `1` | provider world-tier UI/state |
| `apotheosis:reroll_result` | CLIENTBOUND | `1` | provider affix-reroll result/UI state |

Server-side checks observed on relevant inbound paths:

- `LinkItemToChatPayload` resolves/validates the requested slot against the player's current inventory/menu context;
- `GemCaseSelectPayload` requires the relevant held item to be the provider gem case and validates the selected id against `GemRegistry` before storing selection;
- `WorldTierPayload` only accepts a manual tier change when manual tiering is enabled and the requested tier is already unlocked for the player;
- `RadialStatePayload` server handling changes provider radial state rather than invoking a spell/cast runtime.

These provider packets must not be reused as Black Arcana cast intent. Client-originated provider UI/state messages remain subject to provider server validation and never become authority merely because they are bidirectional.

## Casting / spell / ritual negative evidence

The exact 8.8.0 source-tree/bootstrap/network audit did not reveal a standalone spell registry, mana/cast resource, ritual registry, cast-intent payload family or independent casting pipeline.

This is intentionally scoped negative evidence. It establishes that this catalog pass found no competing standalone casting authority in the audited provider surfaces; it does not prove that arbitrary internal classes are supported APIs or that future versions cannot change.

The 8.8.0 changelog mentions a `Spellbreaker` affix adjustment. `Spellbreaker` is an affix name in the provider's affix system, not evidence of a spell/casting registry or an interoperability seam.

## Authority / deduplication interpretation

Apotheosis 8.8.0 is authority for its Adventure/RPG runtime including affix, rarity, gem, affix-loot, encounter/invader, rogue-spawner/elite, world-tier and associated item/workstation semantics.

Separate Apothic providers retain their own authority:

- `apothic_attributes` — attribute/effect/runtime authority already cataloged;
- `apothic_enchanting` — enchanting/table/stat authority already cataloged;
- `apothic_spawners` — spawner modification/runtime authority already cataloged.

A dependency relationship does not collapse those modules into this component and does not justify double counting.

Black Arcana retains canonical authority over server-authoritative casting, targeting, transactional resource costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety. RPG Skill Tree receives no direct Apotheosis Adventure-runtime mutation authority from this catalog record.

## Reload / integration boundary

Because provider registries are data-driven/dynamic and synchronized, future integration must preserve provider lifecycle. Black Arcana must not create a competing mirror or stale long-lived cache without an exact reload/invalidation contract.

Preferred disposition:

1. provider-native public/data/event seam first;
2. isolate any integration behind a Black Arcana boundary/adapter;
3. preserve provider identity and server-side validation;
4. do not double-process provider effects/events;
5. do not create a second resource or cast pipeline;
6. if a safe exact-version seam is not established, fail closed.

Implementation classes inspected here are evidence, not an integration contract by themselves.

## Unproven / intentionally fail-closed

- source/JAR byte reproducibility;
- direct CurseForge-file hash equality with the physical installed artifact;
- complete-modpack datapack/data-registry reload ordering;
- complete-modpack mixin interactions;
- dedicated-server/client smoke for all provider paths;
- optional Curios behavior;
- optional Apothic Enchanting/Spawners compatibility paths;
- binary/source stability of implementation classes not documented as extension APIs;
- future-version parity.

No unproven item is promoted into Black Arcana implementation authority by this catalog closure.

## Licensing / clean-room provenance

Observed license layers:

- root source code at the exact commit: MIT;
- generated source metadata: MIT;
- exact `LICENSE_ASSETS`: Copyright Stormraven Studios, All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

Black Arcana's `SOURCES.md` and `THIRD_PARTY_NOTICES.md` explicitly distinguish factual inspection/API relationships from derivation rights. This audit is `REFERENCE_ONLY / COMPATIBILITY_TARGET`. No provider code, assets, text, models or sounds are copied or adapted.
