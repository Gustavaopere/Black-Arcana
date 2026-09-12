# Provenance Delta — Phase 2BN Ars Sable 1.1.2

Status: `EXACT SOURCE-PINNED / LICENSE CONFLICT / CLEAN-ROOM`

## Physical identity

Current physical modlist authority:

- Ars Sable JAR `ars_sable-1.21.1-1.1.2.jar`;
- mod id/version `ars_sable` / `1.1.2`;
- SHA-1 `df43ad58fb9ca3b7acf7f62dc97ed75fd6da3da8`;
- CurseForge hash `2760241931`;
- current Sable host `sable-neoforge-1.21.1-2.0.5.jar`, mod id/version `sable` / `2.0.5`, SHA-1 `05f666e973d32baaaf405acb9bbed6615b909971`;
- current Ars Nouveau host `5.13.1`.

## Exact source

Official repository: `baileyholl/ars-sable`.

Exact installed-version checkpoint: `1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba`, whose source metadata declares `mod_version=1.1.2`.

Audited factual surfaces include `gradle.properties`, root `LICENSE`, NeoForge metadata, `ars_sable.mixins.json`, initializer/registry scaffolding, spatial persistence helpers, networking registrar and upstream GameTest surfaces.

## Dependency contract

Exact source declares/builds against:

- Minecraft `1.21.1`, runtime range `[1.20.6,1.21.2)`;
- NeoForge `21.1.219`, runtime range `[21,)`;
- Ars Nouveau build `5.11.7.1354`;
- Sable build `1.2.2`.

The physical pack uses Ars Nouveau `5.13.1` and Sable `2.0.5`. The source's broad dependency ranges do not establish binary or behavioral compatibility for its 29 direct mixin bindings.

## License-surface conflict

The same exact source revision exposes incompatible licensing signals:

- `gradle.properties`: `mod_license=LGPLv3`;
- root `LICENSE`: Unlicense/public-domain dedication text.

This audit does not choose one surface as a derivation grant. Classification is `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE CONFLICT / REVIEW_REQUIRED`.

Black Arcana uses the upstream source read-only for factual interoperability/catalog evidence only. No implementation body, assets, localization prose, models, sounds or other creative material are copied or adapted. Any future derivation would require a separate exact-license reconciliation and notice review.

## Evidence hierarchy

- physical modlist establishes installed identity/version/hash and current hosts;
- exact source establishes provider structure at 1.1.2;
- current Black Arcana `main` establishes implemented runtime authority;
- Notion/design material provides context but does not override physical/source/runtime evidence;
- no current-pack behavior is marked PASS without direct execution against the physical host versions.
