# Provenance Delta — Phase 2S Ars Creo 5.4.0

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM / LICENSE METADATA DIVERGENCE`

## Installed identity

- provider: Ars Creo;
- mod id: `ars_creo`;
- physical JAR: `ars_creo-1.21.1-5.4.0.jar`;
- runtime version: `5.4.0`;
- physical SHA-1: `22a6afd4fbe76354acc9c1ba076c89a94d120d94`;
- physical Ars Nouveau: `5.13.1`;
- physical Create: `6.0.10`.

## Source checkpoint

`baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`

The commit is titled `5.4.0`; its `gradle.properties` declares `mod_version=5.4.0`, Minecraft 1.21.1 and `mod_license=LGPLv3`. `neoforge.mods.toml` also says `license = LGPLv3`.

However, the exact root `LICENSE` file is the Unlicense text beginning with a public-domain dedication. Phase 2S does **not** choose between these inconsistent signals. License status is recorded as divergent and any future copying/derivation/bundling requires an explicit legal/provenance resolution.

## Clean-room posture

This phase uses source only to establish factual registry/runtime paths, provider authority, costs/resources, acquisition defaults and integration safety boundaries. No upstream source code, assets, models, textures, translations, sounds or animation data are copied/adapted into Black Arcana.

Matching source version and physical JAR version is not treated as cryptographic proof that the installed artifact was built byte-for-byte from this commit.

Shared provenance indexes are high-churn concurrent surfaces; this narrow overlay is authoritative for the Phase 2S Ars Creo checkpoint until safe shared-index regeneration.