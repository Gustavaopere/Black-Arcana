# Apothic Enchanting 1.6.2 — Evidence and provenance

## Physical authority

Current physical modpack authority:

- Minecraft 1.21.1;
- NeoForge 21.1.248;
- 595 top-level entries;
- modlist SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- artifact `ApothicEnchanting-1.21.1-1.6.2.jar`;
- mod id `apothic_enchanting`;
- embedded/runtime version `1.6.2`;
- physical SHA-1 `2623af251d3ddeae1d8e710afa76afe753834bab`;
- physical Placebo 9.9.2;
- physical Apothic Attributes 2.10.1.

Presence/version/hash claims come from the physical inventory rather than publisher naming alone.

## Publisher evidence

Current publisher surface identifies:

- CurseForge project `1063926`;
- exact 1.6.2 file id `8797650`;
- file name `ApothicEnchanting-1.21.1-1.6.2.jar`;
- uploader `Shadows_of_Fire`;
- uploaded 2026-09-03;
- NeoForge / Minecraft 1.21.1;
- an accompanying sources JAR;
- current project license label All Rights Reserved.

The publisher label is retained separately from source-code and asset-license evidence.

## Exact official source pin

Official repository: `Shadows-of-Fire/Apothic-Enchanting`.

Exact 1.6.2 source:

- commit `00fbcf00a2f42701645daf8906e54f67ec65a5dc`;
- commit message `1.6.2`;
- commit date 2026-09-03;
- root tree `cad9b01b8d366e770cb811552884848afb320b30`;
- exact Java subtree `7f20d16f0d3f0c49caa1c5ae4582f88b22e8bd42`;
- recursive Java-tree inspection reports `truncated=false`;
- direct parent `78f3f0d00b85d4719169df3e5e62fa051e3fe72f`.

GitHub Releases is not used as release authority for this repository because the repository exposes no GitHub release objects; the exact version commit plus publisher file establish the pin.

## Exact source metadata

At the exact 1.6.2 commit:

- mod version: 1.6.2;
- Minecraft: 1.21.1;
- Java: 21;
- NeoForge baseline/range: 21.1.187 / `[21.1.187,)`;
- Placebo baseline/range: 9.9.0 / `[9.9.0,)`;
- Apothic Attributes baseline/range: 2.4.0 / `[2.4.0,)`;
- generated mod ID: `apothic_enchanting`;
- generated license string: `MIT License`.

The physical pack's NeoForge 21.1.248, Placebo 9.9.2 and Apothic Attributes 2.10.1 satisfy the declared minimums. This does not prove runtime compatibility beyond those range checks.

## Exact semantic inventory evidence

Exact source closes the following relevant provider surfaces:

- no standalone spell/glyph/ritual registration surface observed;
- no provider mana/cast resource observed;
- table statistics Eterna, Quanta, Arcana, clues, blacklist, treasure and stability;
- synced `apothic_enchanting:max_eterna` attribute;
- exactly 20 provider enchantment resource keys;
- public-package `EnchantableItem` and `EnchantmentStatBlock` interfaces;
- data-backed `EnchantingStatRegistry`;
- hard-cap IMC method `set_ench_hard_cap`;
- `infusion` and `keep_nbt_infusion` recipe serializers;
- persistent Raven-table stat attachment;
- four PLAY payloads: three clientbound and one serverbound;
- exactly 17 common + 3 client mixins in the generated required mixin manifest.

This closes provider identity/authority for catalog purposes without asserting binary reproduction of the physical JAR.

## Enchanting-stat evidence

`EnchantmentTableStats` stores:

- Eterna;
- Quanta;
- Arcana;
- clues;
- enchantment blacklist;
- treasure permission;
- stability.

The record clamps Eterna/Quanta/Arcana to 0..100 and clues to non-negative values.

`EnchantingStatRegistry` uses a data codec containing:

- `maxEterna`;
- `eterna`;
- `quanta`;
- `arcana`;
- `clues`.

