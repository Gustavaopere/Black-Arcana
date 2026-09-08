# Ars Nouveau — Interact

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_interact`
- Display name: Interact
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Sensitive, Amplify, Dampen
- Default augment limits: Sensitive 1, Amplify 1, Dampen 1

## Provider-native behavior

Interact emulates player interaction against blocks/entities. Sensitive selects off-hand interaction, Amplify switches block interaction to left-click/attack semantics, and Dampen performs shift-click semantics. Non-player/tile casting uses Ars' fake-player and inventory-manager path, including bucket handling and item return/drop behavior. Block use is denied by provider blacklist/claim checks before interaction.

## Authority / deduplication

Ars Nouveau owns this remote interaction/automation primitive. Black Arcana must not replay the interaction, duplicate inventory mutations or bypass provider/NeoForge interaction semantics when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInteract`).
