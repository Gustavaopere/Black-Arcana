# Not Enough Glyphs 4.6.2 — current source revalidation

Status: `CURRENT PHYSICAL 4.6.2 / EXACT PUBLIC SOURCE-SEMVER PIN / REGISTRY MATRIX PRESERVED / DEPLOYED SERVER CONFIG STILL MISSING / CONDITIONAL +0`

## Current physical authority

Latest sibling modlist checked:

- repository: `Gustavaopere/neoforge-rpg-skilltree`;
- checkpoint: `8211ce36e899cc8f55d24f937b0c7200fb0b3ae1`;
- installed filename: `not_enough_glyphs-1.21.1-4.6.2.jar`;
- mod id: `not_enough_glyphs`;
- runtime: `4.6.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- official CurseForge project/file: `1023517 / 8880291`;
- exact publisher-release SHA-1: `32eea2c478a346ee7499f6a0db156241116f73e9`;
- exact publisher-release SHA-256: `efd90f8ed292fd1b6b08fc33330f4344b70ed1661ffbe3684a64b1b485856c12`;
- embedded JarJar: `sauce-1.21.1-0.0.50.97.jar`;
- release date: 2026-09-14;
- license: LGPL-3.0.

The former physical `4.6.1` line and SHA-1 `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4` are historical only and must not be presented as the current installed artifact.

## Exact public source-semver pin

Repository: `Alexthw46/NotEnoughGlyphs`

Current 4.6.2 source checkpoint:

- commit: `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`;
- branch: `1.21`;
- `gradle.properties`: `mod_version=4.6.2`;
- Minecraft: `1.21.1`;
- NeoForge build dependency: `21.1.220`;
- Ars Nouveau source dependency: `5.12.0.1368`;
- Sauce source dependency: `0.0.50.97`;
- Ars Elemental source dependency: `0.7.9.4.170`;
- source license metadata: `LGPL`.

The current physical pack still uses Ars Nouveau `5.13.1`, so host config authority remains the separately audited exact Ars 5.13.1 contract. Source build dependencies are not substituted for physical host versions.

## 4.6.1 -> 4.6.2 source delta

The previous exact source-semver checkpoint was:

`2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b` — `mod_version=4.6.1`.

GitHub compare to 4.6.2 shows three commits and only these provider files changed:

- `build.gradle`;
- `changelog.md`;
- `gradle.properties`;
- generated language/cache data;
- `AbstractEffectFilter.java`;
- `PropagateUnderfoot.java`.

The canonical registration source file:

`src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java`

has the **same Git blob SHA** at both source pins:

`28c2007999ec6e534b8c5cd2c90b012c81072cff`.

The provider-disabled Momentum implementation:

`src/main/java/alexthw/not_enough_glyphs/common/glyphs/effects/EffectMomentum.java`

also has the **same Git blob SHA** at both pins:

`7dd4f7ebe06cbadd282fddb1a6ca603013d2af2a`,

and still overrides `isEnabled()` to return `false`.

Therefore the 4.6.1 source-level registration matrix is preserved by exact source identity across the 4.6.2 update. The 4.6.2 behavioral hotfixes do not add/remove registration entries in `ArsNouveauRegistry`.

## Current loaded-provider conditions

At sibling checkpoint `8211ce36e899cc8f55d24f937b0c7200fb0b3ae1`:

- Ars Elemental remains present;
- Ars Controle remains present;
- the current modlist tree has no provider entry for Too Many Glyphs, Ars Omega, Ars Trinkets or Ars Scalaes.

Combined with the byte-identical 4.6.2 registration source, the current-pack source-level result remains:

- **40 NEG registration primitives** under the current loaded-provider conditions;
- **39 source-enabled** before Ars/NeoForge SERVER config;
- `not_enough_glyphs:momentum` registered but source-disabled;
- four real Ars Elemental primitives delegated/referenced but not re-registered by NEG;
- Ars Controle Random fallback suppressed because Ars Controle is present.

This preserves the existing object-level `REGISTRATION-MATRIX.md`.

## Official 4.6.2 behavior delta

The official 4.6.2 release notes identify three material changes:

- hotfix for filters blocking resolve on runes after an API update;
- Propagate Underfoot can target the vehicle of the entity being resolved on;
- Sauce dependency updated to `0.0.50+`.

These changes affect behavior/dependency compatibility. They do not, by themselves, change the source-level registration count because the exact registration blob is unchanged.

## Remaining semantic blocker

The current 39 source-enabled rows still resolve through Ars Nouveau's per-spell-part SERVER config contract. Exact Ars Nouveau 5.13.1 authority remains:

- config type: `SERVER`;
- path family: `<namespace>/<path>.toml`;
- base key: `[general].enabled`;
- source default: `true`;
- effective deployed server/world value remains authoritative.

No current authoritative deployed `not_enough_glyphs/*.toml` / fallback-namespace serverconfig set is versioned in the project or sibling repository.

Therefore:

- 39 rows remain `CONFIG_CONDITIONAL`;
- Momentum remains `SOURCE_DISABLED`;
- Not Enough Glyphs remains **⚠️ Parcial / condicionado**;
- strict semantic delta remains **+0**;
- no technical component point is awarded.

## Exact 4.6.2 release audit

Temporary evidence PR #334 is intentionally non-merge.

- audit branch: `audit/not-enough-glyphs-4.6.2-release-2026-09-19`;
- exact audit HEAD: `a7b341505464998c37c1563668cc263e978b7c2c`;
- workflow run: `35443734628` — SUCCESS;
- audit artifact: `10585275563`;
- artifact digest: `sha256:6ceeeaf7805857537bbbf297a9dfe21ba9c363845d6fe7d0ff8ef00ebe1fb314`;
- release SHA-1: `32eea2c478a346ee7499f6a0db156241116f73e9`;
- release SHA-256: `efd90f8ed292fd1b6b08fc33330f4344b70ed1661ffbe3684a64b1b485856c12`;
- embedded Sauce JarJar path: `META-INF/jarjar/sauce-1.21.1-0.0.50.97.jar`;
- aggregate class count: `129`;
- aggregate `data/*.json` count: `61`.

The audit retained only hashes, metadata, embedded-JAR path/metadata and aggregate counts. It did not decompile provider classes.

## Release-byte boundary

The public 4.6.2 source pin is sufficient to revalidate the registration matrix because the relevant source blobs are exact and unchanged. It is **not** a claim that GitHub source commit `45604dd1...` is byte-for-byte identical to the installed physical JAR.

The exact publisher-release fingerprint is now retained. Physical-pack byte equality is still not proven because the current sibling modlist does not expose an independent SHA-1 for the installed 4.6.2 JAR. That equality is not required to preserve the source-level matrix, but it must not be invented.
