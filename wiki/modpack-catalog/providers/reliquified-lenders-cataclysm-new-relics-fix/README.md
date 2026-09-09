# Reliquified L_Ender's Cataclysm — New Relics Fix 1.0.2

Status: `EXACT PHYSICAL+PUBLISHER RELEASE / COMPATIBILITY-BRIDGE COMPONENT / 5 EXISTING RELICS IN PUBLISHED SCOPE / 0 NEW SEMANTIC RELIC OR SPELL IDENTITIES PUBLISHED / SOURCE INTERNALS NOT LOCATED / RUNTIME QA FAIL-CLOSED`

## Installed identity

- physical JAR: `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`
- mod id: `reliquified_lenders_cataclysm_new_relics_fix`
- runtime: `1.0.2`
- Minecraft / loader: `1.21.1` / NeoForge
- physical SHA-1: `9d4710e665ec74af917bb9f5f819154ca9f74ca0`
- CurseForge project/file: `1665965 / 8778365`
- release date: `2026-08-31`
- publisher environment: Client & Server
- publisher license: All Rights Reserved
- provider class: `RELICS 0.10 → 0.12 COMPATIBILITY BRIDGE FOR RELIQUIFIED L_ENDER'S CATACLYSM`

Physical modlist/JAR metadata is authority for installed presence, mod id, runtime version and hash. CurseForge release metadata independently matches the physical filename/version and provides the public compatibility scope.

## What this component is

The publisher defines this mod as a compatibility bridge that lets Reliquified L_Ender's Cataclysm `0.1.1` continue to work with newer Relics `0.12` APIs on NeoForge 1.21.1. The original addon referenced Relics `0.10` classes/methods that were removed or changed.

The fix does **not** replace the original addon. It is installed alongside the original addon and its dependencies.

The public 1.0.2 changelog additionally states that the compatibility bridge was limited to the addon's base class, preventing global `RelicItem` modifications. This is a key ownership boundary: the fix adapts one addon family rather than becoming a general Relics runtime.

## Published functional scope

The exact 1.0.2 publisher surface lists eight fix families:

1. startup errors caused by removed `IRelicItem` API;
2. conversion of old relic definitions to the `RelicTemplate` system;
3. Curios integration and attribute modifiers;
4. stats, levels, ranks, cooldowns and experience;
5. legacy active ability behavior;
6. replacement of the removed player-motion network packet;
7. ability order and progression values;
8. descriptions and tooltips.

These are compatibility responsibilities. They do not create a second relic framework, progression ledger or network authority for Black Arcana.

## Five relics in exact published scope

The publisher names exactly five relics as fixed:

1. Void Cloak;
2. Scouring Eye;
3. Void Vortex in Bottle;
4. Vacuum Glove;
5. Void Bubble.

These identities belong to Reliquified L_Ender's Cataclysm. The fix adapts their behavior to the newer Relics API; it does not acquire ownership of the relic identities.

Catalog consequence:

- **0 new semantic relic identities are attributed to this fix**;
- **0 standalone spell identities are published for this fix**;
- the five names above are not counted again as provider-created capabilities.

This is a semantic publisher-surface result, not a source-registry count. Exact internal registrations, mixin classes and packet signatures are not available from a public exact-version source and remain unverified.

## Physical dependency stack

The current physical pack contains the published requirements:

- Relics `0.12.8` — `relics-1.21.1-0.12.8.jar`;
- Curios `9.5.1+1.21.1` — `curios-neoforge-9.5.1+1.21.1.jar`;
- OctoLib `0.6.2` — `OctoLib-NEOFORGE-0.6.2+1.21.jar`;
- L_Ender's Cataclysm `3.33` — `L_Ender's Cataclysm 1.21.1-3.33.jar`;
- Reliquified L_Ender's Cataclysm `0.1.1` — `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`.

Presence of the dependency stack is not proof that every bytecode transform, packet replacement or persistence path works correctly in the full modpack. Runtime correctness remains a separate QA gate.

## Authority model

- **Relics 0.12.8** owns RelicTemplate/framework semantics, rank/level/XP/cooldown infrastructure and provider framework state.
- **Reliquified L_Ender's Cataclysm 0.1.1** owns the five relic identities/content and their intended addon behavior.
- **L_Ender's Cataclysm** owns the underlying Cataclysm content from which the addon derives integration.
- **Curios** owns equipment-slot/equip-state infrastructure.
- **New Relics Fix 1.0.2** owns only the compatibility translation required for that addon to function against the newer Relics API.

The fix must not be treated as authority for Black Arcana casting, Corruption, Strain, Arcane Danger, rituals, hazards or world mutation.

## Black Arcana disposition

Black Arcana must not:

- create a second Relics 0.10→0.12 adaptation path for the same addon;
- duplicate rank/level/XP/cooldown mutation merely because the bridge exposes those compatibility concerns;
- re-run Curios attribute settlement for the same relic lifecycle;
- duplicate or reinterpret the provider's player-motion compatibility packet;
- count the five fixed relics as five new capabilities owned by the fix;
- infer exact mixin targets, transformation classes, packet types or serialization signatures that were not publicly exposed;
- copy or adapt implementation from an All Rights Reserved artifact;
- transfer Black Arcana magic runtime authority to RPG Skill Tree or any relic provider.

If Black Arcana later needs a real Relics integration, it must bind through verified current Relics/Curios contracts and preserve one owner for state mutation and progression settlement.

## Catalog files

- [COMPATIBILITY-BRIDGE-SURFACE.md](COMPATIBILITY-BRIDGE-SURFACE.md)
- [EVIDENCE-AND-PROVENANCE.md](EVIDENCE-AND-PROVENANCE.md)

## Evidence ceiling

Closed for catalog/deduplication:

- exact installed identity/version/hash;
- exact publisher project/file/release identity;
- publisher-declared bridge purpose and dependency family;
- exact five relics in public compatibility scope;
- exact eight public fix families;
- exact 1.0.2 scope restriction to the addon's base class rather than global `RelicItem` modification;
- provider authority and deduplication boundary;
- result that the fix adds no separately published semantic relic/spell identities.

Still fail-closed:

- exact source tree for fix 1.0.2;
- exact mixin count/classes/targets;
- exact bytecode transformer implementation;
- exact packet class/schema/direction/validation;
- exact persistence/migration keys;
- exact source↔physical-JAR reproducibility;
- full-pack dedicated-server, multiplayer, Curios modifier, rank/XP/cooldown and motion regression QA.
