# Ars Creo 5.4.0 — acquisition and player-facing entry points

Status: `SOURCE-PINNED DEFAULT DATA / EFFECTIVE DATAPACK QA PENDING`

Source checkpoint: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2`.

## Provider-owned acquisition

The exact 5.4.0 data tree contains one Ars Creo recipe:

### Starbuncle Wheel

Shapeless crafting:

- `ars_nouveau:starbuncle_charm`
- `create:water_wheel`
- result: `1 x ars_creo:starbuncle_wheel`

This is the only provider-owned item/block acquisition path found in `data/ars_creo/recipe` at the exact source checkpoint.

## Bridge surfaces do not create parallel acquisition

Spell turrets, Source Jars, Portal Blocks, Ritual Blocks, Potion Jars, Display Links/Boards and their normal acquisition remain owned by Ars Nouveau or Create. Ars Creo attaches behavior/capabilities/documentation to those provider objects; it does not register replacement copies.

`ArsNouveauRegistry.registerDocumentation` adds documentation entries for the Starbuncle Wheel plus Create Display Link/Board and Fluid Tank integration, but documentation registration is not a separate recipe or progression authority.

## Boundary

Black Arcana must not create a second unlock ledger for Ars Creo bridge behavior. Effective recipes/datapack overrides in the installed pack remain runtime QA rather than inferred source defaults.
