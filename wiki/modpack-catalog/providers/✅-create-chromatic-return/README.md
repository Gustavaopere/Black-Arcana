# Create: Chromatic Return — 1.0.4 / runtime metadata 1.0.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_ENCHANT_GEAR_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#175**;
- JAR: `createchromaticreturn-1.0.4-neoforge-1.21.1.jar`;
- mod id: `createchromaticreturn`;
- publisher/file label: `1.0.4`;
- embedded/runtime metadata: `1.0.0`;
- physical SHA-1: `be588d9e76ba1ce1a0556354c15fcc19d7fda133`.

The filename/publisher release and embedded metadata divergence is preserved intentionally.

## Exact artifact closure

NON-MERGE evidence PR **#530** audits CurseForge project/file `503784 / 8578225` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `d86a68780e02507a169aa5e6573e56c36dce3012`;
- exact-artifact run: `37012907385` — **SUCCESS**;
- evidence artifact: `11228870754`;
- evidence digest: `sha256:c05a202b0e60799931bf6c91dc4902e87f823ab3dcbaabcf508aac9857c6fedb`;
- publisher SHA-1: `be588d9e76ba1ce1a0556354c15fcc19d7fda133`;
- publisher SHA-256: `ae0042a1c10b5606ab2a9908465e058eecbaa1be2e7d98084886d8b73b846c67`;
- bytes: `285,356`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-1.0.4-ARTIFACT-AUDIT.md`](EXACT-1.0.4-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains **493 archive entries / 78 classes / 415 resources / 253 provider data JSONs**.

Archive/resource keyword scan closes:

- `spell = 0`;
- `magic = 0`;
- `ritual = 0`;
- `ability = 0`;
- `mana = 0`;
- `arcane = 0`;
- `glyph = 0`.

The artifact does contain charms, effects and three provider enchantments. Those surfaces were inspected directly rather than treated as zero merely from keyword absence.

## Three Infused Book application actions

The provider owns three deliberate item-enchantment application branches:

1. `createchromaticreturn:durasteel_book` + off-hand + crouch + valid tool -> consumes/replaces the infused book and applies `createchromaticreturn:durable`;
2. `createchromaticreturn:industrium_book` + off-hand + crouch + valid tool -> applies `createchromaticreturn:wrenching`;
3. `createchromaticreturn:silkstrum_book` + off-hand + crouch + valid tool -> applies `createchromaticreturn:super_silk_touch`.

All three books have exact provider-owned Create compacting acquisition recipes.

Under the canonical Black Arcana semantic metric, these are **enchantment-economy/application utilities**, not standalone spell/glyph/ritual/equivalent supernatural-action identities. This is consistent with Apothic Enchanting and Dis-Enchanting Table: applying or moving enchantments does not mint a spell identity.

## Charms and Creative Flight

The exact provider exposes charm equipment including Refined, Shadow, Industrium, Multiplite, Silkstrum and Antiplite surfaces. Their effects are driven by Curios equip/tick or inventory-tick state:

- speed/haste;
- strength;
- jump boost;
- Creative Flight / flight ability state;
- resistance/side-effect countering;
- charm-slot expansion.

These are passive/gear states. Creative Flight remains an equipment-granted mobility state, not a separate player-cast action.

## Other exact enchant/equipment effects

`durable`, `wrenching` and `super_silk_touch` remain provider-owned enchantments. Their downstream durability/block interaction effects are enchantment behavior and are not counted again.

Glow Saber/Glow Claws and other powerful tools remain weapons/tools; ordinary attacks, mining behavior, one-shot damage and material properties do not become magic identities merely because the items are powerful.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: Chromatic Return remains authority for alloys, charms, Curios behavior, enchantments, tool/weapon behavior, recipes, effects and Creative Flight settlement. Black Arcana records only semantic classification and must not replay enchant application or charm effects.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_ENCHANT_GEAR_INFRA`.**

Strict semantic delta: **+0**.
