# Ars Additions — Reach Perk

Status: `1/1 SOURCE-PINNED / RUNTIME STACKING QA PENDING`

- Registry id: `ars_additions:thread_reach`
- Display name: Reach
- Source class: `ReachPerk`

## Provider-native behavior

For the armor Thread slot value supplied by Ars Nouveau, Reach adds two item attribute modifiers:

- `Attributes.BLOCK_INTERACTION_RANGE`: `+slotValue` using `ADD_VALUE`;
- `Attributes.ENTITY_INTERACTION_RANGE`: `+slotValue` using `ADD_VALUE`.

The same provider registry id is used for the modifiers. The source description summarizes this as +1 interaction distance per level.

## Boundary

This is an Ars armor-perk modifier, not an RPG Skill Tree attribute grant. RPG/Black Arcana bridges must not re-add the same range merely because the Thread is equipped.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`ReachPerk`, `ArsNouveauRegistry`).
