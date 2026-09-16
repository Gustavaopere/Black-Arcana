# Backported Spellbooks — physical 0.1.2 release / embedded metadata 0.1.0

Status: `EXACT PHYSICAL ARTIFACT + EXACT PUBLISHER 0.1.2 RELEASE / RELEASE-DAY OFFICIAL SOURCE CEILING / 6 IRON'S SPELL REGISTRATIONS / 1 SCHOOL / CONTENT+WORLDGEN+EQUIPMENT PROCS / EMBEDDED VERSION MISMATCH PRESERVED / BYTE+FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `backportedspellbooks-0.1.2.jar`
- mod id: `backportedspellbooks`
- display name: `Backported Spellbooks`
- embedded/runtime metadata version: **`0.1.0`**
- physical SHA-1: `747847c1f38c73250ebac05ea06b41a381187850`
- Minecraft: `1.21.1`
- loader: NeoForge
- physical pack loader: NeoForge `21.1.248`

The filename/release label and embedded metadata disagree. This catalog preserves both layers and does not normalize one into the other.

## Publisher release identity

CurseForge project/file `1543731 / 8158731` publishes `backportedspellbooks-0.1.2.jar` for NeoForge 1.21.1 on 2026-05-28. The exact 0.1.2 changelog adds:

- Miasmic Staff;
- Quicksilver Spellbook;
- Slime Boots;
- four new spells: Slime Aspect, Sulfur Clouds, Sulfur Bomb and Sulfur Release;
- Corroded Fossils and Quicksilver ore content in Sulfur Caves.

The project page labels the distributed project MIT and server-side. The publisher description is older than the exact file changelog and is not used as a complete current inventory.

## Official source ceiling

Official repository: `RedReaper28/BackportedSpellbooks-1.21.1`.

The repository has no useful exact-version tag/release. Its terminal commit is `07cb65efca0c264762a21c2d6bce0f83e3947226`, dated 2026-05-28, the same calendar day as CurseForge file 8158731. That source still declares `mod_version=0.1.0`, matching the physical embedded metadata rather than the publisher filename.

The prior May 18 source point `4149c37c77dda46ab0a8697c438101e07ff14d19` exposes two spells. The May 28 source head exposes six. The four added spell registrations are the same four identities named as new in the 0.1.2 publisher changelog. This release-day source alignment is strong semantic evidence but is **not** promoted to byte-for-byte identity with the physical JAR.

## Semantic spell inventory

The release-day official source registers exactly six standalone Iron's `AbstractSpell` identities:

1. `backportedspellbooks:slime_aspect`
2. `backportedspellbooks:sulfur_bomb`
3. `backportedspellbooks:sulfur_clouds`
4. `backportedspellbooks:sulfur_release`
5. `backportedspellbooks:pale_thorn`
6. `backportedspellbooks:resin_spray`

It also registers one provider school: `backportedspellbooks:pale_flora`.

These are provider spell identities executed through Iron's spell infrastructure. Iron's remains authority for cast state, spell configuration plumbing, mana settlement, cooldown settlement and its network/runtime pipeline. Backported Spellbooks owns the semantic spell definitions and provider effects/projectiles/content attached to them.

Black Arcana must not copy the six spells into its own registry merely because their themes overlap BA domains, and it must not route BA-native casts through Iron's solely to inherit this addon.

## Closed provider surface at the source ceiling

Observed registrations/resources include:

- 6 spells;
- 1 school;
- 15 explicit non-block item registrations plus 4 block items = 19 item registry objects;
- 4 blocks;
- 5 entity types;
- 4 mob effects;
- 2 particles;
- 1 fluid and 1 fluid type;
- 19 recipe JSONs in the inspected source tree;
- 2 configured ore features, 2 placed ore features and 2 NeoForge biome modifiers;
- 0 mixin configurations;
- no provider custom payload registration observed;
- no provider-owned persistent player/world subsystem observed.

Asset-only names are not promoted to registry identities unless an actual registration surface exists.

## Worldgen boundary

Both exact biome modifiers target `minecraft:sulfur_caves` at `underground_ores`:

- `backportedspellbooks:corroded_fossil_ore_placed`;
- `backportedspellbooks:quicksilver_ore_placed`.

This agrees with the publisher's 0.1.2 note that the two ores appear in Sulfur Caves. Vanilla Backport remains authority for the referenced Sulfur Caves host content. Black Arcana must not synthesize that biome or substitute its own worldgen when the host is absent.

## Dependency evidence boundary

Exact source metadata formally declares only NeoForge `[21.1.216,)` and Minecraft `[1.21.1]` for the addon. However, the source directly imports and builds against Iron's Spells, Vanilla Backport and selected Ace's Spell Utils APIs; `build.gradle` also carries several development dependencies.

Therefore:

- Iron's / Vanilla Backport / Ace's are **source-level/build/runtime expectations observed in code**, not promoted into fabricated `neoforge.mods.toml` dependency declarations;
- physical presence of those providers is recorded separately;
- missing undeclared hosts must fail closed rather than being replaced by Black Arcana fallbacks.

## Equipment/proc boundary

Observed server-relevant provider behavior includes:

- Miasma Staff: post-damage proc that applies Sulfuric Poison for qualifying Nature/Hydro magic damage, with item cooldown handling;
- Garden Rapier: post-damage provider proc including a nature blastwave/Resin Poison path;
- Slime Boots: provider fall-event cancellation while equipped;
- Quicksilver Spellbook and Pale Guide Spellbook: Iron's spellbook objects whose attributes modify host casting/mana/stat surfaces.

These are provider equipment/proc semantics, not Black Arcana casts. BA Backlash or other BA damage must not be deliberately routed through these procs to create an offensive proc chain.

## Black Arcana authority result

Black Arcana retains its single server-authoritative cast pipeline, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.

Iron's retains its own casting/mana/cooldown runtime. Backported Spellbooks owns its addon spell/content identities and equipment procs. Vanilla Backport owns the referenced host content. Ace's owns its imported utility/attribute surfaces. RPG Skill Tree receives no magic-runtime authority from any of these relationships.

## Evidence ceiling / remaining QA

Still fail-closed:

- byte-for-byte source↔physical-JAR reproducibility;
- direct inspection/hash comparison of CurseForge file 8158731 against the physical JAR;
- physical-JAR class/resource parity with release-day source;
- runtime compatibility of source baseline NeoForge 21.1.216 / Iron's 3.15.4 against physical NeoForge 21.1.248 / Iron's 3.16.3;
- behavior if undeclared Vanilla Backport / Iron's / Ace's dependencies are absent or change API;
- full-modpack worldgen/recipe reload and server/client behavior;
- Slime Boots tooltip cooldown language versus the observed unconditional fall-event cancellation path;
- license reconciliation for reuse.

## License / clean-room

CurseForge labels the project MIT, while the release-day source `gradle.properties` declares `All Rights Reserved`. This conflict is retained. Source/data inspection is factual and read-only for cataloging/interoperability. No code, assets, models, textures, sounds or implementation are copied or adapted into Black Arcana.