# Ars Zero

Status: `PHASE 2AE — RELEASE-PINNED 2.0.2 / 12 CURRENT UNIQUE GLYPH CAPABILITIES NORMALIZED / MULTIPHASE + VOXEL + STATIC-STAFF SURFACES CATALOGED / EXACT BINARY INTERNALS FAIL-CLOSED`

## Runtime identity

- Mod id: `ars_zero`
- Current physical JAR: `ars_zero-1.21.1-2.0.2.jar`
- Runtime version: `2.0.2`
- Loader/game: NeoForge 1.21.1
- Physical SHA-1: `ac9b6e6f7a2bd403ee7cdc16023509fde7c4e1d0`
- CurseForge project: `1377482`
- CurseForge file: `8703997`
- Phase 2 class: `ARS GLYPH / CAST-DEVICE / WORLD-CAPABILITY PROVIDER`

The current 2026-09-08 physical modlist is authority for installed identity. The official 2.0.2 CurseForge file/release notes are the exact release-level functional authority available in this audit. The public upstream GitHub `1.21.1` branch is older than the 2.0.2 release and therefore is **not** treated as exact 2.0.2 source authority.

## Catalog result

Phase 2AE closes the currently public unique glyph capability surface at **12** entries:

1. Temporal Context Form;
2. Near Form;
3. Push;
4. Select;
5. Conjure Voxel;
6. Anchor;
7. Remove Gravity;
8. Convergence;
9. Geometrize;
10. Conjure Blight;
11. Beam;
12. Conjure Arcane Shield.

`AOE II`, `AOE III`, `Amplifier II` and `Amplifier III` remain disabled-by-default copied compatibility content in the public provider documentation and are not counted as unique Ars Zero gaps.

See [`GLYPH-CATALOG.md`](GLYPH-CATALOG.md) for the per-capability evidence/disposition matrix.

## Multiphase authority

Ars Zero already owns a real multiphase spell-device model around **Begin / Tick / End** phases:

- Spell Staff family: up to ten glyph slots per phase and continuous held-use casting;
- Psion's Circlet: Curios head device using the same three-phase model;
- Multi-phase Turret: block/turret execution of phase-aware spells.

The exact 2.0.2 release additionally documents server-side hardening around multiphase/parchment/circlet packet handling and live cast-context cleanup. Black Arcana must not create a second generic multiphase Ars execution path merely to observe or integrate these casts.

## Static staffs and acquisition

The exact NeoForge 1.21.1 2.0.2 changelog directly names five static staffs promoted to full production:

- Staff of Demonbane;
- Staff of Geometrize;
- Staff of Convergence / Explosion Arch Wizard;
- Staff of Lakes;
- Staff of Switcheroo.

That release makes those five Necropolis Lich-exclusive drops with no crafting recipes and connects them to Lich equipment, creative-tab registration, filial crafting inputs and protection upgrades.

Earlier official 2.0.x release material additionally documents **Staff of Telekinesis** and **Staff of Aetherwalk** as production static-staff lineage. Because the exact 2.0.2 file page does not re-enumerate those two by name, Phase 2AE records them as **lineage-supported**, not as direct exact-file inventory proof. Exact preset spell payloads, registry IDs, filial internals and item components remain unverified.

## World/system capabilities

Ars Zero also exposes provider-owned surfaces beyond glyph registration:

- elemental voxel entities with Arcane, Fire, Water, Wind, Stone, Ice and Lightning variants;
- voxel-vs-world and voxel-vs-voxel interactions;
- Blight liquid / Blight Forest content;
- Necropolis structure and Lich encounter/loot;
- Arcane Shield entity/barrier behavior;
- geometry-process lifecycle;
- Temporal Anchor state;
- bounded/protected world mutation for Conjure Blight and temporal restoration in the 2.0.2 release.

See [`SYSTEMS-AND-EQUIPMENT.md`](SYSTEMS-AND-EQUIPMENT.md).

## Deduplication impact

Ars Zero materially overlaps candidate Black Arcana capability families around:

- channelled / multiphase casting;
- geometry / patterned placement;
- gravity and forced movement;
- beam delivery;
- barriers/shields;
- persistent localized constructs;
- blight/corruption-like presentation;
- contextual selection/marking;
- source/mana concentration and environmental interactions.

These are overlap signals, not automatic semantic equivalence. In particular, Ars Zero Blight is **not** Black Arcana Corruption, Arcane Strain or Arcane Danger. A future bridge must preserve provider identity and causal ownership.

## Authority / fail-closed

- Ars Nouveau/Ars Zero own glyph execution, Ars mana/Source semantics and their cast-device lifecycle.
- Black Arcana retains authority over its own canonical casting pipeline, spell domains, Arcane Danger and world-safety policy.
- Never double-cast, double-debit mana/Source or convert an observed Ars Zero effect into a Black Arcana cast.
- Client packets/presentation are never promoted to gameplay authority.
- Geometry, temporal restoration and blight placement must not bypass provider claim/world-bound checks.
- No Mastery, Corruption, Strain or resource settlement is inferred from mere effect presence without a real causal adapter.
- Exact registry IDs, costs, formulas, configs and public API signatures that cannot be proven from exact 2.0.2 evidence remain `NÃO VERIFICADO` / fail-closed.

## Validation boundary

This is a documentation/audit closure, not runtime integration. No Black Arcana Stage 07 spell or Stage 08 balance decision is promoted by this catalog pass. Full binary extraction/runtime QA against the exact installed JAR remains pending.

## Evidence

- [`EVIDENCE-AND-PROVENANCE.md`](EVIDENCE-AND-PROVENANCE.md)
- Official project page: https://www.curseforge.com/minecraft/mc-mods/ars-zero
- Exact NeoForge 1.21.1 release: https://www.curseforge.com/minecraft/mc-mods/ars-zero/files/8703997
- Public upstream repository (historical source only for this release audit): https://github.com/zeroregard/Ars-Zero
