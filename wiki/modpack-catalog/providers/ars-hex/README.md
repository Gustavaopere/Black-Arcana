# Ars Hex 5.0.4b

Status: `PHASE 2W — SOURCE CATALOG CLOSED / INSTALLED RUNTIME + CONFIG QA OPEN`

## Exact installed identity

- Mod id: `ars_hex`
- Physical JAR: `ars_hex-1.21.1-5.0.4b.jar`
- Runtime version: `5.0.4b`
- Physical SHA-1: `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`
- Loader/game: NeoForge 1.21.1
- Pack NeoForge: `21.1.248`
- Phase 2 class: `ARS CROSS-PROVIDER BRIDGE / CONDITIONAL CONTENT PROVIDER`

Physical modlist/JAR identity is authoritative for installed presence/version. The current Notion row still says `Estado no pack: Removido`, while the physical modlist contains the JAR; Phase 2W therefore treats Ars Hex as installed and records the Notion property as stale.

## Release-aligned source checkpoint

Provider source used read-only:

`Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227`

This commit is dated 2026-01-01 and explicitly changes the source version from `5.0.4` to `5.0.4b` while retargeting the Malum compile seam. It is release-aligned with the public 5.0.4b file published on 2026-01-01. It is **not claimed byte-identical** to the installed JAR because Phase 2W did not extract/rebuild and compare the physical binary.

At this checkpoint `gradle.properties` declares:

- NeoForge `21.1.210`;
- Ars Nouveau `5.11.0.1267`;
- Sauce preferred `0.0.16.46`;
- Lodestone `1.8.3.549`;
- Malum `1.8.2.150`;
- Ars Elemental `0.7.6.12.117`;
- Iron's Spells `1.21.1-3.14.8`.

The physical pack instead contains Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1, Iron's 3.16.3, Lodestone 1.8.2 and Malum 1.8.2. The Ars Hex JAR itself also exposes nested Sauce 0.0.16.46 in the physical modlist. Source completeness therefore does not imply full-pack runtime compatibility PASS.

## Provider role

Ars Hex is not a new independent magic school. Its source bootstrap conditionally selects compatibility modules when the corresponding host mod is present:

- **Malum** — physically installed; the Malum module is selected by source bootstrap when Ars Hex initializes, but successful installed-runtime execution is still a QA gate;
- **Iron's Spells 'n Spellbooks** — physically installed; the Iron's module is likewise selected by source bootstrap, with current-host runtime behavior still unverified;
- **Hexerei** — support exists in source, but Hexerei is absent from the physical modlist, so its condition is not eligible in the current pack;
- **Ars Elemental/Sauce** — the exact source for the installed Ars Elemental version line implements the interface consumed by the Iron's bridge; installed interoperability remains runtime QA.

Each host retains authority over its own resource, attribute, spell or entity semantics. Ars Hex owns only the compatibility behavior it actually installs.

## Closed source catalog surface

### Malum-present / source-selected content

[`GLYPHS.md`](GLYPHS.md) closes the single registered Malum-backed glyph in the selected source path:

- `ars_hex:glyph_soul_shatter` / Soul Shatter — Tier II, 30 mana, source-default damage 5, Amplify increment 3, Amplify limit 2, Amplify/Dampen compatible, Malum `VOODOO` damage source, Necromancy school while Ars Elemental is loaded.

[`PERKS-EQUIPMENT.md`](PERKS-EQUIPMENT.md) closes:

- 3 Ars thread perks that directly project Malum/Lodestone attributes;
- Enchanter's Scythe as a Malum weapon + Ars caster tool;
- its 20%-per-Necromancy-part mana discount calculation;
- its provider-owned on-hit Ars spell execution and Malum scythe-boomerang/Reactive seam.

[`ACQUISITION.md`](ACQUISITION.md) records the five Malum-conditioned source recipes present in the release-aligned tree: one glyph recipe plus four Enchanting Apparatus recipes.

### Iron's-present / source-selected bridge

[`SYSTEMS.md`](SYSTEMS.md) records:

- Ars school → Iron school mapping;
- exact `SpellDamageEvent.Pre` multiplier path;
- Ars Elemental armor → Iron school-power modifiers;
- 5 Iron particle wrappers;
- COMMON config source defaults and the duplicate persisted config-key risk;
- the source path that reads general `SPELL_POWER` from the target when the general merge toggle is enabled.

### Hexerei dormant source surface

Hexerei is not installed. Source-only support is cataloged separately rather than counted as current runtime content:

