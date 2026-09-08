# Bubble

Status: `SOURCE-PINNED 5.13.1 / WATER CONTROL EFFECT`

- Registry id: `ars_nouveau:glyph_bubble`
- Display name: `Bubble`
- Default mana cost: `20`
- School: Elemental Water
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Bubble` creates a provider-owned `BubbleEntity`. On entity targets it immediately attempts to capture the target; on block targets it creates the bubble at the hit location.

Pinned defaults:

- base lifetime constructor term: `100 ticks`;
- Extend Time contribution: `3 ticks` per provider duration multiplier unit;
- base pop damage: `5.0`;
- Amplify contribution: `2.0`;
- default mana: `20`.

Compatible augments are Extend Time, Amplify, Dampen and Duration Down.

The bubble carries owner information for non-fake casters and controls captured-entity lift/pop behavior in its own entity runtime.

## Black Arcana boundary

Capture, lift, lifetime and pop damage are provider-owned settlement. Black Arcana must not register a second imprisonment state or apply duplicate pop damage. Any mastery/danger observation must preserve the original cast identity even when the bubble remains in-world after resolution.

## QA

Entity lifecycle behavior is source-pinned at the spell entry point; full `BubbleEntity` behavior and full-pack runtime interactions remain provider/runtime QA.