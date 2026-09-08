# Scrying

Status: `SOURCE-PINNED 5.13.1 / DIVINATION RITUAL`

- Registry id: `ars_nouveau:ritual_scrying`
- Class: `RitualScrying`
- Completion threshold: `15` progress steps, advanced once per 20 server ticks
- Player application radius: `5` blocks
- Base duration: `60 × 20 × 5 = 6000 ticks` (5 minutes)
- Manipulation Essence multiplier: `×3` (15 minutes)
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native admission

The ritual requires at least one consumed item before start. It accepts:

- at most one Manipulation Essence as duration modifier;
- one target-defining item, either a BlockItem or an item matching a registered `ScryRitualRecipe`.

## Provider-native settlement

At completion, each `ServerPlayer` within radius 5 receives the Ars `SCRYING_EFFECT`. The ritual resolves its target as either:

- `TagScryer`, when the consumed item matches a registered scry ritual recipe; or
- `SingleBlockScryer`, when the target item is a block.

The selected `IScryer` is serialized into the player's persisted NBT under `an_scryer`, then synchronized to the client through the provider packet.

## Black Arcana boundary

Discovery/highlighting state and the serialized scry target remain Ars Nouveau authority. Black Arcana must not infer its own discovery ledger from nearby highlighted blocks or overwrite `an_scryer`.

Any Familiars & Divination integration should observe a supported provider state/hook rather than duplicating the scan/highlight system.

## QA

Source lifecycle is pinned to 5.13.1. Exact recipe-driven target coverage and client presentation in the full pack remain runtime/data QA.