- 3 conditional items;
- 1 conditional broom entity;
- 12 conditional particle wrappers;
- Mixing Cauldron/drying-rack/documentation/render integration;
- three Hexerei-conditioned manual recipes.

A fourth manual resource, `archwood_staff.json`, is conditioned on `hexcasting`, which is also absent from the pack. No Java registration for `ars_hex:archwood_staff` was located in the audited source checkpoint, so this is recorded as a dormant/orphan resource rather than provider content.

### Registries / mixins / networking

[`REGISTRIES.md`](REGISTRIES.md) separates source-eligible current-provider registries from dormant source registries. [`MIXIN-NETWORK-BOUNDARIES.md`](MIXIN-NETWORK-BOUNDARIES.md) records:

- `ars_hex.mixins.json` declares 0 common and 0 client mixins;
- no provider-owned custom payload registration was identified in the audited source;
- host networking/lifecycle behavior remains host-owned and is not reclassified as Ars Hex protocol.

## Critical deduplication consequences

Ars Nouveau owns Ars mana, spell recipes/context/resolver, glyph learning and thread/perk infrastructure. Malum owns spirits, Soul Ward, Spirit Spoils, its scythe/entity lifecycle and Malum damage types. Iron's owns its school-power/resistance/general spell-power attributes and Iron particles. Ars Elemental/Sauce owns its elemental armor school surface.

Black Arcana therefore must not:

- recalculate/reapply Ars Hex's Iron school-power/resistance bridge on the same Ars hit when that provider path is confirmed active;
- replay Soul Shatter damage or create a second spirit-reward settlement around the provider path;
- mirror Soul Ward, Spirit Spoils or Magic Proficiency into a second BA stat ledger;
- replay Enchanter's Scythe on-hit spell execution or Reactive/boomerang processing;
- infer that dormant Hexerei broom content is active merely because its classes/resources exist upstream.

Black Arcana remains authoritative for Black Arcana-owned casting, hazards, Corruption, Strain, Arcane Danger and world-safety contracts.

## Source risks carried into runtime QA

1. The provider was built against older Ars/Elemental/Iron's and a different Lodestone build line than the installed pack.
2. `IronsDamageBonusScaling` and `IronsSchoolDamageBonusScaling` are both constructed at the same persisted config path, `IronsDamageBonusScaling`; they cannot be treated as independently persisted settings without runtime/config evidence.
3. When the general Iron's merge is enabled, source reads general `SPELL_POWER` from the **target** living entity rather than the caster before multiplying Ars damage.
4. School-specific factors are applied once per mapped school in the preceding Ars spell part; multi-school parts therefore traverse the multiplier loop more than once.
5. Datagen declares damage/item/block tag bridges, but the release-aligned committed `src/generated/resources/data/ars_hex/` tree contains only recipes. Physical-JAR extraction is required before claiming those generated tag files are packaged.
6. Source dependency metadata does not list Iron's in `neoforge.mods.toml`, even though the code conditionally loads its bridge and the distribution page marks Iron's optional.

These are source observations/risk hypotheses. Phase 2W does not call them installed runtime failures without direct validation.

## Provenance

Code metadata and the root license both identify GNU LGPL v3. The root license additionally states that textures/models/assets are All Rights Reserved unless otherwise permitted. Phase 2W uses source read-only for factual interoperability/cataloging and copies/adapts no upstream implementation or assets.

See [`../../meta/PROVENANCE-DELTA-PHASE2W-ARS-HEX.md`](../../meta/PROVENANCE-DELTA-PHASE2W-ARS-HEX.md).

## Remaining validation

- extract/inspect the installed 5.0.4b JAR and compare packaged recipes/tags/config metadata against this source checkpoint;
- inspect the generated installed COMMON config and resolve the shared-key behavior;
- validate Ars 5.13.1 / Ars Elemental 0.7.10.1 / Iron's 3.16.3 / Malum 1.8.2 / Lodestone 1.8.2 interoperability;
- validate Soul Shatter damage/spirit consequences exactly once;
- validate all three thread modifiers in installed equipment;
- validate Enchanter's Scythe melee/boomerang/Reactive behavior and mana discount;
- validate Iron school damage/resistance and elemental-armor bridges without duplicate processing;
- verify no Hexerei/Hex Casting conditional registry/resource path activates in the current pack;
- dedicated-server/client/full-pack smoke.

None of these runtime/config checks are reported as PASS by this documentation checkpoint.
