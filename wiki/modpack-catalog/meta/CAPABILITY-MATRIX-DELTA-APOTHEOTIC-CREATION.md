# Capability Matrix Delta — Apotheotic Creation 2.0.0

## Phase 2AW scope

Phase 2AW closes the installed `apotheoticcreation` 2.0.0 interoperability addon as candidate catalog component **#51**.

Canonical coverage at the branch base is **50/100 = 50%** after Phase 2AV / PR #160 merged `apotheosis` 8.8.0 at `main@517b3e9c6da648c1470c227a11f571d951fbee47`. This tranche represents **51/100 = 51% only as a candidate** until latest-main reconciliation, CI GREEN on the exact reconciled HEAD, merge and post-merge `main` confirmation.

This component is a narrow Create ↔ Apotheosis metadata-filter bridge. It does not become authority for Create logistics or Apotheosis affix/rarity content.

## Exact identity

- physical artifact: `apotheoticcreation-2.0.0.jar`;
- mod id: `apotheoticcreation`;
- display name: `Apotheosis/Create Addon`;
- physical SHA-1: `6bbb91aea834941b47a6af3318b091f64e4375ab`;
- physical pack: Minecraft 1.21.1 / NeoForge 21.1.248 / 595 top-level entries;
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- physical Create: 6.0.10;
- physical Apotheosis: 8.8.0;
- publisher: CurseForge project `956637`, file `8391265`, released 2026-07-08 for NeoForge / Minecraft 1.21.1;
- publisher source link resolves to `maxpowa/ApotheoticCreation`;
- exact official source: `maxpowa/ApotheoticCreation@ed56ccf54e1be132c983c524597300e852098840`;
- exact source tree: `5c5d51ef69b5f0f50d398d7f0479b8ca83894f7d`;
- recursive exact tree inspection: `truncated=false`.

## Exact source surface

The exact 2.0.0 / Minecraft 1.21.1 source tree contains one Java source file, `us/maxpowa/apc/ApotheoticCreation.java`.

That class registers exactly two entries into Create's `ITEM_ATTRIBUTE_TYPE` registry:

- `apotheoticcreation:rarity`;
- `apotheoticcreation:affix`.

The source declares required mod dependencies on Create `[6,)` and Apotheosis `[8,)`, both `BOTH`, ordered `AFTER`. The physical Create 6.0.10 and Apotheosis 8.8.0 satisfy those declared ranges.

## Authority matrix

| Surface | Exact 2.0.0 evidence | Authority / Black Arcana boundary |
|---|---|---|
| rarity filter attribute | `RarityAttribute.Type`, registered as `apotheoticcreation:rarity` | reads Apotheosis `LootRarity` via `AffixHelper`; Apotheosis remains rarity authority, Create remains filter/logistics authority |
| affix filter attribute | `AffixAttribute.Type`, registered as `apotheoticcreation:affix` | reads Apotheosis affixes via `AffixHelper`; Apotheosis remains affix authority, Create remains filter/logistics authority |
| rarity serialization | `LootRarity.CODEC` + `RarityRegistry.INSTANCE.holderStreamCodec()` | provider-native identity/serialization is reused; BA must not mirror a rarity registry |
| affix serialization | `AffixRegistry.INSTANCE.holderCodec()` + holder stream codec | provider-native identity/serialization is reused; BA must not mirror an affix registry |
| visible affix enumeration | `getAllAttributes` omits affix paths `socket` and `durable` | catalog records the exact UI/enumeration boundary; do not generalize to “every affix” |
| downstream routing | normal Create consumers of `ItemAttribute` | Brass Tunnel, Smart Observer or other logistics behavior is Create-owned downstream behavior, not an independent addon hook |
| state / persistence | no addon-owned persistence/attachment surface observed in the complete Java/source tree | no new BA state and no state-authority transfer |
| networking | no addon-owned payload/network registration observed in the complete Java/source tree | no C2S/S2C bridge to BA casting |
| casting / mana / ritual / hazards | no such registration/resource/runtime surface exists in the complete Java source | Black Arcana retains all canonical magic-runtime authority |

## Matching semantics

`RarityAttribute.appliesTo` obtains the item's Apotheosis rarity and fails false when the holder is unbound; otherwise it matches the selected provider rarity.

`AffixAttribute.appliesTo` obtains the item's Apotheosis affix map and checks whether the selected provider affix holder is present. `AffixAttribute.Type.getAllAttributes` enumerates bound affixes but filters out paths `socket` and `durable` before exposing them as selectable attributes.

The audit does not infer Create whitelist/blacklist, AND/OR combination, Smart Observer, Brass Tunnel or other routing semantics from this addon. Those remain Create-owned downstream behavior and require runtime QA where needed.

## Black Arcana disposition

- `REFERENCE_ONLY / COMPATIBILITY_TARGET` for catalog/deduplication;
- no direct Black Arcana adapter is required merely because this bridge is installed;
- Black Arcana must not reimplement or intercept provider rarity/affix classification;
- no second mana/resource, cast pipeline, affix registry or rarity registry is introduced;
- if a future BA feature needs this exact filter behavior, prefer the existing provider-native Create `ItemAttribute` path rather than parallel classification.

## Clean-room / provenance

- exact `gradle.properties` declares `mod_license=MIT` and `mod_version=2.0.0`;
- exact root `LICENSE.md` contains the MIT License, copyright 2023 maxpowa;
- current CurseForge project surface also labels the project MIT;
- no separate source asset-license file was observed in the exact tree;
- no upstream code/assets/text are copied or adapted into Black Arcana.

## Remaining QA ceiling

Catalog closure does not prove source↔physical-JAR byte reproducibility, direct publisher-file hash equality with the physical artifact, runtime behavior of every Create filter consumer, custom datapack rarity/affix behavior, persisted-filter behavior across reload/restart, or full-modpack compatibility. Those remain fail-closed QA and do not create additional provider authority.