# Corail Tombstone 9.5.6 — conditional castable action matrix

Status: `EXACT PUBLISHER FILE 8842741 / HASH-MATCHED CASTABLE-SURFACE AUDIT / 12 SEMANTIC ACTION FAMILIES DEDUPED / DEPLOYED ALLOW_* VALUES MISSING / NOT STRICT-ADDITIVE YET`

## Evidence

Current sibling authority rechecked at:

`neoforge-rpg-skilltree@006fca21e09b05b0426da1ddd46b3743a5e96fa8`

Physical row remains:

- `tombstone-neoforge-1.21.1-9.5.6.jar`;
- mod id `tombstone`;
- runtime `9.5.6`.

Exact audited publisher artifact:

- CurseForge File `8842741`;
- 2,520,705 bytes;
- SHA-1 `d830d16caa20b0d23a44ed6b1d339bc22afc2460`.

Focused NON-MERGE checkpoint:

- commit `47dad68e71eb6e062aa4ec8b733403fb51c15a5f`;
- CI run `36146834871`;
- `Temporary Tombstone 9.5.6 castable semantic audit NON-MERGE`: SUCCESS;
- canonical unit/build/GameTest/dedicated-server/Stage 05 companion gates: SUCCESS.

The audit retained only method/call/field/type identities needed to classify the actions. No proprietary implementation body is copied here.

## One-to-one conditional action map

| # | Exact class / family | Exact behavioral evidence | Semantic identity | Eligibility gate | Counting disposition |
|---:|---|---|---|---|---|
| 1 | `ItemTabletOfAssistance` | player/profile lookup, engraved name, Tombstone teleport-ticket API, assistance trigger | player-assistance/join teleport request | `allowTabletOfAssistance` | +1 if enabled |
| 2 | `ItemTabletOfCupidity` | randomized candidate selection plus provider spawn/location search | randomized location-search/relocation | `allowTabletOfCupidity` | +1 if enabled |
| 3 | `ItemTabletOfGuard` | `Helper.spawnSpectralWolf(...)`; casting type `SUMMONING` | Spectral Wolf summon | `allowTabletOfGuard` | +1 if enabled |
| 4 | `ItemTabletOfHome` | `CommandTBTeleport.getRespawnPoint(...)`; provider spawn-location validation | respawn/home teleport | `allowTabletOfHome` | +1 if enabled |
| 5 | `ItemTabletOfRecall` | bound Tomb/Location state plus provider location validation; teleport casting types | bound-location recall teleport | `allowTabletOfRecall` | +1 if enabled |
| 6 | `ItemGemstoneOfFamiliar` | saved-familiar lookup and `ItemReceptacleOfFamiliar.revive(...)` | familiar revival | `allowGemstoneOfFamiliar` | +1 if enabled |
| 7 | `ItemGemstoneOfGuardian` | `noGraveGuardianAround(...)` + `spawnGraveGuardian(...)` | Grave Guardian summon | `allowGemstoneOfGuardian` | +1 if enabled |
| 8 | `ItemGemstoneOfMerchant` | villager/provider merchant XP/level mutation and career increase | merchant trade-level improvement | `allowGemstoneOfMerchant` | +1 if enabled |
| 9 | `ItemGraveKey` | stored tomb location, server-level resolution and provider spawn-place validation | grave/tomb-location teleport | `allowGraveKey` | +1 if enabled |
| 10 | `ItemLostTablet` | exact enum `UNKNOWN/EXPLORATION/VILLAGE/TREASURE`; stored destination/location and structure-place lookup | lost-destination discovery/travel family | `allowLostTablet` | +1 if enabled; modes are not separate identities |
| 11 | `ItemMagicScroll` | stored `MobEffectInstance`, target/nearby-entity selection and `EffectHelper.addEffect(...)` | generic magic-effect cast wrapper | `allowMagicScroll` | +1 wrapper if enabled; individual effects +0 |
| 12 | `ItemScrollOfKnowledge` | stores player XP on enchant; restores XP / rewards readable-scroll progress on use | XP/knowledge storage-recovery/reward | `allowScrollOfKnowledge` | +1 if enabled; internal rewards are not separate identities |

## Deduplication rules

The exact audit resolves the previous ambiguity without inflating the provider:

- five tablets are five action families, not one generic tablet family and not multiple branches per ancient/non-ancient mode;
- Familiar/Guardian/Merchant gemstones are three distinct actions;
- Gemstone of Prayer remains outside this table because it invokes/supports the already-counted prayer family;
- Lost Tablet is **one** action family with three exact destination modes, not three spell identities;
- Magic Scroll is **one** generic effect-casting wrapper; the underlying status-effect variants are already metric-excluded and are not re-added;
- Scroll of Knowledge is **one** storage/recovery/reward action family; Erdos/readable-scroll rewards are not additional casts.

Therefore the config-sensitive surface has a maximum semantic contribution of:

`12 enabled gates -> +12 conditional actions`

No part of that +12 enters the strict numerator until the corresponding deployed booleans are observed.

## Remaining blocker

The read-only collector already has a bounded capture path for exactly these 12 Tombstone booleans. Repository evidence still contains no actual deployed pack values.

Consequently:

- strict Tombstone contribution remains **+10 `COUNTED_RELEASE_BOUNDED`**;
- conditional castable ceiling is **+12**;
- provider remains **⚠️ partial / conditioned**;
- runtime/economy/death/grave QA remains separate and fail-closed.

## Clean-room boundary

This matrix records only cryptographic identity, class/type/method/field/call-target names, exact enum constants and high-level behavioral classification needed for catalog interoperability.

No implementation bodies, assets, models, textures, sounds or proprietary code are reproduced.
