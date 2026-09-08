# Provenance Delta — Phase 2V Ars Technica 2.7.6

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM / LICENSE METADATA DIVERGENCE`

## Installed identity

Physical modlist authority:

- provider: Ars Technica;
- mod id: `ars_technica`;
- JAR: `ars_technica-1.21.1-2.7.6.jar`;
- runtime version: `2.7.6`;
- SHA-1: `adb2641d538375f6eff6a22f0196bb330ab0b171`.

The physical modlist contains this JAR. A current Notion property says `Estado no pack: Removido`, while the same page's factual body identifies the physical 2.7.6 JAR. Under Black Arcana's authority rules the physical modlist wins for installed presence, so Phase 2V treats Ars Technica as installed and records the Notion property as stale rather than deleting the provider from the catalog.

## Provider source checkpoint

`zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`

At this checkpoint `gradle.properties` declares Ars Technica 2.7.6 for Minecraft 1.21.1 and pins its build dependencies to Ars Nouveau 5.11.0.1267 and Create 6.0.8.

Phase 2V uses this checkpoint to establish registry membership, spell-part defaults, acquisition datagen, mixins, configs, equipment/perk behavior and provider boundaries. This does not by itself cryptographically prove that every byte of the installed physical JAR was produced from this exact source revision; physical identity and source identity remain separately stated.

## Exact inherited Ars dependency

Ars Nouveau `5.11.0.1267` is publicly present in the upstream Maven line dated 2025-12-30. GitHub's successful `Build and Publish` workflow for upstream commit `f89dacc5d7467aae8497d98e95dad8347a8d7d21` starts at the corresponding publication time. Phase 2V uses that exact source revision only where the provider delegates behavior to the Ars API, notably `AbstractSpellPart.defaultTier() = SpellTier.ONE` for Ars Technica `Insert`.

The installed pack uses Ars Nouveau 5.13.1. Runtime compatibility with the newer host is a separate gate and is not inferred from source-version ranges.

## License discrepancy

At the exact Ars Technica checkpoint:

- `src/main/resources/META-INF/neoforge.mods.toml` declares `GNU Lesser General Public License v3.0`;
- root `LICENSE` contains GNU General Public License v3 text.

Phase 2V does not choose between these inconsistent license signals.

## Clean-room posture

The upstream source is used read-only to extract factual interoperability information:

- registry/content identifiers;
- provider/API relationships;
- configuration defaults;
- causal/resource ownership;
- finite spell/equipment/system behavior necessary for semantic deduplication;
- runtime-risk hypotheses that still require validation.

No upstream Java implementation, texture, model, translation, sound, animation or other asset is copied/adapted into Black Arcana by Phase 2V.

Any future source copying, derivative implementation or asset reuse remains fail-closed until the license discrepancy and applicable provenance obligations are resolved explicitly.

## Semantic-use boundary

Ars Technica may be used as evidence that a capability already exists in the installed ecosystem — for example magic→Create processing, Source→kinetics, provider-owned pressure/backtank integration or Transmutation Focus yield modifiers. That evidence can eliminate duplicate Black Arcana candidates, but it does not authorize code or asset reuse.