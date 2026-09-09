# Apothic Spawners 1.4.0 — Evidence and provenance

## Physical authority

Current physical modpack authority:

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- artifact `ApothicSpawners-1.21.1-1.4.0.jar`;
- mod id `apothic_spawners`;
- embedded/runtime version `1.4.0`;
- physical SHA-1 `b3be29751daea738e691db8949cce079e5aae3be`.

Presence/version/hash claims come from the physical inventory, not from publisher naming alone.

## Publisher evidence

Publisher surface identifies:

- CurseForge project `986583`;
- exact 1.4.0 file id `8469405`;
- NeoForge / Minecraft 1.21.1;
- release date 2026-07-20;
- official source repository `Shadows-of-Fire/Apothic-Spawners`.

The current project surface labels the project All Rights Reserved. That label is retained separately from source-code license metadata.

## Exact official source pin

The official repository keeps a dedicated `1.21` branch. Its commit history provides an exact release commit:

- release commit `d3bc0b40d46bee476fc770f8e4e44a1c35ecddd3`;
- commit message `1.4.0`;
- commit date 2026-07-20;
- release tree `7cd127fe22a9810b22bd8203cb2286d53b840e25`.

Immediate release lineage:

- parent `9b144c0ed58a7c0a83635b9a52653b1228844f55` — `The Nuclear Spawner`, explicitly a backport of the 26.1 feature;
- earlier `af8b7c4f8a5dd7915b18a0cdab7549f12b4f4ea2` — `Fix float comparisons`, explicitly a 26.1 backport.

The later `1.21` HEAD `fa52d69e86817a377116b669383703f8b6838f8a` is five commits ahead. Exact compare `d3bc...fa52...` changes only:

- added schema documentation files;
- Korean localization;
- Portuguese/Russian/Ukrainian localization corrections.

No Java, registry or gameplay datapack file changed after the release commit in that interval. Runtime inventory is therefore pinned to `d3bc...`, not silently sourced from the later branch head.

## Exact source metadata

At the 1.4.0 release source ceiling:

- mod version: `1.4.0`;
- Minecraft: `1.21.1`;
- Java: `21`;
- NeoForge baseline/range: `21.1.187` / `[21.1.187,)`;
- Placebo baseline/range: `9.9.0` / `[9.9.0,)`;
- generated license string: `MIT License`;
- mod description identifies the component as the spawner module allowing silk-touching and modification.

Physical NeoForge 21.1.248 and Placebo 9.9.2 satisfy the declared minimums. Satisfying ranges is not promoted to proof of full-modpack interoperability.

## Exact semantic inventory evidence

The release tree is `truncated=false` and closes the following provider surface:

- 27 Java files under the provider package;
- zero spell/glyph/ritual package or registration surface;
- exactly 16 `spawner_stat` registrations;
- exactly 32 stock modifier recipes: 16 direct + 16 inverse;
- one `spawner_modifier` recipe type and serializer;
- one Capturing enchantment-effect component;
- one spawner-modifier advancement trigger;
- one spawn-egg item-sub-predicate;
- one provider entity-type blacklist tag;
- one unstable-spawner loot table;
- exactly two common mixins, zero client mixins;
- five provider config values;
- one clientbound PLAY config-sync payload;
- explicit block-entity NBT persistence for custom stats, modified state, instability countdown and captured spawn data.

This evidence supports a complete provider-component closure with **0 standalone spells/glyphs/rituals**, not a claim that the physical JAR was decompiled or reproduced byte-for-byte.

## Exact 1.4.0 destructive-behavior evidence

The source closes bounded Nuclear Spawner constants and state:

- 60-tick instability;
- radius-8 provider explosion;
- 12 bounded mob spawn attempts;
- `apothic_spawners:gameplay/unstable_spawner` loot path;
- persisted instability state and captured spawn-data snapshot.

This is recorded because it affects Black Arcana world-effect causality. It is not copied into BA implementation.

## Authority/provenance interpretation

- Apothic Spawners owns the provider's spawner lifecycle and state transition once its own hooks are entered.
- Black Arcana owns whether a BA destructive world effect is permitted through `WorldEffectPolicy`.
- A provider reaction caused by an already-approved BA world effect is not processed a second time by BA.
- RPG Skill Tree receives no spawner tick/throughput authority from this catalog record.
- External spawner-machine or summon systems are separate providers and require their own evidence/contracts.

## Unproven / intentionally fail-closed

- source/JAR byte reproducibility;
- direct CurseForge-file hash equality with the physical artifact;
- full-modpack reload/event ordering;
- interaction with protection mods and alternate spawner implementations;
- external machine-spawner adapter behavior;
- future-version parity.

## Licensing / clean-room provenance

Observed license layers conflict for reuse purposes:

- root source code: MIT;
- generated source metadata: `MIT License`;
- source assets: All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

No reuse conclusion is inferred from this catalog. Source inspection is factual/read-only for interoperability and deduplication; Black Arcana does not copy provider code or assets.