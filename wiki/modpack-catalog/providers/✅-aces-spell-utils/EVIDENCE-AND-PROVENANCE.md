# Ace's Spell Utils 1.2.7.2 — evidence and provenance

## Physical pack authority

Current physical artifact:

- `aces_spell_utils-1.2.7.2-1.21.1.jar`
- mod id `aces_spell_utils`
- runtime `1.2.7.2-1.21.1`
- SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`
- Minecraft 1.21.1 / NeoForge pack baseline `21.1.248`

The physical modlist/JAR metadata is authority for installed presence/version/hash.

## Publisher release pin

Current official release metadata identifies:

- CurseForge project `1299492`;
- file `8789930`;
- filename `aces_spell_utils-1.2.7.2-1.21.1.jar`;
- NeoForge 1.21.1 release;
- upload date `2026-09-02`;
- MIT license;
- client + server environment.

The exact 1.2.7.2 release notes describe the VFX update, `IKeepInventoryEntity`, phase/music interfaces, Evasive fix, and active/passive imbueable/preset-imbue mace support.

Publisher description classifies the project as an Iron's Spells 'n Spellbooks utility API and lists entity/item/attribute/school/VFX helper families rather than a standalone spell pack.

## Exact official source version pin

Official source repository:

`AceTheEldritchKing/Aces_Spell_Utils`

Inspected revision:

`a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`

At that immutable revision, `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `neo_version=21.1.230`;
- `neo_version_range=[21.1.186,)`;
- `mod_id=aces_spell_utils`;
- `mod_license=MIT`;
- `mod_version=1.2.7.2-1.21.1`;
- `irons_spells_version=1.21.1-3.11.0`;
- Curios build property `9.2.2`.

This is strong evidence that the source revision belongs to the exact published version line. It is **not** a cryptographic/source-reproducibility proof that the source tree is byte-for-byte identical to the physical CurseForge JAR.

## Source-derived catalog facts

At the exact version pin:

- no `registerSpell(...)` call was found;
- no Ace's Spell Utils standalone spell registry is present;
- 3 `SchoolType` registrations;
- 19 attributes;
- 3 school damage-type keys;
- 1 attachment type;
- 1 particle type;
- 14 tag contracts;
- 8 rarity enum extensions;
- 27 registered example items;
- 8 play-to-client payload registrations under optional protocol `4.0.0`;
- 2 required mixins;
- 5 common config entries;
- event-driven provider runtime for 11 attribute/proc families plus magic-gun casting helper, keep-inventory support and VFX maintenance.

## Dependency evidence layering

Public project metadata states Iron's Spells 'n Spellbooks as the host/required content. Source code directly imports Iron's and Curios APIs.

The source `neoforge.mods.toml` template itself only declares NeoForge and Minecraft dependency blocks. Therefore that template is not treated as a complete semantic list of the library's host/API requirements.

Current physical pack contains the required host stack, including Iron's Spells 'n Spellbooks `1.21.1-3.16.3`. Source was developed against Iron's `1.21.1-3.11.0`, so exact host-version behavior/API parity remains runtime QA rather than an inferred guarantee.

## Source naming anomalies preserved

Two source naming mismatches are deliberately not “cleaned up” into fabricated registry identities:

1. `ASSchoolRegistry.ABYSSAL` registers the ResourceLocation `aces_spell_utils:hydro`; catalog identity is Hydro.
2. publisher-facing current description calls the `ritual` school Occult, while exact source registry ID remains `aces_spell_utils:ritual`.

Similarly, config comments/keys mix whitelist/blacklist terminology while the runtime fields/tags are whitelist-oriented. Catalog records the actual identifiers and behavior boundary rather than renaming provider contracts.

## Clean-room / reuse

The project is publisher-declared MIT and source metadata also declares MIT. This catalog uses source inspection to establish registries, behavior and interop boundaries.

Black Arcana still does not wholesale transplant implementation. Reuse, if ever appropriate, must respect license notices, architecture authority, provenance and the stronger requirement that Black Arcana retain one canonical magic runtime rather than importing a competing pipeline.

## Runtime QA still required

Catalog closure does not assert:

- source↔physical JAR byte identity;
- successful direct adapter binding to internal classes on Iron's 3.16.3;
- absence of event-order conflicts with Apothic Attributes or other installed proc/attribute providers;
- exact combined Evasive result where source event + mixin paths coexist;
- safe adoption of `AbstractDomainEntity` for Black Arcana — adoption is explicitly rejected by architecture unless a future approved boundary says otherwise;
- full-modpack multiplayer/client VFX correctness.

These remain fail-closed integration/QA questions, not reasons to keep the semantic component inventory open.

## Closure rationale

For a library/API provider, “complete catalog” means the current provider's own registry identities and reusable/runtime capability surfaces are enumerated to the exact source-version evidence ceiling. It does not require inventing player spells that the provider does not register.

Ace's Spell Utils therefore qualifies for component closure with **0 standalone spells**, while retaining explicit runtime/integration QA gates.
