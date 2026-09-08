# Ars Nouveau — Interact

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_interact`
- Display name: Interact
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Sensitive, Amplify, Dampen
- Default augment limits: Sensitive 1, Amplify 1, Dampen 1

## Provider-native behavior

Interact emulates player interaction against blocks/entities. Sensitive selects off-hand interaction, Amplify switches block interaction to left-click/attack semantics, and Dampen performs shift-click semantics. Non-player/tile casting uses Ars' fake-player and inventory-manager path, including bucket handling and item return/drop behavior. Block use is denied by provider blacklist/claim checks before interaction.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:lever` + `#minecraft:wooden_pressure_plates` + `#minecraft:buttons`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this remote interaction/automation primitive. Black Arcana must not replay the interaction, duplicate inventory mutations or bypass provider/NeoForge interaction semantics when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInteract`).
