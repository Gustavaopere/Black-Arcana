# Transmutation Table — Item Transmutation

- Provider: **Alex's Mobs Continued** (`alexsmobs`)
- Version: `2.1.13`
- Exact physical/publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`
- Owner surface: `alexsmobs:transmutation_table`
- Semantic type: deliberate supernatural item-transmutation action
- State: `COUNTED_EXACT`

## Identity and trigger

The exact installed artifact exposes a direct player-driven Transmutation Table path:

- player opens the provider table/menu;
- an eligible input item is inserted;
- the provider exposes three current transmutation possibilities;
- the player selects one possibility;
- the selection reaches the server-side transmutation settlement.

This is one parameterized **Item Transmutation** identity. Inputs, three displayed candidates, rarity pools, XP amounts, rerolls and result items are parameters of this root rather than separate spell identities.

## Server settlement

Exact artifact evidence closes that the provider:

- replaces the input with the selected transmuted result;
- removes the configured XP-level cost;
- records the provider transmutation state;
- rerolls provider result state after settlement.

Black Arcana must not replay the result replacement or charge a second cost.

## Exact acquisition

The exact artifact contains the provider's shaped Transmutation Table recipe. The audited acquisition surface is sufficient for catalog-level owner reachability and does not inherit the Void Worm summon gate.

## Disposition

- exact action identity: closed;
- exact owner acquisition: closed at catalog level;
- strict state: `COUNTED_EXACT`;
- strict contribution from this root: **+1**.

## Evidence boundary

The provider remains authority for candidate generation, rarity pools, effective XP cost, reroll behavior, table state and result settlement. This card does not invent current tuning values.

Source: `../EXACT-2.1.13-ARTIFACT-AUDIT.md`.
