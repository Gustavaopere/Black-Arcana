# Provenance Delta — Phase 2U Ars Elemental 0.7.10.1

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM / LICENSE METADATA DIVERGENCE`

## Installed identity

- provider: Ars Elemental;
- mod id: `ars_elemental`;
- physical JAR: `ars_elemental-1.21.1-0.7.10.1.jar`;
- runtime version: `0.7.10.1`;
- physical SHA-1: `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.

The physical JAR/modlist is authority for installed presence/version/file identity.

## Source checkpoint

`Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`

The source checkpoint is used to establish provider registries, recipes, hooks, defaults and boundaries for the 0.7.10.1 catalog. Phase 2U does not claim cryptographic proof that the installed JAR was built from this exact commit.

## License discrepancy

At the exact checkpoint:

- repository README states the mod is licensed under LGPL v3;
- `src/main/resources/META-INF/neoforge.mods.toml` declares `GNU Lesser General Public License v3.0`;
- root `LICENSE` contains the text of GNU General Public License v3.

Phase 2U does not select between inconsistent license signals. Source copying, derivative implementation or bundled upstream assets require explicit license/provenance resolution first.

## Clean-room posture

The upstream source is used read-only for factual interoperability/catalog information. No Java implementation, texture, model, translation, sound, animation or other upstream asset is copied/adapted into Black Arcana by this phase.

Behavioral overlap informs Black Arcana differentiation, not code reuse.

## Shared-index policy

High-churn shared provenance indexes are not overwritten during concurrent work. This narrow overlay is the Phase 2U authority until a safe shared-index regeneration reconciles it.