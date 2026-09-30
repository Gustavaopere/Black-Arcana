# StarbuncleMania 1.5.8 — Exact Artifact Audit

Status: `EXACT PHYSICAL/PUBLISHER HASH MATCH / 2 GLYPHS / CLEAN-ROOM`

## Artifact identity

- physical JAR: `starbunclemania-1.21.1-1.5.8.jar`;
- physical SHA-1: `6af8bc4f9dc24c9ff4d49367ca37fd914822ceb6`;
- CurseForge project/file: `746215 / 8778598`;
- exact publisher SHA-1: `6af8bc4f9dc24c9ff4d49367ca37fd914822ceb6`;
- exact publisher SHA-256: `1a16c26278a047daba8dde122eb82def0dacdca3b4cdc4c0bd008e4ef664ac1e`;
- exact artifact size: `726074` bytes;
- physical↔publisher equality: **true**.

## Bounded registry result

The exact artifact contains exactly two top-level provider classes in its glyph package:

- `alexthw/starbunclemania/glyph/PlaceFluidEffect.class`;
- `alexthw/starbunclemania/glyph/PickupFluidEffect.class`.

Both class shapes extend Ars Nouveau `AbstractEffect`.

The exact provider registration method references both spell parts before its first conditional branch. Its registration helper delegates each admitted part to Ars Nouveau `GlyphRegistry.registerSpell(...)` and records the same part in the provider list. This closes provider-side registration admission for both glyphs as unconditional.

## Exact packaged glyph resources

Two and only two provider glyph recipe resources exist:

- `data/starbunclemania/recipe/glyph_place_fluid.json` → `starbunclemania:glyph_place_fluid` → type `ars_nouveau:glyph`;
- `data/starbunclemania/recipe/glyph_pickup_fluid.json` → `starbunclemania:glyph_pickup_fluid` → type `ars_nouveau:glyph`.

The exact artifact also packages one Ars Nouveau notebook glyph entry for each identity.

Result: **semantic denominator = 2**.

## Audit execution

- evidence PR: **#476** (`NON-MERGE`);
- workflow run: `36651810169`;
- job: `109687424214`;
- text-only artifact: `11070483445`;
- artifact digest: `sha256:1715e89b256f4a7241bcb81492036f9cf6ed8b7c507fef5d49044fe784a04358`.

PR #476 was intentionally closed without merge after evidence capture.

## Clean-room boundary

The durable audit retains only hashes, archive size, class/type identities, bounded registration ordering facts and exact resource/registry IDs needed for interoperability/cataloging. No upstream implementation body, assets or localization prose are retained.
