# Physical Magic Reconciliation — 2026-09-30

Status: `CURRENT CATEGORY-DIRECTORY AUDIT / 97 OF 97 MAPPED AFTER STARBUNCLEMANIA CLOSURE`

## Authority

- sibling: `Gustavaopere/neoforge-rpg-skilltree@d1659e7abadcf03c386d17b1886a473dc6541195`;
- Black Arcana base before correction: `bd1d66dafb5267d08535ad345c832746ff5ab1df`;
- physical taxonomy source: status-prefixed dossiers under `PROJECT-INSTRUCTIONS/modlist/`;
- classification rule: count a dossier when its **category directory** contains `Magic`; do not infer magic-provider status from the mod name alone.

## Coverage result

The current sibling contains **97 physical dossiers** in category directories containing `Magic`.

After ownership/alias normalization:

- 96 mapped to already-existing Black Arcana provider directories;
- 1 did not: `starbunclemania`;
- after this closure: **97/97 mapped**;
- no current physical Magic-category row remains structurally unmapped.

The old 84/84 result in the 27/09 reconciliation remains a valid historical checkpoint for the older sibling organization; it is not silently rewritten.

## Sole missing provider — StarbuncleMania 1.5.8

Sibling physical dossier:

- physical row: **#527**;
- JAR: `starbunclemania-1.21.1-1.5.8.jar`;
- mod id: `starbunclemania`;
- runtime: `1.5.8`;
- SHA-1: `6af8bc4f9dc24c9ff4d49367ca37fd914822ceb6`.

Exact clean-room audit in NON-MERGE PR #476:

- CurseForge project/file: `746215 / 8778598`;
- exact publisher SHA-1: `6af8bc4f9dc24c9ff4d49367ca37fd914822ceb6`;
- exact publisher SHA-256: `1a16c26278a047daba8dde122eb82def0dacdca3b4cdc4c0bd008e4ef664ac1e`;
- physical↔publisher SHA-1 equality: **true**;
- exact top-level provider glyph classes: **2**;
- exact provider glyph recipes: **2**;
- semantic denominator: **2**.

Exact identities:

1. `starbunclemania:glyph_place_fluid`;
2. `starbunclemania:glyph_pickup_fluid`.

Both are provider-owned Ars Nouveau `AbstractEffect` primitives, both are registered before the first branch in the exact provider registration method, and both have packaged recipes of type `ars_nouveau:glyph`. No third top-level provider glyph implementation class or glyph recipe exists in the exact JAR.

Evidence run: `36651810169`, job `109687424214`, text-only artifact `11070483445`, artifact digest `sha256:1715e89b256f4a7241bcb81492036f9cf6ed8b7c507fef5d49044fe784a04358`.

## Semantic and structural consequence

- StarbuncleMania: **+2 `COUNTED_EXACT`**;
- Ars ecosystem subtotal: **199 → 201**;
- strict reconstructible minimum: **1687 → 1689**;
- provider-directory tree: **115 → 116**;
- current directory state: **114 ✅ + 2 ⚠️**;
- remaining catalog-open providers: Iron's Spellbooks KubeJS and Traveloptics.

## Exclusions and authority

StarbuncleMania's Source/fluid automation, Starbuncle worker jobs, mounts and transport systems are not automatically extra semantic spell identities. They remain provider systems unless a separate discrete player-facing magical action is proven under the catalog metric.

Ars Nouveau remains authority for spell composition, mana/casting grammar and host glyph learning/config semantics. StarbuncleMania owns the two additional glyph identities and its automation systems. Black Arcana does not replay the provider effects or mint duplicate glyph identities.

The public `1.21` source branch currently contains later content and is not projected backward into physical 1.5.8. Exact File `8778598` is the authority for the counted denominator.
