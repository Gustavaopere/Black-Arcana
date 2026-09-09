# Phase 2AW — Apotheotic Creation 2.0.0 checkpoint

## Status

Phase 2AW closes `apotheoticcreation` 2.0.0 as candidate provider component **#51** for the current physical catalog.

- branch base: `main@517b3e9c6da648c1470c227a11f571d951fbee47`;
- canonical base coverage: **50/100 = 50%** after Phase 2AV / PR #160;
- candidate coverage represented here: **51/100 = 51%**;
- no Stage 07 runtime code is changed;
- Phase 3 remains blocked.

Candidate status becomes canonical only after final latest-main reconciliation, CI GREEN on the exact reconciled HEAD, merge and post-merge main confirmation.

## Physical authority

Current physical inventory:

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- `apotheoticcreation-2.0.0.jar`;
- mod id `apotheoticcreation`;
- physical SHA-1 `6bbb91aea834941b47a6af3318b091f64e4375ab`;
- Create 6.0.10;
- Apotheosis 8.8.0.

## Publisher and source pin

Publisher evidence:

- CurseForge project `956637`;
- file `8391265`;
- file name `apotheoticcreation-2.0.0.jar`;
- uploader `themaxpowa`;
- release, NeoForge, Minecraft 1.21.1;
- uploaded 2026-07-08;
- project license label MIT;
- publisher Source link resolves to `maxpowa/ApotheoticCreation`.

Exact official source:

- repository `maxpowa/ApotheoticCreation`;
- branch line `mc/1.21.1`;
- commit `ed56ccf54e1be132c983c524597300e852098840`;
- commit message `feat: support minecraft 1.21.1`;
- exact tree `5c5d51ef69b5f0f50d398d7f0479b8ca83894f7d`;
- recursive tree inspection `truncated=false`;
- `gradle.properties`: mod version 2.0.0, MC 1.21.1, NeoForge 21.1.235 development baseline, Create `[6,)`, Apotheosis `[8,)`, MIT.

## Exact implementation closure

The exact tree contains one Java source file: `src/main/java/us/maxpowa/apc/ApotheoticCreation.java`.

It registers exactly two types in Create's built-in item-attribute registry:

1. `apotheoticcreation:rarity` → `RarityAttribute.Type`;
2. `apotheoticcreation:affix` → `AffixAttribute.Type`.

No addon-owned spell registry, mana/cast resource, ritual runtime, networking/payload class, saved state, attachment, mixin or second content registry is present in the complete exact source tree.

### Rarity path

The rarity attribute:

- serializes through Apotheosis `LootRarity.CODEC`;
- streams through `RarityRegistry.INSTANCE.holderStreamCodec()`;
- reads item rarity through `AffixHelper.getRarity(stack)`;
- returns no attribute for an unbound rarity;
- matches the selected provider rarity directly.

### Affix path

The affix attribute:

- serializes through `AffixRegistry.INSTANCE.holderCodec()`;
- streams through the provider holder stream codec;
- reads item affixes through `AffixHelper.getAffixes(stack)`;
- matches when the selected affix holder is present;
- enumerates bound affixes for Create filtering while excluding affix paths `socket` and `durable` from `getAllAttributes`.

The exclusion is recorded as enumeration behavior only. This audit does not claim a broader impossibility for explicitly constructed/deserialized attributes beyond what the source proves.

## Authority/deduplication result

- Apotheosis remains authority for rarities, affixes and item metadata.
- Create remains authority for Attribute Filter semantics and logistics consumers.
- Apotheotic Creation owns only the translation/registration bridge between those systems.
- Smart Observer, Brass Tunnel, funnel or other Create behavior remains downstream Create behavior, not an independent Apotheotic Creation API.
- Apokinetics remains a different concern: machine gems/sockets/upgrades are not provided by Apotheotic Creation.
- Black Arcana acquires no spell, resource, hazard, ritual, progression or world-effect authority from this addon.
- No direct BA runtime adapter is required for catalog closure.

## Clean-room result

Exact root `LICENSE.md` is MIT, copyright 2023 maxpowa. Exact metadata and the publisher also label the project MIT. No separate asset-license file appears in the exact tree.

The source was inspected read-only for factual compatibility evidence. No code, assets or text are copied/adapted into Black Arcana.

## Remaining fail-closed QA

- source↔physical-JAR reproducibility;
- physical-vs-publisher file hash equality;
- custom datapack rarity/affix behavior;
- multiple-affix Create UI/filter behavior;
- whitelist/blacklist and combination semantics owned by Create;
- downstream Smart Observer / Brass Tunnel / funnel behavior;
- persisted-filter reload/restart behavior;
- full-pack dedicated/client compatibility;
- future Create/Apotheosis version parity.

These items do not justify inventing a wider runtime surface.

## Canonicalization gate

Before merge:

1. fetch latest `origin/main`;
2. reconcile if it advanced;
3. review the final diff and exact eight-file scope;
4. require CI GREEN on the exact reconciled HEAD;
5. merge without discarding concurrent work;
6. confirm final `main` SHA and applicable post-merge validation.

Phase 3 remains blocked.