# Capability Matrix Delta — Apotheosis 8.8.0

## Phase 2AV scope

Phase 2AV closes the installed `apotheosis` 8.8.0 Adventure/RPG provider as candidate catalog component **#50**.

Canonical coverage at the reconciled branch base remains **49/100 = 49%** after Phase 2AU / PR #158. This tranche represents **50/100 = 50% only as a candidate** until latest-main reconciliation, CI GREEN on the exact reconciled HEAD, merge and post-merge `main` confirmation.

This component does **not** re-count `apothic_attributes`, `apothic_enchanting` or `apothic_spawners`; those are separate installed providers with their own catalog records.

## Exact identity

- physical artifact: `Apotheosis-1.21.1-8.8.0.jar`;
- mod id: `apotheosis`;
- physical SHA-1: `1e4837fcaf24fe73dba1082656736d872690b303`;
- physical pack: Minecraft 1.21.1 / NeoForge 21.1.248 / 595 top-level entries;
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- publisher: CurseForge project `313970`, file `8826922`;
- exact official source: `Shadows-of-Fire/Apotheosis@e825cd9dcb9a6fff5e163659812ff32390e343a6`;
- source root tree: `98ffba7432210ac6b5d807a83fc8e49e74db31fd`;
- exact Apotheosis Java package tree: `a517a5e6ecf47bc1eae07c28206868a4317ffb8b`.

## Authority matrix

| Surface | Exact 8.8.0 evidence | Authority / Black Arcana boundary |
|---|---|---|
| rarity / affix / gem | provider dynamic registries | Apotheosis owns its gear-affix/gem semantics; BA does not mirror them as spells or BA state |
| affix loot / rarity overrides | provider dynamic registries | provider loot-generation/rarity authority; consume only through proven provider-native seams |
| invaders / elites / rogue spawners | provider dynamic registries and provider state | Apotheosis owns Adventure encounter selection/runtime; no transfer to BA hazards or ritual authority |
| purity weights / augment / tiered augment | provider registries | provider item-upgrade/gem/augment semantics; no second BA progression resource |
| reforging / salvaging / augmenting / gem cutting | provider recipe/menu/bootstrap surfaces | provider workstation/item transformation authority |
| world tiers | `PLAYER_TIER` / `TIER_UNLOCKS` state plus server-gated `WorldTierPayload` | provider world-tier authority; client request is not BA cast intent and is accepted only under provider rules |
| invader/spawn state | `INVADER_COOLDOWN`, `INVADER_DATA`, `SPAWN_DATA` attachments | provider encounter persistence/state; do not duplicate into BA canonical state |
| loot/damage state | `BONUS_LOOT_TABLES`, `DAMAGE_REDUCTIONS` attachments | provider-owned runtime metadata |
| item/components | affixed-item, gem, rarity, radial-state and related data components | provider item/UI state; no ownership migration |
| network | seven registered provider payload types | provider-native transport only; never route C2S provider UI/state messages into BA casting |
| casting / spell / mana / ritual | no standalone registration or payload surface observed in the exact source-tree/bootstrap/network audit | no provider cast authority established; Black Arcana retains its canonical server-authoritative cast/ritual/resource pipeline |
| Apothic sibling modules | exact metadata lists Attributes mandatory and Enchanting/Spawners as separate ordered optional dependencies | separate providers; no double counting and no implicit authority merge |

## Exact registry set observed in the 8.8.0 bootstrap

`apotheosis:rarity`, `apotheosis:affix`, `apotheosis:gem`, `apotheosis:affix_loot_entry`, `apotheosis:invader`, `apotheosis:rogue_spawner`, `apotheosis:elite`, `apotheosis:purity_weights`, `apotheosis:augment`, `apotheosis:tiered_augment`, `apotheosis:rarity_override`.

The audit uses these internal declarations as factual evidence of provider ownership. It does not declare implementation classes to be stable public integration APIs.

## Network boundary

Exact bootstrap registers seven payload providers:

| Payload | Direction | Version | Boundary |
|---|---|---:|---|
| `apotheosis:config` | CLIENTBOUND | `4` | synchronized Adventure configuration |
| `apotheosis:boss_spawn` | CLIENTBOUND | `1` | provider boss announcement/state |
| `apotheosis:link_item` | SERVERBOUND | `1` | server validates current menu/slot context |
| `apotheosis:radial_state` | BIDIRECTIONAL | `1` | provider radial UI/state |
| `apotheosis:gem_case_select` | BIDIRECTIONAL | `1` | server validates held gem case and selected registry gem |
| `apotheosis:world_tier` | BIDIRECTIONAL | `1` | provider server validates manual-tier enablement and unlock state |
| `apotheosis:reroll_result` | CLIENTBOUND | `1` | provider reroll result/UI data |

These messages are not Black Arcana cast packets. Any future integration remains behind a dedicated adapter/boundary and must use a proven exact-version seam.

## Reload / synchronization consequence

Affix, gem, invader, rogue-spawner, elite, augment, rarity and related provider registries are data-driven/synchronized. Black Arcana must not create a stale second registry or cache provider data without a reload-aware invalidation contract.

## Clean-room / integration disposition

- `REFERENCE_ONLY / COMPATIBILITY_TARGET` for factual catalog closure;
- provider-native first;
- internal implementation classes are evidence, not automatically supported API;
- no code/assets/text copied or adapted;
- source code at the exact pin is MIT, while exact assets are All Rights Reserved and the current CurseForge project surface is All Rights Reserved;
- unsafe/unproven integration seams remain fail-closed.

`Spellbreaker` in the 8.8.0 changelog is an affix name. It is not evidence of a provider spell/casting runtime and creates no Black Arcana bridge.

## Remaining QA ceiling

The catalog closure does not prove source↔physical-JAR byte reproducibility, direct publisher-file hash equality, complete-modpack reload/mixin/runtime compatibility, binary stability of internal implementation classes, or optional compatibility behavior. Those remain fail-closed QA items and do not authorize duplicated runtime authority.
