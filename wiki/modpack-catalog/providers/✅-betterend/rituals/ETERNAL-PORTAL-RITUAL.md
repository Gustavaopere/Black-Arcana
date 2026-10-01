# BetterEnd 21.0.34 — Eternal Portal Ritual

Status: `1/1 COUNTED_EXACT`

## Identity

**Eternal Portal Ritual**

Provider owner: BetterEnd `EternalRitual` / Eternal Pedestal structure.

## Trigger and settlement

The exact installed artifact proves one player-facing causal ritual action:

1. valid portal-key items are placed on the Eternal Pedestals;
2. the provider links the pedestals into one Eternal Ritual and validates the portal structure;
3. every required pedestal must be active and use the same provider-accepted key item;
4. the provider resolves the destination from its portal map;
5. the server activates or generates the Eternal Portal and synchronizes provider ritual state.

This is one semantic ritual identity. Different configured key/destination entries are parameters of the same ritual and are not counted as separate spells/rites.

## Exact configuration behavior

BetterEnd reads `config/betterend/portals.json`.

The exact loader guarantees a non-empty portal map:

- missing file -> provider creates default;
- invalid top-level `portals` shape -> provider recreates default;
- empty portal array -> provider recreates default.

The exact default maps:

- destination: `minecraft:overworld`;
- key: `betterend:eternal_crystal`.

The current project evidence does not contain the deployed `betterend/portals.json`, so exact current custom destination/key values remain runtime/config QA. This does not make the ritual denominator unknown because the loader cannot retain an empty map.

## Catalog-level reachability

The exact artifact packages:

- Eternal Portal structure/worldgen resources;
- Eternal Pedestal control classes;
- `betterend:eternal_crystal` as one of the exact Infusion Ritual recipes.

State: **`COUNTED_EXACT`**.

Black Arcana must observe/deduplicate this provider action rather than implement a second portal ritual or second offering settlement.
