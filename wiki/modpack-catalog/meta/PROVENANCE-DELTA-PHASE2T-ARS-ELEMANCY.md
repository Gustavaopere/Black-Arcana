# Provenance Delta — Phase 2T Ars Elemancy 1.18.3

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM / LICENSE METADATA DIVERGENCE`

## Installed identity

- provider: Ars Elemancy;
- mod id: `ars_elemancy`;
- physical JAR: `ars_elemancy-1.21.1-1.18.3.jar`;
- runtime version: `1.18.3`;
- physical SHA-1: `f7e01437c86fc74e2abb2ad93554dc20c30b214b`.

## Source checkpoint

`Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`

The exact checkpoint's `gradle.properties` declares `mod_version=1.18.3` and Minecraft 1.21.1. The repository continued receiving commits while retaining the same mod version, so this is a semantic source checkpoint rather than cryptographic proof of the installed JAR build origin.

## License divergence

The root `LICENSE` is the text of **GNU General Public License v3**. The exact `src/main/resources/META-INF/neoforge.mods.toml` instead declares `GNU Lesser General Public License v3.0`.

Phase 2T does not choose between these inconsistent signals. Any future source copying, derivative code or bundled upstream assets requires explicit provenance/license resolution first.

## Clean-room posture

Source is used only to establish factual registries, recipes, behavior, version seams and authority boundaries. No source code, texture, model, translation, sound or other asset is copied/adapted into Black Arcana.

Shared provenance indexes are concurrent/high-churn surfaces; this narrow overlay is authoritative for the Phase 2T Ars Elemancy checkpoint until safe shared-index regeneration.