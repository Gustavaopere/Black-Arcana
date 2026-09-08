# Provenance Delta — Phase 2X Ars Morph 2.0.0

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM / LICENSE METADATA DIVERGENCE`

## Installed identity

Physical modlist authority:

- provider: Ars Morph;
- mod id: `ars_morph`;
- JAR: `ars_morph-1.21.1-2.0.0.jar`;
- runtime version: `2.0.0`;
- SHA-1 / Modrinth hash: `68ff47cc58c0ffe9570bb907f65c2910311ed45f`;
- CurseForge hash: `1937242939`.

The physical modlist contains this JAR. A current Notion property says `Estado no pack: Removido`; physical presence wins and the property is treated as stale.

## Release-aligned source checkpoint

`Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`

Evidence:

- branch `1.21.1-v2`;
- commit date 2026-06-12;
- `gradle.properties` declares `mod_version=2.0.0`;
- publisher's 2.0.0 NeoForge 1.21.1 release is dated 2026-06-12.

This establishes release alignment, not cryptographic source↔binary equivalence. Phase 2X did not extract or rebuild/hash-compare the installed JAR.

## Build-host provenance

The source checkpoint was compiled against older host artifacts than the current pack, including Identity2 2.1.1.1 and Gabou's Libs 1.4. The physical pack contains Identity2 2.2.4 and Gabou's Libs 1.8.7.

The source build's CurseForge dependency coordinates are evidence about the development baseline, not a claim that those older artifacts are separately installed now.

## License discrepancy

At the exact source checkpoint:

- `src/main/resources/META-INF/neoforge.mods.toml` declares `GNU Lesser General Public License v3.0`;
- publisher project metadata also identifies LGPLv3;
- root `LICENSE` begins with GNU General Public License Version 3 text.

Phase 2X does not choose between the inconsistent repository license signals.

## Clean-room posture

Source is inspected read-only for factual interoperability data:

- registry identifiers;
- exact spell defaults and target-selection semantics;
- provider API calls;
- variant fields;
- ability assignments/cooldowns;
- data tags;
- source-risk hypotheses;
- authority and causal deduplication.

No upstream Java implementation, texture, model, animation, translation or other asset is copied/adapted into Black Arcana by Phase 2X.

Any future `DERIVED_CODE`/`DERIVED_ASSET` proposal remains fail-closed until the license discrepancy and exact notice/source obligations are resolved and recorded separately.