`EnchantmentStatBlock` exposes block-side overrides for the same provider-owned table semantics plus blacklist/treasure/stability/particle behavior.

`EnchantableItem` exposes deterministic manipulation of the provider-selected enchantment list relative to the provided random seed.

## Exact enchantment-key evidence

`Ench.Enchantments` defines these 20 keys:

`berserkers_fury`, `boon_of_the_earth`, `chainsaw`, `chromatic`, `crescendo_of_bolts`, `endless_quiver`, `growth_serum`, `icy_thorns`, `infusion`, `knowledge_of_the_ages`, `life_mending`, `miners_fervor`, `natures_blessing`, `rebounding`, `reflective_defenses`, `scavenger`, `shield_bash`, `stable_footing`, `tempting`, `worker_exploitation`.

The exact bootstrap registers `infusion` with an empty item target set and zero costs. It remains provider infusion/table machinery, not a BA spell/ritual identity.

## Network and persistence evidence

Exact main-mod initialization registers:

- `CluePayload`;
- `StatsPayload`;
- `EnchantmentInfoPayload`;
- `SetRavenStatsPayload`.

Directions/versions:

- `apothic_enchanting:clue` — PLAY CLIENTBOUND, version `1`;
- `apothic_enchanting:stats` — PLAY CLIENTBOUND, version `1`;
- `apothic_enchanting:enchantment_info` — PLAY CLIENTBOUND, version `1`;
- `apothic_enchanting:set_raven_stats` — PLAY SERVERBOUND, version `1`.

The serverbound handler only acts when the player currently has `RavenEnchantmentMenu`. `RavenEnchantmentMenu` clamps Eterna against the player's provider `MAX_ETERNA`, and Quanta/Arcana to 0..100.

`RavenTableStats` is a serialized NeoForge attachment with integer Eterna/Quanta/Arcana fields constrained by codec to 0..100. It is provider persistence and is not mirrored in BA state.

## Enchantability discrepancy evidence

The exact changelog states:

- 1.6.1 changes Enchantability so it no longer gives Arcana and describes it as a chance to boost enchantment levels;
- 1.6.2 fixes star-prefixed level display and adds Raven-table JEI transfer support.

In the exact 1.6.2 `ApothEnchantmentHelper`, the observed +1-level branch is guarded by `rand.nextFloat() >= chance`.

This audit does not rewrite that expression into the changelog's prose and does not declare a physical runtime bug. Source↔physical-JAR equality is unproven, and no physical runtime reproduction was performed in this tranche. The discrepancy is therefore retained explicitly as QA/fail-closed.

## Authority/provenance interpretation

- Apothic Enchanting is authority for its enchanting-table/stat/selection/infusion/enchantment-effect runtime.
- Eterna/Quanta/Arcana remain provider statistics; the name `Arcana` does not transfer authority to/from Black Arcana.
- Black Arcana retains canonical casting and its own resources/state; it does not treat provider table controls as casting.
- RPG Skill Tree receives no direct enchanting-roll or provider-state mutation authority from this catalog record.
- Real integration should prefer provider extension/API/data/IMC seams and avoid private/internal/mixin coupling.

## Unproven / intentionally fail-closed

- source/JAR byte reproducibility;
- direct publisher-file hash equality with the physical artifact;
- full-modpack datapack reload and event ordering;
- physical runtime result of the Enchantability comparison;
- optional compatibility runtime paths;
- cross-mod behavior of provider mixins;
- binary stability of implementation classes outside explicit extension surfaces;
- future-version parity.

## Licensing / clean-room provenance

Observed license layers:

- root source code: MIT;
- generated source metadata: `MIT License`;
- exact `LICENSE_ASSETS`: Copyright 2024-2025 Stormraven Studios, LLC, All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

Black Arcana's `SOURCES.md` and `THIRD_PARTY_NOTICES.md` policy states that public source, installed artifacts and observable mechanics do not by themselves authorize copying. This audit is `REFERENCE_ONLY / COMPATIBILITY_TARGET` factual inspection. No provider code/assets/text are copied or adapted.
