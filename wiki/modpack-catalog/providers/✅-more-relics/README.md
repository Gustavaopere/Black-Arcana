# More Relics — 1.7.7-forRelics-0.12.8-1.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 29 RELIC OWNERS / 61 OWNER-SCOPED ABILITY ROOTS / COUNTED_EXACT / +61 STRICT / RUNTIME QA SEPARATE`

## Current physical authority

- JAR: `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`;
- mod id: `morerelics`;
- runtime: `1.7.7-forRelics-0.12.8-1.0`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `bc220ed291187c97bd1896f1fdd29b2377879ae1`;
- current base Relics: `0.12.8`.

Exact NON-MERGE audit #409 materialized CurseForge File `8859015` and hard-verified the same SHA-1. Physical↔publisher artifact identity is therefore **closed**.

## Provider role

More Relics owns the added relic identities, owner-scoped Relics abilities, evolution rules and provider-specific behavior. Relics owns the generic ability/progression framework. Black Arcana must not duplicate Relics/More Relics ability state, XP, evolution, cooldown or effect settlement.

## Exact semantic inventory

The hash-matched current artifact closes:

- **29** provider relic owners;
- **61** exact `AbilityTemplate.builder(...)` calls;
- **61/61** resolved ability roots;
- **61** independent owner→ability localization pairs;
- **56** unique root strings.

Owner-scoped counting is canonical for Relics. Reused strings under distinct relic owners are not collapsed. Consequently More Relics contributes **61**, not 56, semantic magic objects.

See:

- [`EXACT-1.7.7-REL0128-ARTIFACT-AUDIT.md`](EXACT-1.7.7-REL0128-ARTIFACT-AUDIT.md);
- [`ABILITY-INVENTORY-EXACT.md`](ABILITY-INVENTORY-EXACT.md).

## Reachability

The exact artifact exposes direct Relics `LootTemplate` routes for 20/29 ability-bearing relics. The current publisher inventory closes the remaining direct/evolution routes for the same content-locked 1.7.7 compatibility line, including the four documented evolution chains.

Catalog-level acquisition is therefore bounded for all 29 owners. Live loot/evolution behavior remains runtime QA rather than a semantic-inventory blocker.

## Semantic disposition

More Relics' owner-scoped Relics abilities are discrete provider-owned supernatural powers under the same metric already applied to Relics and the Reliquified addons.

**+61 `COUNTED_EXACT` semantic magic objects.**

Relic containers, rank/stat modifiers, UI indicators, loot entries, evolution container stages and downstream effects are not extra identities.

## Runtime QA remains separate

Still fail-closed:

- effective common/client config;
- loot injection in the final datapack stack;
- equip/unequip, death/respawn, relog/restart persistence;
- evolution state transfer exactly once;
- Twin Fangs reentrancy regression;
- Eject Button/Bionic Eye effective config;
- multiplayer/network prediction;
- Relics 0.12.8 compatibility under the assembled pack.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Current strict semantic contribution: **61 owner-scoped More Relics abilities**.