# Not Enough Glyphs 4.6.2 — source-delta authority audit

Status: `CURRENT PHYSICAL 4.6.2 / EXACT SOURCE-SEMVER PIN / REGISTRATION BLOB UNCHANGED FROM 4.6.1 / MOMENTUM DISABLE BLOB UNCHANGED / DEPLOYED SERVER CONFIG STILL MISSING`

## Current physical authority

Latest sibling modlist authority checked at `Gustavaopere/neoforge-rpg-skilltree@cd38efb9c1a888c86addace69876400cf8845908` identifies:

- JAR: `not_enough_glyphs-1.21.1-4.6.2.jar`;
- mod id: `not_enough_glyphs`;
- runtime/version line: `4.6.2`;
- CurseForge project/file: `1023517 / 8880291`;
- loader/game: NeoForge / Minecraft 1.21.1;
- release date recorded by the sibling dossier: 2026-09-14;
- physical-pack SHA-1: **not currently preserved in Black Arcana authority material**.

The sibling dossier contains one stale internal line that still says `Runtime: 4.6.1`; it is contradicted by the dossier's physical JAR/version header and its explicit 4.6.2 re-audit/update section. That stale line is not used as current authority.

## Exact public source pin

Official source repository:

`Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77`

At that commit, `gradle.properties` declares:

- `mod_version=4.6.2`;
- `mod_id=not_enough_glyphs`;
- `minecraft_version=1.21.1`;
- `ars_version=5.12.0.1368`;
- `sauce_version=0.0.50.97`.

This is an exact source-semver pin. It is not a byte-for-byte proof that the installed pack JAR equals a locally reconstructed build.

## 4.6.1 → 4.6.2 source delta

Historical 4.6.1 source pin:

`Alexthw46/NotEnoughGlyphs@2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b`

GitHub compare from that pin to 4.6.2 is three commits ahead and changes only seven files:

- `build.gradle`;
- `changelog.md`;
- `gradle.properties`;
- generated `en_us.json` / one generated cache entry;
- `AbstractEffectFilter.java`;
- `PropagateUnderfoot.java`.

Critically, the source files that define the catalog registration matrix and the special Momentum disable boundary are byte-identical across both pins:

- `src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java`
  - 4.6.1 blob SHA: `28c2007999ec6e534b8c5cd2c90b012c81072cff`;
  - 4.6.2 blob SHA: `28c2007999ec6e534b8c5cd2c90b012c81072cff`.

- `src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectMomentum.java`
  - 4.6.1 blob SHA: `7dd4f7ebe06cbadd282fddb1a6ca603013d2af2a`;
  - 4.6.2 blob SHA: `7dd4f7ebe06cbadd282fddb1a6ca603013d2af2a`;
  - the current source still explicitly returns disabled from its `isEnabled` override.

The registration file's optional-provider checks remain for `ars_elemental`, `toomanyglyphs`, `arsomega`, `ars_trinkets` and `ars_controle`.

## Registry consequence

Because the exact registration and Momentum source blobs are unchanged from the already-reconciled 4.6.1 pin, the current 4.6.2 source preserves the existing registration matrix:

- **40 NEG registrations** under the current pack's provider-presence conditions;
- **39 source-enabled candidates** before Ars/NeoForge SERVER config;
- `not_enough_glyphs:momentum` remains registered but provider-source-disabled;
- the four Ars Elemental objects referenced for documentation/listing remain Ars Elemental authority rather than NEG re-registrations.

No new registry enumeration is required solely for the 4.6.2 update.

## 4.6.2 behavioral delta — separate from registry count

The 4.6.2 source/release delta changes behavior rather than registration identity:

- filter/rune resolution hotfix;
- `Propagate Underfoot` vehicle targeting behavior;
- Sauce dependency line updated from the historical 0.0.42.89 line to source property `0.0.50.97`.

Those changes require runtime regression QA where relevant, but they do not alter the semantic registration denominator established by the unchanged registration source.

## Remaining semantic blocker

The catalog blocker remains the same type, but is now explicitly version-bound to 4.6.2:

- capture authoritative deployed SERVER/world config for the 39 source-enabled candidates;
- reconcile each effective `[general].enabled` value;
- do not substitute Ars source default `true` for the deployed state;
- keep Momentum excluded regardless of a hypothetical config value because the provider override remains source-disabled.

Until that deployed evidence exists, Not Enough Glyphs remains **⚠️ Parcial / condicionado** and contributes **+0** to the strict semantic total.

## Authority boundary

Ars Nouveau remains authority for glyph registration/config semantics and casting. NEG remains authority for its addon glyph implementations and SpellBinder/contingency systems. Sauce remains provider/library authority for its shared mechanics. Black Arcana does not recreate these runtimes or synthesize config values.
