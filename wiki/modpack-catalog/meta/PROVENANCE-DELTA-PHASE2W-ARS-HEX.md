# Provenance Delta — Phase 2W Ars Hex 5.0.4b

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM / RELEASE-ALIGNED SOURCE CHECKPOINT`

## Installed identity

Physical modlist authority:

- provider: Ars Hex;
- mod id: `ars_hex`;
- JAR: `ars_hex-1.21.1-5.0.4b.jar`;
- runtime version: `5.0.4b`;
- SHA-1: `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`.

The physical modlist contains this JAR. The current Notion row still exposes `Estado no pack: Removido`; under Black Arcana's source hierarchy that property is stale and does not override the physical artifact.

## Provider source checkpoint

Read-only upstream checkpoint:

`Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227`

Evidence for classification:

- commit date: 2026-01-01;
- exact diff changes `mod_version` from 5.0.4 to 5.0.4b;
- same commit retargets Malum API/build dependency to the 1.8.2 line;
- public 5.0.4b distribution file is dated 2026-01-01.

Phase 2W therefore calls this a **release-aligned source checkpoint**, not a cryptographic binary provenance proof. The installed JAR was not extracted/rebuilt and hash-compared to a build from this commit.

The Notion page uses later commit `a12bf191458f48ae0375d1e1073f24455f654416`, dated months after the release, while that later tree still carried the 5.0.4b version label. It remains useful as later maintenance context but is not used as the release-aligned code checkpoint for Phase 2W.

## Build/host baseline

At the release-aligned source checkpoint:

- NeoForge 21.1.210;
- Ars Nouveau 5.11.0.1267;
- Sauce preferred 0.0.16.46 with jarjar range `>=0.0.14.44` in build logic;
- Ars Elemental 0.7.6.12.117;
- Iron's 3.14.8;
- Lodestone 1.8.3.549;
- Malum 1.8.2.150.

The physical pack is newer/different on several hosts, so installed compatibility is separately gated. The physical Ars Hex row also shows nested Sauce 0.0.16.46, consistent with the source-preferred build line, but global jarjar selection across the full modpack is not inferred.

## License and asset boundary

At the exact checkpoint:

- `neoforge.mods.toml` declares `GNU Lesser General Public License v3.0`;
- root `LICENSE` contains GNU LGPL v3 text;
- the first line of the root license separately states that assets including textures/models are All Rights Reserved unless otherwise stated or explicitly permitted.

There is therefore no code-license contradiction recorded by Phase 2W, but code and assets do **not** share the same reuse posture.

## Clean-room posture

Upstream source is inspected read-only to extract factual interoperability information:

- registry/content identifiers;
- event/API relationships;
- configuration defaults/paths;
- acquisition recipes;
- provider authority/resource ownership;
- finite behavior needed for semantic deduplication;
- runtime-risk hypotheses.

No upstream Java implementation, texture, model, translation, sound, animation or other asset is copied/adapted into Black Arcana by Phase 2W.

Any future `DERIVED_CODE` use requires an explicit derivation record and LGPL obligations review. Any texture/model/other asset remains fail-closed under the upstream All Rights Reserved asset statement unless separate permission/license evidence exists.

## Datagen/package provenance boundary

The source registers datagen providers for cross-provider damage/item/block tags, but the committed release-aligned `src/generated/resources/data/ars_hex/` tree contains only recipes. Because the build includes generated resources but does not itself prove runData was executed before the public artifact was built, those intended tag files are not promoted to physical-JAR facts.

Physical JAR extraction is the correct next evidence source for this question.

## Semantic-use boundary

Ars Hex may be used as evidence that provider-native Malum/Iron's/Lodestone compatibility already exists — Soul Shatter, Ars thread attribute bridges, Enchanter's Scythe and Iron school damage/armor bridges. This can eliminate duplicate BA adapters but does not authorize source/asset reuse or transfer provider authority to Black Arcana.
