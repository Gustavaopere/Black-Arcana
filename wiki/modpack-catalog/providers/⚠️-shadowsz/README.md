# ShadowsZ — 1.1.9

Status: `⚠️ PARTIAL / EXACT PHYSICAL=PUBLISHER ARTIFACT / EXACT SEMANTIC DENOMINATOR 10 / 9 COUNTED_EXACT + 1 CONDITIONAL FUSION`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7`;
- physical row: `#500`;
- JAR: `shadowsz-1.1.9.jar`;
- mod id: `shadowsz`;
- runtime: `1.1.9`;
- physical SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- sibling category: `Addons + Magic + Mobs`;
- required host: Iron's Spells 'n Spellbooks `3.16.3`.

The latest sibling revalidation preserves the same #500 filename/version/category tuple. No physical ShadowsZ drift is present.

## Exact artifact closure

NON-MERGE audit PR `#443` materialized the official Modrinth 1.1.9 artifact and hard-gated it against the physical SHA-1.

Final exact evidence:

- audit branch HEAD: `9628dc7d90f17afbac94372a52cd704740473e86`;
- exact audit run: `36422402267` — GREEN;
- bounded audit artifact: `10970337207`;
- artifact digest: `sha256:aebc421c6f4855e84abb5be6e5442d9cb3f4089093fe7fdbf1595b075bfeba3c`;
- publisher source: Modrinth version `Z5VFhs8D`;
- downloaded SHA-1: `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- exact equality: **publisher artifact SHA-1 = physical SHA-1**;
- metadata: `modId=shadowsz`, `version=1.1.9`, display name `Shadowsz`;
- provider class count: **86**.

CurseForge independently identifies the current NeoForge 1.21.1 release as File `8626238`, uploaded 2026-08-11. The provider is All Rights Reserved, so the audit retains only hashes, metadata, class/resource identities, localization keys, bounded action-routing facts and bounded method-effect call sets. It does not retain the JAR, protected assets, full disassembly or decompiled method bodies.

## Exact semantic denominator

The exact artifact closes **10 provider-owned semantic roots** under the Black Arcana metric.

| # | Semantic root | Exact artifact evidence | State |
|---:|---|---|---|
| 1 | Shadow Eyes | dedicated keybind + `toggleShadowEyes`; toggles provider state with provider feedback | `COUNTED_EXACT` |
| 2 | Shadow Arising | player interaction reaches `tryAbsorb`; mana/difficulty chance converts a fallen shadow into owned shadow data | `COUNTED_EXACT` |
| 3 | Position Swap | dedicated action route reaches `teleportSwap`; swaps player/shadow positions with portal/teleport effects and cooldown | `COUNTED_EXACT` |
| 4 | Summon Shadow | dedicated action route reaches `summon`; spends Iron's mana and manifests the stored shadow with portal/teleport effects | `COUNTED_EXACT` |
| 5 | Dismiss Shadow | dedicated action route reaches `dismiss` / `dismissInternal`; persists shadow state and demanifests the entity with portal/teleport effects | `COUNTED_EXACT` |
| 6 | Banish Wild Shadows | dedicated `DESPAWN_WILD` route reaches `despawnWildShadows`; player-invoked portal banishment of wild shadow entities | `COUNTED_EXACT` |
| 7 | Miasma | exact `ModSpells` registration `miasma` | `COUNTED_EXACT` |
| 8 | Umbral Bond | exact `ModSpells` registration `umbral_bond` | `COUNTED_EXACT` |
| 9 | Aura of the Monarch | exact `ModSpells` registration `aura_of_the_monarch` | `COUNTED_EXACT` |
| 10 | Shadow Fusion | dedicated `FUSE` route reaches `fuseShadows`; implementation reads `ShadowConfig.FUSION_ENABLED` | `CONDITIONAL` |

The exact spell registry contains exactly those **3** provider spell IDs and its initializer has **0 conditional branches**.

Therefore the provider contributes:

- **9 `COUNTED_EXACT` semantic objects**;
- **1 `CONDITIONAL` semantic object** — Shadow Fusion;
- strict global delta: **+9**.

## Deduplication and exclusions

The exact C2S surface contains **20 individual action codes** plus **5 group action codes**. They are not 25 additional magic objects.

Aliases and management surfaces are reconciled as follows:

- `SUMMON_ALL`, group summon and group hotkeys reuse the Summon Shadow causal root;
- `DISMISS_ALL`, group dismiss and group hotkeys reuse the Dismiss Shadow causal root;
- attack-order/stand-down changes mob targeting and is army command, not a new supernatural action;
- rename, behavior, aggro stance, item pickup, hotkey slot assignment, group save/delete and party controls are roster/AI organization;
- shared storage, mount inventory and equipment screens are inventory/UI surfaces;
- permanent release removes owned roster state and has no separate supernatural effect root;
- player/shadow level-point spending, titles and Progress Mode are progression/stat systems;
- accepting/claiming the power is a one-time attunement/consent gate, not a reusable magical action identity;
- administrative grant/revoke/level commands are excluded;
- `bindGuardian` is downstream implementation of Umbral Bond and does not mint a second root;
- `tryAuraConvert` is downstream implementation of Aura of the Monarch and does not mint a second root;
- school, attributes, effects, particles, sounds and downstream shadow AI are not standalone semantic actions.

## Exact config facts

The exact artifact exposes these Boolean config fields/defaults:

- `progressMode = true`;
- `levelingEnabled = true`;
- `blackTexture = true`;
- `fusionEnabled = false`;
- `equipmentEnabled = false`.

The exact gamerule default is:

- `shadowszRestrictPowers = false`.

The publisher description currently characterizes Progress Mode as optional/off by default, but the exact 1.1.9 artifact encodes `progressMode=true`. For exact runtime defaults, the artifact is authoritative.

No provider Boolean enable/disable field exists for Shadow Eyes, Arising, Position Swap, Summon, Dismiss, Banish Wild Shadows or the three spell registrations. Numerical config still tunes conversion chance, mana difficulty/cost, teleport cooldown, attack range and related balance without minting/removing semantic identities.

## Why the provider remains ⚠️

The semantic inventory itself is closed. The only remaining catalog blocker is the **effective deployed value of `fusionEnabled`**:

- exact artifact default: `false`;
- deployed pack/world config: not authoritatively captured;
- if effective `fusionEnabled=false`, Fusion remains inactive/excluded from strict count;
- if effective `fusionEnabled=true`, Fusion promotes to `COUNTED_EXACT` and contributes +1.

Therefore ShadowsZ remains **⚠️ partial/conditioned**, but no longer has an open action denominator.

See:

- [EXACT-1.1.9-SEMANTIC-INVENTORY.md](./EXACT-1.1.9-SEMANTIC-INVENTORY.md)
- [DEPLOYED-FUSION-CONFIG-CHECKLIST.md](./DEPLOYED-FUSION-CONFIG-CHECKLIST.md)

## Ownership boundary

- ShadowsZ owns Shadow Eyes/Arising, shadow manifestation/recall/banishment, Position Swap, Fusion, its army/roster/storage/progression state and its Umbral spell identities.
- Iron's Spells owns host mana and generic spell-runtime infrastructure.
- External mob mods retain authority for their own entity/boss semantics.
- Black Arcana must not duplicate ShadowsZ roster, shadow lifecycle, mana settlement, teleport execution or Umbral spell execution.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates exposed through verified contracts.

## Runtime QA remains separate

Catalog closure does not certify:

- dedicated-server interoperability with Iron's 3.16.3;
- roster/storage persistence;
- chunk-ticket cleanup;
- Position Swap safety;
- multiplayer ownership isolation;
- modded-boss conversion;
- exactly-once loot/XP/state settlement;
- large-army performance.

## Result

**⚠️ Partial / conditioned — exact denominator closed at 10.**

- **9 `COUNTED_EXACT`**
- **1 `CONDITIONAL` — Shadow Fusion**
- **strict global delta: +9**
- **remaining catalog evidence: deployed `fusionEnabled` only**
